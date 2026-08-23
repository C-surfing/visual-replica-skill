from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image


def load_rgb(path: str | Path) -> Image.Image:
    return Image.open(path).convert("RGB")


def pil_to_rgb_array(img: Image.Image) -> np.ndarray:
    return np.asarray(img.convert("RGB"))


def pil_to_gray_array(img: Image.Image) -> np.ndarray:
    return cv2.cvtColor(pil_to_rgb_array(img), cv2.COLOR_RGB2GRAY)


def write_json(path: str | Path, data: Any) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def clamp01(v: float) -> float:
    return float(max(0.0, min(1.0, v)))
