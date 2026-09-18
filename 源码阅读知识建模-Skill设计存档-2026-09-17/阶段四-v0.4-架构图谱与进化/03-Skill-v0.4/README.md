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

