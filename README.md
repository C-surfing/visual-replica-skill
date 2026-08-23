# pixel-perfect-ui v2

A portable Agent Skill for high-fidelity screenshot-to-code replication.

The key difference from a normal “copy this screenshot” prompt is a measured optimization loop:

```text
reference → visual model → code → deterministic render
         → multi-scale + region + hotspot comparison
         → root-cause diagnosis → minimal patch → repeat
```

## What's new in v2

- multi-scale comparison for macro → component → detail errors
- edge-weighted error to avoid blank-background score inflation
- global translation estimation
- automatic diff hotspot clustering and annotated hotspot image
- reference analyzer for palette + edge/anchor evidence
- regional/critical-area scoring
- iteration ledger helper and rollback discipline
- richer diagnostic playbook
- multiple-reference/state rules
- stronger anti-hack acceptance rules
- web / WeChat Mini Program / native adapter guidance

## Install

Copy the folder into a supported skill location, for example:

```text
.cursor/skills/pixel-perfect-ui/
.agents/skills/pixel-perfect-ui/
.claude/skills/pixel-perfect-ui/
.codex/skills/pixel-perfect-ui/
```

## Optional tools

```bash
npm install
npx playwright install chromium
pip install -r requirements.txt
```

Optional SSIM:

```bash
pip install scikit-image
```

## Typical workflow

```bash
python scripts/init_workspace.py --root .
```


```bash
python scripts/analyze_reference.py reference.png --out-dir .ui-replica/analysis
node scripts/capture.mjs --url http://localhost:3000/menu --width 390 --height 844 --out .ui-replica/candidate/candidate.png
python scripts/compare.py reference.png .ui-replica/candidate/candidate.png --out-dir .ui-replica/diff
```

For critical regions:

```bash
python scripts/compare.py reference.png candidate.png --regions-json regions.json --out-dir .ui-replica/diff
```

## Philosophy

The skill does not promise a universal 99% score. It makes fidelity measurable, localizable, repeatable, and hard to fake.

For multiple targets, fill `.ui-replica/replica-config.json` and run:

```bash
python scripts/evaluate_targets.py --config .ui-replica/replica-config.json
```
