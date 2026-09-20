# 表达选择 · Representation 快速入口

表达选择的顺序不可颠倒：

```text
核心问题
  ↓
主导 Pattern
  ↓
Representation Family
  ↓
具体方法
  ↓
Renderer / Tool
```

## 表达族

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

## 图 / 文 / 代码分工

```text
图   → 空间与时间关系
文   → 语义、条件、后果
代码 → 证据与导航
```

## 渲染器选择

- Mermaid：概念性、小图、希望文本化版本控制；
- Graphviz 等：图较大，布局/连线路由重要；
- AST/CodeQL/静态分析：需要机器精确的 CFG、AST、调用/依赖/数据流；
- 表格/散文：关系很小或画图只会重复文字；
- 手工精修图：几何布局本身就是解释的一部分。

核心视图目标约 5–12 个主要节点，过大就拆 context / core / detail。

完整细节见 `references/representation/representation-policy.md` 与 `references/diagrams/diagram-catalog.md`。
