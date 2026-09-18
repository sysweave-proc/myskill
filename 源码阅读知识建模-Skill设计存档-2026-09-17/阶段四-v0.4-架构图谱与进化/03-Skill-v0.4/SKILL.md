---
name: source-code-reading
version: 0.4.0
description: >-
  A graph-first skill for understanding large C/C++ systems such as Linux,
  PostgreSQL, and MySQL. It reconstructs an architecture model, traces runtime
  paths into source, builds a canonical knowledge graph, recognizes the dominant
  comprehension pattern, chooses an evidence-backed representation, generates
  navigable source-reading documents, validates them, and learns from feedback
  through cases and regression tests.
---

# Source Code Reading Skill v0.4

## Purpose

Build a **single, traceable system knowledge model** from large C/C++ codebases and project documentation. The model must support both:

- **zooming in**: System → Subsystem → Path → Mechanism → Entity → Symbol → Code;
- **zooming out**: Code → Symbol → Entity → Mechanism → Path → Subsystem → System;
- **moving sideways**: Entity/Mechanism → related path, resource, lifecycle, concurrency concern, or neighboring subsystem.

The skill is not a Markdown summarizer. Markdown, Mermaid, Graphviz, tables, and code snippets are projections of a canonical model.

## Operating principle

```text
                SYSTEM KNOWLEDGE GRAPH
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
 Architecture          Paths           Concerns
        │                │                │
        └────────────────┼────────────────┘
                         ↓
                    Subsystems
                         ↓
                     Mechanisms
                         ↓
                       Topics
                         ↓
                      Entities
                         ↓
                      Symbols
                         ↓
                     Evidence
```

The graph is one model. Architecture, runtime path, topic, and source are not separate databases connected by hyperlinks.

## Six-stage execution protocol

Architecture orientation is a persistent foundation, not an extra content-generation stage. Every topic task then runs through exactly these six stages:

```text
① Scope & Explore
        ↓
② Knowledge Model
        ↓
③ Pattern Recognition
        ↓
④ Traceability
        ↓
⑤ Representation & Document
        ↓
⑥ Validation & Orchestration
```

Stages may loop backward when validation exposes missing evidence.

## Architecture foundation: System Atlas

Before deep topic work on a large system, establish or load a System Atlas. The atlas should minimally contain:

```text
System Context
Architecture Spine
Critical Scenarios / Paths
Subsystem Map
Cross-cutting Concerns
Known Architecture ↔ Source Mappings
Open Architecture Questions
```

Read `references/architecture-model.md` and `references/architecture-reconstruction.md` when working on a system-scale task or when an existing atlas is missing/stale.

## Stage 1 — Scope & Explore

Define:

```text
subject
core question(s)
reader / intended use
depth
included scope
excluded scope
current architecture coordinates
```

Then explore the source by unknowns, not linearly. Prefer semantic navigation when available:

```text
symbol definition → references → callers/callees → field readers/writers
→ lifecycle functions → synchronization → cross-module boundary
```

Every expansion must answer an explicit unresolved question.

## Stage 2 — Knowledge Model

Extract source-grounded knowledge into:

```text
Entity
Relation
Flow
State
Lifecycle
Concurrency
Constraint
Claim
Evidence
```

Also attach architecture coordinates:

```text
system
subsystem
path(s)
mechanism
concern(s)
```

Use `references/knowledge-model.md`.

## Stage 3 — Pattern Recognition

Choose exactly one **dominant comprehension pattern** and zero or more secondary patterns:

```text
Structural
Lifecycle
Flow
State
Concurrency
Data Path
Resource
Recovery
Architecture
```

Do not classify from keywords alone. The dominant pattern is the question that most strongly determines how the topic should be understood.

Use `references/patterns/pattern-catalog.md`.

## Stage 4 — Traceability

For each substantial claim:

```text
Claim → Evidence → Source Anchor → Trace
```

Distinguish:

```text
FACT
INFERENCE
INTERPRETATION
```

If evidence is insufficient, mark the claim `UNVERIFIED` and either explore further or remove/qualify it.

Use `references/tracing/trace-policy.md` and `references/tracing/claim-verification.md`.

## Stage 5 — Representation & Document

Select representation in this order:

```text
Core Question
  ↓
Dominant Pattern
  ↓
Representation Family
  ↓
Concrete method
  ↓
Renderer / tool
```

Possible families include:

```text
Structural
Management / Ownership
Flow / Control
State / Lifecycle
Sequence / Interaction
Data / Dataflow
Concurrency / Synchronization
Resource / Cache
Architecture / Layer
Recovery / Failure
Memory Layout
```

A diagram is optional. Prefer text or a compact table when a diagram does not reduce cognitive load.

Use `references/representation/representation-policy.md` and `references/diagrams/diagram-catalog.md`.

## Stage 6 — Validation & Orchestration

Validate:

```text
structural
semantic
traceability
representation
reader/navigation
architecture consistency
```

On failure, identify the missing layer and re-enter the minimum necessary stage(s). Do not regenerate blindly.

Use `references/validation/validation-policy.md`.

## Architecture ↔ topic integration rules

1. A topic must have a stable architecture coordinate when the system atlas is available.
2. A topic should normally attach to one or more runtime/scenario paths when such paths exist.
3. A source symbol may belong to multiple concerns or paths; do not force a tree where the source is genuinely a graph.
4. Architecture claims require evidence just like implementation claims.
5. The system atlas is revisable: new source evidence may refine or contradict the current architecture model.
6. Use `contains`, `refines`, `participates_in`, `implemented_by`, `evidenced_by`, and `related_through_path` as first-class cross-level relations.

## External knowledge sources

Use `knowledge-sources/resource-advisor.md` to choose external methodology and tool sources. External sources teach notation, methodology, tool capability, and general language/system semantics; they do not establish facts about the target repository.

## Evolution

User feedback and reviewed cases can produce **candidate rules**, but no rule becomes normative without regression against existing gold cases. Use `evolution/evolution-policy.md`.

Never allow a model to silently rewrite its own rules. The safe loop is:

```text
Feedback
  ↓
Failure classification
  ↓
Rule proposal
  ↓
Regression
  ↓
Human/project approval
  ↓
Adopted rule
```

## Modes

### Explore
Investigate source and architecture without generating the final document.

### Model
Build or update the canonical knowledge model.

### Document
Render a document from an existing verified model.

### Review
Audit an existing document against source, architecture, claims, representation, and navigation.

### Evolve
Analyze reviewed failures and produce candidate rule updates; do not auto-promote them.

## Hard rules

1. Never jump directly from source to polished prose when the task is non-trivial.
2. Never infer ownership from a pointer alone.
3. Never equate a call graph with runtime flow.
4. Never equate an enum with a complete state machine.
5. Never equate the presence of a lock with proof of what it protects.
6. Never invent architecture from directory names alone.
7. Never use a formal notation label just because the rendered picture resembles it.
8. Never put every discovered entity into one diagram.
9. Never repeat the same explanation in graph, prose, and code unless each layer adds distinct value.
10. Never present an interpretation as a source fact.
11. Never let an external source override target-repository evidence.
12. Preserve exact source names as navigation anchors.
13. When a representation repeatedly fails, capture the failure as a case before changing the rule.
14. Prefer the smallest sufficient view over maximal information density.

## Primary deliverables

Depending on mode, return one or more of:

```text
System Atlas
Knowledge Model
Pattern Profile
Trace Map
Representation Plan
Source-reading document
Review Report
Rule Proposal
Regression result
```

## Quality target

A high-quality result should make a reader able to answer:

```text
Where am I in the system?
What problem is this subsystem solving?
What path does this mechanism participate in?
What are the core entities?
How do they relate?
What changes over time?
What concurrency/resource constraints matter?
Where is the implementation?
Why does the document make this particular claim?
What should I read next?
```

