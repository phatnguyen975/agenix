# Axis: user-facing

## Purpose

Verify that changed user-visible behavior is understandable, accessible, responsive, and appropriate for the locales and input methods the product supports.

## Method

1. Identify each affected user flow and the people/devices/locales it is designed to support.
2. Review code for behavior and semantics. Static review cannot establish final visual quality; list rendering, layout, timing, and interaction details as Not verifiable when evidence is unavailable.
3. Walk normal, loading, empty, error, success, disabled, permission-denied, and destructive states that the change introduces or affects.
4. Apply accessibility and localization checks only where the changed surface makes them relevant. Use the project's declared accessibility target; where absent, use WCAG 2.2 AA as a review reference, not a certification claim.

## Checklist

### Behavior and States

- Are labels, actions, navigation, feedback, and outcomes clear and consistent with the user's task?
- Are loading, empty, error, success, offline, and permission states handled with understandable messages and recovery paths?
- Do validation messages identify the problem and a practical correction?
- Are destructive or irreversible actions confirmed, reversible, or otherwise protected in proportion to impact?
- Are repeated submissions, pending states, and network failures communicated without duplicate actions or lost input?
- Does content reflow at 320 CSS pixels where WCAG 2.2 SC 1.4.10 applies, and remain usable at zoom/text enlargement and with long content? Allow two-dimensional layout only for content that genuinely requires it (for example, complex data tables or maps), with an appropriate alternative where needed.
- Are keyboard focus, focus restoration, dialogs, menus, and navigation state sensible after actions and errors?

### Accessibility

- Is semantic structure used, and do custom controls expose an accessible name, role, state, and value?
- Can all actions be completed by keyboard with logical focus order, visible focus, no keyboard trap, and focus not obscured by sticky or overlay content (including WCAG 2.2 SC 2.4.11 where applicable)?
- Are pointer targets at least 24 × 24 CSS pixels or sufficiently spaced under WCAG 2.2 SC 2.5.8, with documented use of the criterion's exceptions where relevant?
- Do informative images/icons have suitable text alternatives; are decorative assets hidden from assistive technology?
- Are form controls programmatically labelled, instructions associated, and errors identified in text and announced when appropriate?
- Are dynamic status updates, validation results, and async changes exposed to assistive technology without disruptive announcements?
- Is meaning not conveyed by color alone? Does text contrast meet applicable WCAG criteria (4.5:1 normal text; 3:1 large text under WCAG 2.2 AA)?
- Do dragging interactions have a single-pointer alternative under WCAG 2.2 SC 2.5.7? Can motion/animation be reduced when the platform/user preference requests it, and are flashing/focus/motion effects safe?
- Do authentication flows support accessible methods such as password-manager use and paste, and avoid relying only on cognitive-function tests (WCAG 2.2 SC 3.3.8 where applicable)?
- Are captions, transcripts, audio descriptions, or equivalent alternatives provided for relevant media?
- For native/hybrid applications, are platform accessibility APIs, semantics, focus behavior, and assistive-technology conventions reviewed in addition to web-oriented WCAG guidance?

### Internationalization and Localization

- Are user-visible strings externalized through the project's localization mechanism rather than concatenated fragments?
- Are dates, times, numbers, units, currencies, calendars, and sorting formatted/compared according to locale and domain rules?
- Are plural forms, grammatical gender/case, interpolation, and text direction handled by localization facilities?
- Can layouts tolerate text expansion, right-to-left scripts, mixed-direction content, and locale-specific input?
- Is Unicode preserved end to end, including normalization and grapheme boundaries where relevant?
- Are time-zone conversions explicit and unambiguous for user-entered or displayed times?

## Severity Guidance

- Core user flow unusable, inaccessible to a substantial user group, or destructive action likely to cause severe loss — High or Critical by impact.
- Missing important error/empty state, inaccessible secondary flow, or localization defect that prevents task completion — Medium or High.
- Minor visual polish or wording with limited impact — Low.

## Boundaries

- Requirement mismatch belongs to spec-compliance.
- Handler logic defects belong to correctness.
- Rendering, loading, and interaction latency belong to performance.
- Security properties of user flows belong to security.

## References

- [W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/wcag/)
