# v0.2.3-cb.2 —— 补齐 core-tools 的中文触发词

> 状态：**当前基准** ｜ 上游：`agent-alchemy-core-tools` v0.2.3（commit `fc1a336b`，MIT） ｜ 包指纹：`e44a2692f51dc2cd3cc6828d5760bece`
> 上一版：[`../v0.2.3-cb.1/`](../v0.2.3-cb.1/)（**首版冻结基准，不再改动**，包指纹 `2a25c41b8b418c0e1b1967053412d66e`）

## 一、本版做了什么

`v0.2.3-cb.1` 只给 3 个**命令型** skill 的 description 追加了中文触发词，
**漏了另外 7 个**（3 个知识库 skill + 4 个 agent）。本版把它们补齐：

- `language-patterns` / `project-conventions` / `technical-diagrams`（3 个 skill）
- `code-architect` / `code-explorer` / `code-synthesizer` / `interview-researcher`（4 个 agent）

改完后，**core-tools 全部 6 个 skill + 4 个 agent 的 description 都含中英双语触发词** ——
中文语境下（"这个项目有什么约定？""帮我画个时序图""把这几份探索结果合并一下"）
不再依赖英文关键词才能命中。

**只动 `description`**：正文一字未改，agent 的中文触发行按折叠/块标量同样的缩进追加。

## 二、包内构成

```
v0.2.3-cb.2/
├── README.md          本文件
├── PROVENANCE.md      逐文件 md5、与 cb.1 及上游的对照、包指纹（权威记录）
├── source.zip         plugin/ 的权威打包存档
├── verify.sh          一键校准（本版 / 存档 / cb.1 基准 / 与 cb.1 的差异 / 上游）
└── plugin/            ← 交付产物
    ├── .codebuddy-plugin/plugin.json
    ├── README.md      使用手册（与 cb.1 相同）
    ├── commands/      3 个命令
    ├── skills/        6 个
    ├── agents/        4 个
    └── hooks/         1 个 PreToolUse hook
```

## 三、改动概览

| 文件 | 改动 |
|---|---|
| `skills/language-patterns/SKILL.md` | description 追加中文触发（语言习惯用法/最佳实践） |
| `skills/project-conventions/SKILL.md` | description 追加中文触发（项目约定/代码风格一致性） |
| `skills/technical-diagrams/SKILL.md` | description 追加中文触发（Mermaid/架构图/时序图/配色） |
| `agents/code-architect.md` | description 追加中文触发（实现方案/架构设计/方案对比/风险） |
| `agents/code-explorer.md` | description 追加中文触发（摸清模块/追执行路径/找相关文件） |
| `agents/code-synthesizer.md` | description 追加中文触发（合并结论/冲突仲裁/查漏补缺） |
| `agents/interview-researcher.md` | description 追加中文触发（查资料/现成做法/合规最佳实践） |
| `.codebuddy-plugin/plugin.json` | `version` 由 `0.2.3-cb.1` 升为 `0.2.3-cb.2`（否则市场清单会显示旧版本号） |

**与 cb.1 的差异**：逐字节一致 **22** ｜ 已改写 **8** ｜ 新增 **0**（合计 30）。
**与上游的关系**：不变（逐字节一致 12 ｜ 已改写 14 ｜ 新增 4 ｜ 未移植 0）。

## 四、校准

```bash
bash verify.sh
```

该校验会**同时确认 cb.1 基准未被改动**（`2a25c41b8b418c0e1b1967053412d66e`）——
这是"修订进新目录、旧版本冻结"这一约定的硬约束。
