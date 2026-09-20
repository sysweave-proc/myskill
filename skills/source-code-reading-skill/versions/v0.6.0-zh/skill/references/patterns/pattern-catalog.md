# Pattern 目录

## 主导 Pattern 规则

选择最能回答读者主要问题的 Pattern。次要 Pattern 用于补充它。

| Pattern | 核心问题 | 强信号 | 典型视图 |
|---|---|---|---|
| Structural | 谁/什么彼此连接？ | 类型、字段、容器 | Entity/Relationship、Class、Structure |
| Lifecycle | 对象如何创建/拥有/释放？ | create/free、refcount、pin/unpin | Lifecycle、Ownership |
| Flow | 一个操作如何执行？ | branch、call path、retry | Flowchart、structured flow |
| State | 存在哪些状态，它们如何变化？ | 状态字段、flags、transitions | State Machine |
| Concurrency | 谁共享、谁保护、谁等待？ | lock、atomics、wait queues | Sync、Sequence |
| Data Path | 数据如何移动/变化？ | copy、reference、transform | Dataflow、Data Path |
| Resource | 稀缺状态如何定位/复用/回收？ | pool、cache、eviction、free list | Management/Resource Map |
| Recovery | 失败后发生什么？ | cleanup、rollback、retry | Failure/Recovery Flow |
| Architecture | 它在系统中属于哪里？ | 模块边界、API、Path | Architecture/Layer |

## Pattern 评分启发式

使用定性判断，不要制造虚假的数值精度：

```text
核心问题匹配度
+ 主导关系密度
+ 时间/控制复杂度
+ 运行时相关性
+ 用户意图
```

## 组合示例

```text
TupleTableSlot
  dominant: Lifecycle
  secondary: Structural, Data Path

Buffer Manager
  dominant: Resource
  secondary: Structural, Lifecycle, State, Concurrency

Lock Manager
  dominant: Concurrency
  secondary: Flow, State, Structural, Resource

Architecture overview
  dominant: Architecture
  secondary: Data Path, Runtime, Dependency
```

## 反混淆

```text
Structure Chart  ≠ Flowchart
Call Graph       ≠ Flow
State            ≠ Lifecycle
DFD              ≠ 源码级 Dataflow
Pointer          ≠ Ownership
Lock presence    ≠ 并发理解
Directory tree   ≠ Architecture
```
