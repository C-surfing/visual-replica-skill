# Visual Replica Skill Pro v12 — Engineering Quality

A focused **Agent Skill + visual QA toolkit** for high-fidelity screenshot-driven UI reconstruction.

The package deliberately separates responsibilities:

- `SKILL.md` — expert workflow and guardrails for Cursor / Claude Code / Codex-like agents.
- `visual_replica/` — deterministic Python toolkit for analysis, comparison, diagnosis, reporting and benchmarking.
- `scripts/capture.mjs` — deterministic web capture via Playwright.
- `references/` — deeper diagnosis and platform guidance loaded only when needed.
- `tests/` — synthetic tests that verify the core measurements rather than merely asserting placeholders.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -e .

visual-replica doctor
visual-replica analyze reference.png --out .visual-replica/reference-analysis.json
visual-replica compare reference.png candidate.png --out-dir .visual-replica/compare
visual-replica diagnose .visual-replica/compare/comparison.json --repo . --out .visual-replica/diagnosis.json
visual-replica report --comparison .visual-replica/compare/comparison.json --diagnosis .visual-replica/diagnosis.json --out-dir .visual-replica/report
```

For browser capture:

```bash
npm install
npx playwright install chromium
visual-replica capture http://localhost:3000 --width 390 --height 844 --out candidate.png
```

## Optional high-cost extras

Core installation includes Pillow, NumPy, scikit-image and OpenCV. These are enough for pixel metrics, SSIM, pyramid multi-scale SSIM, edge comparison, layout proposals and hotspot analysis.

Optional extras:

```bash
pip install -e '.[deep]'
pip install -e '.[ocr]'
```

- `deep`: PyTorch MS-SSIM + LPIPS. LPIPS is a distance: **lower is more similar** and the official implementation expects RGB tensors normalized to `[-1, 1]`.
- `ocr`: pytesseract as the lightweight OCR adapter. PaddleOCR can also be installed separately and selected with `--ocr paddle`.

## Design goal

This is not another autonomous UI agent. The coding agent edits code; Visual Replica supplies a disciplined workflow and visual evidence.
