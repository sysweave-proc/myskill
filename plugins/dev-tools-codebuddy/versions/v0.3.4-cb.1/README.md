# v0.3.4-cb.1 —— dev-tools 首次移植为 CodeBuddy 插件

> 状态：**冻结基准** ｜ 上游：`agent-alchemy-dev-tools` v0.3.4（commit `fc1a336b`，MIT） ｜ 包指纹：`b2fd971573a6b02078c6bb5e3edb5323`

## 一、本版做了什么

把上游 `dev-tools` 插件整体移植为 CodeBuddy 插件，**流程逻辑一字未删**，改动全部收敛在
「路径变量 / 目录约定 / 插件清单 / skill frontmatter / agent frontmatter / 命令入口」六层。

## 二、包内构成

```
v0.3.4-cb.1/
├── README.md          本文件
├── PROVENANCE.md      逐文件 md5、上游对照、包指纹（权威记录）
├── source.zip         plugin/ 的权威打包存档
├── verify.sh          一键校准（基准本体 / 存档 / 上游 / 改造幅度）
└── plugin/            ← 交付产物（可安装的插件本体）
    ├── .codebuddy-plugin/plugin.json
    ├── README.md      使用手册（替换上游 README，非上游内容）
    ├── commands/      5 个斜杠命令
    ├── skills/        9 个 skill
    └── agents/        4 个 agent
```

## 三、改动概览

| 层 | 改动 |
|---|---|
| 路径变量 | `${CLAUDE_PLUGIN_ROOT}` → `${CODEBUDDY_PLUGIN_ROOT}` |
| 跨插件引用 | `../core-tools` → `../agent-alchemy-core-tools`（CodeBuddy 市场里目录名带组织前缀） |
| 目录约定 | `.claude/` → `.codebuddy/`；`CLAUDE.md` → `CODEBUDDY.md` |
| agent 引用 | `agent-alchemy-core-tools:code-architect` → 裸名 `code-architect`（CodeBuddy 的 `subagent_type` 不带插件前缀） |
| skill frontmatter | 去掉 `user-invocable` / `disable-model-invocation` / `argument-hint` / `model`，补 `version`；**description 增补中文触发词** |
| agent frontmatter | `tools` 数组 → 逗号串，补 `color`，description 改写为「Use this agent when … + Examples」形态并增补中文触发词；`docs-writer` 的 `skills: [technical-diagrams]` 改为正文「Required knowledge loading」段 |
| 命令入口 | 上游 5 个 `user-invocable` skill → 新增 5 个 `commands/*.md` 薄封装 |
| hooks | 上游唯一的 `resolve-cross-plugins.sh`（SessionStart 建短名符号链接）**不移植** —— CodeBuddy 本地市场是平铺结构，直接用带前缀的兄弟目录名即可解析 |

**改造幅度**：逐字节一致 **9** ｜ 已改写 **14** ｜ 本产物新增 **6** ｜ 未移植 **2**（hooks）。

## 四、校准

```bash
bash verify.sh
```

任何对 `plugin/` 的修改都应**落到新版本目录**（如 `v0.3.4-cb.2/`）而不是原地改，否则本基准失效。
