# v0.6.0 合并决策记录

## 0. 决策目标

目标不是得到“更短”或“更漂亮”的 SKILL.md，而是把两个已经形成不同强项的版本合成**一套长期可演进的源码阅读 Agent Skill**：

- 有清晰、可执行的认知协议；
- 有完整、可持续的知识资产；
- 有证据与回源码能力；
- 能控制阅读深度，避免 Agent 无限制扩张；
- 能通过案例与回归持续变强；
- 后续版本不能再次因为重写而丢历史能力。

## 1. 输入资产

### A. `source-code-reading-skill-v0.5.1`

定位：**工程母版**。

它最强的是资产完整度与演进纪律，已有：

- System Atlas / architecture model / reconstruction；
- canonical knowledge model；
- 完整 pattern catalog；
- representation policy + diagram catalog；
- tracing / claim verification / exploration policy；
- validation V1–V6；
- document policy；
- knowledge-sources 注册表、advisor、selection matrix；
- gold / failure cases；
- anti-patterns、feedback taxonomy、rule proposal；
- regression 与 baseline / evolution policy；
- templates / examples / integrity test；
- EVOLUTION_AUDIT 与历史回归背景。

### B. `skill-ds`

定位：**认知与执行协议的强化版**。

它最强的部分是：

- 五类知识：Structure / Behavior / Constraint / Evidence / Evolution；
- Cognitive Spine；
- “一份模型，多种视图”作为唯一操作原则；
- 六阶段 × 七道闸门；
- L0–L3 progressive depth；
- 主导 Pattern 唯一化；
- 语义 → 表达族 → 方法 → 渲染器；
- Situated Knowledge；
- learning path / conflict / change impact；
- 更明确的“关系语义不确定时使用弱关系，不猜强语义”；
- merge-not-rewrite 进一步强化为认知级不变量。

## 2. 核心决策

### 决策 A：以 v0.5.1 作为文件资产基线

原因：它已经经历过一次真实的“精简重建导致回归”教训，并建立了能力清单、基线、完整性测试和显式移除协议。

因此 v0.6.0 不是在 `skill-ds` 的 12 个文件基础上重新搭包，而是从完整的 v0.5.1 资产集增量演进。

### 决策 B：以 skill-ds 的 Cognitive Core 重构 SKILL.md

v0.5.1 的思想是完整的，但核心入口仍然偏“工程手册”；skill-ds 对 Agent 的执行心智模型更清晰。

因此 v0.6.0 的 `SKILL.md` 以：

```text
五类知识
→ Cognitive Spine
→ System Atlas
→ 六阶段 × 七闸门
→ L0–L3
→ Pattern
→ Traceability
→ Representation
→ Validation
→ Evolution
```

作为主轴。

### 决策 C：不抛弃 v0.5.1 的“深资产”

skill-ds 把部分历史材料压缩成原则，这对 Agent 入口有利，但如果直接替换，会丢掉：

- 完整图法语义区分；
- 知识源注册与查询策略；
- 详细 tracing / validation / document policy；
- cases / anti-patterns / regression；
- templates / examples / tests。

因此这些全部继续保留，并把 skill-ds 的原则嵌入相应规范文件。

### 决策 D：重复内容不“双轨运行”

不能形成：

```text
representation.md      ← 一套规则
representation-policy  ← 另一套规则
```

这种双规范会逐渐漂移。

处理方式：

- `references/representation/representation-policy.md` 等保持为**规范详情**；
- `references/representation.md` 只作为**快速入口/决策卡**；
- `references/patterns/pattern-catalog.md` 是完整模式规范；
- `references/patterns.md` 是快速入口；
- `references/situated-knowledge.md` 单独成为情境知识规范，因为这是 skill-ds 真正新增的一块能力。

### 决策 E：图法目录不压缩

skill-ds 对历史图法采取了收敛，但 v0.5.1 中已经有完整 `references/diagrams/diagram-catalog.md`。为了“不丢东西”的目标，本次不删除它。

新的规则只负责回答：

```text
何时需要这种语义？
何时不需要？
为什么选这种表达族？
```

而详细图法目录继续作为可查询资产。

### 决策 F：把“情境”提升到正式知识附着层

版本、构建、性能、决策、学习路径、冲突、变更影响容易被普通源码笔记丢掉，但对 PostgreSQL / Linux / 存储系统尤其重要。

因此新增并保留 `references/situated-knowledge.md`，并把它放入核心执行协议，而不是作为可选附录。

### 决策 G：把“演进”视为 Skill 的运行时闭环

v0.5.1 已有 evolution 资产，skill-ds 又进一步把它明确成：

```text
L1 correction
→ L2 case
→ L3 candidate rule
→ L4 adopted rule
```

本版继续强化这一边界：**Agent 可以提案，不能静默改规范。**

## 3. 冲突处理规则

### 3.1 双方都表达了同一原则

采用更完整、可执行、可验证的版本，不重复保留两套定义。

### 3.2 v0.5.1 有细节、skill-ds 有更强抽象

采用：

```text
skill-ds 抽象
+
v0.5.1 具体资产
```

例如：

```text
“语义先于渲染器”
    ↓
representation-policy 的完整表达族 + renderer 取舍
```

### 3.3 skill-ds 有新增能力、v0.5.1 没有

直接增量加入，不回写成含糊的大段原则。

典型：Situated Knowledge。

### 3.4 v0.5.1 有历史资产、skill-ds 没有

默认保留，不因为“当前文档没直接引用”就认为可以删除。

## 4. 非回归核对清单

### Core reasoning

- [x] 一份模型、多种视图
- [x] Architecture foundation
- [x] Canonical Knowledge Model
- [x] Cognitive Spine
- [x] 五类知识
- [x] 六阶段
- [x] 七道闸门
- [x] L0–L3
- [x] Dominant Pattern
- [x] Representation decision pipeline
- [x] Claim → Evidence → Source Anchor
- [x] FACT / INFERENCE / INTERPRETATION
- [x] V1–V6 validation

### Knowledge assets

- [x] architecture-model
- [x] architecture-reconstruction
- [x] diagram catalog
- [x] document policy
- [x] exploration policy
- [x] tracing policies
- [x] validation policy
- [x] knowledge-source registry
- [x] resource advisor
- [x] selection matrix
- [x] templates
- [x] examples

### Evolution assets

- [x] gold cases
- [x] failure cases
- [x] anti-patterns
- [x] feedback taxonomy
- [x] rule proposal
- [x] regression policy
- [x] baseline policy
- [x] capability inventory
- [x] integrity test
- [x] explicit removal records

### 新增/增强

- [x] Situated Knowledge
- [x] Build Context
- [x] Performance Concern
- [x] Decision / Rationale / Evidence
- [x] Learning Path
- [x] Conflict preservation
- [x] Change Impact
- [x] Cognitive Spine as continuous-scale rule
- [x] Weaker-relation fallback
- [x] Explicit “no unresolved question, no deeper trace” rule

## 5. 版本决策

版本：`0.6.0`

理由：相对于 v0.5.1，增加了实质性的认知模型能力与新的正式 reference 资产，属于一个兼容既有能力的 minor evolution，而不是 corrective-only patch。

## 6. 后续演进规则

以后再修改这个 Skill 时，不要直接重写 `SKILL.md` 再“补回文件”。正确流程固定为：

```text
Baseline release
→ Capability inventory
→ Define one concrete improvement
→ Modify the smallest affected assets
→ Run integrity regression
→ Run semantic regression
→ Record approved changes
→ Update changelog
→ Release
```

任何“重新组织后顺便删掉一些旧东西”的动作，都应该先被当作潜在 regression，而不是默认重构。
