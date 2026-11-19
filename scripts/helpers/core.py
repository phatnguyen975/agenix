"""Strict input, contained paths and read-only Git access."""

import argparse
import json
import os
import re
import subprocess
from functools import cache
from pathlib import Path, PureWindowsPath
from urllib.parse import urlsplit


class Invalid(ValueError):
    """Input or evidence contradicts the expected contract."""


class Unavailable(Exception):
    """A prerequisite could not be evaluated."""


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Invalid(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def finite_number(value):
    number = float(value)
    if not -float("inf") < number < float("inf"):
        raise Invalid("Non-finite JSON number")
    return number


def strict_json(raw):
    try:
        return json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=unique_pairs,
            parse_constant=finite_number,
            parse_float=finite_number,
        )
    except Invalid:
        raise
    except (ValueError, RecursionError) as exc:
        raise Invalid("Expected strict UTF-8 JSON") from exc


def read_json(path):
    try:
        return strict_json(path.read_bytes())
    except OSError as exc:
        raise Unavailable(f"Cannot read {path.name}") from exc


def contained(root, relative, *, private=False):
    parts = relative.split("/")
    if (
        not relative
        or PureWindowsPath(relative).drive
        or any(
            part in {"", ".."}
            or part.endswith((" ", "."))
            and part != "."
            or any(ord(ch) < 32 or ch in '\\:*?"<>|' for ch in part)
            or re.fullmatch(
                r"(?:CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|(?:COM|LPT)[1-9\u00b9\u00b2\u00b3])",
                part.partition(".")[0].rstrip().upper(),
            )
            for part in parts
        )
    ):
        raise Invalid(f"Invalid relative path: {relative}")
    path = root.joinpath(*parts).resolve()
    if not path.is_relative_to(root):
        raise Invalid("Path escapes its root")
    if not private and any(
        part.casefold() in {".git", ".agenix"}
        for part in [*parts, *path.relative_to(root).parts]
    ):
        raise Invalid("Managed paths cannot access private project storage")
    return path


def https(value):
    try:
        url = urlsplit(value)
        return (
            url.scheme == "https"
            and bool(url.hostname)
            and url.username is None
            and url.password is None
            and not re.search(r"[\s\\\x00-\x1f]", value)
        )
    except ValueError:
        return False


def run(root, *argv):
    try:
        environment = {
            key: value
            for key, value in os.environ.items()
            if key.upper()
            not in {
                "GIT_DIR",
                "GIT_WORK_TREE",
                "GIT_INDEX_FILE",
                "GIT_COMMON_DIR",
                "GIT_NAMESPACE",
            }
        }
        environment.update(
            GIT_OPTIONAL_LOCKS="0",
            GIT_NO_REPLACE_OBJECTS="1",
            GIT_NO_LAZY_FETCH="1",
            GH_PROMPT_DISABLED="1",
        )
        result = subprocess.run(
            argv,
            cwd=root,
            env=environment,
            capture_output=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Unavailable(f"{argv[0]} could not be run") from exc
    if result.returncode:
        raise Unavailable(f"{argv[0]} {argv[1]} failed (exit {result.returncode})")
    return result.stdout


class Repository:
    def __init__(self, root):
        if not root.is_absolute():
            raise Invalid("Project root must be absolute")
        self.root = root.resolve()
        self.oid = cache(self.oid)
        self.tree = cache(self.tree)
        self.read_blob = cache(self.read_blob)
        actual = self.git("rev-parse", "--show-toplevel").decode("utf-8").rstrip("\r\n")
        if Path(actual).resolve() != self.root:
            raise Invalid("Project root must be the Git worktree root")
        object_format = self.git("rev-parse", "--show-object-format").strip()
        self.oid_length = {b"sha1": 40, b"sha256": 64}.get(object_format)
        if not self.oid_length:
            raise Unavailable("Unsupported Git object format")

    def git(self, *args):
        return run(self.root, "git", *args)

    def oid(self, value, kind):
        if not isinstance(value, str) or not re.fullmatch(
            rf"[0-9a-f]{{{self.oid_length}}}", value
        ):
            raise Invalid(f"Expected a full Git {kind} object ID")
        if self.git("cat-file", "-t", value).decode().strip() != kind:
            raise Invalid(f"Git object is not a {kind}: {value}")
        return value

    def tree(self, commit):
        return (
            self.git("rev-parse", f"{self.oid(commit, 'commit')}^{{tree}}")
            .decode()
            .strip()
        )

    def baseline(self, config):
        branch = config["default-branch"]
        ref = f"refs/remotes/origin/{branch}"
        self.git("check-ref-format", ref)
        expected = config["github-repo"]
        origin = self.git("remote", "get-url", "origin").decode().strip()
        match = re.fullmatch(
            r"(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)([^/]+/[^/]+)",
            origin,
        )
        if not match or match[1].removesuffix(".git").casefold() != expected.casefold():
            raise Invalid("origin does not match the configured GitHub repository")
        return self.oid(
            self.git("rev-parse", "--verify", ref).decode().strip(), "commit"
        )

    def snapshot(self, revision, path, kind="commit"):
        contained(self.root, path)
        return self.read_blob(revision, path, kind)

    def read_blob(self, revision, path, kind):
        entry = self.git(
            "ls-tree", "-z", self.oid(revision, kind), "--", f":(literal){path}"
        )
        if not entry:
            raise Unavailable(f"Path absent from Git snapshot: {path}")
        metadata = entry.split(b"\t", 1)[0].split()
        if metadata[:2] not in ([b"100644", b"blob"], [b"100755", b"blob"]):
            raise Invalid(f"Expected a regular file in Git snapshot: {path}")
        return self.git("cat-file", "blob", metadata[2].decode())


def parser(description):
    cli = argparse.ArgumentParser(description=description)
    cli.add_argument("--project-root", type=Path, required=True)
    return cli


def emit(function, args):
    try:
        result = function(args)
        code = result.pop("exit-code", 0)
    except (Invalid, Unavailable, OSError, RuntimeError) as exc:
        code = 2 if isinstance(exc, Invalid) else 3
        result = {
            "result": "invalid" if code == 2 else "unavailable",
            "detail": str(exc),
        }
    print(json.dumps(result, ensure_ascii=True))
    return code
