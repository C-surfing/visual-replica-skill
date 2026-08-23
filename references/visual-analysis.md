# Visual Analysis

The goal is to turn pixels into constraints before implementation.

## 1. Build a hierarchy, then measure

First infer a visual tree:

```text
viewport
└── shell
    ├── chrome/header
    ├── main
    │   ├── section-title
    │   └── repeated-card-grid
    └── bottom-nav
```

For each node record parent, approximate box, alignment relationships, repeated/singular, fixed/fluid, confidence.

## 2. Find shared anchor lines

Strong anchors often explain most perceived alignment:

- page content left/right edges
- title left edge
- grid column boundaries
- repeated card edges
- image top/bottom lines
- divider lines
- baseline/centerline relationships

A replica can feel globally wrong because one shared anchor is off by 4–8 px.

## 3. Ratios before absolute pixels when scale is uncertain

Estimate:

- content width / viewport width
- page padding / viewport width
- card width / content width
- media height / card width
- header height / viewport height

Ratios are safer than raw pixels when screenshot DPR is uncertain.

## 4. Repetition is calibration evidence

Repeated components let you distinguish local noise from shared geometry.

If all six cards are wrong in the same way, suspect:

- parent width/grid
- shared card component
- shared image ratio
- shared typography token

Do not tune cards individually unless the reference proves they differ.

## 5. Typography is geometry

Record:

- exact visible text when legible
- line count and wrap points
- visual weight
- text box width
- baseline relationships
- line spacing

When a line wraps differently, verify font + width + letter spacing + line-height before moving surrounding boxes.

## 6. Color hierarchy

Separate:

- canvas/background
- surface layers
- primary/secondary text
- borders/separators
- accent/selected state
- shadows/overlays

Dominant palette extraction is evidence, not proof. Anti-aliased text creates many near-duplicate colors.

## 7. Confidence

Use `high`, `medium`, `low`.

Examples:

- image dimensions: high
- number of cards: high
- repeated left anchor: high/medium
- exact font family from appearance alone: low
- subtle shadow blur: low

## 8. Optional script evidence

`scripts/analyze_reference.py` can output:

- dominant colors
- horizontal/vertical edge projection peaks
- coarse edge density
- suggested alignment bands
- reference analysis overlay

Use it to support visual reasoning. It is intentionally conservative and does not claim semantic component detection.
