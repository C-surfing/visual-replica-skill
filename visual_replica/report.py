from __future__ import annotations

import html, json, shutil
from pathlib import Path
from typing import Any

from .utils import read_json, write_json


def _fmt(v):
    if isinstance(v,float):return f"{v:.4f}"
    return str(v)


def generate_report(comparison_path, diagnosis_path=None, out_dir="report"):
    comp=read_json(comparison_path);diag=read_json(diagnosis_path) if diagnosis_path else {"issues":[]}
    out=Path(out_dir);assets=out/"assets";assets.mkdir(parents=True,exist_ok=True)
    copied={}
    for name,path in comp.get("artifacts",{}).items():
        p=Path(path)
        if p.exists():
            target=assets/p.name;shutil.copy2(p,target);copied[name]=f"assets/{target.name}"
    # Also copy reference/candidate where accessible.
    for key in ("reference","candidate"):
        raw = comp.get(key)
        if not raw:
            continue
        p=Path(raw)
        if p.is_file():
            target=assets/f"{key}{p.suffix or '.png'}";shutil.copy2(p,target);copied[key]=f"assets/{target.name}"
    metrics=comp.get("metrics",{})
    rows=[]
    rows.append(("Overall fidelity",comp.get("overall_fidelity","N/A")))
    rows.append(("SSIM",metrics.get("ssim","N/A")))
    rows.append(("Pixel similarity",metrics.get("pixel",{}).get("pixel_similarity","N/A")))
    rows.append(("Edge similarity",metrics.get("edge",{}).get("edge_similarity","N/A")))
    ms=metrics.get("ms_ssim_native",{});rows.append(("MS-SSIM",ms.get("score",metrics.get("ms_ssim_fallback",{}).get("score","N/A"))))
    lp=metrics.get("lpips",{});rows.append(("LPIPS distance",lp.get("distance",lp.get("reason","not available"))))
    metric_html="".join(f"<tr><th>{html.escape(str(k))}</th><td>{html.escape(_fmt(v))}</td></tr>" for k,v in rows)
    issue_html="".join(f"<article class='issue {html.escape(i.get('severity',''))}'><h3>{html.escape(i.get('pattern','issue'))}</h3><p><b>Severity:</b> {html.escape(i.get('severity',''))}</p><p><b>Causes:</b> {html.escape(', '.join(i.get('probable_causes',[])))}</p><p><b>Code area:</b> {html.escape(', '.join(i.get('recommended_code_area',[])))}</p><pre>{html.escape(json.dumps(i.get('evidence',{}),indent=2))}</pre></article>" for i in diag.get("issues",[])) or "<p>No rule-based critical issue detected.</p>"
    region_html="".join(f"<tr><td>{html.escape(r.get('name',''))}</td><td>{r.get('score',0):.4f}</td><td>{'yes' if r.get('critical') else 'no'}</td></tr>" for r in comp.get("regions",[])) or "<tr><td colspan='3'>No explicit regions configured.</td></tr>"
    imgs=[]
    for key,label in (("reference","Reference"),("candidate","Candidate"),("diff_amplified","Amplified diff"),("edge_diff","Edge diff"),("hotspots","Hotspots")):
        if key in copied:imgs.append(f"<figure><img src='{html.escape(copied[key])}'><figcaption>{label}</figcaption></figure>")
    page=f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Visual Replica Report</title><style>body{{font-family:system-ui,sans-serif;max-width:1200px;margin:auto;padding:24px;line-height:1.45}}.score{{font-size:2rem;font-weight:700}}table{{border-collapse:collapse;width:100%}}th,td{{padding:8px;border-bottom:1px solid #ddd;text-align:left}}.gallery{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}}img{{max-width:100%;border:1px solid #ddd}}figure{{margin:0}}.issue{{padding:12px 16px;border-left:4px solid #888;background:#fafafa;margin:12px 0}}.issue.critical{{border-color:#b00020}}.issue.high{{border-color:#d66b00}}pre{{white-space:pre-wrap}}</style></head><body><h1>Visual Replica Report</h1><div class="score">Fidelity: {_fmt(comp.get('overall_fidelity','N/A'))}</div><h2>Metrics</h2><table>{metric_html}</table><h2>Visual evidence</h2><div class="gallery">{''.join(imgs)}</div><h2>Regions</h2><table><tr><th>Region</th><th>Score</th><th>Critical</th></tr>{region_html}</table><h2>Diagnosis</h2>{issue_html}</body></html>"""
    (out/"index.html").write_text(page,encoding="utf-8")
    write_json(out/"comparison.json",comp);write_json(out/"diagnosis.json",diag)
    return out/"index.html"
