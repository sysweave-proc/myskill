# Source Code Reading Skill v0.2

Portable Agent Skill for large C/C++ source-code understanding.

## Unified six-stage execution

```text
1. Scope & Explore
2. Knowledge Model
3. Pattern Recognition
4. Traceability
5. Representation & Document
6. Validation & Orchestration
```

## Core idea

This is not a source-to-Markdown summarizer. It builds a traceable knowledge model first, then selects a comprehension pattern and representation.

```text
Source
  ↓
Knowledge Model
  ↓
Pattern
  ↓
Claim / Evidence / Trace
  ↓
Representation
  ↓
Document
  ↓
Validation
```

## Diagram system

The skill includes a dedicated catalog that teaches an Agent:

- historical diagram families and what questions they answer;
- a concrete small example for each major method;
- traditional/manual vs Mermaid strengths and weaknesses;
- when Mermaid is sufficient;
- when a specialized/manual/static-analysis tool should win;
- when no diagram is the correct answer;
- how to distinguish similar-looking methods such as Flow vs Call Graph, State vs Lifecycle, DFD vs Dataflow, and conceptual graphs vs formal models.

Start with:

- `references/diagrams/diagram-catalog.md`
- `references/representation/representation-policy.md`
- `references/patterns/pattern-catalog.md`

## Modes

- **Explore** — source investigation.
- **Model** — build/update the knowledge model.
- **Document** — generate a reading note.
- **Review** — audit an existing note against source evidence.

## Intended first validation targets

The skill is especially suitable for C/C++ systems code such as:

```text
PostgreSQL Buffer Manager
PostgreSQL Lock Manager
TupleTableSlot
Relation / RelationData
Memory Context
```

The first validation goal should be semantic correctness and source traceability, not visual polish.
