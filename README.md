<div align="center">

# 🧬 Visual Replica Skill Pro

**A disciplined Agent Skill + deterministic visual QA toolkit for high-fidelity screenshot-driven UI reconstruction.**

Make AI behave like a **senior visual frontend engineer** — reproduce the target, not an interpretation of it.

![Agent Skill](https://img.shields.io/badge/Agent%20Skill%20+%20Toolkit-8B5CF6?style=for-the-badge&logo=robot)
![Version](https://img.shields.io/badge/version-0.12.0-6f42c1?style=for-the-badge)
![License](https://img.shields.io/github/license/C-surfing/visual-replica-skill-pro?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CI](https://img.shields.io/github/actions/workflow/status/C-surfing/visual-replica-skill-pro/ci.yml?style=for-the-badge&logo=githubactions&logoColor=white)
![Tests](https://img.shields.io/badge/pytest-passing-22c55e?style=for-the-badge&logo=pytest&logoColor=white)
![Stars](https://img.shields.io/github/stars/C-surfing/visual-replica-skill-pro?style=for-the-badge&logo=github)

*For Cursor · Claude Code · Codex · and any coding agent that can run Python.*

</div>

---

## 🎯 What it is

Not another autonomous UI agent. The **coding agent edits code**; Visual Replica supplies a **disciplined workflow and visual evidence**:

- `SKILL.md` — expert workflow and guardrails for coding agents
- `visual_replica/` — deterministic Python toolkit: analysis, comparison, diagnosis, reporting, benchmarking
- `scripts/capture.mjs` — deterministic web capture via Playwright
- `tests/` — synthetic tests that verify real measurements, not placeholders

> **Fundamental principle:** Reference image = visual specification. Rendered application = only reliable evidence. Never claim success from code inspection alone.

## 🔁 The Loop

```mermaid
flowchart TD
    A["Reference Screenshot"] --> B["visual-replica analyze<br/>(palette · geometry · layout)"]
    B --> C["Agent implements<br/>(SKILL.md workflow)"]
    C --> D["visual-replica capture<br/>(Playwright, fixed viewport)"]
    D --> E["visual-replica compare<br/>(SSIM · pixel · edge · phase-correlation<br/>multi-scale fallback · hotspots)"]
    E --> F["visual-replica diagnose<br/>(root cause + file suggestions)"]
    F --> G{"Accept?"}
    G -->|no| H["Minimal fix → recapture"]
    H --> D
    G -->|yes| I["visual-replica report<br/>(HTML evidence)"]
    style I fill:#d1fae5,stroke:#059669
```

## 🧰 Toolkit

Unified CLI: `visual-replica <command>`

| Command | What it does |
| :--- | :--- |
| `doctor` | Environment self-check (deps, optional adapters) |
| `analyze` | Reference analysis → palette, edges, layout evidence |
| `compare` | Multi-metric diff: SSIM, pixel, edge, phase-correlation, multi-scale fallback, hotspot clustering, regional scoring |
| `diagnose` | Root-cause classification **with repository file suggestions** |
| `report` | Self-contained HTML report of comparison + diagnosis |
| `capture` | Deterministic Playwright screenshot at fixed viewport |
| `benchmark` | Manifest-driven benchmark runs |

### Metrics depth

- **Core** (Pillow / NumPy / scikit-image / OpenCV): pixel, edge, SSIM, pyramid multi-scale SSIM, layout proposals, hotspots
- **`[deep]` extra**: native MS-SSIM + LPIPS (PyTorch — LPIPS is a distance, *lower* = more similar, input normalized to `[-1, 1]`)
- **`[ocr]` extra**: pytesseract adapter (or PaddleOCR via `--ocr paddle`) for text-region fidelity

## 🚀 Quick start

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .                                    # optional: pip install -e '.[deep]' '.[ocr]'

visual-replica doctor
visual-replica analyze reference.png --out .visual-replica/reference-analysis.json
visual-replica compare reference.png candidate.png --out-dir .visual-replica/compare
visual-replica diagnose .visual-replica/compare/comparison.json --repo . --out .visual-replica/diagnosis.json
visual-replica report --comparison .visual-replica/compare/comparison.json \
  --diagnosis .visual-replica/diagnosis.json --out-dir .visual-replica/report
```

Browser capture:

```bash
npm install
npx playwright install chromium
visual-replica capture http://localhost:3000 --width 390 --height 844 --out candidate.png
```

## 📦 Structure

```text
visual-replica-skill-pro/
├── SKILL.md                    # expert workflow + guardrails
├── visual_replica/             # Python toolkit (11 modules)
│   ├── cli.py                  #   unified CLI entry
│   ├── analyze.py / compare.py / metrics.py / hotspots.py
│   ├── diagnose.py / report.py #   root cause + HTML evidence
│   └── benchmark.py / doctor.py / utils.py / assets/capture.mjs
├── scripts/capture.mjs         # Playwright capture
├── references/                 # diff-to-fix · fidelity-model · platform-guidelines
│                               #   self-improvement · toolkit-contract
├── templates/regions.json      # critical-region definitions
├── benchmarks/manifest.example.json
├── examples/synthetic/         # reference vs candidate demo
├── tests/                      # pytest suite (metrics, analyze, report, pipeline)
├── .github/workflows/ci.yml    # pytest + ruff on push/PR
├── pyproject.toml · package.json · VALIDATION.md · CONTRIBUTING.md
└── CHANGELOG.md
```

## 🔬 Validation

`VALIDATION.md` documents how the toolkit is verified. CI runs `pytest` and `ruff` on every push — the measurements are real, and regressions get caught.

## 📜 License

[MIT](LICENSE) © 2026 [C-surfing](https://github.com/C-surfing)

---

<p align="center">Evidence over vibes. Reproduce the reference, not an interpretation of it. 🎯</p>
