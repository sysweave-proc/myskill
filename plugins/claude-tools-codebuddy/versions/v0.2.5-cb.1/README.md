# v0.2.5-cb.1 —— claude-tools 首次移植为 CodeBuddy 插件

> 状态：**冻结基准** ｜ 上游：`agent-alchemy-claude-tools` v0.2.5（commit `fc1a336b`，MIT） ｜ 包指纹：`1d0bc4896dff9d49d39a0becd9acbf59`

## 一、本版做了什么

把上游 `claude-tools`（**参考手册型插件**）移植为 CodeBuddy 插件。
它是 `sdd-tools` 的硬依赖（全镜像 27 处引用），缺了它 sdd-tools 的规划与执行链是断的。

内容上**不做语义裁剪**：两份参考（Task 工具 6 个、Agent Teams 全生命周期）与其 5 份 references 全部保留，
只改路径变量、目录约定、frontmatter，并在正文开头补一段「移植说明」。

## 二、包内构成

```
v0.2.5-cb.1/
├── README.md          本文件
├── PROVENANCE.md      逐文件 md5、上游对照、包指纹（权威记录）
├── source.zip         plugin/ 的权威打包存档
├── verify.sh          一键校准（基准本体 / 存档 / 上游 / 改造幅度）
└── plugin/            ← 交付产物（可安装的插件本体）
    ├── .codebuddy-plugin/plugin.json
    ├── README.md      使用手册（替换上游 README，非上游内容）
    └── skills/        2 个参考型 skill（均 user-invocable: false）+ 5 份 references
```

**没有** `commands/`（上游两个 skill 都不可由用户直接调用）、**没有** `agents/`、**没有** `hooks/`。

## 三、改动概览

| 层 | 改动 |
|---|---|
| 路径变量 | `${CLAUDE_PLUGIN_ROOT}` → `${CODEBUDDY_PLUGIN_ROOT}`（10 处） |
| 目录约定 | `.claude/` → `.codebuddy/`；`CLAUDE.md` → `CODEBUDDY.md` |
| 平台称谓 | 正文里指代运行时的 "Claude Code" → "CodeBuddy"（工具名、参数表**一律不动**） |
| skill frontmatter | 去掉 `user-invocable` / `disable-model-invocation` / `last-verified`，补 `version`；**description 增补中文触发词** |
| 新增段 | 两份 SKILL.md 的 H1 之后各加一段「**移植说明**」：说明参数表按上游保留、平台注入的环境变量名按上游原样引用、是否改名以本机实际环境为准 |
| 保留不动 | skill 名 `claude-code-tasks` / `claude-code-teams` —— 上游命名且被 sdd-tools 的 27 处路径引用，改名收益为零 |

**改造幅度**：逐字节一致 **1** ｜ 已改写 **8** ｜ 本产物新增 **1** ｜ 未移植 **0**。

## 四、校准

```bash
bash verify.sh
```

任何对 `plugin/` 的修改都应**落到新版本目录**（如 `v0.2.5-cb.2/`）而不是原地改，否则本基准失效。
