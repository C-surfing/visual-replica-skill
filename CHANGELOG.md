# Changelog

## 0.12.0 (2026-08-23) — Engineering Quality

- Replaced placeholder metrics with real SSIM, pixel, edge, phase-correlation and multi-scale fallback implementations.
- Added optional native MS-SSIM and LPIPS adapters with explicit availability reporting.
- Added OCR adapters, color clustering, layout proposals and component heuristics.
- Added hotspot detection, regional scoring, diagnosis with repository file suggestions, HTML report, doctor, benchmark and unified CLI.
- Added deterministic Playwright capture and real synthetic tests.
- Added CI (pytest + ruff) and validation documentation.

---

## Repository history

This repository evolved through three generations:

- **v1/v2 — pixel-perfect-ui (toolchain edition):** multi-scale comparison, edge-weighted similarity, hotspot clustering, reference analyzer, quantitative `compare.py` pipeline with example artifacts. Recoverable from git history (commit `448adb5` and earlier).
- **v3 — Visual Replica Skill Pro (methodology edition):** pure expert-workflow skill — task planning, classified visual diagnosis, implementation ordering, iteration learning, quality gates. Recoverable from git history (commit `dba6703`).
- **v0.12.0 — Engineering Quality (current):** the methodology merged with a real, tested Python toolkit (`visual_replica/`) under a unified CLI, shipped with pytest suite and CI.
