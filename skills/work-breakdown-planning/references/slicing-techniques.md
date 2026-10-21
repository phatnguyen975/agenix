# Slicing Techniques

Catalog used in Step 3 of the Create flow. Every Slice produced by any technique must still meet the Slice Quality Bar in `SKILL.md`.

## Selection Rule

1. Identify the dominant source of size in the Work Item or Slice being split: a multi-step process, several operations, several rules, several data shapes, several interfaces, heavy shared effort, an unproven connection between parts, or a quality target.
2. Choose the technique that matches that source. Do not walk through the whole catalog.
3. When several Splits are possible, prefer the one that: isolates parts of low value or doubtful need, or produces Slices of roughly equal size.
4. Check Coverage after the Split: the child Slices together equal the parent's scope, with no overlap and nothing added.

## Default Tier: Techniques That Perform the Cut

### Workflow step

Split along the steps of a process. Deliver the simplest end-to-end step first.

- **Use when:** the work is naturally described as "first A, then B, then C".
- **Examples:**
  - Checkout → add an item to the cart; apply a discount code; confirm payment.
  - Document publishing → save a draft; submit for review; publish an approved draft.
  - Staff onboarding → create the account; assign initial access; send the welcome message.
- **Pitfall:** one Slice for "all storage of the process", another for "all transitions", another for "all notifications". None is verifiable until all three exist.

### Operation boundary

Split by the distinct operations available on the same thing. Create/Read/Update/Delete is one instance; any set of independently useful operations qualifies.

- **Use when:** the work is described as "the user can do X, Y or Z to this thing".
- **Examples:**
  - Notes → create; list; edit; delete.
  - Inventory → receive stock; check stock levels; adjust for damage or loss.
  - Account → register; update profile; deactivate.
- **Pitfall:** building every operation's lower layer first, then every operation's entry point. Nothing is usable until both passes finish.

### Happy path / rule variation

Deliver the simplest successful case first. Each extra business rule, edge case or failure path becomes its own Slice. This includes growing a simple version into a more complex one step by step.

- **Use when:** one normal case carries most of the value and the complexity lives in exceptions.
- **Examples:**
  - Money transfer → between two valid accounts with enough balance; reject on insufficient balance; enforce a daily limit.
  - Loan application → approve when all baseline criteria hold; reject on insufficient income; flag for manual review above a risk threshold.
  - Coupon → apply a valid active coupon; reject an expired coupon; reject below the order minimum.
- **Pitfall:** implementing every rule's condition check first so that no case works end to end.

### Data variation

Split by the kind of data handled.

- **Use when:** the same operation must support more than one data shape.
- **Examples:**
  - Search → over one content type; then a second content type.
  - Report export → summary view; full-detail view.
  - Price calculation → one currency; then additional currencies.
- **Pitfall:** one over-general data layer built to handle every variation before any single variation works.

### Interface variation

Split by the way the same operation is reached or delivered.

- **Use when:** one operation must be offered through several channels.
- **Examples:**
  - Contact import → through a form; through a file upload.
  - Notification → by one channel first; then additional channels.
  - Record lookup → by interactive screen; by programmatic interface.
- **Pitfall:** building all channels' shared handling first, with no channel complete.

### Major effort

When the first variant needs most of the effort and later variants are cheap additions, deliver the first variant as one Slice and the remaining variants as separate Slices.

- **Use when:** one capability has several variants and the first one carries the heavy shared work.
- **Examples:**
  - Several payment providers → integrate one provider end to end; add each further provider.
  - Several file formats for import → support one format fully; add the others.
  - Several languages for a published guide → produce one language including the shared structure; add the rest.
- **Pitfall:** moving the shared effort into its own Slice. It belongs to the first variant, which is the first Slice that needs it.

### Quality-target deferral

Make the behavior work correctly first. Meet the target for performance, scale or another quality attribute in a later Slice.

- **Use when:** the behavior is valid and usable before the quality target is met, and the target is a separate, measurable piece of work.
- **Examples:**
  - Search returns correct results → later: results arrive within a stated response time.
  - Batch processing handles a small data set → later: handles the stated volume.
- **Pitfall:** deferring a target that the behavior needs in order to be correct. In that case the target belongs in the first Slice's acceptance criteria.

### Tracer bullet

Build the thinnest real path through all parts of the Boundary, using minimal data, to prove they connect. It is kept and built on afterwards.

- **Use when:** the risk is whether the parts connect at all, not the business logic.
- **Examples:**
  - Messaging → one fixed message travels from the entry point through storage and back.
  - Sensor dashboard → one fixed reading travels from ingestion through processing to display.
  - External payment provider → one minimal real transaction completes through the full path the capability will use.
- **Distinction:** the result is permanent work that later Slices extend. Work built only to be discarded is not a tracer bullet and is not a Slice.

## Conditional Tier: Techniques That Order or Coordinate

These never cut. They apply only when their condition holds.

### Risk-first

- **Condition:** several valid Slices already exist and uncertainty is concentrated in one of them.
- **Effect:** within a Wave, the Slice that resolves the most uncertainty is placed first. It never overrides a Dependency, creates a new kind of Slice, or relaxes the Slice Quality Bar.
- **Examples:**
  - The Slice that uses an unfamiliar external dependency goes first in its Wave.
  - The Slice with the least predictable performance on a large data set goes first in its Wave.
- **Misapplication:** using "risk" to justify a narrow experiment that does not cross full depth. When the risky part can only be proven at full depth, use Tracer bullet.

### Contract-first

- **Condition:** independent parties (people or agents) build different parts of the same Work Item at the same time.
- **Effect:** the interface between the parties is agreed as an explicit artifact before either side implements. The artifact is recorded in the `Contract` entry of the Slice Plan. It is not a Slice. Each party still has its own vertical Slices.
- **Examples:**
  - A producing team and a consuming team agree on the shape of the interface; the producer tests against it directly, the consumer tests against a stand-in of the same shape.
  - Two independently maintained services agree on the shape of the data they exchange.
  - A library's maintainers and an application agree on a new function signature before either implements it.
- **Misapplication:** treating everything one party owns as a single Slice.

## Worked Example: Recursive Splitting

_Work Item:_ "Let users register an account with email verification". _Mode:_ `Recursive`.

1. **First Split** (Workflow step): "register with email and password" and "verify the email address".
2. **Check against the bar:** "register" is vertical, testable and shippable, but it bundles valid input, duplicate email and weak password rules (Scope Signal 3). It fails _Small_. "Verify the email address" passes.
3. **Second Split** on the failing Slice (Happy path / rule variation):
   - 1a: register with a valid, unused email and a password meeting the minimum policy.
   - 1b: reject registration with an email already in use.
   - 1c: reject registration with a password below the minimum policy.
4. **Result:** four Atomic Slices. Guard G1 stops further splitting. Two Splits were used, within the G4 limit.
5. **Dependencies:** 1b and 1c need 1a (they add rules to a working registration); "verify the email address" needs 1a.

Only the Slice that failed was split again, never the whole Work Item.

## Sources

- Richard Lawrence, _Story Splitting Cheat Sheet_, Humanizing Work: splitting patterns and the INVEST criteria (Bill Wake).
- Mike Cohn, _SPIDR: Five Simple but Powerful Ways to Split User Stories_, Mountain Goat Software.
- Andrew Hunt and David Thomas, _The Pragmatic Programmer_: tracer bullets.
