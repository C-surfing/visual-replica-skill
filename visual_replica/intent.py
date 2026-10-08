"""Design intent contract v1: explicit decisions, provenance and executable checks.

This module parses and validates contracts. It does not infer taste from images.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

MODES = {"replica", "transfer", "preservation"}
PROVENANCE = {"user-confirmed", "agent-inferred", "tool-extracted"}
ACTION_TYPES = {"click", "fill", "press", "check", "uncheck", "wait_for"}
ASSERTIONS = {"visible", "hidden", "text_contains"}
ID = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")

EXAMPLE = """# Design Intent Contract v1
# Generated as an editable example. Nothing here implies user approval.
version: 1
mode: transfer
source:
  prototype: ./prototype/index.html
  approved: false
intent:
  preserve:
    - text: Primary call-to-action remains visually dominant
      provenance: agent-inferred
      critical: true
  avoid:
    - Unnecessary decorative cards
  allowed_changes:
    - Responsive rearrangement
checks:
  scenarios:
    - id: desktop
      url: http://localhost:3000/
      viewport: {width: 1440, height: 900, dpr: 1}
      ready_selector: main
      inspect_selectors: ["main", "header"]
      assertions:
        - {selector: "main", condition: visible}
    - id: mobile
      url: http://localhost:3000/
      viewport: {width: 390, height: 844, dpr: 1}
      assertions:
        - {selector: "main", condition: visible}
# To enable image comparison, set each scenario's reference to an approved PNG.
# Add min_fidelity only if a project-specific threshold has been calibrated.
"""


class ContractError(ValueError):
    """An invalid or misleading design intent contract."""


def _object(value: Any, location: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContractError(f"{location} must be a mapping")
    return value


def _list(value: Any, location: str) -> list[Any]:
    if not isinstance(value, list):
        raise ContractError(f"{location} must be a list")
    return value


def _string(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{location} must be a nonempty string")
    return value


def _strings(value: Any, location: str) -> list[str]:
    return [_string(v, f"{location}[{i}]") for i, v in enumerate(_list(value, location))]


def validate_contract(data: Any) -> dict[str, Any]:
    """Validate in place and return the contract. No guessed defaults for evidence."""
    doc = _object(data, "contract")
    if type(doc.get("version")) is not int or doc["version"] != 1:
        raise ContractError("version must be the integer 1")
    if doc.get("mode") not in MODES:
        raise ContractError(f"mode must be one of {', '.join(sorted(MODES))}")
    source = _object(doc.get("source", {}), "source")
    if "approved" in source and type(source["approved"]) is not bool:
        raise ContractError("source.approved must be a boolean")
    for field in ("prototype", "design_system", "figma_url"):
        if field in source:
            _string(source[field], f"source.{field}")
    intent = _object(doc.get("intent", {}), "intent")
    for i, entry in enumerate(_list(intent.get("preserve", []), "intent.preserve")):
        loc = f"intent.preserve[{i}]"
        item = _object(entry, loc)
        _string(item.get("text"), f"{loc}.text")
        if item.get("provenance") not in PROVENANCE:
            raise ContractError(f"{loc}.provenance must be explicit: {sorted(PROVENANCE)}")
        if "critical" in item and type(item["critical"]) is not bool:
            raise ContractError(f"{loc}.critical must be a boolean")
        if item["provenance"] == "user-confirmed" and source.get("approved") is not True:
            raise ContractError(f"{loc} claims user confirmation but source.approved is not true")
    for field in ("avoid", "allowed_changes"):
        _strings(intent.get(field, []), f"intent.{field}")

    checks = _object(doc.get("checks"), "checks")
    scenarios = _list(checks.get("scenarios"), "checks.scenarios")
    if not scenarios:
        raise ContractError("checks.scenarios must include at least one scenario")
    seen = set()
    for i, candidate in enumerate(scenarios):
        loc = f"checks.scenarios[{i}]"
        s = _object(candidate, loc)
        name = _string(s.get("id"), f"{loc}.id")
        if not ID.fullmatch(name) or name in seen:
            raise ContractError(f"{loc}.id must be unique and use letters, digits, _ or -")
        seen.add(name)
        url = _string(s.get("url"), f"{loc}.url")
        if not (url.startswith("http://") or url.startswith("https://")):
            raise ContractError(f"{loc}.url must be http(s)")
        viewport = _object(s.get("viewport"), f"{loc}.viewport")
        for field in ("width", "height"):
            value = viewport.get(field)
            if type(value) is not int or not 1 <= value <= 10000:
                raise ContractError(f"{loc}.viewport.{field} must be an integer in 1..10000")
        dpr = viewport.get("dpr", 1)
        if type(dpr) not in (int, float) or not 0.5 <= dpr <= 4:
            raise ContractError(f"{loc}.viewport.dpr must be a number in 0.5..4")
        for field in ("reference", "regions", "ready_selector"):
            if field in s:
                _string(s[field], f"{loc}.{field}")
        if doc["mode"] == "replica" and not s.get("reference"):
            raise ContractError(f"{loc}.reference is required for replica mode")
        if "min_fidelity" in s:
            threshold = s["min_fidelity"]
            if type(threshold) not in (int, float) or not 0 <= threshold <= 1:
                raise ContractError(f"{loc}.min_fidelity must be between 0 and 1")
            if "reference" not in s:
                raise ContractError(f"{loc}.min_fidelity requires reference")
        _strings(s.get("inspect_selectors", []), f"{loc}.inspect_selectors")
        for j, act in enumerate(_list(s.get("actions", []), f"{loc}.actions")):
            aloc = f"{loc}.actions[{j}]"
            a = _object(act, aloc)
            if a.get("type") not in ACTION_TYPES:
                raise ContractError(f"{aloc}.type must be one of {sorted(ACTION_TYPES)}")
            _string(a.get("selector"), f"{aloc}.selector")
            if a["type"] in {"fill", "press"}:
                _string(a.get("value"), f"{aloc}.value")
        for j, check in enumerate(_list(s.get("assertions", []), f"{loc}.assertions")):
            cloc = f"{loc}.assertions[{j}]"
            a = _object(check, cloc)
            _string(a.get("selector"), f"{cloc}.selector")
            if a.get("condition") not in ASSERTIONS:
                raise ContractError(f"{cloc}.condition must be one of {sorted(ASSERTIONS)}")
            if a["condition"] == "text_contains":
                _string(a.get("value"), f"{cloc}.value")
    return doc


def load_contract(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ContractError(f"Cannot read contract {path}: {exc}") from exc
    return validate_contract(data)


def init_contract(path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as target:
        target.write(EXAMPLE)
    return path
