# Slicing Techniques

Catalog used in Step 3 of the Create flow. Every Slice produced by any technique must still meet the [Slice Quality Bar](../SKILL.md#slice-quality-bar).

## Selection Rule

1. Identify the dominant source of size in the Work Item or Slice being split: a multi-step process, several operations, several rules, several data shapes, several interfaces, heavy shared effort, an unproven connection between parts, or a quality target.
2. Choose the technique that matches that source. Do not walk through the whole catalog.
3. When several Splits are possible, prefer the one that: isolates parts of low value or doubtful need, or keeps feedback short and dependencies explicit.
4. Check Coverage after the Split: the child Slices together equal the parent's scope with no missing or duplicated delivery obligations. Shared setup and regression checks may recur without duplicating ownership.

## Default Tier: Techniques That Perform the Cut

### Workflow Step

Split along the steps of a process. Deliver the simplest end-to-end step first.

- **Use when:** the work is naturally described as "first A, then B, then C".
- **Examples:**
  - Checkout → add an item to the cart; apply a discount code; confirm payment.
  - Document publishing → save a draft; submit for review; publish an approved draft.
  - Staff onboarding → create the account; assign initial access; send the welcome message.
- **Pitfall:** one Slice for "all storage of the process", another for "all transitions", another for "all notifications". Their local checks do not demonstrate a complete process outcome.

### Operation Boundary

Split by the distinct operations available on the same thing. Create/Read/Update/Delete is one instance; any set of independently useful operations qualifies.

- **Use when:** the work is described as "the user can do X, Y or Z to this thing".
- **Examples:**
  - Notes → create; list; edit; delete.
  - Inventory → receive stock; check stock levels; adjust for damage or loss.
  - Account → register; update profile; deactivate.
- **Pitfall:** building every operation's lower layer first, then every operation's entry point. Nothing is usable until both passes finish.

### Happy Path / Rule Variation

Develop a bounded successful case first where it can be safely isolated. Additional rules or failure paths may be separate Slices, but required safeguards must be present before exposure. This includes growing a simple version into a more complex one step by step.

- **Use when:** one normal case carries most of the value and the complexity lives in exceptions.
- **Examples:**
  - Money transfer → between two valid accounts with enough balance; reject on insufficient balance; enforce a daily limit.
  - Loan application → approve when all baseline criteria hold; reject on insufficient income; flag for manual review above a risk threshold.
  - Coupon → apply a valid active coupon; reject an expired coupon; reject below the order minimum.
- **Pitfall:** implementing every rule's condition check first so that no case works end to end.

### Data Variation

Split by the kind of data handled.

- **Use when:** the same operation must support more than one data shape.
- **Examples:**
  - Search → over one content type; then a second content type.
  - Report export → summary view; full-detail view.
  - Price calculation → one currency; then additional currencies.
- **Pitfall:** one over-general data layer built to handle every variation before any single variation works.

### Interface Variation

Split by the way the same operation is reached or delivered.

- **Use when:** one operation must be offered through several channels.
- **Examples:**
  - Contact import → through a form; through a file upload.
  - Notification → by one channel first; then additional channels.
  - Record lookup → by interactive screen; by programmatic interface.
- **Pitfall:** building all channels' shared handling first, with no channel complete.

### Major Effort

When the first variant needs most of the effort and later variants are cheap additions, deliver the first variant as one Slice and the remaining variants as separate Slices.

- **Use when:** one capability has several variants and the first one carries the heavy shared work.
- **Examples:**
  - Several payment providers → integrate one provider end to end; add each further provider.
  - Several file formats for import → support one format fully; add the others.
  - Several languages for a published guide → produce one language including the shared structure; add the rest.
- **Pitfall:** moving the shared effort into its own Slice. Usually let the first variant own it. A separate technical prerequisite is valid if its contract and verification are independently meaningful.

### Quality-Target Deferral

Make the behavior work correctly first. Meet the target for performance, scale or another quality attribute in a later Slice.

- **Use when:** the behavior is valid and usable before the quality target is met, and the target is a separate, measurable piece of work.
- **Examples:**
  - Search returns correct results → later: results arrive within a stated response time.
  - Batch processing handles a small data set → later: handles the stated volume.
- **Pitfall:** deferring a target that the behavior needs in order to be correct. In that case the target belongs in the first Slice's acceptance criteria.

### Tracer Bullet

Build the thinnest real path through all parts of the Boundary, using minimal data, to prove they connect. It is kept and built on afterwards.

- **Use when:** the risk is whether the parts connect at all, not the business logic.
- **Examples:**
  - Messaging → one fixed message travels from the entry point through storage and back.
  - Sensor dashboard → one fixed reading travels from ingestion through processing to display.
  - External payment provider → one minimal transaction completes through the intended path in an authorized sandbox; live side effects need separate authority.
- **Distinction:** the result is permanent work that later Slices extend. A throwaway spike produces learning, not evidence that the retained implementation works; plan it explicitly as investigation when that is the requested outcome.

## Conditional Tier: Techniques That Order or Coordinate

These never cut. They apply only when their condition holds.

### Risk-First

- **Condition:** several valid Slices already exist and uncertainty is concentrated in one of them.
- **Effect:** within a Wave, the Slice that resolves the most uncertainty is placed first. It never overrides a Dependency, creates a new kind of Slice, or relaxes the Slice Quality Bar.
- **Examples:**
  - The Slice that uses an unfamiliar external dependency goes first in its Wave.
  - The Slice with the least predictable performance on a large data set goes first in its Wave.
- **Misapplication:** treating prioritized exploration as completed implementation. Risk-based ordering and a tracer bullet may be combined.

### Contract-First

- **Condition:** independent parties (people or agents) build different parts of the same Work Item at the same time.
- **Effect:** the interface between the parties is agreed as an explicit artifact before either side implements. The artifact is recorded in the `Contract` entry of the Slice Plan. Reuse an existing agreed contract where valid. Each party verifies its owned boundary; stand-ins do not replace required real integration checks.
- **Examples:**
  - A producing team and a consuming team agree on the shape of the interface; the producer tests against it directly, the consumer tests against a stand-in of the same shape.
  - Two independently maintained services agree on the shape of the data they exchange.
  - A library's maintainers and an application agree on a new function signature before either implements it.
- **Misapplication:** treating everything one party owns as a single Slice.

## Worked Example: Recursive Splitting

_Work Item:_ "Let users register an account with email verification". _Mode:_ `Recursive`.

1. **First Split** (Workflow Step): registration creates a pending account and requests verification; successful verification grants access.
2. **Check the bar:** registration includes valid input, uniqueness, password policy, storage and pending-account access controls. These may form one manageable outcome; several rules do not automatically require another split.
3. **Refine only if needed:** isolate additional variations where there is a safe verifiable boundary. Do not label registration shippable while required validation/access safeguards are missing. If no safe smaller cut exists, keep the coupled criteria together or report the unresolved complexity.
4. **Dependencies:** verification requires a pending account; map that hard prerequisite. Checks for invalid registrations can be part of registration's own acceptance, rather than separate dependent delivery items.
5. **Result:** retain the final items, record why further refinement is or is not needed, and verify coverage plus the combined registration/verification obligations.

Only refine the item that needs it. A requested Flat breakdown stops at one level and labels any remaining coarse work honestly.

## Sources

- Richard Lawrence, [Story Splitting Flowchart](https://www.humanizingwork.com/wp-content/uploads/2020/10/HW-Story-Splitting-Flowchart.pdf), Humanizing Work: splitting patterns and the INVEST criteria (Bill Wake).
- Mike Cohn, [SPIDR](https://www.mountaingoatsoftware.com/agile/five-simple-but-powerful-ways-to-split-user-stories): additional splitting approaches, including exploration when uncertainty prevents a useful cut.
- Andrew Hunt and David Thomas, [The Pragmatic Programmer tips](https://pragprog.com/tips/): tracer bullets for incremental integration.
