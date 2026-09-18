# Pattern Catalog

Patterns describe the **dominant comprehension question**. They do not prescribe a specific diagram language.

## Structural / Topology

Question: Which entities exist and how are they connected?

Strong signals:

- struct/class definitions
- pointer/reference fields
- embedded structures
- containers
- manager/object relationships

Best representations:

- Entity Relationship / Class / Structure Chart
- Management/Ownership graph when responsibility is central

Avoid:

- calling a generic relation graph a Flowchart

## Lifecycle / Ownership

Question: How is an object created, acquired, transferred, released, and destroyed?

Strong signals:

- allocation/free
- constructor/destructor
- palloc/pfree
- retain/release
- refcount
- pin/unpin
- register/unregister

Best representations:

- Lifecycle view
- Ownership graph
- state diagram as secondary

## Flow / Pipeline

Question: How does one operation execute?

Strong signals:

- branch conditions
- main/fallback path
- loops/retries
- cleanup path
- important call chain

Best representations:

- Flowchart
- Activity-style flow
- bounded CFG for deep implementation work

## State Machine

Question: What states exist, how are they represented, and what triggers transitions?

Strong signals:

- state/status field
- flags
- enum + switch
- composite predicates
- state-specific behavior

Best representations:

- State diagram
- state table

## Concurrency / Synchronization

Question: Who shares state, who protects it, who waits, and who wakes?

Strong signals:

- mutex/rwlock/spinlock/LWLock
- atomic/CAS/barrier
- wait queue
- shared/global state
- lock ordering

Best representations:

- protection graph
- sequence diagram
- bounded wait-for/resource graph

## Data Path / Transformation

Question: How does data move and change representation?

Strong signals:

- copy/move/reference
- serialization
- conversion/materialization
- producer/consumer
- buffer handoff

Best representations:

- Data Path
- DFD-style flow
- dataflow graph for deep implementation work

## Resource / Cache / Index

Question: How are many resources found, allocated, reused, evicted, or reclaimed?

Strong signals:

- hash/index
- bucket
- freelist
- cache
- victim/evict
- pool
- lookup/allocate/reclaim

Best representations:

- Resource/Management map
- index map
- lifecycle/state as secondary

## Recovery / Error / Consistency

Question: What happens when the normal path fails, and how is correctness restored?

Strong signals:

- goto cleanup
- rollback
- retry
- recovery/replay
- partial initialization
- transactional undo

Best representations:

- failure/recovery flow
- state diagram if partial states matter

## Architecture / Subsystem Boundary

Question: Where is this module in the system, and what is its interface/dependency boundary?

Strong signals:

- public headers
- module APIs
- callbacks
- registration
- subsystem init/shutdown
- dependency direction

Best representations:

- architecture/component view
- layer view
- dependency graph

## Selection heuristic

1. Identify the Core Question.
2. Identify the dominant knowledge density.
3. Pick one Dominant Pattern.
4. Add only secondary patterns that explain information not covered by the primary view.
5. Select a representation family.
6. Select Mermaid or specialized/manual rendering based on the representation-policy rules.

Do not classify from a keyword alone.

Examples:

```text
struct + pointers + manager
→ likely Structural

struct + malloc/free + refcount
→ Lifecycle/Ownership may dominate

if/switch/loop around one operation
→ Flow

enum + many transition writers + state-specific branches
→ State

lock + shared field + wait queue
→ Concurrency

hash + bucket + victim + reclaim
→ Resource
```

