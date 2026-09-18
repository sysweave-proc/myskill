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
