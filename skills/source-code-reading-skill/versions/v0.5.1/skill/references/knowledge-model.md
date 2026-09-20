# Knowledge Model

## Core entities

- `System`
- `Subsystem`
- `Mechanism`
- `Path`
- `Concern`
- `SourceEntity`: file, symbol, struct, class, function, field, enum, macro, variable.
- `RuntimeEntity`: process, thread, coroutine, buffer, page, request, connection, transaction.
- `Resource`: memory, CPU, lock, FD, buffer, I/O queue, shared memory, NUMA node.
- `State`
- `SourceAnchor`

## Relations

### Structural

```text
contains
embeds
points_to
references
inherits
implements
aliases
```

### Management

```text
manages
owns
allocates
tracks
indexes
registers
queues
```

### Dependency

```text
calls
uses
depends_on
invokes
accesses
modifies
```

### Runtime

```text
produces
consumes
requests
handles
participates_in
```

### Concurrency

```text
protects
synchronized_by
waits_for
competes_for
owns_lock
releases_lock
atomic_update_of
```

### Architecture

```text
contains
refines
realized_by
implemented_by
participates_in
related_through_path
cross_cuts
```

## Behaviors

### Flow

A time-ordered operational path with entry, decisions, branches, effects, and exits.

### State

A condition of an entity plus transitions and conditions. State may be explicit or implicit.

### Lifecycle

Create → initialize → publish → acquire/use → release → destroy, with ownership transfer or deferred reclamation when present.

### Data path

Producer → representation → transformation → consumer, distinguishing copy, move, reference, serialization, materialization, and persistence.

## Constraints

Capture:

```text
precondition
postcondition
invariant
ownership rule
ordering rule
concurrency rule
error/cleanup rule
```

## Claims

A claim is a human-meaningful assertion:

```yaml
claim:
  statement: "..."
  type: FACT | INFERENCE | INTERPRETATION
  confidence: HIGH | MEDIUM | LOW
  evidence: []
  trace: []
  scope: ""
```

## Important modeling rules

1. Pointer ≠ ownership.
2. Pointer ≠ runtime identity unless traced.
3. Lock acquisition ≠ proof of protected state.
4. Enum ≠ complete state machine.
5. Call edge ≠ runtime execution path.
6. Directory adjacency ≠ architectural relationship.
7. Multiple fields can jointly encode state.
8. The same entity can belong to multiple paths and concerns.
9. A graph edge should have semantic direction and relation type.
10. If relation semantics are unknown, use an explicitly weaker relation rather than guessing.
