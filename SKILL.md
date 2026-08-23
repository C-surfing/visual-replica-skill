---
name: visual-replica-skill-pro
description: High-fidelity UI reconstruction skill plus executable visual QA toolkit. Use when recreating or matching an interface from screenshots/design references, auditing visual fidelity, or iterating toward a reference through deterministic rendering and measured comparison.
---

# Visual Replica Skill Pro

## Position

This package is **Skill + Toolkit**.

- The **Skill** gives the coding agent an expert reconstruction workflow, diagnosis discipline, quality gates, and stopping criteria.
- The **Toolkit** provides deterministic evidence: screenshot capture, reference analysis, multi-metric comparison, hotspot detection, diagnosis, reports, and benchmarks.
- The coding agent remains responsible for understanding and editing the host repository.

Do not turn this into an autonomous UI-generation runtime.

## Non-negotiable rules

1. The reference image is the visual source of truth.
2. The rendered implementation is the only visual evidence.
3. Do not declare success after the first implementation.
4. Do not redesign during a replication task.
5. Lock viewport/state before comparing.
6. Fix upstream geometry before downstream offsets.
7. Fix macro geometry before typography and decoration.
8. Use metrics as evidence, not as a substitute for visual judgment.
9. Do not use the screenshot as the page, large screenshot slices, or metric-gaming masks.
10. Keep/rollback changes based on measured evidence and critical-region quality.

## Workflow

### 0. Classify

- existing project + screenshot → preserve architecture and reuse components
- screenshot only → infer a maintainable component structure
- multiple screenshots → treat each viewport/state as a separate constraint
- responsive reference → match known viewports first, then infer behavior between them

### 1. Lock the reference

Record:

- screenshot pixel dimensions
- intended CSS/native viewport
- DPR/scale if known
- application route and state
- dynamic areas that must be stabilized
- exact text/assets if available

A dimension mismatch is a failed comparison, not a low score.

### 2. Analyze before coding

Use the toolkit when useful:

```bash
visual-replica analyze reference.png --out .visual-replica/reference-analysis.json
```

Extract or estimate:

- macro regions and anchor lines
- page/container padding
- repeated geometry
- dominant colors
- text boxes/content (OCR is optional)
- likely component regions
- unresolved assets/fonts

Write the important constraints into a visual spec. Do not dump noisy analysis into implementation code.

### 3. Implement coarse-to-fine

Order:

1. viewport/runtime/safe area
2. root shell and global alignment
3. macro sections
4. repeated component geometry
5. images/assets/crops
6. typography/wrapping
7. colors/borders/radii
8. shadows/micro-alignment
9. interaction states
10. responsive adaptation beyond known references

Prefer semantic flow/flex/grid/native constraints. Use absolute positioning only where the reference itself implies overlaying.

### 4. Capture deterministically

For web, prefer the bundled Playwright capture:

```bash
visual-replica capture http://localhost:3000 \
  --width 390 --height 844 \
  --out .visual-replica/candidate.png
```

For native/mobile runtimes, use their real screenshot mechanism when available. A browser approximation is not final proof for a native target.

### 5. Compare with multiple signals

```bash
visual-replica compare reference.png .visual-replica/candidate.png \
  --out-dir .visual-replica/compare
```

The comparator may report:

- normalized pixel similarity / changed-pixel ratio
- SSIM
- multi-scale SSIM (native backend if installed, deterministic pyramid fallback otherwise)
- LPIPS when its optional dependency is installed
- edge IoU / edge difference
- estimated global translation
- horizontal-band drift profile
- hotspot boxes
- region scores when a regions JSON is supplied

Do not optimize one score in isolation.

### 6. Diagnose before editing

```bash
visual-replica diagnose .visual-replica/compare/comparison.json \
  --repo . \
  --out .visual-replica/diagnosis.json
```

Use this reasoning protocol:

**Observation → Evidence → Pattern → Hypothesis → Code area → Minimal action → Validation**

Typical patterns:

- whole-page double edges → viewport/root/safe-area/container offset
- top close, bottom increasingly wrong → accumulated gap/line-height/component height
- repeated hotspots of similar size → shared component/token
- mostly character-level contours → font/weight/line-height/letter-spacing/rasterization
- image region perceptually poor but geometry good → wrong asset/crop/object-fit
- high pixel error but strong structure/edges → color/theme/rasterization rather than geometry

### 7. Iterate scientifically

For every meaningful post-first-pass change record:

- observed mismatch
- hypothesis
- files/properties changed
- comparison before/after
- keep / revise / rollback

Prefer one coherent mismatch family per iteration.

If two or three rounds plateau, stop nudging pixels and revisit assumptions: viewport, font, asset, safe area, layout model, or reference scaling.

### 8. Quality gate

A replica is complete only when:

- the correct screen/state is implemented
- the primary reference viewport is reproducible
- a real candidate screenshot was captured
- comparison artifacts exist (or a concrete runtime limitation is documented)
- no critical region remains obviously wrong
- dominant assets/icons are faithful or gaps are disclosed
- text wrapping/baselines are close
- no visual hack replaces interactive UI
- engineering quality remains maintainable
- the last accepted iteration did not materially regress
- remaining differences are stated instead of claiming unsupported “100% pixel perfect”

Generate a report when useful:

```bash
visual-replica report \
  --comparison .visual-replica/compare/comparison.json \
  --diagnosis .visual-replica/diagnosis.json \
  --out-dir .visual-replica/report
```

## Toolkit discipline

The toolkit is intentionally model-independent and dependency-tolerant:

- core metrics must work without PyTorch
- LPIPS and native MS-SSIM are optional enhancements
- OCR is optional; failure to find an OCR backend must not block visual comparison
- missing optional dependencies must be reported explicitly, never silently converted into fake scores

Read the references only when needed:

- `references/diff-to-fix.md`
- `references/fidelity-model.md`
- `references/platform-guidelines.md`
- `references/toolkit-contract.md`
- `references/self-improvement.md`
