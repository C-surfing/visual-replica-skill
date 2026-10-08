from PIL import Image, ImageDraw

from visual_replica.metrics import edge_metrics, estimate_translation, pixel_metrics, pyramid_ms_ssim, ssim_score


def sample(shift=(0,0)):
    img=Image.new("RGB",(160,120),"white");d=ImageDraw.Draw(img);dx,dy=shift
    d.rectangle((20+dx,20+dy,100+dx,75+dy),fill=(230,230,230),outline="black",width=2)
    d.text((30+dx,35+dy),"UI",fill="black")
    return img


def test_identical_metrics_are_high():
    a=sample();b=sample()
    assert pixel_metrics(a,b)["pixel_similarity"] == 1.0
    assert ssim_score(a,b) > 0.999
    assert pyramid_ms_ssim(a,b)["score"] > 0.999
    assert edge_metrics(a,b)[0]["edge_iou"] > 0.999


def test_shift_reduces_similarity_and_translation_is_detected():
    a=sample();b=sample((5,7))
    assert ssim_score(a,b) < 0.99
    tr=estimate_translation(a,b)
    assert abs(tr["candidate_relative_to_reference_dx"]-5) < 1.5
    assert abs(tr["candidate_relative_to_reference_dy"]-7) < 1.5
