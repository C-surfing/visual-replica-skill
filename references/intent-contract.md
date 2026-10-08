# Task-level design intent contract (version 1)

The contract is a small portable agreement that belongs to one UI task or surface. Its main responsibility is **carrying human taste and decisions through repeated Agent work**. It is not a design system, style generator, or pixel-specification schema.

Use `visual-replica intent init` to create a sample and replace all illustrative values before showing it to the user. `intent brief` renders a plain-language version. Existing version-1 screenshot contracts remain readable.

## What's recorded

- `direction` (optional): `product`, `audience`, `desired_feeling`, `primary_action`, `success_looks_like`. These describe desired human experience, not implementation.
- `references` (optional): a list of entries with stable `id`, `source`, `borrow`, `not_copy`, `why`. Multiple inspirations can supply different parts of the final design.
- `intent.preserve`: decisions with `text`, `provenance`, optional stable `id`, `reason`, `critical`. Provenance is `user-confirmed`, `agent-inferred` or `tool-extracted`.
- `intent.avoid` and `intent.allowed_changes`: a few important boundaries.
- `open_questions`: decisions that still affect the design direction.
- `iterations` (optional): meaningful round `round`, actual `user_feedback`, `agreed_change`, and `status` (`proposed`, `confirmed`, `rejected`). Do not invent comments or implied approvals.
- `source.approved`: a declaration of explicit approval made outside this tool. Any `user-confirmed` preserved choice requires this flag; the tool **cannot authenticate user consent**.
- `checks.scenarios`: optional browser/image checks. Transfer and preservation contracts may have no scenarios. Replica mode requires at least one reference scenario.

These fields are optional where indicated so simple projects can remain small. A user's own words and current visual references should be kept ahead of generic design boilerplate.

## Continuing across rounds

Save a previous snapshot of the approved contract before modifying it. Run:

```bash
visual-replica intent guard --before intent.previous.yaml --after intent.yaml
```

This flags edits to confirmed preserved choices as well as changed direction, reference roles and avoid choices when the original source was marked approved. Agent-inferred notes, pending feedback and open questions can be revised without treating them as confirmed decisions.

The result is a **request for review**, not a permission system: the agent should ask the user and only then record an approved new choice. The tool does not prevent someone from manually deleting a snapshot or claiming approval without evidence.

## Optional browser checks

If you need to test implemented appearance, `checks.scenarios` can contain `id`, `url`, `viewport`, optional `ready_selector`, `actions`, `assertions`, `inspect_selectors`, `reference`, `regions`, and `min_fidelity`.

Browser actions: `click`, `fill`, `press`, `check`, `uncheck`, `wait_for`. Conditions: `visible`, `hidden`, `text_contains`. Image acceptance thresholds require calibration to the environment and task. A screenshot cannot certify intent.

`verify` reports `PASS` (declared automated checks only), `FAIL`, `ERROR`, `REVIEW_REQUIRED`. If the contract has no scenarios, it yields `REVIEW_REQUIRED` and can still generate a human-readable design summary without opening a browser.

Never require a visual metric when a user simply wants help articulating a design direction. Never claim a passing screenshot proves that the user likes the result.
