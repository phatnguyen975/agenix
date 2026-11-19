"""Validate managed project artifacts at an explicit stage.

Usage:
    python "<script-path>" --project-root "<absolute-project-root>" --stage "<stage>"
    python "<script-path>" --project-root "<absolute-project-root>" --stage "<stage>" --item "<item-id>"

Select the stage for the current gate. Supply the owning item ID when the stage
requires one. Resolve placeholders before invoking. Run with --help for options.
"""

from helpers.cli import main, validate

if __name__ == "__main__":
    raise SystemExit(main(validate))
