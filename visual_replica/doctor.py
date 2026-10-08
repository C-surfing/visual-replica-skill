from __future__ import annotations

import importlib.util
import shutil


def doctor():
    mods={m:bool(importlib.util.find_spec(m)) for m in ["PIL","numpy","skimage","cv2","torch","pytorch_msssim","lpips","pytesseract","paddleocr"]}
    return {"python_modules":mods,"executables":{"node":bool(shutil.which("node")),"tesseract":bool(shutil.which("tesseract"))},"notes":["core compare requires Pillow/NumPy/scikit-image/OpenCV","LPIPS and native MS-SSIM are optional","OCR is optional"]}
