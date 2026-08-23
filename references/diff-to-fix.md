# Diff To Fix Knowledge

Convert visual symptoms into likely engineering causes.

## Double edges everywhere

Meaning:
Global position mismatch.

Investigate:
- viewport
- parent offset
- container padding


## Error increasing downward

Meaning:
Accumulated layout drift.

Investigate:
- repeated margins
- line height
- card heights


## Only text differs

Meaning:
Typography mismatch.

Investigate:
- font
- weight
- rendering engine


## All repeated cards differ

Meaning:
Shared component problem.

Investigate:
- component structure
- design tokens
