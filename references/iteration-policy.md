# Iteration Policy

## Every iteration is an experiment

Record:
- observed mismatch
- evidence source: hotspot/region/global/manual
- hypothesis
- files/properties changed
- metrics before/after
- critical region before/after
- decision: keep/revise/rollback

## Patch size

After first pass, prefer one coherent mismatch family per iteration:
- environment/shell
- geometry
- typography
- imagery/assets
- surface/depth
- state/interaction

A coherent fix can span files if it repairs one shared root cause.

## Prioritization

Fix in this order unless user-visible criticality says otherwise:
1. wrong screen/state/viewport
2. global geometry
3. critical region geometry
4. repeated component geometry
5. typography/wrapping
6. image crop/asset
7. color/border/shadow
8. micro polish

## Keep
- target defect visibly improves
- global/critical metrics improve or remain stable within noise
- no important regression

## Revise
- target region improves but another critical area regresses
- result is flat and root cause remains unclear

## Rollback
- structure materially worsens
- fix needs many brittle offsets
- repeated elements diverge
- patch is redesign, not replication

## Plateau
If 2–3 iterations barely improve:
- revisit viewport/DPR
- inspect crop locally
- inspect DOM/native geometry
- verify fonts/assets
- inspect system chrome/safe area
- reconsider component hierarchy

Do not keep adding ±1 px nudges to a wrong model.
