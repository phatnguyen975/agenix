# Test Design Techniques

Techniques for building and reviewing the test list. They turn a specification into candidate items.

## How to use the techniques

1. Identify the data and logic the behavior depends on: inputs, outputs, configuration, state, and the conditions that decide outcomes.
2. Pick techniques by trigger:
   | Trigger in the specification                            | Technique                | Default coverage criterion                                                |
   | ------------------------------------------------------- | ------------------------ | ------------------------------------------------------------------------- |
   | Input has ranges, sets, or formats                      | EP                       | Every partition at least once (Each Choice when there are several inputs) |
   | Partitions are ordered (limits, lengths, counts, dates) | BVA                      | 3-value BVA: every boundary value and both its neighbors                  |
   | Several conditions combine to decide an outcome         | Decision Table Testing   | Every feasible rule (column)                                              |
   | Behavior depends on lifecycle or status                 | State Transition Testing | Valid transitions coverage (0-switch)                                     |
   | Always, as a final pass                                 | Error Guessing           | Checklist entries relevant to the behavior                                |
   | A general rule holds for all inputs                     | Property-based Testing   | The property, checked over many inputs                                    |
3. Derive candidates. Take every expected value from the specification. If the specification does not define the expected result of a derived case (for example, an unspecified invalid input), mark the item `needs-confirmation`; never choose a result yourself.
4. Filter candidates with "name the break": keep a candidate only if a realistic wrong production change would make its test fail. Drop duplicates; one value may serve several purposes.
5. Write the survivors as test list items.

## 1. Equivalence Partitioning (EP)

**Mechanism:** Divide a data element into partitions whose members the system should process the same way. If one value of a partition exposes a defect, any other value of that partition should expose it too, so one test per partition is sufficient.

**Rules:**

- Partitions can be defined for inputs, outputs, configuration values, internal values, time-related values, and interface parameters.
- Partitions must not overlap and must not be empty. They may be continuous or discrete, ordered or unordered.
- A valid partition holds values the system should process; an invalid partition holds values the system should ignore or reject.
- If the specification does not say whether a class of values is valid, or what happens to it, do not decide: mark the item `needs-confirmation`.
- Coverage item = a partition. Coverage = partitions exercised ÷ partitions identified.
- Each Choice coverage is the simplest criterion for multiple input partitions. It tests every partition at least once but does not cover all combinations, so defects caused by specific combinations may be missed.

**Steps:**

1. List each input and output the behavior depends on.
2. Split each into non-overlapping partitions that cover the whole domain, including invalid ones.
3. Pick one representative per partition and take its expected result from the specification.
4. For several inputs, build test cases so that every partition of every input appears at least once; the number of test cases is at least the size of the largest set of partitions. Group valid representatives together. Cover each invalid partition in its own test (one invalid value per test) so that one rejection cannot hide another.

**Example:** "A ticket category depends on age in whole years: 0–12 child, 13–64 adult, 65–120 senior. Any other age is rejected."

| Partition                       | Values | Valid | Expected                             |
| ------------------------------- | ------ | ----- | ------------------------------------ |
| Below range                     | ≤ −1   | no    | rejected                             |
| Child                           | 0–12   | yes   | child                                |
| Adult                           | 13–64  | yes   | adult                                |
| Senior                          | 65–120 | yes   | senior                               |
| Above range                     | ≥ 121  | no    | rejected                             |
| Not a whole number (e.g., 12.5) | —      | no    | not specified → `needs-confirmation` |

Representatives such as −5, 6, 40, 90, 200 cover the partitions. When BVA also applies, its values already cover the ordered partitions (see below), so do not duplicate rows.

**Each Choice with a second input:** add `member` (yes or no), whose effect the specification defines. The age partitions need five tests; membership needs two partitions, so five tests are enough: (−5, member), (6, non-member), (40, member), (90, non-member), (200, member). Every partition of both inputs appears at least once, and the ten combinations are not all required.

## 2. Boundary Value Analysis (BVA)

**Mechanism:** Exercise the boundaries of ordered partitions, because defects often come from misplaced or omitted boundaries. The minimum and maximum of a partition are its boundary values.

**Rules:**

- BVA applies only to ordered partitions.
- **2-value BVA:** for each boundary value, two coverage items: the boundary value and its closest neighbor in the adjacent partition.
- **3-value BVA:** for each boundary value, three coverage items: the boundary value and both its neighbors.
- **Why 3-value matters:** if `x ≤ 10` is wrongly implemented as `x = 10`, the 2-value values (10, 11) cannot detect it; 9 does.

**Steps:**

1. Take the ordered partitions from EP.
2. Write each partition's minimum and maximum (its boundary values).
3. Determine the step between neighbors from the specification's precision (whole numbers: 1; currency: 0.01; and so on). If the specification states no precision, state the assumed step in the item; if the step changes the expected result, mark the item `needs-confirmation`.
4. For each boundary value, add its two neighbors. Remove duplicates across adjacent boundaries.
5. Take each expected result from the specification.

**Example:** Same ticket specification, whole numbers.

| Limit between        | Boundary values | 3-value set        | Expected                           |
| -------------------- | --------------- | ------------------ | ---------------------------------- |
| below range / child  | −1 and 0        | −2, −1, 0, 1       | rejected, rejected, child, child   |
| child / adult        | 12 and 13       | 11, 12, 13, 14     | child, child, adult, adult         |
| adult / senior       | 64 and 65       | 63, 64, 65, 66     | adult, adult, senior, senior       |
| senior / above range | 120 and 121     | 119, 120, 121, 122 | senior, senior, rejected, rejected |

What the values detect (checked against mutated implementations):

- EP representatives alone (−5, 6, 40, 90, 200) miss a boundary shifted by one, such as `age < 12` instead of `age ≤ 12`. The boundary values catch it.
- Looking only at the values around the child/adult limit, the 2-value pair (12, 13) cannot detect `age ≤ 12` implemented as `age = 12`; the 3-value neighbor 11 does.

**Applies beyond numbers:** lengths, collection sizes, dates and times, versions, and any other ordered data.

## 3. Decision Table Testing

**Mechanism:** Record how combinations of conditions lead to outcomes. Each column of the table is a rule: one unique combination of conditions with its actions. Each feasible rule becomes one test.

**Rules:**

- Rows hold conditions and actions; columns hold rules. Limited-entry tables use Boolean values; extended-entry tables may use several values (ranges, partitions, discrete values).
- **Notation:** `T` condition satisfied; `F` not satisfied; `–` irrelevant for the outcome; `N/A` infeasible combination. For actions, `X` action occurs; blank action does not occur.
- A full table has one column for every combination. Delete columns with infeasible combinations. Merge columns whose differing conditions do not affect the outcome.
- Coverage item = a column with a feasible combination. Coverage = columns exercised ÷ feasible columns.
- The number of rules grows exponentially with the number of conditions. Reduce with a minimized table or a risk-based choice, and record the reduction.
- Building the table exposes gaps and contradictions in the specification.

**Steps:**

1. List conditions and actions from the specification.
2. Enumerate the combinations (2ⁿ for n Boolean conditions), one column each.
3. Mark infeasible combinations `N/A` only when the specification or domain makes them impossible.
4. Fill actions from the specification. An outcome the specification does not define is a gap: mark the item `needs-confirmation`.
5. Merge columns only when the specification states that the differing condition is irrelevant. When unsure, keep them separate.
6. Each remaining column becomes one test with concrete values for the conditions (columns with the same shape become rows of one data-driven test).

**Example:** "Shipping is free when the customer is a member or the order total is at least 100. A valid coupon gives 10% off only when the order total is at least 100."

- **Conditions:** C1 (member), C2 (total ≥ 100), C3 (valid coupon).
- **Actions:** A1 (free shipping), A2 (10% off).
- **Full table, eight rules:**
  |                    | R1  | R2  | R3  | R4  | R5  | R6  | R7  | R8  |
  | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- |
  | **Conditions**     |     |     |     |     |     |     |     |     |
  | C1 (member)        | T   | T   | T   | T   | F   | F   | F   | F   |
  | C2 (total ≥ 100)   | T   | T   | F   | F   | T   | T   | F   | F   |
  | C3 (valid coupon)  | T   | F   | T   | F   | T   | F   | T   | F   |
  | **Actions**        |     |     |     |     |     |     |     |     |
  | A1 (free shipping) | X   | X   | X   | X   | X   | X   |     |     |
  | A2 (10% off)       | X   |     |     |     | X   |     |     |     |
- **Minimized:** merge the columns whose outcomes are equal and whose differing condition is irrelevant by the specification (R1+R5, R2+R6, R3+R4, R7+R8). Four rules instead of eight:
  |                    | R1+R5 | R2+R6 | R3+R4 | R7+R8 |
  | ------------------ | ----- | ----- | ----- | ----- |
  | **Conditions**     |       |       |       |       |
  | C1 (member)        | –     | –     | T     | F     |
  | C2 (total ≥ 100)   | T     | T     | F     | F     |
  | C3 (valid coupon)  | T     | F     | –     | –     |
  | **Actions**        |       |       |       |       |
  | A1 (free shipping) | X     | X     | X     |       |
  | A2 (10% off)       | X     |       |       |       |
- Merging hides interactions the specification does not rule out; for a condition whose irrelevance is not stated, keep the full columns. For example, after merging, a wrongly implemented "coupon applies only to non-members" survives if every merged rule is exercised with a non-member.

A condition that is itself a limit (C2: total ≥ 100) still needs Boundary Value Analysis when choosing concrete values: use 99.99 for `F` and 100 for `T`, otherwise `total > 100` survives.

## 4. State Transition Testing

**Mechanism:** Model states, events, and the transitions between them. A test is a sequence of events that causes a sequence of state changes.

**Rules:**

- A transition is labeled `event [guard condition] / action`. Guard and action are omitted when absent.
- A state table has states as rows and events (with guards) as columns. Each cell holds the target state and action. Empty cells are invalid transitions.
- **Coverage criteria:**
  - **All states:** every state is visited. Weakest.
  - **Valid transitions (0-switch):** every valid transition is exercised. Most widely used. Guarantees all states coverage.
  - **All transitions:** every valid transition is exercised and every invalid transition is attempted. Guarantees the other two. A minimum for mission- and safety-critical software.
- Attempt only one invalid transition per test, to avoid fault masking (one defect hiding another).

**Steps:**

1. List the states and events from the specification.
2. Build the state table. Each empty cell is an invalid transition.
3. Take the expected result of each valid transition from the specification: target state and action. Take the expected result of an invalid attempt from the specification (e.g. rejected with an error, state unchanged). If it is unspecified, mark the item `needs-confirmation`.
4. Choose the criterion: valid transitions coverage by default; add invalid attempts (all transitions coverage) when wrongly allowing a transition would cause harm.
5. Write event sequences that cover the chosen items. Where the interface lets a test set the starting state directly, do so instead of replaying a long sequence.

**Example:** "An order starts `Created`. `pay` moves `Created` to `Paid`. `ship` moves `Paid` to `Shipped`. `cancel` moves `Created` or `Paid` to `Cancelled` (a `Paid` order is refunded). `Shipped` and `Cancelled` are final."

| State / Event | pay       | ship      | cancel              |
| ------------- | --------- | --------- | ------------------- |
| Created       | → Paid    | (invalid) | → Cancelled         |
| Paid          | (invalid) | → Shipped | → Cancelled, refund |
| Shipped       | (invalid) | (invalid) | (invalid)           |
| Cancelled     | (invalid) | (invalid) | (invalid)           |

- 4 valid transitions and 8 invalid cells (12 in total).
- Valid transitions coverage with 3 tests: `[pay, ship]`; `[cancel]`; `[pay, cancel]`.
- All states coverage is met by `[pay, ship]` and `[cancel]`, which never exercises `Paid` → `Cancelled`. That is why it is weaker.
- All transitions coverage adds 8 single-attempt tests, such as "ship from Created is rejected and the state stays Created".
- Valid transitions coverage cannot detect a transition that is wrongly allowed; only invalid attempts can.

## 5. Error Guessing

**Mechanism:** Anticipate defects from knowledge of how similar software fails and which mistakes developers tend to make. A fault attack is the methodical form: work from a list of possible errors and design tests that expose them. Errors may concern input, output, logic, computation, interfaces, or data.

**Steps:**

1. Run the checklist below against each behavior in the test list. Use only entries relevant to that behavior; a long checklist loses value.
2. Turn each relevant entry into a candidate item with a concrete input.
3. Take the expected result from the specification. If unspecified, mark the item `needs-confirmation`.
4. Apply the "name the break" filter.

**Checklist:**

- **Input:** empty, missing or null, whitespace only, zero, negative, maximum or overflow, wrong type, malformed format, very long, special characters and Unicode.
- **Collections and data:** empty, single element, duplicates, ordering, large volume.
- **Time:** time zones, daylight-saving shifts, month and year ends, leap years.
- **Calls and state:** repeated call (idempotence), different call order, concurrent access.
- **Dependencies:** timeout, error response, malformed response, partial failure.
- **Authorization:** missing permission, wrong owner.

**Example:** For a function that parses a quantity from text, relevant entries: empty text, whitespace only, negative sign, a value above the maximum, a number with a thousands separator. Each becomes an item only if the specification states its result.

## 6. Property-based Testing

**Mechanism:** State a property (an invariant that must hold for every input), then check it over many inputs.

- **Round trip:** `decode(encode(x)) = x`.
- **Idempotence:** `f(f(x)) = f(x)`.
- **Ordering:** a sorted result is non-decreasing and contains the same elements as the input.

Use when a general rule matters more than specific examples. The property is the independent oracle; never compute the expected value with the code under test. Use a property-based testing tool only if the project already has one. Otherwise express the property as a data-driven test over a few explicit inputs.
