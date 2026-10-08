from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
from skimage.metrics import structural_similarity

from .utils import clamp01, pil_to_gray_array, pil_to_rgb_array


def require_same_size(reference: Image.Image, candidate: Image.Image) -> None:
    if reference.size != candidate.size:
        raise ValueError(f"dimension mismatch: reference={reference.size}, candidate={candidate.size}")


def pixel_metrics(reference: Image.Image, candidate: Image.Image, threshold: int = 16) -> dict[str, float]:
    require_same_size(reference, candidate)
    a = pil_to_rgb_array(reference).astype(np.float32)
    b = pil_to_rgb_array(candidate).astype(np.float32)
    d = np.abs(a - b)
    per_pixel = d.max(axis=2)
    mae = float(d.mean() / 255.0)
    rmse = float(np.sqrt(np.mean((a - b) ** 2)) / 255.0)
    changed = float((per_pixel > threshold).mean())
    return {
        "mae_normalized": mae,
        "rmse_normalized": rmse,
        "changed_pixel_ratio": changed,
        "pixel_similarity": clamp01(1.0 - mae),
    }


def ssim_score(reference: Image.Image, candidate: Image.Image) -> float:
    require_same_size(reference, candidate)
    a = pil_to_rgb_array(reference)
    b = pil_to_rgb_array(candidate)
    return float(structural_similarity(a, b, channel_axis=2, data_range=255))


def _resize(img: Image.Image, scale: float) -> Image.Image:
    w = max(8, round(img.width * scale))
    h = max(8, round(img.height * scale))
    return img.resize((w, h), Image.Resampling.LANCZOS)


def pyramid_ms_ssim(reference: Image.Image, candidate: Image.Image, scales=(1.0, 0.5, 0.25), weights=(0.5, 0.3, 0.2)) -> dict[str, Any]:
    require_same_size(reference, candidate)
    values = []
    usable_weights = []
    for scale, weight in zip(scales, weights):
        r = _resize(reference, scale)
        c = _resize(candidate, scale)
        # SSIM requires a window that fits; tiny images are skipped.
        if min(r.size) < 7:
            continue
        values.append({"scale": scale, "ssim": ssim_score(r, c)})
        usable_weights.append(weight)
    if not values:
        return {"score": ssim_score(reference, candidate), "backend": "single-scale-fallback", "scales": []}
    ws = np.asarray(usable_weights, dtype=np.float64)
    ws /= ws.sum()
    score = float(sum(v["ssim"] * w for v, w in zip(values, ws)))
    return {"score": score, "backend": "deterministic-ssim-pyramid", "scales": values}


def native_ms_ssim(reference: Image.Image, candidate: Image.Image, device: str = "cpu") -> dict[str, Any]:
    try:
        import torch
        from pytorch_msssim import ms_ssim
    except Exception as exc:  # noqa: BLE001 - optional metric backend may raise third-party errors
        return {"available": False, "reason": f"optional dependency unavailable: {exc}"}
    require_same_size(reference, candidate)
    a = torch.from_numpy(pil_to_rgb_array(reference)).permute(2, 0, 1).unsqueeze(0).float().to(device)
    b = torch.from_numpy(pil_to_rgb_array(candidate)).permute(2, 0, 1).unsqueeze(0).float().to(device)
    # pytorch-msssim accepts data_range=255 with tensors in [0,255].
    try:
        with torch.no_grad():
            value = ms_ssim(a, b, data_range=255, size_average=True)
        return {"available": True, "score": float(value.detach().cpu()), "backend": "pytorch-msssim"}
    except Exception as exc:  # noqa: BLE001 - optional metric backend may raise third-party errors
        return {"available": False, "reason": f"native MS-SSIM failed: {exc}", "backend": "pytorch-msssim"}


@lru_cache(maxsize=2)
def _lpips_model(net: str):
    import lpips
    model = lpips.LPIPS(net=net)
    model.eval()
    return model


def lpips_distance(reference: Image.Image, candidate: Image.Image, net: str = "alex", device: str = "cpu") -> dict[str, Any]:
    try:
        import lpips  # noqa: F401
        import torch
    except Exception as exc:  # noqa: BLE001 - optional metric backend may raise third-party errors
        return {"available": False, "reason": f"optional dependency unavailable: {exc}"}
    require_same_size(reference, candidate)
    try:
        model = _lpips_model(net).to(device)
        def tensor(img: Image.Image):
            arr = pil_to_rgb_array(img).astype(np.float32) / 127.5 - 1.0
            return torch.from_numpy(arr).permute(2, 0, 1).unsqueeze(0).to(device)
        with torch.no_grad():
            d = model(tensor(reference), tensor(candidate))
        return {"available": True, "distance": float(d.detach().cpu().reshape(-1)[0]), "net": net}
    except Exception as exc:  # noqa: BLE001 - optional metric backend may raise third-party errors
        return {"available": False, "reason": f"LPIPS failed: {exc}", "net": net}


def edge_metrics(reference: Image.Image, candidate: Image.Image, low: int = 80, high: int = 160) -> tuple[dict[str, float], np.ndarray, np.ndarray, np.ndarray]:
    require_same_size(reference, candidate)
    def edges(img):
        gray = pil_to_gray_array(img)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        return cv2.Canny(gray, low, high) > 0
    ea, eb = edges(reference), edges(candidate)
    inter = np.logical_and(ea, eb).sum()
    union = np.logical_or(ea, eb).sum()
    iou = float(inter / union) if union else 1.0
    xor = np.logical_xor(ea, eb)
    diff_ratio = float(xor.mean())
    # A one-pixel tolerance makes the geometry signal less sensitive to antialiasing/rasterization noise.
    kernel = np.ones((3, 3), np.uint8)
    ea_d = cv2.dilate(ea.astype(np.uint8), kernel, iterations=1) > 0
    eb_d = cv2.dilate(eb.astype(np.uint8), kernel, iterations=1) > 0
    ref_count = int(ea.sum()); cand_count = int(eb.sum())
    recall = float(np.logical_and(ea, eb_d).sum() / ref_count) if ref_count else 1.0
    precision = float(np.logical_and(eb, ea_d).sum() / cand_count) if cand_count else 1.0
    f1 = float(2 * precision * recall / (precision + recall)) if precision + recall else 0.0
    return {"edge_iou": iou, "edge_precision_tolerant": precision, "edge_recall_tolerant": recall, "edge_f1_tolerant": f1, "edge_diff_ratio": diff_ratio, "edge_similarity": f1}, ea, eb, xor


def estimate_translation(reference: Image.Image, candidate: Image.Image) -> dict[str, float]:
    require_same_size(reference, candidate)
    a = pil_to_gray_array(reference).astype(np.float32)
    b = pil_to_gray_array(candidate).astype(np.float32)
    # phaseCorrelate returns the translation from src1 to src2. To align candidate to reference use the negative shift.
    (dx, dy), response = cv2.phaseCorrelate(a, b)
    return {
        "candidate_relative_to_reference_dx": float(dx),
        "candidate_relative_to_reference_dy": float(dy),
        "candidate_alignment_dx": float(-dx),
        "candidate_alignment_dy": float(-dy),
        "response": float(response),
    }


def band_error_profile(reference: Image.Image, candidate: Image.Image, bands: int = 8) -> list[dict[str, float]]:
    require_same_size(reference, candidate)
    a = pil_to_rgb_array(reference).astype(np.float32)
    b = pil_to_rgb_array(candidate).astype(np.float32)
    h = a.shape[0]
    result = []
    for i in range(bands):
        y0 = round(i * h / bands)
        y1 = round((i + 1) * h / bands)
        mae = float(np.abs(a[y0:y1] - b[y0:y1]).mean() / 255.0)
        result.append({"band": i, "y0": y0, "y1": y1, "mae": mae})
    return result


def save_diff_artifacts(reference: Image.Image, candidate: Image.Image, out_dir: Path, threshold: int = 16) -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    diff = ImageChops.difference(reference, candidate)
    diff_path = out_dir / "diff.png"
    amp_path = out_dir / "diff-amplified.png"
    overlay_path = out_dir / "overlay.png"
    diff.save(diff_path)
    ImageEnhance.Contrast(diff).enhance(4).save(amp_path)
    Image.blend(reference, candidate, 0.5).save(overlay_path)
    _, _, _, xor = edge_metrics(reference, candidate)
    edge_path = out_dir / "edge-diff.png"
    Image.fromarray(xor.astype(np.uint8) * 255).save(edge_path)
    return {
        "diff": str(diff_path),
        "diff_amplified": str(amp_path),
        "overlay": str(overlay_path),
        "edge_diff": str(edge_path),
    }
