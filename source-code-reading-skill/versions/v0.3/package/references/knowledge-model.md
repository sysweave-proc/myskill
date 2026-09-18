# Knowledge Model

## Core entities

- Source Entity: file, symbol, struct, class, function, field, enum, macro, variable.
- Runtime Entity: process, thread, coroutine, buffer, page, request, connection, transaction.
- Resource: memory, CPU, lock, file descriptor, buffer, I/O queue, shared memory, NUMA node.
- Subsystem: manager or architectural component spanning multiple source symbols.

## Core relations

Structural:

```text
contains / embeds / points_to / references / inherits / implements / aliases
```

Management:

```text
manages / owns / allocates / tracks / indexes / registers / queues / dispatches
```

Dependency:

```text
calls / uses / depends_on / invokes / accesses / modifies
```

Runtime:

```text
producer_of / consumer_of / request_to / handled_by / associated_with
```

Concurrency:

```text
protects / synchronized_by / waits_for / competes_for / owns_lock / releases_lock / atomic_update_of
```

## Behaviors

### Flow

A time-ordered operational path with entry, decisions, branches, effects and exits.

### State

An object condition plus transitions and transition conditions. Include implicit states derived from combinations of fields/flags when evidence supports them.

### Lifecycle

Creation, initialization, publication, acquisition/use, release, and destruction. Track ownership transfer and deferred release when relevant.

## Constraints

Capture:

- preconditions;
- postconditions;
- invariants;
- ordering rules;
- ownership rules;
- concurrency rules;
- error/cleanup rules.

## Claims

A claim is a human-meaningful assertion about the source or its behavior.

Each important claim carries:

```text
statement
claim type
confidence
supporting evidence
optional trace
scope
```

## Modeling rules

1. A pointer proves a pointer relation, not ownership.
2. A lock call proves synchronization activity, not what it protects; protection target must be traced.
3. An enum proves named states exist, not that the complete state machine is known.
4. A call edge proves a potential code dependency, not necessarily a single runtime path.
5. Multiple fields may jointly encode an implicit state.
6. Management structures should be modeled as resources when they control allocation/reuse/eviction/reclamation.
7. Keep source names intact for navigation.
