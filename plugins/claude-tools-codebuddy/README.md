# agent-alchemy-claude-tools（CodeBuddy 版）

把上游 [`sequenzia/agent-alchemy`](https://github.com/sequenzia/agent-alchemy) 的 `claude-tools` 插件移植到 CodeBuddy。

| 项 | 内容 |
|---|---|
| 上游 | `agent-alchemy-claude-tools` v0.2.5 ｜ commit `fc1a336b`（2026-05-31）｜ MIT（版权归 Stephen Sequenzia） |
| 上游原样镜像 | [`../../external-skills/agent-alchemy-marketplace/claude-tools/`](../../external-skills/agent-alchemy-marketplace/claude-tools/)（只读，零改写） |
| 插件名 | `agent-alchemy-claude-tools`（沿用上游，保持跨插件引用一致） |
| 定位 | **参考手册型插件**：无命令、无 agent、无 hook，被其它 skill / agent 读取 |
| 被谁依赖 | `agent-alchemy-sdd-tools`（**27 处**硬引用：`run-tasks` 8、`create-tasks` 4、`communication-protocols.md` 3、`wave-lead` 3、`task-executor-v2` 2 等） |

**按版本聚合**：一版一个目录；`plugin/` 与 `source.zip` 是同一份内容的两种形态。

## 版本谱系

| 版本 | 主题 | 状态 |
|---|---|---|
| [`v0.2.5-cb.1`](versions/v0.2.5-cb.1/) | 首次移植为 CodeBuddy 插件（纯参考型：2 个 skill + 5 份 references） | **冻结基准** |

`-cb.N` 只在**上游版本不变、本产物需修订**时递增；上游版本变化时改为 `<新上游版本>-cb.1`。
旧版本目录**不再原地修改** —— 校准靠的是"基准不变"，改动一律进新版本目录。

## 目录结构

```
plugins/claude-tools-codebuddy/
├── README.md                本文件
├── docs/CONVERSION.md       本插件的转换规则 + 上游同步清单
└── versions/v0.2.5-cb.1/
    ├── README.md            本版说明：主题、包内构成、改动概览
    ├── PROVENANCE.md        逐文件 md5、与上游对照、包指纹
    ├── source.zip           plugin/ 的权威打包存档
    ├── verify.sh            一键校准
    └── plugin/              **交付产物**（安装这个目录）
```

## 安装

```bash
bash plugins/claude-tools-codebuddy/install.sh   # 幂等；自动取 versions/ 下最新版
bash plugins/sdd-tools-codebuddy/install.sh      # 唯一实际使用方
```

本插件**本身不产生任何用户可见入口**，装它的理由只有一个：**让 `sdd-tools` 的规划与执行链不断链**。所以它应始终与 sdd-tools 装在同一个市场里。装完**完全重启** CodeBuddy，用 `/plugin list` 确认都在 `agent-alchemy-local` 市场里。

## 使用

无任何命令。两种用法：让模型自己加载（`description` 含中英双语触发词，问"给队友派活的消息格式是什么"这类问题会命中），或在 skill / agent 正文里显式读取 —— 后者是主要用法：

```
Read ${CODEBUDDY_PLUGIN_ROOT}/skills/claude-code-tasks/SKILL.md
Read ${CODEBUDDY_PLUGIN_ROOT}/skills/claude-code-teams/SKILL.md
```

| Reference | 内容 |
|---|---|
| `claude-code-tasks/references/task-patterns.md` | 任务写法与状态流转范例 |
| `claude-code-tasks/references/anti-patterns.md` | 任务层反模式 |
| `claude-code-teams/references/messaging-protocol.md` | `SendMessage` 消息类型与投递机制 |
| `claude-code-teams/references/orchestration-patterns.md` | 6 种编排模式 |
| `claude-code-teams/references/hooks-integration.md` | `TeammateIdle` / `TaskCompleted` 等 hook |

## 校准与上游同步

```bash
bash plugins/claude-tools-codebuddy/versions/v0.2.5-cb.1/verify.sh
```

校验：本版 `plugin/` 包指纹、`source.zip` 解包后与本体一致、上游镜像基线未被改动。

**改产物的正确姿势**：不要原地改已冻结的 `versions/*/plugin/`；新建 `versions/v0.2.5-cb.2/`，放入改动后的 `plugin/`，按模板补 `README.md`、`PROVENANCE.md`、`source.zip`、`verify.sh`。

**上游更新时**：重下上游 → `diff -rq` 定位变更 → 按 [`docs/CONVERSION.md`](docs/CONVERSION.md) 逐类重放改动 → 版本号改为 `<新上游版本>-cb.1`。

## 注意事项

- **不改上游镜像** —— `../../external-skills/agent-alchemy-marketplace/` 是只读基线。
- **skill 名保留 `claude-code-*`** —— 上游命名，且被 sdd-tools 的 27 处路径引用；改名会波及跨插件引用而收益为零。
- **环境变量名按上游原样保留** —— 正文里 `CLAUDE_CODE_TEAM_NAME`、`CLAUDE_TEAMMATE_ID` 等是**平台注入**的变量，本产物不擅自改名（改名可能变成对不存在变量的引用）；两处「移植说明」段已写明"以本机实际环境为准"。
- **上游 `last-verified` 字段未保留** —— CodeBuddy skill frontmatter 无此字段，日期改记在 `PROVENANCE.md` 第二节。
