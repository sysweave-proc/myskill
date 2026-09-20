---
name: source-code-reading
version: 0.1.0
description: >-
  A general-purpose skill for understanding large C/C++ codebases by
  transforming source code into a traceable knowledge model, identifying the
  dominant comprehension pattern, building source evidence traces, selecting
  the right representation, and generating navigable source-reading notes.
---

# Source Code Reading Skill

## Purpose

Turn large C/C++ source trees into **verifiable, navigable knowledge**, not merely summaries.

The skill follows one unified six-stage execution model:

```text
1. Scope & Explore
        ↓
2. Knowledge Model
        ↓
3. Pattern Recognition
        ↓
4. Traceability
        ↓
5. Representation & Document
        ↓
6. Validation & Orchestration
```

The final document must help a reader:

1. understand the mental model,
2. verify important claims against source,
3. continue reading the source independently.

## Non-goals

Do not:

- summarize files linearly unless requested;
- treat a call graph as an execution flow automatically;
- infer ownership from a pointer merely because a pointer exists;
- infer design intent from a function name alone;
- invent state machines from enums without transitions;
- generate diagrams merely because diagrams are available;
- hide uncertainty behind confident prose;
- expand into unrelated modules just to appear comprehensive.

## Core intermediate model

The skill treats the source as a graph of:

```text
Entity
Relation
Flow
State
Lifecycle
Concurrency
Constraint
Evidence
Claim
Trace
```

The key document unit is a **Claim**, not a paragraph.
Every important claim should be traceable to one or more pieces of source evidence.

## Operating rules

### Rule 1 — Never jump directly from source to final document

Always pass through the knowledge model and pattern decision. The internal model may be lightweight, but the reasoning stages must occur.

### Rule 2 — Scope before depth

Define the current question and boundary before expanding the source context.

### Rule 3 — Expand context by unknowns

Every exploration step should answer a concrete unresolved question.

### Rule 4 — One dominant pattern

Select one dominant comprehension pattern and zero or more secondary patterns. Patterns are not mutually exclusive.

Supported patterns:

- Structural / Topology
- Lifecycle / Ownership
- Flow / Pipeline
- State Machine
- Concurrency / Synchronization
- Data Path / Transformation
- Resource / Cache / Index
- Recovery / Error / Consistency
- Architecture / Subsystem Boundary

See `references/patterns/pattern-catalog.md`.

### Rule 5 — Claims have epistemic types

Use:

- `FACT` — directly supported by source;
- `INFERENCE` — derived from multiple facts;
- `INTERPRETATION` — explanation of likely intent or design rationale.

Never present an unverified inference as a fact.

### Rule 6 — Source identity should be stable

Prefer:

```text
repository + revision/commit/tag + path + symbol + field/code region
```

over line numbers alone.

Line ranges are useful secondary anchors, not the primary identity.

### Rule 7 — Evidence must explain the claim

A source location by itself is not sufficient. Record what the code demonstrates.

### Rule 8 — Stop tracing when the claim is proven

Do not trace the whole call tree. Stop when the claim is sufficiently supported or the trace reaches the defined boundary.

### Rule 9 — Representation follows the question

Choose diagrams, tables, prose, and snippets based on the comprehension problem. A diagram is optional.

### Rule 10 — Keep graph and prose non-redundant

- graph: structure/path/change;
- prose: semantics/conditions/reasons;
- code: evidence.

### Rule 11 — Preserve source names

Use real symbol names such as `BufferDesc`, `BufferAlloc()`, `ExecStoreHeapTuple()` so the document doubles as source-navigation material.

### Rule 12 — Validate before finalizing

Run semantic, trace, representation, and reader checks. If validation fails, re-enter the earliest stage that can resolve the problem.

## Six-stage execution

### Stage 1 — Scope & Explore

Define:

- subject;
- core questions;
- reader/depth;
- included modules;
- excluded modules.

Then explore the source enough to build the initial search space:

```text
Target symbol
  ↓
Definition
  ↓
Direct references
  ↓
Related fields/structs
  ↓
Relevant callers/callees
  ↓
State/lifecycle/synchronization clues
  ↓
Cross-module only when needed
```

Output: `SourceContext`.

See `references/tracing/exploration-policy.md`.

### Stage 2 — Knowledge Model

Extract the important:

- entities;
- relations;
- flows;
- states;
- lifecycles;
- concurrency semantics;
- constraints/invariants;
- claims;
- evidence.

Do not optimize for document prose yet.

Output: `KnowledgeModel`.

See `references/knowledge-model.md`.

### Stage 3 — Pattern Recognition

Ask:

> What is the primary question required to understand this source fragment?

Choose one dominant pattern and optional secondary patterns.

Do not classify from keywords such as `struct`, `lock`, `enum`, or `if` alone.

Output: `PatternProfile`.

See `references/patterns/pattern-catalog.md`.

### Stage 4 — Traceability

For each important claim, establish:

```text
Claim
  ↓
Evidence
  ↓
Symbol / Field / Code Region
  ↓
Trace if necessary
```

Possible trace directions:

- definition;
- usage/readers;
- mutation/writers;
- call;
- data;
- lifecycle;
- synchronization.

Use D1/D2/D3 trace depth:

- D1 Local
- D2 Structural
- D3 System

Stop when evidence closes the claim.

See `references/tracing/trace-policy.md` and `references/tracing/claim-verification.md`.

### Stage 5 — Representation & Document

First create a representation plan:

```text
Core question
  ↓
Dominant pattern
  ↓
Primary view
  ↓
Secondary views (usually 0–2)
  ↓
Source anchors/snippets
```

Then generate the document.

Recommended generic skeleton:

```text
# Title

> Core Question

## 一句话模型

## 1. 核心对象

## 2. 核心行为

## 3. 关键状态 / 生命周期

## 4. 并发与约束

## 5. 关键实现

## 6. 源码导读

## 7. 关键结论

## 8. 下一步阅读
```

Sections are conditional; do not add empty boilerplate.

See `references/representation/representation-policy.md` and `references/document-policy.md`.

### Stage 6 — Validation & Orchestration

Validate in this order:

1. structural;
2. semantic;
3. traceability;
4. representation;
5. reader/navigation.

For failures, re-enter the earliest useful stage:

```text
Missing source evidence → Stage 1 or 4
Wrong semantic model → Stage 2
Wrong dominant view → Stage 3
Poor expression → Stage 5
Formatting/style-only problem → Stage 5
```

See `references/validation/validation-policy.md`.

## Source exploration guidance

Use source tooling appropriate to the environment. Typical operations include:

```text
find symbol
find definition
find references
find callers/callees
find field readers/writers
find allocation/free
find lock acquire/release
find atomic access
find state checks/transitions
find registration/unregistration
```

For very large systems, prefer targeted search + bounded expansion over reading entire files linearly.

## Knowledge model

A minimal internal representation can look like:

```yaml
source_context:
  repository:
  revision:
  subject:
  core_questions: []
  included_modules: []
  excluded_modules: []
  symbols: []

knowledge:
  entities: []
  relations: []
  flows: []
  states: []
  lifecycles: []
  concurrency: []
  constraints: []
  claims: []
  evidence: []
  traces: []

pattern_profile:
  core_question:
  dominant:
    name:
    reason:
  secondary: []

representation:
  primary:
    type:
    purpose:
  secondary: []
  source_anchors: []
  snippets: []
  exclusions: []
```

This is an internal intermediate representation, not a requirement to expose YAML to the end user.

## Claim protocol

For each important claim record:

```yaml
claim:
  statement:
  type: FACT | INFERENCE | INTERPRETATION
  confidence: HIGH | MEDIUM | LOW
  evidence: []
  trace: []
  scope:
```

Use `UNVERIFIED` when evidence is insufficient. Do not silently fill gaps.

## Evidence protocol

Evidence should identify:

```yaml
evidence:
  id:
  kind: definition | access | mutation | control_flow | call | lifecycle | synchronization | comment | design_doc
  source:
    repository:
    revision:
    path:
    symbol:
    field:
    code_region:
    line_range:
  demonstrates:
```

## Representation selection

Primary-view defaults by dominant pattern:

| Pattern | Primary view |
|---|---|
| Structural | Entity Relationship |
| Lifecycle | Lifecycle |
| Flow | Flow |
| State | State Transition |
| Concurrency | Synchronization |
| Data Path | Data Path |
| Resource | Management / Resource |
| Recovery | Failure / Recovery |
| Architecture | Layer / Architecture |

Useful secondary views:

- Structural → Management
- Lifecycle → Entity / State
- Flow → Sequence / Recovery
- State → Lifecycle
- Concurrency → Sequence / Entity
- Data Path → Flow
- Resource → Entity / State / Concurrency
- Recovery → Flow / State
- Architecture → Entity / Dependency

Do not force secondary views when they add little information.

## Diagram policy

Prefer a diagram when relationships, paths, transitions, or interactions become difficult to understand in prose.

Prefer prose/table when information is mostly:

- definitions;
- small field sets;
- straightforward properties;
- one or two facts without meaningful topology.

Typical core-graph target: roughly 5–12 meaningful nodes. Split larger graphs by question or level rather than creating a wall of nodes.

Use diagrams to show:

- relationship;
- ownership/management;
- execution path;
- state transitions;
- sequence/interaction;
- data movement;
- synchronization;
- architecture boundaries;
- failure/recovery.

Use Mermaid only when it materially improves comprehension.

## Document style

Write in clear professional Chinese unless the user requests another language.

Prefer:

- exact source names;
- concrete conditions;
- short explanatory paragraphs;
- compact tables for attributes;
- short, purposeful code snippets.

Avoid:

- generic praise;
- long copied source blocks;
- fake precision;
- unsupported motive claims;
- repeating the same fact in graph, prose, and table.

## Source snippets

A snippet should usually be short and selected to show one of:

- definition;
- key branch;
- state mutation;
- synchronization boundary;
- ownership transfer;
- cleanup/error path.

After the snippet, explain its semantic role.

## Source navigation

Every substantial chapter should identify the next source reading targets where useful:

```text
Current concept
  ↓
Current symbol
  ↓
Next symbol
  ↓
Why it is the next hop
```

This is a core output, not decorative metadata.

## Incremental knowledge

When prior knowledge exists, merge into the existing graph rather than recreating duplicate entities.

Prefer stable identities such as:

```text
<repository>::<qualified symbol>
```

For example:

```text
postgresql::BufferDesc
postgresql::BufferAlloc()
```

## Supported modes

### Explore

Investigate source only; return structured findings.

### Model

Build or update the knowledge model.

### Document

Generate a document from an existing or newly built model.

### Review

Audit an existing source-reading note for semantic errors, unsupported claims, stale anchors, missing patterns, and navigation quality.

## Completion criteria

A task is complete when:

- the core question is explicit;
- the dominant pattern is justified;
- important claims are evidence-backed;
- source anchors are usable;
- the representation matches the comprehension problem;
- the document is readable without flattening the source semantics;
- the next source-reading path is clear;
- validation finds no critical issue.

## Final quality bar

The ideal result is not:

```text
“这篇笔记把源码讲完了。”
```

It is:

```text
“读者现在有一个准确的 Mental Model，
知道为什么这样组织，知道运行时怎么走，
并且可以从笔记直接回到真实源码继续读。”
```
