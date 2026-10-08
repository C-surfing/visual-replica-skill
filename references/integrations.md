# Composable Taste-to-Code workflow

Keep the visual workflow composable. Visual Replica is the evidence layer, not an end-to-end design agent.

## Design exploration and taste

Use [oil-ui](https://github.com/oil-oil/oil-ui), [Impeccable](https://github.com/pbakaus/impeccable), inspiration boards or your preferred design method for divergent exploration, comparison and critique. The user picks a direction. Do not import their large instruction sets into this Skill.

## Design artifacts

Use [Figma](https://www.figma.com/) and its existing MCP / Code Connect information if available; otherwise use [OpenDesign](https://github.com/nexu-io/open-design) or a running HTML prototype. Prefer the real approved artifact over reconstructing an interpretation of screenshots. Reference the project's existing design tokens instead of generating competing token files.

## Engineering implementation

Codex, Claude Code and other coding agents retain application-level authority: component reuse, state design, data fetching, build/testing, accessibility and responsive layout. Keep ownership of these tasks outside Visual Replica.

## Verification contract

For a small change, use the existing capture/compare commands directly. For major prototype migration or multiple states, add `intent.yaml`. Record why the user chose the direction, what can vary, and which states are critical. The contract is machine-readable but qualitative acceptance remains with a human.

Run `visual-replica verify --spec intent.yaml` after implementation and again on subsequent changes. Feed screenshots, assertions, computed-style evidence and discrepancy summaries back into the coding agent. Do not present guesses as confirmed bugs.

## No forced prototype-first rule

If the application already has good components and design tokens, exploring directly in those components can be cheaper and more faithful than building throwaway HTML. The invariant is **validate high-uncertainty design decisions before expensive implementation**, not "HTML must always precede React."

## Ecosystem boundary

No UI component library, prompt-pack for visual polish, site inspiration scraper, autonomous frontend implementation runtime, or bespoke Figma reverse-engineering engine. Build narrow adapters only where they demonstrably reduce the cost of declared verification.
