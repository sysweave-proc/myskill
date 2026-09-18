# skill-ds

一版**源码阅读知识建模技能**：面向大型 C/C++ 系统（Linux / PostgreSQL / MySQL / LLVM 一类），
把"读源码 → 写笔记"重构成"**建一张可追溯的知识模型 → 再投影成文档**"。

## 它从哪来

读完 [`versions/v0.5.1`](../versions/v0.5.1/)（该版 24 轮对话全文 + 技能包）与
[`docs/evolution-audit.md`](../docs/evolution-audit.md)（六版演进审计），我按自己的理解把这套方法论
重新收敛了一遍，落成这一版。

所以它的定位是：**同一条思想主线的再表达**，不是另一个技能。与本技能仓的关系是"读后重写"：
主张一致，组织方式与取舍不同。

## 为什么平铺在顶层

本版不属于 [`versions/`](../versions/) 的六版谱系——那六版是**同一场会话在六个时刻的冻结**，
而本版是**读完之后自己重写**的，血缘不同，所以不进 `versions/`，而是与它、与 `docs/` 平铺并列，
供对照阅读。

它同时是 v0.6.0 的一手输入：[`versions/v0.6.0/skill/MERGE_DECISION.md`](../versions/v0.6.0/skill/MERGE_DECISION.md)
把它定位为 `cognitive_execution_source`（认知与执行协议的强化版），与作为工程母版的 v0.5.1 增量合并成
[`versions/v0.6.0`](../versions/v0.6.0/)。

## 我读到的七条主张

1. **文档是投影，模型才是资产。** 不要从源码直接跳到成品散文；先建单一、可追溯的系统知识模型
   （Canonical Knowledge Model），Markdown / Mermaid / 表格 / 代码都是它的视图。
2. **知识只有五类**：结构 / 行为 / 约束 / 证据 / 演化。一切规则都该落在这五类里；
   落不进去的多半是工具细节，属于扩展层。
3. **认知坐标是一条唯一的骨架**，且**不允许跨尺度跳跃**：
   `System → Subsystem → Concern → Scenario → Path → Mechanism → Entity → State/Protocol → Symbol → Code`。
   "读起来顺畅"的来源是尺度连续，不是措辞。
4. **先架构，后细节。** 大型系统的最大失败模式不是"某个函数没懂"，而是"局部都懂、整体没骨架"；
   所以 System Atlas 是持久地基，但要按需构建（渐进闸门 + L0–L3 深度），不是一上来重建全仓。
5. **理解模式先于表达方式。** 模式是"理解问题的分类"，不是"图的分类"；
   表达选择永远是「核心问题 → 主导模式 → 表达族 → 方法 → 渲染器」，**语义在前，渲染器在后**。
6. **每条结论都要能回到源码。** `Claim → Evidence → Source Anchor`，区分
   FACT / INFERENCE / INTERPRETATION，证据不足就标 UNVERIFIED 或降级删除。
7. **技能自身的演进也必须是可追溯的。** 反馈 → 失败分类 → 病例 → 候选规则 → 回归 → 人批准；
   版本演进**默认是 merge，不是 rewrite**，任何删除都要留下 reason / replacement / regression evidence。
   （这条是拿一次真实的回归事故换来的，见 `skill/evolution/evolution-policy.md` 末节。）

## 目录

```text
skill-ds/
├── README.md                        本文件：来龙去脉与取舍
└── skill/                           技能包本体
    ├── SKILL.md                     核心协议（认知总纲 / 坐标骨架 / 六阶段·七闸门 / 硬规则）
    ├── references/
    │   ├── architecture-atlas.md    架构地基：Atlas 内容、重构方法、静态≠运行时
    │   ├── knowledge-model.md       规范知识模型：实体 / 关系 / 行为 / 约束 / Claim
    │   ├── situated-knowledge.md    情境化知识：版本 / 构建 / 性能 / 决策 / 学习路径 / 变更影响
    │   ├── patterns.md              九种理解模式 + 打分 + 易混淆清单
    │   ├── representation.md        表达族与渲染器取舍
    │   ├── traceability.md          结论→证据→锚点、D1–D3、五类证据、置信度四因子
    │   └── validation.md            V1–V6 校验与返修路由
    ├── evolution/evolution-policy.md  学习闭环 + 版本非回归纪律
    ├── knowledge-sources/README.md    外部"老师"的查询条件、注册 schema 与权威边界
    └── templates/source-reading-note.md  笔记骨架与交付自检
```

## 与 v0.5.1 的取舍

**保留**（同一思想的承重墙）

- 一份模型、多种视图；六阶段推理协议；System Atlas 作为持久地基；
- 一个主导理解模式；`Claim → Evidence → Source Anchor` + D1/D2/D3；
- 表达选择流水线；V1–V6 校验；merge-not-rewrite 的版本纪律。

**收敛**（避免把工具手册混进认知规则）

- 23 种历史图法的完整目录 → 压缩为"表达族 + 渲染器取舍"，
  UML / C4 / SEI / DFD / NS / HIPO / Petri Net 的细节下沉到 `knowledge-sources/`，按需查；
- 具体的 `Clang / CodeQL / Sourcegraph` 等能力不写进核心，只在核心留一句
  "文本搜索不够时请求语义分析"。

**新增**（对话里讨论过、但未被显式前置的部分）

- 五类知识的**总纲前置**，作为一切规则的收纳箱；
- 认知坐标写死 9 层并明确"**不得跨认知尺度跳跃**"；
- 情境化知识单独成篇：时间/版本、构建变体、性能关注点、决策理由、学习路径、知识冲突、变更影响；
- 证据五来源（Source / Documentation / Static / Runtime / Test）与置信度四因子；
- 反模式命名表与中英术语对照表。

**刻意不做**

- 不保留 SHA-256 基线清单与完整性测试脚本：那是工程手段，不是认知规则。
  本版只把"**不许静默丢能力**"写成纪律并给出移除记录格式。

## 已知边界

- 本版是**理解版**，未做逐条基线能力比对，也没有 gold case 回归集；也正因如此它**没有直接发版**——
  v0.6.0 走的是「以 v0.5.1 为基线、把本版的原则增量并进去」的路线，
  避开了"理解版直接发版会丢工程资产"的风险。
- `SKILL.md` 的 frontmatter 使用单行 `description`、不含尖括号——
  这是刻意规避上一系列六版都踩到的官方校验器报错（`description: >-` 里含 `<`/`>`）。
