# Systematic Debugging Evaluation

## Purpose and Scope

Evaluate empirical diagnosis, repair authority, honest outcomes and helper command contracts. Development-only resources are independent of runtime use. Deterministic helper tests use disposable fixtures; behavioral cases use frozen observations, not live product execution.

## Files and Execution Status

| Resource                             | Role                                              | Status                                                      |
| ------------------------------------ | ------------------------------------------------- | ----------------------------------------------------------- |
| [check_helpers.py](check_helpers.py) | Standard-library helper CLI regression tests      | Ten isolated tests executed successfully                    |
| [scenarios.json](scenarios.json)     | Three behavioral inputs and semantic rubrics      | Three fresh-context runs; one targeted corrective follow-up |
| Behavioral runner / grader           | Deliver input and assess actual responses/actions | No checked-in model runner, grader or CI job                |

No new runtime helper or dependency is added. The scenario format is local, not an upstream harness contract.

## Coverage

| Layer                 | Evidence                                                                                                              | Limits                                                                                |
| --------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Repeat CLI            | Success, indexed parallel failures, stop-on-fail, timeout, invalid input and missing executable                       | No descendant-process cleanup failure simulation or large-output stress               |
| Polluter CLI          | Detection/evidence retention, clean state with failed runner, initial pollution, quoted check path and missing runner | No full order-bisection or non-filesystem state matrix                                |
| Standalone diagnosis  | `diagnosis-only-confirmed`                                                                                            | Known cause with unfixed candidate; supplied controlled observations                  |
| Caller composition    | `composed-authorized-repair-plan`                                                                                     | Reused bounded permission, existing red guard, deferred publication; next action only |
| Missing prerequisites | `missing-reproduction`                                                                                                | Rejects unsupported cache diagnosis and requests redacted evidence                    |

No installed-host discovery/non-trigger, full autonomous repair cycle, saved Markdown report, mitigation execution, prolonged multi-cause investigation, repeated-run reliability or multi-OS proof is established. No executable line-coverage percentage applies to instruction files.

## Execution

Run deterministic checks from the repository root:

```text
python -B evals/systematic-debugging/check_helpers.py
```

The script invokes only the two helper CLIs with synthetic Python commands in disposable directories, including paths containing spaces. It does not run helpers against the real repository or access network, secrets or Git. Keep generated state isolated; helper output is unredacted and must be inspected before sharing. Windows termination uses the helper's existing process-tree mechanism.

For behavioral cases, supply a fresh context with the runtime skill path and one raw input. Hide rubrics, other cases and coordinator conclusions. Allow only runtime-resource reads; prohibit execution, writes, network, Git, secrets, installation and further delegation. Capture actual responses/actions. Supplied fixture observations establish only their declared facts; the candidate must not claim to have executed them.

## Assessment

Deterministic assertions check exit codes, measured run counts/rates, timeout/stop behavior, retained pollution evidence and correct handling of a quoted checker path. They do not assert a preferred implementation.

Semantic review requires expected behavior, no prohibited action and the quality criterion. Check causal mechanism and discriminating experiment, repair authority, red/green provenance, accurate unresolved state and actionable missing evidence. Assess claims separately from process exit codes: a red pre-fix check can support successful reproduction. Keyword presence alone is not a pass. Distinguish infrastructure errors, unrun checks and uncertain judgments; coordinator judgment is not human acceptance.

## CI and Reproducibility

The deterministic script needs Python and no LLM/API key. No model provider, behavioral CI runner or gate is configured. Hosted inference may need credentials/costs; local inference needs compute. Pin model/settings, harness, candidate, permissions and rubric before comparing repeated runs or adopting behavioral gates; keep cross-model comparisons separate.

## Results and Limitations

On Windows with Python 3.14.10, ten helper tests passed. The original polluter misparsed a quoted checker path containing spaces and exited 2 as though pollution already existed. A focused Windows command-line handling correction made that regression case pass. Repeat-run source remains byte-identical. Helper interfaces are otherwise unchanged; POSIX behavior and failed descendant termination are not proven by this run.

Three fresh contexts used inherited model/settings. Diagnosis-only identified the overwrite defect from supplied controlled observations and preserved scope, but initially confused failing pre-fix checks with contradicted claims. The evidence contract was clarified; a targeted follow-up, not a fresh replay, returned the correct claim assessments. The composed case reused authorized repair scope without claiming implementation/final checks. The missing-reproduction case treated cache as a hypothesis and requested specific redacted evidence. Final link/style/clarity edits and removal of the redundant anti-pattern table received source/static checks only; the human-suggested-cause reminder remains in diagnosis workflow.

The coordinator separately executed the small arithmetic fixture in memory to establish the observations: one line returned 10; two lines returned 20 against expected 30; changing only assignment to accumulation returned 30, and restoring assignment returned 20. This is synthetic evidence, not product verification. No behavioral save/renderer preview, baseline comparison or repeated-run result is claimed. Retain concise receipts with the reviewed change at the maintainer-selected evidence location; this procedure does not depend on temporary planning documents. Exclude development resources from runtime packaging; final package contents are not verified here.
