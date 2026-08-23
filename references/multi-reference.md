# Multiple References

Treat every screenshot as an independent constraint with metadata.

Classify references:
- same screen, different viewport
- same screen, different state
- different screen, shared design system

For each target record:
- file
- viewport/logical size
- DPR if known
- state
- system chrome
- critical regions
- weight/priority

## Different viewports

Infer breakpoints from observed structural changes, not conventional breakpoint habits.

Verify every known viewport independently. A fix for desktop that breaks the supplied mobile screenshot is not a successful replica.

## Different states

Examples:
- tab A/tab B
- modal closed/open
- dropdown closed/open
- hover/focus
- empty/populated

Capture every state separately. Do not combine state references into one global score.

## Shared design tokens

Use references collectively to infer stable values:
- palette
- type roles
- radii
- icon family
- repeated card treatment

But preserve target-specific geometry where evidence differs.
