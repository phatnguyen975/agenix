# Slicing Techniques

Use this reference when selecting a new increment or resolving a slicing/coordination question. Reuse an approved breakdown instead of applying this catalog again. Each candidate must satisfy the [Slice Quality Bar](../SKILL.md#slice-quality-bar).

Prefer a coherent outcome across the owned boundary. The cuts below are options, not a mandatory taxonomy. Later slices may build on verified predecessors. Examples describe capability growth, not permission to expose incomplete security, validation or business safeguards.

## Techniques for Selecting a Cut

### Workflow Step

Split along the steps of a process. Implement the simplest verifiable step first; remaining steps become later slices. Expose only outcomes that are safe under the agreed visibility policy.

**Recognize it when:** the unit of work is naturally described as "the user does A, then B, then C".

**Examples:**

- A checkout process → slice 1: add an item to the cart; slice 2: apply a discount code; slice 3: confirm payment.
- A content publishing workflow → slice 1: save a draft; slice 2: submit a draft for review; slice 3: publish an approved draft.
- An employee onboarding process → slice 1: create the account; slice 2: assign initial access; slice 3: send the welcome notification.

**Horizontal anti-pattern:** building "all data storage for the whole process" as one slice, then "all the step-transition logic" as another, then "all the notifications" as a third. Each stops at one layer and does not demonstrate the whole process. A separately scoped storage contract may still be a valid technical prerequisite; do not claim it completes the user outcome.

### Operation Boundary

Split by the type of operation the unit of work exposes. Create/Read/Update/Delete is one common instance of this, not the definition — any set of distinct operations on the same thing qualifies.

**Recognize it when:** the unit of work is naturally described as "the user can do X, Y, or Z to this thing", and each operation is independently useful.

**Examples:**

- A "manage notes" feature → slice 1: create a note; slice 2: list notes; slice 3: edit a note; slice 4: delete a note.
- An inventory feature → slice 1: receive new stock; slice 2: check current stock levels; slice 3: adjust stock for damage/loss.
- A user-account feature → slice 1: register an account; slice 2: update profile details; slice 3: deactivate an account.

**Horizontal anti-pattern:** writing the full set of operations at one layer before any other layer exists for any of them (e.g., every operation's data-access code first, then every operation's entry point second). Individual layers may be testable, but those checks do not establish a complete operation.

### Happy Path / Rule Variation

Implement a bounded successful case first when it can be safely isolated. Additional rules or failure paths may become later slices, but required safeguards must exist before the behavior is exposed. Keep tightly coupled safety obligations in the same increment when isolation cannot enforce them.

**Recognize it when:** one "normal" case covers most value, and the rest of the complexity is in exceptions to it.

**Examples:**

- A "transfer money" feature → slice 1: transfer between two valid accounts with sufficient balance; slice 2: reject a transfer with insufficient balance; slice 3: enforce a daily transfer limit.
- A "loan application" feature → slice 1: approve an application meeting all baseline criteria; slice 2: reject an application with insufficient income; slice 3: flag an application for manual review above a risk threshold.
- A "coupon at checkout" feature → slice 1: apply a valid, active coupon; slice 2: reject an expired coupon; slice 3: reject a coupon below the order minimum.

**Horizontal anti-pattern:** implementing every rule's condition-checking logic first, with no case fully working end-to-end, instead of making one case fully work before touching the next.

### Data / Input Variation

Split by the kind of data handled, or by the way it enters or exits the system.

**Recognize it when:** the same underlying operation needs to support more than one data shape or more than one entry/exit path.

**Examples:**

- An "import contacts" feature → slice 1: add a contact through a form; slice 2: import contacts from a file.
- A "search" feature → slice 1: search over one kind of content; slice 2: extend search to a second kind of content.
- A "report export" feature → slice 1: export a summary view; slice 2: export the full detail view.

**Horizontal anti-pattern:** building a single, over-general input/output layer meant to handle every variation at once before any single variation is proven to work end-to-end.

### Tracer Bullet

When the connection between the parts of the current boundary is unproven, build the thinnest possible real (non-throwaway) path through all of them first, using minimal data, to confirm they are wired together before expanding. Use the actual components needed to prove that path; doubles can support local development but do not prove the replaced integration.

**Recognize it when:** the risk is in whether the parts of the boundary even connect correctly, not in the business logic itself.

**Examples:**

- Before building a full messaging feature, first prove one hardcoded message can travel from the entry point through to storage and back.
- Before building a sensor-data dashboard, first prove one hardcoded reading can travel from ingestion through processing to display.
- Before integrating a new external payment provider, first prove one minimal transaction through the intended path in an authorized sandbox. Live charges or other external effects require their own authority.

**Important distinction:** a tracer bullet is kept and built on, not deleted after the risk is resolved. A throwaway prototype used only to learn something and then discarded is a spike, not a tracer bullet.

## Ordering and Coordination

### Risk-First

**Condition to apply:** several valid vertical slices are already identified, and uncertainty is concentrated in one of them.

**What it does:** changes the _order_ slices are implemented in — the slice that resolves the greatest uncertainty goes first, so a fundamental problem surfaces early rather than after most of the unit of work is built. Respect dependency order and supplied priorities; risk does not permit bypassing prerequisites or redefining approved work.

**Examples:**

- Among several planned slices for a new feature, the one exercising an unfamiliar external dependency is built first.
- Among several planned slices, the one with the least certain performance characteristics (e.g., operating over a potentially large data set) is built and measured first.

**Misapplication to avoid:** treating an exploratory spike as proof that the retained implementation works. Risk-based ordering and a tracer bullet can be combined: one prioritizes work, the other demonstrates a thin working path.

### Contract-First

**Condition to apply:** the same unit of work is being built by more than one independent party at the same time (human or agent), each responsible for a different part of it.

**What it does:** defines the interface between the parties as an explicit, agreed artifact before either side implements against it. Each party verifies its owned contract. Local checks can proceed before the other side is ready, but agreed-contract doubles do not remove the need for real integration and compatibility verification.

**Examples:**

- Two teams split by layer of ownership (one producing an interface, one consuming it) agree on the shape of the interface first; the producing side implements and tests against it directly, the consuming side implements and tests against a stand-in that matches the same shape.
- Two services maintained independently agree on the shape of the data they exchange before either changes its internals.
- A shared library's maintainers and a consuming application agree on a new function's signature before either side writes the implementation that depends on it.

**Misapplication to avoid:** treating "contract-first" as license to build an entire layer (e.g., everything one party owns) as a single slice. Each party's own unit-of-work boundary is still sliced using a relevant cut; agree only the interface detail needed for the dependent work and resolve material changes before implementing against them.

## Worked Walkthrough: Recursive Slicing

**Unit of work:** "Let users register for an account with email verification."

1. **First cut (Operation Boundary / Workflow Step):** identify "register with email and password" and "verify the email address" as candidate outcomes. Establish how pending accounts are isolated before protected access.
2. **Check the quality bar:** registration may combine input policy, uniqueness, persistence and confirmation delivery. Keep them together if they form one manageable, testable outcome; the number of rules alone does not force a split.
3. **Recurse only if feedback would be too slow:** one candidate is a valid registration that creates a pending account and requests verification, followed by additional rejection cases and the verification outcome. Use this sequence only if incomplete registration remains inaccessible to real users and unsafe account states cannot grant access. Otherwise include required rejection safeguards in the first increment.
4. **Record dependencies and checks:** later candidates may rely on verified registration. Check each outcome through its owned boundary, then verify the combined registration/verification flow. Required security and password-policy checks precede exposure.
5. **Execute under the supplied policy:** implement and verify eligible increments, retaining evidence. Commit and expose only under the caller's cadence and authority.

Cut once, assess the specific source of size or uncertainty, and refine only what needs it. Do not recreate a supplied approved breakdown to match this example.
