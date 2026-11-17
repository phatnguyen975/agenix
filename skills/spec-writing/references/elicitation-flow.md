# Elicitation Flow

## 1. Discover the Behavioral Gaps

Map confirmed input and relevant existing contracts to [spec coverage](spec-template.md#coverage-and-format). Distinguish missing information, stale/conflicting decisions and accepted facts. Do not re-ask clear answers or treat all source documents as equally authoritative. For revisions, investigate the requested delta and its consequences, preserving unrelated decisions.

Usually establish context and scope, actors and outcomes, rules, state behavior, quality conditions and acceptance examples. Follow dependencies rather than a rigid interview order: security constraints or concurrency can shape the main flow early, and a concrete example can expose an ambiguity before prose is complete. Confirm motivation only if it is genuinely unclear.

## 2. Explore Relevant Boundaries

Check applicability, then resolve the feature-specific obligations rather than requiring an answer for every generic category:

- **Paths and data boundaries:** success, denial, invalid/missing input, empty results, domain boundaries and observable consequences.
- **Failure and recovery:** unavailable dependencies, partial completion, retry, duplicate delivery/idempotency and what must remain unchanged.
- **State and concurrency:** valid/rejected events, guards, simultaneous actors, ordering and consistency promises.
- **Security and privacy:** permissions, tenant/ownership boundaries, sensitive information and applicable audit needs.
- **Quality and compatibility:** latency/throughput under stated load, reliability windows, existing consumer behavior and migration/exposure constraints.
- **Accessibility and operation:** applicable interaction/semantic accessibility criteria, diagnostics and operational observability. These are not limited to compliance-sensitive features; detailed UI contracts remain separately owned.

A functional denial or retry rule belongs with behavior, not automatically in NFRs because it concerns security/reliability. A quality target needs conditions and a measurement basis. Do not invent numbers, legal duties or interface contracts. Preserve inherited criteria and define only the feature's delta where appropriate.

## 3. Ask and Resolve

Use open questions to discover missing context, probes for specific actors/triggers/guards/outcomes, and neutral bounded alternatives for an already understood decision. Ask dependent questions sequentially; small independent batches are useful when they reduce burden without hiding dependencies. Explain consequential trade-offs and allow an alternative.

Ground discovery in real examples and existing behavior. For new behavior, ask directly about intended policy; do not confuse a hypothetical preference with observed demand. Reflect material interpretations for agreement, but do not add confirmation gates after clear answers.

If probing stops yielding information, summarize the unresolved issue and propose explicit options with consequences. Obtain agreement for a proposed decision; a follow-up count cannot guarantee convergence. Silence is not acceptance. An unknown policy, acceptance target or required contract must be resolved, explicitly excluded within authority, or reported as a blocker. Do not hide it in an empirical assumption.

## 4. Check Readiness

Cross-check happy paths, material failures, rule/transition boundaries and examples together. A final spec has concrete accepted decisions, verifiable obligations and no unanswered questions. Distinguish accepted empirical uncertainty from missing mandatory decisions. Required behavior cannot be deferred merely to complete the document. Independent drafting may continue, but incomplete output is labeled accordingly and delivered only as requested.
