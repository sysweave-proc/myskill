# Representation Selection

## Decision tree

```text
What does the reader need?
├─ object organization      → entity/relationship
├─ execution order          → flow/sequence
├─ legal states             → state
├─ synchronization/order    → concurrency
├─ data/value movement      → data path
├─ resource/index/reuse     → resource/cache/index
└─ subsystem structure      → architecture
```

## Structure/entity relationship view

Use when the central question is:
- what objects exist
- who contains/references/manages/indexes whom
- how a group of core objects is organized

Useful edge labels:
- contains
- embedded
- points_to
- references
- owns
- manages
- indexes
- protects

Do not replace semantic edge labels with generic arrows when the distinction matters.

## Diagram sizing

Aim for 5–12 meaningful nodes in a primary visual. Split large graphs by viewpoint.

A note may legitimately have no diagram.
