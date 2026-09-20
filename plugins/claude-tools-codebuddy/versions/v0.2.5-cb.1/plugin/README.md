# agent-alchemy-claude-tools · 使用手册

Task 管理原语 与 Agent Teams 原语的**参考手册**（不是流程，也不是命令）。

> 本文件是**使用手册**，不属于上游移植内容（上游 `README.md` 未移植）。
> 上游来源：`sequenzia/agent-alchemy` → `agent-alchemy-claude-tools` v0.2.5，commit `fc1a336b`，MIT。

---

## 一、这个插件是干什么的

它不是"用户打命令"的插件，而是**给其他 skill / agent 读的底层参考**。两个 skill 都标为
`user-invocable: false`，没有 `commands/`：

| Skill | 内容 | 谁在读 |
|---|---|---|
| `claude-code-tasks` | 6 个任务工具：`TaskCreate` / `TaskGet` / `TaskList` / `TaskUpdate`（结构化跟踪）+ `TaskOutput` / `TaskStop`（后台执行）；参数、状态生命周期、完成规则、依赖管理、常见反模式 | sdd-tools 的 `/create-tasks`、`spec-analyzer`、`task-executor-v2`、`wave-lead` |
| `claude-code-teams` | Agent Teams：`TeamCreate` / `Task(name:, team_name:)` / `SendMessage` 消息类型 / `shutdown_request` 握手 / 团队生命周期 / `TeammateIdle`、`TaskCompleted` 等 hook 事件 / 6 种编排模式 | sdd-tools 的 `/run-tasks`、`context-manager`、`wave-lead` |

**跨插件引用规模**：`sdd-tools` 全镜像共 **27 处**指向本插件（含 `/run-tasks` 8 处、`/create-tasks` 4 处、
`/run-tasks/references/communication-protocols.md` 3 处、`wave-lead` 3 处、`task-executor-v2` 2 处等）。
**缺了本插件，sdd-tools 的规划与执行链是断的** —— 所以它必须与 sdd-tools 装在同一个市场里。

---

## 二、为什么值得单独装

除了被 sdd-tools 依赖，它本身也是**改造/自建多智能体流程时的对照文档**：

- 想知道 CodeBuddy 的 `Task` / `TeamCreate` / `SendMessage` 到底有哪些参数、状态怎么流转 —— 直接读它
- 想自己写一个"建队 → 派活 → 收结果 → 解散"的流程 —— `orchestration-patterns.md`（792 行）给了 6 种现成拓扑
- 想避免踩坑 —— `anti-patterns.md`（274 行）列了任务与消息层面的典型错误

它也解释了**为什么 core-tools 的 deep-analysis 不必降级**：hub-and-spoke 拓扑所需原语在这里都有定义。

---

## 三、怎么用

无需任何命令。两种用法：

```
# 1. 让模型自己加载（description 含中英双语触发词）
怎么给队友派活？团队的 hook 事件有哪些？

# 2. 在 skill / agent 正文里显式读取
Read ${CODEBUDDY_PLUGIN_ROOT}/skills/claude-code-tasks/SKILL.md
Read ${CODEBUDDY_PLUGIN_ROOT}/skills/claude-code-teams/SKILL.md
```

参考文件按需加载：

```
skills/claude-code-tasks/references/task-patterns.md          # 任务写法与状态流转范例（561 行）
skills/claude-code-tasks/references/anti-patterns.md          # 任务层反模式（274 行）
skills/claude-code-teams/references/messaging-protocol.md     # SendMessage 消息类型与投递机制（260 行）
skills/claude-code-teams/references/orchestration-patterns.md # 6 种编排模式（792 行）
skills/claude-code-teams/references/hooks-integration.md      # TeammateIdle / TaskCompleted 等 hook（337 行）
```

---

## 四、这个包里有什么

```
agent-alchemy-claude-tools/
├── skills/     2 个（都是 user-invocable: false 的参考型 skill）
│   ├── claude-code-tasks/   + 2 份 references
│   └── claude-code-teams/   + 3 份 references
└── README.md   本手册
```

**没有** `commands/`（上游两个 skill 都不可由用户直接调用，无需命令入口）；
**没有** `agents/`（上游没有 agent）；**没有** `hooks/`（上游也没有）。

---

## 五、注意事项

1. **移植说明在正文里** —— 两个 SKILL.md 的开头都有一段「移植说明」，说明：参数表按上游原样保留
   （CodeBuddy 的同名原语行为一致），而少数**平台注入的环境变量名**（`CLAUDE_CODE_TEAM_NAME`、
   `CLAUDE_TEAMMATE_ID` 等）按上游原样引用，是否需要改名以本机实际环境为准。
2. **skill 名保留 `claude-code-*`** —— 上游命名，且被 sdd-tools 的 27 处路径引用；
   改名会波及跨插件引用，收益为零，故保留（它描述的就是这套原语的谱系）。
3. **不参与用户交互** —— 它不会主动问你问题，也不会产生会话产物；它只在你或其它 skill 读它时起作用。
