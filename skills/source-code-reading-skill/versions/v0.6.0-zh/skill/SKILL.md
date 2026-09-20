---
name: source-code-reading
description: |-
  一套面向大型 C/C++ 系统（Linux、PostgreSQL、MySQL、LLVM 一类）的「源码阅读知识建模」认知与执行协议：
  先建立单一、可追溯的系统知识模型（System Atlas + Cognitive Spine），再把模型投影成图、表、文档。
  它规定的是「拿到源码事实之后怎样理解、建模、追踪、表达、校验」，本身不产出成品交付物。
  This skill should be used when the user asks to 读源码、读懂某段 C/C++ 代码、追一条真实调用链、
  搞清楚某机制到底怎么实现、判断某个符号在系统里的位置、复核或审计一份源码笔记/架构文档的结论
  有没有源码证据、表达是否恰当，或为大型仓库建立与更新架构模型（System Atlas）；
  也适用于需要在多种图示/表达方式之间做取舍，或确定主导理解模式的场合。
  SCOPE BOUNDARY (hard)：本技能只提供认知与执行协议，不交付成品文档集。
  单篇机制级源码笔记及其笔记库的落盘规范、仓库级架构/系统设计文档集（模块职责、依赖全景），
  都属于「成品交付」层，不由本技能产出；本技能只负责让它们的结论可追溯、表达有据。
metadata:
  version: 0.6.0
  scope: "global / cross-project（任何大型 C/C++ 代码库）"
  canonical: "source-code-reading-skill/versions/v0.6.0-zh/"
---

# Source Code Reading Skill v0.6.0

> 面向 Linux / PostgreSQL / MySQL / LLVM 这类几十万行以上、持续演进的 C/C++ 系统。
> 本技能不是“把源码总结成 Markdown”，而是：**先建立一份可追溯、可缩放、可更新的知识模型，再把模型投影成不同视图。**

## 0. 唯一操作原则：一份模型，多种视图

```text
                         Canonical Knowledge Model
                                      │
                  ┌───────────────────┼───────────────────┐
                  ↓                   ↓                   ↓
             Architecture          Paths              Topics
                  │                   │                   │
                  └───────────────────┼───────────────────┘
                                      ↓
                                Source / Code
```

Markdown、Mermaid、Graphviz、表格、代码片段、评审报告都只是投影。**投影可以重画，模型不能丢。**

任何进入最终文档的重要句子都应该能够回答：

```text
这句话挂在模型的哪个节点/关系上？
它的证据在哪里？
它适用于哪个版本/构建上下文？
```

答不上来时，不要把它写成无条件结论。

受控术语一律以 `references/glossary.md` 为准：**一个概念只有一个英文原名和一个中文正名**，不得另起写法。

---

## 1. 认知总纲：五类知识 + 情境

所有源码阅读知识先归入五类：

| 维度 | 核心问题 | 主要对象 |
|---|---|---|
| Structure | 系统由什么组成？ | Architecture、Subsystem、Entity、Relation |
| Behavior | 系统怎么运行？ | Scenario、Path、Flow、State、Lifecycle、Concurrency、Data Path |
| Constraint | 什么规则不能破？ | Invariant、Protocol、Precondition、Ownership、Ordering、Cleanup |
| Evidence | 凭什么相信？ | Claim、Evidence、SourceAnchor、Conflict |
| Evolution | 这个知识怎么随系统变化？ | Version、BuildContext、Case、Rule、ChangeImpact |

口诀：**谁组成 → 怎么动 → 不许怎样 → 凭什么 → 怎么变。**

一个活着的系统还要记录情境：版本、构建变体、性能、决策理由、学习路径、变更影响。它们不是第六类知识，而是五类知识的上下文，见 `references/situated-knowledge.md`。

### 1.1 Core 与扩展边界

```text
Core Skill
  = 拿到事实之后，应该怎样理解、建模、追踪、表达、校验

Capability extensions
  = 如何获得事实（AST、CodeQL、perf、BPF、VTune、Sourcegraph...）

Knowledge sources
  = 从外部老师学习方法、记号、工具能力和通用语义

Evolution assets
  = 用病例、gold、failure、回归、反馈改进技能
```

判据：**“拿到事实之后怎么理解”进核心；“怎么获取事实”进扩展。**

---

## 2. 唯一认知坐标：Cognitive Spine

所有知识对象都应能在下面的连续坐标中定位：

```text
System
 └─ Subsystem
     └─ Concern                我为什么关注它
         └─ Scenario           什么真实事件触发它
             └─ Path           它怎么穿过系统
                 └─ Mechanism  它靠什么机制实现
                     └─ Entity / Resource   由哪些对象承载
                         └─ State / Protocol 对象处于什么状态、守什么协议
                             └─ Symbol       哪段代码实现
                                 └─ Code
                                     └─ Evidence
```

三个方向必须同时支持：

- **Zoom in**：System → … → Code，回答“实现到底是什么”；
- **Zoom out**：Code → … → System，回答“它究竟属于哪里”；
- **Sideways**：Entity / Mechanism → 其他 Path、Concern、生命周期、并发、资源或邻接子系统。

### 2.1 不允许跨尺度跳跃

```text
✗ Storage → spin_lock_irqsave()

✓ Storage → Buffer Manager → Buffer Lookup → Mapping → Mapping Lock → 锁获取代码
```

尺度连续比措辞华丽更重要。源码天然是图：一个实体可以参加多条 Path、多个 Concern，不要为了排版强行压成树。

---

## 3. 架构地基：System Atlas

大型系统先建立或加载 **System Atlas**，但必须渐进构建，不允许一上来重建整个仓库。

Atlas 至少包含：

```text
System Context
Architecture Spine
Subsystem Map
Critical Scenarios / Runtime Paths
Cross-cutting Concerns
Architecture ↔ Source mappings
Open Architecture Questions / Gaps
```

架构是**持久坐标系**，不是每篇笔记重复的一张大图。系统级工作优先阅读：

- `references/architecture-model.md`
- `references/architecture-reconstruction.md`
- `references/architecture-atlas.md`

### 3.1 架构不是目录树

架构结论必须经过场景/运行时路径和源码证据验证。目录名、文件相邻、单纯调用关系都不足以证明高层架构关系。

当“意图架构”与“as-built 行为”冲突时，同时保留两份证据，并标记是实现细节、架构漂移、过时文档还是未决歧义。

---

## 4. 执行协议：六阶段 × 七道闸门

**六阶段**解决“现在要做哪类思考”；**七道闸门**解决“做到什么程度才准继续、什么时候停”。

```text
六阶段（推理）                    闸门（进出）
① Scope & Explore       ←→      Gate 0 Scope
② Knowledge Model       ←→      Gate 1 Orient → Gate 2 Minimum Model
③ Pattern Recognition   ←→      Gate 3 Pattern
④ Traceability          ←→      Gate 4 Trace
⑤ Representation & Doc  ←→      Gate 5 Represent
⑥ Validation            ←→      Gate 6 Validate
                                       ↓
                           只有出现具体缺口才继续加深
```

### Gate 0 — Scope

明确：用户问题、目标主题/子系统、源码仓库与 revision、构建上下文（若相关）、读者/用途、深度、包含范围、排除范围、期望输出。

**退出条件：**目标能用 1–3 句话准确描述。

### Gate 1 — Orient

只找回答“它在系统哪里”所需的上下文：边界、邻接子系统、入口点、关键类型/符号、明显的测试/文档。

**不要在这里重建全系统。**

### Gate 2 — Minimum Knowledge Model

只建立回答当前问题所需的最小模型：

```text
System → Subsystem → Path / Scenario → Mechanism → Entity → Symbol
```

不是每个任务都需要所有节点。**没有阻塞性未知，就可以继续。**

### Gate 3 — Pattern

选择**恰好一个主导理解模式**，可有若干次要模式。主导模式由“哪个问题最决定该知识如何被理解”决定，不由关键字或你会画哪种图决定。

### Gate 4 — Trace

只追踪足以证明/限定中心结论的证据。使用 D1/D2/D3 深度和显式 `trace_boundary`。

### Gate 5 — Represent

先确定语义，再决定表达方式和渲染器。目标是最小有用视图集，确保“概念 → 关系 → 源码”可导航。

### Gate 6 — Validate

执行结构、语义、可追溯、表达、读者导航、架构一致性校验。失败时回到**最早受影响的最小阶段**，不要整篇盲目重生成。

---

## 5. Progressive Depth：L0–L3

- **L0 Orientation**：它在哪、周围是什么；
- **L1 Local model**：核心实体、管理/数据关系、一条代表性路径；
- **L2 Source trace**：关键函数/字段/状态/生命周期/并发/数据流；
- **L3 Cross-cutting**：更广的子系统关系、恢复、性能、权衡。

**默认从 L1 开始。进入 L2/L3 必须有点名道姓的未解问题。**

例如：

```text
因为我要判断 X 是否会走 Y 分支，
所以必须继续追 Z 的读取方/状态迁移。
```

### 5.1 反过度设计

```text
不要 默认读遍全仓
不要 在任务还没有理由之前就重建完整架构
不要 枚举每一个实体和每一条边
不要 生成所有可能的图
不要 源码已经能回答时还查外部资料
不要 图、正文、代码三处重复同一解释
```

每一次探索都必须消掉或细化至少一个 `open_question`；否则是在闲逛。

---

## 6. 六阶段执行细则

### Stage 1 — Scope & Explore

从问题开始，不从文件开始。典型语义导航顺序：

```text
符号定义 → 引用 → 调用者/被调者 → 字段读/写 → 生命周期函数
→ 同步操作 → 资源操作 → 跨模块边界 → 测试/运行时证据
```

维护 `open_questions`，细节见 `references/tracing/exploration-policy.md`。

### Stage 2 — Knowledge Model

把源码事实抽成：

```text
Entity / Relation
Flow / State / Lifecycle / Concurrency / Data Path
Constraint / Invariant / Protocol
Claim / Evidence / Conflict
```

并挂上架构坐标：

```text
system / subsystem / concern / scenario / path / mechanism
```

见 `references/knowledge-model.md`。

### Stage 3 — Pattern Recognition

从：

```text
Structural
Lifecycle
Flow
State
Concurrency
Data Path
Resource
Recovery
Architecture
```

中选择一个 dominant。见 `references/patterns/pattern-catalog.md`。

### Stage 4 — Traceability

所有实质结论都走：

```text
Claim → Evidence → Source Anchor → Trace
```

并区分：

```text
FACT
INFERENCE
INTERPRETATION
```

证据不足：`UNVERIFIED`；然后继续追踪、降级限定或删除。见 `references/tracing/`。

### Stage 5 — Representation & Document

表达选择必须按：

```text
核心问题
  ↓
主导模式
  ↓
表达族
  ↓
具体方法
  ↓
渲染器 / 工具
```

语义优先，渲染器第二。图是可选项，不是默认产物。见 `references/representation/representation-policy.md` 和 `references/diagrams/diagram-catalog.md`。

### Stage 6 — Validation & Orchestration

执行 V1–V6。失败后沿最小受影响路径回退。见 `references/validation/validation-policy.md`。

---

## 7. 主导理解模式与表达族

### 7.1 主导理解模式

| Pattern | 核心问题 |
|---|---|
| Structural | 谁和谁相连？ |
| Lifecycle | 对象如何诞生、持有、释放？ |
| Flow | 一次操作怎么执行？ |
| State | 有哪些状态、怎么迁移？ |
| Concurrency | 谁共享、谁保护、谁等待？ |
| Data Path | 数据怎么移动、怎么变形？ |
| Resource | 稀缺资源如何定位、复用、回收？ |
| Recovery | 失败之后发生什么？ |
| Architecture | 它在系统里处于哪里？ |

**Pattern 是理解问题的分类，不是图的分类。**

### 7.2 Representation Family

```text
Entity/Relationship
Management/Ownership
Flow/Control
State/Lifecycle
Sequence/Interaction
Data/Dataflow
Concurrency/Sync
Resource/Cache
Architecture/Layer
Recovery/Failure
Memory Layout
```

表达族要解决的不是“图长什么样”，而是“读者缺哪种关系”。

### 7.3 图 / 文 / 代码的分工

```text
图   → 空间与时间关系
文   → 语义、条件、后果
代码 → 证据与导航
```

图不承担语义定义，文字不承担拓扑，代码不代替结论。

核心图视图建议控制在 **5–12 个主要节点**。过大就拆 context / core / detail，不要靠缩小字体解决。

---

## 8. Traceability：证据纪律

### 8.1 证据优先级

目标仓库的源码、目标项目官方文档、静态分析、运行时观察、测试都是证据，但其“证明什么”不同。

尤其区分：

```text
“代码可能这么执行”                  ← 静态证据
“这个 workload 下确实这么执行”       ← 运行时证据
```

### 8.2 Source Anchor

优先使用：

```text
repository + revision
path
qualified symbol
field / expression
code region
```

行号只是导航辅助，不能作为唯一身份；符号名通常比行号更耐代码演进。

### 8.3 D1–D3

```text
D1 Local       局部事实
D2 Structural  跨符号语义
D3 System      架构/运行时解释
```

结论尺度与追踪深度必须匹配，不要为了“看起来更充分”无理由继续往下追。

### 8.4 置信度

不要只给 High/Medium/Low；在可能时记录：

```yaml
confidence:
  level: MEDIUM
  because:
    direct_source: yes
    runtime_verified: no
    version: "17"
    inference_depth: 2
```

---

## 9. Situated Knowledge：让知识保持“活”

同一条结论必须能回答“针对哪个版本/构建/场景”。至少考虑：

```text
Version / Revision
Build / Configuration
Performance Concern
Decision / Rationale
Learning Path
Conflict
Change Impact
```

### 9.1 构建变体

```text
Code exists ≠ Code compiled ≠ Code reachable ≠ Code active
```

记录：compiler、platform、arch、build_type、defines、enabled_modules 等。

### 9.2 性能关注点

对数据库/OS/存储，性能本身是一等 Concern：

```text
Query → Lock → Hash → Memory → NUMA → Cache → IO
latency · contention · locality · bandwidth · queueing · CPU migration
```

### 9.3 决策与理由

```text
Decision
├── Problem
├── Constraint
├── Alternative
├── Choice
├── Consequence
└── Evidence
```

没有 Evidence 的设计动机必须标为 `INTERPRETATION`。

### 9.4 学习路径

知识间的“先学什么”本身是另一种图：

```text
Architecture → Process Model → Memory Model
→ Buffer Manager → Buffer Lookup → Buffer State
```

可记录：

```yaml
learning:
  prerequisites: []
  unlocks: []
  recommended_depth: L0 | L1 | L2 | L3
```

### 9.5 冲突与变更影响

不覆盖冲突：

```text
different version / build / runtime path
documentation drift / historical behavior
```

并记录：

```text
源码变化 → 受影响符号 → 受影响结论 → 受影响架构 → 受影响文档/图
```

---

## 10. 模式、关系与常见误判的硬约束

1. Pointer ≠ ownership。
2. Pointer ≠ runtime identity，除非已经完成相应追踪。
3. Lock acquisition ≠ 已经证明某个状态受到该锁保护。
4. enum ≠ 完整状态机。
5. 调用边 ≠ 运行时执行路径。
6. 目录相邻关系 ≠ architecture。
7. 状态可以由多个字段联合编码。
8. 一个实体可以参与多条 Path / Concern。
9. 图的每条边都必须具有明确的语义方向和关系类型。
10. 关系语义未知时，应使用更弱的关系，而不是猜测一个更强的关系。
11. 架构 Claim 与实现 Claim 一样，都必须有证据支持。
12. Mermaid / Graphviz 的视觉表现永远不能证明其具有某种形式化记法语义。
13. 不要把发现的所有实体都放进一张图。
14. 不要在图、正文和代码中重复同一解释，除非三者分别提供不同价值。
15. 外部来源可以教授方法或工具语义，但目标仓库证据决定目标行为。
16. 绝不能把 `INTERPRETATION` 表述成源码 `FACT`。
17. 保留源码中的原始名称，作为导航锚点。
18. 优先选择足够小且能够完成任务的视图，而不是追求最大信息密度。

---

## 11. Modes

### Explore
只调查源码与架构，不急于生成最终文档。

### Model
建立或更新 canonical knowledge model。

### Document
从已经验证的模型投影成文档。

### Review / 评审
从源码、架构、Claim、Representation、Navigation 等维度审计已有文档。

### Evolve / 演进
分析复核失败，生成 candidate rule 和 regression；**不得自动升级规范规则**。

---

## 12. 外部知识源

只有在以下情况才查外部资料：

```text
规则含糊
方法/记号选择没把握
渲染器能力不确定
分析精度不足
出现反复失败，需要寻找候选规则
```

不要为了“给文档加引用”而查。

权威边界：

```text
外部方法论      → 定义方法
渲染器官方文档  → 定义工具能力
目标源码        → 定义目标实现事实
项目 reviewed case → 定义本地偏好
```

见 `knowledge-sources/README.md`、`knowledge-sources/resource-advisor.md` 与 `knowledge-sources/index.yaml`。

---

## 13. Evolution：合并式演进，不是重写式演进

这是本技能自身的硬约束：**版本演进默认是 merge（增量合并），不是 rewrite（重写）。**

```text
反馈
  ↓
失败分类
  ↓
Case
  ↓
候选规则
  ↓
针对 Gold Case 的回归
  ↓
人工 / 项目批准
  ↓
已采纳规则
```

### 13.1 四级演进

```text
L1 当前任务就地修正
L2 可复用病例
L3 候选规则
L4 已采纳规范变更
```

只有 L4 才改变规范 Skill。模型可以提出候选规则，但不能静默修改规范。

### 13.2 版本非回归不变量

```text
上一版
  + 新能力 / 新修正
  ↓
能力清单
  ↓
基线对比
  ↓
最小增量合并
  ↓
完整性回归
  ↓
语义回归
  ↓
变更日志
  ↓
新版本
```

发版前：

1. 盘点上一版能力与文件；
2. 与基线逐文件、逐能力比对；
3. 原有能力默认全部保留；
4. 只做解决新问题的最小增量修改；
5. 任何删除必须记录 `reason / replacement / regression_evidence / approved`；
6. 运行完整性与语义回归；
7. 更新 CHANGELOG 与能力清单。

### 13.3 为什么写死这一条

历史演进中已经出现过“为了更好表达执行阶段而重建整个包”，导致知识源、案例、图法目录、演进资产和其他参考资料整体消失。那不是进化，而是回归。

因此：**Skill 的质量不是某一版 SKILL.md 看起来多漂亮，而是整个知识资产集合能否持续增长而不悄悄丢能力。**

---

## 14. 主要交付物

按任务返回一个或多个：

```text
System Atlas
Knowledge Model
Pattern Profile
Trace Map
Representation Plan
Source-reading document
Review Report
Rule Proposal
Regression Result
```

高质量结果至少让读者能够回答：

```text
我在哪？
核心机制是什么？
它为什么存在？
哪条路径会用它？
核心实体如何管理、交互、迁移？
哪些约束/并发/资源规则重要？
源码在哪里？
这条结论为什么成立？
针对哪个版本/构建？
下一步读什么？
```
