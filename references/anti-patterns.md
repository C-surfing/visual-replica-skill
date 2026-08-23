# Anti-patterns

These may increase a screenshot score while producing a bad implementation.

Forbidden for final acceptance:

- whole-page screenshot as CSS background
- placing the reference under/over the live UI
- screenshot slices for buttons/text/layout
- canvas recreation of the whole interface when normal UI components are expected
- global `transform: scale(...)` to compensate for wrong viewport
- post-capture resize/crop/color correction
- hiding deterministic mismatches with masks
- changing the reference/golden to candidate output
- excessive one-off negative margins instead of fixing parent geometry
- absolute-positioning the entire page solely to trace one screenshot
- blurring to reduce edge error
- swapping exact text for shorter text merely to match boxes

A legitimate crop is an actual image/illustration/logo asset region, not a substitute for interface structure.
