"""Verify local tracker status and its Git/PR evidence.

Usage:
    python "<script-path>" --project-root "<absolute-project-root>" --item "<item-id>"

Use the selected local work item's ID. Resolve placeholders before invoking.
Run with --help for candidate selection and required CI evidence options.
"""

from helpers.cli import main, verify

if __name__ == "__main__":
    raise SystemExit(main(verify))
