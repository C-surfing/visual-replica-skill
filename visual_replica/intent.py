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

EXAMPLE = """# Design Intent Contract v1. This draft is NOT user-approved.
version: 1
mode: transfer
source:
  approved: false
direction:
  product: A focused reading workspace
  audience: People who collect references and read
  desired_feeling: Quiet, spacious, intentional
  primary_action: Start reading without distraction
  success_looks_like: The most important content is immediately obvious
references:
  - id: layout
    source: https://example.com/reference-a
    borrow: Spacious composition and text hierarchy
    not_copy: Brand identity and decorative details
    why: It makes the main content easy to find
  - id: interaction
    source: https://example.com/reference-b
    borrow: Quiet navigation
    not_copy: Its color palette
    why: Navigation should not compete with reading
intent:
  preserve:
    - id: focus
      text: Keep reading content visually dominant
      reason: Readers come here to focus, not browse dashboards
      provenance: agent-inferred
      critical: true
  avoid:
    - Decorative dashboards around reading content
  allowed_changes:
    - Adapt spacing across devices without losing focus
open_questions:
  - Which typography reference matches your intended mood?
iterations: []
checks:
  scenarios: []  # Screenshots and browser checks are optional
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
    direction = _object(doc.get("direction", {}), "direction")
    for field in ("product", "audience", "desired_feeling", "primary_action", "success_looks_like"):
        if field in direction:
            _string(direction[field], f"direction.{field}")
    references = _list(doc.get("references", []), "references")
    ref_ids = set()
    for i, ref in enumerate(references):
        loc = f"references[{i}]"
        ref = _object(ref, loc)
        key = _string(ref.get("id"), f"{loc}.id")
        if not ID.fullmatch(key) or key in ref_ids:
            raise ContractError(f"{loc}.id must be unique and stable")
        ref_ids.add(key)
        for field in ("source", "borrow", "not_copy", "why"):
            _string(ref.get(field), f"{loc}.{field}")
    _strings(doc.get("open_questions", []), "open_questions")
    for i, iteration in enumerate(_list(doc.get("iterations", []), "iterations")):
        loc = f"iterations[{i}]"
        item = _object(iteration, loc)
        if type(item.get("round")) is not int or item["round"] <= 0:
            raise ContractError(f"{loc}.round must be a positive integer")
        for field in ("user_feedback", "agreed_change"):
            _string(item.get(field), f"{loc}.{field}")
        if item.get("status") not in {"proposed", "confirmed", "rejected"}:
            raise ContractError(f"{loc}.status must be proposed, confirmed or rejected")
    intent = _object(doc.get("intent", {}), "intent")
    choice_ids = set()
    for i, entry in enumerate(_list(intent.get("preserve", []), "intent.preserve")):
        loc = f"intent.preserve[{i}]"
        item = _object(entry, loc)
        _string(item.get("text"), f"{loc}.text")
        if "id" in item:
            key = _string(item["id"], f"{loc}.id")
            if not ID.fullmatch(key) or key in choice_ids:
                raise ContractError(f"{loc}.id must be unique and stable")
            choice_ids.add(key)
        if "reason" in item:
            _string(item["reason"], f"{loc}.reason")
        if item.get("provenance") not in PROVENANCE:
            raise ContractError(f"{loc}.provenance must be explicit: {sorted(PROVENANCE)}")
        if "critical" in item and type(item["critical"]) is not bool:
            raise ContractError(f"{loc}.critical must be a boolean")
        if item["provenance"] == "user-confirmed" and source.get("approved") is not True:
            raise ContractError(f"{loc} claims user confirmation but source.approved is not true")
    for field in ("avoid", "allowed_changes"):
        _strings(intent.get(field, []), f"intent.{field}")

    checks = _object(doc.get("checks", {}), "checks")
    scenarios = _list(checks.get("scenarios", []), "checks.scenarios")
    if doc["mode"] == "replica" and not scenarios:
        raise ContractError("replica mode requires at least one reference scenario")
    seen = set()
    for i, candidate in enumerate(scenarios):
        loc = f"checks.scenarios[{i}]"
        s = _object(candidate, loc)
        name = _string(s.get("id"), f"{loc}.id")
        if not ID.fullmatch(name) or name in seen:
            raise ContractError(f"{loc}.id must be unique and use letters, digits, _ or -")
        seen.add(name)
        url = _string(s.get("url"), f"{loc}.url")
        if not (url.startswith(("http://", "https://"))):
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
