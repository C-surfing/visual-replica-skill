import copy

import pytest
import yaml

from visual_replica.intent import ContractError, init_contract, load_contract, validate_contract


def valid():
    return {
        "version": 1, "mode": "transfer", "source": {"approved": True},
        "intent": {"preserve": [{"text": "Keep primary action prominent",
                                "provenance": "user-confirmed", "critical": True}]},
        "checks": {"scenarios": [{"id": "desktop", "url": "http://localhost:3000/",
                                  "viewport": {"width": 1440, "height": 900},
                                  "assertions": [{"selector": "main", "condition": "visible"}]}]},
    }


def test_example_is_valid_but_unapproved(tmp_path):
    file = tmp_path / "intent.yaml"
    init_contract(file)
    assert load_contract(file)["source"]["approved"] is False
    with pytest.raises(FileExistsError):
        init_contract(file)


def test_valid_contract_preserves_source_decisions():
    doc = valid()
    assert validate_contract(doc) is doc


@pytest.mark.parametrize("mutation", [
    lambda x: x.update(version=True),
    lambda x: x["checks"]["scenarios"].append(copy.deepcopy(x["checks"]["scenarios"][0])),
    lambda x: x["checks"]["scenarios"][0].update(min_fidelity=0.9),
    lambda x: x["source"].update(approved=False),
    lambda x: x["checks"]["scenarios"][0]["viewport"].update(width=0),
    lambda x: x["checks"]["scenarios"][0].update(actions=[{"type": "eval", "selector": "main"}]),
])
def test_invalid_contracts_rejected(mutation):
    doc = valid()
    mutation(doc)
    with pytest.raises(ContractError):
        validate_contract(doc)


def test_replica_requires_baseline():
    doc = valid()
    doc["mode"] = "replica"
    with pytest.raises(ContractError, match="reference"):
        validate_contract(doc)


def test_yaml_parse_error_returns_context(tmp_path):
    file = tmp_path / "bad.yaml"
    file.write_text("checks: [unclosed", encoding="utf-8")
    with pytest.raises(ContractError, match="Cannot read contract"):
        load_contract(file)


def test_manual_only_provenance_is_explicit(tmp_path):
    doc = valid()
    doc["intent"]["preserve"][0]["provenance"] = "model-says-yes"
    file = tmp_path / "intent.yaml"
    file.write_text(yaml.safe_dump(doc), encoding="utf-8")
    with pytest.raises(ContractError, match="provenance"):
        load_contract(file)
