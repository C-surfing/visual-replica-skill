# Fidelity Model

No single metric represents visual identity.

- **Pixel MAE / changed ratio**: exact color/position sensitivity; noisy across font rasterizers.
- **SSIM**: structural signal; still affected by content and local contrast.
- **MS-SSIM**: either `pytorch-msssim` when installed or a deterministic SSIM pyramid fallback. Use it to separate macro and detail errors.
- **LPIPS**: optional perceptual distance. Lower is more similar. Do not arbitrarily convert it to “percent fidelity” without calibration. The official package documents RGB tensors normalized to `[-1, 1]`.
- **Edge similarity**: especially useful for UI geometry, alignment, separators and text contours.
- **Region scores**: protect critical regions from being diluted by large matching backgrounds.

Default composite intentionally excludes raw LPIPS because distance calibration depends on model/content. Use LPIPS as corroborating evidence.
