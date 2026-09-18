---
name: source-code-reading
version: 0.5
summary: A staged, evidence-driven method for understanding large C/C++ codebases and producing source-traceable knowledge notes.
---

# Source Code Reading Skill

## Purpose

Turn source code into a navigable, evidence-backed knowledge model without asking the agent to understand the whole repository at once.

The skill is **progressive**: build the smallest useful understanding first, validate it, then deepen only where needed.

The durable asset is a canonical knowledge model. Markdown, Mermaid, tables, and diagrams are views over that model.

## Non-negotiable execution rule

**Never attempt to understand the whole system before solving the current question.**

Always execute in this order:

```text
0. Scope
  ↓
1. Orient
  ↓
2. Model the minimum
  ↓
3. Identify the dominant pattern
  ↓
4. Trace the evidence
  ↓
5. Represent + document
  ↓
6. Validate
  ↓
7. Expand only if a gap remains
```

The canonical six-stage loop remains:

```text
Scope & Explore
→ Knowledge Model
→ Pattern Recognition
→ Traceability
→ Representation & Document
→ Validation & Orchestration
```

`0. Scope` and `1. Orient` are entry controls; they are not extra knowledge-production stages.

## Stop / continue gates

At every stage, ask whether the exit condition is satisfied. If yes, stop that stage. Do not continue “for completeness”.

### Gate 0 — Scope

Define:
- user question
- target subsystem/topic
- repository/version/build context
- requested depth
- expected output

Exit when the target can be stated in 1–3 sentences.

### Gate 1 — Orient

Find only enough context to locate the target:
- repository/module boundary
- major neighboring subsystems
- likely entry points
- critical types/symbols
- relevant docs/tests if obvious

Exit when you can answer: **Where is this topic in the system?**

Do not build the full architecture here.

### Gate 2 — Minimum Knowledge Model

Create only the entities and relations required to answer the scoped question.

Minimum useful chain:

```text
System → Subsystem → Topic/Concern → Path → Mechanism → Entity → Symbol
```

Not every topic requires every node.

Exit when the current question has a plausible model with no major unknown that blocks tracing.

### Gate 3 — Pattern

Select:
- one dominant pattern
- zero or more secondary patterns

Patterns:
- Structural / Topology
- Lifecycle / Ownership
- Flow / Pipeline
- State Machine
- Concurrency / Synchronization
- Data Path / Transformation
- Resource / Cache / Index
- Recovery / Error / Consistency
- Architecture / Subsystem Boundary

Pattern selection is based on the **comprehension question**, not keywords.

Exit once the representation goal is clear.

### Gate 4 — Traceability

Trace only the evidence needed to support the claims.

For important claims, record:
- claim
- source anchor
- relevant code element
- evidence kind
- confidence / unresolved ambiguity

Prefer actual source relationships over inferred intent.

Important distinctions:
- pointer ≠ ownership
- pointer ≠ runtime identity
- lock presence ≠ proof of protected data
- enum ≠ complete state machine
- call graph ≠ runtime flow
- directory adjacency ≠ architecture

Exit when the central claims can be followed back to source.

### Gate 5 — Representation & Document

Choose the smallest representation that makes the model easy to understand.

Decision order:

```text
Core question
→ Dominant pattern
→ Representation family
→ Concrete diagram type
→ Renderer
```

A diagram is optional.

Default output is usually:
1. one concise explanation of the model
2. one primary visual when it adds information
3. selected source/code anchors
4. important constraints/invariants

Exit when the reader can navigate from concept → relationship → source.

### Gate 6 — Validation

Validate from the target source again.

Check:
- factual accuracy
- relation semantics
- source anchors
- pattern/diagram fit
- cross-view consistency
- missing constraints/invariants
- unsupported interpretation

If a check fails, return to the earliest affected stage instead of patching prose blindly.

## Progressive depth policy

Use four depth levels:

### L0 — Orientation

Answer where the topic sits and what surrounds it.

### L1 — Local model

Explain the core entities, management/data relationships, and one representative path.

### L2 — Source trace

Follow key functions, fields, state transitions, ownership, synchronization, or data movement into source.

### L3 — Cross-cutting architecture

Add broader subsystem relationships, competing paths, failure/recovery, performance concerns, or design trade-offs only when the task requires them.

**Default: start at L1.**
Do not enter L2/L3 until a concrete unknown requires it.

## Architecture foundation policy

For a large repository, maintain a persistent **System Atlas / Architecture View**, but build it incrementally.

Start with:
- architecture spine: roughly 5–12 meaningful subsystem elements
- critical paths relevant to current work
- architecture coordinates for the current topic

Do not reverse-engineer the entire repository up front.

Architecture is a view of the same canonical knowledge graph:

```text
Canonical Knowledge Graph
├── Architecture View
├── Path / Runtime View
├── Topic View
└── Source View
```

Keep `documented/intended` and `observed/as-built` separate when they differ.

## Canonical knowledge objects

Use only objects needed by the current task. Common objects:

- System
- Subsystem
- Concern
- Path / Scenario
- Mechanism
- Entity
- Symbol
- Relation
- State
- Lifecycle
- Constraint / Invariant / Protocol
- Claim
- Evidence
- Source Anchor
- Decision / Rationale

Relations may be structural, management, dependency, runtime, concurrency, or architectural.

### Semantic safety

Never infer semantics from syntax alone.

Examples:
- `foo *p` proves a pointer, not ownership.
- `LockAcquire(x)` proves locking, not what x protects.
- `state = X` proves a write, not the complete state machine.
- `a()` calling `b()` proves a call edge, not that every runtime path is `a → b`.

## Source navigation policy

Prefer a small set of high-value anchors:
- entry point
- central type
- key manager/index
- lifecycle constructor/destructor
- state transition writer
- synchronization boundary
- I/O or persistence boundary
- representative test

Avoid dumping large source listings into the note.

## Representation policy

Use a structure/entity relationship view when the question is about:
- what objects exist
- who references whom
- who contains/manages/indexes what
- how core objects are organized

Use flow/sequence when the question is temporal execution.
Use state diagrams when the question is legal state transition.
Use concurrency views when the question is protection, waiting, ordering, or ownership of synchronization.
Use data-path views when values/pages/tuples move or transform.
Use resource/cache/index views when lookup, reuse, residency, victim selection, or resource management dominates.

Avoid giant diagrams. Prefer ~5–12 meaningful nodes per primary visual; split by view when needed.

Mermaid is a renderer, not the semantic model.

## External knowledge sources

External methodology, standards, renderer docs, and analysis-tool docs may teach:
- notation
- method
- tool capability
- general language/concurrency semantics

They do not override repository evidence.

Consult external sources only when:
- a notation choice is genuinely ambiguous
- a tool capability matters
- a semantic rule cannot be safely established from local source
- a mature example is useful for method, not for repository facts

Record the useful rule, not a pasted literature review.

## Self-evolution

Do not silently modify the normative skill.

Use:

```text
Feedback
→ Failure classification
→ Case
→ Candidate rule
→ Regression
→ Human/project approval
→ Adopted rule
```

A reusable failure case should preserve enough context to reproduce the mistake.

## Anti-overengineering rules

The agent must not:
- read the entire repository by default
- create a complete system architecture before understanding the task
- build every possible relation
- generate multiple diagrams just because they are available
- consult external sources for facts already established by the target source
- infer design intent without evidence
- turn every symbol into a knowledge node
- produce documentation that is broader than the scoped question without a clear reason

## Completion criteria

A task is complete when:
1. the scoped question is answered
2. the core model is understandable
3. important claims are source-traceable
4. the primary representation matches the dominant pattern
5. validation finds no known contradiction or unsupported central claim

Do not optimize for repository coverage. Optimize for **useful, navigable, source-grounded understanding**.
