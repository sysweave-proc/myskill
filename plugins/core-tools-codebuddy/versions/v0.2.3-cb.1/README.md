# v0.2.3-cb.1 — core-tools 的 CodeBuddy 移植（首版 / 校准基准）

| 项 | 值 |
|---|---|
| 版本 | `0.2.3-cb.1` |
| 上游 | `agent-alchemy-core-tools` **0.2.3**，commit `fc1a336b`（2026-05-31） |
| 基线日期 | 2026-09-19 |
| 包指纹 | `2a25c41b8b418c0e1b1967053412d66e` |
| 上一版 | **无**（本仓首个 CodeBuddy 移植版） |
| 状态 | **冻结基准** —— 用于日后校准，不再原地修改 |

## 一、本版主题

把 agent-alchemy 的 `core-tools` 从 Claude Code 插件形态移植为 **CodeBuddy 可加载的插件**，
目标是**功能完整继承**（不是简化重写）：代码库分析、多智能体深度探索、交互式访谈、语言模式、技术图表全部可用。

**关键结论：协调层无需降级。** 实测 CodeBuddy 生态存在完整团队原语
（`TeamCreate` / `TeamDelete` / `TaskCreate` / `TaskUpdate` / `TaskList` / `TaskGet` / `SendMessage` / `AskUserQuestion`），
因此 `deep-analysis` 的 6 阶段流程、hub-and-spoke 拓扑、任务依赖与状态守卫、断点续传、缓存 TTL、
错误降级矩阵、分级审批**原样保留**。证据与逐项映射见 [`../../docs/CONVERSION.md`](../../docs/CONVERSION.md)。

## 二、包内构成

```
v0.2.3-cb.1/
├── README.md          ← 本文件
├── PROVENANCE.md      ← 逐文件 md5 + 与上游对照 + 包指纹（权威记录）
├── source.zip         ← plugin/ 的权威打包存档
├── verify.sh          ← 一键校准：本体 / 存档 / 上游基线 / 改造幅度
└── plugin/            ← 交付产物（CodeBuddy 插件本体，可直接安装）
    ├── .codebuddy-plugin/plugin.json
    ├── README.md      ← **使用手册**（随插件一起安装）
    ├── commands/      ← 3 个斜杠命令（/deep-analysis、/codebase-analysis、/interview-me）
    ├── skills/        ← 6 个 skill（deep-analysis、codebase-analysis、interview-me、language-patterns、project-conventions、technical-diagrams）
    ├── agents/        ← 4 个 agent（code-explorer、code-synthesizer、code-architect、interview-researcher）
    └── hooks/         ← PreToolUse 自动放行（会话/缓存目录）
```

## 三、相对上游的改动概览

| 类别 | 改动 |
|---|---|
| 路径与目录 | `${CLAUDE_PLUGIN_ROOT}` → `${CODEBUDDY_PLUGIN_ROOT}`；`.claude/` → `.codebuddy/`；`CLAUDE.md` → `CODEBUDDY.md` |
| 清单 | `.claude-plugin/` → `.codebuddy-plugin/` |
| skill frontmatter | 删 `user-invocable` / `disable-model-invocation` / `argument-hint`（CodeBuddy 不识别），补 `version` |
| agent frontmatter | 补 `color`；`description` 改写为 CodeBuddy 触发规范；`skills:` 预加载字段改为正文显式 `Read` |
| 斜杠入口 | 上游靠 `user-invocable` skill，CodeBuddy 靠 `commands/` → 新增 3 个命令 |
| 可选依赖 | Context7 MCP 工具名不再写死，改为可选 + `WebSearch`/`WebFetch` 兜底 |

**改动幅度（实测）**：12 个文件逐字节一致 ｜ 14 个改写 ｜ 4 个新增 ｜ **0 未移植**（上游 26 文件全部有对应，含上游 `README.md` → 本产物的使用手册）。

## 四、校准

```bash
bash verify.sh
```

校验项：① `plugin/` 本体指纹未被改动；② `source.zip` 解包后与本体一致；③ 上游基线指纹仍为 `808192241ec2c53ced9bd83227279279`，且改造幅度仍为 12 / 14 / 4。

**不要原地改 `plugin/`** —— 一律新建版本目录（如 `v0.2.3-cb.2`），旧版保持冻结。
本版在首次冻结前曾就地修订过 2 次（修两处保真缺陷：agent 引用误用带插件前缀的写法、派队友未显式传 `name`；以及补使用手册），完整缺陷表与**残留不确定点**见 [`PROVENANCE.md`](PROVENANCE.md) 第七节，转换规则已沉淀到 [`../../docs/CONVERSION.md`](../../docs/CONVERSION.md)。

## 五、已知注意事项

1. **hook 依赖 `jq`**。未安装时脚本静默 `exit 0`（无意见），退化为 CodeBuddy 正常审批流，不会阻断执行。
2. **Context7 MCP 可选**，仅 `interview-me` 的主动研究使用；缺失时自动退回 Web/搜索。
3. **`${CODEBUDDY_PLUGIN_ROOT}` 兜底**：若运行时不展开该变量，`skills/` 与 `agents/` 内已写明用 Glob 定位或按 skill 本地 `references/` 相对路径读取。
