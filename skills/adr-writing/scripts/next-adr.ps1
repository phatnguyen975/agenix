<#
.SYNOPSIS
    Suggest the next ADR number and a filename slug for a given title.
    Windows version. For Linux/macOS, use the equivalent next-adr.sh instead.

.DESCRIPTION
    This script only PRINTS a suggestion. It never creates, writes, or modifies
    any file — the workflow always confirms the final path and content with the
    human before anything is written to disk.

    Logic matches next-adr.sh exactly: the next number is the highest existing
    "ADR-NNN-*.md" number in the target directory, plus one (not a plain file
    count, so it stays correct even if numbers are ever non-contiguous). The
    slug is the title lowercased, with every run of non a-z0-9 characters
    collapsed to a single hyphen, and leading/trailing hyphens trimmed.

.PARAMETER Title
    Required. The decision title. Expected to be plain ASCII (English) —
    matching the project's own ADR title convention. Non-ASCII characters are
    dropped during slugification, not transliterated.

.PARAMETER Directory
    Optional. Defaults to docs/adrs. Pass the project's actual ADR directory if
    it differs from the default.

.EXAMPLE
    ./next-adr.ps1 -Title "Use PostgreSQL for the order service"

.EXAMPLE
    ./next-adr.ps1 -Title "Adopt OAuth2 for service-to-service auth" -Directory "docs/adrs"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false, Position = 0)]
    [string]$Title,

    [Parameter(Mandatory = $false, Position = 1)]
    [string]$Directory = "docs/adrs"
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($Title)) {
    Write-Error 'Usage: next-adr.ps1 -Title "Decision title" [-Directory <path>]'
    exit 1
}

# --- Compute the next number, based on the highest existing ADR number ------
$nextNumber = 1
if (Test-Path -LiteralPath $Directory -PathType Container) {
    $max = 0
    Get-ChildItem -LiteralPath $Directory -Filter "ADR-*.md" -File -ErrorAction SilentlyContinue |
        ForEach-Object {
            if ($_.Name -match '^ADR-(\d{3})-.+\.md$') {
                $num = [int]$Matches[1]
                if ($num -gt $max) { $max = $num }
            }
        }
    $nextNumber = $max + 1
}
$padded = "{0:D3}" -f $nextNumber

# --- Warn on non-ASCII characters, same threshold as next-adr.sh ------------
if ($Title -match '[^\x00-\x7F]') {
    [Console]::Error.WriteLine("Warning: title contains non-ASCII characters; they will be dropped, not transliterated, which can produce a misleading slug. Prefer an ASCII (English) title, matching the project's own ADR title convention.")
}

# --- Slugify the title: lowercase, kebab-case, trimmed ----------------------
$slug = $Title.ToLowerInvariant()
$slug = [regex]::Replace($slug, '[^a-z0-9]+', '-')
$slug = $slug.Trim('-')

if ([string]::IsNullOrEmpty($slug)) {
    Write-Error "Could not derive a slug from the given title — it may contain no ASCII alphanumeric characters."
    exit 1
}

$filename = "ADR-$padded-$slug.md"

Write-Output "Next number : $padded"
Write-Output "Slug        : $slug"
Write-Output "Suggested   : $Directory/$filename"
