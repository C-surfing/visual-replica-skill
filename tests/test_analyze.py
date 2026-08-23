from PIL import Image, ImageDraw
from visual_replica.analyze import analyze_reference


def test_analyze_without_ocr(tmp_path):
    p=tmp_path/"ref.png";img=Image.new("RGB",(180,120),(245,245,245));d=ImageDraw.Draw(img);d.rectangle((20,20,160,90),fill=(255,255,255),outline=(10,10,10));img.save(p)
    r=analyze_reference(p,ocr_backend="none",colors=3)
    assert r["viewport_pixels"] == {"width":180,"height":120}
    assert len(r["dominant_colors"]) >= 1
    assert isinstance(r["layout_regions"],list)
