# Interaction and State Fidelity

Visual replication includes behavior when the screenshot or user request implies it.

## Required semantics

Use real:
- buttons
- links
- inputs
- checkboxes/radios
- tabs
- dialogs

Do not create a visually accurate but dead surface when interaction is expected.

## State capture

For each reference state define actions such as:
- click selector
- hover selector
- focus selector
- set input value
- wait for selector

Use `scripts/capture.mjs` arguments for simple states or project-native e2e tooling for complex flows.

## Visual state rules

Reproduce only states supported by evidence. Do not invent motion/hover styling when not requested unless needed for basic usable controls.

## Motion

Animation is not part of static pixel fidelity unless the user supplies motion/video/reference state. Stabilize motion during static comparison.
