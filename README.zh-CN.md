<div align="center">

# Visual Replica

**让设计意图贯穿每一轮迭代。**

一个轻量的 Agent Skill：把分散的视觉参考整理成共同认可的设计方向，并让这些选择在后续实现与修改中得以延续。

<p>
  <a href="https://github.com/C-surfing/visual-replica-skill/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/C-surfing/visual-replica-skill/actions/workflows/ci.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/C-surfing/visual-replica-skill"></a>
  <a href="pyproject.toml"><img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white"></a>
  <img alt="Agent Skill" src="https://img.shields.io/badge/Agent-Skill-334155">
</p>

[**快速开始**](#快速开始) · [**推荐工作流**](#推荐工作流) · [**设计意图契约**](#设计意图契约) · [**项目边界**](#项目边界) · [**English**](README.md)

</div>

---

## 为什么需要 Visual Replica？

用户可能喜欢网站 A 的布局、网站 B 的字体，以及网站 C 的交互，但真正想做的是**一个符合自己审美的完整产品，而不是复制某张截图**。

Coding Agent 可以迅速做出第一版界面。问题是，在多轮修改后，最初确定的视觉重点、氛围和交互取舍可能逐渐偏移。Visual Replica 帮助 Agent 持续记住：**喜欢什么、为什么喜欢、不希望照搬什么、哪些选择已经确认、哪里仍需要讨论。**

> **核心原则：** 用户决定审美方向，Coding Agent 负责实现，Visual Replica 让双方已经达成的设计约定在迭代中保持清晰。

## 核心能力

| 能力 | 作用 |
| :-- | :-- |
| **多参考融合** | 分别借鉴不同网站的布局、排版与交互，不机械复制完整页面。 |
| **设计意图契约** | 记录希望呈现的体验、重要偏好、决策原因、边界与待确认事项。 |
| **多轮设计连续性** | 保留有意义的用户反馈，发现之前确认的选择是否被悄悄改变。 |
| **自然语言反馈** | 直接说明哪里更接近目标、哪里仍不理想，而不是向用户堆砌技术指标。 |
| **可选视觉验证** | 需要精确还原或排查问题时，继续使用原有截图对比与浏览器检查工具。 |

Visual Replica **不是**另一套 UI 生成器、组件库或完整设计平台。它专注于设计决策在 Agent 工作流中的延续。

## 推荐工作流

| 阶段 | 推荐工具 | 主要目标 |
| :-- | :-- | :-- |
| **寻找参考** | [Awwwards](https://www.awwwards.com/)、[Godly](https://godly.design/)、[Mobbin](https://mobbin.com/)、[Pinterest](https://www.pinterest.com/) | 找到真正喜欢的元素，并明确喜欢的原因。 |
| **探索与确认** | [oil-ui](https://github.com/oil-oil/oil-ui)、[Figma](https://www.figma.com/)、[OpenDesign](https://github.com/nexu-io/open-design) | 比较设计方向，确认想要的体验。 |
| **保留设计意图** | **Visual Replica** | 记录各参考的借鉴部分、已确认的选择与尚未解决的问题。 |
| **工程实现** | [Codex](https://github.com/openai/codex)、Claude Code 等 | 按照既有架构与设计系统完成实现。 |
| **反馈与精修** | Coding Agent、用户反馈、[Impeccable](https://github.com/pbakaus/impeccable) | 审视真实体验，逐轮修正，避免设计方向漂移。 |

**不强制 HTML 原型优先。** 可以使用 Figma、独立 HTML 原型，也可以直接在项目现有组件里探索；选择最能减少设计不确定性的方式即可。

### 一个实际例子

| 用户提供的参考 | 需要保留的设计意图 |
| :-- | :-- |
| 网站 A | 喜欢大面积留白与页面构图，但不照搬品牌。 |
| 网站 B | 喜欢字体层级，但不照搬配色方案。 |
| 网站 C | 喜欢克制的导航，不需要其它无关功能。 |
| 用户的反馈 | “还是太像后台了，卡片太多，内容不够突出。” |
| 下一轮的重点 | 减少次要元素的视觉权重，同时保留已确认的内容优先原则。 |

Agent 应该告诉用户哪些地方仍不符合想要的感觉，而不是仅仅汇报相似度分数。

## 快速开始

小型 UI 修改可以直接让支持自定义 Skill 的 Agent 使用 [`SKILL.md`](SKILL.md)，**无需创建额外文件，也不需要先准备截图**。

对于需要多轮修改的设计项目，可以使用可选的设计契约（Python 3.10+）：

```bash
git clone https://github.com/C-surfing/visual-replica-skill.git
cd visual-replica-skill
python -m pip install -e .

visual-replica intent init --out intent.yaml
visual-replica intent brief --spec intent.yaml
```

初始化得到的是**尚未经用户确认的示例**，需要用真实参考和用户意见替换。契约不要求已有可运行界面。

保留上一版契约后，可以检查重要设计选择是否发生变化：

```bash
visual-replica intent guard \
  --before intent.previous.yaml \
  --after intent.yaml
```

工具只会提示需要确认的变化，**不会代替用户批准新的设计方向**。

## 设计意图契约

契约只记录当前任务重要的决策，不另建一套 CSS 规则或重复已有的设计系统。

```yaml
version: 1
mode: transfer
source:
  approved: false

direction:
  product: 阅读工作台
  desired_feeling: 安静、克制、内容优先

references:
  - id: composition
    source: https://example.com/reference-a
    borrow: 大面积留白与清晰的文字层级
    not_copy: 原网站的品牌与装饰
    why: 让阅读内容成为页面焦点

intent:
  preserve:
    - id: content-priority
      text: 阅读内容始终是视觉中心
      provenance: agent-inferred
      critical: true
  avoid:
    - 密集的后台式卡片排版
  allowed_changes:
    - 移动端可调整布局，但不能丢失阅读重点

open_questions:
  - 导航需要更加低调，还是更容易找到？

checks:
  scenarios: []
```

Agent 推断的偏好应保持**待确认**状态。项目原有的 `DESIGN.md` 仍然管理设计系统；Visual Replica 的契约只记录**这个用户、这个界面、这轮任务**的选择。

更多内容：[契约规范](references/intent-contract.md) · [多参考案例](examples/mixed-references.md)。

## 可选的视觉验证工具

项目原有的截图比较、差异诊断和浏览器检查能力继续保留，适合精确还原、困难问题定位及回归检查；它们不是默认流程。

```bash
npm install
npx playwright install chromium

visual-replica compare reference.png candidate.png \
  --out-dir .visual-replica/compare
```

视觉分数和自动测试结果只能作为证据，**不能证明最终设计符合用户审美**。

## 项目边界

| Visual Replica 负责 | 使用现有生态工具 |
| :-- | :-- |
| 记录针对当前任务的审美选择 | 生成与探索设计方向 |
| 在多轮迭代中保留已确认的约定 | 组件库、前端代码与工程架构 |
| 提醒设计冲突和待确认的问题 | Figma 编辑、设计系统管理 |
| 必要时提供可检查的视觉证据 | 常规视觉精修与全面 UX 评审 |

更强的 Agent 会逐步吸收许多通用设计建议，因此我们不追求成为功能最多的设计工具。这个项目的价值应该来自**让用户更容易做出选择，并减少设计偏离**。

## 文档

| 内容 | 链接 |
| :-- | :-- |
| Agent 使用指南 | [`SKILL.md`](SKILL.md) |
| 设计对话与反馈原则 | [Design dialogue](references/design-dialogue.md) |
| 设计契约规范 | [Intent contract](references/intent-contract.md) |
| 开源生态协作流程 | [Integrations](references/integrations.md) |
| 多参考组合示例 | [Mixed references](examples/mixed-references.md) |
| 历史验证记录 | [VALIDATION.md](VALIDATION.md) |

## 开发与贡献

```bash
python -m pip install -e '.[dev]'
pytest
ruff check visual_replica tests
```

欢迎在现有定位内贡献改进：[CONTRIBUTING.md](CONTRIBUTING.md)。

---

<div align="center">
  <sub>Human taste · Agent execution · Intent continuity</sub>
  <p><a href="LICENSE">MIT License</a> · <a href="README.md">English</a></p>
</div>
