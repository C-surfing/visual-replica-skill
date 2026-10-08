---
name: visual-replica-skill
description: Evidence-based design intent preservation, screenshot replication, prototype-to-code verification and UI state regression checks. Use after a visual direction is selected, when recreating a reference, or when ensuring an implemented UI still matches approved behavior and appearance.
---

# Visual Replica — preserve intent, verify reality

This Skill supplies a bounded verification protocol. The coding agent edits application code; the toolkit captures evidence. **Do not redesign while replicating, and do not mistake metric similarity for taste, usability or user approval.**

## Decide the smallest appropriate workflow

- **Small local UI change:** inspect the affected component/state; existing `compare`/`capture` tools may suffice. Do not require a new design workshop.
- **Replica:** lock screenshot reference, font/assets, state, viewport and DPR. Never silently resize before final comparison. Treat critical hotspots ahead of aggregate scores.
- **Transfer:** after the owner selects a prototype/visual direction, create a versioned Design Intent Contract. State what must survive implementation versus what may legitimately change.
- **Preservation:** use an existing contract or create one from *approved* decisions; target the actual states and viewports affected by the code change.

The contract is not an aesthetic generator. oil-ui / Impeccable can explore and critique; Figma / OpenDesign can host the design; Codex or equivalent implements. Visual Replica provides evidence after those choices.

## Contract procedure

1. Run `visual-replica intent init --out intent.yaml` only when no contract exists. This writes an **unapproved sample**, not user intent.
2. Set `mode`, scenarios, target URLs and viewports. Document explicit decisions in `intent.preserve` with honest provenance. Do not label agent inference as `user-confirmed`. A user-confirmed entry requires `source.approved: true`.
3. Put behavior and state checks in `actions`/`assertions`. For image comparisons, include real `reference` files and, if justified by calibration, `min_fidelity`. Never invent a threshold.
4. Run `visual-replica intent validate --spec intent.yaml`.
5. Implement in the user's application with existing components/architecture; do not embed target screenshots into the UI, mask important differences, or game scores.
6. Run `visual-replica verify --spec intent.yaml`. Check `verification.json`, local screenshots, DOM evidence, comparison artifacts and `index.html`. Explicitly disclose unresolved `REVIEW_REQUIRED` items.
7. Fix the most consequential mismatch, rerun at affected states/viewports, and compare before/after. Do not update a baseline to make a regression disappear. Never modify approved decisions without owner review.

For screenshot-only tasks, the older `analyze`, `capture`, `compare`, `diagnose` and `report` pipeline remains valid. Inspect image pixels, typography, geometry and assets coarse to fine.

## Evidence invariants

- Only real rendered output can prove visual appearance. A screenshot cannot prove behavior.
- Browser assertions cover *declared* observable behavior, not complete product UX.
- CSS/DOM dumps are diagnostic clues, not guaranteed source-level root causes.
- `PASS` means declared automated checks passed, **not** that a human accepted the design.
- `REVIEW_REQUIRED` is not failure: it records missing or qualitative proof. `FAIL` denotes a violated check; `ERROR` means execution/configuration was invalid.
- A missing reference, metric backend or runtime must be disclosed, never silently treated as success.
- If two or three patches plateau, revisit reference scaling, fonts, viewport, assets, global layout model and dynamic state before tuning pixels.

## Reference documents (load on demand)

- [Design contract and verification](references/intent-contract.md)
- [Composing with existing tools](references/integrations.md)
- [Diff-to-fix troubleshooting](references/diff-to-fix.md)
- [Fidelity metrics](references/fidelity-model.md)
- [Platform boundaries](references/platform-guidelines.md)
- [Toolkit contract](references/toolkit-contract.md)
- [Evidence-driven improvement](references/self-improvement.md)

The tool never writes application code. Its artifacts belong in `.visual-replica/` and should normally remain uncommitted.
