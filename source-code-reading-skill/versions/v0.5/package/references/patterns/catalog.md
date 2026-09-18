# Pattern Catalog

| Pattern | Main question | Typical evidence | Common representation |
|---|---|---|---|
| Structural / Topology | What is connected to what? | structs, pointers, embedded fields, managers | Entity/relationship map |
| Lifecycle / Ownership | Who creates/releases/owns it? | alloc/free, refcount, lifetime states | Lifecycle + ownership map |
| Flow / Pipeline | What happens in what order? | calls, branches, phases | Flow / sequence |
| State Machine | What states/transitions are legal? | state fields + transition writers | State diagram |
| Concurrency | Who protects/waits/orders? | locks, atomics, queues, barriers | Concurrency/sequence |
| Data Path | How does data move/transform? | read/write, buffers, conversions | Data-path diagram |
| Resource / Cache / Index | How is resource found/reused? | hash, buckets, indexes, eviction | Resource map |
| Recovery / Consistency | What happens on failure/recovery? | WAL, rollback, retries, checkpoints | Recovery flow |
| Architecture | Where is the boundary? | APIs, modules, dependencies, paths | Architecture view |

Pattern classification must be driven by the comprehension goal, not by keywords alone.
