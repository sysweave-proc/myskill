# v0.5

**主题**：执行闸门与瘦身 ｜ **规模**：12 文件 / 748 行 ｜ `SKILL.md` 的 `version: 0.5`

## 本版变化

**整包重写，而且是六个版本里唯一一次做减法**：文件 -66%、行数 -72%，把前四版的知识库压回 `SKILL.md` 正文，包内只留执行协议。

追问从「源码怎么读」变成了「**什么时候该停**」：

- **Stop/Continue Gates（Gate 0~6）**——Scope → Orient → Minimum Model → Pattern → Trace → Represent → Validate，只在出现具体缺口时扩张
- **渐进深度 L0~L3**——默认从 L1 起步，`references/stage-gates.md`
- **反过度设计规则**
- 包内 12 个文件：`SKILL.md`、`README.md`、`references/{architecture-foundation, execution-protocol, stage-gates, traceability}.md`、`references/patterns/catalog.md`、`references/representation/selection.md`、`examples/{buffer-manager-example.md, reading-sequence.md}`、`templates/{topic-note.md, architecture-topic-link.yaml}`

## 目录

| 路径 | 内容 |
|---|---|
| `skill/` | 技能包文件树（12 个文件，可直接阅读） |
| `source.zip` | 原始 zip（权威字节，勿改） |
| `conversation/` | 对话材料：`conversation.md` 逐轮全文 · `raw-data.json` 页面内嵌数据 · `snapshot.html` 页面快照 |

## ⚠️ 这是一次回归，不是演进

`knowledge-sources/`、`evolution/`、`cases/`、`references/diagrams/` **整体消失**，详细的 tracing / validation / document 策略文件也没了。部分概念被压缩重述进更短的 `SKILL.md`，但**规则资产本身丢了**。v0.5.1 就是来修这个的。

## 备注

- **frontmatter 是六个版本里唯一的异常**：`description` 字段被整个删掉、换成了 `summary`，校验器报 `Missing 'description' in frontmatter`。
- 本版对话中有 **53 条**工具回显被 ChatGPT 抹掉（`redacted`）。
