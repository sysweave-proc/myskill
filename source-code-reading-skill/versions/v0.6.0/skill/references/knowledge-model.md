# 规范知识模型 · Canonical Knowledge Model

模型的目标是：**让图、正文、代码共享一份语义**。文档不是模型本身，而是模型的视图。

## 1. 五类知识

| 维度 | 核心问题 | 主要对象 |
|---|---|---|
| Structure | 系统由什么组成 | Architecture、Subsystem、Entity、Relation |
| Behavior | 系统怎么运行 | Scenario、Path、Flow、State、Lifecycle、Concurrency、Data Path |
| Constraint | 什么规则不能破 | Invariant、Protocol、Precondition、Ownership、Ordering、Cleanup |
| Evidence | 凭什么相信 | Claim、Evidence、SourceAnchor、Conflict |
| Evolution | 怎么随源码/反馈变化 | Version、BuildContext、Case、Rule、ChangeImpact |

## 2. 实体

```text
架构实体   System、Subsystem、Mechanism、Path、Concern
源码实体   file、symbol、struct、class、function、field、enum、macro、variable
运行时实体 process、thread、coroutine、buffer、page、request、connection、transaction
资源实体   memory、CPU、lock、FD、buffer、I/O queue、shared memory、NUMA node
状态实体   State
证据实体   SourceAnchor
```

## 3. 关系：必须有方向与语义

| 类别 | 关系 |
|---|---|
| Structural | `contains` `embeds` `points_to` `references` `inherits` `implements` `aliases` |
| Management | `manages` `owns` `allocates` `tracks` `indexes` `registers` `queues` |
| Dependency | `calls` `uses` `depends_on` `invokes` `accesses` `modifies` |
| Runtime | `produces` `consumes` `requests` `handles` `participates_in` |
| Concurrency | `protects` `synchronized_by` `waits_for` `competes_for` `owns_lock` `releases_lock` `atomic_update_of` |
| Architecture | `contains` `refines` `realized_by` `implemented_by` `participates_in` `related_through_path` `cross_cuts` |

**语义未知时使用更弱的关系，而不是猜测更强关系。** 例如只证明有指向，不足以写 `owns` 时可以写 `points_to` / `references`。

## 4. 行为

### Flow

带时间顺序的操作路径：入口、判断、分支、副作用、出口。

### State

状态由条件 + 迁移 + 迁移条件组成。状态既可以显式编码，也可以由多个字段联合编码。

### Lifecycle

```text
create → initialize → publish → acquire/use → release → destroy
```

需要时标记 ownership transfer、refcount、延迟回收等事实。

### Data Path

```text
producer → representation → transformation → consumer
```

重要时区分 copy / move / reference / serialization / materialization / persistence。

## 5. 约束

```text
precondition
postcondition
invariant
ownership rule
ordering rule
concurrency rule
error/cleanup rule
```

不变量和协议应是一等知识对象，而不是藏在正文里。例如：

```text
Buffer: pin > 0       → 不能被回收
Lock:   持有 L1       → 不能再获取 L0
Memory: free          → 不允许再访问
Commit: 提交前         → WAL 约束必须满足
```

## 6. Claim

```yaml
claim:
  statement: "..."
  type: FACT | INFERENCE | INTERPRETATION
  confidence: HIGH | MEDIUM | LOW
  evidence: []
  trace: []
  scope: ""
```

Claim 是人类可读断言，不等于源码行。

## 7. 建模不变量

1. Pointer ≠ ownership。
2. Pointer ≠ runtime identity，除非追过。
3. Lock acquisition ≠ proof of protected state。
4. enum ≠ complete state machine。
5. Call edge ≠ runtime execution path。
6. Directory adjacency ≠ architecture。
7. 状态可以由多个字段联合编码。
8. 一个实体可以属于多条 Path 和多个 Concern。
9. 每条图边必须有方向和关系类型。
10. 不确定时宁可弱关系，不要强猜。
