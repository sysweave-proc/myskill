# Agent Alchemy 市场镜像（本地归档）

> 本目录是 **Stephen Sequenzia** 的 `agent-alchemy` Claude Code 插件市场的本地只读镜像。
> 目的：为后续「改造成 WorkBuddy 可用」提供未改动的原始基线，并作为长期跟踪该市场的锚点。

---

## 一、这是什么

`agent-alchemy` 是一个**开源 Claude Code 插件套件**，把 Claude Code 从"对话式编码助手"扩展成一个**结构化开发平台**：

```
想法 → 规格 → 任务 → 自主执行
```

作者的设计哲学是 **markdown-as-code**（"prompts as software"）—— 所有 agent 行为、工作流、领域知识**全部由 Markdown + YAML frontmatter 定义，没有编译步骤**。Markdown 文件本身就是可执行代码，由 Claude Code 运行时直接解释。

**两个互相咬合的系统：**

```
插件框架 (claude/)                   任务看板 (apps/task-manager/)
  28 skills / 16 agents               Next.js 16 + TanStack Query
  6 个插件组                           SSE 实时 Kanban
  markdown-as-code                    监听 ~/.claude/tasks/
         │                                      ▲
         │  生成 task JSON 文件                  │  监听文件系统
         └──────────────────────────────────────┘
```

---

## 二、作者是谁

| 项 | 内容 |
|---|---|
| **姓名** | Stephen Sequenzia |
| **GitHub** | [@sequenzia](https://github.com/sequenzia)（uid 1118205） |
| **职位** | Staff AI/ML Engineer, Architect & Technical Lead |
| **雇主** | Lockheed Martin（洛克希德·马丁） |
| **地点** | Orlando, FL（美国佛罗里达州奥兰多） |
| **个人站** | https://sequenzia.com |
| **Twitter/X** | [@sequenzia](https://twitter.com/sequenzia) |
| **自述** | "AI/ML Engineer, Architect & Technical Lead with a strong foundation in Software Engineering, Data Engineering, MLOps and Agentic AI" |

**背景解读**：他不是纯前端或纯工具链开发者，而是**数据工程 + MLOps + 智能体（Agentic AI）**方向的一线工程负责人。这个背景解释了 `agent-alchemy` 的几个特征：

- 为什么偏好 **"prompts as software"** 而非写代码 —— 数据/ML 工程师习惯把配置和管线当代码管理
- 为什么流程设计如此**强调可验证性**（验收标准、质量闸门、验证模式）—— MLOps 的核心就是"实验可复现"
- 为什么做了 **Task Manager 看板** —— 生产化思维，而不只是 prompt 收藏

**其他公开项目**（从 pinned repos 看，他关注的是 agent 基础设施而非业务）：

| 项目 | 说明 | Star |
|---|---|---|
| **agent-alchemy** | 本目录对应项目，插件套件 + 看板 | **44** ⭐ / 7 fork |
| **agent-tools** | 纯 markdown/JSON 的 skill 与 agent 库，26 skills / 12 agents / 零编译代码 | 2 |
| **mamba-agents** | 基于 `pydantic-ai` 的 AI Agent 框架（薄封装 + 生产级基础设施） | 2 |
| **mamba-mcp** | MCP 服务器测试调试工具箱（TUI + CLI + Python API） | 2 |
| **datax** | 自然语言转 SQL 的数据问答 agent | 1 |
| **discord-claudebot** | Discord ↔ Claude Code 双向 MCP 通道服务 | 1 |

**活跃度判断**：`agent-alchemy` 是唯一过两位数的项目（44 ⭐），其余都是个位数。**这是典型的"个人高质量工具集"而非"社区项目"** —— 有真实工程深度，但缺少规模化采用。最近提交 `2026-05-31`（3.7 个月前），更新节奏属于稳定维护期而非活跃开发期。

---

## 三、市场地址与跟踪方式

| 项 | 地址 |
|---|---|
| **GitHub 仓库** | https://github.com/sequenzia/agent-alchemy |
| **marketplace.json** | https://raw.githubusercontent.com/sequenzia/agent-alchemy/main/.claude-plugin/marketplace.json |
| **市场名（name）** | `agent-alchemy` |
| **owner** | Stephen Sequenzia `<sequenzia@gmail.com>` |
| **安装方式** | `claude plugins install agent-alchemy/<插件名>` |
| **License** | MIT |
| **本镜像 commit** | `fc1a336b8267e70579af8517d14718e626824e54` |
| **该 commit 日期** | `2026-05-31` |
| **下载日期** | `2026-09-19` |

**该 HEAD 提交的说明**：`docs(skills): harden technical-diagrams and docs-manager against dark-mode mermaid breakage` —— 加固 `technical-diagrams` 和 `docs-manager` 在深色模式下的 Mermaid 渲染，顺带补了依赖安装步骤。

**重要事实**：该市场**未提交到 Anthropic 的官方或社区市场**（在 `claude-plugins-official` 310 条与 `claude-plugins-community` 2282 条中检索 `agent-alchemy` / `sequenzia` 均无命中）。只能通过仓库地址手动安装。

### 长期跟踪方法

```bash
# 1. 查市场清单是否变化（最简单）
curl -sSL "https://raw.githubusercontent.com/sequenzia/agent-alchemy/main/.claude-plugin/marketplace.json" \
  | python -c "import sys,json; d=json.load(sys.stdin); [print(p['name'], p.get('version'), '|', p.get('description','')[:60]) for p in d['plugins']]"

# 2. 查最新 commit
#    https://github.com/sequenzia/agent-alchemy/commits/main

# 3. 全量重下并比对（换掉 $VER 当日日期）
cd "$HOME" && curl -sSL -o aa.zip "https://codeload.github.com/sequenzia/agent-alchemy/zip/refs/heads/main"
python -c "import zipfile; zipfile.ZipFile('aa.zip').extractall('aa_new')"
diff -rq aa_new/agent-alchemy-main/claude/core-tools "X:/myskill/external-skills/agent-alchemy-marketplace/core-tools"

# 4. 校验本地镜像是否被改动（各处指纹见第七节，务必带 LC_ALL=C）
cd /home/zhq/mydisk/myskill/external-skills/agent-alchemy-marketplace/sdd-tools \
  && find . -type f ! -name PROVENANCE.md | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32

```

**归档范围**：**5 个插件 + 市场注册表**（共 125 文件，其中上游原样文件 123）。未归档的有 `opencode-tools`、`cs-tools`、`git-tools` 三个插件（用途见第四节）。

> 2026-09-19 补齐：`claude-tools`（`sdd-tools` 的 27 处跨插件引用原为断链）。

**版本对照表**（截至 `fc1a336b`，来自 marketplace.json）：

| 插件 | 市场内版本 |
|---|---|
| `agent-alchemy-claude-tools` | 0.2.5 |
| `agent-alchemy-core-tools` | 0.2.3 |
| `agent-alchemy-dev-tools` | 0.3.4 |
| `agent-alchemy-git-tools` | 0.1.0 |
| `agent-alchemy-sdd-tools` | 0.2.11 |
| `agent-alchemy-tdd-tools` | 0.2.1 |
| `agent-alchemy-opencode-tools` | 0.1.3 |
| `agent-alchemy-cs-tools` | 0.1.0 |

---

## 四、插件全览

本目录归档 **5 个**（★ 标记）；其余未归档的插件也一并列出用途备查。

| 插件 | 版本 | 文件 | md 行数 | 用途 | 场景 |
|---|---|---|---|---|---|
| ★ `core-tools` | 0.2.3 | 26 (+PROVENANCE) | 5,774 | 代码库分析、多智能体深度探索、语言模式 | **读懂**一个陌生/已有代码库 |
| ★ `sdd-tools` | 0.2.11 | 41 | 12,716 | 规格驱动开发全流水线 | **规划并建造**新功能 |
| ★ `tdd-tools` | 0.2.1 | 21 | 8,961 | 测试驱动开发（RED-GREEN-REFACTOR） | **用测试驱动实现**，保证质量 |
| ★ `dev-tools` | 0.3.4 | 25 | 5,699 | 功能开发、代码评审、架构模式、文档、changelog | **日常开发流程**辅助 |
| ★ `claude-tools` | 0.2.5 | 9 | 3,033 | Claude Tasks 与 Agent Teams 的参考手册 | 理解 Claude 原生任务/团队机制；**已归档**（sdd-tools 硬依赖） |
| `opencode-tools` | 0.1.3 | 18 | 3,660 | 生成 OpenCode 兼容的 skill/agent/command | 给 OpenCode 平台写扩展 |
| `cs-tools` | 0.1.0 | 11 | 3,471 | 竞赛编程 / LeetCode 题解 | 算法练习与教学 |
| `git-tools` | 0.1.0 | 2 | 159 | Conventional Commits 自动化 | 规范化 git 提交 |

---

## 五、逐个插件详解

### ★ 1. `core-tools` —— 代码库理解（已归档）

**定位**：读懂现有代码库。这是最初要"全流程复原"的那个插件。

**组成**
- **6 个 skill**：`codebase-analysis`(276)、`deep-analysis`(521，流程引擎)、`interview-me`(444)、`language-patterns`(444)、`project-conventions`(273)、`technical-diagrams`(405 + 6 个 Mermaid 图型参考)
- **4 个 agent**：`code-synthesizer`(265, opus)、`code-architect`(180, opus)、`code-explorer`(156, sonnet)、`interview-researcher`(127, opus)
- **1 个 hook**：`auto-approve-da-session.sh`

**三段式工作流**
```
Phase 1  读 deep-analysis → 6 阶段深读（侦察→规划→评审→组队→并行探索→综合）
Phase 2  读 technical-diagrams + report-template → 出架构图与报告
Phase 3  拉起 code-architect / code-explorer agent → actionable insights
```

**亮点**：`deep-analysis` 是全场最工程化的一份 —— 带**探索缓存 + TTL**、**断点续传**（逐阶段恢复策略表）、**错误降级矩阵**（1 个 worker 挂/2 个挂/全挂分别怎么办）、**分级审批**（直接调用要审批，被其他 skill 调用不审批）。

**适用场景**
- 接手一个陌生代码库，需要快速建立架构认知
- 做技术尽调 / 代码评审前的摸底
- 需要输出架构图、关系图、风险清单的场合

**改造难点**：Phase 3 依赖 `TeamCreate`/`SendMessage`/model tier（opus/sonnet），WorkBuddy 无此原语，协调层需重写。另外 `interview-me` 依赖 Context7 MCP。

---

### ★ 2. `sdd-tools` —— 规格驱动开发（已归档，市场最大）

**定位**：把模糊想法变成"规格 → 任务 → 自主执行"。**建新东西，不是读旧东西。**

**核心概念 —— 什么是规格驱动开发（SDD）**

传统 vibe coding：丢一句"帮我加个登录功能" → AI 直接改文件 → 理解错了 → 返工。问题在于**需求只存在于对话里，模糊、易变、不可验证**。

SDD 把中间产物显式化：
```
模糊想法 → 规格文档(SPEC) → 任务列表 → 自主执行 → 验证
            ↑ 可评审可追溯    ↑ 带依赖可排序  ↑ 可并行可恢复
```
关键差别：**规格是落盘的工件，不是聊天记录**。它可 diff、可 review、可复用，也能让 AI 在上下文丢失后重新加载。AI 先把"登录功能"逼问成"支持邮箱 + Google OAuth、记住我 30 天、失败 5 次锁定 10 分钟、写审计日志"——这些是**可验收的**，然后才动手。

**四段流水线**
```
/create-spec    →  specs/SPEC-{name}.md           自适应访谈生成规格
      ↓
/analyze-spec   →  {name}.analysis.md + .html     规格质量体检
      ↓
/create-tasks   →  ~/.claude/tasks/{list}/*.json  拆成带依赖的任务
      ↓
/execute-tasks  →  波次式自主执行
```

**四段各自的门道**
- **`/create-spec`(742)**：不是问卷，是**自适应访谈** —— 三档深度（high-level 6-10 问 / detailed 12-18 问 / full-tech 18-25 问）、**复杂度信号检测**（命中就自动扩容到 28-40 问，要你点头）、**主动推荐**（该不该插一句"你可能需要 X"有专门触发器）、**可选代码库勘察**（拉 `codebase-explorer` 先摸清既有模式，让问题问到点上）、**外部研究**（`researcher` 查最佳实践）
- **`/analyze-spec`(446)**：找不一致/歧义/缺失需求（`common-issues.md` 360 行缺陷库），出 md + HTML 双报告（带 789 行评审界面模板）
- **`/create-tasks`(946)**：依赖有序分解 + 验收标准；**合并模式**用 `task_uid` 增量更新（已完成不动、待办按新规格更新、进行中跳过、新需求新建）
- **`/execute-tasks` + `/run-tasks`(255+1098)**：**拓扑排序分波**（无依赖先跑，循环依赖在最薄弱环断开）+ **三层 agent 架构**（Orchestrator 规划 → Wave Lead(opus) 带队 → Context Manager 跨波传知识，每波任务 ≥3 才拉）+ 并行度封顶 + **中断会话恢复**（从下一未阻塞波继续，扫描孤儿团队目录）

**8 个 agent**：`codebase-explorer`(120, sonnet)、`context-manager`(290)、`researcher`(218)、`spec-analyzer`(332)、`task-executor`(324) + `task-executor-v2`(317)、`wave-lead`(462)

**适用场景**
- 需求模糊、需要先逼清楚再动手的复杂功能
- 多任务并行、需要依赖排序和进度可见（配 Task Manager 看板）
- 团队协作，规格需要评审与留痕

**改造难点**：**难度最高的一个**。`run-tasks` 显式依赖 `claude-tools` 插件（那 3033 行的 Claude Tasks/Agent Teams 手册），执行层深度绑定 Claude 团队系统。改造需整体重设计执行层。

---

### ★ 3. `tdd-tools` —— 测试驱动开发（已归档）

**定位**：用 RED-GREEN-REFACTOR 循环驱动实现，保证质量。

**组成**
- **5 个 skill**：`tdd-cycle`(727 + `test-rubric.md` 530 评分表)、`analyze-coverage`(628 + `coverage-patterns.md` 695)、`generate-tests`(524 + `test-patterns.md` 776 模式库 + `framework-templates.md` 686)、`create-tdd-tasks`(656)、`execute-tdd-tasks`(669)
- **3 个 agent**：`tdd-executor`(493)、`test-writer`(296)、`test-reviewer`(285)

**门道**：`test-rubric.md`(530 行) 是给测试质量打分的标准；`test-patterns.md`(776 行) 是跨框架的测试模式库；`framework-templates.md`(686 行) 提供各框架模板。从 task 分解（`tdd-decomposition-patterns`）到执行验证（`tdd-verification-patterns`）全链路覆盖。

**适用场景**
- 需要严格测试覆盖的关键模块
- 自动化测试生成与覆盖率分析
- 想给 core-tools 的分析能力加**验证闭环**

---

### ★ 4. `dev-tools` —— 日常开发流程（已归档）

**定位**：功能开发、评审、架构、文档、changelog 的日常辅助。

**组成**
- **11 个 skill**：`bug-killer`(470 + 分语言调试参考：`python-debugging` 265 / `typescript-debugging` 325 / `general-debugging` 221)、`docs-manager`(410 + 3 份模板)、`architecture-patterns`(349)、`code-quality`(346)、`document-changes`(277)、`feature-dev`(275)、`changelog-format`(169)、`project-learnings`(117)、`release-python-package`(287)
- **4 个 agent**：`changelog-manager`(329)、`docs-writer`(247)、`code-reviewer`(178)、`bug-investigator`(168)

**重要**：`core-tools` 引用了 `feature-dev` 和 `docs-manager` 作为**下游依赖**（我之前在 core-tools 的 PROVENANCE 里标为 "downstream-only refs"）—— **它们就在这里**。

**适用场景**
- 修 bug（有分语言调试手册）
- 写文档 / 维护 changelog
- 代码质量自查、发版

---

### 5. `claude-tools` —— Claude 原语参考手册（**已归档**，2026-09-19 补齐）

3033 行，9 个文件。内容是 **Claude Tasks 与 Agent Teams 功能的参考文档**（含 `references/orchestration-patterns.md`）。

**这是理解其余插件的基础**：`sdd-tools` 的 `run-tasks` 会 `Read ${CLAUDE_PLUGIN_ROOT}/../claude-tools/skills/claude-code-tasks/SKILL.md` 来获取工具参数、生命周期规则、消息协议。

**为何必须归档**：这是唯一构成**硬依赖**的跨插件引用——全镜像共 **27 处**指向它（`run-tasks/SKILL.md` 8、`create-tasks/SKILL.md` 4、`run-tasks/references/communication-protocols.md` 3、`wave-lead.md` 3、`task-executor-v2.md` 2、`verification-patterns.md` / `create-spec` / `analyze-spec` / `spec-analyzer` / `context-manager` 各 1）。缺了它，`sdd-tools` 的规划与执行链是**断的**。

**对你的意义**：这份文档描述的正是 **WorkBuddy 缺失的那套原语**。改造时读它，能明确知道"要替代掉什么"。

**适用场景**：理解 Claude Code 原生任务/团队机制；作为改造的对照文档。

---

### 6. `opencode-tools` —— OpenCode 扩展生成（未归档）

3660 行，18 个文件。7 个 skill（`oc-tool-dev` 统一入口 + create/update × skill/agent/command 各一对）+ 3 个 agent（`oc-researcher` 抓最新文档验证兼容、`oc-validator` 校验、`oc-generator` 生成）+ 4 份参考（`platform-overview.md` 436 行含平台差异表）。

**它是一个"模式范例"而非"移植工具"**：产出的是 **OpenCode 格式**，不读 Claude 插件、也不输出其他格式。

**最有价值的 40 行**：`platform-overview.md` 里的 **"Key Differences from Claude Code"** 差异表。摘要：

| 特性 | Claude Code | OpenCode |
|---|---|---|
| 团队编排 | 完整（TeamCreate/SendMessage） | **完全没有** —— 只能顺序/并行 `task` 调用 |
| skill 组合 | 文件路径加载 | **名字注册表** |
| 子代理提问工具 | 可用 | **不可用**，仅主 agent |
| 插件 SDK | 无（hooks 是 JSON） | `@opencode-ai/plugin`（ESM JS/TS） |
| hook 格式 | `hooks.json` | JS/TS 插件文件 |
| 规则文件 | `CLAUDE.md` | `AGENTS.md` |

**注意**：OpenCode 同样缺 `TeamCreate`/`SendMessage` —— **与 WorkBuddy 缺口相同**。作者面对这个缺口时的取舍（降级成串行/并行 task），大概率就是你该做的取舍。

**关键信号**：作者**没有**把 core-tools 机械转换到 OpenCode，而是**新写了一个 opencode-tools 插件**。这说明他的判断是：**原语差异大到硬转不如重写**。你的改造策略应参考这一点。

**适用场景**：给 OpenCode 写扩展；**借它的差异表与策略判断改造 WorkBuddy 的方案**。

---

### 7. `cs-tools` —— 竞赛编程（未归档）

3471 行，11 个文件。2 个 agent（`problem-solver`、`solution-verifier`）+ 7 个 skill：`data-structures`(450)、`dp-patterns`(428)、`graph-algorithms`(478)、`math-and-combinatorics`(492)、`search-and-optimization`(493)、`string-algorithms`(450)、`solve`(164)、`verify`(136)。

**适用场景**：算法练习、LeetCode 题解、算法教学（含"带教育性解释"）。

---

### 8. `git-tools` —— Git 自动化（未归档）

仅 2 个文件 / 159 行。Conventional Commits 自动化。**几乎是空壳**，是 9 个里最轻的。

**适用场景**：规范化 git 提交信息。

---

## 六、插件之间怎么配合

```
                    ┌─────────────────────────────────────┐
                    │  core-tools（读懂现状）              │
                    │  deep-analysis 6 阶段 → 架构图/报告  │
                    └──────────────┬──────────────────────┘
                                   │ 理解之后
                                   ▼
   ┌───────────────────────────────────────────────────────┐
   │  sdd-tools（规划并建造）                                │
   │  create-spec → analyze-spec → create-tasks → execute   │
   │         ↑ 其中的代码库勘察可复用 core-tools 的洞察        │
   └──────────────┬────────────────────────────────────────┘
                  │ 实现时
                  ▼
   ┌─────────────────────────────┐   ┌──────────────────────┐
   │  tdd-tools（测试驱动保证质量） │   │  dev-tools（日常辅助） │
   │  tdd-cycle / generate-tests  │   │  bug-killer / docs    │
   └─────────────────────────────┘   └──────────────────────┘

   claude-tools（底层参考）：所有插件依赖的 Claude 原语文档
   ```

   **对你（改造 WorkBuddy 版）的组合建议**：

   1. **core-tools** = 目标能力本体（要改造的）
   2. **claude-tools** = 差异对照（明确要替换掉哪些原语）
   3. **opencode-tools** = 策略参考（看作者如何处理同类缺口）
   4. **sdd-tools / tdd-tools / dev-tools** = 后续扩展储备

---

## 七、目录结构与指纹

```
agent-alchemy-marketplace/                    125 files（上游原样 123）
├── README.md                                 ← 本文件（本地文档）
├── .claude-plugin/
│   └── marketplace.json                      1 file   指纹 bc0236b5d4cbd3baedcda888549e1419
├── core-tools/              26 files /  5,774 md 行   指纹 808192241ec2c53ced9bd83227279279  (+PROVENANCE.md)
├── claude-tools/             9 files /  3,033 md 行   指纹 37c98b0026d9d87e376684c7a4bd147b
├── sdd-tools/               41 files / 12,716 md 行   指纹 d05f987a0964c02cd90b512a7234fba2
├── tdd-tools/               21 files /  8,961 md 行   指纹 fcfafcbfd6d2b114663a85675b0648a6
└── dev-tools/               25 files /  5,699 md 行   指纹 a9c9403919c7a3154afc000922a2f00b

```

**全部文件均从上游原样复制，未做任何修改。**（插件来自 `claude/<插件名>/`，注册表来自 `.claude-plugin/`）

> 本目录内仅两个文件不是上游件：`README.md`（本文件）与 `core-tools/PROVENANCE.md`（本地溯源记录）。因此对 `core-tools/` 做 `diff -rq` 会**稳定地多出这 1 行差异**，属预期。
>
> `.claude-plugin/` 的层级与上游差一层（本镜像拍平了上游的 `claude/`），详见顶层 README 第六节。

**校验镜像完整性**（应逐位得到上表指纹）：

```bash
cd /home/zhq/mydisk/myskill/external-skills/agent-alchemy-marketplace/<包名>
find . -type f ! -name PROVENANCE.md | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32
```

> ⚠️ `LC_ALL=C` 与 `! -name PROVENANCE.md` **缺一不可**：前者防 locale 排序漂移，后者防 `PROVENANCE.md` 自引用。详见顶层 README 第六节。**本节此前记录的 `f7e9c36c…`／`435ccfc9…`／`610ebe47…`／`86ead9e4…`／`33c8b817…` 五种值均已作废。**

---

## 八、本地已有的其他相关材料

| 路径 | 说明 |
|---|---|
| [`../README.md`](../README.md) | 顶层索引与**更新基线**：基准 commit、全部包指纹、已知本地偏差、更新检查方法 |
| [`core-tools/PROVENANCE.md`](core-tools/PROVENANCE.md) | core-tools 的逐文件 md5 与完整溯源（**本地新增文件，上游无此件**） |
| [`../skills/`](../skills/) | A 类独立 skill：`codebase-reading`、`deep-read`（上游未定位，非本市场资产） |

> 已删除（2026-09-19）：`../agent-alchemy-core-tools/`（并入本目录 `core-tools/`）、`../codebase-analysis/`（冗余，原件即 `core-tools/skills/codebase-analysis/`；该 skill 已确认后续不使用，不留适配留档）、`../CATALOG.md`（索引职责并入顶层 README）。

---

## 九、贡献者提醒：这不是 WorkBuddy 可用的 skill

⚠️ **本目录是"上游原始基线"，不是可直接运行的 WorkBuddy skill。**

已识别的改造障碍（详见 `../README.md`）：

1. **`${CLAUDE_PLUGIN_ROOT}` 路径变量** —— 全镜像实测 **104 处、分布 27 个文件**，WorkBuddy 不展开此变量
2. **Agent Teams 原语** —— `TeamCreate` / `TeamDelete` / `SendMessage` / `Task(model: opus|sonnet)` 在 WorkBuddy 中不存在，需映射为 `Task` 子代理 + 磁盘任务记录。**这套原语的完整语义在 [`claude-tools/`](claude-tools/) 里（3033 行）—— 改造前先读它，才能明确"要替代掉什么"；`sdd-tools` 的 27 处引用也全部指向它**
3. **目录约定** —— `.claude/sessions/`、`~/.claude/tasks/`、`.claude/agent-alchemy.local.md` 等路径需改为 WorkBuddy 的 `.workbuddy/` 树
4. **`AskUserQuestion` 在子代理中不可用**（这条在 OpenCode 说明里也出现过，需实测 WorkBuddy 行为）
5. **Context7 MCP 依赖** —— `interview-me` / `interview-researcher` 用到 `mcp__context7__*`，非 core-tools 分析链上的必需项


---

*本镜像仅作技术研究与改造基线用途。原项目 MIT 协议，版权归 Stephen Sequenzia。*
