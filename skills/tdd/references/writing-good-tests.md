# Writing Good Tests

## Properties of a good test

A behavior is a guarantee the system makes about how it responds to a series of inputs while in a particular state. Write one test per behavior, not one per method.

**Target:**

- Verify behavior through the public interface, not through a side channel such as querying storage directly. If the code is rewritten and the behavior is unchanged, the test needs no edit.
- Test only the project's own code. Do not test framework or library mechanics. When upstream behavior is surprising, write one narrow characterization test that records the assumption.
- Do not test private methods, call order, or internal collaborators.
- Do not test trivial code (constructors, getters, constants, forwarding) unless it validates, normalizes, defaults, derives, enforces, or causes side effects.

**Structure and naming:**

- One behavior per test (one logical assertion). Split a name that needs "and".
- Arrange-Act-Assert (equivalently Given-When-Then): minimal Arrange, exactly one Act, Assert only what the name promises.
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
- Avoid synchronizing with fixed sleeps or polling. Wait on a completion signal, or control time with a double.
- A test that passes or fails without a code change is flaky: find the uncontrolled input and remove it. Do not retry until green.

**Test data and readability:**

- Specify only the data relevant to the behavior; take the rest from defaults or builders. The expected value stays visible in the test.
- Name a constant when its meaning is not obvious from the value.
- Prefer DAMP over DRY: each test reads on its own. Use helpers only to remove setup noise, never to hide expected values.
- Keep logic (conditionals, loops, computation) out of tests. The iteration mechanism of a data-driven runner is allowed.
- A helper that contains logic needs its own test or must be simplified.
- Keep test-only code (cleanup, helpers) in test utilities rather than as methods on production classes.

**Examples:**

```
BAD   test "checkout calls payment.process"
        checkout(cart); assert payment.process was called with cart.total
GOOD  test "checkout of a valid cart is confirmed"
        result = checkout(cart); assert result.status == "confirmed"

BAD   createUser("Alice"); row = query("SELECT ... WHERE name = 'Alice'"); assert row exists
GOOD  user = createUser("Alice"); assert getUser(user.id).name == "Alice"

BAD   assert that the call fails (any error)
GOOD  assert that the call raises InvalidTotalError for total = -1
```

## Name the break

Before writing a test body, name the production change that would make the test fail, and confirm that change is a bug and not a design decision.

- Cannot name one → redesign around an observable behavior.
- Only an intentional decision can fail it (a constant, message wording, private structure) → it is a change detector; test the behavior that depends on the decision. Not "the retry limit constant equals 5" but "a call that keeps failing is retried 5 times, then reported as failed".
- It depends on the text of a source or configuration file rather than on running behavior → run the behavior and assert its result.

## Expected values

Derive every expected value without the code under test: from the specification, a hand computation, or a verified literal. A value computed by the code or its helpers passes whatever the code does.

```
BAD   expected = sum of item prices, computed in the test the way the code does
      assert total(items) == expected
GOOD  assert total([price 10, price 5]) == 15
```

- The reader must be able to see how each literal follows from the specification. Add the derivation to the test list's "Source of expected" when it is not obvious.
- Never copy an observed output into an expected value. If you do not know the right answer, ask.

## Test doubles

A test double replaces a dependency during a test (terms from Meszaros, as used by Fowler).

| Kind  | Definition                                                                                           |
| ----- | ---------------------------------------------------------------------------------------------------- |
| Dummy | Passed around but never used; fills a parameter list                                                 |
| Stub  | Returns canned answers to calls made during the test                                                 |
| Spy   | A stub that also records how it was called, for later assertions                                     |
| Mock  | Pre-programmed with expectations about the calls it must receive                                     |
| Fake  | A working implementation with a shortcut unsuitable for production (for example, an in-memory store) |

Verify state and results with real collaborators wherever possible. Use a double only where a dependency cannot be real in a test.

### Choosing a double

1. **Is the dependency in the same process, fast, deterministic, and free of effects outside the process?** Use the real implementation. Never double code the project owns just to isolate a unit.
2. **Otherwise** (it crosses a system boundary such as network, database, file system, clock, randomness, or an external process, or it is slow or non-deterministic), choose by what the test needs:
   | Test need                                                                                               | Use                                                        | Examples                                                                                                         |
   | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
   | Control what the dependency returns, including forced errors, timeouts, or malformed responses          | Stub                                                       | A clock that returns a fixed time; a payment provider that answers "declined"; an HTTP client that returns a 503 |
   | The dependency must behave like the real one across several calls with state (write, then read)         | Fake                                                       | An in-memory repository; an in-memory file system; a local queue                                                 |
   | Verify an outward effect that no state reveals (a message sent, an event published, a charge requested) | Spy (record, then assert) or Mock (set expectations first) | An email sender; an event publisher                                                                              |
   | A parameter is required but irrelevant to the behavior                                                  | Dummy                                                      | A placeholder logger argument                                                                                    |
3. When more than one kind fits, use judgment. Prefer real → fake → stub → spy or mock. A fake costs effort to build and keep faithful; it pays off when many tests need the same stateful behavior. A stub is enough for a single canned answer. Choose between spy and mock by the project's convention and tooling. Many frameworks offer one "mock" object that can play stub, spy, or mock; decide its role by what the test does with it.
4. If the code under test creates its dependency internally and the test cannot replace it, make the dependency injectable (pass it in) in the smallest way, as part of the code the test requires.

### Rules

- Make doubles specific. Give each branch (success, error, malformed) its own fixture or spy so a wrong branch cannot satisfy the expectation. Assert arguments, call counts, or order only when they are part of the contract; a double that accepts any input verifies nothing.
- Make doubles faithful. Reproduce the full real structure (every documented field), not only the fields the test reads. A fake is trustworthy when tests that run against both the fake and the real implementation agree (a verified fake).
- Shape boundary interfaces per operation instead of one generic fetch function with conditionals; it keeps doubles small and specific.
- Learn the real method's side effects before replacing it. Replace only the slow or external part; keep real what the test depends on.
- Do not assert on the double itself. If you are doing so, remove the mock or the assertion.
- When mock setup is larger than the test logic, or the double misses methods the real component has, switch to real components.

## Data-driven testing

**Purpose:** gather tests that share one flow and differ only in input into one test.

**Use when:** behavior, setup, and assertion shape are identical and only input → expected pairs differ (partitions, boundaries, decision-table rules).

**Do not use when:**

- Cases need different setup, flow, or assertions.
- There are only one or two cases.
- Expected values must be computed.

**Rules:**

- Give each row a descriptive label and a literal expected value. Rows are independent. A failure report must identify the failing row.
- In RED, write all rows already in the confirmed test list into one test. Run it and confirm each row fails for the right reason before writing the implementation.
- In GREEN, make rows pass one at a time on the same test (Fake It, Triangulation). A row that passes because the implementation generalized is valid; it was observed red.
- A row that passes on the first RED run is redundant or wrong.
- A row added after the behavior was implemented (an "Added in Loop" item) passes immediately. Keep it only if the mutation analysis shows a realistic mutation that it would catch.

## Anti-patterns

| Anti-pattern              | Sign                                                                 | Fix                                           |
| ------------------------- | -------------------------------------------------------------------- | --------------------------------------------- |
| Implementation-coupled    | Breaks on refactor with unchanged behavior                           | Test through the interface                    |
| Over-specified            | Asserts call order, counts, or internals that are not the contract   | Assert results and state                      |
| Tautological test         | Expected value computed by the code's own logic                      | Use an independent literal                    |
| Change detector           | Fails only when a deliberate decision changes                        | Test the behavior behind the decision         |
| Horizontal slicing        | Test code for several behaviors is written before the implementation | One test → one implementation → repeat        |
| Asserting on a mock       | The assertion checks the mock, not behavior                          | Test the real component                       |
| Obscure test              | Expected values or inputs hidden behind helpers, builders, or loops  | Show them in the test                         |
| Conditional test logic    | `if`, loops, or computation inside the test                          | Split tests or use data-driven rows           |
| Flaky                     | Result depends on time, order, environment, or concurrency           | Control the input and isolate state           |
| Fixed sleep               | Waits a set time for something to happen                             | Wait on a completion signal                   |
| Shared mutable state      | Tests affect each other                                              | Separate setup and teardown per test          |
| Mystery Guest             | Test depends on data defined far away or outside the test            | Create the needed data in or next to the test |
| Snapshot abuse            | Large snapshots nobody reviews                                       | Assert specific values                        |
| Source-text assertion     | Asserts source or config contents instead of running behavior        | Run the behavior and assert results           |
| Generic failure assertion | Passes on any error                                                  | Assert the specific error and condition       |
| Assertion-free test       | Exists only to raise coverage                                        | Assert behavior                               |
| Permanent skip            | Test skipped so the suite passes                                     | Fix it, or delete it with a stated reason     |
