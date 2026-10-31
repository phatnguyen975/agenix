# Axis: maintainability

## Purpose

Verify that another engineer can understand, modify, and extend the changed code safely, with no unnecessary complexity and with names and documentation that reflect actual behavior.

## Method

1. Read each changed unit as a competent newcomer, without relying on the author's unstated knowledge.
2. Assess complexity at line, function, type, module, and test level.
3. Compare identifiers, comments, and documentation with actual behavior and surrounding conventions.
4. Inspect dead code and obsolete artifacts introduced or made obsolete by the change.
5. Use the smell baseline as a heuristic, not as an automatic rule. A justified project pattern or domain constraint can make a smell appropriate.
6. Recommend the simplest change that removes the concrete comprehension or maintenance cost.

## Checklist

### Complexity and Simplicity

- Is each changed line/function/type understandable without tracing unrelated code?
- Is control flow straightforward, without avoidable deep nesting, tangled callbacks, nested ternaries, hidden side effects, or clever tricks?
- Is related behavior grouped logically, with cohesive modules and clear boundaries?
- Could the same behavior be expressed materially more simply without weakening correctness or explicit requirements?
- Does each abstraction earn its cost? Is generalization solving a real repeated need rather than a hypothetical one?
- Are speculative parameters, options, hooks, extension points, or configuration branches introduced without a current requirement?
- Are conditionals attached to unrelated flows, or repeated conditionals on the same data shape that obscure a missing model or dispatcher?
- Does the change enlarge a difficult-to-understand function/module instead of extracting cohesive responsibilities? File/function size is a signal, not a fixed limit.

### Naming

- Do names convey domain meaning, intent, units, and side effects?
- Are names consistent with nearby code and the project's vocabulary?
- Are vague names (`data`, `result`, `temp`, `handle`) ambiguous in context?
- Are magic thresholds, units, retry counts, and limits named or documented where their meaning is not obvious?

### Comments and Documentation

- Do comments explain non-obvious reasons, constraints, or trade-offs rather than restating code?
- Are comments, TODOs, examples, and docs stale, misleading, contradictory, or made obsolete by the change?
- Do public API docs explain purpose, inputs, outputs, errors, side effects, and relevant constraints?
- Are READMEs and reference docs updated when behavior, setup, build, test, or release steps change?
- Does the change description/history communicate what changed and why when that is part of the project's review standard?

### Repository Hygiene

- Are generated outputs, caches, build artifacts, local environment files, secrets, and unnecessary binaries excluded from version control according to repository policy?
- Are ignore rules updated when new local artifacts are introduced?

### Dead Code

- Did the change leave unreachable functions, unused constants/parameters, obsolete compatibility shims, commented-out code, no-op placeholders, or stale exports?
- Is removal safe, or does usage need confirmation across dynamic/reflection/plugin/serialization boundaries? Recommend verification before deletion when static search cannot prove non-use.

## Smell Baseline

Treat each item as **possible <smell>**; report only when the changed code shows a concrete maintenance cost.

| Smell                  | Signal                                                 | Candidate Remedy                                                        |
| ---------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| Mysterious Name        | Name hides purpose                                     | Rename or clarify the domain concept                                    |
| Duplicated Code        | Same invariant/logic maintained in several places      | Extract a cohesive shared unit when duplication is real                 |
| Long Function          | Function has several independently changing concerns   | Extract named steps or split responsibilities                           |
| Long Parameter List    | Parameters travel together or obscure roles            | Group cohesive values into a type or simplify responsibilities          |
| Feature Envy           | Unit depends mainly on another object's data           | Move behavior to the appropriate owner or expose a meaningful operation |
| Data Clumps            | Same fields repeatedly travel together                 | Introduce a cohesive value/model where semantics justify it             |
| Primitive Obsession    | Primitive values represent constrained domain concepts | Introduce a small validated type where it improves correctness          |
| Repeated Switches      | Same type/state branching repeats across units         | Centralize dispatch or use a suitable polymorphic model                 |
| Shotgun Surgery        | One concept requires edits across unrelated modules    | Revisit ownership and cohesion                                          |
| Divergent Change       | One module changes for unrelated reasons               | Separate responsibilities                                               |
| Speculative Generality | Abstraction serves no current use case                 | Inline/remove unused generality                                         |
| Message Chains         | Callers navigate internal object structure             | Encapsulate a stable operation where useful                             |
| Middle Man             | Unit only delegates without adding a boundary          | Remove it or give it a real responsibility                              |
| Refused Bequest        | Subtype ignores most inherited behavior                | Prefer composition or a better type boundary                            |

## Severity Guidance

- Complexity that hides a likely defect or makes safe change materially difficult — Medium or High.
- Misleading documentation/name that causes incorrect use — Medium or High by impact.
- Smell/readability issue with concrete but limited cost — Low or Medium.
- Cosmetic naming/comment polish without a rule or practical impact — Low or do not report.

## Boundaries

- Documented naming/comment/structure rule violations belong to standards-compliance.
- Module boundaries, dependency direction, and architecture-level complexity belong to design.
- Runtime behavior defects belong to correctness.
- Dead code or style already enforced by tooling is excluded unless the change bypasses the enforcement.
