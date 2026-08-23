from __future__ import annotations

from pathlib import Path
from typing import Any

from .utils import read_json, write_json

CODE_EXTS={".css",".scss",".less",".tsx",".ts",".jsx",".js",".vue",".svelte",".dart",".wxml",".wxss",".swift",".kt",".xml"}


def _trend(bands):
    vals=[b.get("mae",0.0) for b in bands]
    if len(vals)<4:return 0.0
    n=len(vals); xs=list(range(n)); xmean=sum(xs)/n; ymean=sum(vals)/n
    num=sum((x-xmean)*(y-ymean) for x,y in zip(xs,vals)); den=sum((x-xmean)**2 for x in xs) or 1
    return num/den


def _repo_candidates(repo: str|None, keywords: list[str], limit=20):
    if not repo:return []
    root=Path(repo)
    scored=[]
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in CODE_EXTS:continue
        rel=str(p.relative_to(root))
        low=rel.lower(); score=sum(3 for k in keywords if k and k.lower() in low)
        if score==0 and p.stat().st_size < 1_000_000:
            try:
                txt=p.read_text(encoding="utf-8",errors="ignore").lower()
                score+=sum(1 for k in keywords if k and k.lower() in txt)
            except Exception:pass
        if score:scored.append((score,rel))
    scored.sort(key=lambda x:(-x[0],x[1]))
    return [{"file":rel,"score":score} for score,rel in scored[:limit]]


def diagnose(comparison: dict[str,Any], repo: str|None=None):
    if comparison.get("status")!="OK":
        return {"status":"FAIL","issues":[{"pattern":comparison.get("reason","comparison_failed"),"severity":"critical","probable_causes":["viewport/state mismatch"],"recommended_code_area":["capture configuration","root layout"]}]}
    issues=[]
    t=comparison.get("translation",{}); dx=t.get("candidate_alignment_dx",0);dy=t.get("candidate_alignment_dy",0);resp=t.get("response",0)
    if resp>0.12 and (abs(dx)>=2 or abs(dy)>=2):
        issues.append({"pattern":"global_offset","severity":"high","evidence":{"alignment_dx":dx,"alignment_dy":dy,"phase_response":resp},"probable_causes":["root/container offset","safe-area or navigation height","wrong reference viewport/state"],"recommended_code_area":["page shell","root layout","navigation/safe-area wrapper"],"repo_candidates":_repo_candidates(repo,["layout","shell","app","page","nav","container"])})
    slope=_trend(comparison.get("band_error_profile",[]))
    if slope>0.004:
        issues.append({"pattern":"vertical_drift","severity":"high","evidence":{"band_mae_slope":slope},"probable_causes":["repeated gap/margin accumulation","line-height mismatch","shared component height mismatch"],"recommended_code_area":["spacing tokens","shared list/card component","typography line-height"],"repo_candidates":_repo_candidates(repo,["card","list","spacing","token","typography"])})
    metrics=comparison.get("metrics",{}); edge=metrics.get("edge",{}).get("edge_similarity",1); ssim=metrics.get("ssim",1); pix=metrics.get("pixel",{}).get("pixel_similarity",1)
    if ssim>0.94 and edge>0.92 and pix<0.94:
        issues.append({"pattern":"appearance_or_rasterization","severity":"medium","evidence":{"ssim":ssim,"edge_similarity":edge,"pixel_similarity":pix},"probable_causes":["color/theme mismatch","font antialiasing/rendering environment","subtle shadow/border differences"],"recommended_code_area":["design tokens","theme/colors","typography/font loading"],"repo_candidates":_repo_candidates(repo,["theme","color","token","font","typography"])})
    hs=comparison.get("hotspots",[])
    if len(hs)>=2:
        top=hs[:6]; ws=[h["width"] for h in top];hsz=[h["height"] for h in top]
        if max(ws)-min(ws) <= max(6,0.12*sum(ws)/len(ws)) and max(hsz)-min(hsz) <= max(6,0.12*sum(hsz)/len(hsz)):
            issues.append({"pattern":"repeated_component_geometry","severity":"high","evidence":{"similar_hotspot_count":len(top)},"probable_causes":["shared component geometry/token mismatch"],"recommended_code_area":["repeated card/list/button component","component-level styles"],"repo_candidates":_repo_candidates(repo,["card","item","button","component"])})
    for r in comparison.get("regions",[]):
        if r.get("critical") and r.get("score",1)<0.90:
            name=r.get("name","critical region")
            issues.append({"pattern":"critical_region_failure","severity":"critical","region":name,"evidence":{"score":r["score"]},"probable_causes":["region-specific geometry, typography or asset mismatch"],"recommended_code_area":[name],"repo_candidates":_repo_candidates(repo,[name.replace("-"," ").replace("_"," "),name])})
    if not issues and comparison.get("overall_fidelity",0)<0.96:
        issues.append({"pattern":"distributed_micro_mismatch","severity":"medium","evidence":{"overall_fidelity":comparison.get("overall_fidelity")},"probable_causes":["typography/assets/micro-spacing","rendering-environment differences"],"recommended_code_area":["largest hotspot first"],"repo_candidates":[]})
    return {"status":"OK","overall_fidelity":comparison.get("overall_fidelity"),"issues":issues,"next_action":"Fix the highest-severity/highest-impact root cause, recapture, and compare again."}


def diagnose_file(comparison_path, out_path, repo=None):
    result=diagnose(read_json(comparison_path),repo=repo);write_json(out_path,result);return result
