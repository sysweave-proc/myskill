# Agent Alchemy 市场镜像（本地归档）

> [`sequenzia/agent-alchemy`](https://github.com/sequenzia/agent-alchemy) 的**只读镜像**：为改造提供未改动的原始基线，并作为长期跟踪该市场的锚点。
> 本目录是上游原文，**不是可直接安装的 CodeBuddy 插件** —— 移植产物在仓根 [`plugins/`](../../plugins/) 下的 5 个包。
> 归档范围、本地偏差与更新检查见 [顶层 README](../README.md)。

| 项 | 值 |
|---|---|
| 仓库 | https://github.com/sequenzia/agent-alchemy |
| 市场名 / owner | `agent-alchemy` ／ Stephen Sequenzia `<sequenzia@gmail.com>` |
| 安装（Claude Code） | `claude plugins install agent-alchemy/<插件名>` |
| License | MIT |
| 本镜像 commit | `fc1a336b8267e70579af8517d14718e626824e54`（2026-05-31） |

**该市场未提交到 Anthropic 的官方或社区市场**，只能通过仓库地址手动安装。

## 这是什么

一套 Claude Code 插件套件，把 Claude Code 从"对话式编码助手"扩展成**结构化开发平台**：

```
想法 → 规格 → 任务 → 自主执行
```

设计哲学是 **markdown-as-code**（"prompts as software"）—— agent 行为、工作流、领域知识全部由 Markdown + YAML frontmatter 定义，**没有编译步骤**，文件本身就是可执行代码。

## 版本对照表

截至 `fc1a336b`，取自 `.claude-plugin/marketplace.json`（**也是上游更新检查的比对基准**）。★ = 本镜像已归档：

| 插件 | 版本 | |
|---|---|---|
| `agent-alchemy-core-tools` | 0.2.3 | ★ |
| `agent-alchemy-claude-tools` | 0.2.5 | ★ |
| `agent-alchemy-sdd-tools` | 0.2.11 | ★ |
| `agent-alchemy-tdd-tools` | 0.2.1 | ★ |
| `agent-alchemy-dev-tools` | 0.3.4 | ★ |
| `agent-alchemy-opencode-tools` | 0.1.3 | |
| `agent-alchemy-cs-tools` | 0.1.0 | |
| `agent-alchemy-git-tools` | 0.1.0 | |

## 逐个插件详解

### ★ `core-tools` —— 读懂现有代码库

**6 个 skill**：`codebase-analysis`、`deep-analysis`（流程引擎）、`interview-me`、`language-patterns`、`project-conventions`、`technical-diagrams`（+ 6 份 Mermaid 图型参考）
**4 个 agent**：`code-synthesizer`、`code-architect`（opus）、`code-explorer`（sonnet）、`interview-researcher`　**1 个 hook**

三段式工作流：`deep-analysis` 6 阶段深读 → `technical-diagrams` 出架构图与报告 → 拉起 `code-architect` / `code-explorer` 出可执行洞察。
`deep-analysis` 是全市场最工程化的一份：探索缓存 + TTL、断点续传（逐阶段恢复策略表）、错误降级矩阵、分级审批（直接调用要批准，被 skill 调用自动批准）。

### ★ `sdd-tools` —— 规格驱动开发（市场里最大的一包）

**5 个 skill / 7 个 agent**。四段流水线：

```
/create-spec → specs/SPEC-{name}.md      自适应访谈生成规格（三档深度：6-10 / 12-18 / 18-25 问，命中复杂度信号自动扩容）
/create-tasks → ~/.claude/tasks/…        拆成带依赖与验收标准的任务；重跑走 task_uid 合并
/execute-tasks → 波次自主执行            拓扑排序分波；三层 agent（Orchestrator → Wave Lead → Context Manager）
/analyze-spec → 双报告                   规格体检，缺陷库 360 行
```

核心主张：**规格是落盘的工件，不是聊天记录** —— 可 diff、可 review、可复用，AI 在上下文丢失后能重新加载。

### ★ `tdd-tools` —— 测试驱动开发

**5 个 skill / 3 个 agent**：`tdd-cycle`（+ 530 行测试质量评分表 `test-rubric.md`）、`analyze-coverage`、`generate-tests`（+ 776 行跨框架模式库）、`create-tdd-tasks`、`execute-tdd-tasks`。

### ★ `dev-tools` —— 日常开发流程

**9 个 skill / 4 个 agent**：`bug-killer`（+ 分语言调试参考）、`docs-manager`、`architecture-patterns`、`code-quality`、`document-changes`、`feature-dev`、`changelog-format`、`project-learnings`、`release-python-package`。

### ★ `claude-tools` —— Claude 原语参考手册

**2 个 skill + 5 份 references**，3033 行。内容是 **Claude Tasks 与 Agent Teams 的参考文档**（含 6 种编排模式、消息协议、hook 集成）。

它是理解其余插件的基础：`sdd-tools` 的 `run-tasks` 会 `Read` 它来获取工具参数、生命周期规则、消息协议 —— 全镜像共 **27 处**引用指向它，是唯一构成**硬依赖**的跨插件引用，缺了 `sdd-tools` 的规划与执行链就是断的。

### 未归档的 3 个

| 插件 | 用途 |
|---|---|
| `opencode-tools` | 生成 OpenCode 兼容的 skill / agent / command。含 **Claude Code ↔ OpenCode 差异表**，是跨平台移植的范例 |
| `cs-tools` | 竞赛编程 / LeetCode：数据结构、DP、图算法、字符串等 7 个主题 skill |
| `git-tools` | Conventional Commits 自动化，仅 2 文件，几乎是空壳 |

## 插件怎么配合

```
core-tools（读懂现状）→ sdd-tools（规划并建造）→ tdd-tools（测试驱动保证质量）
                                              ↘ dev-tools（日常辅助：修 bug / 文档 / 发版）
claude-tools：底层参考，sdd-tools 的硬依赖
```

## 目录结构

```
agent-alchemy-marketplace/
├── README.md                 本文件（本地文档）
├── .claude-plugin/
│   └── marketplace.json      市场注册表（版本号 source of truth）
├── core-tools/    26 文件（另有本地新增的 PROVENANCE.md）
├── claude-tools/   9 文件
├── sdd-tools/     41 文件
├── tdd-tools/     21 文件
└── dev-tools/     25 文件
```

全部文件均从上游原样复制（插件来自 `claude/<插件名>/`，注册表来自 `.claude-plugin/`，镜像拍平了上游的 `claude/` 一层）。

## 其他材料

| 路径 | 说明 |
|---|---|
| [`core-tools/PROVENANCE.md`](core-tools/PROVENANCE.md) | core-tools 的逐文件 md5 与完整溯源（**本地新增，上游无此件**） |
| [`../../skills/`](../../skills/) | 本机在用的 skill（含两份外部来源的 `codebase-reading` / `deep-read`）—— 它们**不是本市场资产** |
| [`../README.md`](../README.md) | 顶层说明：归档是什么、里面有什么、怎么查上游更新 |
