bash -lc set -e
ROOT=/mnt/data/source-code-reading-skill-v0.5
rm -rf "$ROOT"
mkdir -p "$ROOT"/references/patterns "$ROOT"/references/representation "$ROOT"/templates "$ROOT"/examples
cat > "$ROOT/SKILL.md" <<'EOF'
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
EOF

cat > "$ROOT/README.md" <<'EOF'
# Source Code Reading Skill v0.5

This version focuses on **execution discipline** rather than adding more theory.

The most important change is the staged-gate protocol: the Agent must stop at each layer once the current question is sufficiently explained, and only deepen when an unresolved question forces it to.

## Intended architecture

```text
Source Understanding System
├── Core Skill
│   ├── staged execution + gates
│   ├── architecture foundation
│   ├── canonical knowledge model
│   ├── pattern recognition
│   ├── traceability
│   ├── representation policy
│   └── validation
├── Capability Extensions
│   ├── static analysis
│   ├── runtime observation
│   ├── performance analysis
│   ├── test analysis
│   └── diagram rendering
├── Knowledge Sources
│   └── standards / methods / tool docs / project examples
└── Evolution
    ├── cases
    ├── feedback
    ├── anti-patterns
    └── regression
```

## What is deliberately not in the core

Tool manuals, exhaustive diagram catalogs, vendor-specific workflows, perf/BPF/VTune procedures, and project-specific rules should remain extensions or knowledge sources.

## Default operating behavior

Start small → build model → choose pattern → trace → represent → validate → deepen only if needed.
EOF

cat > "$ROOT/references/execution-protocol.md" <<'EOF'
# Execution Protocol

## 1. Intake

Before reading deeply, write a compact task statement:

```yaml
scope:
  question: "..."
  target: "..."
  repository: "..."
  version_or_commit: "..."
  build_context: "..."
  depth: L1
  output: "..."
```

If version/build context is unknown and can change the answer, resolve it before deep tracing.

## 2. Orientation

Answer these in order:

1. Where is the topic?
2. What subsystem owns or surrounds it?
3. What are the likely entry points?
4. Which 3–8 symbols are most likely to matter?
5. Which path/operation makes those symbols meaningful?

Do not continue browsing once enough evidence exists to establish the local neighborhood.

## 3. Minimum model

Construct only the smallest graph that can support the scoped question.

Example:

```text
Buffer Manager
  └─ Buffer Lookup Path
      ├─ BufferTag
      ├─ hash/partition mapping
      ├─ BufferDesc
      └─ mapping lock
```

Add entities only when a missing edge or missing behavior blocks understanding.

## 4. Choose the dominant pattern

Ask: **What is the reader really trying to understand?**

- topology → structural/entity relation
- lifetime → lifecycle/ownership
- order → flow/sequence
- legal transitions → state
- protection/order/waiting → concurrency
- movement/transformation → data path
- reuse/index/residency → resource/cache/index
- subsystem boundary → architecture

## 5. Trace claims

For each central claim, capture one or more source anchors.

Prefer this shape:

```text
Concept
  ↓ relation
Function / field / type
  ↓ evidence
Source location
```

Use confidence levels when interpretation is not fully proven:
- observed
- strongly inferred
- hypothesis

## 6. Document

Use this default note order:

```text
1. What this thing is
2. Where it sits
3. Core entities/relationships
4. Representative path
5. Key mechanism
6. Important constraints/invariants
7. Source anchors
8. Validation / open questions
```

## 7. Deepening rule

Deepen only when one of these remains unresolved:
- a central relation is ambiguous
- runtime behavior cannot be explained
- lifecycle/ownership is unclear
- state transitions are incomplete
- concurrency semantics are unclear
- architecture position conflicts with source evidence
- a critical claim lacks a source anchor

Otherwise stop.
EOF

cat > "$ROOT/references/stage-gates.md" <<'EOF'
# Stage Gates

| Gate | Minimum artifact | Stop condition | Deepen when |
|---|---|---|---|
| Scope | task statement | question bounded | scope changes |
| Orient | local neighborhood | topic location is clear | boundary/entry unknown |
| Model | minimal graph | central objects/relations are plausible | missing edge blocks answer |
| Pattern | dominant pattern | comprehension question is clear | multiple patterns compete materially |
| Trace | claim→source links | central claims trace | evidence conflict/ambiguity |
| Represent | chosen view | reader can follow model | current view hides needed semantics |
| Validate | check results | no known central issue | contradiction or unsupported claim |

## Hard stop rules

Stop reading when the unresolved items are peripheral to the user's question.

Stop drawing when the diagram stops adding information.

Stop expanding architecture when the current topic already has a stable architecture coordinate.

Stop adding source anchors when every important claim is traceable and additional anchors are redundant.
EOF

cat > "$ROOT/references/architecture-foundation.md" <<'EOF'
# Architecture Foundation

## Goal

Provide enough system context that topic notes do not become isolated islands.

## Incremental construction

Build the Atlas in this order:

```text
1. Architecture spine
2. Current topic coordinate
3. One or two critical paths
4. Neighboring subsystem relations
5. Cross-cutting concerns only when required
```

Do not attempt full repository architecture reconstruction as a prerequisite for every topic.

## Architecture coordinate

```yaml
architecture_position:
  system: ""
  subsystem: ""
  layer: ""
  concerns: []
  mechanisms: []
  paths: []
  upstream: []
  downstream: []
  neighboring_topics: []
```

## Architecture vs implementation

Store separately when useful:

```yaml
architecture_fact:
  documented: "..."
  observed: "..."
  status: aligned | partially_aligned | divergent | unknown
  evidence: []
```

The source repository is authoritative for implementation behavior; architecture documents are evidence of intended structure.
EOF

cat > "$ROOT/references/patterns/catalog.md" <<'EOF'
# Pattern Catalog

| Pattern | Main question | Typical evidence | Common representation |
|---|---|---|---|
| Structural / Topology | What is connected to what? | structs, pointers, embedded fields, managers | Entity/relationship map |
| Lifecycle / Ownership | Who creates/releases/owns it? | alloc/free, refcount, lifetime states | Lifecycle + ownership map |
| Flow / Pipeline | What happens in what order? | calls, branches, phases | Flow / sequence |
| State Machine | What states/transitions are legal? | state fields + transition writers | State diagram |
| Concurrency | Who protects/waits/orders? | locks, atomics, queues, barriers | Concurrency/sequence |
| Data Path | How does data move/transform? | read/write, buffers, conversions | Data-path diagram |
| Resource / Cache / Index | How is resource found/reused? | hash, buckets, indexes, eviction | Resource map |
| Recovery / Consistency | What happens on failure/recovery? | WAL, rollback, retries, checkpoints | Recovery flow |
| Architecture | Where is the boundary? | APIs, modules, dependencies, paths | Architecture view |

Pattern classification must be driven by the comprehension goal, not by keywords alone.
EOF

cat > "$ROOT/references/representation/selection.md" <<'EOF'
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
EOF

cat > "$ROOT/references/traceability.md" <<'EOF'
# Traceability

## Claim record

```yaml
claim:
  text: "..."
  status: observed | strongly_inferred | hypothesis
  evidence:
    - source_anchor: "path/to/file.c:123-145"
      element: "FunctionOrType"
      kind: field_write | call | allocation | lock | branch | test | docs | runtime
      note: "..."
```

## Evidence hierarchy

For implementation behavior, prefer:

```text
source code
> executable tests / runtime observation
> project docs/design notes
> external methodology
> model memory / generic expectation
```

External material may define notation or general semantics, but it must not replace repository evidence.
EOF

cat > "$ROOT/templates/topic-note.md" <<'EOF'
# {{Topic}}

## 1. 一句话定位

> {{What is it and why does it matter?}}

## 2. 在系统中的位置

```text
{{System → Subsystem → Topic → Path}}
```

## 3. 核心对象与关系

{{Concise explanation}}

```mermaid
{{Primary visual only if useful}}
```

## 4. 代表性路径

```text
{{entry}} → {{mechanism}} → {{result}}
```

## 5. 关键机制

{{Source-grounded explanation with a few code anchors}}

## 6. 约束 / 不变量 / 协议

- {{constraint}}

## 7. 源码落脚点

- `{{file:function/type/field}}` — {{why it matters}}

## 8. 未决问题

- {{open question, if any}}
EOF

cat > "$ROOT/templates/architecture-topic-link.yaml" <<'EOF'
topic: ""
architecture_position:
  system: ""
  subsystem: ""
  layer: ""
  concerns: []
  mechanisms: []
  paths: []
  upstream: []
  downstream: []
  neighboring_topics: []
EOF

cat > "$ROOT/examples/buffer-manager-example.md" <<'EOF'
# Example: Buffer Manager topic at L1/L2

This example demonstrates **progressive depth** rather than exhaustive coverage.

## Start at L1

```text
Executor / Access Method
        ↓
   Buffer Manager
        ↓
 Buffer Lookup
   ├─ page identity
   ├─ mapping/index structure
   ├─ buffer descriptor
   └─ synchronization
```

At L1, the agent only needs enough symbols to explain the management backbone.

## Move to L2 only for a concrete question

For example:

> How does a page identity become a specific buffer descriptor?

Now trace the lookup path, mapping structure, partition lock, and descriptor access into source.

Do not automatically add replacement policy, WAL interaction, I/O workers, background writer, checkpointing, and performance analysis unless the question requires them.
EOF

cat > "$ROOT/examples/reading-sequence.md" <<'EOF'
# Example execution sequence

```text
User question
  ↓
Scope: "Explain TupleTableSlot's object relationships and tuple ownership"
  ↓
Orient: executor/tuptable + slot-related types
  ↓
Minimum model: Slot → TupleTableSlot / TupleTableSlotOps / tuple storage
  ↓
Pattern: Structural + Lifecycle
  ↓
Trace: constructors, tuple store fields, materialization/release paths
  ↓
Represent: one entity/management view + a small lifecycle note
  ↓
Validate: verify ownership claims and cleanup paths
  ↓
Stop
```

Only after this should a new question trigger a second loop, such as execution flow, deforming, or memory ownership.
EOF

cd /mnt/data
zip -qr source-code-reading-skill-v0.5.zip source-code-reading-skill-v0.5
python - <<'PY'
from pathlib import Path
import zipfile, yaml
root=Path('/mnt/data/source-code-reading-skill-v0.5')
files=list(root.rglob('*'))
print('files', sum(p.is_file() for p in files))
print('lines', sum(sum(1 for _ in p.open(errors='ignore')) for p in files if p.is_file()))
with zipfile.ZipFile('/mnt/data/source-code-reading-skill-v0.5.zip') as z:
    bad=z.testzip()
    print('zip_test', bad)
print('size', Path('/mnt/data/source-code-reading-skill-v0.5.zip').stat().st_size)
PY