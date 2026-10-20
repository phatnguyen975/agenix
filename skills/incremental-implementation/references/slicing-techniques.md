# Slicing Techniques

Expands the technique tables in `SKILL.md` with examples from different kinds of work, for when the short table isn't enough to decide how to cut the current unit of work. Every example here still has to pass the Slice Quality Bar in `SKILL.md`.

## Default tier — techniques that perform the cut

### Workflow step

Split along the steps of a process. Ship the simplest end-to-end step first; the remaining steps become later slices.

**Recognize it when:** the unit of work is naturally described as "the user does A, then B, then C".

**Examples:**

- A checkout process → slice 1: add an item to the cart; slice 2: apply a discount code; slice 3: confirm payment.
- A content publishing workflow → slice 1: save a draft; slice 2: submit a draft for review; slice 3: publish an approved draft.
- An employee onboarding process → slice 1: create the account; slice 2: assign initial access; slice 3: send the welcome notification.

**Horizontal anti-pattern:** building "all data storage for the whole process" as one slice, then "all the step-transition logic" as another, then "all the notifications" as a third. Each of those stops at a single part and proves nothing end-to-end until all three are finished together.

### Operation boundary

Split by the type of operation the unit of work exposes. Create/Read/Update/Delete is one common instance of this, not the definition — any set of distinct operations on the same thing qualifies.

**Recognize it when:** the unit of work is naturally described as "the user can do X, Y, or Z to this thing", and each operation is independently useful.

**Examples:**

- A "manage notes" feature → slice 1: create a note; slice 2: list notes; slice 3: edit a note; slice 4: delete a note.
- An inventory feature → slice 1: receive new stock; slice 2: check current stock levels; slice 3: adjust stock for damage/loss.
- A user-account feature → slice 1: register an account; slice 2: update profile details; slice 3: deactivate an account.

**Horizontal anti-pattern:** writing the full set of operations at one layer before any other layer exists for any of them (e.g., every operation's data-access code first, then every operation's entry point second). Nothing is usable or testable until both passes are done.

### Happy path / rule variation

Ship the simplest successful case first. Each additional business rule, edge case, or failure path becomes its own slice afterward.

**Recognize it when:** one "normal" case covers most value, and the rest of the complexity is in exceptions to it.

**Examples:**

- A "transfer money" feature → slice 1: transfer between two valid accounts with sufficient balance; slice 2: reject a transfer with insufficient balance; slice 3: enforce a daily transfer limit.
- A "loan application" feature → slice 1: approve an application meeting all baseline criteria; slice 2: reject an application with insufficient income; slice 3: flag an application for manual review above a risk threshold.
- A "coupon at checkout" feature → slice 1: apply a valid, active coupon; slice 2: reject an expired coupon; slice 3: reject a coupon below the order minimum.

**Horizontal anti-pattern:** implementing every rule's condition-checking logic first, with no case fully working end-to-end, instead of making one case fully work before touching the next.

### Data / input variation

Split by the kind of data handled, or by the way it enters or exits the system.

**Recognize it when:** the same underlying operation needs to support more than one data shape or more than one entry/exit path.

**Examples:**

- An "import contacts" feature → slice 1: add a contact through a form; slice 2: import contacts from a file.
- A "search" feature → slice 1: search over one kind of content; slice 2: extend search to a second kind of content.
- A "report export" feature → slice 1: export a summary view; slice 2: export the full detail view.

**Horizontal anti-pattern:** building a single, over-general input/output layer meant to handle every variation at once before any single variation is proven to work end-to-end.

### Tracer bullet

When the connection between the parts of the current boundary is unproven, build the thinnest possible real (non-throwaway) path through all of them first, using minimal data, to confirm they are wired together before expanding. This is still a full-depth cut — only a minimal one, not a shortcut around verticality.

**Recognize it when:** the risk is in whether the parts of the boundary even connect correctly, not in the business logic itself.

**Examples:**

- Before building a full messaging feature, first prove one hardcoded message can travel from the entry point through to storage and back.
- Before building a sensor-data dashboard, first prove one hardcoded reading can travel from ingestion through processing to display.
- Before integrating a new external payment provider, first prove one minimal, real transaction can complete through the full path the feature will use.

**Important distinction:** a tracer bullet is kept and built on, not deleted after the risk is resolved. A throwaway prototype used only to learn something and then discarded is a spike, not a tracer bullet.

## Conditional tier — techniques that order or coordinate, never cut

### Risk-first

**Condition to apply:** several valid vertical slices are already identified, and uncertainty is concentrated in one of them.

**What it does:** changes the _order_ slices are implemented in — the slice that resolves the greatest uncertainty goes first, so a fundamental problem surfaces early rather than after most of the unit of work is built. It does not create a new kind of slice and does not excuse the prioritized slice from the Slice Quality Bar.

**Examples:**

- Among several planned slices for a new feature, the one exercising an unfamiliar external dependency is built first.
- Among several planned slices, the one with the least certain performance characteristics (e.g., operating over a potentially large data set) is built and measured first.

**Misapplication to avoid:** using "risk" as a reason to build a narrow technical spike that doesn't cross full depth. If the risky part can't be proven without a full-depth cut, that's a Tracer Bullet, not Risk-first.

### Contract-first

**Condition to apply:** the same unit of work is being built by more than one independent party at the same time (human or agent), each responsible for a different part of it.

**What it does:** defines the interface between the parties as an explicit, agreed artifact before either side implements against it. Each party still produces its own vertical slice within its own boundary using the default tier — this technique only removes the need for both sides to be finished together before either can be tested.

**Examples:**

- Two teams split by layer of ownership (one producing an interface, one consuming it) agree on the shape of the interface first; the producing side implements and tests against it directly, the consuming side implements and tests against a stand-in that matches the same shape.
- Two services maintained independently agree on the shape of the data they exchange before either changes its internals.
- A shared library's maintainers and a consuming application agree on a new function's signature before either side writes the implementation that depends on it.

**Misapplication to avoid:** treating "contract-first" as license to build an entire layer (e.g., everything one party owns) as a single slice. Each party's own unit-of-work boundary is still sliced with the default tier; only the interface is agreed upfront.

## Worked walkthrough: recursive slicing

Unit of work: "Let users register for an account with email verification."

1. **First cut (Operation boundary / Workflow step):** the unit of work naturally splits into "register with email and password" and "verify the email address." Two candidate slices.
2. **Check against the Slice Quality Bar:** "register with email and password" is vertical, testable, and independently verifiable — but it bundles several rules (valid input, duplicate email, weak password) that would require more behaviors than one focused TDD run can safely cover. It fails **Small**.
3. **Recurse (Happy path / rule variation) on that slice:**
   - _Slice 1a:_ register with a valid, unused email and a password meeting the minimum policy.
   - _Slice 1b:_ reject registration with an email already in use.
   - _Slice 1c:_ reject registration with a password that doesn't meet the minimum policy.
4. Each of 1a–1c and the original "verify the email address" slice now independently satisfies the Slice Quality Bar: each crosses full depth, has a test expressing its behavior, can be verified and shipped without the others existing, and is small enough for one focused run of TDD micro-cycles.
5. These four slices are implemented and committed in order.

This is the general shape recursion takes: cut once, check against the bar, and only split further the specific slice that fails — not the whole unit of work again from scratch.
