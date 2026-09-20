# v0.6.0 中文版翻译说明

本版本是在 `source-code-reading-skill-v0.6.0-merged.zip` 基础上的完整中文化版本。

## 翻译原则

1. 所有面向读者的英文自然语言均翻译为中文，并尽量保持原有规范强度、条件关系和因果关系。
2. `System`、`Subsystem`、`Path`、`Claim`、`Evidence`、`Source Anchor`、`Pattern`、`Renderer`、`Ownership`、`Lifecycle`、`Validation` 等在 Skill 中承担规范语义或机器可识别作用的术语保留英文，并在首次出现处用中文解释。
3. YAML key、程序变量、测试标识、文件路径、命令、代码、Mermaid/Graphviz 语法、源码符号和 URL 不翻译，以保证 Skill 的机器可执行性和源码导航能力不被破坏。
4. 图中的 `Start`、`Lookup`、`Use`、`Allocate` 等代码/图表标签保持原样，因为它们属于示例中的语法元素，而非正文。
5. 不改变原有目录结构、文件名、规范 ID、关系名和测试接口；本次仅进行语义等价的语言转换。

## 完整性目标

中文版本必须继续满足：

```text
原有文件资产不丢失
原有机器接口不改变
核心知识模型不改变
规范强度不降低
演进/回归机制不改变
```

## 交付后修订记录

本中文包在交付后做过「可用性修复」「受控标识统一」「触发面重写」「术语表与撞号消歧」「去除跨 skill 引用」，逐条留痕，不静默改动：

| # | 位置 | 原状 | 修正 | 原因 |
|---|---|---|---|---|
| 1 | `SKILL.md` frontmatter | `version: 0.6.0` 为顶层键；`description: >-` | `version` 移入 `metadata.version`；`description` 改为 `\|-` | 官方校验器 `quick_validate.py` 的允许键为 `{name, description, license, allowed-tools, metadata}`，顶层 `version` 会直接判非法并退出，Skill 无法通过校验；`>-` 是 v0.6.0 已修过的折叠标量回归，恢复为 `\|-` |
| 2 | `SKILL.md` §10 第 5、17 条 | 仍为英文正文 | 译为中文 | 与「翻译原则 1」不一致的漏译 |
| 3 | `references/knowledge-model.md` §7 第 3–6 条 | 仍为英文正文 | 译为中文，并与 `SKILL.md` §10 同位条目用词对齐 | 同一规则在两处出现，漏译 + 措辞不一致 |
| 4 | 包内 `tests/__pycache__/` | 携带 `*.pyc` 二进制 | 已删除 | 非源码产物，不应随包分发 |
| 5 | `templates/source-reading-note.md` 篇头 | 标签为 `**Core Question**` | 改为 `**核心问题**` | 模板会被逐字带进成品笔记，英文标签会外泄到交付文档 |
| 6 | `evolution/evolution-policy.md` 的 yaml 代码块 | 顶层键 `removal:` 被译为 `移除:` | 改回 `removal:` | 该块是「删除记录」的 schema 样例，同块内的子键（`path`/`capability`/`reason`/…）以及 `templates/evolution-change.yaml` 的 `removal` 都保留英文；只译父键会自相矛盾，且与规范正文（`SKILL.md` §13.2 步骤 5 用英文键名）脱节 |
| 7 | `references/tracing/trace-policy.md`、`references/validation/validation-policy.md`、`references/execution-progressive.md`、`references/tracing/exploration-policy.md` | **受控标识双轨**：这些文件把标识译成了纯中文（`D1 局部`、`V1 结构`、`L0：定位`、`L0 目标符号`） | 统一为「英文标识 + 中文释义」：`D1 Local（局部事实）`、`V1 Structural（结构）`、`L0 Orientation（定位）`、`L0 Target symbol（目标符号）` | `SKILL.md` 与快速入口页 `references/traceability.md`、`references/validation.md` 都保留英文标识；同一标识在同一包内出现两种写法时，读者与 Agent 都无法确定 `V4 表达` 与 `V4 Representation` 是否同一物——这正是「术语未锚定」的直接来源 |
| 8 | `SKILL.md` frontmatter（`description` / `metadata`） | 描述只陈述方法论，**没有一句说明「用户说什么话时该用本技能」**，也没有边界声明 | 重写为三段式：①是什么 ②`This skill should be used when the user asks to …`（中英触发词）③边界声明（按交付物类型划界）；并补 `metadata.scope / canonical`。同时把 `merge` / `rewrite` 术语**锚回 §13 正文**——原文这两个词只出现在描述里，一改描述就会使包内能力测试的必需标记失守 | 依据 `skill-creator` 指南：`name` + `description` 决定 CodeBuddy 何时使用该 skill，须说明「做什么」与「何时用」，并使用第三人称。描述是触发层唯一可见文本 |
| 9 | 新增 `references/glossary.md`；`SKILL.md` §0 增加指针 | 全包没有术语表：`Concern`、`Path`、`Mechanism` 等受控术语无定义、可多义使用 | 新增术语表，逐条给出「英文原名 / 中文正名 / 定义 / 权威位置」，并单列 §10 消歧（`Concern` 的四种角色、三套 `L` 编号、`Path` vs `Flow` 等） | 一个概念只有一个正名，才能保证语义不歧义。此前有一版再表达件曾声称加过「中英术语对照表」，但 v0.6.0 里实际没有 |
| 10 | `references/tracing/exploration-policy.md` | 上下文扩展顺序梯子写作 `L0–L6`，与 `SKILL.md` §5 的深度等级 `L0–L3` 撞号（都从 `L0` 起） | 改为 `C0–C6`（Context）；`SKILL.md` §13.1 的演进四级 `L1–L4` 保持不变，改由术语表 §10.2 说明三者区别 | 撞号会让读者与 Agent 把「理解深度」与「跟踪向外扩多远」当成同一条梯子。只改收敛在一个文件内的那条（7 行），避免动到跨文件的演进编号与历史记录 `MERGE_DECISION.md` |
| 11 | 打包方式 | 交付物只有自定的 `source.zip` | 用官方 `skill-creator/scripts/package_skill.py` 产出 `source-code-reading.skill`（内部根目录 `source-code-reading/`），与 `source.zip` 并存；`tests/test_merged_capabilities.py` 的必需资产与标记新增 `references/glossary.md` | 官方打包器 = 校验 + 官方分发格式；包内自检清单需要覆盖新增资产 |
| 12 | `SKILL.md` frontmatter（`description` / `metadata`）——**撤回第 8 项的一半** | 第 8 项写的边界声明**点名了其它 skill**，并加了 `metadata.companion` | 删除对其它 skill 的具名引用；边界声明改为按**交付物类型**划界（不点名）；移除 `metadata.companion`（`metadata.scope` / `canonical` 保留，二者不涉及其它 skill） | Skill 必须**自包含**：在触发层点名别的 skill，会把「该找我」误导成「该找他」 |
| 13 | `README.md`、`MERGE_DECISION.md`、`MERGE_MANIFEST.yaml`，以及本文件的第 8、9 行 | 包内**出处记录**仍以专名引用另**一个** skill 包（v0.6.0 合并的两个输入之一） | 该专名中性化为「**再表达件**」；机器可读处用 `cognitive-reexpression` / `cognitive-reexpression-variant`。**只换专名，不动任何其他字**（逐行 diff 已验：`MERGE_DECISION.md` 仅 14 处专名、`README.md` 仅 3 处） | 任何指向别的 skill 的名字都可能把无关上下文拉进本次执行，污染判断。出处记录只需说明「有两个输入、各自强项是什么」，不需要点名外部包；改名后语义不变，v0.6.0 的合并事实仍然完整 |

修订后 `quick_validate.py` 对包根目录报 `Skill is valid!`。

**未处理（属流程问题，非可用性问题）**：`tests/test_skill_integrity.py` 以 v0.4 基线做 SHA-256 逐字节比对，中文版按定义无法通过（一切被翻译文件都算「未批准的基线内容变更」）。该测试服务于「合并发版」流程，不应作为中文变体的交付判据；若要保留该判据，需按 `evolution/approved-removals.yaml` 的格式补一份中文变体的 approved-changes 记录。
