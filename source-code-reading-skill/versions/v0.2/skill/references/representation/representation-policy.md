# Representation Policy

## 1. Core rule

Representation selection is driven by:

```text
Core Question
  ↓
Dominant Pattern
  ↓
Representation Family
  ↓
Concrete Diagram Type
  ↓
Renderer
```

The renderer is not the semantic model. Mermaid, draw.io, Visio, a UML editor, or a static-analysis tool are presentation choices.

## 2. Pattern → family defaults

| Pattern | Default representation family | Typical primary view |
|---|---|---|
| Structural | Structural | Entity/ER/Class/Management |
| Lifecycle | State/Lifecycle | Lifecycle / Ownership |
| Flow | Control | Flowchart |
| State | State/Lifecycle | State diagram |
| Concurrency | Interaction/Concurrency | Synchronization + Sequence |
| Data Path | Data | Data Path / DFD-style |
| Resource | Resource | Resource/Management/Index |
| Recovery | Failure | Recovery flow |
| Architecture | Architecture | Component/Layer |

## 3. Historical representation map

```text
Structural:
  ER / Class / Structure Chart / Ownership / Dependency

Control:
  Flowchart / NS / Activity / CFG

State:
  State Diagram / State Table / Petri Net (advanced)

Interaction:
  Sequence / Synchronization

Data:
  DFD / Data Path / Dataflow

Architecture:
  Component / Layer / Deployment / C4-style

Resource:
  Cache / Index / Management map

Implementation geometry:
  Memory Layout / Offset / Cache-line map
```

See `references/diagrams/diagram-catalog.md` for detailed examples and Mermaid/manual trade-offs.

## 4. Traditional/manual vs Mermaid

### Mermaid default

Use Mermaid when the diagram is:

- small and curated;
- maintained with Markdown/Git;
- primarily explanatory/navigation-oriented;
- expressible with Mermaid's actual semantics.

Benefits:

- text-based and diffable;
- easy to review with source notes;
- easy to keep source names visible;
- low maintenance cost for small graphs.

Costs:

- auto-layout can be imperfect;
- fine visual control is limited;
- not every historical notation has native Mermaid semantics;
- complex graphs become hard to read.

### Traditional/manual/specialized default

Use it when:

- exact geometry matters;
- formal semantics matter;
- the graph is exhaustive/huge;
- analysis-tool output is required;
- custom notation is needed.

Benefits:

- precise visual control;
- specialized formal semantics;
- better for large generated analysis views.

Costs:

- harder to version/diff as source;
- manual maintenance can drift from code;
- heavier authoring workflow.

## 5. Diagram-or-no-diagram gate

Before generating a diagram, answer:

```text
1. What one question does the diagram answer?
2. Why is a diagram better than prose/table?
3. Which semantic family is correct?
4. Is Mermaid faithful enough?
5. If not, which specialized/manual representation is appropriate?
```

If there is no strong answer, do not draw.

## 6. One primary view

Use exactly one primary visual view when a visual is justified, plus normally 0–2 secondary views.

Each secondary view must provide unique information.

Bad:

```text
Call Graph + Flowchart + Sequence + CFG
```

for one short function if they all show the same path.

Good:

```text
Concurrency graph
+
Sequence diagram
```

when one answers “who protects what?” and the other answers “what happens over time?”.

## 7. Grain control

Target roughly 5–12 meaningful nodes in a core conceptual diagram. Split large graphs by question or abstraction level rather than creating a graph wall.

## 8. Semantic edge rule

Never use an unlabeled arrow when the exact relationship matters.

Prefer:

```text
contains
references
points-to
owns
manages
indexes
calls
produces
consumes
protects
waits-for
```

The predicate must be backed by source evidence.

## 9. Source-name rule

Use source names as node labels:

```text
BufferDesc
BufferAlloc()
TupleTableSlot
```

Add a short semantic gloss only when useful:

```text
BufferDesc
(shared buffer metadata)
```

## 10. Formal-notation caveat

When a Mermaid diagram approximates a historical/formal method, name it honestly:

```text
DFD-style data path
CFG-like teaching view
State diagram
Management graph
```

Do not call a generic flowchart a canonical Petri Net, NS diagram, or UML deployment diagram.

