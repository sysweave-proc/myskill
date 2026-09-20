# v0.2.11-cb.1 —— sdd-tools 首次移植为 CodeBuddy 插件

> 状态：**冻结基准** ｜ 上游：`agent-alchemy-sdd-tools` v0.2.11（commit `fc1a336b`，MIT） ｜ 包指纹：`7bd5a590e650a9c9b97aae5152baf596`

## 一、本版做了什么

把上游 `sdd-tools`（市场里**最大**的插件：5 skill / 7 agent / 3 hook 事件 / 5 份 references +
HTML 评审模板 + 轮询脚本）整体移植为 CodeBuddy 插件。

**流程逻辑一字未删**：自适应访谈的三档深度与复杂度扩容、规格体检的缺陷分类、
`task_uid` 增量合并、拓扑分波、三层 agent 架构（Orchestrator → Wave Lead → Context Manager）、
并行度封顶、三级重试、中断会话恢复（含孤儿团队目录扫描）全部保留。

**这次移植最关键的一点**：上游 `run-tasks` 深度依赖 `claude-tools` 插件（任务/团队原语手册）。
CodeBuddy 实测具备同名原语（`TeamCreate` / `TaskCreate` / `SendMessage` / `AskUserQuestion`），
因此**执行层未降级**为串行 task 调用，而是按原架构落地，只把跨插件路径改成同市场的
`agent-alchemy-claude-tools`。

## 二、包内构成

```
v0.2.11-cb.1/
├── README.md          本文件
├── PROVENANCE.md      逐文件 md5、上游对照、包指纹（权威记录）
├── source.zip         plugin/ 的权威打包存档
├── verify.sh          一键校准（基准本体 / 存档 / 上游 / 改造幅度）
└── plugin/            ← 交付产物（可安装的插件本体）
    ├── .codebuddy-plugin/plugin.json
    ├── README.md      使用手册（替换上游 README，非上游内容）
    ├── DEEP-DIVE.md   上游架构深度分析（路径已本地化，保留）
    ├── commands/      5 个斜杠命令
    ├── skills/        5 个 skill（+ references / HTML 模板 / 轮询脚本）
    ├── agents/        7 个 agent
    └── hooks/         3 个事件（PreToolUse / TaskCompleted / TeammateIdle）
```

## 三、改动概览

| 层 | 改动 |
|---|---|
| 路径变量 | `${CLAUDE_PLUGIN_ROOT}` → `${CODEBUDDY_PLUGIN_ROOT}`（14 处） |
| 跨插件引用 | `../claude-tools` → `../agent-alchemy-claude-tools`（26 处，本插件最重的依赖）；`../core-tools` → `../agent-alchemy-core-tools`（1 处） |
| 目录约定 | `.claude/` → `.codebuddy/`（含 `~/.claude/tasks/`、`.claude/teams/`） |
| 环境变量 | `CLAUDE_CODE_TASK_LIST_ID` → `TASK_LIST_ID`，并在两处首次出现处补「运行时未暴露该标识时用任务列表名或 `default`」 |
| agent / 命令引用 | `agent-alchemy-sdd:*` 等命名空间前缀 → 裸名 |
| skill frontmatter | 去掉 `user-invocable` / `disable-model-invocation` / `argument-hint` / `arguments`；补 `version`；**description 增补中文触发词** |
| agent frontmatter | `tools` 数组 → 逗号串，补 `color`，description 改写为「Use this agent when … + Examples」并增补中文触发词；`skills:` 预加载改为正文「Required knowledge loading」段；`researcher` 去掉写死的 `mcp__context7__*` 改为可选说明 |
| 命令入口 | 上游 4 个 `user-invocable` skill → 4 个 command；**另补 1 个 `/run-tasks`**（上游漏标 `user-invocable` 但其 README 与 `analyze-spec` 都以命令形式引用它） |
| hooks | 保留 `auto-approve-session.sh`（改放行 `.codebuddy/`）、`verify-task-completion.sh`（原文未改）、`TeammateIdle` prompt；**删除建链脚本** `resolve-cross-plugins.sh` 与 `hooks.json` 的 `SessionStart` 条目 |

**改造幅度**：逐字节一致 **16** ｜ 已改写 **24** ｜ 本产物新增 **6** ｜ 未移植 **1**（建链 hook）。

## 四、校准

```bash
bash verify.sh
```

任何对 `plugin/` 的修改都应**落到新版本目录**（如 `v0.2.11-cb.2/`）而不是原地改，否则本基准失效。
