"""Human-oriented design brief and changes to previously approved taste decisions.

No model calls or UI judgments are made here. Text is grounded only in the contract.
"""
from __future__ import annotations

from typing import Any

from .intent import validate_contract


def _lines(items: list[str], empty: str) -> str:
    return "\n".join(f"- {value}" for value in items) if items else f"- {empty}"


def render_brief(contract: dict[str, Any], lang: str = "zh") -> str:
    """Summarize the design intent without technical implementation language."""
    validate_contract(contract)
    direction = contract.get("direction", {})
    references = contract.get("references", [])
    intent = contract.get("intent", {})
    questions = contract.get("open_questions", [])
    iterations = contract.get("iterations", [])
    if lang == "zh":
        lines = ["# 我们想做成什么样", ""]
        for key, label in [
            ("product", "正在设计"),
            ("audience", "为谁设计"),
            ("desired_feeling", "希望呈现的感觉"),
            ("primary_action", "用户最重要的操作"),
            ("success_looks_like", "什么样才算达到了目标"),
        ]:
            if direction.get(key):
                lines.append(f"**{label}：** {direction[key]}")
        lines += ["", "## 参考里真正想借鉴的", ""]
        lines += [f"- **{ref['id']}：** 想保留「{ref['borrow']}」；不照搬「{ref['not_copy']}」。因为：{ref['why']}" for ref in references]
        if not references:
            lines.append("- 还没有明确的参考，需要和你一起确认。")
        lines += ["", "## 不能在修改中丢失的", ""]
        for item in intent.get("preserve", []):
            name = item["text"]
            pending = "（待你确认）" if item["provenance"] != "user-confirmed" else ""
            reason = f"——{item['reason']}" if item.get("reason") else ""
            lines.append(f"- {name}{pending}{reason}")
        if not intent.get("preserve"):
            lines.append("- 尚未确认关键设计选择。")
        lines += ["", "## 不希望出现的", "", _lines(intent.get("avoid", []), "暂未提出"), ""]
        if iterations:
            last = iterations[-1]
            lines += ["## 最近一轮反馈", "",
                      f"- 你的反馈：{last['user_feedback']}",
                      f"- 调整方向：{last['agreed_change']}",
                      f"- 当前约定：{'已确认' if last['status'] == 'confirmed' else '尚待确认'}", ""]
        lines += ["## 还需要你决定的", "", _lines(questions, "没有明确待确认事项"), ""]
        return "\n".join(lines).strip() + "\n"

    lines = ["# The design we are aiming for", ""]
    for key, label in [
        ("product", "Product"), ("audience", "For"),
        ("desired_feeling", "Desired feeling"), ("primary_action", "Primary action"),
        ("success_looks_like", "Success means"),
    ]:
        if direction.get(key):
            lines.append(f"**{label}:** {direction[key]}")
    lines += ["", "## What we borrow from references", ""]
    for ref in references:
        lines.append(f"- **{ref['id']}:** Borrow {ref['borrow']}; do not copy {ref['not_copy']}. Why: {ref['why']}")
    lines += ["", "## Keep through iterations", ""]
    for item in intent.get("preserve", []):
        pending = " (needs your confirmation)" if item["provenance"] != "user-confirmed" else ""
        lines.append(f"- {item['text']}{pending}")
    lines += ["", "## Avoid", "", _lines(intent.get("avoid", []), "Not specified"), ""]
    if iterations:
        last = iterations[-1]
        lines += ["## Latest feedback", "", f"- Feedback: {last['user_feedback']}",
                  f"- Change: {last['agreed_change']}", f"- State: {last['status']}", ""]
    lines += ["## Open decisions", "", _lines(questions, "None recorded"), ""]
    return "\n".join(lines).strip() + "\n"


def guard_confirmed_decisions(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    """Detect changed confirmed choices. No authorization or implicit approval."""
    validate_contract(before)
    validate_contract(after)
    changes = []

    def flag(what: str, previous: Any, proposed: Any) -> None:
        if previous != proposed:
            changes.append({"what": what, "before": previous, "after": proposed})

    prior = before.get("intent", {}).get("preserve", [])
    current = after.get("intent", {}).get("preserve", [])
    by_id = {item["id"]: item for item in current if "id" in item}
    for item in prior:
        if item["provenance"] != "user-confirmed":
            continue
        existing = by_id.get(item["id"]) if "id" in item else next(
            (candidate for candidate in current if candidate.get("text") == item["text"]), None
        )
        if existing is None:
            flag(f"confirmed: {item.get('id', item['text'])}", item, None)
        else:
            for field in ("text", "reason", "critical", "provenance"):
                flag(f"{item.get('id', item['text'])}.{field}", item.get(field), existing.get(field))

    if before.get("source", {}).get("approved") is True:
        for field in ("direction", "references"):
            flag(field, before.get(field), after.get(field))
        flag("avoid", before.get("intent", {}).get("avoid", []), after.get("intent", {}).get("avoid", []))
        if after.get("source", {}).get("approved") is not True:
            flag("source approval", True, after.get("source", {}).get("approved"))
    return {"status": "REVIEW_REQUIRED" if changes else "UNCHANGED_CONFIRMED",
            "changes": changes}


def render_guard(result: dict[str, Any], lang: str = "zh") -> str:
    if not result["changes"]:
        return "已确认的设计选择没有被改动。\n" if lang == "zh" else "Confirmed design choices are unchanged.\n"
    if lang == "zh":
        lines = ["这些已确认的设计选择发生了变化，需要你重新决定：", ""]
        for item in result["changes"]:
            lines.append(f"- {item['what']}：原来是「{item['before']}」，现在变成「{item['after']}」。")
        lines.append("\n在确认前，不应悄悄用新版本替换原来的约定。")
        return "\n".join(lines) + "\n"
    lines = ["Previously approved choices changed; your review is needed:", ""]
    for item in result["changes"]:
        lines.append(f"- {item['what']}: before={item['before']!r}; proposed={item['after']!r}")
    return "\n".join(lines) + "\n"
