# v0.3

**主题**：外部知识源自学 ｜ **规模**：21 文件 / 4,345 行 ｜ `SKILL.md` 的 `version: 0.3.0`

## 本版变化

方向从「怎么画图」转到「**Agent 怎么自我进化、从哪里学**」，新增 `knowledge-sources/` 外部资源注册表：

- `knowledge-sources/index.yaml`——30 条外部资源（UML、C4、SEI、arc42、渲染器文档、成熟项目示例…），每条带 `authority` / `teaches` / `query_when` / `do_not_use_when` / `direct_fact_scope` / `extract_to_rules`
- `knowledge-sources/resource-advisor.md`——选源决策树
- `knowledge-sources/selection-matrix.md`——选择矩阵
- `knowledge-sources/README.md`

关键原则：外部来源只教「方法与工具语义」，**不能推翻目标仓库的源码事实**。

## 目录

| 路径 | 内容 |
|---|---|
| `package/` | 技能包文件树（21 个文件，可直接阅读） |
| `source.zip` | 原始 zip（权威字节，勿改） |
| `conversation/` | 对话材料：`conversation.md` 逐轮全文 · `raw-data.json` 页面内嵌数据 · `snapshot.html` 页面快照 |

## 备注

- frontmatter 仍用 `description: >-`，仍过不了官方校验器。
- 本版对话中有 **39 条**工具回显被 ChatGPT 抹掉（`redacted`），其中包含联网检索的返回。
