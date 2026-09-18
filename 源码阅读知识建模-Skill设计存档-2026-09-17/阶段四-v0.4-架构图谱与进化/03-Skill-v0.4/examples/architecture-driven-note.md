# Buffer Lookup：从系统架构到源码

> **Core Question**：BufferTag 如何在 PostgreSQL Storage 中定位到对应的 BufferDesc？

## 系统位置

```text
PostgreSQL
  → Storage
    → Page Read Path
      → Buffer Lookup
```

## 一句话模型

Buffer Lookup 是 Page Read Path 中把逻辑 page identity 映射到具体 buffer metadata 的资源定位机制；理解它首先需要看 `BufferTag`、mapping structure 和 `BufferDesc` 的关系，再进入 hash/partition 的实现细节。

## 主视图：Management / Resource

```mermaid
flowchart LR
    Tag[BufferTag] -->|identity / hash| Table[BufTable]
    Table -->|locates| Desc[BufferDesc]
    Desc -->|represents| Buffer[Shared Buffer]
```

## 源码导读

```text
Buffer lookup concept
  → BufferTag
  → BufTable / hash helper
  → BufferDesc
  → ReadBuffer / allocation path
```

注意：图中只表达理解该问题所需的关系，不把完整 call graph 塞进主视图。

