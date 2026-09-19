# agent-alchemy-core-tools · 使用手册

代码库分析 / 多智能体深度探索 / 交互式访谈。

> 本文件是**使用手册**，不属于上游移植内容（上游 `README.md` 未移植）。
> 上游来源：`sequenzia/agent-alchemy` → `agent-alchemy-core-tools` v0.2.3，commit `fc1a336b`，MIT。

---

## 一、30 秒上手

插件**没有"启动"这个动作**，它的入口就是下面三条命令 —— 打命令即是在用它：

| 我要做什么 | 输入 | 它实际会做什么 |
|---|---|---|
| 搞懂一个陌生/已有代码库 | `/deep-analysis 这套鉴权是怎么串起来的` | 侦察 → 生成焦点区 → 给你团队计划让你批 → 组队**并行**探索 → 综合 |
| 要一份结构化报告 | `/codebase-analysis` | 深读 → 出架构图 + 报告 → 问你要不要存盘/更新文档 |
| 把一件事想透 | `/interview-me 我在纠结要不要把这个模块拆开` | 一轮轮追问 + 按需查资料 → 落盘一份 markdown |

**不想记命令**就直接说人话，`description` 里的中文触发词会让模型自动加载对应 skill：

```
这个项目是干什么的？整体结构讲一下
帮我梳一遍 A 模块和 B 模块之间的关系
```

三条命令对应三条不同的能力链，**没有"一键全跑"的入口** —— 按需选一条即可。

---

## 二、打完后会看到什么

### `/deep-analysis`

```
[Phase 1/6] Reconnaissance & Planning — Mapping codebase structure...
  → 输出一份「团队计划」：拆成几个焦点区、每个焦点区派几个 explorer

[Phase 2/6] Review & Approval
  → 弹出选项问你：批准 / 修改 / 重新生成

[Phase 3/6] Team Assembly        ← 只有你批准后才继续
[Phase 4/6] Focused Exploration  → N 个 explorer 并行跑
[Phase 5/6] Synthesis            → 综合 + 用 Bash 深挖（git 历史、依赖树）
[Phase 6/6] Completion           → 归档会话、解散团队
```

### `/codebase-analysis`

3 个阶段，**必须跑完**：深读 → 报告（执行摘要 / 架构总览含 Mermaid 图 / 技术栈 / 关键文件 / 风险 / 建议）→ 后续动作（存报告、存自定义报告、更新文档、留一份速查）。

### `/interview-me`

先问 5 个框定问题（主题 / 目标 / 焦点 / 深度 / 产出物与路径），然后按你选的深度一轮轮追问。所有面向你的提问**都是弹选项的**，不会用一段话糊弄。

---

## 三、怎么判断"整个插件"在工作

关键信号：**有没有派生多个子代理**。

| 现象 | 含义 |
|---|---|
| `/deep-analysis` 派出多个 `code-explorer` + 1 个 `code-synthesizer` | ✅ 插件完整生效（agent 全部就位） |
| 只有它自己埋头读文件，**没有任何子代理** | ❌ 插件未完整加载，退化成单线程 —— 检查下面的排错 |

---

## 四、配置（可选）

在**项目根目录**建 `.codebuddy/agent-alchemy.local.md`，不建则全走默认值：

```markdown
## agent-alchemy 配置

- **deep-analysis**:
  - **direct-invocation-approval**: true     # 你直接调用时，团队计划是否要人工批准（默认 true）
  - **invocation-by-skill-approval**: false  # 被其他 skill 调用时是否批准（默认 false = 自动批准）
  - **cache-ttl-hours**: 24                  # 探索缓存有效期，0 = 关闭缓存
  - **enable-checkpointing**: true           # 逐阶段写 checkpoint，支持中断续跑
  - **enable-progress-indicators**: true      # 是否显示 [Phase N/6]

- **interview-me**:
  - **default-depth**: detailed              # overview | detailed | deep-dive
  - **default-output-type**: report-detailed # report-detailed | report-summary | implementation-plan | something-else
  - **output-directory**: internal/interviews/
  - **proactive-research-budget**: 3          # 0 = 关闭主动研究
  - **enable-context-argument**: true
  - **slug-collision-strategy**: timestamp-suffix
```

嫌它老问你批不批，就把 `direct-invocation-approval` 设成 `false`。

**运行时产物**都落在项目内 `.codebuddy/sessions/`：

| 路径 | 内容 |
|---|---|
| `.codebuddy/sessions/__da_live__/` | 进行中会话：`checkpoint.md`、`team_plan.md`、`recon_summary.md`、`explorer-{N}-findings.md`、`progress.md`、`synthesis.md` |
| `.codebuddy/sessions/exploration-cache/` | 探索缓存（按 TTL 复用，24h 内重跑同一分析会命中） |
| `.codebuddy/sessions/da-{timestamp}/` | 已完成会话归档 |

这些目录的读写由插件的 **hook 自动放行**，不会弹审批。如果频繁弹审批 → 见排错第 4 条。

---

## 五、排错

| 现象 | 原因 | 处理 |
|---|---|---|
| 打 `/deep-analysis` 没反应 | 插件没加载 | `/plugin list` 确认出现 `agent-alchemy-core-tools@<你的市场名>`；没有就先 `/plugin marketplace add <市场目录>` 再**完全重启** CodeBuddy（不是新开对话） |
| 命令能跑，但没有任何子代理 | agent 没加载（可能只装了 skills，没走插件通道） | 确认装的是**插件**而不是把 `skills/` 拷到 `~/.codebuddy/skills/` |
| 跑到一半频繁弹文件审批 | hook 未生效 | 检查 `jq` 是否安装（hook 用它解析输入）；缺 `jq` 时 hook 静默失效，不阻断但也不放行 |
| 没看到任何弹窗提问 | 当前运行时不支持 `AskUserQuestion` | 它会退化成用文字提问，功能不丢，只是体验不同 |
| 想研究某个库但查不到资料 | 未配置 Context7 MCP | 只有 `interview-me` 的主动研究用到；缺失时自动退回 WebSearch/WebFetch，不阻断 |

---

## 六、这个包里有什么

```
agent-alchemy-core-tools/
├── commands/   3 个命令入口：/deep-analysis、/codebase-analysis、/interview-me
├── skills/     6 个：deep-analysis、codebase-analysis、interview-me、
│                     language-patterns、project-conventions、technical-diagrams
├── agents/     4 个：code-explorer（探索）、code-synthesizer（综合）、
│                     code-architect（实现蓝图）、interview-researcher（访谈研究）
├── hooks/      PreToolUse 自动放行（会话/缓存目录写入）
└── README.md   本手册
```

`language-patterns` / `project-conventions` / `technical-diagrams` 三个**不是入口** ——
它们是被流程与子代理加载的知识库（语言模式、项目约定、Mermaid 图表规范）。

`code-architect` 也可被其他插件复用（例如 dev-tools 的 `feature-dev`）。
