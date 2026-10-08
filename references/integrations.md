# Taste-to-Code: recommended ecosystem workflow

Visual Replica exists **between design decisions and repeated implementation**. The Coding Agent likely already knows how to inspect the UI and take screenshots. Do not add redundant screen capture simply because this Skill supports it.

## Find the references

Use [Awwwards](https://www.awwwards.com/), [Godly](https://godly.design/), [Mobbin](https://mobbin.com/), [Pinterest](https://www.pinterest.com/), [Site of Sites](https://www.siteofsites.co/) or any existing user reference library. Record exactly which part of which source matters and why. This is not permission to clone or scrape an entire design.

## Explore and agree

Use [oil-ui](https://github.com/oil-oil/oil-ui) for contrasting directions and user selection. Use Figma, [OpenDesign](https://github.com/nexu-io/open-design) or an HTML prototype to express the chosen direction. [Impeccable](https://github.com/pbakaus/impeccable) already provides strong design vocabulary, critique, polish and anti-pattern checks. Do not reimplement any of these tools.

Visual Replica maintains a brief agreed upon by a person: what they want to feel and do, what each reference contributes, which choices must remain, and what is not yet decided. It doesn't replace `PRODUCT.md` or `DESIGN.md`, which may be maintained by another tool.

## Implement and refine

Codex, Claude Code or another coding agent owns the app's architecture and frontend implementation. Reuse existing components where appropriate. There is no requirement to write throwaway HTML before using a framework; use a prototype when it reduces design uncertainty.

After each meaningful revision, compare the *experienced result* with the agreed direction. Preserve feedback without inventing consent. If a confirmed choice now seems wrong, surface the trade-off, propose an alternative, and let the owner choose. Optional `intent guard` checks that previously approved decisions did not change silently.

## Optional visual evidence

The host may already take screenshots. Only call Visual Replica's capture/compare/verify/diagnose tools for a specific question: reference precision, a difficult mismatch, or a regression that is expensive to identify manually. Numeric score improvements do not necessarily mean increased user satisfaction.

## Ecosystem boundary and replaceability

Model-native design judgment will improve. If Visual Replica only tells a stronger model to "remember the taste", it has no durable niche. Keep its contribution limited to portable, inspectable agreements and measurable reduction of taste drift. Do not build another variant generator, component library, Figma editor, design-system extractor, generic QA suite or autonomous code-writing runtime.
