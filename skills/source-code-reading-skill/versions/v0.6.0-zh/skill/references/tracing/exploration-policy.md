# 探索规范

## 从用户问题开始

不要从通读整个文件开始。先定义精确的问题。

## 搜索顺序

典型顺序：

```text
1. 查找目标符号
2. 阅读定义和局部注释
3. 查找引用
4. 检查关键字段和相关类型
5. 检查直接调用方/被调用方
6. 搜索关键字段的读取方/写入方
7. 根据需要搜索分配/释放或锁/状态操作
8. 只有必要时才跨模块扩展
```

## 上下文扩展

```text
C0 Target symbol（目标符号）
C1 Direct definition（直接定义）
C2 Direct references（直接引用）
C3 Related structures/fields（相关结构/字段）
C4 Relevant control flow（相关控制流）
C5 Runtime/lifecycle/synchronization（运行时/生命周期/同步）
C6 Cross-module（跨模块）
```

不要自动遍历所有层级。

## Open Questions

维护内部列表：

```yaml
open_questions:
  - question:
    importance: high | medium | low
    related_symbols: []
    status: open | investigating | resolved | blocked
```

每次扩展都应该至少关闭或细化一个 open question。

## 冲突处理

当注释/文档与实现看起来不一致时，保留两组证据并标记冲突。不要强行制造虚假的一致。
