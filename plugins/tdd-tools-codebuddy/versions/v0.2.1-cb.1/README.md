# v0.2.1-cb.1 —— tdd-tools 首次移植为 CodeBuddy 插件

> 状态：**冻结基准** ｜ 上游：`agent-alchemy-tdd-tools` v0.2.1（commit `fc1a336b`，MIT） ｜ 包指纹：`9a3e892b6b6deb735d87164667592cfa`

## 一、本版做了什么

把上游 `tdd-tools` 插件整体移植为 CodeBuddy 插件，**RED-GREEN-REFACTOR 流程、评分表、
并行波次执行、断点续跑逻辑一字未删**，改动收敛在路径变量、frontmatter、命令入口与 hook 裁剪。

## 二、包内构成

```
v0.2.1-cb.1/
├── README.md          本文件
├── PROVENANCE.md      逐文件 md5、上游对照、包指纹（权威记录）
├── source.zip         plugin/ 的权威打包存档
├── verify.sh          一键校准（基准本体 / 存档 / 上游 / 改造幅度）
└── plugin/            ← 交付产物（可安装的插件本体）
    ├── .codebuddy-plugin/plugin.json
    ├── README.md      使用手册（替换上游 README，非上游内容）
    ├── commands/      5 个斜杠命令
    ├── skills/        5 个 skill
    ├── agents/        3 个 agent
    └── hooks/         PreToolUse 自动放行（会话目录写入）
```

## 三、改动概览

| 层 | 改动 |
|---|---|
| 路径变量 | `${CLAUDE_PLUGIN_ROOT}` → `${CODEBUDDY_PLUGIN_ROOT}` |
| 跨插件引用 | `../core-tools` → `../agent-alchemy-core-tools`；`../sdd-tools` → `../agent-alchemy-sdd-tools` |
| 目录约定 | `.claude/` → `.codebuddy/`（含 `~/.claude/tasks/` → `~/.codebuddy/tasks/`） |
| 环境变量 | `CLAUDE_CODE_TASK_LIST_ID` → `TASK_LIST_ID`，并在首次出现处补一句「运行时未暴露该标识时用任务列表名或 `default`」 |
| agent / 命令引用 | `agent-alchemy-tdd:*`、`agent-alchemy-sdd:*` → 裸名（`/create-tasks`、`tdd-executor`…） |
| skill frontmatter | 去掉 `user-invocable` / `disable-model-invocation` / `argument-hint` / `arguments`；补 `version`；**description 增补中文触发词** |
| agent frontmatter | `tools` 数组 → 逗号串，补 `color`，description 改写为「Use this agent when … + Examples」并增补中文触发词；`skills:` 预加载改为正文「Required knowledge loading」段 |
| 命令入口 | 上游 5 个 `user-invocable` skill → 新增 5 个 `commands/*.md` |
| hooks | 保留 `auto-approve-session.sh`（改为放行 `.codebuddy/sessions/`、`~/.codebuddy/tasks/`）；**删除建链脚本** `resolve-cross-plugins.sh` 及 `hooks.json` 的 `SessionStart` 条目 |

**改造幅度**：逐字节一致 **4** ｜ 已改写 **16** ｜ 本产物新增 **6** ｜ 未移植 **1**（建链 hook）。

## 四、校准

```bash
bash verify.sh
```

任何对 `plugin/` 的修改都应**落到新版本目录**（如 `v0.2.1-cb.2/`）而不是原地改，否则本基准失效。
