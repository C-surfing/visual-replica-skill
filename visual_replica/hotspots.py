from __future__ import annotations

import cv2
import numpy as np
from PIL import Image, ImageDraw

from .utils import pil_to_rgb_array


def detect_hotspots(reference: Image.Image, candidate: Image.Image, threshold: int = 24, min_area: int = 36, max_items: int = 12):
    a = pil_to_rgb_array(reference).astype(np.int16)
    b = pil_to_rgb_array(candidate).astype(np.int16)
    magnitude = np.max(np.abs(a - b), axis=2).astype(np.uint8)
    mask = (magnitude > threshold).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    items = []
    for idx in range(1, n):
        x, y, w, h, area = map(int, stats[idx])
        if area < min_area:
            continue
        region = magnitude[y:y+h, x:x+w]
        mean_error = float(region.mean() / 255.0)
        impact = float(area * max(mean_error, 1e-6))
        items.append({"x": x, "y": y, "width": w, "height": h, "area": area, "mean_error": mean_error, "impact": impact})
    items.sort(key=lambda x: x["impact"], reverse=True)
    return items[:max_items], mask


def render_hotspots(base: Image.Image, hotspots, path):
    img = base.copy().convert("RGB")
    draw = ImageDraw.Draw(img)
    for i, hs in enumerate(hotspots, start=1):
        x, y, w, h = hs["x"], hs["y"], hs["width"], hs["height"]
        draw.rectangle((x, y, x+w, y+h), outline="red", width=2)
        draw.text((x+3, y+3), str(i), fill="red")
    img.save(path)
