"""Run explicit design-contract scenarios and produce evidence without false PASS claims."""
from __future__ import annotations

import html
import json
import subprocess
from pathlib import Path
from typing import Any

from .compare import compare_images
from .continuity import render_brief
from .intent import load_contract
from .utils import read_json, write_json


def _resolve(spec_path: Path, relative: str) -> Path:
    path = Path(relative)
    return path if path.is_absolute() else spec_path.parent / path


def _scenario_status(evidence: dict[str, Any], visual: dict[str, Any]) -> str:
    if evidence.get("status") == "ERROR" or visual.get("status") == "ERROR":
        return "ERROR"
    if evidence.get("status") == "FAIL" or visual.get("status") == "FAIL":
        return "FAIL"
    if visual.get("status") != "PASS":
        return "REVIEW_REQUIRED"
    return "PASS"


def _overall_status(scenarios: list[dict[str, Any]], review_items: list[str]) -> str:
    statuses = [s["status"] for s in scenarios]
    if "ERROR" in statuses:
        return "ERROR"
    if "FAIL" in statuses:
        return "FAIL"
    if not statuses or "REVIEW_REQUIRED" in statuses or review_items:
        return "REVIEW_REQUIRED"
    return "PASS"


def verify_contract(
    spec_path: str | Path,
    out_dir: str | Path = ".visual-replica/verification",
    *,
    runner: Any = None,
    comparator: Any = None,
) -> dict[str, Any]:
    """Execute scenarios; injectable runner/comparator enable deterministic tests.

    A numerical similarity never verifies qualitative design intent. Anything
    without an explicit assertion/threshold remains REVIEW_REQUIRED.
    """
    spec_path = Path(spec_path).resolve()
    contract = load_contract(spec_path)
    output = Path(out_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    script = Path(__file__).resolve().parent / "assets" / "verify.mjs"
    runner = runner or subprocess.run
    comparator = comparator or compare_images
    results: list[dict[str, Any]] = []

    for scenario in contract.get("checks", {}).get("scenarios", []):
        name = scenario["id"]  # validated as a safe directory name
        folder = output / name
        folder.mkdir(parents=True, exist_ok=True)
        spec_file = write_json(folder / "scenario.json", scenario)
        evidence_file = folder / "evidence.json"
        screenshot = folder / "screenshot.png"
        evidence: dict[str, Any] = {"status": "ERROR"}
        visual: dict[str, Any] = {"status": "NOT_CHECKED", "reason": "No reference image"}
        try:
            process = runner(
                ["node", str(script), str(spec_file), str(evidence_file), str(screenshot)],
                capture_output=True, text=True, timeout=90, check=False,
            )
            if evidence_file.is_file():
                evidence = read_json(evidence_file)
            else:
                evidence = {
                    "status": "ERROR",
                    "error": (process.stderr or process.stdout or "Browser evidence missing").strip(),
                }
            if process.returncode != 0 and evidence.get("status") != "ERROR":
                evidence = {**evidence, "status": "ERROR", "error": f"Browser exited {process.returncode}"}
            if evidence.get("status") != "ERROR" and scenario.get("reference"):
                reference = _resolve(spec_path, scenario["reference"])
                if not reference.is_file():
                    visual = {"status": "ERROR", "reason": f"Reference not found: {reference}"}
                else:
                    regions = scenario.get("regions")
                    regions_file = _resolve(spec_path, regions) if regions else None
                    if regions_file is not None and not regions_file.is_file():
                        visual = {"status": "ERROR", "reason": f"Regions not found: {regions_file}"}
                    else:
                        comparison = comparator(
                            reference, screenshot, folder / "compare",
                            regions_path=regions_file, lpips_mode="off",
                        )
                        threshold = scenario.get("min_fidelity")
                        if comparison.get("status") != "OK":
                            visual = {"status": "FAIL", "reason": comparison.get("reason", "comparison failed")}
                        elif threshold is None:
                            visual = {
                                "status": "REVIEW_REQUIRED",
                                "fidelity": comparison["overall_fidelity"],
                                "reason": "Reference compared; no calibrated acceptance threshold",
                            }
                        else:
                            score = comparison["overall_fidelity"]
                            visual = {
                                "status": "PASS" if score >= threshold else "FAIL",
                                "fidelity": score, "threshold": threshold,
                                "reason": "Threshold is user-supplied and not a universal design-quality score",
                            }
        except (OSError, subprocess.TimeoutExpired, ValueError, RuntimeError) as exc:
            evidence = {"status": "ERROR", "error": str(exc)}
        results.append({
            "id": name, "status": _scenario_status(evidence, visual),
            "browser": evidence, "visual": visual,
            "evidence_path": str(evidence_file),
            "screenshot_path": str(screenshot) if screenshot.is_file() else None,
        })

    intent = contract.get("intent", {})
    review_items = [
        f"preserve: {item['text']} (provenance: {item['provenance']})"
        for item in intent.get("preserve", [])
    ]
    review_items += [f"avoid: {s}" for s in intent.get("avoid", [])]
    if contract.get("source", {}).get("approved") is not True:
        review_items.append("Source or design direction has not been explicitly approved")
    report = {
        "contract_version": 1,
        "mode": contract["mode"],
        "status": _overall_status(results, review_items),
        "scenarios": results,
        "manual_review": review_items,
        "notes": [
            "Automated checks cover declared assertions and calibrated visual thresholds only.",
            "Qualitative design intent is never automatically certified by image metrics.",
            "A generated baseline is not accepted or updated by this command.",
        ],
    }
    write_json(output / "verification.json", report)
    _render_report(report, output)
    briefing = render_brief(contract, lang="zh")
    status_note = ("已发现明确未通过的检查，仍需修正。"
                   if report["status"] == "FAIL" else
                   "检查未能正常完成，需要处理运行问题。"
                   if report["status"] == "ERROR" else
                   "已声明的自动检查完成，但这不代表设计已经得到你的认可。"
                   if report["status"] == "PASS" else
                   "部分审美选择仍待确认；没有截图或自动检查时也可以继续完善设计。")
    pending_lines = []
    for item in intent.get("preserve", []):
        if item["provenance"] == "user-confirmed":
            pending_lines.append(f"- 仍需看看实际作品有没有保留「{item['text']}」。")
        else:
            pending_lines.append(f"- 还需要你确认：是否希望「{item['text']}」？")
    for item in intent.get("avoid", []):
        pending_lines.append(f"- 需要留意有没有出现你不喜欢的「{item}」。")
    for question in contract.get("open_questions", []):
        pending_lines.append(f"- 尚待决定：{question}")
    pending = "\n".join(pending_lines)
    if not results:
        status_note = "目前还没有需要自动检查的页面，可以先继续确认想要的设计体验。"
    (output / "design-update.zh.md").write_text(
        briefing + "\n## 当前进展\n\n" + status_note + "\n\n"
        + ("## 仍需判断的地方\n\n" + pending + "\n" if pending else ""),
        encoding="utf-8",
    )
    return report


def _render_report(report: dict[str, Any], folder: Path) -> Path:
    def esc(value: Any) -> str:
        return html.escape(str(value), quote=True)

    rows = []
    for scenario in report["scenarios"]:
        name = scenario["id"]
        image = (
            f'<a href="{esc(name)}/screenshot.png">Screenshot</a>'
            if scenario["screenshot_path"] else "Not captured"
        )
        comparison = folder / name / "compare" / "comparison.json"
        visual_link = (
            f'<a href="{esc(name)}/compare/comparison.json">Comparison JSON</a>'
            if comparison.is_file() else "No comparison"
        )
        rows.append(
            f"<tr><td>{esc(name)}</td><td>{esc(scenario['status'])}</td>"
            f"<td>{esc(scenario['browser'].get('status'))}</td>"
            f"<td>{esc(scenario['visual'].get('status'))}</td>"
            f"<td>{image} · {visual_link}</td></tr>"
        )
    pending = "".join(f"<li>{esc(item)}</li>" for item in report["manual_review"])
    payload = esc(json.dumps(report["notes"], ensure_ascii=False))
    page = f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Visual Replica Verification</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;max-width:1100px;margin:auto;padding:28px}}
table{{border-collapse:collapse;width:100%}}td,th{{padding:10px;border-bottom:1px solid #ddd;text-align:left}}
.status{{font-size:1.5rem;font-weight:bold}}code{{background:#eee;padding:2px}}</style>
<h1>Visual Replica · Evidence Report</h1>
<p class="status">Overall: {esc(report['status'])}</p>
<p>Mode: <code>{esc(report['mode'])}</code>. Review individual checks before approving a design.</p>
<table><thead><tr><th>Scenario</th><th>Status</th><th>Browser</th><th>Visual</th><th>Artifacts</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
<h2>Human review remaining</h2><ul>{pending or '<li>No declared qualitative constraints</li>'}</ul>
<h2>Evidence policy</h2><p>{payload}</p>
<p>Machine-readable detail: <a href="verification.json">verification.json</a></p></html>
"""
    path = folder / "index.html"
    path.write_text(page, encoding="utf-8")
    return path
