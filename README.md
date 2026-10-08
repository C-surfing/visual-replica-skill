# Visual Replica

**Preserve design intent. Verify the actual interface.**

Visual Replica is a model-independent **Agent Skill + executable evidence toolkit**. It helps coding agents reproduce approved screenshots, preserve decisions while moving from prototype to production code, and detect regressions without confusing pixel similarity with usability or design quality.

It is **not** a UI generator, Figma clone, design system, aesthetic prompt library, or autonomous code editor. Use oil-ui, Impeccable, OpenDesign, Figma and your preferred coding agent for those roles. Visual Replica specializes in evidence and declared acceptance boundaries.

## Three workflows

| Mode | Input | What it verifies |
| --- | --- | --- |
| **Replica** | Approved screenshots | Rendered fidelity at known viewports/states |
| **Transfer** | HTML/Figma prototype and declared decisions | Visual references, browser state assertions, decision retention |
| **Preservation** | Existing application and design constraints | Changed states, behavior assertions and any supplied baselines |

**Important:** A screenshot is evidence of appearance, not proof of product quality. Qualitative "preserve" and "avoid" requirements always require a human review. Inferred decisions are not automatically user-confirmed.

## Quick start

For the Python toolkit (Python 3.10+):

~~~bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
~~~

For browser-backed checks (Node.js and Chromium):

~~~bash
npm install
npx playwright install chromium
~~~

Start with an editable, **unapproved** design intent contract:

~~~bash
visual-replica intent init --out intent.yaml
visual-replica intent validate --spec intent.yaml
~~~

Edit its URLs, scenarios and assertions; add approved image references where available. Then run:

~~~bash
visual-replica verify --spec intent.yaml --out-dir .visual-replica/verification
~~~

Open the local HTML report at `.visual-replica/verification/index.html`, or inspect `verification.json`. These outputs contain scenario screenshots, browser assertions, selected DOM bounds/computed style evidence, image comparison artifacts when references exist, and items still requiring human review.

### Exit/status semantics

| Status | CLI exit | Meaning |
| --- | --- | --- |
| `PASS` | 0 | All **declared automated** checks pass, with no unresolved qualitative requirements |
| `REVIEW_REQUIRED` | 1 | Visual baseline missing, threshold uncalibrated, or a qualitative design decision remains |
| `FAIL` | 2 | An explicit browser assertion or calibrated visual threshold fails |
| `ERROR` | 3 | Invalid contract or execution/environment problem |

A passing result does **not** certify an entire UI as beautifully designed or accessible.

## Design Intent Contract v1

The contract is *per task/surface*. It does not replace a project's `DESIGN.md` or product facts. A decision records its text, provenance (`user-confirmed`, `agent-inferred`, `tool-extracted`) and optionally whether it is critical. Confirmation is only valid when the source was explicitly approved. Automated checks are separate.

~~~yaml
version: 1
mode: transfer
source:
  prototype: ./prototype/index.html
  approved: true
intent:
  preserve:
    - text: Primary call-to-action must remain dominant
      provenance: user-confirmed
      critical: true
  avoid:
    - Unnecessary decorative cards
  allowed_changes:
    - Mobile layout can rearrange
checks:
  scenarios:
    - id: desktop
      url: http://localhost:3000/
      viewport: {width: 1440, height: 900, dpr: 1}
      ready_selector: main
      actions:
        - {type: click, selector: "#menu-button"}
      assertions:
        - {selector: "#menu", condition: visible}
      inspect_selectors: ["main", "#menu"]
      # reference: ./reference/desktop-menu.png
      # min_fidelity: 0.92 # Optional, calibrate for your app
~~~

Supported action types: `click`, `fill`, `press`, `check`, `uncheck`, `wait_for`. Assertion conditions: `visible`, `hidden`, `text_contains`. Each scenario has an independent viewport, state and evidence folder. Scenario references and optional region files are resolved relative to the contract.

See [Contract and evidence model](references/intent-contract.md) for acceptance semantics and known limitations.

## Existing screenshot-replication toolkit

The existing deterministic tools remain available; none of the contract commands modifies application code:

~~~bash
visual-replica doctor
visual-replica analyze reference.png --out .visual-replica/reference-analysis.json
visual-replica capture http://localhost:3000 --width 390 --height 844 --out candidate.png
visual-replica compare reference.png candidate.png --out-dir .visual-replica/compare
visual-replica diagnose .visual-replica/compare/comparison.json --repo . --out .visual-replica/diagnosis.json
visual-replica report --comparison .visual-replica/compare/comparison.json \
  --diagnosis .visual-replica/diagnosis.json --out-dir .visual-replica/report
visual-replica benchmark benchmarks/manifest.example.json
~~~

Comparison uses pixel/edge/SSIM/multi-scale metrics, hotspots and optional LPIPS. A score is not a universal percentage of "design quality"; region or whole-page acceptance thresholds should be calibrated per project. Root-cause suggestions are hypotheses, **not proven DOM-to-source mappings**.

## Integration philosophy

- **Taste / direction:** humans with oil-ui, Mobbin and other inspiration sources.
- **Prototype / design system:** Figma, OpenDesign or a simple working HTML prototype.
- **Implementation:** Codex, Claude Code or another coding agent, retaining the product's architecture.
- **Verification:** Visual Replica captures reproducible evidence; existing accessibility and testing tools handle their own domains.

No mandatory online account, style library, editor UI or custom Figma parser. See [Integrations](references/integrations.md).

## Development and validation

~~~bash
pip install -e '.[dev]'
pytest
ruff check visual_replica tests
~~~

The test suite includes contract validation, pure orchestration tests and a real Playwright state/DOM smoke test. GitHub CI installs Chromium for that browser test. The older visual comparison tests remain. Synthetic success is not represented as production-world design acceptance.

See [VALIDATION.md](VALIDATION.md) for the historical v0.12.0 release record; current CI status is authoritative for subsequent changes.

MIT licensed. Contributions are welcome; please preserve the boundary between design generation and evidence-based verification.
