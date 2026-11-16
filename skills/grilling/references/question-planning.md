# Question Planning

Use this reference to organize interdependent choices and form manageable rounds. A decision map records the unresolved questions, their priority and prerequisites. It can branch like a tree or share prerequisites across questions.

## Find and Classify Decisions

Start from consequential forks or underspecified outcomes, such as "make it fast" without a relevant target or "handle conflicting edits" without a conflict policy. Exclude unchanged confirmed choices, routine implementation discretion and facts available from permitted evidence.

| Priority | Practical Meaning                                                |
| -------- | ---------------------------------------------------------------- |
| Blocking | Needed to proceed safely or define the requested outcome         |
| Shaping  | Materially changes the result, trade-offs or acceptance          |
| Routine  | Reversible detail covered by existing constraints or conventions |

Prioritize by consequences and uncertainty in this subject. A visual detail can be consequential; category names do not determine risk. Do not escalate every uncertainty into a user decision or create questions for every routine detail. A request for a thorough interview expands relevant coverage, not permission to reopen settled choices.

## Dependencies and Evidence

If answering B requires A's answer, or A would materially change B's options, resolve A first. Do not add dependencies merely because questions concern related topics. If the map seems cyclic, identify the shared premise or ask about the coupled trade-off together rather than forcing contradictory sequential answers.

Check available evidence before asking. If a lookup is uncertain, state its source and limits. The user may decide a policy under that uncertainty, but cannot turn an unverified technical fact into verified evidence by accepting a suggestion.

## Frontier and Rounds

The **frontier** is the set of unresolved decisions whose prerequisites are resolved. Ask a manageable subset, prioritizing impact and coherent topics. Use fewer questions for complex trade-offs or host interface limits, and group short independent questions when they can be answered together.

Recompute after each reply, including partial answers. Carry unanswered questions forward without repeating already-resolved ones. Never send a dependent question merely to fill a batch. When no question is currently answerable, check for missing evidence, unresolved prerequisites or a modeling error before declaring completion.

Use stable question identifiers across a round and its follow-ups so answers map unambiguously. A useful chat shape is:

```markdown
## Round 1

1. Which <concrete choice> fits <stated constraint>?
   Options: <meaningful alternatives, if helpful>.
   Recommendation: <choice and reason, only when justified>.

2. <Independent question>?
```

Ask one clear decision per question, with enough context to explain why it matters. Use open questions to discover needs or missing alternatives; use concrete options to compare known choices. Allow ranges, examples, alternatives and explicit delegation. State a recommendation's rationale separately so it does not imply the user's agreement. Use plain chat or the available question interface while preserving these properties.

## Worked Example

**Subject:** "Add notifications for collaboration events." No event list or delivery channel has been agreed.

**Round 1:**

1. Which collaboration events must notify users initially? For example, comments, mentions or assignments; specify the required set.
2. Which channels are required: in-app, email, push or a combination? Explain the reach and setup trade-offs; do not presume one is sufficient.

**User:** "Comments and mentions; in-app only."

Those answers resolve the initial events and channel. Now ask relevant timing, history and user-control questions, whose options depend on that scope. Email delivery retry policy is out of scope; an in-app unread-history decision may still matter. Existing visual conventions can cover routine styling without another question.

If the user instead answers only "in-app", keep the event set open and ask the still-relevant questions in the next manageable batch. If they stop, summarize the confirmed channel and the unanswered event/timing choices; do not infer a complete notification specification.
