# Visual Replica

**让 Agent 做出你真正想要的界面，并在反复修改后仍然保持这个方向。**

Visual Replica 是一个轻量的 **设计意图连续性（Design Intent Continuity）Skill**，面向 Codex、Claude Code 等 Coding Agent。它不是 UI 生成器，也不是新的 Figma，更不应该仅仅通过截图分数来评价你的审美。

## 为什么需要它？

你可能喜欢网站 A 的版式、网站 B 的字体、网站 C 的交互，但并不想复制其中任何一个网站。Coding Agent 能写出一个漂亮的初稿，却可能在之后不断修改时慢慢丢掉你最在意的感觉。

这个 Skill 帮你和 Agent 留住最重要的选择：**喜欢什么、为什么、不能照搬什么、哪些已经确认、哪些还需要讨论，以及每一轮修改后的反馈。**

## 推荐工作流

1. **找方向。** 在 [Awwwards](https://www.awwwards.com/)、[Godly](https://godly.design/)、[Mobbin](https://mobbin.com/)、[Pinterest](https://www.pinterest.com/) 等地方收集参考。必要时用 [oil-ui](https://github.com/oil-oil/oil-ui) 对比不同方向。
2. **确定想要的体验。** 用 Figma、[OpenDesign](https://github.com/nexu-io/open-design)、简单原型或直接讨论，把喜欢和不喜欢的部分说清楚。Visual Replica 协助整理成简短设计约定。
3. **交给 Agent 实现。** 让 Codex 或其他 Coding Agent 负责写代码；可以用 [Impeccable](https://github.com/pbakaus/impeccable) 提供设计点评与精修。
4. **一轮轮接近目标。** 根据实际界面和你的反馈调整，而不是只盯着代码或截图分数。重要的已确认决定不会被 Agent 悄悄改掉。
5. **按需验证。** Agent 本身可以截图观察；只有真的需要时才调用 Visual Replica 原有的截图比较和浏览器检查工具。

## 给用户的反馈应该是什么样？

> **想要的感觉：** 安静、留白充足、内容优先。  
> **这次更接近的地方：** 主内容开始成为视觉中心。  
> **还没做好：** 顶部导航仍然太抢眼，影响了阅读节奏。  
> **需要你决定：** 导航再弱一些，还是保留目前的易发现性？

这才是面向用户的设计交流；CSS 属性、DOM 数据和数值评分留给 Agent 自己分析。

## 如何使用

把 [SKILL.md](SKILL.md) 交给支持 Skill 的 Coding Agent 即可。小的 UI 修改无需引入文件或额外流程。对于多轮设计项目，可使用可选的设计契约：

```bash
pip install -e .
visual-replica intent init --out intent.yaml
visual-replica intent brief --spec intent.yaml
```

开始时会得到**尚未经你确认的示例**，Agent 需要将参考和你的意见替换进去。无需先写代码、准备截图或启动网站。

修改已确认的设计决定前，保留旧版本并检查：

```bash
visual-replica intent guard --before intent.previous.yaml --after intent.yaml
```

检查会提示哪些已确认选择发生了变化，但不会自行把新决定视为用户批准。

## 项目边界

**Visual Replica 负责：** 设计意图的记录、跨轮次保持、反馈整理、决策变化提醒；可选的视觉证据。

**Visual Replica 不负责：** 美学风格生成、完整设计工具、组件库、通用前端代码生成、代替用户批准设计。

我们不应该与 oil-ui、Impeccable、OpenDesign、Figma 正面重复建设。更强的 Agent 也可能替代大量通用 Skill 指令，因此项目的价值必须通过“用户满意度是否提升、审美漂移是否减少”证明，而不是通过功能数量证明。

英文主文档：[README.md](README.md) · [设计对话指南](references/design-dialogue.md) · [多参考示例](examples/mixed-references.md)

MIT 开源。
