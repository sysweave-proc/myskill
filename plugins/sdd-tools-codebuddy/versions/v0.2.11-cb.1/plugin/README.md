# agent-alchemy-sdd-tools · 使用手册

规格驱动开发（SDD）：**模糊想法 → 规格 → 任务 → 自主执行**。

> 本文件是**使用手册**，不属于上游移植内容（上游 `README.md` 未移植）。
> 上游来源：`sequenzia/agent-alchemy` → `agent-alchemy-sdd-tools` v0.2.11，commit `fc1a336b`，MIT。
> **同市场依赖**：`agent-alchemy-claude-tools`（任务/团队原语参考，**硬依赖**）；
> `agent-alchemy-core-tools`（`create-spec` 生成 Mermaid 图时用其 `technical-diagrams`）。

---

## 一、30 秒上手

插件**没有"启动"这个动作**，入口就是五条命令，按流水线顺序用：

| 步骤 | 输入 | 它实际会做什么 |
|---|---|---|
| 1. 出规格 | `/create-spec 用户想支持邮箱+Google 登录` | 自适应访谈（三档深度，命中有复杂度信号会自动扩容并问你）→ 落盘 `specs/SPEC-{name}.md` |
| 2. 体检 | `/analyze-spec specs/SPEC-login.md` | 找矛盾/遗漏/歧义 → 出 md + HTML 双报告 → 问你要不要建修复任务 |
| 3. 拆任务 | `/create-tasks specs/SPEC-login.md` | 依赖排序 + 验收标准 + `task_group` 元数据；重跑时按 `task_uid` 智能合并 |
| 4a. 执行（默认） | `/execute-tasks --max-parallel 3` | 单编排器 + 每任务一个 agent + 共享执行上下文；中断可续 |
| 4b. 执行（团队版） | `/run-tasks --dry-run` | 拓扑分波 → 每波一个 `wave-lead` 组队 → `context-manager` 传知识 → 三级重试；`--dry-run` 只看计划 |

**不想记命令**就直接说人话，`description` 里的中文触发词会让模型自动加载对应 skill：

```
帮我把这个需求整理成规格文档
把这份规格拆成任务
按依赖顺序把没做的任务跑掉
```

---

## 二、四段流水线

```
/create-spec    →  specs/SPEC-{name}.md                      自适应访谈生成规格
      ↓
/analyze-spec   →  {name}.analysis.md + {name}.analysis.html  规格质量体检
      ↓
/create-tasks   →  Task 原语（task_uid / task_group / 验收标准 / blockedBy）
      ↓
/execute-tasks  →  单编排器波次执行        ← 默认
/run-tasks      →  Agent Teams 波次执行    ← 需要团队编排/--phase/--dry-run 时用
```

**`/execute-tasks` 与 `/run-tasks` 的区别**（这是最容易混的两条）：

| | `/execute-tasks` | `/run-tasks` |
|---|---|---|
| 编排方式 | 单编排 skill 派 agent | 每波一个 `wave-lead` **自己组队**（TeamCreate） |
| 跨任务知识 | 共享 `execution_context.md` | `context-manager` 显式分发消息（每波任务 ≥3 才拉） |
| 参数 | `[task-id]`、`--task-group`、`--retries`、`--max-parallel` | 上面全部 + `--phase <N,M>` + `--dry-run` |
| 适用 | 大多数情况 | 想要团队级并行/分阶段推进/先看计划 |

---

## 三、打完后会看到什么

### `/create-spec`

```
三档深度：high-level（6-10 问）｜detailed（12-18 问）｜full-tech（18-25 问）
命中复杂度信号 → 自动扩容到 28-40 问（先征求你同意）
可选：codebase-explorer 探代码库 ｜ researcher 查外部资料（**仅在你明确要求时**）
输出：specs/SPEC-{name}.md（含验收标准、边界、非目标）
```

### `/analyze-spec`

```
Critical / Warning / Info 三级发现 → 逐条与你确认
输出：{name}.analysis.md + {name}.analysis.html（可评审界面）
可选：把发现变成 spec-fixes-{name} 任务组 → /run-tasks --task-group spec-fixes-{name}
```

### `/create-tasks`

```
按 phase 分解 + 依赖推断 + 验收标准 + task_group 元数据
重跑 = **合并模式**：已完成不动｜待办按新规格更新｜进行中跳过｜新需求新建
```

### `/execute-tasks` / `/run-tasks`

```
[a] 过滤任务 → [b] 拓扑分波（无依赖先跑；循环依赖在最薄弱环断开）
[c] 每波并行执行（默认上限 5；超过则拆子波 N.1 / N.2）→ [d] 逐条校验验收标准
[e] 失败重试（`--retries`，默认 3）→ [f] 汇总
会话产物：.codebuddy/sessions/__live_session__/（中断后从下一个未阻塞波继续）
```

---

## 四、怎么判断"整个插件"在工作

关键信号：**有没有派生 agent / 组建队伍**。

| 现象 | 含义 |
|---|---|
| `/create-spec` 派出了 `codebase-explorer` 或 `researcher` | ✅ agent 已加载（且你确实要求了探索/调研） |
| `/run-tasks` 出现了 `wave-lead` → `context-manager` → 每任务一个 `task-executor-v2` | ✅ 完整生效（团队原语可用） |
| `/execute-tasks` 每任务一个 `task-executor` | ✅ 完整生效 |
| 全程只有它自己读写文件，没有任何子代理 | ❌ agent 未加载，退化成单线程 —— 见排错 |
| `/run-tasks` 建队失败退回串行 | 团队原语不可用或 agent 未加载；功能不丢，但不再是并行 |

---

## 五、配置（可选）

在**项目根目录**建 `.codebuddy/agent-alchemy.local.md`，用 YAML frontmatter 写设置，不建则全走默认值：

```markdown
---
run-tasks.max_parallel: 3                 # 每波并行上限（默认 5）
run-tasks.max_retries: 2                  # 每层重试次数（默认 1）
run-tasks.retry_partial: false            # 是否重试 PARTIAL 任务（默认 false = 直接标记完成）
run-tasks.context_manager_threshold: 3    # 每波任务数 ≥ 该值才拉 context-manager（默认 3）
run-tasks.wave_lead_model: opus           # wave-lead 的模型档
run-tasks.context_manager_model: sonnet   # context-manager 的模型档
run-tasks.executor_model: opus            # task-executor 的模型档
---
```

优先级：**CLI flag > 设置文件 > 内置默认值**。文件缺失或 YAML 写坏都不是错误 —— 会静默用默认值（写坏时打一条 warning）。

**运行时产物**：

| 路径 | 内容 |
|---|---|
| `.codebuddy/sessions/__live_session__/` | `execution_context.md`、`execution_plan.md`、`progress.md`、`context-task-{id}.md`、`result-task-{id}.md`、`tasks/`、`.lock`、`.abort` |
| `.codebuddy/sessions/interrupted-{时间戳}/` | 中断归档 |
| `.codebuddy/teams/` | 波次团队目录（`/run-tasks` 用） |
| `~/.codebuddy/tasks/{TASK_LIST_ID}/execution_pointer.md` | 指向 live session 的指针，供中断续跑 |
| `specs/SPEC-{name}.md`、`{name}.analysis.md/.html` | 规格与其体检报告 |

会话/团队目录的写入由插件的 **hook 自动放行**，不会弹审批。

---

## 六、排错

| 现象 | 原因 | 处理 |
|---|---|---|
| 打 `/create-spec` 没反应 | 插件没加载 | `/plugin list` 确认出现 `agent-alchemy-sdd-tools@<市场名>`；没有就先 `/plugin marketplace add <市场目录>` 再**完全重启** CodeBuddy |
| 读 `${CODEBUDDY_PLUGIN_ROOT}/../agent-alchemy-claude-tools/...` 失败 | 运行时不展开变量，或参考插件不在同一市场 | 装 `agent-alchemy-claude-tools` 到同一市场；正文已写 Glob 兜底（搜 `**/agent-alchemy-claude-tools/skills/**`） |
| 跑到一半频繁弹文件审批 | hook 未生效 | `hooks/auto-approve-session.sh` 需要 `jq`；缺 `jq` 时静默退化为正常审批流，不阻断 |
| 任务标记完成时被拦下并提示测试失败 | `TaskCompleted` 质量闸门生效 | 这是设计如此：`metadata.spec_path` 存在的任务完成时会跑项目测试，失败即阻止完成（认 pnpm/npm/pytest） |
| 队友 idle 却被告知要补发消息 | `TeammateIdle` hook 的 prompt 检查 | 提示执行者必须已发 TASK RESULT 与 CONTEXT CONTRIBUTION；非执行者角色不适用 |
| `/run-tasks` 报 `--phase` 无匹配 | 任务没有 phase 元数据 | 用 `/create-tasks --phase 1,2` 重跑生成带 phase 的任务，或不带 `--phase` 执行 |
| 没看到任何弹窗提问 | 当前运行时不支持 `AskUserQuestion` | 退化成文字提问，功能不丢，只是体验不同 |

---

## 七、这个包里有什么

```
agent-alchemy-sdd-tools/
├── commands/   5 个命令入口：/create-spec、/analyze-spec、/create-tasks、
│                     /execute-tasks、/run-tasks
├── skills/     5 个：create-spec、analyze-spec、create-tasks、execute-tasks、run-tasks
│                     （+ 各自 references/，analyze-spec 含 HTML 评审模板，
│                        execute-tasks 含 poll-for-results.sh 轮询脚本）
├── agents/     7 个：codebase-explorer（探索）、researcher（外部调研）、
│                     spec-analyzer（规格体检）、task-executor（4 阶段执行）、
│                     task-executor-v2（run-tasks 专用执行器）、
│                     context-manager（跨波知识）、wave-lead（波次领队）
├── hooks/      3 个事件：PreToolUse 自动放行、TaskCompleted 测试质量闸门、
│                     TeammateIdle 消息完整性检查（上游的建链 hook 未移植）
├── DEEP-DIVE.md  架构深度分析（上游原文，路径已本地化）
└── README.md     本手册
```

`/run-tasks` 的**消息协议与团队语义**来自同市场的 `agent-alchemy-claude-tools`
（`skills/claude-code-teams/` 与 `skills/claude-code-tasks/`）—— 那是本插件的硬依赖。
