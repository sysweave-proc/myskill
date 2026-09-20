# agent-alchemy-core-tools（CodeBuddy 版）

把上游 [`sequenzia/agent-alchemy`](https://github.com/sequenzia/agent-alchemy) 的 `core-tools` 插件移植到 CodeBuddy。

| 项 | 内容 |
|---|---|
| 上游 | `agent-alchemy-core-tools` v0.2.3 ｜ commit `fc1a336b`（2026-05-31）｜ MIT |
| 上游原样镜像 | [`../../external-skills/agent-alchemy-marketplace/core-tools/`](../../external-skills/agent-alchemy-marketplace/core-tools/)（只读，零改写） |
| 插件名 | `agent-alchemy-core-tools`（沿用上游，保持跨插件引用一致） |

**按版本聚合**：一版一个目录；`plugin/` 与 `source.zip` 是同一份内容的两种形态。

## 版本谱系

| 版本 | 主题 | 状态 |
|---|---|---|
| [`v0.2.3-cb.1`](versions/v0.2.3-cb.1/) | 首次移植为 CodeBuddy 插件（skill + agent + command + hook） | 首版冻结基准 |
| [`v0.2.3-cb.2`](versions/v0.2.3-cb.2/) | 补齐中文触发词（3 个知识库 skill + 4 个 agent 的 `description`） | **当前基准** |

`-cb.N` 只在**上游版本不变、本产物需修订**时递增；上游版本变化时改为 `<新上游版本>-cb.1`。
旧版本目录**不再原地修改** —— 校准靠的是"基准不变"，改动一律进新版本目录。

## 目录结构

```
plugins/core-tools-codebuddy/
├── README.md                本文件
├── docs/CONVERSION.md       上游→CodeBuddy 转换规则 + 上游同步清单
└── versions/v0.2.3-cb.N/
    ├── README.md            本版说明：主题、包内构成、改动概览
    ├── PROVENANCE.md        逐文件 md5、与上游对照、包指纹
    ├── source.zip           plugin/ 的权威打包存档
    ├── verify.sh            一键校准
    └── plugin/              **交付产物**（安装这个目录）
```

## 安装

```bash
bash plugins/core-tools-codebuddy/install.sh              # 幂等；自动取 versions/ 下最新版
bash plugins/core-tools-codebuddy/install.sh --uninstall
```

脚本做的事：校准基准 → 备份配置 → 放入本地市场 `agent-alchemy-local` → **按 `plugins/` 重建市场清单** → 注册 → 启用 → 校验。**五个 agent-alchemy 包共用同一份脚本**（字节一致），因此多插件共存互不覆盖。

只要 skill、不要 agent 与 hook 的退化装法：

```bash
cp -r core-tools-codebuddy/versions/v0.2.3-cb.2/plugin/skills/* ~/.codebuddy/skills/
```

> 本机 `~/.codebuddy/skills/` 若已有上游同名旧副本 `codebase-analysis`，先移走再拷。这种方式下 `deep-analysis` 会因缺子代理而无法组队。

`hooks/auto-approve-da-session.sh` 依赖 `jq`；缺失时静默失效（等于"无意见"），退化为正常审批流，**不会阻断执行**：`sudo dnf install -y jq`

## 使用

**入口就是三条命令**，装好即用，没有"启动"动作：`/deep-analysis`、`/codebase-analysis`、`/interview-me`。也可以直接说人话 —— `description` 里的中文触发词会让模型自动加载对应 skill。

完整使用手册（30 秒上手、每条命令的交互过程、可选的 `.codebuddy/agent-alchemy.local.md` 配置、运行时产物目录、排错表）随插件交付：[`versions/v0.2.3-cb.2/plugin/README.md`](versions/v0.2.3-cb.2/plugin/README.md)。

## 校准与上游同步

```bash
bash plugins/core-tools-codebuddy/versions/v0.2.3-cb.2/verify.sh
```

校验四件事：本版 `plugin/` 包指纹、`source.zip` 解包后与本体一致、**上一版基准未被改动**、上游镜像基线未变。

**改产物的正确姿势**：不要原地改已冻结的 `versions/*/plugin/`（那会让基准失效）。新建 `versions/v0.2.3-cb.3/`，放入改动后的 `plugin/`，按模板补 `README.md`、`PROVENANCE.md`、`source.zip`、`verify.sh`，且新版 `verify.sh` 要像 cb.2 那样核对上一版基准。

**上游更新时**：重下上游 → `diff -rq` 定位变更 → 按 [`docs/CONVERSION.md`](docs/CONVERSION.md) 的映射表逐类重放改动 → 版本号改为 `<新上游版本>-cb.1`。

## 注意事项

- **不改上游镜像** —— `../../external-skills/agent-alchemy-marketplace/` 是只读基线；本产物是独立目录，便于 `diff` 与校准。
- **`${CODEBUDDY_PLUGIN_ROOT}` 兜底** —— 若运行时不展开该变量，`skills/` 与 `agents/` 内已写明用 Glob 定位或按相对路径读取。
- 可选依赖 Context7 MCP，仅 `interview-me` 的主动研究使用，缺失时退回 Web 搜索。
