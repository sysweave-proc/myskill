# agent-alchemy-sdd-tools（CodeBuddy 版）

把上游 [`sequenzia/agent-alchemy`](https://github.com/sequenzia/agent-alchemy) 的 `sdd-tools` 插件移植到 CodeBuddy。

| 项 | 内容 |
|---|---|
| 上游 | `agent-alchemy-sdd-tools` v0.2.11 ｜ commit `fc1a336b`（2026-05-31）｜ MIT（版权归 Stephen Sequenzia） |
| 上游原样镜像 | [`../../external-skills/agent-alchemy-marketplace/sdd-tools/`](../../external-skills/agent-alchemy-marketplace/sdd-tools/)（只读，零改写） |
| 插件名 | `agent-alchemy-sdd-tools`（沿用上游，保持跨插件引用一致） |
| 同市场依赖 | **`agent-alchemy-claude-tools`（硬依赖，27 处引用）**、`agent-alchemy-core-tools`（Mermaid 图表 1 处） |

**按版本聚合**：一版一个目录；`plugin/` 与 `source.zip` 是同一份内容的两种形态。

## 版本谱系

| 版本 | 主题 | 状态 |
|---|---|---|
| [`v0.2.11-cb.1`](versions/v0.2.11-cb.1/) | 首次移植为 CodeBuddy 插件（5 command / 5 skill / 7 agent / 3 hook 事件） | **冻结基准** |

`-cb.N` 只在**上游版本不变、本产物需修订**时递增；上游版本变化时改为 `<新上游版本>-cb.1`。
旧版本目录**不再原地修改** —— 校准靠的是"基准不变"，改动一律进新版本目录。

## 目录结构

```
plugins/sdd-tools-codebuddy/
├── README.md                本文件
├── docs/CONVERSION.md       本插件的转换规则 + 上游同步清单
└── versions/v0.2.11-cb.1/
    ├── README.md            本版说明：主题、包内构成、改动概览
    ├── PROVENANCE.md        逐文件 md5、与上游对照、包指纹
    ├── source.zip           plugin/ 的权威打包存档
    ├── verify.sh            一键校准
    └── plugin/              **交付产物**（含上游架构深度分析 `DEEP-DIVE.md`）
```

## 安装

```bash
bash plugins/claude-tools-codebuddy/install.sh   # 硬依赖（任务/团队原语手册）
bash plugins/core-tools-codebuddy/install.sh     # 可选（Mermaid 图表规范）
bash plugins/sdd-tools-codebuddy/install.sh      # 本插件
```

**依赖必须同市场**：`run-tasks` 的团队 / 消息语义来自 `agent-alchemy-claude-tools`，`create-spec` 画图用 `agent-alchemy-core-tools` 的 `technical-diagrams`。装完**完全重启** CodeBuddy，用 `/plugin list` 确认都在 `agent-alchemy-local` 市场里。

hook 依赖：

| Hook | 依赖 |
|---|---|
| `auto-approve-session.sh`（PreToolUse） | `jq`；缺失时静默 `exit 0`（无意见），退化为正常审批流，**不阻断执行** |
| `verify-task-completion.sh`（TaskCompleted） | `jq`；按仓库类型跑 `pnpm test` / `npm test` / `python -m pytest` |
| `TeammateIdle`（prompt 型） | 无外部依赖 |

`sudo dnf install -y jq`（或 `apt-get install -y jq`）

## 使用

| 入口 | 作用 |
|---|---|
| `/create-spec [context]` | 自适应访谈生成规格 → `specs/SPEC-{name}.md` |
| `/analyze-spec [spec-path]` | 规格体检 → md + HTML 双报告 → 可选建修复任务 |
| `/create-tasks [spec] [--phase <phases>]` | 拆解为带依赖/验收标准/`task_group` 的任务；重跑走 `task_uid` 合并 |
| `/execute-tasks [task-id] [--task-group] [--retries] [--max-parallel]` | 单编排器波次执行（默认入口） |
| `/run-tasks [...] [--phase N,M] [--dry-run]` | Agent Teams 波次执行（wave-lead 组队 + context-manager 传知识） |

5 个 skill 的 `description` 均含中英双语触发词，相关语境下模型会自动加载。

完整使用手册（含运行时产物目录、`.codebuddy/agent-alchemy.local.md` 的 `run-tasks.*` 七个配置键及其优先级）随插件交付：[`versions/v0.2.11-cb.1/plugin/README.md`](versions/v0.2.11-cb.1/plugin/README.md)。

## 校准与上游同步

```bash
bash plugins/sdd-tools-codebuddy/versions/v0.2.11-cb.1/verify.sh
```

校验：本版 `plugin/` 包指纹、`source.zip` 解包后与本体一致、上游镜像基线未被改动。

**改产物的正确姿势**：不要原地改已冻结的 `versions/*/plugin/`（那会让基准失效）。新建 `versions/v0.2.11-cb.2/`，放入改动后的 `plugin/`，按模板补 `README.md`、`PROVENANCE.md`、`source.zip`、`verify.sh`。

**上游更新时**：重下上游 → `diff -rq` 定位变更 → 按 [`docs/CONVERSION.md`](docs/CONVERSION.md) 逐类重放改动 → 版本号改为 `<新上游版本>-cb.1`。

## 注意事项

- **不改上游镜像** —— `../../external-skills/agent-alchemy-marketplace/` 是只读基线。
- **跨插件引用改名** —— `../claude-tools` → `../agent-alchemy-claude-tools`；`../core-tools` → `../agent-alchemy-core-tools`。
- **建链 hook 未移植** —— `resolve-cross-plugins.sh` 是 Claude Code 缓存布局专用；CodeBuddy 平铺市场不需要。
- **`TASK_LIST_ID`** —— 上游用 `CLAUDE_CODE_TASK_LIST_ID`；本产物改名，并补「运行时未暴露时用任务列表名或 `default`」的兜底说明。
- **多补了一条 `/run-tasks` 命令** —— 上游 `run-tasks` skill 漏标 `user-invocable: true`，但其 README 与 `analyze-spec` 都以命令形式使用它；视为上游疏漏，本产物补上入口。
- **`${CODEBUDDY_PLUGIN_ROOT}` 兜底** —— 若运行时不展开该变量，各 skill / agent 正文已写明用 Glob 按名字定位。
