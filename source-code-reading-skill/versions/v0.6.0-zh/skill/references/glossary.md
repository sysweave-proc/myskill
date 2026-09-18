# 术语表 · Glossary

本表是**唯一的中英术语准绳**。任何文件里出现的受控术语，一律以本表的「英文原名 / 中文正名」为准。

## 0. 使用规则

```text
1. 一个概念只有一个英文原名和一个中文正名，不得另起写法。
2. 规范正文（SKILL.md 及 references/ 规范件）优先写英文原名；中文正名只用于必须中文叙述之处。
3. 新术语必须先在本表登记再使用。
```

第 1 条是硬约束。历史上 `D1 局部` 与 `D1 Local` 曾同时存在，导致读者与 Agent 无法确定二者是否同一物——这正是本表要消灭的「术语未锚定」。

---

## 1. 骨架坐标 · Cognitive Spine

自上而下是一条**连续的尺度**，不允许跨尺度跳跃（见 `SKILL.md` §2.1）。

| 英文原名 | 中文正名 | 定义 | 权威位置 |
|---|---|---|---|
| System | 系统 | 被阅读的目标软件整体 | `SKILL.md` §2 |
| Subsystem | 子系统 | 系统内一个可命名的职责划分 | `SKILL.md` §2 |
| Concern | 关注点 | 我为什么关注它（见 §10.1 消歧） | `SKILL.md` §2 |
| Scenario | 场景 | 什么真实事件触发它 | `SKILL.md` §2 |
| Path | 路径 | 它怎么穿过系统 | `SKILL.md` §2 |
| Mechanism | 机制 | 它靠什么机制实现 | `SKILL.md` §2 |
| Entity | 实体 | 由哪些对象承载 | `SKILL.md` §2 |
| Resource | 资源 | 稀缺且需复用/回收的对象 | `knowledge-model.md` §2 |
| State | 状态 | 对象当前处于什么状态 | `knowledge-model.md` §4 |
| Protocol | 协议 | 对象之间必须遵守的交互约定 | `knowledge-model.md` §5 |
| Symbol | 符号 | 哪段代码实现它 | `SKILL.md` §2 |
| Code | 代码 | 最终实现本身 | `SKILL.md` §2 |
| Evidence | 证据 | 这条结论凭什么成立（见 §10.4 消歧） | `SKILL.md` §2 |

跨尺度：**Zoom in**（System → Code）、**Zoom out**（Code → System）、**Sideways**（Entity / Mechanism → 其他 Path、Concern）。

---

## 2. 五类知识

| 英文原名 | 中文正名 | 核心问题 | 主要对象 |
|---|---|---|---|
| Structure | 结构 | 系统由什么组成 | Architecture、Subsystem、Entity、Relation |
| Behavior | 行为 | 系统怎么运行 | Scenario、Path、Flow、State、Lifecycle、Concurrency、Data Path |
| Constraint | 约束 | 什么规则不能破 | Invariant、Protocol、Precondition、Ownership、Ordering、Cleanup |
| Evidence | 证据 | 凭什么相信 | Claim、Evidence、SourceAnchor、Conflict |
| Evolution | 演化 | 这个知识怎么随系统变化 | Version、BuildContext、Case、Rule、ChangeImpact |

口诀：**谁组成 → 怎么动 → 不许怎样 → 凭什么 → 怎么变。**

---

## 3. 行为与约束

| 英文原名 | 中文正名 | 定义 |
|---|---|---|
| Flow | 流程 | 带时间顺序的操作路径：入口、判断、分支、副作用、出口 |
| State | 状态 | 由条件 + 迁移 + 迁移条件组成；可由多个字段联合编码 |
| Lifecycle | 生命周期 | `create → initialize → publish → acquire/use → release → destroy` |
| Data Path | 数据路径 | `producer → representation → transformation → consumer` |
| Concurrency | 并发 | 谁共享、谁保护、谁等待 |
| Invariant | 不变量 | 任何时刻都必须成立的条件 |
| Ownership | 归属 | 谁负责释放；与「指向」不是一回事 |
| Ordering | 次序 | 谁必须先于谁 |

---

## 4. 证据与可追溯

| 英文原名 | 中文正名 | 定义 | 权威位置 |
|---|---|---|---|
| Claim | 结论 | 一条人类可读的断言，不等于源码行 | `knowledge-model.md` §6 |
| Evidence | 证据 | 支撑 Claim 的源码/文档/分析/运行时/测试事实 | `SKILL.md` §8.1 |
| Source Anchor | 源码锚点 | 结论定位到源码的最小坐标 | `SKILL.md` §8.2 |
| Conflict | 冲突 | 两处证据互相矛盾，不得强行调和 | `SKILL.md` §9.5 |
| Trace | 追踪 | 从 Claim 走到 Evidence 的过程 | `tracing/trace-policy.md` |
| `trace_boundary` | 追踪边界 | 有意停止追踪的位置及理由 | `SKILL.md` §6 Stage 4 |
| `open_question` | 未解问题 | 待消解或细化的疑问；每次探索至少消掉一个 | `tracing/exploration-policy.md` |

**Source Anchor 优先使用**：`repository + revision` / `path` / `qualified symbol` / `field / expression` / `code region`。行号只是导航辅助，不能作为唯一身份。

**置信度类型**

| 英文原名 | 中文正名 | 含义 |
|---|---|---|
| `FACT` | 事实 | 源码直接表明 |
| `INFERENCE` | 推断 | 由多个事实稳定推出 |
| `INTERPRETATION` | 解读 | 合理但证据不完整；**绝不能表述成 `FACT`** |
| `UNVERIFIED` | 未验证 | 证据不足；须继续追踪、降级限定或删除 |

**追踪深度**

| 标识 | 定义 |
|---|---|
| `D1 Local` | 局部事实 |
| `D2 Structural` | 跨符号语义 |
| `D3 System` | 架构/运行时解释 |

结论尺度与追踪深度必须匹配。

---

## 5. 模式与表达

| 英文原名 | 中文正名 | 定义 |
|---|---|---|
| Pattern | 理解模式 | **理解问题的分类，不是图的分类**。九种：Structural / Lifecycle / Flow / State / Concurrency / Data Path / Resource / Recovery / Architecture |
| Dominant Pattern | 主导模式 | 恰好一个；由「哪个问题最决定该知识如何被理解」决定，不由关键字或你会画哪种图决定 |
| Representation Family | 表达族 | 读者缺哪种关系（见 `SKILL.md` §7.2） |
| Renderer | 渲染器 | 具体出图工具（Mermaid / PlantUML / Graphviz…） |
| View | 视图 | 模型的一次投影；投影可以重画，模型不能丢 |

表达选择永远是：**核心问题 → 主导模式 → 表达族 → 具体方法 → 渲染器 / 工具**（语义在前，渲染器在后）。

**图 / 文 / 代码的分工**：图 → 空间与时间关系；文 → 语义、条件、后果；代码 → 证据与导航。

---

## 6. 执行与闸门

| 英文原名 | 中文正名 | 定义 |
|---|---|---|
| Stage | 阶段 | 六阶段推理：Scope & Explore / Knowledge Model / Pattern Recognition / Traceability / Representation & Doc / Validation |
| Gate | 闸门 | 进出控制：Gate 0 Scope → Gate 6 Validate |
| `L0–L3` | 深度等级 | 理解深度（见 §10.2 消歧） |
| Mode | 模式 | Explore / Model / Document / Review / Evolve |

**六阶段 × 七道闸门**：六阶段解决「现在要做哪类思考」，七闸门解决「做到什么程度才准继续、什么时候停」。

**Modes 分工**

| Mode | 做什么 |
|---|---|
| Explore | 只调查源码与架构，不急于生成最终文档 |
| Model | 建立或更新 canonical knowledge model |
| Document | 从已经验证的模型投影成文档 |
| Review | 从源码、架构、Claim、Representation、Navigation 等维度审计已有文档 |
| Evolve | 分析复核失败，生成候选规则与回归；**不得自动升级规范规则** |

---

## 7. 校验

| 标识 | 检查什么 |
|---|---|
| `V1 Structural` | 结构 |
| `V2 Semantic` | 语义 |
| `V3 Traceability` | 可追溯性 |
| `V4 Representation` | 表达 |
| `V5 Reader / Navigation` | 读者 / 导航 |
| `V6 Architecture Consistency` | 架构一致性 |

失败后回到**最早受影响的最小阶段**，不要整篇盲目重生成。

---

## 8. 演进

| 英文原名 | 中文正名 | 定义 |
|---|---|---|
| merge | 增量合并 | 版本演进的默认方式 |
| rewrite | 重写 | 默认禁止；需记录 `reason / replacement / regression_evidence / approved` |
| Case | 病例 | 一次可复用的失败/成功样本 |
| Candidate Rule | 候选规则 | 由病例归纳、尚未升级为规范的规则 |
| Regression | 回归 | 用 Gold Case 验证改动没有打破既有能力 |
| `L1–L4` | 演进四级 | 见 §10.2 消歧 |

**演进四级**：`L1` 当前任务就地修正 → `L2` 可复用病例 → `L3` 候选规则 → `L4` 已采纳规范变更。只有 `L4` 才改变规范。

---

## 9. 情境化知识

一条结论必须能回答「针对哪个版本/构建/场景」：`Version / Revision`、`Build / Configuration`、`Performance Concern`、`Decision / Rationale`、`Learning Path`、`Conflict`、`Change Impact`。

判据：`Code exists ≠ Code compiled ≠ Code reachable ≠ Code active`。

---

## 10. 易混术语消歧

### 10.1 `Concern` 的四种角色

同一个词在四类位置出现，**含义不同**，读到时先判断是哪一个：

| 角色 | 中文正名 | 出现位置 | 含义 |
|---|---|---|---|
| 坐标层 | 关注点 | `SKILL.md` §2 Cognitive Spine | 我为什么关注这个子系统 |
| 架构实体 | 关注点 | `knowledge-model.md` §2 | 架构模型里的一类节点 |
| 横切关注点 | 横切关注点 | `SKILL.md` §3 Atlas、ISO 42010 | 跨越多个子系统的关注面 |
| 性能关注点 | 性能关注点 | `SKILL.md` §9.2 | 对数据库/OS/存储，性能本身是一等上下文 |

写「关注点」时若指后两者，**必须带限定词**（横切 / 性能），不得裸用。

### 10.2 三套 `L` 编号

三套都用 `L`，但轴不同。**看数字就知道是哪一套**：

| 梯子 | 编号范围 | 轴 | 权威位置 |
|---|---|---|---|
| 深度等级 | `L0–L3` | 理解深度 | `SKILL.md` §5 |
| 演进四级 | `L1–L4` | 技能自身的演进等级 | `SKILL.md` §13.1 |
| 上下文扩展顺序 | `C0–C6` | 追一条符号时向外扩多远 | `tracing/exploration-policy.md` |

注：第三套原写作 `L0–L6`，与深度等级撞号（都从 `L0` 起），已改为 `C0–C6`。历史记录文件（`MERGE_DECISION.md`）保留原写法，不回改。

### 10.3 其他易混对

| 易混 | 区别 |
|---|---|
| `Path` ≠ `Flow` | `Path` 是知识对象（一条穿过系统的路线）；`Flow` 是行为类别（一次操作怎么执行） |
| `Pattern` ≠ 图 | `Pattern` 是理解问题的分类；图只是它的投影之一 |
| `Representation Family` ≠ `Renderer` | 前者是「读者缺哪种关系」，后者是出图工具 |
| `Mechanism` ≠ `Entity` | 机制是「靠什么实现」，实体是「由谁承载」 |
| `Evidence` ≠ `Source Anchor` | 证据是事实本身，锚点是它在源码里的坐标 |
| `Claim` ≠ `FACT` | `Claim` 是断言本身，`FACT` 是它的一种类型 |
| `System Atlas` ≠ `Cognitive Spine` | Atlas 是持久架构地基，Spine 是所有知识对象的统一坐标 |
| `State` ≠ `Lifecycle` | 状态是横切快照，生命周期是纵向过程 |
| `Stage` ≠ `Gate` | 阶段是推理分工，闸门是进出条件 |
