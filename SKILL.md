---
name: pixel-perfect-ui
description: High-fidelity screenshot-to-code replication and visual repair skill for web, WeChat Mini Program, Flutter, React Native, and native UI. Use when the user asks to reproduce, clone, match, restore, audit, or visually align an implementation to one or more reference screenshots. Operates as a measured visual optimization loop: lock the reference environment, infer a visual specification, implement, render deterministically, compare globally and regionally, diagnose the highest-impact mismatch, patch minimally, and repeat until convergence.
---

# Pixel Perfect UI

Reproduce the reference, not an interpretation of it.

Treat UI replication as constrained optimization:

```text
reference evidence + project constraints
                ↓
          visual model
                ↓
          implementation
                ↓
        deterministic render
                ↓
   multi-scale / regional comparison
                ↓
       mismatch attribution
                ↓
        smallest useful patch
                ↓
              repeat
```

The reference screenshot is the visual source of truth. The running implementation is the thing being judged. Source code alone is never evidence of visual fidelity.

## 0. Choose the operating mode

Choose exactly one:

- **REPLICA** — reproduce the supplied UI as faithfully as practical. Fidelity outranks creativity.
- **REPAIR** — an implementation already exists; align it to the reference with minimal code changes.
- **AUDIT** — report visual mismatches and probable causes without editing unless requested.
- **ADAPT** — transfer the visual system to a different screen/platform while preserving the style grammar. This is not pixel replication.

Default to **REPLICA** for “复刻 / 还原 / 一样 / 对齐设计稿 / match / clone / recreate / pixel perfect”.

Do not silently switch REPLICA/REPAIR into redesign.

## 1. Non-negotiable rules

1. **Do not redesign, embellish, simplify, or modernize the reference.**
2. **Do not stop after a plausible first pass.** Run at least one measured verification loop; normally run multiple loops until convergence or a real blocker is identified.
3. **Never judge fidelity from source code.** Render the real implementation.
4. **Lock the primary reference viewport/state before responsive work.**
5. **Fix upstream geometry before downstream micro-spacing.**
6. **Fix geometry before typography, typography before cosmetic polish.**
7. **Preserve the host project’s architecture unless it directly prevents fidelity.**
8. **Use semantic flow/flex/grid for structural layout.** Use absolute positioning only for true overlays, decorations, or evidence-backed fixed placement.
9. **Do not replace the whole UI with the reference image, CSS background screenshot, canvas painting, or large screenshot slices.** Cropping is allowed only for genuine visual assets that are part of the reference.
10. **Do not update/replace the golden reference to make a candidate pass.**
11. **Do not resize/crop the candidate after capture to improve a score.** A diagnostic resize must be explicitly labeled and never used for acceptance.
12. **Stabilize animations, clocks, random content, carousels, remote imagery, caret, and async layout before comparison.**
13. **Every post-first-pass iteration must have: observed mismatch → hypothesis → patch → render → measurement → keep/revise/rollback.**
14. **Rollback changes that materially reduce fidelity unless they fix a higher-priority critical defect and the tradeoff is documented.**
15. **Do not claim “pixel-perfect / identical / 100%” unless the evidence and environment justify it.**

## 2. Evidence hierarchy

Use evidence in this priority order:

1. exact user-provided screenshots/design exports
2. exact user-provided assets/fonts
3. existing repository assets/fonts/tokens/components
4. multiple screenshots of the same UI/state family
5. live implementation behavior
6. visual inference from the screenshot
7. placeholders, only when unavoidable

If sources disagree, do not average them. Record which reference constrains which viewport/state.

## 3. Required working artifacts

Create a project-local working directory when practical. `scripts/init_workspace.py` can initialize it:

```text
.ui-replica/
  reference/
  analysis/
  candidate/
  diff/
  crops/
  states/
  visual-spec.json
  replica-config.json
  iteration-ledger.json
  fidelity-report.json
```

Do not commit this directory unless the repository convention or user asks for it.

Use the templates in `templates/`.

## 4. Phase A — Repository reconnaissance

Before editing code:

1. identify framework/runtime/platform
2. identify package manager and dev/test commands
3. identify target route/screen and navigation path
4. locate styling system, theme, tokens, fonts, icons, images
5. locate reusable components and repeated patterns
6. locate existing screenshot/golden/e2e tooling
7. identify platform chrome assumptions: status bar, safe area, custom nav, tab bar, browser scrollbar
8. identify the smallest coherent file set that should change

Prefer the repository’s existing tooling over installing another framework.

For an existing project, integrate with it. Do not replace the app with a disconnected demo.

## 5. Phase B — Reference lock

Before implementation, establish a comparison contract in `visual-spec.json` and `replica-config.json`.

Record:

- reference image pixel dimensions
- intended CSS/logical viewport dimensions
- DPR/scale when known
- browser/runtime/device class
- target route/screen/state
- whether system chrome is included
- safe-area assumptions
- dynamic/volatile regions
- exact text visible in the reference when legible
- uncertainty/confidence for inferred values
- whether the environment is **strict-comparable** or **loosely-comparable**

Example:

```json
{
  "reference": {"width_px": 1170, "height_px": 2532},
  "viewport": {"width_css_px": 390, "height_css_px": 844, "dpr": 3},
  "platform": "wechat-mini-program",
  "state": "menu-home/default",
  "system_chrome": "included",
  "comparability": "loosely-comparable"
}
```

Never compute an acceptance score between screenshots representing different intended viewports or states.

If DPR is uncertain, reason in ratios first and keep the uncertainty explicit.

## 6. Phase C — Analyze the reference before coding

Create a compact visual model. Use `scripts/analyze_reference.py` as supporting evidence, not as an oracle.

### C1. Macro layout graph

Model the page as nested regions and relationships:

```text
viewport
└── shell
    ├── top chrome/header
    ├── primary section
    │   ├── title block
    │   └── repeated cards
    └── bottom navigation
```

Identify:

- major horizontal/vertical anchor lines
- content bounds
- section heights
- column/row structure
- repeated units
- fixed vs fluid regions
- scrolling vs pinned regions

### C2. Geometry

For important components estimate:

- x/y and width/height
- internal padding
- sibling gaps
- border widths
- corner radii
- image slots and aspect ratios
- icon optical size
- text box width

Prefer relationships over isolated numbers:

- `card.left == section.left`
- `all cards share width`
- `title baseline aligns with action icon center`
- `bottom-nav is pinned to viewport bottom`

### C3. Typography

For every text role infer:

- family or likely family class
- size
- weight
- line-height
- letter spacing
- color
- text box width
- alignment
- observed line count and wrap points

Text wrapping is geometry. Wrong font metrics often masquerade as wrong layout.

### C4. Appearance

Infer:

- dominant palette
- background surfaces
- border/shadow hierarchy
- gradient direction/stops when visible
- opacity/blur
- image crop and focal point
- icon stroke/fill language

### C5. Confidence

Assign `high / medium / low` confidence to uncertain estimates. Do not turn low-confidence guesses into hard architectural constraints.

Read `references/visual-analysis.md` for the detailed method.

## 7. Phase D — First faithful implementation

Implement in this order:

1. canvas / shell / safe area
2. macro region geometry
3. repeated component geometry
4. exact assets and image crops
5. typography and wrapping
6. colors / borders / radii / shadows
7. micro alignment
8. interaction/state fidelity
9. responsive adaptation after the primary reference matches well

Rules:

- Reuse project components when they can match without override piles.
- If a generic component blocks fidelity, create a narrow visual variant rather than accumulating one-off hacks.
- Centralize values only when they actually repeat.
- Preserve intentional asymmetry in the reference.
- Preserve exact text when possible; changing text changes layout.
- Do not “clean up” unconventional spacing merely because a design system would normally be more regular.

## 8. Phase E — Deterministic render

Capture the real implementation at the locked target.

Preferred order:

1. existing project visual/e2e harness
2. native platform screenshot tooling
3. Playwright for web-like targets
4. another deterministic capture tool

For web, `scripts/capture.mjs` supports viewport locking, DPR, ready selectors, style stabilization, and state actions.

Before capture:

- set exact viewport and intended DPR/scale
- use 100% browser zoom
- wait for fonts
- wait for images
- wait for a stable layout
- disable transitions/animations
- hide caret
- stabilize dynamic content
- enter the exact reference state
- ensure scrollbar/system chrome behavior matches the contract

A render is not ready merely because the dev server returned 200.

## 9. Phase F — Multi-signal comparison

Use `scripts/compare.py` for one target, or `scripts/evaluate_targets.py` to evaluate every target in `replica-config.json`.

Generate at minimum:

- `diff.png`
- `diff-amplified.png`
- `overlay.png`
- `edge-diff.png`
- `hotspots.png`
- `metrics.json`

The evaluator should consider several signals because each catches different failure modes:

### F1. Pixel/color error
Good for exact surface/border differences under a stable environment.

### F2. Structural similarity (SSIM, when available)
Good for broad perceptual/structural agreement.

### F3. Edge similarity
Good for geometry, separators, glyph contours, and alignment.

### F4. Edge-weighted error
Weights content boundaries more heavily than blank backgrounds, reducing false confidence from large empty areas.

### F5. Multi-scale similarity
Compare at coarse, medium, and native scale:

- coarse scale → macro composition
- medium scale → component geometry
- native scale → typography/borders/polish

### F6. Global translation estimate
Estimate whether the whole candidate is shifted relative to the reference. If a large global x/y shift exists, inspect upstream shell/header/safe-area geometry before tuning children.

### F7. Mismatch hotspots
Cluster the largest diff areas and rank them by impact. Work on the biggest meaningful hotspot first unless a smaller region is more semantically critical.

### F8. Region metrics
Evaluate important regions separately. A globally high score cannot compensate for one broken primary card, title, form, or navigation region.

## 10. Fidelity model

Treat metrics as navigation signals, not objective proof of “looks perfect”.

Conceptual weighting:

```text
Macro geometry / edges            30%
Multi-scale structure / SSIM      20%
Regional critical-area quality    20%
Pixel / color fidelity            15%
Typography / wrapping             10%
Asset + interaction/state          5%
```

The scripts provide image-based metrics. Typography, asset identity, and interaction fidelity may require agent review.

### Comparability classes

**Strict-comparable**: same intended viewport, browser/runtime, OS/rendering class, font files, scale/DPR. Tight pixel thresholds are meaningful.

**Loosely-comparable**: cross-OS/browser/device/font rasterization or unavailable exact font. Emphasize structure, edges, region fidelity, and visible defects more than raw pixel equality.

### Quality target

Do not use one universal numeric threshold. Aim for:

- no wrong/missing dominant region
- no unexplained global displacement
- no critical hotspot with obvious geometry mismatch
- primary text wraps on the same lines where practical
- major assets/icons are exact or explicitly disclosed
- remaining differences are localized, low-impact, and explainable

Read `references/fidelity-model.md`.

## 11. Phase G — Error attribution before patching

Never modify CSS/layout merely because “the screenshot looks off”. Classify the mismatch first.

Use this priority:

1. environment/viewport mismatch
2. shell/safe-area/system chrome mismatch
3. global translation/scale mismatch
4. parent/container geometry mismatch
5. repeated component geometry mismatch
6. font metrics/wrapping mismatch
7. image crop/asset mismatch
8. surface/color/border/shadow mismatch
9. one-off micro alignment

Read `references/diagnostic-playbook.md` for common diff patterns and likely causes.

## 12. Phase H — Controlled iteration

After the first pass, each iteration must be small enough to understand causality.

For every iteration:

1. list the top 1–3 observed mismatches, preferably from hotspot/region evidence
2. state the root-cause hypothesis
3. choose one coherent mismatch family
4. patch the smallest shared/root implementation
5. capture again
6. compare again
7. record before/after metrics and affected regions
8. decide `keep`, `revise`, or `rollback`

Do not simultaneously rewrite layout, typography, colors, imagery, and interaction after the first pass unless the implementation is fundamentally wrong.

Maintain `.ui-replica/iteration-ledger.json`; use `scripts/ledger.py` if helpful.

## 13. Root-cause discipline

Prefer upstream/shared fixes:

- everything below the header shifted → inspect header/safe-area height
- every card too wide → fix grid/container/shared card width
- repeated baseline drift → inspect shared line-height/font
- all images crop differently → fix shared image rule/object-fit/mode
- only glyph edges differ → investigate font/rasterization before moving boxes
- error grows down the page → inspect cumulative line-height/gap/box sizing rather than adding negative margins

Do not patch six children if one parent explains all six errors.

## 14. Regional debugging

When full-page comparison becomes noisy:

1. select the highest-impact hotspot/critical region
2. crop the same coordinates from reference and candidate
3. compare the crop at native scale
4. inspect the candidate DOM/native component geometry
5. fix the root container before descendants
6. re-run the full-page evaluation after the local fix

Use `scripts/crop_region.py` and `scripts/dom_snapshot.mjs` where applicable.

## 15. Plateau protocol

If 2–3 iterations produce negligible or oscillating improvement, stop micro-tweaking.

Re-check:

- wrong viewport/DPR/scale
- hidden system chrome/safe-area mismatch
- wrong font or unavailable font
- incorrect asset/crop
- incorrect component hierarchy
- browser/default styles
- scrollbar appearance
- screenshot compression/scaling
- reference includes state not reproduced by the candidate

A plateau often means the model is wrong, not that another `margin-left: -1px` is needed.

## 16. Regression and rollback policy

Rollback/revise when:

- global structure worsens materially
- a critical region regresses
- the same fix needs many one-off offsets
- repeated elements become inconsistent
- the patch improves aesthetics but diverges from the reference
- the score rises only because blank/background areas improved while the primary content worsened

Use critical-region floors and hotspot review to prevent metric gaming.

## 17. Assets and fonts

Resolve assets in this order:

1. exact user-provided asset
2. exact repository asset
3. authorized official/project-owned source asset
4. faithful crop from the supplied reference for a genuine asset region
5. generated replacement only when the user permits it
6. neutral placeholder

Never silently substitute a distinctive icon/logo/illustration with a merely similar icon.

For images, match:

- crop
- focal point
- aspect ratio
- object-fit / mini-program image mode
- clipping radius
- overlays

For fonts, prefer exact files. If exact font metrics are unavailable, disclose the limitation.

Read `references/asset-policy.md`.

## 18. Interaction and state fidelity

A screenshot can imply behavior. When behavior is part of the target:

- use real buttons/links/inputs/tabs
- reproduce selected/open/disabled states supported by evidence
- verify hover/focus/active for web controls when applicable
- preserve keyboard/focus semantics
- capture reference-relevant states separately

For multiple states, do not compare them as one image. Treat every state as its own target constraint.

Read `references/interaction-states.md` and `references/multi-reference.md`.

## 19. Multiple references and responsive constraints

If references show different viewports/states/screens:

- keep a separate target record per reference
- identify shared tokens/components versus target-specific geometry
- infer breakpoints only from observed structural changes
- verify each known reference independently
- test at least one intermediate viewport if responsive interpolation matters

Do not optimize one viewport by breaking another known reference.

## 20. Platform adapters

### Web / React / Vue / HTML
- deterministic browser capture is expected when possible
- inspect DOM geometry for stubborn mismatch
- keep CSS scale at 1; do not transform the entire page to fit

### WeChat Mini Program
- account for `rpx ↔ logical px` conversion
- lock custom/system navigation behavior and safe-area assumptions
- verify image `mode`, scroll containers, custom tab bars
- prefer WeChat DevTools/device screenshots for final fidelity
- browser emulation is diagnostic, not final evidence for native rendering

### Flutter / React Native / native
- lock logical viewport, scale/density, text scale, safe area, platform theme
- prefer emulator/device/native golden screenshots
- do not treat a web renderer as final proof

Read `references/platform-adapters.md`.

## 21. Anti-hacks

Forbidden acceptance shortcuts:

- background-image of the whole reference
- transparent overlay of the reference during final capture
- screenshot slicing for text/buttons/layout regions
- CSS transforms that globally scale a wrongly-sized page into place
- candidate post-processing to alter scale/crop/colors
- masking deterministic but incorrect regions
- changing the reference/golden
- blurring the candidate to reduce high-frequency diff

Read `references/anti-patterns.md`.

## 22. Definition of done

REPLICA/REPAIR is complete only when all applicable items are true:

- [ ] target screen/state is correct
- [ ] viewport/logical size/DPR assumptions are recorded
- [ ] primary reference has been rendered from the real implementation
- [ ] animations/dynamic instability are controlled
- [ ] comparison artifacts exist or a tooling limitation is explicit
- [ ] macro composition and shared anchors are close
- [ ] no unexplained global shift remains
- [ ] repeated components are consistent and close
- [ ] primary typography wraps/alignment closely match
- [ ] major assets/icons match or gaps are disclosed
- [ ] critical regions have been evaluated separately
- [ ] top mismatch hotspots are minor/localized or explained
- [ ] required interactions/states work
- [ ] known reference viewports are not broken by the final patch
- [ ] final iteration did not materially regress fidelity
- [ ] final report states remaining differences instead of declaring unsupported perfection

## 23. Final response contract

Report concisely:

1. what was implemented/fixed
2. target route/screen/state and viewport
3. verification environment and method
4. major before/after visual findings
5. regional/hotspot status
6. remaining mismatches, unavailable fonts/assets, or rendering limitations
7. files changed
8. command(s) to rerun the visual check

Never say “pixel-perfect”, “identical”, or “100% restored” without evidence.

## 24. Progressive references

Load only what is needed:

- `references/visual-analysis.md` — screenshot → measurable visual model
- `references/diagnostic-playbook.md` — diff shape → likely root cause
- `references/fidelity-model.md` — metric interpretation and acceptance
- `references/iteration-policy.md` — keep/revise/rollback and convergence
- `references/multi-reference.md` — multiple viewports/states/screens
- `references/interaction-states.md` — interactive state fidelity
- `references/platform-adapters.md` — web / mini-program / native
- `references/asset-policy.md` — fonts, images, icons, logos
- `references/anti-patterns.md` — forbidden screenshot hacks and metric gaming
- `references/evaluation-benchmark.md` — benchmark the skill itself and track false-success rate

Use scripts as measurement tools. The agent remains responsible for interpretation and code changes.
