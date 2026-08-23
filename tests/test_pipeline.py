from PIL import Image, ImageDraw
from visual_replica.compare import compare_images
from visual_replica.diagnose import diagnose


def test_compare_and_diagnose(tmp_path):
    a=Image.new("RGB",(160,120),"white");d=ImageDraw.Draw(a);d.rectangle((20,20,100,75),outline="black",width=3)
    b=Image.new("RGB",(160,120),"white");d=ImageDraw.Draw(b);d.rectangle((25,27,105,82),outline="black",width=3)
    rp=tmp_path/"r.png";cp=tmp_path/"c.png";a.save(rp);b.save(cp)
    result=compare_images(rp,cp,tmp_path/"out",lpips_mode="off")
    assert result["status"] == "OK"
    assert result["overall_fidelity"] < 1
    diagnosis=diagnose(result)
    assert diagnosis["status"] == "OK"
    assert len(diagnosis["issues"]) >= 1
