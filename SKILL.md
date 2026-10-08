---
name: visual-replica-skill
description: Help coding agents carry a user's visual intent from mixed inspirations to the finished UI across repeated changes. Use for translating references into a design agreement, preventing aesthetic drift between iterations, discussing unfinished design in plain language, and optionally checking a rendered UI.
---

# Visual Replica — design intent continuity

**Your job is not to generate the prettiest default interface or to score screenshots. Your job is to help the person get the interface THEY intend, even after multiple design and code iterations.** Treat references as evidence of taste, not as instructions to clone a site.

Visual Replica is a continuity and feedback skill. Code generation, component libraries, design creativity and web browser inspection stay with the host agent and ecosystem tools. Existing screenshot QA is optional.

## Choose the lightest route

- **Small design edit with unambiguous taste:** change it using the existing project system and tell the person what visibly changed. Do not force a contract.
- **New design, redesign, or mixed visual references:** build or update a shared design intent agreement before significant implementation.
- **Subsequent rounds:** reread the agreement, reconcile user feedback, preserve confirmed choices, and update only what was actually decided.
- **Exact screenshot recreation:** use the original analyze / capture / compare toolkit if image precision is expressly desired.
- **The user only wants design direction or a prototype:** do not demand a running app, screenshot, CSS value, or technical acceptance criterion.

## Phase 1: Hear the design, not just describe images

From the user's words and references, distinguish these four facts:

1. **What they are making and for whom:** dominant job, reader/user priorities, feeling they want the product to evoke.
2. **What each reference contributes:** e.g. reference A's layout, B's type, C's interaction. Record why the user chose it and what should NOT be copied.
3. **What must remain true:** user-confirmed decisions, explicitly marked as such; agent hypotheses remain unconfirmed.
4. **What remains open:** only questions that would materially change the direction. Prefer one focused comparison or question over a long questionnaire.

If the user says "like this", do not translate it into a large set of assumed px values. Discuss hierarchy, rhythm, mood, content, density, responsiveness and key interactions using the user's vocabulary. Avoid introducing a visual aesthetic that the references do not support.

When direction is uncertain, use the agent's existing visual comparison/design tools (e.g. oil-ui, Figma, OpenDesign) to present **distinct** alternatives. Let the person choose. Do not develop a redundant variant generator within Visual Replica.

## Phase 2: Establish the agreement

Use a short human-readable summary as the primary conversation artifact. An optional `intent.yaml` retains task-specific decisions between agent runs:

- `direction` describes the product, desired feeling, primary action and success experience.
- `references` describes what to borrow from each source, what not to copy, and why.
- `intent.preserve` records choices with `user-confirmed` / `agent-inferred` / `tool-extracted` provenance. Use stable IDs for major choices.
- `intent.avoid` and `intent.allowed_changes` describe boundaries, not arbitrary universal aesthetic rules.
- `open_questions` keeps truly unresolved choices explicit.
- `iterations` captures the user's feedback, planned change and whether that proposal has been confirmed.
- `checks.scenarios` is **optional**. Only add browser or image checks when they resolve an actual risk.

Call `visual-replica intent init --out intent.yaml` to create a draft, then edit it to reflect ACTUAL references and user statements. The example file is not approved. Call `visual-replica intent brief --spec intent.yaml` for a readable summary.

Do not turn this file into a competing `DESIGN.md`. Reuse a product's existing design system and token sources; this file describes **this user, this surface and this round's decisions**. There is no requirement to use this CLI if the user already has an effective, readable design brief.

## Phase 3: Keep intent alive as code changes

Before coding, consult the contract and identify the 1–3 highest-impact constraints for the current work. After each meaningful visual pass:

- Inspect the current product using the host's available tools or ask the user for their actual impression when it matters. Do not treat code correctness as visual correctness.
- Compare the outcome **against the agreement**: what feels closer, what remains off, which assumption was false. Appearance, interaction and intent are separate dimensions.
- Use the person's language: "The headline is still too dominant; it pushes the reading area down" instead of "line-height 1.3 failed".
- Suggest the smallest meaningful change for the next iteration. Do not say "pixel-perfect" or "looks great" without support.
- Record an iteration only when meaningful feedback or a design decision actually occurs. Never manufacture user feedback or approval.
- Update confirmed constraints only after the person approves the changed design direction. Run `visual-replica intent guard --before previous.yaml --after intent.yaml` to flag unexpected changes. It detects changes; it cannot authenticate consent.

The agent must **not** silently mark its own design critique as user-confirmed. Keep previous approved agreement versions through git or separate snapshots before editing; otherwise the guard cannot compare them.

## Phase 4: Close the loop in everyday language

Use a few short paragraphs, not an engineering report. Tell the person:

- What is now noticeably closer to their intended design.
- What still does **not** match their goal, with observable examples.
- Which single important choice, if any, needs their feedback.
- What the next design revision would address.

Do not routinely show DOM, SSIM, tokens, CSS properties, numeric scores, test counts, or file paths to non-technical stakeholders. These belong in a detail view for the coding agent. When you cannot inspect an actual rendered UI, say so; do not invent observations.

**Only use visual testing when appropriate.** If needed, run `visual-replica verify --spec intent.yaml` for optional state/screenshots. A technical PASS is never user design approval.

## Boundaries

- The user owns aesthetic choices; agent creativity is a proposal, not authority.
- Long-term user taste across unrelated products is NOT automatically inferred from a single task contract.
- Neither an LLM nor an image metric can definitively determine whether a user likes the result.
- Visual Replica does not replace oil-ui, Impeccable, Figma, OpenDesign, Codex, Playwright or accessible UX testing.
- It should be valuable even when the host coding agent already takes screenshots without this Skill.
- The most replaceable part is generic advice. Keep the distinct value in explicit, portable, reviewable intent continuity.

Load only the relevant references when needed:
- [Design dialogue and feedback](references/design-dialogue.md)
- [Intent Contract](references/intent-contract.md)
- [Ecosystem workflow](references/integrations.md)
- [Optional fidelity diagnostics](references/fidelity-model.md)
