# agent-alchemy-tdd-tools（CodeBuddy 版）

把上游 [`sequenzia/agent-alchemy`](https://github.com/sequenzia/agent-alchemy) 的 `tdd-tools` 插件移植到 CodeBuddy。

| 项 | 内容 |
|---|---|
| 上游 | `agent-alchemy-tdd-tools` v0.2.1 ｜ commit `fc1a336b`（2026-05-31）｜ MIT（版权归 Stephen Sequenzia） |
| 上游原样镜像 | [`../../external-skills/agent-alchemy-marketplace/tdd-tools/`](../../external-skills/agent-alchemy-marketplace/tdd-tools/)（只读，零改写） |
| 插件名 | `agent-alchemy-tdd-tools`（沿用上游，保持跨插件引用一致） |
| 同市场依赖 | `agent-alchemy-core-tools`（`language-patterns` / `project-conventions`）、`agent-alchemy-sdd-tools`（`task-executor` agent、`/create-tasks`） |

**按版本聚合**：一版一个目录；`plugin/` 与 `source.zip` 是同一份内容的两种形态。

## 版本谱系

| 版本 | 主题 | 状态 |
|---|---|---|
| [`v0.2.1-cb.1`](versions/v0.2.1-cb.1/) | 首次移植为 CodeBuddy 插件（5 command / 5 skill / 3 agent + PreToolUse hook） | **冻结基准** |

`-cb.N` 只在**上游版本不变、本产物需修订**时递增；上游版本变化时改为 `<新上游版本>-cb.1`。
旧版本目录**不再原地修改** —— 校准靠的是"基准不变"，改动一律进新版本目录。

## 目录结构

```
plugins/tdd-tools-codebuddy/
├── README.md                本文件
├── docs/CONVERSION.md       本插件的转换规则 + 上游同步清单
└── versions/v0.2.1-cb.1/
    ├── README.md            本版说明：主题、包内构成、改动概览
    ├── PROVENANCE.md        逐文件 md5、与上游对照、包指纹
    ├── source.zip           plugin/ 的权威打包存档
    ├── verify.sh            一键校准
    └── plugin/              **交付产物**（安装这个目录）
```

## 安装

```bash
bash plugins/tdd-tools-codebuddy/install.sh      # 幂等；自动取 versions/ 下最新版
bash plugins/core-tools-codebuddy/install.sh     # 同市场依赖
bash plugins/sdd-tools-codebuddy/install.sh      # 同市场依赖（/create-tasks、task-executor）
```

装完**完全重启** CodeBuddy，用 `/plugin list` 确认三个插件都在 `agent-alchemy-local` 市场里。安装脚本的具体行为见根 [`README.md`](../README.md)。

`hooks/auto-approve-session.sh` 依赖 `jq`；缺失时静默失效（等于"无意见"），退化为正常审批流，**不会阻断执行**：`sudo dnf install -y jq`

## 使用

| 入口 | 作用 |
|---|---|
| `/tdd-cycle <功能描述｜任务ID｜规格章节>` | 完整 RED-GREEN-REFACTOR（先给计划确认，再自主跑） |
| `/generate-tests <spec｜task-id｜file>` | 从验收标准或源码生成测试（自动识别 pytest / Jest / Vitest，并行派 `test-writer`） |
| `/analyze-coverage [项目路径] [--spec <path>] [--threshold <n>]` | 覆盖率缺口分析 + 可执行补测建议 |
| `/create-tdd-tasks [--task-group <group>]` | 把 SDD 任务转成「前置测试任务 + 实现任务」的 TDD 对 |
| `/execute-tdd-tasks [--task-group <g>] [--max-parallel <n>] [--retries <n>]` | 拓扑分波自主执行；TDD 对派 `tdd-executor`，非 TDD 派 sdd-tools 的 `task-executor` |

5 个 skill 的 `description` 均含中英双语触发词，相关语境下模型会自动加载。

完整使用手册（含运行时产物目录 `~/.codebuddy/sessions/` 与 `~/.codebuddy/tasks/` 的说明）随插件交付：[`versions/v0.2.1-cb.1/plugin/README.md`](versions/v0.2.1-cb.1/plugin/README.md)。

## 校准与上游同步

```bash
bash plugins/tdd-tools-codebuddy/versions/v0.2.1-cb.1/verify.sh
```

校验：本版 `plugin/` 包指纹、`source.zip` 解包后与本体一致、上游镜像基线未被改动。

**改产物的正确姿势**：不要原地改已冻结的 `versions/*/plugin/`（那会让基准失效）。新建 `versions/v0.2.1-cb.2/`，放入改动后的 `plugin/`，按模板补 `README.md`、`PROVENANCE.md`、`source.zip`、`verify.sh`。

**上游更新时**：重下上游 → `diff -rq` 定位变更 → 按 [`docs/CONVERSION.md`](docs/CONVERSION.md) 逐类重放改动 → 版本号改为 `<新上游版本>-cb.1`。

## 注意事项

- **不改上游镜像** —— `../../external-skills/agent-alchemy-marketplace/` 是只读基线。
- **跨插件引用改名** —— `../core-tools` → `../agent-alchemy-core-tools`；`../sdd-tools` → `../agent-alchemy-sdd-tools`。
- **建链 hook 未移植** —— `resolve-cross-plugins.sh` 是 Claude Code 缓存布局专用；CodeBuddy 平铺市场不需要。
- **`TASK_LIST_ID`** —— 上游用 `CLAUDE_CODE_TASK_LIST_ID`，本产物改为 `TASK_LIST_ID`，并在首次出现处说明「运行时未暴露该标识时，用任务列表名或 `default`」。
- **`${CODEBUDDY_PLUGIN_ROOT}` 兜底** —— 若运行时不展开该变量，各 skill / agent 正文已写明用 Glob 按名字定位。
