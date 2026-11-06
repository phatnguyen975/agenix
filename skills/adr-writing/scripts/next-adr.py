#!/usr/bin/env python3
"""Suggest the next ADR number and a filename slug without writing any files.

Usage:
    python next-adr.py "Decision title" [adr-directory]
    python next-adr.py -- "--Decision title starting with a dash"

Arguments:
    title          Required. Prefer an ASCII (English) decision title.
                   Non-ASCII characters become separators, not transliterations;
                   a warning is printed to stderr when any are present.
    adr-directory  Optional. Defaults to docs/adrs, relative to the current
                   working directory, not this script's directory.

Only immediate files named ADR-NNN-<slug>.md are counted (case-sensitive, at
least three ASCII digits). The next number is the highest number plus one,
or 001 if none match or the directory does not exist. Numbers are padded to at
least three digits and continue beyond 999: 999, 1000, 1001, and so on.

Output: next number, lowercase ASCII kebab-case slug, and suggested path.
The directory is never created and existing files are never modified.

Exit codes:
    0: suggestion printed (or --help)
    1: title has no ASCII alphanumeric characters, or directory cannot be read
    2: invalid command-line arguments
"""

import argparse
import re
import sys
from pathlib import Path

ADR_NAME = re.compile(r"ADR-([0-9]{3,})-.+\.md", re.DOTALL)
ASCII_LOWER = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")


def next_number(directory):
    """Return max matching ADR number + 1; ignore subdirectories and other names."""
    directory = Path(directory)
    if not directory.is_dir():
        return 1

    maximum = 0
    for entry in directory.iterdir():
        match = ADR_NAME.fullmatch(entry.name)
        if match is not None and entry.is_file():
            maximum = max(maximum, int(match.group(1)))
    return maximum + 1


def slugify(title):
    """Lowercase ASCII letters, collapse other runs to '-', and trim both ends."""
    slug = re.sub(r"[^a-z0-9]+", "-", title.translate(ASCII_LOWER)).strip("-")
    if not slug:
        raise ValueError(
            "could not derive a slug from the given title; "
            "it may contain no ASCII alphanumeric characters."
        )
    return slug


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("title", help="decision title (prefer ASCII English)")
    parser.add_argument(
        "directory",
        nargs="?",
        default="docs/adrs",
        help="ADR directory (absolute, or relative to the current working directory)",
    )
    args = parser.parse_args(argv)

    if any(ord(char) > 127 for char in args.title):
        print(
            "Warning: title contains non-ASCII characters; they are replaced with "
            "separators, without transliteration. Prefer an ASCII (English) title "
            "to avoid a misleading slug.",
            file=sys.stderr,
        )

    directory = args.directory or "docs/adrs"
    try:
        number = next_number(directory)
        slug = slugify(args.title)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    padded = f"{number:03d}"
    print(f"Next number : {padded}")
    print(f"Slug        : {slug}")
    print(f"Suggested   : {directory}/ADR-{padded}-{slug}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
