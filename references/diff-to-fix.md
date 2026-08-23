# Diff → Fix Playbook

Use this after a comparison, not before.

| Visual evidence | Likely root cause | Investigate first |
|---|---|---|
| Whole page has parallel/double edges | global translation | viewport, body/root margin, safe-area, header/nav height, page shell |
| Error is small at top and grows toward bottom | accumulated vertical drift | repeated gap/margin, line-height, fixed row/card height, box sizing |
| Repeated hotspots have nearly identical dimensions | shared component mismatch | shared card/list/button component, spacing/radius/image-ratio token |
| Containers align but glyph contours differ | typography/rasterization | exact font file, weight, line-height, letter-spacing, browser/OS rendering |
| Geometry/edges are strong but pixel similarity is weaker | appearance | colors, borders, shadows, alpha, antialiasing |
| Image box aligns but LPIPS/perceptual difference is poor | asset/crop | wrong image, object-fit/content mode, focal point, overlay/gradient |
| Only one critical region is poor while global score is high | local failure hidden by background | inspect and crop that region; fix its owning component |

Never compensate for an upstream root cause with many child offsets.
