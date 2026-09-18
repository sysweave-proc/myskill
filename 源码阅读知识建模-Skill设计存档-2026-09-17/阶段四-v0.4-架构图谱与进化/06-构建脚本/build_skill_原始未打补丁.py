from pathlib import Path
import yaml, textwrap, shutil, zipfile

root = Path('/mnt/data/source-code-reading-skill-v0.4/source-code-reading-skill')
if root.parent.exists(): shutil.rmtree(root.parent)
(root / 'references' / 'patterns').mkdir(parents=True)
(root / 'references' / 'representation').mkdir(parents=True)
(root / 'references' / 'diagrams').mkdir(parents=True)
(root / 'references' / 'tracing').mkdir(parents=True)
(root / 'references' / 'validation').mkdir(parents=True)
(root / 'knowledge-sources').mkdir(parents=True)
(root / 'evolution' / 'anti-patterns').mkdir(parents=True)
(root / 'cases' / 'gold').mkdir(parents=True)
(root / 'cases' / 'failures').mkdir(parents=True)
(root / 'templates').mkdir(parents=True)
(root / 'examples').mkdir(parents=True)

files = {}

def add(path, content):
    files[path] = textwrap.dedent(content).lstrip()

add('SKILL.md', r'''
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
''')

add('README.md', r'''
# Source Code Reading Skill v0.4

A graph-first Agent Skill for large C/C++ systems. It combines architecture reconstruction, source-grounded knowledge modeling, pattern-driven representation, source tracing, document generation, validation, and feedback-driven evolution.

## What changed in v0.4

The skill now treats the **System Atlas / Canonical Knowledge Graph** as the foundation for all topic notes.

```text
System
  ↓
Subsystem
  ↓
Path / Scenario
  ↓
Mechanism
  ↓
Entity
  ↓
Symbol
  ↓
Evidence
```

A note is a view onto this graph, not an isolated Markdown file.

## Package structure

```text
SKILL.md
references/
  architecture-model.md
  architecture-reconstruction.md
  knowledge-model.md
  patterns/
  representation/
  diagrams/
  tracing/
  validation/
  document-policy.md
knowledge-sources/
evolution/
cases/
templates/
examples/
```

## Recommended use

1. Build a System Atlas for the target system once.
2. For each topic, run the six-stage protocol in `SKILL.md`.
3. Store accepted cases under `cases/gold/`.
4. Store recurring failures under `cases/failures/` and `evolution/anti-patterns/`.
5. Propose rule changes only after regression against the gold set.

## Intended targets

Especially suitable for Linux, PostgreSQL, MySQL, databases, operating systems, storage engines, networking stacks, runtimes, compilers, and other large C/C++ systems.
''')

add('references/architecture-model.md', r'''
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
''')

add('references/architecture-reconstruction.md', r'''
# Architecture Reconstruction Method

## Purpose

Use architecture reconstruction when the target is a large existing system whose architecture is only partially documented or where “as-built” architecture may differ from intended design.

## Method

```text
1. Form architecture hypothesis
2. Collect source facts
3. Extract architectural candidates
4. Cluster / aggregate
5. Reconstruct scenarios and runtime paths
6. Map high-level elements to source evidence
7. Compare model against source
8. Refine
```

## Top-down + bottom-up

### Top-down inputs

- official project documentation;
- design documents;
- public APIs and subsystem descriptions;
- build/module boundaries;
- established terminology.

These produce an **architecture hypothesis**, not proof.

### Bottom-up inputs

- symbol references;
- call/dependency graphs;
- AST information;
- data-flow/control-flow evidence;
- lifecycle patterns;
- runtime entry points;
- synchronization and resource ownership.

These provide source evidence for validating or correcting the hypothesis.

## Architecture spine discovery

Start with 5–12 high-level elements that have distinct responsibilities and stable interfaces.

Avoid:

- every source directory;
- every library dependency;
- every background worker;
- every helper function.

## Critical path discovery

Select representative scenarios that traverse multiple subsystems. Typical classes:

```text
request/query path
transaction path
data read path
data write path
recovery path
background maintenance path
startup/shutdown path
```

A critical path is a first-class knowledge object because it connects otherwise isolated subsystems.

## Mapping

Use an explicit mapping model:

```yaml
mapping:
  high_level_element: "Buffer Manager"
  source_symbols: ["BufferDesc", "ReadBuffer_common", "BufferAlloc"]
  source_paths: ["src/backend/storage/buffer"]
  runtime_paths: ["Page Read Path"]
  evidence: []
```

## Refinement rule

When source evidence contradicts architecture documentation, do not silently choose one. Record:

```text
intent / documented architecture
vs
as-built behavior
```

Then decide whether the difference is:

- implementation detail;
- architectural drift;
- obsolete documentation;
- an unresolved ambiguity.

## Architecture reconstruction anti-patterns

- directory-tree-as-architecture;
- single giant architecture diagram;
- architecture inferred from naming alone;
- architecture frozen after the first draft;
- architecture claims without scenario validation.
''')

add('references/knowledge-model.md', r'''
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
''')

add('references/patterns/pattern-catalog.md', r'''
# Pattern Catalog

## Dominant-pattern rule

Choose the pattern that best answers the reader's main question. Secondary patterns support it.

| Pattern | Core question | Strong signals | Typical views |
|---|---|---|---|
| Structural | Who/what is connected? | types, fields, containers | Entity/Relationship, Class, Structure |
| Lifecycle | How is an object born/owned/released? | create/free, refcount, pin/unpin | Lifecycle, Ownership |
| Flow | How does an operation execute? | branch, call path, retry | Flowchart, structured flow |
| State | What states exist and how do they change? | state fields, flags, transitions | State Machine |
| Concurrency | Who shares, protects, waits? | lock, atomics, wait queues | Sync, Sequence |
| Data Path | How does data move/change? | copy, reference, transform | Dataflow, Data Path |
| Resource | How is scarce state located/reused/reclaimed? | pool, cache, eviction, free list | Management/Resource Map |
| Recovery | What happens after failure? | cleanup, rollback, retry | Failure/Recovery Flow |
| Architecture | Where does this fit in the system? | module boundary, APIs, paths | Architecture/Layer |

## Pattern scoring heuristics

Use qualitative scoring, not fake numerical precision:

```text
core-question fit
+ dominant relation density
+ temporal/control complexity
+ runtime relevance
+ user intent
```

## Combination examples

```text
TupleTableSlot
  dominant: Lifecycle
  secondary: Structural, Data Path

Buffer Manager
  dominant: Resource
  secondary: Structural, Lifecycle, State, Concurrency

Lock Manager
  dominant: Concurrency
  secondary: Flow, State, Structural, Resource

Architecture overview
  dominant: Architecture
  secondary: Data Path, Runtime, Dependency
```

## Anti-confusions

```text
Structure Chart  ≠ Flowchart
Call Graph       ≠ Flow
State            ≠ Lifecycle
DFD              ≠ source-level Dataflow
Pointer          ≠ Ownership
Lock presence    ≠ Concurrency understanding
Directory tree   ≠ Architecture
```
''')

add('references/representation/representation-policy.md', r'''
# Representation Policy

## Selection pipeline

```text
Core Question
   ↓
Dominant Pattern
   ↓
Representation Family
   ↓
Concrete Diagram Method
   ↓
Renderer / Tool
```

## Representation families

| Family | Use when | Avoid when |
|---|---|---|
| Entity/Relationship | object topology is the main difficulty | runtime order is the main issue |
| Management/Ownership | ownership/management/resource control is central | only a pointer relation is known |
| Flow/Control | execution path and branch structure matter | calls are merely dependencies |
| State/Lifecycle | state or object life is the key question | only static structure matters |
| Sequence/Interaction | multiple roles interact over time | a single routine is enough |
| Data/Dataflow | data propagation/transformation matters | the issue is only control order |
| Concurrency/Sync | shared state + synchronization matter | a lock is incidental |
| Architecture/Layer | subsystem boundaries and system position matter | topic is too local |
| Recovery/Failure | failure changes system state | normal path only |
| Memory Layout | offsets/alignment/cache-line geometry matter | conceptual relations are sufficient |

## Mermaid vs specialized/manual

### Prefer Mermaid when

- the diagram is conceptual;
- node count is small;
- versionable text is valuable;
- Markdown is the delivery surface;
- exact geometric layout is not part of the semantics.

### Prefer Graphviz or another layout engine when

- the graph is larger;
- automatic edge routing matters;
- layout quality dominates authoring convenience.

### Prefer specialized/static-analysis output when

- exact CFG, AST, dataflow, call graph, or dependency facts matter;
- the graph is machine-derived;
- source-level precision is more important than hand-curated readability.

### Prefer a table or prose when

- the relationship graph is tiny;
- node count is high but semantics are simple;
- the diagram would merely duplicate text.

### Prefer a manually edited diagram when

- exact visual composition is itself part of the explanation;
- publication-quality layout is required;
- formal notation or geometry is important and the chosen renderer cannot preserve it.

## Granularity

Core view target: roughly 5–12 major nodes. Split large graphs into context/core/detail views instead of shrinking every label.

## Graph/text/code division

```text
Graph → spatial/temporal relationship
Text  → semantics, conditions, consequences
Code  → evidence and navigation
```

## Mermaid is never the semantic authority

A Mermaid `flowchart` can render a curated control view, but it should not be called a formal CFG merely because it looks like one. Keep the semantic model independent from rendering syntax.
''')

add('references/diagrams/diagram-catalog.md', r'''
# Diagram Catalog for Source Reading

This catalog exists so an Agent can select a diagram method from semantics rather than from visual habit.

## 1. Entity / ER-style Relationship Map

**Question:** What are the core entities and how are they related?

Traditional/manual concept:

```text
┌───────────────┐       points_to       ┌──────────────┐
│ TupleTableSlot│ ───────────────────→ │ HeapTuple    │
└───────────────┘                      └──────────────┘
```

Mermaid:

```mermaid
flowchart LR
    Slot[TupleTableSlot] -->|points_to| Tuple[HeapTuple]
```

Traditional/manual strengths:
- best for carefully curated semantic grouping;
- easy to emphasize ownership/management labels;
- good for publication and large conceptual layouts.

Mermaid strengths:
- versionable in Git;
- quick to revise;
- natural in Markdown.

Use when the question is “who is connected to whom?”. Do not use when the core question is execution order.

## 2. Structure Chart

**Question:** What is the module hierarchy and calling organization?

Traditional:

```text
             Main
          /    |    \
         A     B     C
              / \
             D   E
```

Mermaid:

```mermaid
flowchart TB
    Main --> A
    Main --> B
    Main --> C
    B --> D
    B --> E
```

Traditional strengths:
- clear hierarchical composition;
- can encode coupling conventions in formal variants.

Mermaid strengths:
- fast and maintainable.

Use when module decomposition/calling hierarchy is central. Do not call this an execution flow without additional evidence.

## 3. Flowchart / Control Flow

**Question:** How does an operation proceed?

Traditional:

```text
Start
  ↓
Lookup
  ↓
Found?
 ┌──┴──┐
Yes    No
 ↓      ↓
Use   Allocate
 └──┬───┘
    ↓
  Return
```

Mermaid:

```mermaid
flowchart TD
    S[Start] --> L[Lookup]
    L --> F{Found?}
    F -->|Yes| U[Use]
    F -->|No| A[Allocate]
    U --> R[Return]
    A --> R
```

Use when branches and execution stages explain the problem. If exact compiler-level CFG is required, use a static-analysis representation instead.

## 4. Nassi–Shneiderman / Structogram

**Question:** What is the structured control composition?

Traditional:

```text
┌───────────────────────┐
│ condition             │
├──────────┬────────────┤
│ path A   │ path B     │
└──────────┴────────────┘
```

Mermaid approximation: use a flowchart or subgraphs; do not pretend it is a formal NS diagram.

Use when sequence/selection/iteration structure is the learning target. Better for explaining structured code than arbitrary cross-jumps.

## 5. HIPO

**Question:** What is the hierarchy, and what is each unit's input/process/output?

Traditional:

```text
System
 ├── A
 │    Input → Process → Output
 └── B
      Input → Process → Output
```

Mermaid:

```mermaid
flowchart TB
    System --> A[Module A]
    System --> B[Module B]
    A --> AIn[Input]
    A --> AProc[Process]
    A --> AOut[Output]
```

Use mainly for legacy/system-function documentation where hierarchy + IPO is the concern.

## 6. DFD / Data Flow Diagram

**Question:** How does information move through processes and stores?

Traditional:

```text
Client ──request──→ Process ──record──→ Storage
```

Mermaid approximation:

```mermaid
flowchart LR
    Client -->|request| Process
    Process -->|record| Storage
```

Use when conceptual data movement matters. For variable-level source analysis, prefer a dataflow/CodeQL/Clang result.

## 7. State Diagram

**Question:** How does an object change state?

Traditional:

```text
FREE --allocate--> ACTIVE --modify--> DIRTY
DIRTY --flush--> CLEAN --release--> FREE
```

Mermaid:

```mermaid
stateDiagram-v2
    [*] --> FREE
    FREE --> ACTIVE: allocate
    ACTIVE --> DIRTY: modify
    DIRTY --> CLEAN: flush
    CLEAN --> FREE: release
```

Use when transitions and guards are the key semantics.

## 8. Lifecycle Diagram

**Question:** What is the object's lifetime from creation to destruction?

Traditional:

```text
create → initialize → publish → use → release → destroy
```

Mermaid can use a flowchart or state diagram, but label it as Lifecycle View, not necessarily State Machine.

Use for ownership/resource validity questions.

## 9. Sequence Diagram

**Question:** How do several actors interact over time?

Traditional:

```text
Client       LockMgr        WaitQueue
  │             │               │
  │ acquire     │               │
  ├────────────→│               │
  │             │ conflict      │
  │             ├──────────────→│
  │             │               │
  │←────────────┤               │
```

Mermaid:

```mermaid
sequenceDiagram
    participant C as Client
    participant L as LockMgr
    participant W as WaitQueue
    C->>L: acquire()
    L->>W: enqueue()
    L-->>C: wait
```

Use when roles and temporal interaction matter. If there is only one linear function path, a flowchart is usually simpler.

## 10. Activity Diagram

**Question:** What activities and parallel branches form a behavior?

Traditional: UML activity notation.

Mermaid approximation:

```mermaid
flowchart TD
    A[Start] --> B[Validate]
    B --> C[Process A]
    B --> D[Process B]
    C --> E[Join]
    D --> E
```

Use for behavior with parallel/guarded activities. For exact formal UML semantics, use a UML-capable tool.

## 11. Petri Net

**Question:** How do concurrent tokens/resources move through synchronization points?

Conceptual:

```text
● → [acquire] → ● → [wait] → ●
```

Mermaid is not a substitute for a formal Petri Net renderer. Use a specialized/manual tool when token semantics, reachability, deadlock, or formal concurrency properties matter.

## 12. Call Graph

**Question:** Who may call whom?

Mermaid:

```mermaid
flowchart TD
    A --> B
    A --> C
    B --> D
```

Use for navigation and dependency discovery. Do not automatically present it as runtime order.

For large machine-derived call graphs, Doxygen, clang tooling, or other analyzers are better sources; a curated Mermaid view should be a distilled projection.

## 13. Control-flow Graph (CFG)

**Question:** What are the possible basic-block control paths?

Conceptual:

```text
Entry → A → Branch ─→ B → Exit
              └──────→ C ───┘
```

Use a compiler/static-analysis backend when exactness matters. Mermaid is suitable only for a simplified explanatory projection.

## 14. Data-flow Graph

**Question:** How does a value or memory state propagate?

Conceptual:

```text
input → decode → transform → store → output
```

For source-accurate variable/value propagation, prefer Clang Dataflow or CodeQL over hand-authored Mermaid.

## 15. Dependency Graph

**Question:** What depends on what?

Traditional:

```text
A → B → C
A → D
```

Mermaid:

```mermaid
flowchart LR
    A --> B
    B --> C
    A --> D
```

Use for modules, headers, libraries, packages, or components. Avoid calling dependency a runtime call.

## 16. Component / Architecture View

**Question:** Where is a subsystem/module in the larger system?

Mermaid example:

```mermaid
flowchart TB
    Frontend --> Execution
    Execution --> Storage
    Storage --> Persistence
```

For large formal architecture documentation, C4/Structurizr or UML may be more appropriate.

## 17. Deployment View

**Question:** Which runtime process/service is deployed where?

Traditional:

```text
[Client] → [DB Server] → [Storage]
```

Mermaid can approximate this with flowcharts, but deployment semantics should be preserved when topology matters.

## 18. Memory Layout View

**Question:** What is the actual in-memory geometry?

Traditional/manual:

```text
+0    tag
+16   state
+24   lock
+40   padding
```

Mermaid is a poor choice when exact offsets, alignment, cache lines, or ABI geometry are semantically important. Prefer a table, generated layout output, or a custom diagram.

## 19. Ownership Graph

**Question:** Who owns, borrows, retains, or releases an object?

```mermaid
flowchart LR
    Manager -->|owns| Object
    Client -->|borrows| Object
```

Use only when lifetime evidence supports the ownership relation. Raw pointer presence alone is insufficient.

## 20. Synchronization Graph

**Question:** Who shares what, and what protects it?

```mermaid
flowchart TB
    A[Thread A] --> Shared[Shared State]
    B[Thread B] --> Shared
    Lock[Lock] -->|protects| Shared
```

Use when protected state is known. Add Sequence when timing of acquire/wait/wake matters.

## 21. Resource / Cache Map

**Question:** How is a scarce/shared resource indexed, allocated, reused, and reclaimed?

```mermaid
flowchart LR
    Request --> Lookup
    Lookup --> Hit
    Lookup --> Miss
    Miss --> Allocate
    Allocate --> Resource
    Hit --> Resource
```

Use for buffer pools, caches, free lists, object pools, connection pools, registries.

## 22. Failure / Recovery View

**Question:** What happens after an error and how is consistency preserved?

```mermaid
flowchart TD
    A[Normal] --> B[Operation]
    B -->|success| C[Continue]
    B -->|failure| D[Cleanup]
    D --> E[Rollback]
    E --> F[Retry / Abort / Recover]
```

Use when partial state and cleanup semantics matter.

## 23. Decision matrix for the Agent

```text
“Who/what is connected?”
  → Entity/Relationship

“Who manages/owns what?”
  → Management/Ownership

“How does the operation run?”
  → Flow / Activity

“Who calls whom?”
  → Call Graph

“What states exist and change?”
  → State Diagram

“How long does this object live?”
  → Lifecycle

“How do actors interact over time?”
  → Sequence

“How does data move?”
  → Data Path / DFD / Dataflow

“How is shared state synchronized?”
  → Synchronization / Sequence

“How is a scarce resource managed?”
  → Resource / Cache Map

“How does the subsystem fit the system?”
  → Architecture / Component

“How does memory actually look?”
  → Memory Layout

“How does failure recover?”
  → Failure / Recovery
```

## Traditional vs Mermaid summary

| Goal | Traditional/manual | Mermaid | Recommendation |
|---|---|---|---|
| quick conceptual graph | very flexible | excellent | Mermaid |
| Markdown/Git maintenance | poor | excellent | Mermaid |
| exact geometric layout | excellent | limited | manual/specialized |
| formal UML semantics | excellent with UML tool | partial/not universal | UML tool |
| huge graph layout | manual effort | can become dense | Graphviz/specialized |
| exact CFG/dataflow | not ideal manually | not authoritative | analysis backend |
| memory offsets/cache lines | excellent | poor | table/custom |
| publication-quality architecture | excellent | adequate for simple views | specialized/manual when needed |

The key rule is not “Mermaid first”. The key rule is **semantic method first, renderer second**.
''')

add('references/tracing/trace-policy.md', r'''
# Trace Policy

## Claim-centered tracing

Trace only enough source to prove or qualify a claim.

```text
Claim
 ↓
Definition evidence
 ↓
Use/mutation evidence
 ↓
Relevant caller/callee or state/lifecycle evidence
 ↓
Stop when the claim is proven
```

## Trace depth

```text
D1 Local
D2 Structural
D3 System
```

Use D1 for local facts, D2 for cross-symbol semantics, and D3 for architecture/runtime explanations.

## Source anchors

Prefer:

```text
repository + revision
path
qualified symbol
field/expression
code region
```

Use line ranges as helpful navigation, not as the only identity.

## Trace types

```text
definition
reference
read
write
call
return
state-transition
lifecycle
ownership
synchronization
resource-management
architecture-mapping
```

## Trace expansion

Expand only when the current evidence does not answer the open question.

## Boundaries

Record `trace_boundary` when deeper implementation exists but is irrelevant to the current claim.

## Conflicts

When comment/documentation and implementation disagree, retain both evidence sources and flag the conflict.
''')

add('references/tracing/claim-verification.md', r'''
# Claim Verification

## Claim states

```text
SUPPORTED
PARTIALLY_SUPPORTED
UNVERIFIED
CONFLICTING
```

## Epistemic labels

### FACT
Directly observable from source or authoritative target-project documentation.

### INFERENCE
Derived from multiple facts.

### INTERPRETATION
An explanation of rationale/design intent not directly established by code.

## Verification rules

1. Every substantial claim has at least one evidence anchor.
2. Claims about semantics usually require multiple evidence points: definition + reads/writes or behavior.
3. Ownership requires lifetime evidence.
4. Synchronization claims require the protected state and access context.
5. State claims require transition evidence, not only a field name.
6. Design-intent claims require comments/design documentation or must be explicitly qualified as interpretation.
7. Architecture claims require mapping evidence from high-level concepts to source/runtime facts.

## Confidence

```text
HIGH   — directly demonstrated by strong source evidence
MEDIUM — stable inference from multiple facts
LOW    — plausible but evidence incomplete
```

## Example

```yaml
claim:
  statement: "content_lock protects page contents"
  type: FACT
  confidence: HIGH
  evidence:
    - LockBuffer()
    - page access between lock/unlock
```

## Unsupported claim repair

```text
Unsupported → search readers/writers/callers → update evidence → re-evaluate
                                  ↓
                         still unsupported
                                  ↓
                         qualify or remove
```
''')

add('references/validation/validation-policy.md', r'''
# Validation Policy

## Validation layers

### V1 Structural

- core question exists;
- architecture position exists when applicable;
- primary view exists when useful;
- source navigation exists;
- next reading exists when useful.

### V2 Semantic

- entity relations are supported;
- ownership is not confused with referencing;
- flow is not confused with call graph;
- state transitions are real;
- synchronization target is real;
- data movement distinguishes copy/reference when material.

### V3 Traceability

Every major claim must resolve:

```text
Claim → Evidence → Source Anchor
```

### V4 Representation

- primary representation matches dominant pattern;
- graph is not overloaded;
- diagram does not duplicate prose;
- renderer is capable of expressing the chosen semantics;
- specialized tools are used when precision matters.

### V5 Reader/navigation

A reader should be able to answer:

```text
Where am I?
What is the core mechanism?
Why does it matter?
Which path uses it?
Where is the source?
What should I read next?
```

### V6 Architecture consistency

- topic coordinates resolve to the current atlas;
- source evidence does not contradict the architecture without a recorded conflict;
- critical paths have no unexplained gaps.

## Revision routing

On validation failure, route to the minimum repair stage:

```text
scope/context missing      → Stage 1
knowledge missing          → Stage 2
wrong abstraction/pattern  → Stage 3
unsupported claim          → Stage 4
bad diagram/document       → Stage 5
cross-layer inconsistency  → Stage 6, then earlier stage as needed
```
''')

add('references/document-policy.md', r'''
# Document Policy

## Purpose

A source-reading document is a **view of the verified knowledge graph**, optimized for a particular question and reader.

## Recommended skeleton

```text
# Title

> Core Question

## System position

## 一句话模型

## 1. 核心对象

## 2. 核心路径 / 行为

## 3. 状态 / 生命周期

## 4. 并发 / 资源 / 约束

## 5. 关键实现

## 6. 源码导读

## 7. 关键结论

## 8. 下一步阅读
```

Only include sections supported by the pattern profile.

## System position

For large systems, show the zoom path:

```text
System → Subsystem → Path → Topic
```

This should orient, not repeat the whole architecture atlas.

## One-sentence model

Give the smallest accurate mental model before detail.

## Primary View

Place the dominant representation near the point where the reader needs it.

## Object cards

Use compact cards for important entities:

```text
### BufferDesc

职责：...
关键字段：...
管理者：...
生命周期：...
```

## Source snippets

Use short, purposeful snippets. The snippet must have a reason: structure, branch, transition, lock, ownership, cleanup, or other decisive evidence.

## Source navigation

Every important topic should have a path such as:

```text
Current concept
  → current symbol
  → next symbol
  → why to continue
```

## Cross-chapter links

Prefer canonical references instead of duplicating definitions. A note should feel like one window into a shared graph.

## Style

Prefer exact source names, condition-oriented prose, concise paragraphs, tables for compact properties, and diagrams only when they reduce cognitive load.

Avoid source dumps, boilerplate, praise-heavy prose, unsupported intent claims, and diagram-as-decoration.
''')

add('knowledge-sources/index.yaml', r'''
version: 0.4.0
name: source-reading-knowledge-sources
purpose: >-
  Curated external resources that teach the skill methodology, notation,
  rendering, source-analysis techniques, language/system semantics, and mature
  project documentation practices.

policy:
  source_of_truth:
    target_repository_facts: target_source_code
    target_project_behavior: target_source_code_plus_official_project_docs
    notation_semantics: registered_standards_or_methodology
    renderer_capabilities: official_tool_docs
  priority:
    - target_repository_and_project_docs
    - standards_or_original_methodology
    - official_tool_docs
    - mature_project_examples
    - books_and_textbooks
    - community_material
  external_sources_may:
    - define notation semantics
    - teach methodology
    - provide examples and anti-patterns
    - suggest analysis techniques
    - establish tool capabilities
  external_sources_may_not:
    - override target repository facts
    - prove target source behavior without target evidence
    - turn renderer syntax into a formal notation by resemblance alone

resource_schema:
  required:
    - id
    - name
    - category
    - authority
    - url
    - verification
    - teaches
    - query_when
    - do_not_use_when
    - direct_fact_scope
    - extract_to_rules
  categories:
    - methodology
    - standard
    - renderer
    - analysis_tool
    - project_example
    - language_semantics
    - archival
resources:
''')

resources = [
('uml-omg','OMG UML','standard','Tier-1','https://www.omg.org/spec/UML/About-UML/','UML semantics and diagram vocabulary','When choosing or checking Class, Sequence, State, Activity, Component, Deployment semantics','Do not use to infer target-code facts','Defines UML notation semantics; not target-code behavior',['formal_notation_guard','view_semantics']),
('iso-42010','ISO/IEC/IEEE 42010','standard','Tier-1','https://www.iso.org/standard/74393.html','Architecture description concepts: concern, viewpoint, view, architecture description','When designing architecture viewpoints or distinguishing architecture concerns','Do not use it as a source of implementation facts','Architecture description methodology/vocabulary',['concern_viewpoint_rule','architecture_description_guard']),
('sei-vab','SEI Views and Beyond','methodology','Tier-1','https://www.sei.cmu.edu/library/views-and-beyond-collection/','View selection, documentation structure, cross-view consistency','When deciding which architecture views to document','Not a source of C/C++ runtime truth','Architecture documentation method',['view_selection','view_completeness']),
('c4model','C4 Model','methodology','Tier-1','https://c4model.com/','Hierarchical architecture visualization and zoom levels','When creating system/container/component/code-oriented architecture views','Do not force all four levels or treat them as source truth','Architecture abstraction and view selection',['control_abstraction_depth','one_model_multiple_views']),
('arc42','arc42','methodology','Tier-2','https://docs.arc42.org/','Practical structure for architecture documentation','When organizing a larger documentation set and cross-cutting concepts','Do not force a section into a source-reading note if the concern is absent','Document section selection',['section_selection','cross_cutting_concepts']),
('yourdon-constantine','Yourdon/Constantine Structured Design','methodology','Tier-1','https://vtda.org/books/Computing/Programming/StructuredDesign_EdwardYourdonLarryConstantine.pdf','Structure charts and distinction from control/data flow','When distinguishing modular structure from execution flow','Historical material; do not treat every legacy convention as mandatory today','structure_vs_control_flow',['structure_vs_control_flow','module_decomposition']),
('nassi-shneiderman','Nassi-Shneiderman / Structured Programming','methodology','Tier-1','https://www.cs.umd.edu/~ben/publications.html','Structured sequence/selection/iteration representations','When structured control composition is the learning target','Not suitable for arbitrary cross-jump or system architecture views','structured_flow',['structured_flow']),
('jsp','Jackson Structured Programming','methodology','Tier-1','https://link.springer.com/book/10.1007/978-1-349-22081-6','Data-structure-first program structuring','When data structure strongly determines control/program structure','Do not assume modern systems were designed using JSP','data_structure_first',['data_structure_first']),
('hipo','IBM HIPO archival material','archival','Tier-2','https://www.bitsavers.org/pdf/ibm/generalInfo/GC20-1850-0_Improved_Programming_Technologies_-_An_Overview_1st_ed_197410.pdf','Hierarchy + Input/Process/Output','When documenting legacy function hierarchies and IPO','Legacy projects where the method adds unnecessary ceremony','Legacy methodology',['legacy_hipo_trigger']),
('mermaid','Mermaid','renderer','Tier-2','https://mermaid.js.org/intro/syntax-reference.html','Text-based diagram rendering in Markdown','When a conceptual/versionable diagram is sufficient','Do not use as a substitute for formal semantics or exact static-analysis output','Renderer syntax/capabilities',['renderer_capability','mermaid_selection']),
('plantuml','PlantUML','renderer','Tier-2','https://plantuml.com/','Text-based UML-oriented rendering','When UML-like diagrams need more formal notation support than Mermaid','Do not treat renderer support as proof of formal conformance','UML rendering',['renderer_fallback']),
('graphviz','Graphviz','renderer','Tier-2','https://graphviz.org/documentation/','Graph layout, especially directed graphs','When graph size/layout becomes the problem','Do not use to infer graph semantics','Graph rendering only',['graph_layout_escalation']),
('structurizr','Structurizr','renderer','Tier-2','https://docs.structurizr.com/','Model-as-code with multiple views; C4-oriented patterns','When one architecture model must drive multiple views','Do not use as target-code semantic proof','Model/view separation',['one_model_multiple_views']),
('clang-ast','Clang AST / LibTooling','analysis_tool','Tier-2','https://clang.llvm.org/docs/LibASTMatchers.html','Semantic C/C++ AST matching and source locations','When grep/text matching is insufficient for type/symbol/source relationships','AST does not by itself establish runtime ownership semantics','Semantic source extraction',['semantic_source_extraction','source_anchor_precision']),
('clang-dataflow','Clang Dataflow','analysis_tool','Tier-2','https://clang.llvm.org/docs/DataFlowAnalysisIntro.html','Static dataflow analysis concepts and tooling','When source-level dataflow/analysis precision matters','Do not treat static possibilities as observed runtime execution','Dataflow analysis',['analysis_backend_selection']),
('codeql-cpp','CodeQL for C/C++','analysis_tool','Tier-2','https://codeql.github.com/docs/codeql-language-guides/codeql-for-cpp/','AST, control flow, dataflow and queryable source relationships','When exact source-graph or dataflow queries are needed','CodeQL findings still require interpretation in target context','Source analysis queries',['analysis_backend_selection','pointer_semantics_guard']),
('doxygen','Doxygen','analysis_tool','Tier-2','https://www.doxygen.nl/','Generated documentation and call/dependency graphs','For fast source orientation and generated graph candidates','Generated call graphs are not automatically runtime flow','Generated graph as input',['generated_graph_as_input']),
('sourcegraph','Sourcegraph','analysis_tool','Tier-2','https://sourcegraph.com/docs','Large-repository code navigation and search','When symbol navigation/search at repository scale is needed','Tool index is navigation aid, not semantic truth','Repository navigation',['navigation_backend']),
('cpp-guidelines','C++ Core Guidelines','language_semantics','Tier-1','https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines','Ownership vocabulary, RAII, pointer/reference guidance','When reasoning about generic C++ ownership/lifetime concepts','Never override target-project behavior or infer ownership from a raw pointer','Language guardrails',['ownership_guardrail','lifetime_vocabulary']),
('linux-locking','Linux Kernel Locking Documentation','project_example','Tier-2','https://www.kernel.org/doc/html/latest/locking/index.html','Real-world lock semantics, lock types, locking rules','When learning concurrency documentation patterns or Linux locking concepts','Do not directly transfer Linux lock semantics to PostgreSQL/MySQL','Concurrency semantics and examples',['concurrency_guardrail']),
('lkmm','Linux Kernel Memory Model','project_example','Tier-2','https://docs.kernel.org/dev-tools/lkmm/index.html','Memory ordering, barriers, litmus-style reasoning','When analyzing low-level atomic/order constraints','Only relevant when memory ordering is actually part of the topic','Ordering guardrail',['memory_ordering_guardrail']),
('postgres-coding','PostgreSQL Developer / Coding','project_example','Tier-2','https://www.postgresql.org/developer/coding/','Project-native source navigation and backend flowchart examples','When building a PostgreSQL System Atlas or source-reading navigation','PostgreSQL-specific patterns should not be generalized blindly to other systems','Project-specific navigation',['project_specific_source_navigation']),
]
for row in resources:
    rid,name,cat,auth,url,teaches,query,donot,direct,extracts=row
    files['knowledge-sources/index.yaml'] += f"""  - id: {rid}\n    name: {name}\n    category: {cat}\n    authority: {auth}\n    url: {url}\n    verification: verified-for-registry-v0.4\n    teaches: {teaches}\n    query_when: {query}\n    do_not_use_when: {donot}\n    direct_fact_scope: {direct}\n    extract_to_rules: {extracts}\n    \n"""

add('knowledge-sources/resource-advisor.md', r'''
# Resource Advisor

## Purpose

Choose external material only when the internal skill rules or target-source evidence are insufficient for the current decision.

## Decision table

| Need | First source class | Example resources | Expected extracted rule |
|---|---|---|---|
| architecture viewpoints | standards/methodology | ISO 42010, SEI V&B | concern/viewpoint/view selection |
| architecture zoom | methodology | C4, Structurizr | abstraction depth / one model, many views |
| documentation organization | methodology | arc42, SEI | section and cross-cutting organization |
| distinguish structure vs control | historical method | Yourdon/Constantine, NS | structure_vs_control_flow |
| data-centric program modeling | methodology | JSP, DFD | data_structure_first / dataflow semantics |
| renderer capability | official tool docs | Mermaid, PlantUML, Graphviz | renderer selection |
| C++ ownership vocabulary | language guidance | C++ Core Guidelines | ownership guardrails |
| source graph extraction | analysis tools | Clang, CodeQL, Doxygen, Sourcegraph | source-analysis backend choice |
| concurrency semantics | system docs | Linux locking, LKMM | synchronization/order guardrails |
| project-native example | mature project docs | PostgreSQL | project-specific navigation conventions |

## When to consult

Consult when:

```text
rule ambiguity
method selection uncertainty
unfamiliar diagram notation
renderer limitation
analysis precision problem
new recurring failure pattern
```

Do not consult merely to decorate a document with citations.

## How to extract a lesson

Do not copy a paragraph into the skill. Convert the source into:

```text
Principle
Trigger
Do / Don't
Example
Boundary
Candidate Rule
```

## Authority boundaries

- External methodology defines the method.
- Official renderer docs define tool capability.
- Target source defines target implementation facts.
- Human-approved project cases define local preferences.

## Learning loop

```text
External source
   ↓
Principle extraction
   ↓
Candidate rule
   ↓
Target-source test
   ↓
Case / regression
   ↓
Adopt or reject
```
''')

add('knowledge-sources/selection-matrix.md', r'''
# Knowledge Source Selection Matrix

```text
Architecture concern?
  → ISO 42010 / SEI / C4 / arc42

Need formal UML semantics?
  → OMG UML

Need structure vs flow distinction?
  → Yourdon/Constantine / NS

Need legacy hierarchy + IPO?
  → HIPO

Need data-structure-first modeling?
  → JSP

Need diagram rendering?
  → Mermaid / PlantUML / Graphviz

Need model + multiple views?
  → Structurizr

Need exact C/C++ symbol relationships?
  → Clang AST

Need exact source-level dataflow / query?
  → CodeQL / Clang Dataflow

Need generated orientation graph?
  → Doxygen

Need large-repository navigation?
  → Sourcegraph

Need C++ ownership vocabulary?
  → C++ Core Guidelines

Need Linux concurrency/memory-order examples?
  → Linux locking / LKMM

Need PostgreSQL-native examples?
  → PostgreSQL developer/coding docs
```

Always apply the authority boundary from `index.yaml`.
''')

add('evolution/evolution-policy.md', r'''
# Evolution Policy

## Goal

Improve the skill without allowing uncontrolled self-modification.

## Four levels

```text
L1 Current-task correction
L2 Reusable case
L3 Candidate rule
L4 Adopted skill change
```

## Safe loop

```text
Generated result
   ↓
Human/project feedback
   ↓
Failure classification
   ↓
Case record
   ↓
Candidate rule
   ↓
Regression against gold cases
   ↓
Human/project approval
   ↓
Rule adoption
```

## Rule proposal requirements

A proposal must include:

```text
problem
trigger
bad behavior
desired behavior
rationale
evidence cases
regression cases
possible side effects
status
```

## Never auto-promote

An Agent may generate a candidate rule, but must not silently modify the normative skill rules. Adoption should be explicit in the engineering workflow.

## Anti-pattern learning

Recurring failures should be named and stored. Examples:

```text
giant-diagram
pointer-is-ownership
call-graph-is-flow
source-location-spam
unsupported-design-intent
architecture-from-directories
view-without-core-question
```

## External learning

External sources can trigger candidate rules, but target-source replay is mandatory before adoption.
''')

add('evolution/feedback-taxonomy.md', r'''
# Feedback Taxonomy

Classify feedback before changing a rule.

```text
F1 Accuracy
F2 Missing Knowledge
F3 Wrong Architecture Position
F4 Wrong Pattern
F5 Wrong Relationship Semantics
F6 Wrong Representation
F7 Wrong Granularity
F8 Wrong Source Anchor
F9 Redundancy
F10 Readability
F11 Navigation
F12 Unsupported Interpretation
F13 Missing Constraint/Invariant
F14 Cross-view inconsistency
```

## Diagnosis questions

For “图画得不好”，ask internally:

```text
method wrong?
entity set wrong?
edge semantics wrong?
granularity wrong?
layout wrong?
reader context missing?
formal semantics required?
```

Convert the feedback into a structured case, not a vague preference statement.
''')

add('evolution/rule-proposal.md', r'''
# Rule Proposal Template

```yaml
rule_proposal:
  id: ""
  title: ""
  problem_type: ""
  trigger:
    pattern: ""
    representation: ""
    context: ""
  bad_behavior: ""
  desired_behavior: ""
  rationale: ""
  do:
    - ""
  avoid:
    - ""
  evidence_cases:
    - ""
  regression_cases:
    - ""
  external_sources:
    - ""
  side_effects:
    - ""
  status: proposed
```
''')

add('evolution/case-learning.md', r'''
# Case Learning

## Case structure

A useful case stores the full decision context, not just the final Markdown.

```text
Case
├── task
├── source context
├── architecture position
├── knowledge model
├── pattern profile
├── representation plan
├── generated document
├── feedback
├── failure analysis
├── correction
└── learned rule(s)
```

## Gold case

A human/project-reviewed result that is suitable for regression.

## Failure case

A result that exposes a repeatable weakness. Failure cases are valuable only when the failure reason is recorded.

## Case similarity

Retrieve similar cases using:

```text
system domain
core question
pattern
representation family
relationship type
source language
failure type
```

Do not treat lexical similarity alone as semantic similarity.
''')

add('evolution/regression.md', r'''
# Regression Policy

## Purpose

Prevent a local improvement from damaging previously accepted behavior.

## Regression suite

At minimum maintain representative gold cases for:

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

For each new diagram rule, replay at least:

```text
one positive case
one borderline case
one previous failure
one unrelated case
```

## Result classes

```text
PASS
IMPROVED
NO_CHANGE
REGRESSION
AMBIGUOUS
```

## Adoption rule

A candidate rule is not adopted when it introduces a material regression in a canonical gold case without an explicit decision to change that gold case.

## Regression report

```yaml
regression:
  proposal: ""
  cases:
    - id: ""
      result: PASS | REGRESSION | AMBIGUOUS
      note: ""
  summary: ""
  decision: adopt | revise | reject
```
''')

anti = {
'giant-diagram.md': '# Anti-pattern: Giant Diagram\n\n**Symptom:** dozens of nodes and crossing edges in one view.\n\n**Repair:** identify the core question; keep 5–12 core nodes; split context/core/detail views.\n',
'pointer-is-ownership.md': '# Anti-pattern: Pointer Means Ownership\n\n**Symptom:** `A *b` is rendered as `A owns B`.\n\n**Repair:** trace allocation, lifetime, release, transfer, and reference conventions before asserting ownership.\n',
'call-graph-is-flow.md': '# Anti-pattern: Call Graph Means Runtime Flow\n\n**Symptom:** every call edge is placed on a single linear execution path.\n\n**Repair:** inspect branches, callbacks, deferred work, parallelism, and runtime conditions.\n',
'architecture-from-directories.md': '# Anti-pattern: Directory Tree Is Architecture\n\n**Symptom:** folders are directly promoted to subsystems.\n\n**Repair:** validate responsibility, dependency, runtime collaboration, resource ownership, and public boundaries.\n',
'unsupported-design-intent.md': '# Anti-pattern: Unsupported Design Intent\n\n**Symptom:** “this exists to improve performance” is stated from code shape alone.\n\n**Repair:** separate FACT, INFERENCE, and INTERPRETATION and cite comments/design evidence when available.\n',
}
for p,c in anti.items(): add('evolution/anti-patterns/'+p,c)

add('templates/knowledge-model.yaml', r'''
source_context:
  repository: ""
  revision: ""
  subject: ""
  core_questions: []
  included_modules: []
  excluded_modules: []
  architecture_position:
    system: ""
    subsystem: ""
    layer: ""
    paths: []
    concerns: []
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
  core_question: ""
  dominant:
    name: ""
    reason: ""
  secondary: []

representation:
  primary:
    family: ""
    method: ""
    renderer: ""
    purpose: ""
  secondary: []
  source_anchors: []
  snippets: []
  exclusions: []

validation:
  structural: pass
  semantic: pass
  traceability: pass
  representation: pass
  reader_navigation: pass
  architecture_consistency: pass
''')

add('templates/source-reading-note.md', r'''
# {{TITLE}}

> **Core Question**：{{CORE_QUESTION}}

## 系统位置

```text
{{SYSTEM}} → {{SUBSYSTEM}} → {{PATH}} → {{TOPIC}}
```

## 一句话模型

{{MENTAL_MODEL}}

{{PRIMARY_VIEW}}

## 1. 核心对象

{{ENTITIES}}

## 2. 核心路径 / 行为

{{FLOW_OR_DATA_PATH_OR_SEQUENCE}}

## 3. 关键状态 / 生命周期

{{STATE_OR_LIFECYCLE}}

## 4. 并发 / 资源 / 约束

{{CONCURRENCY_RESOURCE_INVARIANTS}}

## 5. 关键实现

{{IMPLEMENTATION_EXPLANATION}}

### 关键源码

```c
{{SNIPPET}}
```

{{SNIPPET_EXPLANATION}}

## 6. 源码导读

| 目标 | Symbol | 下一跳 | 为什么继续 |
|---|---|---|---|
| {{PURPOSE}} | `{{SYMBOL}}` | `{{NEXT_SYMBOL}}` | {{REASON}} |

## 7. 关键结论

{{CLAIMS}}

## 8. 下一步阅读

{{NEXT_READING}}
''')

add('templates/review-report.md', r'''
# Source Note Review

## Scope

{{SCOPE}}

## Architecture position

{{ARCHITECTURE_POSITION}}

## Findings

| Severity | Type | Location | Finding | Evidence | Repair |
|---|---|---|---|---|---|
| {{SEVERITY}} | {{TYPE}} | {{LOCATION}} | {{FINDING}} | {{EVIDENCE}} | {{REPAIR}} |

## Pattern assessment

Dominant: {{DOMINANT_PATTERN}}

Secondary: {{SECONDARY_PATTERNS}}

## Traceability gaps

{{TRACE_GAPS}}

## Representation issues

{{REPRESENTATION_ISSUES}}

## Navigation issues

{{NAVIGATION_ISSUES}}

## Evolution candidates

{{RULE_PROPOSALS}}

## Overall readiness

{{READINESS}}
''')

add('templates/feedback.yaml', r'''
feedback:
  case_id: ""
  target: ""
  severity: high | medium | low
  type: F1
  user_observation: ""
  underlying_problem: ""
  desired_correction: ""
  evidence: []
  candidate_rule: ""
''')

add('examples/system-atlas-postgresql.yaml', r'''
system: PostgreSQL
architecture_spine:
  - id: frontend
    role: protocol, parsing, session entry
  - id: execution
    role: planning and executor runtime
  - id: transaction
    role: transaction/locking/concurrency semantics
  - id: storage
    role: access methods, buffers, storage manager
  - id: persistence
    role: WAL, files, IO
paths:
  - id: query_path
    steps: [frontend, execution, storage]
  - id: page_read_path
    steps: [execution, storage, persistence]
  - id: transaction_path
    steps: [execution, transaction, storage, persistence]
concerns:
  - concurrency
  - memory
  - durability
  - performance
note: "Illustrative architecture scaffold; validate against the target revision before treating any relation as a repository fact."
''')

add('examples/representation-plan.yaml', r'''
subject: BufferLookup
architecture:
  subsystem: Storage / Buffer Manager
  path: Page Read Path
core_question: "BufferTag 如何定位到具体 Buffer，并在哪里发生并发保护？"
pattern:
  dominant: Resource
  secondary: [Structural, Concurrency]
representation:
  primary:
    family: Resource
    method: Resource / Index Map
    renderer: Mermaid
  secondary:
    - family: Structural
      method: Entity Relationship
      renderer: Mermaid
    - family: Concurrency
      method: Synchronization Graph
      renderer: Mermaid
exclude:
  - full call graph
  - unrelated replacement policy
''')

add('examples/evolution-case.yaml', r'''
case_id: buffer-management-chain-001
kind: feedback_case
context:
  pattern: Resource
  representation: Entity Relationship
observation: "图把 lookup 主链埋在了大量函数节点里。"
classification: F6
failure:
  type: wrong_representation_granularity
  detail: "implementation-level call nodes dominated the management relationship."
correction:
  keep:
    - BufferTag
    - BufTable
    - BufferDesc
  suppress:
    - incidental helper calls
candidate_rule:
  title: prefer-management-backbone
  trigger: "Resource + Entity Relationship"
  behavior: "Prefer identity/index/managed-resource chain; suppress incidental call edges in the primary view."
status: proposed
''')

add('cases/gold/README.md', r'''
# Gold Cases

Store reviewed cases here. A case should preserve the decision context, not just the final note.

Recommended:

```text
case.yaml
source-context.yaml
knowledge-model.yaml
pattern.yaml
representation.yaml
document.md
review.yaml
```
''')
add('cases/failures/README.md', r'''
# Failure Cases

Store repeatable failures with their classification, evidence, repair, and whether a rule proposal resulted.
''')

# Add a compact architecture example note to illustrate the integrated zooming model.
add('examples/architecture-driven-note.md', r'''
# Buffer Lookup：从系统架构到源码

> **Core Question**：BufferTag 如何在 PostgreSQL Storage 中定位到对应的 BufferDesc？

## 系统位置

```text
PostgreSQL
  → Storage
    → Page Read Path
      → Buffer Lookup
```

## 一句话模型

Buffer Lookup 是 Page Read Path 中把逻辑 page identity 映射到具体 buffer metadata 的资源定位机制；理解它首先需要看 `BufferTag`、mapping structure 和 `BufferDesc` 的关系，再进入 hash/partition 的实现细节。

## 主视图：Management / Resource

```mermaid
flowchart LR
    Tag[BufferTag] -->|identity / hash| Table[BufTable]
    Table -->|locates| Desc[BufferDesc]
    Desc -->|represents| Buffer[Shared Buffer]
```

## 源码导读

```text
Buffer lookup concept
  → BufferTag
  → BufTable / hash helper
  → BufferDesc
  → ReadBuffer / allocation path
```

注意：图中只表达理解该问题所需的关系，不把完整 call graph 塞进主视图。
''')

# Write all
for path, content in files.items():
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')

# Validate YAML files
for p in root.rglob('*.yaml'):
    yaml.safe_load(p.read_text(encoding='utf-8'))

# Create zip
zip_path = Path('/mnt/data/source-code-reading-skill-v0.4.zip')
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in sorted(root.parent.rglob('*')):
        if p.is_file():
            z.write(p, p.relative_to(root.parent.parent))

print('files', len([p for p in root.rglob('*') if p.is_file()]))
print('zip', zip_path, zip_path.stat().st_size)
print('resources', len(resources))