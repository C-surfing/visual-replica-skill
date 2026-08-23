from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image

from .hotspots import detect_hotspots, render_hotspots
from .metrics import (band_error_profile, edge_metrics, estimate_translation, lpips_distance,
                      native_ms_ssim, pixel_metrics, pyramid_ms_ssim, save_diff_artifacts, ssim_score)
from .utils import load_rgb, read_json, write_json


def _crop(img: Image.Image, r: dict[str, Any]):
    x,y,w,h = int(r["x"]), int(r["y"]), int(r["width"]), int(r["height"])
    return img.crop((x,y,x+w,y+h))


def _region_scores(reference, candidate, regions):
    out=[]
    for region in regions:
        rr,cc=_crop(reference,region),_crop(candidate,region)
        p=pixel_metrics(rr,cc)
        e,_,_,_=edge_metrics(rr,cc)
        s=ssim_score(rr,cc) if min(rr.size)>=7 else None
        composite = 0.45*e["edge_similarity"] + 0.30*p["pixel_similarity"] + (0.25*s if s is not None else 0.25*p["pixel_similarity"])
        out.append({"name":region.get("name","region"),"bbox":{k:region[k] for k in ("x","y","width","height")},"critical":bool(region.get("critical",False)),"weight":float(region.get("weight",1.0)),"score":float(composite),"pixel":p,"edge":e,"ssim":s})
    return out


def compare_images(reference_path, candidate_path, out_dir, regions_path=None, threshold=16, lpips_mode="auto", device="cpu"):
    out_dir=Path(out_dir); out_dir.mkdir(parents=True,exist_ok=True)
    ref,cand=load_rgb(reference_path),load_rgb(candidate_path)
    if ref.size != cand.size:
        report={"status":"FAIL","reason":"dimension_mismatch","reference_size":list(ref.size),"candidate_size":list(cand.size)}
        write_json(out_dir/"comparison.json",report)
        return report
    pixel=pixel_metrics(ref,cand,threshold)
    ssim=ssim_score(ref,cand)
    pyramid=pyramid_ms_ssim(ref,cand)
    native=native_ms_ssim(ref,cand,device=device)
    edge,_,_,_=edge_metrics(ref,cand)
    translation=estimate_translation(ref,cand)
    bands=band_error_profile(ref,cand)
    artifacts=save_diff_artifacts(ref,cand,out_dir,threshold)
    hs,_=detect_hotspots(ref,cand,threshold=max(threshold,20))
    hotspot_path=out_dir/"hotspots.png"; render_hotspots(cand,hs,hotspot_path); artifacts["hotspots"]=str(hotspot_path)
    lp={"available":False,"reason":"disabled"}
    if lpips_mode != "off":
        lp=lpips_distance(ref,cand,device=device)
        if lpips_mode == "on" and not lp.get("available"):
            raise RuntimeError(lp.get("reason","LPIPS unavailable"))
    regions=[]
    if regions_path:
        data=read_json(regions_path); defs=data.get("regions",data) if isinstance(data,dict) else data
        regions=_region_scores(ref,cand,defs)
    # Core score deliberately avoids LPIPS because its raw distance has no universal normalization.
    core_score=float(0.35*edge["edge_similarity"] + 0.30*ssim + 0.20*pyramid["score"] + 0.15*pixel["pixel_similarity"])
    if regions:
        total_weight=sum(max(r["weight"], 0.0) for r in regions) or 1.0
        region_mean=sum(r["score"] * max(r["weight"], 0.0) for r in regions) / total_weight
        core_score=0.65*core_score + 0.35*region_mean
        critical=[r for r in regions if r["critical"]]
        if critical:
            critical_floor=min(r["score"] for r in critical)
            core_score=min(core_score, 0.7*core_score+0.3*critical_floor)
    report={
        "status":"OK",
        "reference":str(reference_path),"candidate":str(candidate_path),"size":list(ref.size),
        "overall_fidelity":core_score,
        "metrics":{"pixel":pixel,"ssim":ssim,"ms_ssim_fallback":pyramid,"ms_ssim_native":native,"lpips":lp,"edge":edge},
        "translation":translation,"band_error_profile":bands,"hotspots":hs,"regions":regions,"artifacts":artifacts,
        "interpretation_notes":["LPIPS is reported as a distance and is not mixed into the default fidelity score.","Cross-OS/browser/font rasterization can create irreducible pixel noise."]
    }
    write_json(out_dir/"comparison.json",report)
    return report
