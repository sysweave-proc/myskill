# v0.2

**主题**：图表表达（传统画法 vs Mermaid） ｜ **规模**：17 文件 / 3,022 行 ｜ `SKILL.md` 的 `version: 0.2.0`

## 本版变化

在六阶段之后补上「该用哪种图画法」：历史上结构关联图的谱系、各自何时适用，以及**让 Agent 自己判断该用传统画法还是 Mermaid** 的规则。

相对 v0.1：**+2 新增、3 覆写**（`SKILL.md`、`references/representation/representation-policy.md`、`README.md`）

- 新增 `references/diagrams/diagram-catalog.md`——选择总表 / 决策树 / 「传统 vs Mermaid vs 不画」的判定条件
- 新增 `examples/diagram-selection-examples.yaml`

## 目录

| 路径 | 内容 |
|---|---|
| `package/` | 技能包文件树（17 个文件，可直接阅读） |
| `source.zip` | 原始 zip（权威字节，勿改） |
| `conversation/` | 对话材料：`conversation.md` 逐轮全文 · `raw-data.json` 页面内嵌数据 · `snapshot.html` 页面快照 |

## 备注

- frontmatter 仍用 `description: >-`，仍过不了官方校验器。
- 本版对话中有 **17 条**工具回显被 ChatGPT 抹掉（`redacted`）。
