# 规范知识模型 · Canonical Knowledge Model

模型的目的是：**让"图、正文、代码"三种表达共享同一份语义**，而不是各说各话。

## 实体

```text
架构实体   System、Subsystem、Mechanism、Path、Concern
源码实体   file、symbol、struct、class、function、field、enum、macro、variable
运行时实体 process、thread、coroutine、buffer、page、request、connection、transaction
资源实体   memory、CPU、lock、FD、buffer、I/O queue、shared memory、NUMA node
状态实体   State
证据实体   SourceAnchor
```

## 关系：必须带方向与语义类型

| 类别 | 关系 |
|---|---|
| Structural | `contains` `embeds` `points_to` `references` `inherits` `implements` `aliases` |
| Management | `manages` `owns` `allocates` `tracks` `indexes` `registers` `queues` |
| Dependency | `calls` `uses` `depends_on` `invokes` `accesses` `modifies` |
| Runtime | `produces` `consumes` `requests` `handles` `participates_in` |
| Concurrency | `protects` `synchronized_by` `waits_for` `competes_for` `owns_lock` `releases_lock` `atomic_update_of` |
| Architecture | `contains` `refines` `realized_by` `implemented_by` `participates_in` `related_through_path` `cross_cuts` |

**语义未知时用更弱的关系，而不是猜一个更强的关系。** 宁可写 `references`，不要写 `owns`。

## 行为

### Flow 流程
带时间顺序的操作路径：入口、判断、分支、副作用、出口。

### State 状态
某个实体的条件 + 迁移 + 迁移条件。**状态可以是显式的（状态字段），也可以是隐式的（多个字段联合编码）。**

### Lifecycle 生命周期
`create → initialize → publish → acquire/use → release → destroy`，有所有权转移或延迟回收时要标出来。

### Data Path 数据路径
`producer → representation → transformation → consumer`，并区分 copy / move / reference / serialization / materialization / persistence。

## 约束

```text
precondition
postcondition
invariant
ownership rule
ordering rule
concurrency rule
error/cleanup rule
```

大型系统最值得记的往往不是某条 Claim，而是这些**不变量与协议**：

```text
Buffer: pin > 0        → 不能被回收
Lock:   持有 L1        → 不能再获取 L0
Memory: free           → 不允许再访问
Commit: 提交前         → WAL 约束必须满足
```

它们应当是一等知识对象（`Invariant` / `Protocol`），不是正文里的一个段落。

## 结论 Claim

一条人类可读的断言，而不是源码行：

```yaml
claim:
  statement: "..."
  type: FACT | INFERENCE | INTERPRETATION
  confidence: HIGH | MEDIUM | LOW
  evidence: []
  trace: []
  scope: ""
```

## 建模规则

1. 指针 ≠ ownership。
2. 指针 ≠ 运行时同一性（除非追过）。
3. 获得锁 ≠ 证明了被保护的状态。
4. enum ≠ 完整状态机。
5. 调用边 ≠ 运行时执行路径。
6. 目录相邻 ≠ 架构关系。
7. 状态可以由多个字段联合编码。
8. 同一实体可以属于多条 Path 和多个 Concern。
9. 图的每条边都要有语义方向与关系类型。
10. 关系语义未知时用更弱的关系，不要猜。
