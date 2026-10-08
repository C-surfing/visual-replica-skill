from __future__ import annotations

from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image

from .utils import load_rgb, pil_to_rgb_array


def dominant_colors(img: Image.Image, k: int = 8, max_samples: int = 40000) -> list[dict[str, Any]]:
    rgb = pil_to_rgb_array(img)
    flat = rgb.reshape(-1, 3)
    if len(flat) > max_samples:
        idx = np.linspace(0, len(flat)-1, max_samples, dtype=np.int64)
        flat = flat[idx]
    lab = cv2.cvtColor(flat.reshape(-1, 1, 3), cv2.COLOR_RGB2LAB).reshape(-1, 3).astype(np.float32)
    k = max(1, min(k, len(lab)))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.5)
    _, labels, centers = cv2.kmeans(lab, k, None, criteria, 3, cv2.KMEANS_PP_CENTERS)
    counts = np.bincount(labels.reshape(-1), minlength=k)
    rgb_centers = cv2.cvtColor(np.uint8(centers.reshape(1, -1, 3)), cv2.COLOR_LAB2RGB).reshape(-1, 3)
    order = np.argsort(counts)[::-1]
    total = counts.sum()
    out = []
    for i in order:
        color = [int(v) for v in rgb_centers[i]]
        out.append({"rgb": color, "hex": f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}", "fraction": float(counts[i]/total)})
    return out


def layout_regions(img: Image.Image, min_area_ratio: float = 0.001, max_regions: int = 80) -> list[dict[str, Any]]:
    rgb = pil_to_rgb_array(img)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(cv2.GaussianBlur(gray, (3,3), 0), 50, 130)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    merged = cv2.dilate(edges, kernel, iterations=1)
    contours, _ = cv2.findContours(merged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    image_area = img.width * img.height
    regions = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = w*h
        if area < image_area * min_area_ratio:
            continue
        if w < 6 or h < 6:
            continue
        regions.append({"x": int(x), "y": int(y), "width": int(w), "height": int(h), "area_ratio": float(area/image_area)})
    regions.sort(key=lambda r: r["width"] * r["height"], reverse=True)
    return regions[:max_regions]


def _ocr_tesseract(img: Image.Image):
    import pytesseract
    from pytesseract import Output
    data = pytesseract.image_to_data(img, output_type=Output.DICT)
    out = []
    for i, text in enumerate(data["text"]):
        text = text.strip()
        conf_raw = data["conf"][i]
        try: conf = float(conf_raw)
        except (TypeError, ValueError): conf = -1
        if not text or conf < 0:
            continue
        out.append({"text": text, "confidence": conf/100.0, "bbox": [int(data["left"][i]), int(data["top"][i]), int(data["width"][i]), int(data["height"][i])]})
    return out


def _ocr_paddle(img_path: str | Path):
    from paddleocr import PaddleOCR
    ocr = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False)
    result = ocr.predict(str(img_path))
    out = []
    # PaddleOCR APIs have evolved; normalize defensively from dictionary-like result objects.
    for item in result:
        data = getattr(item, "json", None)
        if callable(data): data = data()
        if not isinstance(data, dict):
            continue
        payload = data.get("res", data)
        texts = payload.get("rec_texts", [])
        scores = payload.get("rec_scores", [])
        boxes = payload.get("rec_boxes", [])
        for t, s, box in zip(texts, scores, boxes):
            x0,y0,x1,y1 = [int(v) for v in box]
            out.append({"text": str(t), "confidence": float(s), "bbox": [x0,y0,x1-x0,y1-y0]})
    return out


def run_ocr(image_path: str | Path, backend: str = "auto") -> dict[str, Any]:
    backend = backend.lower()
    if backend == "none":
        return {"backend": "none", "available": True, "items": []}
    errors = []
    if backend in ("auto", "paddle"):
        try:
            return {"backend": "paddle", "available": True, "items": _ocr_paddle(image_path)}
        except Exception as exc:  # noqa: BLE001 - optional OCR backend may raise third-party errors
            errors.append(f"paddle: {exc}")
            if backend == "paddle": return {"backend": "paddle", "available": False, "reason": str(exc), "items": []}
    if backend in ("auto", "tesseract"):
        try:
            return {"backend": "tesseract", "available": True, "items": _ocr_tesseract(load_rgb(image_path))}
        except Exception as exc:  # noqa: BLE001 - optional OCR backend may raise third-party errors
            errors.append(f"tesseract: {exc}")
            if backend == "tesseract": return {"backend": "tesseract", "available": False, "reason": str(exc), "items": []}
    return {"backend": "none", "available": False, "reason": "; ".join(errors) or "no OCR backend", "items": []}


def propose_components(regions: list[dict[str, Any]], ocr_items: list[dict[str, Any]], width: int, height: int):
    proposals = []
    def inside(box, region):
        x,y,w,h = box; rx,ry,rw,rh = region["x"],region["y"],region["width"],region["height"]
        cx,cy = x+w/2,y+h/2
        return rx <= cx <= rx+rw and ry <= cy <= ry+rh
    sizes = [(r["width"], r["height"]) for r in regions]
    for idx, r in enumerate(regions):
        text_count = sum(1 for t in ocr_items if inside(t.get("bbox", [0,0,0,0]), r))
        similar = sum(1 for w,h in sizes if abs(w-r["width"]) <= max(4, r["width"]*0.08) and abs(h-r["height"]) <= max(4, r["height"]*0.08))
        label = "container_candidate"
        if r["y"] < height*0.18 and r["width"] > width*0.6 and r["height"] < height*0.25:
            label = "header_candidate"
        elif similar >= 2 and text_count >= 1:
            label = "repeated_component_candidate"
        elif text_count >= 2 and r["width"] < width*0.8:
            label = "card_candidate"
        proposals.append({"region_index": idx, "type": label, "text_count": text_count, "similar_region_count": similar, "bbox": [r["x"],r["y"],r["width"],r["height"]]})
    return proposals[:40]


def analyze_reference(image_path: str | Path, ocr_backend: str = "auto", colors: int = 8) -> dict[str, Any]:
    img = load_rgb(image_path)
    ocr = run_ocr(image_path, ocr_backend)
    regions = layout_regions(img)
    return {
        "image": str(image_path),
        "viewport_pixels": {"width": img.width, "height": img.height},
        "dominant_colors": dominant_colors(img, colors),
        "ocr": ocr,
        "layout_regions": regions,
        "component_proposals": propose_components(regions, ocr.get("items", []), img.width, img.height),
        "notes": ["layout/component proposals are heuristic evidence, not semantic ground truth"]
    }
