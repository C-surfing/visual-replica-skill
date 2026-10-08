# Visual Replica

**Make the interface the user actually wanted — and keep it that way through every iteration.**

**Design Intent Continuity** is a small, model-independent Agent Skill that helps turn scattered visual references and vague aesthetic preferences into an agreed direction that survives code generation, redesigns and feedback rounds.

[中文说明](README.zh-CN.md) · [Skill instructions](SKILL.md) · [Design dialogue](references/design-dialogue.md)

## The problem

A user might love **site A's composition**, **site B's typography**, and **site C's interaction**. They want a coherent product, not three screenshots pasted together. Even excellent coding agents can produce a convincing first page, then slowly move away from the chosen hierarchy, feeling and priorities as the implementation changes.

The hard part is not describing a screenshot. It is remembering **what they liked, why, what should not be copied, what has been approved, and what remains unfinished**.

This Skill makes those decisions explicit and revisitable without turning design into a checklist of CSS values.

## The workflow we recommend

1. **Explore.** Gather references with Awwwards, Mobbin, Godly, Pinterest or your own collection. Explain which quality of each example you want. Use [oil-ui](https://github.com/oil-oil/oil-ui) to explore different directions if needed.
2. **Agree.** Use Figma, [OpenDesign](https://github.com/nexu-io/open-design), a quick prototype or a design conversation to choose a direction. Visual Replica records what to borrow, what to avoid and what should feel different in your product.
3. **Build.** Let Codex, Claude Code or another coding agent implement with your existing design system. [Impeccable](https://github.com/pbakaus/impeccable) can provide dedicated design critique and polish.
4. **Refine.** Look at the actual experience with the agent. Ask "Does this still feel like what we chose?" rather than "Did the CSS satisfy the screenshot score?" Record important feedback, preserve confirmed decisions and iterate.
5. **Check only when useful.** Browser tests and screenshots are optional evidence. The host agent may already have excellent visual inspection. Visual Replica should never demand redundant capture or pretend that image similarity equals aesthetic approval.

**Simple rule:** design decisions belong to the person; execution belongs to the agent; continuity is shared and reviewable.

## What the person sees

> **Our direction:** Quiet and editorial, with the content as the main character.  
> **What you liked:** Layout from A, type hierarchy from B, interaction from C — not A's branding or C's loud colors.  
> **Closer now:** The main content has room to breathe.  
> **Still off:** The navigation still competes too much with the headline.  
> **One choice for you:** Do you want the navigation even quieter, or is discoverability more important?

No requirement to read DOM dumps, review CSS, understand accessibility audit IDs or compare SSIM scores.

## What makes this different?

Visual Replica does **not** claim to be a better designer than oil-ui, Impeccable, Figma, OpenDesign or a newer model. It also does not create another design editor, component library, screenshot loop or coding agent.

Its narrow responsibility is **keeping intentional choices explicit during repeated edits**. When an approved choice changes, it raises the change for confirmation instead of quietly rewriting it. A new agent can resume work from the same task agreement.

This is **not an unassailable moat**. More capable agents may absorb generic prompt-based design coaching. Our investment is in a portable, human-reviewable agreement and evidence that this workflow actually reduces aesthetic drift. If it does not, we should simplify rather than add more framework.

## Minimal start

For small tasks, simply use the [SKILL.md](SKILL.md) with your coding agent and converse normally. For a design that will take several rounds, it can maintain an optional `intent.yaml`.

```bash
pip install -e .
visual-replica intent init --out intent.yaml
visual-replica intent brief --spec intent.yaml --lang en
```

The starter agreement is a **draft**, with examples you must replace; it does not pretend the user approved anything. It works before there is code, a screenshot or a running website.

For subsequent rounds, keep the previous contract snapshot and check changes:

```bash
visual-replica intent guard --before intent.previous.yaml --after intent.yaml --lang en
```

This flags changed approved choices for the user to decide. It **does not** automatically prove or register the user's consent.

A task agreement describes `direction`, mixed `references`, `intent`, `open_questions` and feedback `iterations`. Read [the reference](references/intent-contract.md) or [the multi-reference example](examples/mixed-references.md). A project's existing `DESIGN.md` remains the source of its design system.

## Optional visual evidence toolkit

The original high-fidelity screenshot comparison tools remain available for users who explicitly want them:

```bash
npm install && npx playwright install chromium
visual-replica capture http://localhost:3000 --width 390 --height 844 --out candidate.png
visual-replica compare reference.png candidate.png --out-dir .visual-replica/compare
visual-replica verify --spec intent.yaml
```

The toolkit includes comparison metrics, detected discrepancies, diagnosis hypotheses, browser scenarios and HTML/JSON evidence. None of them replace subjective approval. `verify` with no browser scenarios returns `REVIEW_REQUIRED`, not a misleading PASS.

## Contribution priorities

- **Core:** clearer agreements, mixed-reference intent, feedback continuity, protection against silently changed confirmed choices.
- **Review:** optional visual and interaction evidence, task-level acceptance studies.
- **Delegate / reuse:** screenshot capture, component libraries, design generation, Figma parsing and generic design-rule catalogs.

[MIT License](LICENSE). Python 3.10+ for optional CLI; no mandatory app, server, Figma account or screenshot workflow.
