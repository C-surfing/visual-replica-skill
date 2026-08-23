# Release Validation

Validation performed for the packaged v0.12.0 release in the build environment.

## Passed

- Python syntax compilation for toolkit and tests.
- 5 synthetic pytest tests: metrics, translation detection, reference analysis, compare→diagnose pipeline, HTML report.
- Unified CLI smoke flow: `doctor`, `analyze`, `compare`, `diagnose`, `report`, `benchmark`.
- Deterministic synthetic shift case: phase correlation recovered approximately +4 px X / +6 px Y candidate displacement.
- Tesseract OCR adapter executed successfully on the synthetic example.
- Playwright capture script passed `node --check` syntax validation.
- `pyproject.toml` parsed successfully.

## Optional dependency coverage

The build environment did not include `lpips` or `pytorch-msssim`, so their runtime adapters were not executed here. The toolkit explicitly reports these backends as unavailable and continues with core metrics. Their APIs follow the packages' documented tensor/data-range contracts.

## Engineering policy

A missing optional backend must never create a fabricated score. Core comparison remains usable with Pillow + NumPy + scikit-image + OpenCV.
