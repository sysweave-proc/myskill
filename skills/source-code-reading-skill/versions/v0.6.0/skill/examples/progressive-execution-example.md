# Progressive Execution Example

## Topic

PostgreSQL Buffer Lookup

### Gate 0 — Scope

Question: how does a buffer lookup locate the corresponding `BufferDesc` and reach the page?

### Gate 1 — Orient

Locate Buffer Manager, buffer mapping structures, and the read path. Do not yet inspect eviction, WAL, bgwriter, or recovery.

### Gate 2 — Minimum model

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

Dominant: **Resource / Cache / Index**.
Secondary: Structural, Concurrency.

### Gate 4 — Trace

Trace only the key lookup, bucket/partition selection, `BufferDesc` resolution, and page access needed to answer the question.

### Gate 5 — Represent

Use one compact management/resource view plus selected source anchors.

### Gate 6 — Validate

Check that the diagram does not imply ownership or a runtime sequence unsupported by the source.

### Expand only when needed

Only after the central lookup is clear should the agent expand to replacement/victim selection, LWLock partitioning, I/O, or recovery.
