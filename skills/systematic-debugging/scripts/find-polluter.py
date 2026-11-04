#!/usr/bin/env python3
"""Find the test that leaves unwanted state behind.

Runs candidate tests one at a time and stops at the first test after which the pollution
is present. Pollution is either a path that must not exist (--pollution-path) or a check
command that must exit 0 (--check-command).

Usage:
  python find-polluter.py (--pollution-path PATH | --check-command "CMD")
                          [--glob PATTERN]... [--tests-file FILE] [--test TEST]...
                          [--cwd DIR] [--timeout SECONDS]
                          -- RUNNER [ARGS...] {test}

The literal {test} in any runner argument is replaced by the candidate test.
The runner's own exit code is reported but does not decide pollution.
The script never deletes pollution; remove it before the first run.

Exit codes: 0 no polluter found; 1 polluter found; 2 usage error or the pollution
was already present before any test ran.
"""

import argparse
import glob
import os
import shlex
import signal
import subprocess
import sys


def candidates(args):
    """Return a list of candidate test paths based on the given arguments."""
    found = []
    base = args.cwd or "."
    for pattern in args.glob or []:
        matches = glob.glob(os.path.join(base, pattern), recursive=True)
        found.extend(sorted(os.path.relpath(m, base) for m in matches))
    if args.tests_file:
        with open(args.tests_file, encoding="utf-8") as handle:
            found.extend(
                stripped
                for line in handle
                if (stripped := line.strip()) and not stripped.startswith("#")
            )
    found.extend(args.test or [])
    seen, ordered = set(), []
    for item in found:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def run(argv, cwd, timeout):
    """Run a command; return its exit code, or "timeout" after killing its process tree."""
    try:
        if os.name != "nt":
            proc = subprocess.Popen(
                argv,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                errors="replace",
                start_new_session=True,
            )
        else:
            proc = subprocess.Popen(
                argv,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                errors="replace",
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            )
    except OSError as exc:
        return f"not started: {exc}"
    try:
        proc.communicate(timeout=timeout)
        return proc.returncode
    except subprocess.TimeoutExpired:
        try:
            if os.name == "nt":
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                    capture_output=True,
                    check=False,
                )
            else:
                os.killpg(proc.pid, signal.SIGKILL)
        except (OSError, ProcessLookupError):
            proc.kill()
        proc.communicate()
        return "timeout"


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--pollution-path", help="path (relative to --cwd) that must not exist"
    )
    parser.add_argument(
        "--check-command", help="command that exits 0 while state is clean"
    )
    parser.add_argument(
        "--glob", action="append", help="glob of candidate tests (repeatable)"
    )
    parser.add_argument("--tests-file", help="file with one candidate test per line")
    parser.add_argument("--test", action="append", help="candidate test (repeatable)")
    parser.add_argument("--cwd", default=None, help="current working directory")
    parser.add_argument(
        "--timeout", type=float, default=None, help="per-test timeout in seconds"
    )
    parser.add_argument(
        "runner", nargs=argparse.REMAINDER, help="runner command after --"
    )
    args = parser.parse_args()

    runner = args.runner[1:] if args.runner[:1] == ["--"] else args.runner
    if not runner or not any("{test}" in part for part in runner):
        parser.error("a runner command containing {test} is required after --")
    if bool(args.pollution_path) == bool(args.check_command):
        parser.error("give exactly one of --pollution-path or --check-command")
    cwd = args.cwd or os.getcwd()

    check = None
    if args.check_command:
        try:
            check = shlex.split(args.check_command, posix=(os.name != "nt"))
        except ValueError as exc:
            parser.error(f"invalid --check-command: {exc}")
        if not check:
            parser.error("--check-command must not be empty")

    try:
        tests = candidates(args)
    except OSError as exc:
        parser.error(f"cannot read tests file {args.tests_file!r}: {exc}")
    if not tests:
        parser.error("no candidate tests found")

    def pollution_status():
        if args.pollution_path:
            return os.path.lexists(os.path.join(cwd, args.pollution_path))

        result = run(check, cwd, args.timeout)
        if isinstance(result, str) and result.startswith("not started:"):
            return result
        # A non-zero exit or timeout means the checker did not confirm clean state.
        return result != 0

    status = pollution_status()
    if isinstance(status, str):
        print(
            f"error: cannot start --check-command: {status.removeprefix('not started: ')}",
            file=sys.stderr,
        )
        return 2
    if status:
        print(
            "error: pollution is already present before any test ran; "
            "remove it and run again",
            file=sys.stderr,
        )
        return 2

    for position, test in enumerate(tests, 1):
        argv = [part.replace("{test}", test) for part in runner]
        code = run(argv, cwd, args.timeout)
        if isinstance(code, str) and code.startswith("not started:"):
            print(
                f"error: cannot start runner for test {test!r}: "
                f"{code.removeprefix('not started: ')}",
                file=sys.stderr,
            )
            return 2

        status = pollution_status()
        if isinstance(status, str):
            print(
                f"error: cannot start --check-command: "
                f"{status.removeprefix('not started: ')}",
                file=sys.stderr,
            )
            return 2
        if status:
            print(
                f"[{position}/{len(tests)}] {test} ... POLLUTES (runner exit code: {code})"
            )
            print(f"polluter: {test}")
            print("the pollution was left in place for inspection")
            return 1
        print(f"[{position}/{len(tests)}] {test} ... clean (runner exit code: {code})")
    print(f"no polluter found among {len(tests)} tests")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(1)
