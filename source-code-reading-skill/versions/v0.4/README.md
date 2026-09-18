# v0.4

**主题**：架构图谱与进化 ｜ **规模**：35 文件 / 2,662 行 ｜ `SKILL.md` 的 `version: 0.4.0`

## 本版变化

**整包重写**（不是增量）。视角从「某个主题怎么读」抬到「**整个系统怎么被理解**」：

- **架构成为一等公民**：新增 `references/architecture-model.md`、`references/architecture-reconstruction.md`，引入 System Atlas（系统上下文 / 架构脊柱 / 关键场景路径 / 子系统图 / 横切关注点 / 架构↔源码映射 / 待解架构问题）
- **Path 升为一级知识对象**（不再只是「某主题的附带」）
- 新增 **进化引擎** `evolution/`（含 `anti-patterns/` 5 条反模式）与 `cases/`（gold / failures）
- `templates/` 增至 4 个（新增 `feedback.yaml`），`examples/` 增至 4 个

## 目录

| 路径 | 内容 |
|---|---|
| `package/` | 技能包文件树（35 个文件，可直接阅读） |
| `source.zip` | 原始 zip（权威字节，勿改） |
| `conversation/` | 对话材料：`conversation.md` 逐轮全文 · `raw-data.json` 页面内嵌数据 · `snapshot.html` 页面快照 |

## 本版已知缺陷（v0.5.1 才补回）

**丢了 `references/tracing/exploration-policy.md`**——v0.1/v0.2/v0.3 都有它，v0.4 重建包时忘带，其 `references/tracing/` 只剩 `trace-policy.md` 与 `claim-verification.md` 两个。`knowledge-sources/README.md` 也在同一波丢失。这是审计报告认定的「v0.3→v0.4 隐性回退」。

## 备注

- frontmatter 仍用 `description: >-`，仍过不了官方校验器。
- 本版对话中有 **50 条**工具回显被 ChatGPT 抹掉（`redacted`）。
- 原始 zip 内是**双层目录**（`source-code-reading-skill-v0.4/source-code-reading-skill/`），本目录的 `package/` 已展平到包根。
