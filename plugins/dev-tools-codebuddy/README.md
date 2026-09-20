# agent-alchemy-dev-tools（CodeBuddy 版）

把上游 [`sequenzia/agent-alchemy`](https://github.com/sequenzia/agent-alchemy) 的 `dev-tools` 插件移植到 CodeBuddy。

| 项 | 内容 |
|---|---|
| 上游 | `agent-alchemy-dev-tools` v0.3.4 ｜ commit `fc1a336b`（2026-05-31）｜ MIT（版权归 Stephen Sequenzia） |
| 上游原样镜像 | [`../../external-skills/agent-alchemy-marketplace/dev-tools/`](../../external-skills/agent-alchemy-marketplace/dev-tools/)（只读，零改写） |
| 插件名 | `agent-alchemy-dev-tools`（沿用上游，保持跨插件引用一致） |
| 同市场依赖 | `agent-alchemy-core-tools`（复用其 `code-architect` / `code-explorer` / `deep-analysis` / `language-patterns` / `technical-diagrams`） |

**按版本聚合**：一版一个目录；`plugin/` 与 `source.zip` 是同一份内容的两种形态。

## 版本谱系

| 版本 | 主题 | 状态 |
|---|---|---|
| [`v0.3.4-cb.1`](versions/v0.3.4-cb.1/) | 首次移植为 CodeBuddy 插件（5 command / 9 skill / 4 agent） | **冻结基准** |

`-cb.N` 只在**上游版本不变、本产物需修订**时递增；上游版本变化时改为 `<新上游版本>-cb.1`。
旧版本目录**不再原地修改** —— 校准靠的是"基准不变"，改动一律进新版本目录。

## 目录结构

```
plugins/dev-tools-codebuddy/
├── README.md                本文件
├── docs/CONVERSION.md       本插件的转换规则 + 上游同步清单
└── versions/v0.3.4-cb.1/
    ├── README.md            本版说明：主题、包内构成、改动概览
    ├── PROVENANCE.md        逐文件 md5、与上游对照、包指纹
    ├── source.zip           plugin/ 的权威打包存档
    ├── verify.sh            一键校准
    └── plugin/              **交付产物**（安装这个目录）
```

## 安装

```bash
bash plugins/dev-tools-codebuddy/install.sh      # 幂等；自动取 versions/ 下最新版
bash plugins/core-tools-codebuddy/install.sh     # 同市场依赖
```

装完**完全重启** CodeBuddy，用 `/plugin list` 确认两个插件都在 `agent-alchemy-local` 市场里。安装脚本的具体行为见根 [`README.md`](../README.md)。

## 使用

| 入口 | 作用 |
|---|---|
| `/feature-dev <功能描述>` | 7 阶段功能开发：理解 → 探索 → 提问 → 架构（2-3 套方案）→ 实现 → 评审 → 总结 |
| `/bug-killer <bug 或报错> [--deep]` | 5 阶段假设驱动排查：复现 → 取证 → 根因 → 修复验证 → 复盘 |
| `/docs-manager <动作或描述>` | 文档管理：MkDocs / 独立 markdown；生成 / 更新 / 变更摘要 |
| `/document-changes [范围]` | 生成当前会话的 markdown 变更报告 |
| `/release-python-package [版本]` | Python 包发布（uv + ruff），9 步 fail-fast |

9 个 skill 的 `description` **全部含中英双语触发词**，相关语境下模型会自动加载；其余 4 个（`architecture-patterns`、`code-quality`、`project-learnings`、`changelog-format`）是"被加载型"知识库，由上述流程在对应阶段引用。

完整使用手册随插件交付：[`versions/v0.3.4-cb.1/plugin/README.md`](versions/v0.3.4-cb.1/plugin/README.md)。

## 校准与上游同步

```bash
bash plugins/dev-tools-codebuddy/versions/v0.3.4-cb.1/verify.sh
```

校验：本版 `plugin/` 包指纹、`source.zip` 解包后与本体一致、上游镜像基线未被改动。

**改产物的正确姿势**：不要原地改已冻结的 `versions/*/plugin/`（那会让基准失效）。新建 `versions/v0.3.4-cb.2/`，放入改动后的 `plugin/`，按模板补 `README.md`、`PROVENANCE.md`、`source.zip`、`verify.sh`。

**上游更新时**：重下上游 → `diff -rq` 定位变更 → 按 [`docs/CONVERSION.md`](docs/CONVERSION.md) 逐类重放改动 → 版本号改为 `<新上游版本>-cb.1`。

## 注意事项

- **不改上游镜像** —— `../../external-skills/agent-alchemy-marketplace/` 是只读基线。
- **跨插件引用改名** —— 上游写 `../core-tools`，本产物写 `../agent-alchemy-core-tools`（CodeBuddy 市场里目录名带组织前缀）。
- **hooks 未移植** —— 上游的 `resolve-cross-plugins.sh` 是 Claude Code 缓存布局专用的建链机制，CodeBuddy 平铺市场不需要。
- **`${CODEBUDDY_PLUGIN_ROOT}` 兜底** —— 若运行时不展开该变量，各 skill / agent 正文已写明用 Glob 按名字定位。
