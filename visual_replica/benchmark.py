from __future__ import annotations

from pathlib import Path

from .compare import compare_images
from .utils import read_json, write_json


def run_benchmark(manifest_path, out_path):
    manifest=read_json(manifest_path);results=[]
    for case in manifest.get("cases",[]):
        out_dir=Path(out_path).parent/(case.get("name","case"))
        result=compare_images(case["reference"],case["candidate"],out_dir,regions_path=case.get("regions"),lpips_mode="off")
        results.append({"name":case.get("name"),"status":result.get("status"),"overall_fidelity":result.get("overall_fidelity"),"comparison":str(out_dir/"comparison.json")})
    valid=[r["overall_fidelity"] for r in results if isinstance(r.get("overall_fidelity"),(int,float))]
    report={"cases":results,"mean_fidelity":sum(valid)/len(valid) if valid else None}
    write_json(out_path,report);return report
