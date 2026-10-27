# Reproduction Fallbacks (Phase 1)

Use when no automated feedback loop can be built: specific hardware, production-only data, or interaction that cannot be scripted. Do not hypothesize or change code in the meantime (G1).

## Order of attempts

1. **Reproducing environment:** ask for access to one (staging, a copy of the environment, a container image).
2. **Captured artifact:** ask for redacted evidence from a real occurrence (logs, stack trace, network capture, crash dump, screenshot or recording, input file, configuration). Replay it as described in `feedback-loops.md`.
3. **Temporary instrumentation:** with the human's permission, add tagged logging that captures the state at the failure point on the next occurrence. Remove it in Phase 6.
4. **Human-in-the-loop protocol.**
   - Write numbered steps the human can follow exactly: one action per step, with the expected observation after each.
   - Ask for observations in a fixed form: step number, what happened, exact error text or value.
   - Change one variable per round and say which one.
   - Never ask for credentials, tokens, or personal data; ask for redacted values.
   - Turn each reply into the same pass/fail verdict a feedback loop would give; record every round in the investigation log.
   - Batch independent checks into one round to keep rounds few.

## Blocked message

Send when steps 1–4 fail or are refused, then stop:

```markdown
## Cannot build a feedback loop

- **Tried:** <what was attempted and the result>
- **Blocked by:** <the missing access, artifact, or permission>
- **Need:** <the smallest thing that would unblock the investigation>
```
