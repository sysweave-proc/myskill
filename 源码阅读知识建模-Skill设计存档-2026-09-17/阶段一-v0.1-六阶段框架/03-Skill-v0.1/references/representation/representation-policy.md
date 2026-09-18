# Representation Policy

## Purpose

Choose the smallest set of views that makes the core knowledge easy to understand and trace.

## Primary view mapping

```text
Structural   → Entity Relationship
Lifecycle    → Lifecycle
Flow         → Flow
State        → State Transition
Concurrency  → Synchronization
Data Path    → Data Path
Resource     → Management / Resource
Recovery     → Failure / Recovery
Architecture → Architecture / Layer
```

## Secondary view rules

Use 0–2 secondary views by default. Add more only when a real comprehension gap remains.

Examples:

```text
Structural  + Lifecycle
    → Entity Relationship + Lifecycle

Concurrency + Flow + State
    → Synchronization + Flow + State Transition

Resource + Structural + Concurrency
    → Management + Entity Relationship + Synchronization
```

## View selection rules

### Entity Relationship

Use when the reader needs to see “who points to/contains/manages whom”.

### Management / Ownership

Use when the key issue is responsibility for allocation/reuse/reclamation.

### Flow

Use when the reader needs the operational path, branches and outcomes.

### State Transition

Use when the object's semantics change by state.

### Lifecycle

Use when creation/ownership/release/destruction matters.

### Sequence

Use when several actors interact over time. Do not use it as a decorative alternative to Flow.

### Data Path

Use when data movement/transformation is the primary story.

### Synchronization

Use when shared state and synchronization semantics are central. Always try to show what is protected.

### Architecture

Use when module boundary and layering are central.

### Recovery

Use when failure/rollback/retry is a first-class understanding problem.

## Diagram vs prose

Prefer prose/table for:

- small factual sets;
- simple field descriptions;
- one obvious relation.

Prefer diagrams when:

- topology is non-trivial;
- multiple branches exist;
- state changes over time;
- multiple actors synchronize;
- data passes across several transformations.

## Diagram sizing

Aim for roughly 5–12 meaningful nodes in a core diagram.

Split larger views by question or abstraction level rather than compressing everything into one graph.

## Graph/prose/code division

```text
Graph  = what relates/flows/changes
Prose  = what it means, conditions, consequences
Code   = where the claim is evidenced
```

Do not repeat identical information in all three forms.
