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
                      f"- 当前约定：{ {'confirmed': '已确认', 'proposed': '尚待确认', 'rejected': '未采纳'}[last['status']] }", ""]
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
        old_direction = before.get("direction", {})
        new_direction = after.get("direction", {})
        names = {
            "product": "正在设计的产品",
            "audience": "想服务的人",
            "desired_feeling": "想要的氛围",
            "primary_action": "最重要的操作",
            "success_looks_like": "成功的体验",
        }
        for key in set(old_direction) | set(new_direction):
            flag(names.get(key, key), old_direction.get(key), new_direction.get(key))

        old_refs = {ref["id"]: ref for ref in before.get("references", [])}
        new_refs = {ref["id"]: ref for ref in after.get("references", [])}
        for key in sorted(set(old_refs) | set(new_refs)):
            old_ref = old_refs.get(key)
            new_ref = new_refs.get(key)
            if old_ref is None or new_ref is None:
                flag(f"参考「{key}」", old_ref, new_ref)
                continue
            for field, label in [
                ("source", "来源"), ("borrow", "借鉴的部分"),
                ("not_copy", "不照搬的部分"), ("why", "选择原因"),
            ]:
                flag(f"参考「{key}」的{label}", old_ref[field], new_ref[field])
        flag("不希望出现的内容", before.get("intent", {}).get("avoid", []),
             after.get("intent", {}).get("avoid", []))
        if after.get("source", {}).get("approved") is not True:
            flag("整体设计是否已确认", True, after.get("source", {}).get("approved"))
    return {"status": "REVIEW_REQUIRED" if changes else "UNCHANGED_CONFIRMED",
            "changes": changes}


def _display_change(value: Any, lang: str) -> str:
    if value is None:
        return "没有" if lang == "zh" else "none"
    if isinstance(value, dict):
        if "text" in value:
            return str(value["text"])
        if "borrow" in value:
            return f"{value['source']}（借鉴：{value['borrow']}）"
        return "、".join(f"{key}：{item}" for key, item in value.items())
    if isinstance(value, list):
        return "、".join(_display_change(item, lang) for item in value) or (
            "没有" if lang == "zh" else "none"
        )
    return str(value)


def render_guard(result: dict[str, Any], lang: str = "zh") -> str:
    if not result["changes"]:
        return "已确认的设计选择没有被改动。\n" if lang == "zh" else "Confirmed design choices are unchanged.\n"
    if lang == "zh":
        lines = ["以下设计选择与你之前确认的不一样，需要你决定是否更改：", ""]
        for item in result["changes"]:
            before = _display_change(item["before"], lang)
            after = _display_change(item["after"], lang)
            lines.append(f"- {item['what']}：之前「{before}」，现在「{after}」。")
        lines.append("\n在你确认前，我会保留原来的设计方向。")
        return "\n".join(lines) + "\n"
    lines = ["These decisions differ from the agreed design and need your input:", ""]
    for item in result["changes"]:
        before = _display_change(item["before"], lang)
        after = _display_change(item["after"], lang)
        lines.append(f"- {item['what']}: previously '{before}', now '{after}'.")
    return "\n".join(lines) + "\n"
