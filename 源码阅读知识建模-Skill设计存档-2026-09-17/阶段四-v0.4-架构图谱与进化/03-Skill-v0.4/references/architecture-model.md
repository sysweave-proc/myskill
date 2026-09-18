# Architecture Model

## Purpose

The architecture model is the stable coordinate system for the entire source-reading knowledge graph.

It answers four different questions:

```text
System context      → What is the system and its boundary?
Architecture spine  → How is the system broadly organized?
Runtime paths       → When do parts work together?
Topic/source        → How is a specific mechanism implemented?
```

## Canonical graph

```text
System
 └─contains→ Subsystem
              ├─contains→ Mechanism
              ├─participates_in→ Path
              └─addresses→ Concern

Mechanism
 ├─realized_by→ Entity / Symbol
 ├─participates_in→ Path
 └─depends_on→ Mechanism

Entity / Symbol
 ├─references→ Entity
 ├─modifies→ Entity
 ├─protects→ State
 └─evidenced_by→ SourceRange
```

## Architecture layers

### A0 System context
Boundary, external actors, external dependencies.

### A1 Architecture spine
5–12 broad subsystems or layers. Do not attempt to enumerate the whole repository.

### A2 Capability / mechanism
The stable capabilities inside a subsystem.

### A3 Runtime path / scenario
End-to-end behavior that crosses subsystems.

### A4 Source realization
Core entities, symbols, fields, code regions.

## Core architecture relations

```text
contains
refines
depends_on
interfaces_with
participates_in
realized_by
implemented_by
managed_by
owns
cross_cuts
```

Use relations only when evidence supports them.

## Architecture coordinates for a topic

Each major topic should record:

```yaml
architecture_position:
  system: ""
  subsystem: ""
  layer: ""
  mechanisms: []
  paths: []
  concerns: []
  upstream: []
  downstream: []
  neighboring_topics: []
```

## Do not use the architecture model as a rigid tree

The architecture spine may be tree-like for readability, but the canonical model is a graph. A topic may participate in several paths and concerns.

## Architecture quality tests

A system atlas is useful only if it can answer:

1. Where is a topic located?
2. Which major path(s) use it?
3. Which neighboring subsystems does it depend on?
4. Can a reader zoom from architecture to source and back?
5. Does the architecture explain at least one representative end-to-end scenario?

## Architecture gaps

A missing node on a critical path is a knowledge gap even if no note file is missing.

```text
Path:
A → B → C → D

Known:
A ✓ B ✓ C ? D ✓

Gap:
C
```

The gap should be tracked as an `open_question` or `knowledge_gap`, not papered over with a guessed relationship.

