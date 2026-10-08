from types import SimpleNamespace

from PIL import Image
import yaml

from visual_replica.utils import write_json
from visual_replica.verify import verify_contract


def contract(reference=True, threshold=True, preserve=False):
    scenario = {
        "id": "desktop", "url": "http://localhost:3000/",
        "viewport": {"width": 320, "height": 240},
        "assertions": [{"selector": "#cta", "condition": "visible"}],
    }
    if reference:
        scenario["reference"] = "reference.png"
    if threshold:
        scenario["min_fidelity"] = 0.9
    if preserve:
        intent = {"preserve": [{"text": "Preserve CTA hierarchy", "provenance": "user-confirmed"}]}
    else:
        intent = {}
    return {
        "version": 1, "mode": "transfer",
        "source": {"approved": True},
        "intent": intent,
        "checks": {"scenarios": [scenario]},
    }


def runner(status="PASS"):
    def simulate(command, **kwargs):
        _, _, _, evidence, screenshot = command
        Image.new("RGB", (320, 240), "white").save(screenshot)
        write_json(evidence, {
            "status": status,
            "assertions": [{"selector": "#cta", "condition": "visible", "passed": status == "PASS"}],
            "dom": [],
        })
        return SimpleNamespace(returncode=0, stdout="", stderr="")
    return simulate


def comparator(reference, candidate, output, **kwargs):
    return {"status": "OK", "overall_fidelity": 0.96}


def run(tmp_path, doc, fake=runner()):
    spec = tmp_path / "intent.yaml"
    spec.write_text(yaml.safe_dump(doc), encoding="utf-8")
    Image.new("RGB", (320, 240), "white").save(tmp_path / "reference.png")
    return verify_contract(spec, tmp_path / "results", runner=fake, comparator=comparator)


def test_all_explicit_checks_pass(tmp_path):
    result = run(tmp_path, contract())
    assert result["status"] == "PASS"
    assert result["scenarios"][0]["visual"]["status"] == "PASS"
    assert (tmp_path / "results" / "index.html").is_file()


def test_no_calibrated_threshold_needs_review(tmp_path):
    result = run(tmp_path, contract(threshold=False))
    assert result["status"] == "REVIEW_REQUIRED"


def test_qualitative_intent_cannot_be_automatically_certified(tmp_path):
    result = run(tmp_path, contract(preserve=True))
    assert result["status"] == "REVIEW_REQUIRED"
    assert "Preserve CTA hierarchy" in result["manual_review"][0]


def test_browser_assertion_failure_is_not_masked_by_good_visual_score(tmp_path):
    result = run(tmp_path, contract(), fake=runner("FAIL"))
    assert result["status"] == "FAIL"


def test_missing_reference_is_error_not_success(tmp_path):
    doc = contract()
    doc["checks"]["scenarios"][0]["reference"] = "missing.png"
    result = run(tmp_path, doc)
    assert result["status"] == "ERROR"


def test_no_reference_is_not_a_visual_pass(tmp_path):
    result = run(tmp_path, contract(reference=False, threshold=False))
    assert result["status"] == "REVIEW_REQUIRED"


def test_report_escapes_contract_text(tmp_path):
    doc = contract(preserve=True)
    doc["intent"]["preserve"][0]["text"] = "<script>alert(1)</script>"
    run(tmp_path, doc)
    html = (tmp_path / "results" / "index.html").read_text(encoding="utf-8")
    assert "&lt;script&gt;" in html
    assert "<script>" not in html
