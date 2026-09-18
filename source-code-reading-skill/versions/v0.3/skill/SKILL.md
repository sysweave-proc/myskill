---
name: source-code-reading
version: 0.3.0
description: >-
  A general-purpose skill for understanding large C/C++ codebases by
  transforming source code into a traceable knowledge model, identifying the
  dominant comprehension pattern, selecting an appropriate representation
  method (including historical diagram families and Mermaid/manual tools),
  generating navigable source-reading notes, and validating the result.
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

1. build a mental model;
2. verify important claims against source;
3. continue reading the source independently.

## Core philosophy

The skill is a **source-understanding pipeline**, not a Markdown generator:

```text
Source
  ↓
Source Context
  ↓
Knowledge Model
  ↓
Pattern Profile
  ↓
Claim / Evidence / Trace
  ↓
Representation Plan
  ↓
Document
  ↓
Validation
  ↓
Back to Source
```

The durable internal asset is the **knowledge graph + trace map**. Markdown and diagrams are projections of that model.

## Non-goals

Do not:

- summarize files linearly unless requested;
- treat a call graph as an execution flow automatically;
- infer ownership from a pointer merely because a pointer exists;
- infer design intent from a function name alone;
- invent state machines from enums without transitions;
- generate diagrams merely because diagrams are available;
- use Mermaid as a semantic substitute for a formal notation it does not actually implement;
- hide uncertainty behind confident prose;
- expand into unrelated modules just to appear comprehensive.

## Operating rules

### Rule 1 — Never jump directly from source to document

The agent must conceptually pass through all six stages even if some intermediate artifacts are kept internal.

### Rule 2 — Scope before depth

Define the current question and boundary before expanding the source context.

### Rule 3 — Explore by unknowns

Every exploration step should answer a concrete unresolved question.

### Rule 4 — Build a model before choosing a diagram

A `struct`, `if`, `lock`, `enum`, or pointer is evidence, not a diagram instruction.

### Rule 5 — One dominant pattern

Select exactly one dominant comprehension pattern and zero or more secondary patterns.

### Rule 6 — Claims require evidence

Every substantial semantic claim should have source evidence or be explicitly marked `UNVERIFIED`.

### Rule 7 — Separate epistemic status

Use:

- `FACT` — directly supported by source;
- `INFERENCE` — derived from multiple facts;
- `INTERPRETATION` — likely rationale/design explanation.

### Rule 8 — Preserve source identity

Prefer:

```text
repository + revision/commit/tag + path + symbol + field/code region
```

over line numbers alone.

### Rule 9 — Stop tracing when the claim is proven

Do not trace the entire call tree. Stop when the claim is sufficiently supported or the boundary is reached.

### Rule 10 — Representation follows the question

The agent must select a representation family before selecting a concrete diagram syntax.

```text
Core Question
    ↓
Dominant Pattern
    ↓
Representation Family
    ↓
Concrete Diagram Type
    ↓
Mermaid vs specialized/manual
```

### Rule 11 — Mermaid is a renderer, not the model

A Mermaid diagram can express a curated source-reading view. It does not automatically become canonical UML, ER, Petri Net, CFG, HIPO, JSP, or another formal notation merely by resembling it.

### Rule 12 — Graph, prose, and code must divide the work

```text
Graph → structure/path/change/interaction
Prose → semantics/conditions/consequences
Code → source evidence/navigation
```

### Rule 13 — Preserve source names

Use exact names such as `BufferDesc`, `BufferAlloc()`, `ExecStoreHeapTuple()` whenever useful so the document remains grep-friendly.

### Rule 14 — Validate before finalizing

Run structural, semantic, traceability, representation, and reader/navigation checks.

---

## External knowledge sources

The skill has a curated external-learning registry under `knowledge-sources/`.
Read `knowledge-sources/resource-advisor.md` before consulting external methodology,
notation, renderer, or analysis-tool material. The registry is not a bibliography: each
source must have a learning role, trigger conditions, scope of authority, and rule-extraction target.

Use external sources as follows:

```text
Need to understand / choose a method
    → consult methodology source

Need to know whether a renderer can express the chosen model
    → consult renderer documentation

Need compiler-accurate source facts
    → use source analysis / navigation tools

Need C/C++ ownership/concurrency vocabulary
    → consult language/system guardrails
```

Never use an external methodology to override a fact established by the target repository.
For target-code claims, the source tree and project-specific documentation remain authoritative.
When a source is consulted, record what was learned and whether it produced a candidate rule.

### Source consultation belongs to the six-stage loop

```text
1. Scope & Explore
   → external source only when exploration method/tool choice is uncertain

2. Knowledge Model
   → external semantics may clarify terminology; target source still proves facts

3. Pattern Recognition
   → methodology may help distinguish Structural / Flow / State / etc.

4. Traceability
   → external analysis tools may strengthen source tracing

5. Representation & Document
   → use diagram/architecture methodologies and renderer docs

6. Validation & Orchestration
   → compare against registered methods and historical cases
```

# Six-stage execution

## Stage 1 — Scope & Explore

### Objective

Answer:

```text
What exactly am I trying to understand?
Which source is relevant?
Where should I stop?
```

### Scope

Define:

```text
subject
core_questions[]
reader/depth
included_modules[]
excluded_modules[]
```

### Explore

Build the initial source search space:

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

Typical operations:

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

### Context expansion rule

Use the smallest context that resolves the current unknown:

```text
L0 Target
→ L1 Definition
→ L2 Direct references
→ L3 Related structures
→ L4 Relevant control flow
→ L5 Runtime/synchronization
→ L6 Cross-module
```

### Output

`SourceContext`.

See `references/tracing/exploration-policy.md`.

---

## Stage 2 — Knowledge Model

### Objective

Convert source observations into structured knowledge.

Core types:

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
Trace
```

### Entity categories

```text
Source Entity:
  file / function / struct / class / field / enum / macro / variable

Runtime Entity:
  process / thread / coroutine / task / buffer / page / lock / request

Resource Entity:
  memory / CPU / file / buffer / queue / shared memory / connection

Subsystem Entity:
  Buffer Manager / Lock Manager / WAL / Executor / Storage
```

### Relation categories

```text
Structural:
  contains / embeds / points-to / references / inherits

Management:
  owns / manages / allocates / tracks / indexes / caches

Dependency:
  calls / uses / depends-on / invokes / modifies

Runtime:
  produces / consumes / associated-with / dispatches

Concurrency:
  protects / waits-for / synchronized-by / owns-lock / updates-atomically
```

### Behavior categories

```text
Flow
State
Lifecycle
```

### Constraint categories

```text
Precondition
Postcondition
Invariant
OwnershipRule
OrderingRule
ConcurrencyRule
ErrorRule
```

### Claim model

```yaml
claim:
  statement:
  type: FACT | INFERENCE | INTERPRETATION
  confidence: HIGH | MEDIUM | LOW
  evidence: []
  trace: []
  scope:
```

### Evidence model

```yaml
evidence:
  id:
  kind: definition | access | mutation | control_flow | call |
        lifecycle | synchronization | comment | design_doc
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

### Important distinction

Do not collapse:

```text
pointer/reference
```
into:

```text
ownership
```

Do not collapse:

```text
enum
```
into:

```text
state machine
```

Do not collapse:

```text
call graph
```
into:

```text
execution flow
```

Output: `KnowledgeModel`.

See `references/knowledge-model.md`.

---

## Stage 3 — Pattern Recognition

### Objective

Answer:

> What is the primary comprehension problem?

Supported patterns:

```text
Structural / Topology
Lifecycle / Ownership
Flow / Pipeline
State Machine
Concurrency / Synchronization
Data Path / Transformation
Resource / Cache / Index
Recovery / Error / Consistency
Architecture / Subsystem Boundary
```

### Pattern profile

```yaml
pattern_profile:
  core_question:
  dominant:
    name:
    reason:
  secondary:
    - name:
      reason:
```

### Recognition rule

Do not classify from keywords alone.

Instead evaluate:

```text
What does the reader need to know to understand this code?
What knowledge type is densest?
What relation/time/state/concurrency dimension is dominant?
```

Examples:

```text
struct + pointers + manager
→ Structural may dominate

malloc/free + refcount + retain/release
→ Lifecycle may dominate

branch-heavy one-operation path
→ Flow may dominate

enum + transition writers + state-specific behavior
→ State may dominate

shared fields + locks + wait queues
→ Concurrency may dominate

hash + bucket + victim + reuse/eviction
→ Resource may dominate
```

Output: `PatternProfile`.

See `references/patterns/pattern-catalog.md`.

---

## Stage 4 — Traceability

### Objective

Make every important semantic claim auditable:

```text
Claim
  ↓
Evidence
  ↓
Source Anchor
  ↓
Trace (when needed)
```

### Trace directions

```text
Definition
Usage / Readers
Mutation / Writers
Call
Data
Lifecycle
Synchronization
```

### Trace depth

```text
D1 Local
D2 Structural
D3 System
```

Use the minimum depth needed to prove the claim.

### Trace expansion loop

```text
Claim
 ↓
Can current source prove it?
 ├─ yes → stop
 └─ no  → inspect relevant field/callee/caller/manager/lock
              ↓
           retry proof
```

### Trace failure

If evidence is insufficient:

```text
UNVERIFIED
```

Do not fill the gap with a plausible story.

### Design-intent rule

For “why” questions use:

```text
FACT
  ↓
Observed constraint
  ↓
Consequence
  ↓
Possible interpretation
```

Do not turn a possible motivation into a fact without supporting evidence.

See:

- `references/tracing/trace-policy.md`
- `references/tracing/claim-verification.md`

Output: `TraceMap`.

---

## Stage 5 — Representation & Document

### Objective

Project the verified knowledge model into the smallest set of useful human-facing views.

### Required selection sequence

```text
Core Question
   ↓
Dominant Pattern
   ↓
Representation Family
   ↓
Concrete Diagram Type
   ↓
Traditional/manual vs Mermaid vs specialized tool
```

### Representation families

```text
Structural
  → Entity/ER/Class/Structure/Management/Ownership/Dependency

Control
  → Flowchart/Activity/structured flow/bounded CFG

State/Lifecycle
  → State diagram/Lifecycle/State table

Interaction
  → Sequence/Synchronization

Data
  → DFD-style/Data Path/Dataflow

Resource
  → Resource/Cache/Index/Management map

Architecture
  → Component/Layer/Architecture/Deployment

Failure
  → Recovery/Rollback/Error flow

Implementation geometry
  → Memory layout/Cache-line/Offset/ABI view
```

### Primary/secondary rule

Use:

```text
1 primary view
+ usually 0–2 secondary views
```

Each secondary view must add information not already provided by the primary view.

### Diagram/no-diagram gate

Before drawing ask:

1. What single question does this visual answer?
2. Does it expose structure, path, state, time, data, or concurrency better than prose/table?
3. Is the graph small enough to remain readable?
4. Are the important edge semantics source-supported?
5. Does Mermaid express the semantics adequately?

If not, use prose/table/code or a specialized visual tool.

### Mermaid vs traditional/manual

Prefer **Mermaid** when:

- the view is small and curated;
- source names are important navigation anchors;
- the note lives in Markdown/Git;
- textual diff/review matters;
- the semantics fit Mermaid's supported diagram types.

Prefer **traditional/manual/specialized tooling** when:

- exact geometry is itself semantic;
- the graph is exhaustive or very large;
- static-analysis output is required;
- formal notation semantics matter;
- physical memory/ABI/deployment geometry must be precise;
- a formal model such as Petri Net is the deliverable.

See `references/diagrams/diagram-catalog.md` for the full catalog, examples, and selection rules.

### Document skeleton

Adapt to the dominant pattern; do not generate empty boilerplate.

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

### Layering

Prefer three depths:

```text
L1 Mental Model
L2 Core Implementation
L3 Deep Dive
```

A reader should be able to stop at L1 or L2 without needing L3.

### Graph/prose/code division

```text
Graph = relation/path/transition/interaction
Prose = meaning/condition/consequence
Code = evidence and navigation
```

Avoid repeating the exact same content three times.

### Source snippets

Use short snippets to show one important:

```text
definition
key branch
state mutation
synchronization boundary
ownership transfer
cleanup/error path
```

The snippet must have a semantic explanation after it.

### Source navigation

Substantial chapters should identify:

```text
Current concept
  ↓
Current symbol
  ↓
Next symbol
  ↓
Why this is the next hop
```

Output: `Document` plus internal `RepresentationPlan`.

See:

- `references/representation/representation-policy.md`
- `references/diagrams/diagram-catalog.md`
- `references/document-policy.md`

---

## Stage 6 — Validation & Orchestration

### Objective

Verify both the document and the process, and decide whether to re-enter an earlier stage.

### Validation order

```text
V1 Structural
V2 Semantic
V3 Traceability
V4 Representation
V5 Reader / Navigation
```

### V1 Structural

Check:

```text
Core Question exists
Mental Model exists
Primary View exists if a view is justified
Source Navigation exists for substantial notes
Key Conclusions exist
```

### V2 Semantic

Check:

```text
relations are real
ownership is evidenced
state transitions are real
locks are mapped to protected state
copy/reference semantics are correct
parallelism is evidenced rather than guessed
```

### V3 Traceability

Every important claim must resolve:

```text
Claim → Evidence → Source
```

Otherwise mark `UNVERIFIED` or remove the claim.

### V4 Representation

Check:

```text
Primary view matches dominant pattern
No unnecessary diagrams
No diagram wall
No graph/prose duplication
No Call Graph = Flow mistake
No State = Lifecycle mistake
No generic pointer = Ownership mistake
```

### V5 Reader / Navigation

Ask:

```text
Does a first-time reader know what this is?
Do they know the core entities and relations?
Do they understand the primary behavior?
Do they know key states/lifecycle/concurrency constraints?
Can they find the source?
Do they know the next symbol to read?
```

### Re-entry policy

```text
Missing source/evidence
    → Stage 1 or Stage 4

Wrong semantic model
    → Stage 2

Wrong pattern
    → Stage 3

Poor representation/document
    → Stage 5

Only validation/coordination issue
    → remain in Stage 6
```

Use a bounded revision loop; normally 2–3 iterations are enough.

### Orchestration rule

The orchestrator controls the six stages but does not require six separate agents.

Recommended implementation:

```text
One orchestrator
+
modular rule files
+
shared intermediate model
```

---

# Internal intermediate model

A minimal internal model may be represented as:

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
    family:
    type:
    question:
    renderer: mermaid | manual | specialized | prose | table
  secondary: []
  source_anchors: []
  snippets: []
  exclusions: []
```

This is an internal contract, not a requirement to expose YAML to the user.

---

# Diagram selection quick reference

Use this compact mapping first:

| Core question | Preferred family | Typical representation |
|---|---|---|
| Who/what is connected? | Structural | Entity/ER/Class/Management |
| Who owns/manages what? | Lifecycle/Resource | Ownership/Management |
| What happens next? | Control | Flowchart/Activity |
| What state is it in? | State | State diagram |
| Who interacts with whom over time? | Interaction | Sequence |
| How does data move/change? | Data | Data Path/DFD-style |
| How are resources found/reused/evicted? | Resource | Resource/Index/Cache map |
| What protects/waits/updates shared state? | Concurrency | Synchronization + Sequence |
| Where is the subsystem boundary? | Architecture | Component/Layer/Architecture |
| What happens on failure? | Failure | Recovery flow |
| What is the exact object layout? | Implementation geometry | Memory/offset/cache-line diagram |
| None of the above | — | Prose/table/code |

For historical methods, formal semantics, and Mermaid/manual trade-offs, read `references/diagrams/diagram-catalog.md`.

---

# Source-reading modes

## Explore

Investigate source and return structured findings. Do not generate polished prose unless requested.

## Model

Build or update the knowledge model.

## Document

Generate a reading note from an existing/new model.

## Review

Audit an existing note against source evidence, especially diagrams, claims, source anchors, and stale symbols.

---

# Incremental knowledge

When prior knowledge exists:

```text
Existing Knowledge Graph
        +
New Source Exploration
        ↓
Merge
        ↓
Update
        ↓
Validate
```

Prefer stable entity identities such as:

```text
<repository>::<qualified symbol>
```

Examples:

```text
postgresql::BufferDesc
postgresql::BufferAlloc()
```

Avoid creating duplicate entities for the same source symbol.

Maintain `open_questions` and `conflicts` when useful:

```yaml
open_questions:
  - question:
    importance:
    related_symbols: []
    status: open | investigating | resolved

conflicts:
  - description:
    evidence_a: []
    evidence_b: []
    status: unresolved | resolved
```

---

# Completion criteria

A substantial source-reading note is complete only when:

```text
[ ] Scope is explicit
[ ] Core question is clear
[ ] Knowledge model is internally coherent
[ ] Dominant pattern is explicit
[ ] Important claims have evidence
[ ] Diagram choice is justified or diagram use is intentionally rejected
[ ] Diagram semantics are source-supported
[ ] Source anchors are usable
[ ] Key implementation points are shown with short snippets when helpful
[ ] Reader can continue from the note into the source
[ ] Validation passes
```

The final product is a **knowledge projection that points back to source**, not a replacement for source code.


## Knowledge-source registry contract

When the skill learns from an external source, do not merely remember the URL. Persist:

```yaml
source_consultation:
  source_id:
  question:
  learned:
  direct_fact_scope:
  candidate_rule:
  status: observed | proposed | adopted
```

Permanent rules require validation against historical cases. See `knowledge-sources/resource-advisor.md`.
