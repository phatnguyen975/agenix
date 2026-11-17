# Writing Good Tests

## Properties of a Good Test

A behavior is a guarantee the system makes about how it responds to a series of inputs while in a particular state. Write one test per behavior, not one per method.

**Target:**

- Verify behavior through the public interface, using a boundary appropriate to the test purpose. Storage inspection is appropriate for a persistence/adapter contract; avoid incidental private state in a user-flow test. If the code is rewritten and the behavior is unchanged, the test needs no edit.
- Test only the project's own code. Do not test framework or library mechanics. When upstream behavior is surprising, write one narrow characterization test that records the assumption.
- Avoid private structure and incidental interaction order; assert ordered outward effects when their order is contractual.
- Do not test trivial code (constructors, getters, constants, forwarding) unless it validates, normalizes, defaults, derives, enforces, or causes side effects.

**Structure and naming:**

- One coherent behavior/scenario per test; several assertions may establish its outcome and invariants. Split independently failing concerns, not names containing "and" mechanically.
- Arrange-Act-Assert (equivalently Given-When-Then): minimal Arrange, one coherent action or interaction sequence, Assert only what the name promises.
- The name states the behavior and the condition (what, not how), in domain language, following the project's naming convention.
- The test body contains all information needed to understand it and nothing irrelevant. A reader should not need the production code to follow it.

**Assertions:**

- Assert specific values. Avoid assertions so broad that many wrong results would pass (for example, only checking that a result is not empty), and avoid large snapshots.
- Assert the specific error type and condition for failures, not a generic "something failed".
- Compare floating-point results with a tolerance unless the specification defines exact values (for example, integer minor units or a decimal type).
- Prefer asserting state and results. Assert interactions only when the interaction is the contract: an outward side effect that no state shows.
- Make a failure self-explanatory: the message shows the expected value, the actual value, and which case failed.

**Isolation and determinism:**

- Each test creates its own state, cleans up after itself, and does not depend on test order, on another test's leftovers, or on shared mutable state.
- Control time, randomness, identifiers, environment, and concurrency. Inject a clock or seed.
- Prefer completion signals or controlled time. When polling is necessary for an asynchronous boundary, use fresh observations, a bounded timeout and a specific failure; avoid arbitrary sleeps.
- A test that passes or fails without a code change is flaky: find the uncontrolled input and remove it. Do not retry until green.

**Test data and readability:**

- Specify only the data relevant to the behavior; take the rest from defaults or builders. The expected value stays visible in the test.
- Name a constant when its meaning is not obvious from the value.
- Keep each test understandable on its own rather than aggressively deduplicating it. Use helpers only to remove setup noise, never to hide expected values.
- Avoid branching that changes assertions and calculations that reimplement the subject. Simple setup, framework iteration, property checks and independent reference models are legitimate when transparent and justified.
- A helper that contains logic needs its own test or must be simplified.
- Keep test-only code (cleanup, helpers) in test utilities rather than as methods on production classes.

**Examples:**

```
BAD   test "checkout calls internal total-formatting helper"
        checkout(cart); assert internalFormat was called
GOOD  test "checkout of a valid cart is confirmed"
        result = checkout(cart); assert result.status == "confirmed"

USER-FLOW TEST (storage assertions remain valid for persistence integration):
BAD   createUser("Alice"); row = query("SELECT ... WHERE name = 'Alice'"); assert row exists
GOOD  user = createUser("Alice"); assert getUser(user.id).name == "Alice"

BAD   assert that the call fails (any error)
GOOD  assert that the call raises InvalidTotalError for total = -1
```

## Name the Break

Before writing a test body, name the production change that would make the test fail, and confirm that change is a bug and not a design decision.

- Cannot name one → redesign around an observable behavior.
- Only an incidental implementation choice can fail it (a private constant or structure) → it is a change detector; test the behavior that depends on the decision. Not "the retry limit constant equals 5" but "a call that keeps failing is retried 5 times, then reported as failed".
- It depends on the text of a source or configuration file rather than on running behavior → assert the actual artifact contract when file contents are the product; otherwise run behavior rather than grepping its implementation.

## Expected Values

Derive every expected value without the code under test: from the specification, a hand computation, or a verified literal. A value computed by the code or its helpers passes whatever the code does.

```
BAD   expected = sum of item prices, computed in the test the way the code does
      assert total(items) == expected
GOOD  assert total([price 10, price 5]) == 15
```

- The reader must be able to see how each literal follows from the specification. Add the derivation to the test list's "Source of expected" when it is not obvious.
- For intended behavior, never adopt actual output as its own oracle. Characterization may pin observed existing behavior after inspection; label its provenance and do not imply that observation proves business correctness.

## Test Doubles

A test double replaces a dependency during a test (terms from Meszaros, as used by Fowler).

| Kind  | Definition                                                                                           |
| ----- | ---------------------------------------------------------------------------------------------------- |
| Dummy | Passed around but never used; fills a parameter list                                                 |
| Stub  | Returns canned answers to calls made during the test                                                 |
| Spy   | A stub that also records how it was called, for later assertions                                     |
| Mock  | Pre-programmed with expectations about the calls it must receive                                     |
| Fake  | A working implementation with a shortcut unsuitable for production (for example, an in-memory store) |

Verify state and results with real collaborators wherever possible. Use doubles to control relevant inputs/failures or observe contractual effects, balancing realism, isolation and maintenance cost.

### Choosing a Double

1. **Prefer real collaborators** when fast, deterministic and appropriate to the test scope. A deliberate isolation seam can justify a double for owned code.
2. **When a double is justified**, choose by what the test needs to control or observe:
   | Test Need                                                                                               | Use                                                        | Examples                                                                                                         |
   | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
   | Control what the dependency returns, including forced errors, timeouts, or malformed responses          | Stub                                                       | A clock that returns a fixed time; a payment provider that answers "declined"; an HTTP client that returns a 503 |
   | The dependency must behave like the real one across several calls with state (write, then read)         | Fake                                                       | An in-memory repository; an in-memory file system; a local queue                                                 |
   | Verify an outward effect that no state reveals (a message sent, an event published, a charge requested) | Spy (record, then assert) or Mock (set expectations first) | An email sender; an event publisher                                                                              |
   | A parameter is required but irrelevant to the behavior                                                  | Dummy                                                      | A placeholder logger argument                                                                                    |
3. When more than one kind fits, use judgment. Prefer real → fake → stub → spy or mock. A fake costs effort to build and keep faithful; it pays off when many tests need the same stateful behavior. A stub is enough for a single canned answer. Choose between spy and mock by the project's convention and tooling. Many frameworks offer one "mock" object that can play stub, spy, or mock; decide its role by what the test does with it.
4. If the code under test creates its dependency internally and the test cannot replace it, make the dependency injectable (pass it in) in the smallest way, as part of the code the test requires.

### Rules

- Make doubles specific. Give each branch (success, error, malformed) its own fixture or spy so a wrong branch cannot satisfy the expectation. Assert arguments, call counts, or order only when they are part of the contract; unconstrained inputs can hide a wrong effect when its payload is contractual.
- Make doubles faithful. Model the contract-relevant shape, behavior, errors and required fields; do not invent optional fields or build an entire provider emulator for a narrow scenario. A fake is trustworthy when tests that run against both the fake and the real implementation agree (a verified fake).
- Shape boundary interfaces per operation instead of one generic fetch function with conditionals; it keeps doubles small and specific.
- Learn the real method's side effects before replacing it. Replace only the slow or external part; keep real what the test depends on.
- Assert recorded spy/mock interactions when they demonstrate a required outward effect, including relevant payload/count/order. Do not assert a stub's canned answer without invoking the subject, or an internal call that is merely an implementation choice.
- When mock setup obscures the scenario or misrepresents required behavior, simplify the seam/fixture or use real components at a suitable scope.

## Data-driven Testing

**Purpose:** gather tests that share one flow and differ only in input into one test.

**Use when:** behavior, setup, and assertion shape are identical and only input → expected pairs differ (partitions, boundaries, decision-table rules).

**Do not use when:**

- Cases need different setup, flow, or assertions.
- Rows require different or obscured oracles; use a clearer independent property/reference model when appropriate.

**Rules:**

- Give each row a descriptive label and an explicit independently justified expected value or property. Rows are independent. A failure report must identify the failing row.
- Add a case that drives the next missing behavior and observe its intended RED before implementing. Related rows can share a parameterized test; do not require writing the entire matrix before the first cycle. Record already-supported rows separately.
- In GREEN, make rows pass one at a time on the same test (Fake It, Triangulation). A row that passes because the implementation generalized is valid; it was observed red.
- A row that passes first may exercise already-generalized behavior; keep it if it adds meaningful coverage and sensitivity, without claiming a new RED.
- A row added after implementation may already pass. Keep it only if the [Test Sensitivity Review](../SKILL.md#test-sensitivity-review) identifies a realistic defect that it would catch.

## Anti-patterns

| Anti-pattern              | Sign                                                                 | Fix                                                                             |
| ------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Implementation-coupled    | Breaks on refactor with unchanged behavior                           | Test through the interface                                                      |
| Over-specified            | Asserts call order, counts, or internals that are not the contract   | Assert results and state                                                        |
| Tautological test         | Expected value computed by the code's own logic                      | Use an independent oracle                                                       |
| Change detector           | Fails on an incidental implementation choice                         | Test the behavior behind the decision                                           |
| Horizontal slicing        | Test code for several behaviors is written before the implementation | One test → one implementation → repeat                                          |
| Asserting only stub data  | The subject is not exercised; a canned answer asserts itself         | Test the real component                                                         |
| Obscure test              | Expected values or inputs hidden behind helpers, builders, or loops  | Show them in the test                                                           |
| Conditional test logic    | Branches hide assertions or calculations duplicate the subject       | Split tests or use data-driven rows                                             |
| Flaky                     | Result depends on time, order, environment, or concurrency           | Control the input and isolate state                                             |
| Fixed sleep               | Waits a set time for something to happen                             | Wait on a signal or bounded condition check                                     |
| Shared mutable state      | Tests affect each other                                              | Separate setup and teardown per test                                            |
| Mystery Guest             | Test depends on data defined far away or outside the test            | Create the needed data in or next to the test                                   |
| Snapshot abuse            | Large snapshots nobody reviews                                       | Assert specific values                                                          |
| Source-text assertion     | Greps implementation text instead of verifying the intended contract | Check the artifact contract when it is the product; otherwise exercise behavior |
| Generic failure assertion | Passes on any error                                                  | Assert the specific error and condition                                         |
| Assertion-free test       | Exists only to raise coverage                                        | Assert behavior                                                                 |
| Permanent skip            | Test skipped so the suite passes                                     | Fix it; change required coverage only with the applicable authority             |
