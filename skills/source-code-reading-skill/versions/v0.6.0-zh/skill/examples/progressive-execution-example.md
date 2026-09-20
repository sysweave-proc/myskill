# 渐进式执行示例

## 主题

PostgreSQL Buffer Lookup

### Gate 0 — Scope

问题：Buffer Lookup 如何定位对应的 `BufferDesc`，并最终访问页面？

### Gate 1 — Orient

定位 Buffer Manager、buffer mapping 结构以及读取路径。暂时不要检查 eviction、WAL、bgwriter 或 recovery。

### Gate 2 — Minimum Model

```text
Buffer Manager
  ↓
Buffer Mapping / hash partition
  ↓
BufferDesc
  ↓
shared buffer page
```

### Gate 3 — Pattern

主导模式：**Resource / Cache / Index**。
次要模式：Structural、Concurrency。

### Gate 4 — Trace

只追踪回答当前问题所需的关键 lookup、bucket/partition 选择、`BufferDesc` 定位以及页面访问。

### Gate 5 — Represent

使用一个紧凑的管理/资源视图，并配合选定的 Source Anchor。

### Gate 6 — Validate

检查图是否暗示了源码并未支持的 ownership 或 runtime sequence。

### 仅在需要时扩展

只有在核心 lookup 已经清楚之后，Agent 才应该继续扩展到 replacement/victim selection、LWLock partitioning、I/O 或 recovery。
