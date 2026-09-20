# 反模式：Pointer 就意味着 Ownership

**症状：** 把 `A *b` 直接表示成 `A owns B`。

**修复：** 在断言 ownership 之前，追踪分配、生命周期、释放、转移和引用约定。
