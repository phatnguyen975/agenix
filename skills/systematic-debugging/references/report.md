# Report (Phase 8)

The report is one self-contained HTML file per session, rendered from `assets/debug-report-template.html`. Several root causes go into one report.

## Setup question

Ask once, in the same message as the evidence table, before generating any report content. Reuse any path, filename, or language the human has already specified; ask only for missing details and explicit confirmation to create the report:

```markdown
## Report setup

- **Path:** <proposed path: `docs/debug-report-SLUG-YYYYMMDD.html`, or the project's documentation directory when it uses another>
- **Language:** <the language the project defines and where it is defined, or the question "Which language should the report use?">

Reply "approve" to confirm, or give another path, filename, or language. Reply "skip" for no report.
```

**Rules:**

1. Propose `docs/debug-report-SLUG-YYYYMMDD.html`; follow the project's documentation directory when it uses another one.
2. **Filename:** `debug-report-<slug>-<YYYYMMDD>.html`. The slug is 2–5 lowercase hyphenated words naming the symptom or area; an issue identifier, when one exists, comes first in the slug. The date is the report date.
3. **Language:** use the language the project defines (project instruction files, contribution guidelines, documentation conventions). Without such a rule, ask in this question; when the reply confirms without naming a language, use the language the human writes in and state it.
4. Use the path, filename, and language the human gives, exactly as given.
5. Generate the content once, then save the file immediately.
6. When the human declines or no human is reachable, write nothing; the evidence table remains.
7. Never overwrite an existing file without asking.

## Findings file

Create a temporary JSON file outside the project (or delete it afterwards). Start from `python scripts/render-report.py --example`. The script uses `assets/debug-report-template.html` by default when `--template` is omitted; pass `--template PATH` only when intentionally using a different template. The default is resolved relative to the script location, not the current working directory.

| Key             | Content                                                                                             | Required                |
| --------------- | --------------------------------------------------------------------------------------------------- | ----------------------- |
| `lang`          | Language tag such as `en` or `vi`                                                                   | Optional (default `en`) |
| `title`         | One line naming the symptom or area                                                                 | Yes                     |
| `date`          | `YYYY-MM-DD`                                                                                        | Optional                |
| `status`        | `resolved`, `mitigated`, or `unresolved`                                                            | Yes                     |
| `summary`       | Two to five sentences                                                                               | Yes                     |
| `symptom`       | `expected` and `actual` (required), `impact` (optional)                                             | Yes                     |
| `root_causes`   | List of `what`, `where`, `why`, `evidence` (all required) and `id` (optional)                       | Resolved                |
| `investigation` | List of `hypothesis`, `prediction`, `experiment`, `result` (`confirmed`, `refuted`, `inconclusive`) | Unresolved              |
| `fix`           | `description` (required) and `changes`: list of `path` and `summary`                                | Resolved, Mitigated     |
| `guard`         | `level` 1–5 (required), `description`, `before`, `after`                                            | Resolved                |
| `verification`  | List of `claim`, `command`, `output`, `verdict` (`pass`, `fail`, `not_run`)                         | Resolved, Mitigated     |
| `statistics`    | List of `metric`, `before`, `after`                                                                 | Optional                |
| `follow_ups`    | List of text items                                                                                  | Optional                |
| `appendix`      | `commands`: list of `command` and `exit_code`; `environment`: text                                  | Optional                |
| `empty`         | One reason sentence for every section without content                                               | When a section is empty |
| `labels`        | Translated titles for the report language                                                           | Non-English reports     |

**Content rules:**

- A section without content keeps its place and shows the reason from `empty`. Keys: `root_causes`, `investigation`, `fix`, `guard`, `verification`, `statistics`, `follow_ups`, `appendix_commands`, `appendix_environment`. `render-report.py` refuses a missing reason.
- Statistics contain only values taken from captured command output: reproduction rate before and after, test results against the baseline, benchmark measurements with the method, diff statistics. No estimates and no durations that were not measured.
- Evidence follows the rules in `closing.md`.
- Redact secrets and personal data before writing the file.
- Non-English reports: run `python scripts/render-report.py --labels`, translate every value, and put the result under `labels`. Commands, paths, identifiers, and tool output stay unchanged.

## Render

```bash
python scripts/render-report.py --input FINDINGS.json --output REPORT.html
```

| Exit code | Meaning                                                           | Action                                                                            |
| --------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| 0         | Written; with `--dry-run`, valid but not written                  | Tell the human the path only when a file was actually written                     |
| 2         | Invalid findings, template problem, usage error, or output exists | Fix what the message names; never add `--overwrite` without the human's agreement |
| 3         | Likely secret detected (nothing written)                          | Redact at the JSON paths listed, then rerun                                       |

Use `--dry-run` to validate and render without writing. A successful dry-run returns exit code 0 but creates no report file. The secret scan is pattern-based and does not replace the agent's redaction judgment. Do not commit the report unless the human asks.

## Manual fallback (no Python)

1. Copy `assets/debug-report-template.html` to the confirmed path.
2. Follow the GUIDE comment above each section, including its empty-section rule.
3. Apply the syntax, derived values, and examples in the overview GUIDE comment of the template exactly; change no markup, class name, order, or style.
4. Remove every GUIDE comment, marker comment, and double-brace token.
5. Check: all nine sections are present, each empty section shows its reason, all tokens/markers/GUIDE comments are removed, no external resources or user-provided scripts are present, and no secrets are exposed.
