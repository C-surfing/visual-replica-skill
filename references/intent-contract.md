# Design Intent Contract v1

**Scope:** a task-specific acceptance boundary, not a design system, style library or Figma parser. Keep existing `PRODUCT.md` / `DESIGN.md` as durable sources of project facts and tokens.

## Distinguish what can be proven

| Evidence | Can establish | Cannot establish |
| --- | --- | --- |
| Pixel/edge/SSIM comparison | Appearance at a fixed viewport and state | Usability or visual taste |
| Playwright action + assertion | The declared state/action produced a visible outcome | All user flows or backend correctness |
| DOM bounds/computed styles | Observed positions, type and box properties | Which source line is causally responsible |
| Human qualitative review | Whether hierarchy and brand decisions are acceptable | Reproducibility without a recorded decision |

A model may draft the contract but must not self-certify its assumptions. All `preserve` entries contain one of `user-confirmed`, `agent-inferred` or `tool-extracted`. Only the first represents an approved decision, and `source.approved` must then be true.

## Contract fields

- `version`: integer `1`.
- `mode`: `replica`, `transfer`, or `preservation`.
- `source`: optional `prototype`, `design_system`, `figma_url`, and boolean `approved`.
- `intent.preserve`: list of `{text, provenance, critical?}`; these remain **human review items**. No image score automatically approves them.
- `intent.avoid`, `intent.allowed_changes`: text lists. Avoid requirements are explicitly reviewed; allowed changes inform the human/code agent.
- `checks.scenarios`: non-empty list of independently named scenarios. Each requires an HTTP(S) `url`, a `viewport` containing `width`, `height`, optional `dpr`, and a unique `id`.

A scenario optionally declares `ready_selector`, ordered `actions`, `assertions`, `inspect_selectors`, `reference`, `regions` and `min_fidelity`. URLs must be reachable by the local browser. Reference/regions file paths resolve relative to the contract's location. `replica` requires every scenario to supply a baseline.

Supported actions: `click`, `fill` (with `value`), `press` (with `value`), `check`, `uncheck`, `wait_for`. Supported conditions: `visible`, `hidden`, `text_contains` (with `value`). Prefer semantic selectors, `data-testid` for stable state anchors, or Playwright-supported CSS selectors.

## Execution and results

For each scenario, the browser opens an isolated context at the declared viewport/DPR, performs actions, waits for font/image decode after reaching the target state, checks selectors, records selected DOM boxes and computed styles, and takes a screenshot.

When a reference exists the Python comparator records raw metrics/artifacts. `min_fidelity` is **optional** and must be deliberately calibrated against your design, browser, font rasterizer and allowable content variance. Without a calibrated threshold, visual comparison requires human review regardless of numeric score.

Overall status precedence: `ERROR` if an execution/asset error occurs; otherwise `FAIL` if any declared assertion/threshold fails; otherwise `REVIEW_REQUIRED` if a baseline/threshold or qualitative review is outstanding; otherwise `PASS`.

CLI exits with `0`, `2`, `1`, or `3` respectively for `PASS`, `FAIL`, `REVIEW_REQUIRED`, `ERROR`. The machine-readable `verification.json` is authoritative for automation.

## Limitations and hardening roadmap

1. A contract is a declaration, not cryptographic evidence that the source really was approved. A human must check provenance.
2. Browser assertions are a deliberately small subset of Playwright. Use your existing accessibility/security/performance tests rather than expanding this project into every QA discipline.
3. CSS selectors and screenshots do not establish real source ownership. Correlating DOM with component mapping is a future optional adapter; do not overstate the current diagnostic precision.
4. Browser capture disables animations to stabilize snapshots. It does not validate motion behavior, non-browser UI, or arbitrary asynchronous application protocols.
5. Never auto-bless references. Modifying an approved baseline is a separate, explicit review action.
