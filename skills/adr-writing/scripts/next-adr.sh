#!/usr/bin/env bash
# next-adr.sh — suggest the next ADR number and a filename slug for a given title.
# Linux/macOS version. For Windows, use the equivalent next-adr.ps1 instead.
#
# This script only PRINTS a suggestion. It never creates, writes, or modifies any
# file — the workflow always confirms the final path and content with the human
# before anything is written to disk.
#
# Usage:
#   ./next-adr.sh "Decision title" [adr-directory]
#
# Arguments:
#   Decision title   Required. Expected to be plain ASCII (English) — matching
#                    the project's own ADR title convention. Non-ASCII characters
#                    are dropped during slugification, not transliterated.
#   adr-directory    Optional. Defaults to docs/adrs. Pass the project's actual
#                    ADR directory if it differs from the default.
#
# Output:
#   Next number, generated slug, and the suggested "<directory>/<filename>" path.

set -euo pipefail

TITLE="${1:?Usage: next-adr.sh \"Decision title\" [adr-directory]}"
DIR="${2:-docs/adrs}"

# --- Compute the next number, based on the highest existing ADR number ------
next_number=1
if [ -d "$DIR" ]; then
  max=0
  for f in "$DIR"/ADR-[0-9][0-9][0-9]-*.md; do
    [ -e "$f" ] || continue
    base="$(basename "$f")"
    num="${base#ADR-}"
    num="${num%%-*}"
    num=$((10#$num)) # strip any leading zeros safely before arithmetic
    if [ "$num" -gt "$max" ]; then
      max=$num
    fi
  done
  next_number=$((max + 1))
fi
padded=$(printf '%03d' "$next_number")

# --- Slugify the title: lowercase, kebab-case, trimmed ----------------------
if [ -n "$(printf '%s' "$TITLE" | LC_ALL=C tr -d '\0-\177')" ]; then
  echo "Warning: title contains non-ASCII characters; they will be dropped, not" >&2
  echo "transliterated, which can produce a misleading slug. Prefer an ASCII" >&2
  echo "(English) title, matching the project's own ADR title convention." >&2
fi

slug=$(printf '%s' "$TITLE" \
  | tr '[:upper:]' '[:lower:]' \
  | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//')

if [ -z "$slug" ]; then
  echo "Error: could not derive a slug from the given title — it may contain no" >&2
  echo "ASCII alphanumeric characters." >&2
  exit 1
fi

filename="ADR-${padded}-${slug}.md"

echo "Next number : ${padded}"
echo "Slug        : ${slug}"
echo "Suggested   : ${DIR}/${filename}"
