<div align="center">

# 🧬 Visual Replica Skill Pro

**Make AI behave like a senior visual frontend engineer.**

[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-visual--replica--pro-8B5CF6?style=for-the-badge&logo=robot)]
[![Version](https://img.shields.io/badge/version-v3-6f42c1?style=for-the-badge)]
[![License](https://img.shields.io/github/license/C-surfing/pixel-perfect-ui?style=for-the-badge)]
[![Clients](https://img.shields.io/badge/Cursor%20·%20Claude%20Code%20·%20Codex-0ea5e9?style=for-the-badge)]

*An expert-level UI replication skill — screenshot-first reconstruction with visual QA, regression thinking, diff diagnosis, and continuous improvement.*

</div>

---

## 🎯 Goal

Make AI behave like a **senior visual frontend engineer** — not someone who makes a *beautiful new design*, but someone who **reproduces the existing visual target faithfully while keeping production-quality code**.

## 🧭 Design Principles

> **Reference image = visual specification.**
>
> **Rendered application = only reliable evidence.**
>
> **Never claim success from code inspection alone.**

## 🔁 The Workflow

```mermaid
flowchart TD
    A["Task Planning<br/>(A: existing project · B: screenshot-only<br/>C: multi-reference · D: responsive)"] --> B["Visual Analysis<br/>(structure · geometry · typography · assets)"]
    B --> C["Implementation<br/>(viewport → macro → components → details)"]
    C --> D["Verification Loop<br/>render → capture → compare → diagnose"]
    D --> E{"Differences?"}
    E -->|yes| F["Classified Diagnosis<br/>(global offset · vertical drift<br/>typography · component)"]
    F --> G["Minimal Fix"]
    G --> D
    E -->|no| H["Quality Gates<br/>(visual + engineering + validation)"]
    H --> I["Continuous Improvement<br/>(failure log · reusable patterns)"]
    style H fill:#d1fae5,stroke:#059669
```

## ✨ What makes it *Pro*

| Capability | How |
| :--- | :--- |
| **Task-aware planning** | Classifies 4 task types (existing project / screenshot-only / multi-reference / responsive) before touching code |
| **Classified diagnosis** | Global offset → vertical drift → typography mismatch → component mismatch, each with its own check-list |
| **Implementation ordering** | Viewport first, micro-details last — never tune shadows while layout is wrong |
| **Iteration learning** | Every iteration records Problem → Hypothesis → Change → Result; only keep improvements, rollback regressions |
| **Quality gates** | Visual + engineering + validation — no screenshot hacks, no excessive absolute positioning |
| **Continuous improvement** | Failure patterns and successful fixes feed future tasks |

## 📦 Structure

```text
visual-replica-skill-pro/
├── SKILL.md                        # The skill itself
├── references/
│   ├── task-planning.md            #   task type classification
│   ├── diff-to-fix.md              #   diagnosis → fix mapping
│   ├── quality-gates.md            #   acceptance criteria
│   ├── platform-guidelines.md      #   platform-specific rules
│   └── anti-patterns.md            #   what NOT to do
├── templates/
│   ├── visual-spec.json            #   visual specification output
│   └── iteration-log.json          #   iteration learning record
├── learning/
│   └── failure-log.template.md     #   failure pattern ledger
├── scripts/README.md               #   tooling notes
└── README.md
```

## 🚀 Install

Copy the folder into any supported skill location:

```text
.cursor/skills/visual-replica-skill-pro/
.claude/skills/visual-replica-skill-pro/
.codex/skills/visual-replica-skill-pro/
.agents/skills/visual-replica-skill-pro/
```

## 📜 License

[MIT](LICENSE) © 2026 [C-surfing](https://github.com/C-surfing)

---

<p align="center">Reproduce the reference, not an interpretation of it. 🎯</p>
