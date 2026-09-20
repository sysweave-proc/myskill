# myskill

个人资产仓：**3 个在用 skill** + **1 个留档 skill** + **5 个 CodeBuddy 插件** + 上游留档与评测产物。

## 目录

| 节 | 讲什么 |
|---|---|
| [布局](#布局) | 目录结构，以及 skill 与插件的判别 |
| [资产速览](#资产速览) | 粗表：8 个在用资产 + 1 个留档 skill，一行一个（每行带详情跳转） |
| [用法详解](#用法详解) | 每个插件的命令、用法、作用 |
| [场景与对比](#场景与对比) | 同域资产之间的差别与适用场景（详细） |
| [安装与校准](#安装与校准) | install.sh / 依赖 / verify.sh |
| [留档与产物](#留档与产物) | 上游镜像留档、评测产物 |
| [约定](#约定) | 新增 skill 的目录结构、中文触发词 |

## 布局

```
myskill/
├── skills/                        【skill】装到 ~/.codebuddy/skills/
│   ├── repo-wiki-authoring/       自建 · 仓库 wiki 地图
│   ├── codebase-reading/          外部来源 · 阅读成稿（五件套）
│   ├── deep-read/                 外部来源 · 逐行读源码出事实
│   └── source-code-reading-skill/ 自建 ·【留档】已被外部 skill 取代，暂不使用
├── plugins/                       【插件】装进本地市场 agent-alchemy-local
│   ├── core-tools-codebuddy/      读懂代码库
│   ├── sdd-tools-codebuddy/       规格驱动开发
│   ├── tdd-tools-codebuddy/       测试驱动开发
│   ├── dev-tools-codebuddy/       日常开发辅助
│   └── claude-tools-codebuddy/    原语参考手册（无命令）
├── external-skills/               【留档】上游市场整包镜像，不是本仓资产
│   └── agent-alchemy-marketplace/ 5 插件 + 注册表（移植包的比对基线）
└── skill-test/                    【评测产物】外部 skill 的实测输出
```

**skill 与插件是两种东西**，决定放哪、装到哪：

| | 根下是什么 | 装到哪 | 入口 |
|---|---|---|---|
| **skill** | `SKILL.md` + `references/` | `~/.codebuddy/skills/` | **无命令**，靠 `description` 在相关语境自动加载 |
| **插件** | `.codebuddy-plugin/plugin.json` + `commands/` `skills/` `agents/` `hooks/` | 本地市场 `agent-alchemy-local` | **斜杠命令由插件提供** |

## 资产速览

粗表，只给定位；每个资产的用法与适用场景见后面各节（表格末列可跳转）。

### skill（`skills/`）— 详见[场景与对比](#场景与对比)

| skill | 状态 | 一句话定位 | 产出 | 版本 | 详情 |
|---|---|---|---|---|---|
| [`repo-wiki-authoring`](skills/repo-wiki-authoring/) | 在用 | 仓库级**宏观文档（地图）**写作方法论 | 子系统 wiki + 横切知识卡 | v0.2.0（无谱系） | [对比](#s-read-codebase) |
| [`codebase-reading`](skills/codebase-reading/) | 在用 | **体系化理解方法**：以目标 / 一条执行流为入口，理解过程由它支撑；**不做全覆盖** | 五件套：`README` / `code-reading` / `architecture`（C4）/ `api-flow` / `key-modules` | 外部来源 | [能力](#s-codebase-reading) |
| [`deep-read`](skills/deep-read/) | 在用 | 静态源码阅读的**深度上限**：有界目标内读到语句级 | 带 `文件:行号` 的事实，不出交付文档 | 外部来源 | [深度](#s-deep-read-depth) |
| [`source-code-reading-skill`](skills/source-code-reading-skill/) | **留档** | 自建 · **源码阅读知识建模**：先建可追溯模型，再投影成文档 | 图 / 表 / 文档；六阶段流程 | v0.1 → v0.6.0 | [对比](#s-read-codebase) |

> `source-code-reading-skill` 是自建产物，**已被外部 skill 取代，暂不使用，仅留档**：实际阅读走 `deep-read`（取事实）+ `codebase-reading`（成稿）；此包保留其七版演进谱系与对话过程供查。

### 插件（`plugins/`）— 命令见[用法详解](#用法详解)

| 插件 | 一句话定位 | 命令数 | 版本 | 详情 |
|---|---|---|---|---|
| [`core-tools-codebuddy`](plugins/core-tools-codebuddy/) | **读懂**现有代码库：深读、出报告、访谈 | 3 | `v0.2.3-cb.2` | [用法](#p-core-tools) |
| [`sdd-tools-codebuddy`](plugins/sdd-tools-codebuddy/) | **规划并建造**新功能：规格 → 任务 → 波次执行 | 5 | `v0.2.11-cb.1` | [用法](#p-sdd-tools) |
| [`tdd-tools-codebuddy`](plugins/tdd-tools-codebuddy/) | **用测试驱动实现**，含覆盖率缺口分析 | 5 | `v0.2.1-cb.1` | [用法](#p-tdd-tools) |
| [`dev-tools-codebuddy`](plugins/dev-tools-codebuddy/) | **日常开发**辅助：功能开发、排查、文档、发版 | 5 | `v0.3.4-cb.1` | [用法](#p-dev-tools) |
| [`claude-tools-codebuddy`](plugins/claude-tools-codebuddy/) | **参考手册型**：任务 / 团队原语文档，被 `sdd-tools` 读取 | 0（无命令） | `v0.2.5-cb.1` | [用法](#p-claude-tools) |

## 用法详解

<a id="p-core-tools"></a>

### core-tools-codebuddy `v0.2.3-cb.2` —— 读懂现有代码库

| 命令 | 用法 | 作用 |
|---|---|---|
| `/deep-analysis` | `/deep-analysis [上下文或焦点区]` | 6 阶段深读：侦察 → 动态规划 → 评审审批 → 组队 → 并行探索 → 综合；结束后归档会话并解散团队 |
| `/codebase-analysis` | `/codebase-analysis [上下文]` | 3 阶段：深读 → 出报告（含 Mermaid 架构图）→ 后续动作（存报告 / 更新文档 / 处理可执行洞察） |
| `/interview-me` | `/interview-me [主题或上下文文件]` | 自适应访谈（三档深度、主动研究、模板产出），落盘 markdown 报告 |

另带 3 个**被加载型** skill（无命令）：`language-patterns`、`project-conventions`、`technical-diagrams`。

<a id="p-sdd-tools"></a>

### sdd-tools-codebuddy `v0.2.11-cb.1` —— 规划并建造新功能

| 命令 | 用法 | 作用 |
|---|---|---|
| `/create-spec` | `/create-spec [context]` | 自适应访谈生成规格 → `specs/SPEC-{name}.md` |
| `/analyze-spec` | `/analyze-spec [spec-path]` | 规格体检 → md + HTML 双报告 → 可选建修复任务 |
| `/create-tasks` | `/create-tasks [spec] [--phase <phases>]` | 拆成带依赖 / 验收标准 / `task_group` 的任务；重跑走 `task_uid` 合并 |
| `/execute-tasks` | `/execute-tasks [task-id] [--task-group] [--retries] [--max-parallel]` | 单编排器波次执行（默认入口） |
| `/run-tasks` | `/run-tasks [...] [--phase N,M] [--dry-run]` | Agent Teams 波次执行（wave-lead 组队 + context-manager 跨波传知识） |

流水线：`/create-spec` → `/analyze-spec` → `/create-tasks` → `/execute-tasks`（或 `/run-tasks`）。市场里最大的一包（5 command / 5 skill / 7 agent / 3 hook 事件）。

<a id="p-tdd-tools"></a>

### tdd-tools-codebuddy `v0.2.1-cb.1` —— 用测试驱动实现

| 命令 | 用法 | 作用 |
|---|---|---|
| `/tdd-cycle` | `/tdd-cycle <功能描述｜任务ID｜规格章节>` | **从头实现**一个功能：完整 RED-GREEN-REFACTOR，先给计划确认再自主跑 |
| `/generate-tests` | `/generate-tests <spec｜task-id｜file>` | 已有代码或规格，**只补测试**（自动识别 pytest / Jest / Vitest，并行派 `test-writer`） |
| `/analyze-coverage` | `/analyze-coverage [项目路径] [--spec <path>] [--threshold <n>]` | 已有测试，**找缺口**并要可执行的补测建议 |
| `/create-tdd-tasks` | `/create-tdd-tasks [--task-group <group>]` | 把 SDD 任务转成「前置测试任务 + 实现任务」的 TDD 对 |
| `/execute-tdd-tasks` | `/execute-tdd-tasks [--task-group <g>] [--max-parallel <n>] [--retries <n>]` | 拓扑分波自主执行；TDD 对派 `tdd-executor`，非 TDD 派 sdd-tools 的 `task-executor` |

<a id="p-dev-tools"></a>

### dev-tools-codebuddy `v0.3.4-cb.1` —— 日常开发辅助

| 命令 | 用法 | 作用 |
|---|---|---|
| `/feature-dev` | `/feature-dev <功能描述>` | 7 阶段功能开发：理解 → 探索 → 提问 → 架构（2-3 套方案）→ 实现 → 评审 → 总结 |
| `/bug-killer` | `/bug-killer <bug 或报错> [--deep]` | 5 阶段假设驱动排查：复现 → 取证 → 根因 → 修复验证 → 复盘 |
| `/docs-manager` | `/docs-manager <动作或描述>` | 维护**正式文档**：MkDocs 站点或独立 markdown 的生成 / 更新 / 变更摘要 |
| `/document-changes` | `/document-changes [范围]` | 记录**这一次会话改了什么**，一次性变更报告 |
| `/release-python-package` | `/release-python-package [版本]` | Python 包发布（uv + ruff），9 步 fail-fast |

另带代码质量、架构模式、changelog 格式等**被加载型** skill（无命令）。

<a id="p-claude-tools"></a>

### claude-tools-codebuddy `v0.2.5-cb.1` —— 参考手册型

没有命令、没有 agent、没有 hook：**2 个被读取的 skill**（`claude-code-tasks` / `claude-code-teams` + 5 份 references），由 `sdd-tools` 的正文显式 `Read` —— 是它的**硬依赖**。

各命令的交互过程、可选配置与排错见对应包的 `versions/<版本>/plugin/README.md`（随插件交付的使用手册）；转换规则与上游同步清单见各包 `docs/CONVERSION.md`。

## 场景与对比

<a id="s-read-codebase"></a>

### 读懂一个代码库：6 个在用入口（+1 留档）

| 入口 | 关键差异 | 什么时候选它 |
|---|---|---|
| `deep-read`（skill） | 出**事实**，不写交付文档；每条结论带 `文件:行号` | 只要答案，不要文档 |
| `codebase-reading`（skill） | **体系化理解方法**：以目标 / 一条执行流为入口（定目标 → 跑起来 → C4 粗图 → 追链路 → git 考古 → 术语表）；理解过程由它支撑，**不做全覆盖**；**深度到模块级为止** | 要对一个目标 / 流程形成成体系的理解，并留下文档时（一般在对模块已有一定了解之后） |
| `repo-wiki-authoring`（skill） | 出**主题树**：一页一子系统 + 横切知识卡，每句带坐标 | 要长期维护的地图 |
| `/codebase-analysis` | 单线程 3 阶段，出一份报告 | 快速拿一份报告 |
| `/deep-analysis` | 团队式深读：侦察切成默认 3 个焦点区（小项目 2 / 大项目最多 4）→ 各区并行探、互不通信 → 1 个 synthesizer 合并、解冲突、补空白；亦可被其他 skill 当构件自动调用 |  |
| `/interview-me` | 不读代码，靠追问 + 按需查资料 | 要把一件事想透 |
| `source-code-reading-skill`（skill · **留档**） | 自建；出**知识模型**再投影成文档，面向 C/C++ 大型项目 | 已停用——实际阅读由 `deep-read` + `codebase-reading` 取代；仅留方法论谱系 |

三条最容易混的边界：

- **`deep-read` ↔ `codebase-reading`** —— 取证协议 vs 阅读方法论 + 成稿骨架。`deep-read`：每条结论锚 `文件:行号`、< 50 文件硬闸、只出报告；`codebase-reading`：给「怎么读」的完整流程与五件套文档结构，行号只是「when helpful」，范围靠目标与优先级软控制。差别在**证据强度与产出形态**。
- **`codebase-reading` ↔ `repo-wiki-authoring`** —— 「一个库 → 一套扁平五件套」 vs 「一个库 → 主题树 + 知识卡」。
- **`/codebase-analysis` ↔ `/deep-analysis`** —— 单线程出报告 vs 组团队并行。后者是 core-tools 的流程引擎，上游注明它被 `codebase-analysis`、`feature-dev`、`create-spec` 等作为可复用构件加载。

<a id="s-deep-read-depth"></a>

#### `deep-read` 能读到多深（深度上限）

6 阶段协议逐层加深，默认终点是**语句层 + 契约层**，再上系统层做归纳：

| 层 | 读到的内容 | 阶段 |
|---|---|---|
| 结构层 | 目录组织、技术栈（读配置不读文档）、入口点（读文件确认而非看文件名）、依赖中心度排名 | 2 MAP |
| 路径层 | 入口 → 终点的完整调用链（DB / API / IO / return），含错误路径、webhook、后台任务；每个**分支点**读条件本身 | 3 TRACE |
| 语句层 | 关键文件**逐行读**：把公式**写出来**（不是概述）、条件、状态变更与副作用，以及**已处理与未处理的边界** | 4 DEEP READ |
| 契约层 | 跨文件核对：调用方期望 vs 被调方实现、接口契约与抛错是否对齐 | 4 step 4 |
| 系统层 | ≥3 条模式（含隐式约定、反模式、技术债）、端到端数据流、风险与未校验假设（竞态 / 一致性 / 安全） | 5 CONNECT |

**硬边界**（它到不了的地方）：

- **静态阅读，不执行** —— 运行时行为、性能、真实并发时序只能推断，无法证实；不跑测试。
- **单次 < 50 源文件** —— 超出按「导入扇入 + 文件近因」**确定性裁剪**，越界必须在报告里声明为覆盖上限（不是任意采样）。
- **只出报告，不出文档** —— 这是与 `codebase-reading` / `repo-wiki-authoring` 的分界。
- **fork 内运行，不能中途问人** —— 真正的歧义以开放问题写进报告。

> 一句话：`deep-read` 的深度来自**范围有界**——在一个有界目标内，它能还原实际算术、分支条件、状态副作用和代码自己没兜住的边界，每条结论锚 `文件:行号`；但它止于运行时。

<a id="s-codebase-reading"></a>

#### `codebase-reading` 给的是什么（能力素描）

**以目标 / 一条执行流为入口的体系化理解方法** —— 理解过程本身由它支撑，五件套是这个过程的产物；**不做全覆盖**（skill 原话：`not read every file`），也不做逐条行号取证。**深度到模块级为止**，函数级细节交给 `deep-read`。

四层深度阶梯：`repo-wiki-authoring`（地图）→ **`codebase-reading`（体系化理解 + 成稿）** → `/deep-analysis`（团队式深读）→ `deep-read`（函数 / 语句级取证）。

流程：定目标 → 先跑起来（构建 + 跑一个测试/示例）→ 画 C4 粗图（L1–L3）→ 追一条真实链路（推荐断点实走）→ 把测试当文档（缺则写 characterization tests 记录现状）→ git 考古 → 从第一天起建术语表 → 按优先级深潜模块 → 成稿。

| 维度 | 事实 |
|---|---|
| 产出 | `code-reading/` 五件套：`README` / `code-reading` / `architecture` / `api-flow` / `key-modules`，**渐进披露**（专门文档按需加载） |
| 附带资产 | 跨语言工具清单（检索 / git 考古 / 按语言构建·测试·lint / 调试与 profiler）+ 术语表 **5 步构建法**（定义 / 用途 / 上下文 / 代码引用 / 关系 / 示例 / 缩写展开） |
| 证据强度 | `文件:行号` 是 when helpful、**不强制** |
| 范围控制 | 目标 + 优先级**软控制**，**无文件数闸门** |
| 不做 | 不执行、不测性能、不出架构决策 |

细节（11 步机制、内置资产、能力边界、内部小不一致）见 [`skills/codebase-reading/README.md`](skills/codebase-reading/README.md)。

<a id="s-sdd-tdd"></a>

### 拆任务并执行：sdd 与 tdd 两套

| | `sdd-tools-codebuddy` | `tdd-tools-codebuddy` |
|---|---|---|
| 拆任务 | `/create-tasks` —— 带依赖、验收标准、`task_group` | `/create-tdd-tasks` —— 转成「测试任务 + 实现任务」的 TDD 对 |
| 执行 | `/execute-tasks` 单编排器；`/run-tasks` 走 Agent Teams | `/execute-tdd-tasks` —— TDD 对派 `tdd-executor`，非 TDD 对派 sdd 的 `task-executor` |
| 什么时候用 | 常规功能开发，无「测试先行」硬要求 | 每步都要**验证闭环**：先让测试失败，再让实现通过 |

`tdd-tools` 这两个命令**依赖 sdd-tools**（读它的任务清单、复用它的 `task-executor`），必须装在同一市场。
`/execute-tasks` ↔ `/run-tasks` 只是编排方式不同：单编排器串波次 vs Agent Teams 分波组队（每波任务 ≥3 才值得）。

## 安装与校准

```bash
# 装（幂等；版本号可省略，自动取 versions/ 下最新版）
bash plugins/core-tools-codebuddy/install.sh        # 多数包的依赖
bash plugins/claude-tools-codebuddy/install.sh      # sdd-tools 的硬依赖
bash plugins/tdd-tools-codebuddy/install.sh
bash plugins/dev-tools-codebuddy/install.sh
bash plugins/sdd-tools-codebuddy/install.sh

# 校准（校验本版产物、存档、上游基线）
bash plugins/core-tools-codebuddy/versions/v0.2.3-cb.2/verify.sh
```

- **5 个包共用同一份 `install.sh`**（字节一致）：插件名读自包内 `plugin.json`、按 `plugins/` 重建市场清单，因此多插件共存互不覆盖。装完**完全重启** CodeBuddy，用 `/plugin list` 确认。
- **包间有依赖**（`sdd-tools → claude-tools` 27 处等），**必须装在同一市场**。
- **每包按版本聚合**：`versions/<版本>/{README.md, PROVENANCE.md, source.zip, verify.sh, plugin/}`，`plugin/` 是插件本体。**已冻结的版本目录不原地修改**，改动一律进新版本目录。
- **上游零改写**：所有改造只落在 `plugins/`，`external-skills/` 里的上游镜像始终原样，随时可逐包比对。

## 留档与产物

| 目录 | 是什么 |
|---|---|
| [`external-skills/`](external-skills/) | **上游留档**（不是本仓资产、不参与运行）：上游 [`sequenzia/agent-alchemy`](https://github.com/sequenzia/agent-alchemy) 的市场整包镜像（5 插件 + 注册表），是 `plugins/` 下 5 个移植包的上游比对基线。更新检查与已知偏差见其 [`README.md`](external-skills/README.md) |
| [`skill-test/`](skill-test/) | **评测产物**：`codebase-reading` / `deep-read` 在 PostgreSQL 19beta2 源码上的实测输出，[`postgres-notes/`](skill-test/postgres-notes/) 共 6 篇 |

## 约定

**本仓在用的 skill 放在 `skills/` 下**（此约定只管 `skills/`；`plugins/` 与 `external-skills/` 各按自己的形态）：

```
skills/<skill-name>/
├── README.md               是什么、来源、已知问题
└── versions/               有版本谱系时
    └── vX.Y/
        ├── README.md       本版说明：主题、变化、包内构成
        ├── skill/          交付产物
        ├── source.zip      原始打包（权威字节，勿改）
        └── conversation/   讨论过程
```

`skill/` 与 `source.zip` 是同一份内容的两种形态。**从未按版本冻结过的 skill 可省去 `versions/`**，本体直接放 `skill/`（如 `skills/repo-wiki-authoring/`、`skills/codebase-reading/`）。

改完 `skill/` 要回灌安装位（`skills/` 下的副本是安装位之外的另一份）：

```bash
cp -r skills/<skill-name>/skill/. ~/.codebuddy/skills/<skill-name>/
```

**中文触发词**：本仓 skill / agent 的 `description` 一律追加一行 `中文触发（用户这样说时使用）：…` —— 上游只有英文触发词，中文语境几乎不命中。
