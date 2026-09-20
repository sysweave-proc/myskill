# Pattern Catalog

## Dominant-pattern rule

Choose the pattern that best answers the reader's main question. Secondary patterns support it.

| Pattern | Core question | Strong signals | Typical views |
|---|---|---|---|
| Structural | Who/what is connected? | types, fields, containers | Entity/Relationship, Class, Structure |
| Lifecycle | How is an object born/owned/released? | create/free, refcount, pin/unpin | Lifecycle, Ownership |
| Flow | How does an operation execute? | branch, call path, retry | Flowchart, structured flow |
| State | What states exist and how do they change? | state fields, flags, transitions | State Machine |
| Concurrency | Who shares, protects, waits? | lock, atomics, wait queues | Sync, Sequence |
| Data Path | How does data move/change? | copy, reference, transform | Dataflow, Data Path |
| Resource | How is scarce state located/reused/reclaimed? | pool, cache, eviction, free list | Management/Resource Map |
| Recovery | What happens after failure? | cleanup, rollback, retry | Failure/Recovery Flow |
| Architecture | Where does this fit in the system? | module boundary, APIs, paths | Architecture/Layer |

## Pattern scoring heuristics

Use qualitative scoring, not fake numerical precision:

```text
core-question fit
+ dominant relation density
+ temporal/control complexity
+ runtime relevance
+ user intent
```

## Combination examples

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

## Anti-confusions

```text
Structure Chart  ≠ Flowchart
Call Graph       ≠ Flow
State            ≠ Lifecycle
DFD              ≠ source-level Dataflow
Pointer          ≠ Ownership
Lock presence    ≠ Concurrency understanding
Directory tree   ≠ Architecture
```
