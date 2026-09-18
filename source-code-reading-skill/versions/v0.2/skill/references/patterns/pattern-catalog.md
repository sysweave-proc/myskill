# Pattern Catalog

## P1 Structural / Topology

Core question: what are the important objects and how are they organized?

Signals:

- struct/class definitions;
- pointer/embedded fields;
- lists, trees, hash tables, registries;
- manager-to-object relationships.

Primary representation: Entity Relationship.

## P2 Lifecycle / Ownership

Core question: where does an object come from, who holds it, and when is it no longer valid?

Signals:

- alloc/free;
- ctor/dtor;
- retain/release;
- pin/unpin;
- register/unregister;
- reference counts;
- deferred/free-on-release patterns.

Primary representation: Lifecycle.

## P3 Flow / Pipeline

Core question: what happens during one operation?

Signals:

- call chains;
- branch conditions;
- loops/retries;
- callbacks;
- cleanup/return paths.

Primary representation: Flow.

## P4 State Machine

Core question: what states exist and what causes transitions?

Signals:

- state/status fields;
- enums plus switch cases;
- flag combinations;
- state checks and state writers.

Primary representation: State Transition.

## P5 Concurrency / Synchronization

Core question: who accesses shared state, who protects it, and who can wait for whom?

Signals:

- locks/atomics;
- shared globals;
- wait queues;
- wakeups;
- lock ordering;
- memory barriers;
- RCU/lock-free constructs.

Primary representation: Synchronization.

## P6 Data Path / Transformation

Core question: where does data come from, how is it transformed, and where does it go?

Signals:

- copy/move/reference;
- encode/decode;
- materialization;
- serialization;
- cache handoff;
- persistence/output.

Primary representation: Data Path.

## P7 Resource / Cache / Index

Core question: how are large numbers of resources located, allocated, reused, evicted or reclaimed?

Signals:

- hash/index lookup;
- pools;
- free lists;
- victim selection;
- LRU/clock;
- cache hit/miss;
- reclaim.

Primary representation: Management / Resource.

## P8 Recovery / Error / Consistency

Core question: what happens after partial failure, and how is correctness preserved?

Signals:

- error returns;
- goto cleanup;
- rollback;
- retry;
- replay;
- abort/recovery;
- consistency checks.

Primary representation: Failure / Recovery.

## P9 Architecture / Subsystem Boundary

Core question: where does this subsystem sit and how does it interact with neighboring layers?

Signals:

- public headers/APIs;
- opaque types;
- callbacks;
- registration;
- module init/shutdown;
- cross-module dependencies.

Primary representation: Architecture / Layer.

## Dominant pattern rule

Choose one dominant pattern by asking which question, if left unanswered, would make the rest of the chapter hard to understand.

Use secondary patterns only when they materially support the dominant mental model.
