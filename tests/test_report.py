from visual_replica.report import generate_report
from visual_replica.utils import write_json


def test_report(tmp_path):
    c=tmp_path/"comparison.json";d=tmp_path/"diagnosis.json"
    write_json(c,{"status":"OK","overall_fidelity":0.95,"metrics":{"ssim":0.96,"pixel":{"pixel_similarity":0.94},"edge":{"edge_similarity":0.95},"ms_ssim_fallback":{"score":0.95},"ms_ssim_native":{"available":False},"lpips":{"available":False,"reason":"optional"}},"artifacts":{},"regions":[]})
    write_json(d,{"issues":[]})
    out=generate_report(c,d,tmp_path/"report")
    assert out.exists()
    assert "Visual Replica Report" in out.read_text(encoding="utf-8")
