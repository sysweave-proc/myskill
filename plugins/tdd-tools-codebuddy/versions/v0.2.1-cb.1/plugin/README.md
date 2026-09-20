# agent-alchemy-tdd-tools · 使用手册

用测试驱动实现：RED-GREEN-REFACTOR / 测试生成 / 覆盖率分析 / TDD 任务对。

> 本文件是**使用手册**，不属于上游移植内容（上游 `README.md` 未移植）。
> 上游来源：`sequenzia/agent-alchemy` → `agent-alchemy-tdd-tools` v0.2.1，commit `fc1a336b`，MIT。
> **同市场依赖**：复用 core-tools 的 `language-patterns` / `project-conventions`；
> 执行非 TDD 任务时复用 sdd-tools 的 `task-executor` agent。

---

## 一、30 秒上手

| 我要做什么 | 输入 | 它实际会做什么 |
|---|---|---|
| TDD 开发一个功能 | `/tdd-cycle 给订单模块加折扣计算` | 出 TDD 计划给你确认 → 写测试 → 跑出 RED → 实现 → GREEN → 重构 |
| 给已有代码补测试 | `/generate-tests src/order/pricing.py` | 自动识别框架（pytest / Jest / Vitest）→ 派 `test-writer` 并行生成行为级测试 |
| 看看测试覆盖缺口 | `/analyze-coverage --threshold 80` | 跑覆盖率 → 找未覆盖分支 → 给出可执行的补测建议 |
| 把 SDD 任务改成测试先行 | `/create-tdd-tasks` | 读 `/create-tasks` 生成的任务 → 为每个实现任务配对前置测试任务（RED-GREEN 依赖） |
| 自主跑完 TDD 任务 | `/execute-tdd-tasks --max-parallel 3` | 拓扑分波 → TDD 任务派 `tdd-executor`、非 TDD 派 sdd-tools 的 `task-executor` → 波次校验 |

**不想记命令**就直接说人话，`description` 里的中文触发词会让模型自动加载对应 skill：

```
走一遍红绿重构，把这个功能 TDD 出来
这段代码哪些分支没测到？
```

---

## 二、打完后会看到什么

### `/tdd-cycle`

```
1. 解析输入（功能描述 / 任务 ID / 规格章节）
2. 给出 TDD 计划 → AskUserQuestion 确认
3. RED    写测试 → 运行 → 必须**因为正确的原因失败**
4. GREEN  最小实现让测试通过
5. REFACTOR 重构并保持测试常绿
6. 用 test-rubric（行为驱动评分表）自检测试质量
```

### `/execute-tdd-tasks`

```
初始化 .codebuddy/sessions/__live_session__/
  ├── execution_context.md / execution_plan.md / task_log.md / progress.md
  └── execution_pointer.md → ~/.codebuddy/tasks/{TASK_LIST_ID}/execution_pointer.md
按依赖分波 → 每波并行跑（默认上限 5）→ 失败任务重试（默认 3 次）
中断后可从「下一个未阻塞波」继续，不必从头再来
```

### `/create-tdd-tasks` 与 `/analyze-coverage`

- `create-tdd-tasks` **不改写已有任务**，只补齐「前置测试任务 + RED-GREEN 依赖」；
  没有任务时会明确让你先跑 `/create-tasks`。
- `analyze-coverage` 输出的是**补测建议**（缺哪个行为、该加什么测试），不是只报一个百分比。

---

## 三、怎么判断"整个插件"在工作

| 现象 | 含义 |
|---|---|
| `/generate-tests` 派出了多个 `test-writer` 子代理 | ✅ agent 已加载 |
| `/execute-tdd-tasks` 派出 `tdd-executor`（TDD 对）与 `task-executor`（非 TDD） | ✅ 完整生效 |
| 只有它自己埋头写测试，没有任何子代理 | ❌ agent 未加载，退化成单线程 —— 见排错 |

---

## 四、配置（可选）

在**项目根目录**建 `.codebuddy/agent-alchemy.local.md`，不建则全走默认值：

```markdown
- **tdd**:
  - **coverage-threshold**: 80          # analyze-coverage 的默认阈值（默认 80）
  - **strictness**: standard            # RED 阶段遇到"实现前就通过"的测试怎么办
  - **test-review-threshold**: 70       # test-reviewer 评分表合格线（默认 70）
  - **framework**: auto                 # auto | pytest | jest | vitest；自动识别失败时兜底
  - **max-parallel**: 5                 # execute-tdd-tasks 每波并行度（可被 --max-parallel 覆盖）
```

优先级：命令行 flag > 该配置文件 > 内置默认值。

---

## 五、排错

| 现象 | 原因 | 处理 |
|---|---|---|
| 打 `/tdd-cycle` 没反应 | 插件没加载 | `/plugin list` 确认出现 `agent-alchemy-tdd-tools@<市场名>`；没有就先 `/plugin marketplace add <市场目录>` 再**完全重启** CodeBuddy |
| `/create-tdd-tasks` 说找不到任务 | 还没跑过 `/create-tasks` | 先装并运行 sdd-tools 的 `/create-tasks <spec-path>` |
| 跑 `/execute-tdd-tasks` 频繁弹文件审批 | hook 未生效 | `hooks/auto-approve-session.sh` 需要 `jq` 解析输入；缺 `jq` 时静默退化为正常审批流（不阻断，但也不放行） |
| 非 TDD 任务报 `task-executor` 找不到 | sdd-tools 没装在同一市场 | 在本市场同时启用 `agent-alchemy-sdd-tools` |
| 读 `${CODEBUDDY_PLUGIN_ROOT}/../agent-alchemy-core-tools/...` 失败 | 运行时不展开变量，或两个插件不在同一市场 | 正文已写兜底：Glob 搜 `**/agent-alchemy-core-tools/skills/**` 按名字定位 |

---

## 六、这个包里有什么

```
agent-alchemy-tdd-tools/
├── commands/   5 个命令入口：/tdd-cycle、/generate-tests、/analyze-coverage、
│                     /create-tdd-tasks、/execute-tdd-tasks
├── skills/     5 个：tdd-cycle、generate-tests、analyze-coverage、
│                     create-tdd-tasks、execute-tdd-tasks
├── agents/     3 个：tdd-executor（6 阶段 TDD 执行）、test-writer（测试生成）、
│                     test-reviewer（按评分表评审测试）
├── hooks/      PreToolUse 自动放行（会话目录写入）—— 上游的建链 hook 未移植
└── README.md   本手册
```

**知识库引用**：`tdd-executor` / `test-writer` 原本通过上游的 `skills:` 预加载字段引用
core-tools 的 `language-patterns` / `project-conventions`；本产物改为正文顶部的
「Required knowledge loading」段（`Read` 同一份文件），能力等价。
