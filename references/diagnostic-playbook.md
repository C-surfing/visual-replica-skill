# Diagnostic Playbook

Use the *shape* of the diff to infer root causes before editing.

## Uniform whole-page shift

Symptoms:
- most edges appear as parallel double contours
- global translation estimate is non-trivial
- many regions have similar direction of error

Likely causes:
- wrong safe area/status bar
- header height
- body margin/default browser style
- wrong shell padding
- wrong viewport origin

Action: inspect shell/header before child margins.

## Error grows progressively down the page

Symptoms:
- top looks close, bottom increasingly displaced

Likely causes:
- repeated gap off by 1–2 px
- line-height mismatch
- card height mismatch
- cumulative margins
- box-sizing assumptions

Action: find the repeated unit that accumulates error.

## Glyph-only/noisy text halos

Symptoms:
- containers align well
- diff concentrated around glyph contours

Likely causes:
- wrong font family/file
- weight mismatch
- font smoothing/rasterization difference
- letter spacing / line-height

Action: verify font availability and environment before nudging boxes.

## Text wraps one line earlier/later

Likely causes:
- content width
- font family metrics
- font size/weight
- letter spacing

Action: fix the text box/font, not the section height first.

## Repeated cards all too wide/tall

Likely causes:
- shared card token/component
- grid columns/gap
- image aspect ratio

Action: patch the shared source.

## Only images differ strongly

Likely causes:
- wrong asset
- wrong crop/object-fit/object-position
- reference uses overlay/gradient

Action: resolve asset identity before layout micro-tuning.

## Border halo around otherwise-correct component

Likely causes:
- 1 px size mismatch
- border width/color
- radius mismatch
- device/CSS pixel scale mismatch

Action: inspect box dimensions and border box model.

## Large blank-background score looks good but UI feels wrong

Cause:
- global metric diluted by empty pixels

Action:
- use edge-weighted metrics
- use critical region scores
- inspect hotspots

## One region is wrong while neighbors are right

Likely causes:
- local component variant
- wrong asset/content
- state mismatch

Action: crop and debug that region, then rerun full-page comparison.

## Alternating one-pixel stripe diff

Likely causes:
- subpixel placement
- DPR/scale mismatch
- transform scaling

Action: remove global transforms, verify integer logical geometry where appropriate, verify capture scale.

## Shadow-only diff

Likely causes:
- blur/spread/opacity/color
- clipping/overflow

Action: tune shadow only after geometry is stable.

## Candidate seems uniformly smaller/larger

Likely causes:
- wrong viewport
- browser zoom
- CSS transform scale
- reference DPR interpreted as CSS width

Action: fix environment; do not scale the whole app to compensate.
