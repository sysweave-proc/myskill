# 理解模式 · Pattern 快速入口

Pattern 是“理解问题的分类”，不是“图的分类”。必须先选**恰好一个 dominant pattern**，其他作为 secondary。

| Pattern | 核心问题 |
|---|---|
| Structural | 谁和谁相连？ |
| Lifecycle | 如何创建、持有、释放？ |
| Flow | 一次操作怎么执行？ |
| State | 状态如何迁移？ |
| Concurrency | 谁共享、谁保护、谁等待？ |
| Data Path | 数据怎么移动/变形？ |
| Resource | 稀缺资源如何定位/复用/回收？ |
| Recovery | 失败后怎么恢复？ |
| Architecture | 它在系统哪里？ |

## 选择启发式

```text
核心问题契合度
+ 主导关系密度
+ 时间/控制复杂度
+ 运行时相关性
+ 用户意图
```

不要追求假的数值精度。真正目的只是避免“关键字命中就选模式”。

常见混淆：

```text
Structure Chart ≠ Flowchart
Call Graph ≠ Runtime Flow
State ≠ Lifecycle
DFD ≠ source-level Dataflow
Pointer ≠ Ownership
Lock presence ≠ Concurrency understanding
Directory tree ≠ Architecture
```

完整目录见 `references/patterns/pattern-catalog.md`。
