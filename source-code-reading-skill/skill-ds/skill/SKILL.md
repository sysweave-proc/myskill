---
name: skill-ds
version: 0.1.0
description: Read large C/C++ systems as one canonical, traceable knowledge model instead of free-form summaries: build an architecture foundation, execute through progressive gates, extract the knowledge model, recognize the dominant comprehension pattern, choose representation by semantics before renderer, trace every claim to source evidence, and evolve by merge rather than rewrite.
---

# skill-ds · 源码阅读知识建模

> 面向 Linux / PostgreSQL / MySQL / LLVM 这类**几十万行以上、还在演进的 C/C++ 系统**。
> 本技能不产出"读完就过期的总结"，它产出**一张可缩放、可回源、可更新的知识模型**，以及模型的若干视图。

## 0. 唯一的操作原则

```text
                       系统知识模型
                            │
          ┌─────────────────┼─────────────────┐
          ↓                 ↓                 ↓
      架构视图           路径视图           主题视图
          └─────────────────┼─────────────────┘
                            ↓
                        源码视图
```

**一份模型，多种视图。** Markdown、Mermaid、表格、代码片段都是投影；投影可以重画，模型不能丢。

任何时候写下一句话，都要能回答：

```text
这句话挂在模型的哪个节点上？
它的证据在哪一段源码？
```

如果答不上来，这句话就还不该写进文档。

---

## 1. 认知总纲：五类知识

不论读什么都先问一句"我现在在建哪一类知识"，再动手。允许无限扩展的只有细节，不允许无限扩展的是这五类。

| 维度 | 回答的问题 | 承载的知识对象 |
|---|---|---|
| Structure 结构 | 系统由什么组成 | Architecture、Subsystem、Entity、Relation |
| Behavior 行为 | 系统怎么运行 | Scenario、Path、Flow、State、Lifecycle、Concurrency、Data Path |
| Constraint 约束 | 什么规则不能破 | Invariant、Protocol、Precondition、Ownership rule |
| Evidence 证据 | 凭什么相信 | Claim、Evidence、Source anchor、Conflict |
| Evolution 演化 | 知识怎么随源码/反馈变化 | Version、Build context、Case、Rule、Change impact |

口诀：**谁组成（结构）→ 怎么动（行为）→ 不许怎样（约束）→ 凭什么（证据）→ 怎么变（演化）**。

新增任何规则前先自检：它落在哪一类？落不进去的，多半是工具细节，属于扩展层（见 §7），不属于核心。

> 一个**活着**的系统还有情境维度：版本、构建变体、性能、决策理由、学习路径、变更影响。
> 它们不是第六类知识，而是把上面五类放回情境——见 `references/situated-knowledge.md`。

---

## 2. 认知坐标：唯一骨架

所有知识对象都要能挂到下面这条骨架上。**总图按需、设则唯一且前置**：这条骨架就是本技能唯一的总图。

```text
System
 └─ Subsystem
     └─ Concern                我为什么关注它
         └─ Scenario           什么真实事件会触发它
             └─ Path           它怎么穿过系统
                 └─ Mechanism  它靠什么机制实现
                     └─ Entity / Resource      由哪些对象承载
                         └─ State / Protocol   对象处于什么状态、守什么协议
                             └─ Symbol         哪段代码实现
                                 └─ Code
                                     └─ Evidence
```

三个方向都必须支持：

- **向下 zoom in**：System → … → Code，回答"实现到底是什么"；
- **向上 zoom out**：Code → … → System，回答"它究竟属于哪里"；
- **横向 sideways**：Entity / Mechanism → 其他 Path、Concern、生命周期、并发关注点、邻接子系统。

**硬约束：不得跨认知尺度跳跃。**

```text
✗ 上一段：Storage（子系统尺度）
  下一段：spin_lock_irqsave()（指令/符号尺度）

✓ Storage → Buffer Manager → Buffer Lookup → Mapping → Mapping Lock → 锁获取代码
```

"顺畅"的观感来自尺度连续，不来自措辞。一条来源是一条来源，一个实体可以同时属于多条 Path 和多个 Concern——**源码本身是图，不要为了排版把它压成树**。

---

## 3. 执行协议：六阶段 × 七道闸门

两层结构，各管一件事：

- **六阶段**是推理阶段（"要做哪几种思考"），顺序固定；
- **闸门**是进出门（"做到什么程度才准进下一步、什么时候停"），用来防止一上来重建整个仓库。

```text
六阶段（推理）                    闸门（进出）
① Scope & Explore       ←→      Gate 0 Scope
② Knowledge Model       ←→      Gate 1 Orient → Gate 2 Minimum Model
③ Pattern Recognition   ←→      Gate 3 Pattern
④ Traceability          ←→      Gate 4 Trace
⑤ Representation & Doc  ←→      Gate 5 Represent
⑥ Validation            ←→      Gate 6 Validate
                                        ↓
                            只在出现具体缺口时加深
```

| 闸门 | 最小产出 | 准出条件 |
|---|---|---|
| 0 Scope | 问题 + 边界 | 目标能用 1–3 句话说清 |
| 1 Orient | 系统坐标 | 能回答"这东西在哪" |
| 2 Minimum Model | 最小够用的模型 | 没有阻塞性未知 |
| 3 Pattern | 主导理解问题 | 表达目标已明确 |
| 4 Trace | 有证据的结论 | 核心结论能回源 |
| 5 Represent | 最小有用视图集 | 概念 → 关系 → 源码可导航 |
| 6 Validate | 已校验结果 | 无已知的中心矛盾 |

### 深度分级

- **L0 Orientation**：它在哪、周围是什么；
- **L1 Local model**：核心实体、管理/数据关系、一条代表性路径；
- **L2 Source trace**：关键函数/字段/状态/生命周期/并发/数据流；
- **L3 Cross-cutting**：更大的子系统关系、恢复、性能、权衡。

**默认从 L1 起步。** 进入 L2/L3 必须有一个点名道姓的未解问题（"因为要判断 X 是否会走 Y 分支，所以要追 Z"）。

### 反过度设计（明确不许做的事）

```text
不要 默认读遍全仓
不要 在任务还没理由之前就重建完整架构
不要 枚举每一个实体和每一条边
不要 生成所有可能的图
不要 目标源码已经能回答时还去查外部资料
不要 图、正文、代码三处重复同一解释
```

### 受阻时的重入路由

```text
缺上下文/证据   → Scope & Explore / Trace
模型不对        → Knowledge Model
模式选错        → Pattern Recognition
图/文档不好     → Representation & Document
跨视图不一致    → Validation + 回到最小受影响阶段
```

重入是**回退到最早出问题的阶段**，不是推倒重来。

---

## 4. 分阶段要点

### Stage 1 — Scope & Explore

先写清：主题、核心问题、读者与用途、深度、包含范围、**排除范围**、当前架构坐标。

然后**按未知探索，不线性翻文件**。有语义导航能力时优先用它：

```text
符号定义 → 引用 → 调用者/被调者 → 字段读/写方
→ 生命周期函数 → 同步操作 → 跨模块边界
```

每一次展开都必须消掉一个显式未解问题（维护 `open_questions`，见 `references/traceability.md`）。

### Stage 2 — Knowledge Model

把源码事实抽成 Entity / Relation / Flow / State / Lifecycle / Concurrency / Constraint / Claim / Evidence，并同时挂上架构坐标（system / subsystem / concern / scenario / path / mechanism）。

细节见 `references/knowledge-model.md`；需要把知识放回版本 / 构建 / 决策 / 性能 / 学习路径 / 变更影响的情境时，见 `references/situated-knowledge.md`。

### Stage 3 — Pattern Recognition

选**恰好一个主导理解模式**，可挂若干次要模式。判断依据是"哪个问题最决定这段知识该怎么被理解"，**不是关键词命中**。

```text
Structural / Lifecycle / Flow / State / Concurrency
/ Data Path / Resource / Recovery / Architecture
```

细节见 `references/patterns.md`。

### Stage 4 — Traceability

每个实质结论走同一条链：

```text
Claim → Evidence → Source anchor → Trace
```

区分 `FACT` / `INFERENCE` / `INTERPRETATION`；证据不足就标 `UNVERIFIED`，然后要么继续追，要么降级限定，要么删掉。

细节见 `references/traceability.md`。

### Stage 5 — Representation & Document

表达选择严格按下面的顺序，**语义在前，渲染器在后**：

```text
核心问题 → 主导模式 → 表达族 → 具体方法 → 渲染器/工具
```

图是**可选项**。当图不能降低认知负荷时，优先文字或紧凑表格。

细节见 `references/representation.md`。

### Stage 6 — Validation

六个校验层：结构、语义、可追溯、表达、读者可导航、架构一致性。失败时按 §3 的重入路由回到最小受影响阶段。

细节见 `references/validation.md`。

---

## 5. 架构 ↔ 主题 的整合规则

1. 有 System Atlas 时，每个主题必须有稳定的架构坐标；
2. 主题通常应挂到一条或多条运行时/场景路径上；
3. 一个符号可以属于多个 Concern / Path，不要强行排成树；
4. **架构结论和实现结论一样需要证据**；
5. Atlas 可被修订：新证据可以细化甚至推翻当前架构模型；
6. 跨层关系用一等类型：`contains`、`refines`、`participates_in`、`implemented_by`、`evidenced_by`、`related_through_path`。

架构地基的构造方法见 `references/architecture-atlas.md`。

---

## 6. 演进：合并式演进，不是重写式演进

用户反馈与复核过的病例可以产生**候选规则**，但没有跑过回归的规则不得成为规范。

```text
反馈 → 失败分类 → 病例 → 候选规则 → 回归 → 人/项目批准 → 采纳
```

**绝不允许模型静默改写自己的规则。**

### 版本非回归不变量

一个 Skill 版本是**增量演进**，不是推倒重建：

```text
上一版 + 新能力/修正
   → 能力清单 → 与基线比对 → 最小补丁/增量合并
   → 回归 → 发版
```

发版前必做：①盘点上一版能力与文件；②与基线比对；③除显式记录外保留既有能力；④只加解决新问题的最小改动；⑤跑完整性/回归检查；⑥在 CHANGELOG 记录。

**任何删除都必须留下 `reason` / `replacement` / `regression evidence`。** 这不是洁癖：曾有一版为了强调"分阶段执行"而整包重建，结果 `knowledge-sources/`、`evolution/`、`cases/`、`references/diagrams/` 整体消失——那是回归，不是进化。

细节见 `evolution/evolution-policy.md`。

---

## 7. 分层：什么进核心，什么不进

| 层 | 内容 | 例子 |
|---|---|---|
| Core Skill | 推理协议 + 规范模型 + 安全规则 | 架构、模式、追踪、表达、校验 |
| Capability extensions | 获取事实的能力（工具） | Clang AST、CodeQL、Sourcegraph、perf、BPF、VTune |
| Knowledge sources | 外部"老师"，教方法与工具语义 | UML、ISO 42010、SEI V&B、C4、arc42、渲染器文档 |
| Evolution assets | 反馈/病例/回归/变更流程 | gold case、failure case、候选规则 |

判据一句话：

> **"拿到事实之后怎么理解"进核心；"如何获取事实"进扩展。**

核心只需要知道"文本搜索不够时去请求语义分析"，不需要装下每个分析工具的手册。外部资料可以定义记号语义、教方法论、给正反例、说明工具能力；**但不能推翻目标仓库的事实，也不能因为一张图长得像 CFG 就把它当 CFG**。

细节见 `knowledge-sources/README.md`。

---

## 8. 硬规则

1. 非平凡任务，绝不允许从源码直接跳到成品散文（必须先有模型）。
2. 绝不因为一个指针字段就断言 ownership。
3. 绝不把调用图当作运行时流程。
4. 绝不把 enum 当作完整状态机。
5. 绝不因为"看到有锁"就断言它保护了什么。
6. 绝不只凭目录名推断架构。
7. 绝不因为图形相似就给某张图贴上形式记号的名字。
8. 绝不把发现的每个实体都塞进一张图。
9. 绝不在图、正文、代码里重复同一解释（除非每层都增加不同价值）。
10. 绝不把 INTERPRETATION 当作源码 FACT 呈现。
11. 绝不让外部资料压过目标仓库的证据。
12. 保留精确的源码名作为导航锚点。
13. 当某种表达反复失败时，先把它记成病例，再改规则。
14. 优先"最小够用的视图"，而不是最大信息密度。

---

## 9. 模式

| 模式 | 做什么 | 不产出什么 |
|---|---|---|
| Explore | 研究源码与架构 | 不产出最终文档 |
| Model | 建立/更新规范知识模型 | — |
| Document | 由已验证模型渲染文档 | 不新增未验证结论 |
| Review | 审计既有文档（源码/架构/结论/表达/导航） | 不直接改文档 |
| Evolve | 分析复核过的失败，产出候选规则 | **不自动采纳** |

---

## 10. 交付物

按模式返回其中若干项：

```text
System Atlas
Knowledge Model
Pattern Profile
Trace Map
Representation Plan
源码阅读文档
Review Report
Rule Proposal
Regression Result
```

---

## 11. 质量目标

好的结果应让读者能回答：

```text
我在系统的哪里？
这个子系统在解决什么问题？
这个机制参与哪条路径？
核心实体有哪些？彼此什么关系？
什么随时间变化？
有哪些并发/资源约束必须知道？
实现在哪？
文档凭什么下这个结论？
下一步该读什么？
```

---

## 12. 术语对照

| 中文 | 规范标识 | 含义 |
|---|---|---|
| 认知坐标 | Cognitive Spine | System → … → Code 的唯一骨架 |
| 架构地基 | System Atlas | 系统的稳定坐标系 |
| 规范知识模型 | Canonical Knowledge Model | 一份模型多种视图的那个模型 |
| 理解模式 | Comprehension Pattern | 决定"该怎么理解"的主导问题 |
| 表达族 | Representation Family | 与语义匹配的一类表达方式 |
| 结论 | Claim | 可被证据支持或推翻的断言 |
| 证据锚点 | Source Anchor | 仓库 + 版本 + 路径 + 限定符号 |
| 病例 | Case | 一次失败的可回归记录 |
| 静默丢能力 | Silent Capability Loss | 版本演进中未记录的删除，等价于回归 |
