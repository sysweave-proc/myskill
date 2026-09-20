# Source Code Reading Skill v0.6.0

这是对 `source-code-reading-skill-v0.5.1` 与再表达件的**增量合并版**。

核心决策不是“二选一”，而是：

```text
v0.5.1
= 完整工程资产、历史演进、知识源、案例、回归、图法、验证、模板与测试

再表达件
= 更强的认知骨架、五类知识、Cognitive Spine、六阶段×七闸门、L0–L3、模式先于表达、情境化知识

                 ↓ 合并

v0.6.0
= 一个完整、可执行、可追溯、可回归、可持续演进的源码阅读 Skill
```

## 本版的核心原则

### 1. 一个模型，多个视图

Canonical Knowledge Model 是长期资产；Markdown、Mermaid、Graphviz、表格和代码只是投影。

### 2. 五类知识

```text
Structure → Behavior → Constraint → Evidence → Evolution
```

版本、构建、性能、决策、学习路径、冲突和变更影响作为情境附着在这五类知识上。

### 3. 唯一认知坐标

```text
System
 → Subsystem
 → Concern
 → Scenario
 → Path
 → Mechanism
 → Entity / Resource
 → State / Protocol
 → Symbol
 → Code
 → Evidence
```

源码天然是图，因此同时支持 zoom in / zoom out / sideways。

### 4. 六阶段 × 七道闸门

```text
Scope & Explore
→ Knowledge Model
→ Pattern Recognition
→ Traceability
→ Representation & Document
→ Validation
```

闸门负责防止过度阅读、过度建模和无目的加深。

### 5. Pattern 先于 Representation

先问“我需要理解什么关系”，再选表达族，再选具体方法和渲染器；图不是默认产物。

### 6. Claim 必须可回源

```text
Claim → Evidence → Source Anchor → Trace
```

并区分 `FACT / INFERENCE / INTERPRETATION`、`SUPPORTED / PARTIALLY_SUPPORTED / UNVERIFIED / CONFLICTING`。

### 7. Skill 自己也必须可演进

```text
反馈 → 失败分类 → Case → Candidate Rule
→ Regression → Approval → Adopted Rule
```

新版本默认是 merge，不是 rewrite；任何删除必须留下证据。

## 目录

```text
SKILL.md                              核心操作协议
MERGE_DECISION.md                    两套 Skill 的完整合并决策记录

references/
  architecture-model.md              架构模型与坐标
  architecture-reconstruction.md    架构重构方法
  architecture-atlas.md              Atlas 操作卡（新增）
  knowledge-model.md                规范知识模型
  situated-knowledge.md             活系统情境维度（新增）
  patterns/pattern-catalog.md       理解模式
  patterns.md                       模式快速入口（新增）
  representation/representation-policy.md
  representation.md                 表达选择快速入口（新增）
  diagrams/diagram-catalog.md       历史图法与语义目录（完整保留）
  tracing/
  validation/
  document-policy.md
  execution-progressive.md
  extension-boundary.md

knowledge-sources/                  外部“老师”与权威边界

evolution/                         案例、规则、回归、版本非回归
  anti-patterns/
  capability-inventory.md
  case-learning.md
  feedback-taxonomy.md
  rule-proposal.md
  regression.md
  baseline-policy.md
  evolution-policy.md

cases/                              gold / failure
examples/                           示例资产

templates/                          文档、知识模型、review、反馈、演进模板
tests/                              完整性与合并后能力检查
```

## 与两个来源的关系

### 从 v0.5.1 保留并继续增强

包括 System Atlas、架构重构、完整知识模型、完整图法目录、表示策略、追踪、验证、文档政策、知识源注册、gold/failure case、anti-pattern、feedback taxonomy、rule proposal、regression、baseline/evolution policy、模板、示例和完整性测试。

### 从再表达件吸收并整合

包括五类知识、Cognitive Spine、六阶段×七闸门、L0–L3、主导模式唯一性、语义先于渲染器、Situated Knowledge、Conflict、Learning Path、Change Impact，以及更严格的“关系语义未知时降级而不是猜测”的建模纪律。

### 本版刻意没有做的事

没有把两个 Skill 的重复页面机械复制成两个平行规范；重复内容已经收敛为单一规范，必要时用“快速入口/操作卡”保留易用性。

## 最重要的验证目标

后续每次演进都应证明两件事：

```text
A. 新能力真的被增加/修正；
B. 旧能力没有因为“重新组织”而消失。
```

详见 `MERGE_DECISION.md` 与 `evolution/baseline-policy.md`。
