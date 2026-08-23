# Evaluation Benchmark Protocol

Use a benchmark to improve the skill itself instead of judging it from one favorite screenshot.

## Suggested case classes

Maintain private/user-authorized references across:

1. sparse landing page — large typography, whitespace, hero asset
2. dense dashboard — grids, tables, cards, icons
3. mobile commerce/feed — repeated cards, image crop, bottom navigation
4. form/settings screen — controls, borders, states, text alignment
5. modal/dropdown state — overlay and state fidelity
6. WeChat Mini Program — rpx, safe area, custom navigation/tab bar

## For every case record

- reference metadata
- target viewport/DPR
- stack/platform
- first-pass score
- final score
- number of measured iterations
- worst critical region before/after
- unresolved font/asset limitation
- whether any regression occurred
- manual reviewer verdict: strong / acceptable / weak

## Skill-level metrics

Track:

- median improvement from first pass to final
- median number of iterations to plateau
- proportion of cases with unresolved global translation
- proportion with critical region below project threshold
- regression rate
- false-success rate: agent says done while reviewer says obvious mismatch remains

The false-success rate is especially important. A good replica skill should become harder to fool, not merely better at producing optimistic prose.

## Ablations

To learn what actually improves fidelity, compare runs with and without:

- hotspot prioritization
- edge-weighted metric
- region scoring
- DOM geometry inspection
- exact assets
- font matching
- rollback policy

Do not tune the system exclusively to one UI family.
