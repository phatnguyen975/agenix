#!/usr/bin/env python3
"""Ensure HANDOFF.md has its own entry in the target directory's .gitignore.

Usage:
    python ensure-gitignore.py [target-directory]
    python ensure-gitignore.py "path/to/project"
    python ensure-gitignore.py -- "-project"

The target defaults to the current working directory, not the script's directory.
It must already exist. Creates .gitignore if missing, or appends HANDOFF.md only
when no exact, case-sensitive whole-line entry exists. Wildcards, comments, and
negation rules are not evaluated as Git ignore patterns.

Existing bytes are preserved, including a UTF-8 BOM. New entries use CRLF when
already present in the file, otherwise LF. A missing final newline is supplied
before appending. Repeated runs do not rewrite the file once the entry exists.

Exit codes:
    0: entry created, appended, or already present (or --help)
    1: target is not a directory, or .gitignore cannot be read or written
    2: invalid command-line arguments
"""

import argparse
import codecs
import sys
from pathlib import Path

ENTRY = b"HANDOFF.md"


def ensure_gitignore(target_directory="."):
    """Ensure an exact entry exists; return 'created', 'appended', or 'unchanged'."""
    target = Path(target_directory)
    if not target.is_dir():
        raise NotADirectoryError(f"directory not found: {target}")

    gitignore = target / ".gitignore"
    try:
        content = gitignore.read_bytes()
    except FileNotFoundError:
        with gitignore.open("xb") as stream:
            stream.write(ENTRY + b"\n")
        return "created"

    # Ignore a UTF-8 BOM only for matching; never change the existing bytes.
    lines = content.removeprefix(codecs.BOM_UTF8)
    entries = (line.removesuffix(b"\r") for line in lines.split(b"\n"))
    if ENTRY in entries:
        return "unchanged"

    newline = b"\r\n" if b"\r\n" in content else b"\n"
    separator = newline if lines and not content.endswith(b"\n") else b""
    with gitignore.open("ab") as stream:
        stream.write(separator + ENTRY + newline)
    return "appended"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "directory", nargs="?", default=".", help="target project directory"
    )
    args = parser.parse_args(argv)
    directory = args.directory or "."
    try:
        status = ensure_gitignore(directory)
    except OSError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    gitignore = Path(directory) / ".gitignore"
    if status == "created":
        print(f"Created {gitignore} and added 'HANDOFF.md'.")
    elif status == "appended":
        print(f"Appended 'HANDOFF.md' to {gitignore}.")
    else:
        print(f"'HANDOFF.md' is already present in {gitignore} - no change made.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
