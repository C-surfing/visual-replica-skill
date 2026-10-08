<div align="center">

# Visual Replica

**Design intent, carried through every iteration.**

A lightweight, agent-native skill for turning visual references into a shared design direction — and keeping that direction intact as the interface evolves.

<p>
  <a href="https://github.com/C-surfing/visual-replica-skill/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/C-surfing/visual-replica-skill/actions/workflows/ci.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/C-surfing/visual-replica-skill"></a>
  <a href="pyproject.toml"><img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white"></a>
  <img alt="Agent Skill" src="https://img.shields.io/badge/Agent-Skill-334155">
</p>

[**Getting started**](#quick-start) · [**Workflow**](#the-workflow) · [**Design contract**](#design-intent-contract) · [**Documentation**](#documentation) · [**简体中文**](README.zh-CN.md)

</div>

---

## Why Visual Replica?

A user might like the composition of one site, the typography of another, and the interaction of a third. The goal is a coherent experience shaped by those choices — **not a pixel-perfect copy of any single reference**.

A coding agent can produce a strong first pass, but the original direction may gradually drift as components are refactored and new feedback arrives. Visual Replica keeps the essential decisions visible: **what matters, why it matters, what should not be copied, and what still needs a decision**.

> **The principle:** The user owns taste. The coding agent owns implementation. Visual Replica helps preserve the agreement between them.

## At a glance

| Capability | What it provides |
| :-- | :-- |
| **Reference-aware direction** | Combine specific qualities from multiple inspirations without copying them wholesale. |
| **Design Intent Contract** | Capture the desired experience, confirmed choices, rationale, boundaries, and open questions. |
| **Iteration continuity** | Record meaningful feedback and flag changes to previously approved decisions. |
| **Human-readable feedback** | Explain what feels closer, what remains off, and what needs the user's input — without requiring CSS or DOM knowledge. |
| **Optional visual evidence** | Reuse screenshot comparison, browser scenarios, and diagnostic tooling when a task actually needs them. |

**Visual Replica is not a design generator or another frontend framework.** It complements the tools you already use instead of replacing them.

## The workflow

An effective Taste-to-Code process is modular. No tool is required at every stage.

| Stage | Recommended tools | Responsibility |
| :-- | :-- | :-- |
| **Discover** | [Awwwards](https://www.awwwards.com/), [Godly](https://godly.design/), [Mobbin](https://mobbin.com/), [Pinterest](https://www.pinterest.com/) | Gather references and identify what you actually like about each one. |
| **Explore & align** | [oil-ui](https://github.com/oil-oil/oil-ui), [Figma](https://www.figma.com/), [OpenDesign](https://github.com/nexu-io/open-design) | Compare possible directions and agree on the intended experience. |
| **Preserve intent** | **Visual Replica** | Keep a small, reviewable record of selected references, important decisions, and remaining questions. |
| **Implement** | [Codex](https://github.com/openai/codex), Claude Code, your existing stack | Build the UI using the product's components and design system. |
| **Refine** | Coding agent, user feedback, [Impeccable](https://github.com/pbakaus/impeccable) | Evaluate the actual experience, address visible gaps, and preserve confirmed choices across revisions. |

**Prototype-first is an option, not a rule.** Use HTML, Figma, or real application components based on what reduces uncertainty. There is no need to create throwaway markup when the existing design system is sufficient.

### Example: a design that survives revisions

| Input | What the agent should retain |
| :-- | :-- |
| Reference A | Its spacious layout, **not** its branding. |
| Reference B | Its clear type hierarchy, **not** its entire color scheme. |
| Reference C | Its quiet navigation, **not** unrelated interactions. |
| User feedback | “The page still feels like a dashboard; the secondary cards compete with the content.” |
| Next revision | Reduce secondary visual weight while keeping the previously agreed content priority. |

The agent should report the design gap in ordinary language, not simply claim that a visual score improved.

## Quick start

For small changes, use [`SKILL.md`](SKILL.md) with an agent that supports custom skills. **No screenshot, browser test, or contract file is required** for routine UI edits.

For multi-round design work, use the optional contract tools (Python 3.10+):

```bash
git clone https://github.com/C-surfing/visual-replica-skill.git
cd visual-replica-skill
python -m pip install -e .

visual-replica intent init --out intent.yaml
visual-replica intent brief --spec intent.yaml --lang en
```

Replace the starter examples with actual user references and decisions. **The generated contract is a draft; it does not imply approval.**

When the agreement changes, keep the previous version and check for conflicts:

```bash
visual-replica intent guard \
  --before intent.previous.yaml \
  --after intent.yaml \
  --lang en
```

The guard flags changes to previously confirmed design choices. It does **not** authenticate consent or make aesthetic decisions on behalf of the user.

## Design Intent Contract

A contract is intentionally small and **specific to the current design task**. It records experience-level decisions rather than prescribing arbitrary CSS measurements.

```yaml
version: 1
mode: transfer
source:
  approved: false

direction:
  product: Reading workspace
  desired_feeling: Calm, focused, editorial

references:
  - id: composition
    source: https://example.com/reference-a
    borrow: Spacious layout and strong hierarchy
    not_copy: Branding or decorative details
    why: Content should remain the visual focus

intent:
  preserve:
    - id: content-priority
      text: Reading content remains visually dominant
      provenance: agent-inferred
      critical: true
  avoid:
    - Dense dashboard-style card layouts
  allowed_changes:
    - Adapt the composition for small screens

open_questions:
  - Should navigation be quieter or more discoverable?

checks:
  scenarios: []
```

Design ideas inferred by an agent remain explicitly **unconfirmed** until the user accepts them. Existing `DESIGN.md` files stay authoritative for design-system tokens and components; the contract captures **this user's choices for this task**.

See [Contract reference](references/intent-contract.md) and [multi-reference example](examples/mixed-references.md).

## Optional visual verification

Visual Replica retains its original image-comparison and browser-evidence toolkit for **precision replication, difficult discrepancies, and regression checks**. It is an optional layer, not the default interaction model.

```bash
npm install
npx playwright install chromium

visual-replica compare reference.png candidate.png \
  --out-dir .visual-replica/compare
```

The tools can measure visual differences, inspect specified states, and produce evidence reports. They **cannot establish whether the user likes the result**. A technical pass never substitutes for design approval.

## Scope & philosophy

| Visual Replica owns | Existing tools own |
| :-- | :-- |
| Expressing task-specific aesthetic intent | Visual direction generation and exploration |
| Preserving confirmed decisions between rounds | Component libraries and frontend implementation |
| Surfacing conflicts and unfinished choices | Figma editing, design systems, and code architecture |
| Optional evidence when requested | General visual polishing and end-to-end UX evaluation |

As coding agents improve, generic design prompting will become easier to replace. This project stays deliberately small: its value depends on **clearer user decisions and less aesthetic drift**, not on having the most commands.

## Documentation

| Resource | Description |
| :-- | :-- |
| [`SKILL.md`](SKILL.md) | Primary instructions for coding agents |
| [Design dialogue](references/design-dialogue.md) | User-centered reference selection and feedback |
| [Intent contract](references/intent-contract.md) | Contract fields and decision-change semantics |
| [Ecosystem integration](references/integrations.md) | How to compose existing design tools |
| [Mixed-reference example](examples/mixed-references.md) | End-to-end design discussion example |
| [Validation](VALIDATION.md) | Historical validation record; check Actions for current CI |

## Development

```bash
python -m pip install -e '.[dev]'
pytest
ruff check visual_replica tests
```

Contributions should respect the project's narrow scope. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

<div align="center">
  <sub>Built for human taste, agent execution, and consistent design decisions.</sub>
  <p><a href="LICENSE">MIT License</a> · <a href="README.zh-CN.md">简体中文</a></p>
</div>
