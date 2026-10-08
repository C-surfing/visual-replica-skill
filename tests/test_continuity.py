import copy

import pytest
import yaml

from visual_replica.continuity import guard_confirmed_decisions, render_brief, render_guard
from visual_replica.intent import ContractError, init_contract, load_contract, validate_contract
from visual_replica.verify import verify_contract


def sample():
    return {
        "version": 1, "mode": "transfer", "source": {"approved": True},
        "direction": {"product": "Reading tool", "desired_feeling": "Calm"},
        "references": [
            {"id": "layout", "source": "reference A", "borrow": "Whitespace",
             "not_copy": "Colors", "why": "Less noise"}
        ],
        "intent": {
            "preserve": [
                {"id": "calm", "text": "Keep the reader central",
                 "reason": "Avoid dashboard density", "provenance": "user-confirmed",
                 "critical": True}
            ], "avoid": ["Busy card grids"], "allowed_changes": ["Mobile layout"]
        },
        "open_questions": ["Which font?"],
        "iterations": [{"round": 1, "user_feedback": "Too many panels",
                        "agreed_change": "Simplify the sidebar", "status": "proposed"}],
        "checks": {"scenarios": []},
    }


def test_creative_brief_needs_no_browser(tmp_path):
    contract = sample()
    assert validate_contract(contract) is contract
    path = tmp_path / "intent.yaml"
    path.write_text(yaml.safe_dump(contract), encoding="utf-8")
    result = verify_contract(path, tmp_path / "output")
    assert result["status"] == "REVIEW_REQUIRED"
    assert result["scenarios"] == []
    narrative = (tmp_path / "output" / "design-update.zh.md").read_text(encoding="utf-8")
    assert "Reading tool" in narrative
    assert "截图" in narrative
    assert "Which font?" in narrative


def test_default_template_is_creative_not_screenshot_task(tmp_path):
    path = tmp_path / "intent.yaml"
    init_contract(path)
    contract = load_contract(path)
    assert contract["checks"]["scenarios"] == []
    assert len(contract["references"]) == 2
    assert "待你确认" in render_brief(contract)


def test_guard_detects_silent_change_to_approved_taste():
    old = sample()
    new = copy.deepcopy(old)
    new["intent"]["preserve"][0]["text"] = "Make metrics central"
    result = guard_confirmed_decisions(old, new)
    assert result["status"] == "REVIEW_REQUIRED"
    assert "calm.text" in result["changes"][0]["what"]
    assert "需要你决定是否更改" in render_guard(result)


def test_guard_detects_changed_approved_reference():
    old = sample()
    new = copy.deepcopy(old)
    new["references"][0]["borrow"] = "Decorative layout"
    assert guard_confirmed_decisions(old, new)["status"] == "REVIEW_REQUIRED"


def test_guard_allows_feedback_without_mutating_confirmed_choices():
    old = sample()
    new = copy.deepcopy(old)
    new["iterations"].append(
        {"round": 2, "user_feedback": "Less decoration", "agreed_change": "Reduce icons",
         "status": "proposed"}
    )
    new["open_questions"].append("Which icons should remain?")
    assert guard_confirmed_decisions(old, new)["status"] == "UNCHANGED_CONFIRMED"


def test_old_v1_contract_still_valid():
    old = {"version": 1, "mode": "transfer", "source": {"approved": False},
           "checks": {"scenarios": []}}
    assert validate_contract(old) is old
    assert guard_confirmed_decisions(old, old)["changes"] == []


def test_replica_still_requires_reference():
    doc = sample()
    doc["mode"] = "replica"
    with pytest.raises(ContractError, match="reference scenario"):
        validate_contract(doc)


@pytest.mark.parametrize("change", [
    lambda x: x["references"][0].update(id="bad space"),
    lambda x: x["references"][0].pop("why"),
    lambda x: x["iterations"][0].update(status="trusted"),
    lambda x: x["intent"]["preserve"][0].update(id="bad id"),
])
def test_invalid_continuity_data_is_rejected(change):
    data = sample()
    change(data)
    with pytest.raises(ContractError):
        validate_contract(data)


def test_english_summary_uses_design_language():
    text = render_brief(sample(), lang="en")
    assert "Desired feeling" in text
    assert "Whitespace" in text
    assert "CSS" not in text
