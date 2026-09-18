# 理解模式 Catalog

## 主导模式规则

**先选恰好一个主导模式**，其余为次要模式。

选法：哪个问题**最决定这段知识应当怎么被理解**，它就是主导。不是关键词命中，也不是"哪个图我会画"。

> Pattern 是**理解问题的分类**，不是图的分类。
> 先定主导问题，图是后面的事（见 `representation.md`）。

| 模式 | 核心问题 | 强信号 | 典型视图 |
|---|---|---|---|
| Structural | 谁和谁相连？ | 类型、字段、容器 | Entity/Relationship、Class、Structure |
| Lifecycle | 对象如何诞生/被持有/被释放？ | create/free、refcount、pin/unpin | Lifecycle、Ownership |
| Flow | 一次操作怎么执行？ | 分支、调用路径、重试 | Flowchart、结构化流程 |
| State | 有哪些状态、怎么迁移？ | 状态字段、flags、迁移 | State Machine |
| Concurrency | 谁共享、谁保护、谁等待？ | lock、atomic、等待队列 | Sync、Sequence |
| Data Path | 数据怎么移动、怎么变形？ | copy、reference、transform | Dataflow、Data Path |
| Resource | 稀缺状态如何定位/复用/回收？ | pool、cache、eviction、free list | Management/Resource Map |
| Recovery | 失败之后发生什么？ | cleanup、rollback、retry | Failure/Recovery Flow |
| Architecture | 它在系统里处于哪里？ | 模块边界、API、路径 | Architecture/Layer |

## 打分启发式

定性打分，不追求假的数值精度：

```text
核心问题契合度
+ 主导关系密度
+ 时间/控制复杂度
+ 运行时相关性
+ 用户意图
```

## 组合示例

```text
TupleTableSlot
  dominant:  Lifecycle
  secondary: Structural, Data Path

Buffer Manager
  dominant:  Resource
  secondary: Structural, Lifecycle, State, Concurrency

Lock Manager
  dominant:  Concurrency
  secondary: Flow, State, Structural, Resource

架构总览
  dominant:  Architecture
  secondary: Data Path, Runtime, Dependency
```

## 易混淆清单

```text
Structure Chart  ≠ Flowchart
Call Graph       ≠ Flow
State            ≠ Lifecycle
DFD              ≠ 源码级 Dataflow
Pointer          ≠ Ownership
有锁             ≠ 理解了并发
目录树           ≠ 架构
```

这些不是"表述差异"，而是**会把结论带错**的分类错误。每次都回到主导问题重新判定。
