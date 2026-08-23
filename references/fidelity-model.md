# Fidelity Model

No single score equals perceptual identity.

## Signals

### Pixel MAE / changed pixel ratio
Strong for stable same-environment regression; sensitive to anti-aliasing and font rasterization.

### SSIM
Good for broad structural/perceptual similarity. Optional via `scikit-image`.

### Edge similarity
Strong for boxes, separators, glyph contours, component geometry.

### Edge-weighted error
Weights errors near visual boundaries more than blank surfaces. Useful for UI because large backgrounds otherwise dominate global metrics.

### Multi-scale similarity
Use native + downsampled views:
- coarse: macro composition
- medium: component geometry
- native: type/border/detail

### Translation estimate
A large estimated x/y shift is a diagnosis clue, not something to correct by shifting the screenshot.

### Hotspots
Rank largest connected mismatch areas. Hotspots are useful for choosing the next repair target.

## Conceptual weighting

```text
Macro geometry / edge evidence        30
Multi-scale structure / SSIM          20
Critical regions                       20
Pixel/color                             15
Typography/wrapping                     10
Assets/interactions                      5
```

The first four are partly automatable. Typography, exact asset identity, and behavior still need semantic review.

## Strict vs loose comparability

### Strict-comparable
Same runtime/browser/OS class, fonts, viewport, scale/DPR. Pixel thresholds can be tight.

### Loosely-comparable
Different font renderer/browser/device or unavailable exact font. Prefer structural, edge, region, and obvious-visible-difference judgment.

## Acceptance principles

A strong replica should have:
- correct viewport/state
- no missing dominant region
- no unexplained global translation
- no large critical hotspot
- same primary text wrapping where practical
- exact or disclosed major assets
- stable repeated geometry
- localized/explainable residual differences

## Metric gaming is forbidden

Do not:
- blur candidate
- resize/crop after render
- mask deterministic wrong areas
- use the reference as a background
- optimize empty background at the expense of content
