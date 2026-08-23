from __future__ import annotations

import argparse, json, subprocess, sys
from pathlib import Path

from .analyze import analyze_reference
from .benchmark import run_benchmark
from .compare import compare_images
from .diagnose import diagnose_file
from .doctor import doctor
from .report import generate_report
from .utils import write_json


def _print(data):print(json.dumps(data,indent=2,ensure_ascii=False,default=str))


def main(argv=None):
    p=argparse.ArgumentParser(prog="visual-replica",description="Skill companion toolkit for high-fidelity UI reconstruction")
    sub=p.add_subparsers(dest="command",required=True)
    sp=sub.add_parser("doctor")
    sp=sub.add_parser("init");sp.add_argument("directory",nargs="?",default=".visual-replica")
    sp=sub.add_parser("analyze");sp.add_argument("image");sp.add_argument("--out",default=".visual-replica/reference-analysis.json");sp.add_argument("--ocr",choices=["auto","paddle","tesseract","none"],default="auto");sp.add_argument("--colors",type=int,default=8)
    sp=sub.add_parser("compare");sp.add_argument("reference");sp.add_argument("candidate");sp.add_argument("--out-dir",default=".visual-replica/compare");sp.add_argument("--regions");sp.add_argument("--threshold",type=int,default=16);sp.add_argument("--lpips",choices=["auto","off","on"],default="auto");sp.add_argument("--device",default="cpu")
    sp=sub.add_parser("diagnose");sp.add_argument("comparison");sp.add_argument("--repo");sp.add_argument("--out",default=".visual-replica/diagnosis.json")
    sp=sub.add_parser("report");sp.add_argument("--comparison",required=True);sp.add_argument("--diagnosis");sp.add_argument("--out-dir",default=".visual-replica/report")
    sp=sub.add_parser("benchmark");sp.add_argument("manifest");sp.add_argument("--out",default=".visual-replica/benchmark.json")
    sp=sub.add_parser("capture");sp.add_argument("url");sp.add_argument("--width",type=int,default=390);sp.add_argument("--height",type=int,default=844);sp.add_argument("--dpr",type=float,default=1);sp.add_argument("--out",default=".visual-replica/candidate.png");sp.add_argument("--selector");sp.add_argument("--full-page",action="store_true");sp.add_argument("--wait-ms",type=int,default=250);sp.add_argument("--mask",default="")
    a=p.parse_args(argv)
    if a.command=="doctor":_print(doctor());return 0
    if a.command=="init":
        root=Path(a.directory);[(root/d).mkdir(parents=True,exist_ok=True) for d in ["reference","candidate","compare","report"]]
        cfg={"viewport":{"width":390,"height":844,"dpr":1},"comparison":{"pixel_threshold":16,"lpips":"auto"}}
        write_json(root/"config.json",cfg);_print({"status":"OK","workspace":str(root)});return 0
    if a.command=="analyze":
        r=analyze_reference(a.image,a.ocr,a.colors);write_json(a.out,r);_print(r);return 0
    if a.command=="compare":
        r=compare_images(a.reference,a.candidate,a.out_dir,a.regions,a.threshold,a.lpips,a.device);_print(r);return 0 if r.get("status")=="OK" else 2
    if a.command=="diagnose":r=diagnose_file(a.comparison,a.out,a.repo);_print(r);return 0
    if a.command=="report":path=generate_report(a.comparison,a.diagnosis,a.out_dir);_print({"status":"OK","report":str(path)});return 0
    if a.command=="benchmark":r=run_benchmark(a.manifest,a.out);_print(r);return 0
    if a.command=="capture":
        script=Path(__file__).resolve().parent/"assets"/"capture.mjs"
        cmd=["node",str(script),"--url",a.url,"--width",str(a.width),"--height",str(a.height),"--dpr",str(a.dpr),"--out",a.out,"--wait-ms",str(a.wait_ms)]
        if a.selector:cmd += ["--selector",a.selector]
        if a.full_page:cmd += ["--full-page"]
        if a.mask:cmd += ["--mask",a.mask]
        try:return subprocess.call(cmd)
        except FileNotFoundError:
            print("Node.js was not found. Run visual-replica doctor.",file=sys.stderr);return 3
    return 1


if __name__=="__main__":raise SystemExit(main())
