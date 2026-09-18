# Source Code Reading Skill v0.5.1

A graph-first Agent Skill for understanding large C/C++ systems through progressive, source-grounded reasoning.

## What v0.5.1 fixes

This release is built by **incremental merge on the complete v0.4 baseline**. It adds progressive execution gates and a non-regression evolution policy without deleting the architecture, knowledge-source, evolution, cases, diagram, tracing, validation, template, or example assets from v0.4.

The withdrawn v0.5 package was a regression because it rebuilt the package from a reduced subset and dropped previously established capabilities. v0.5.1 is the repaired additive release.

## Core model

```text
Canonical Knowledge Graph
├── Architecture View
├── Path / Runtime View
├── Topic View
└── Source View
```

One graph supports zooming:

```text
System → Subsystem → Path → Mechanism → Entity → Symbol → Code
```

## Execution

The six-stage protocol remains:

```text
Scope & Explore
→ Knowledge Model
→ Pattern Recognition
→ Traceability
→ Representation & Document
→ Validation & Orchestration
```

An entry/exit gate layer keeps execution progressive:

```text
Scope → Orient → Minimum Model → Pattern → Trace → Represent → Validate
                                                ↘ expand only when needed
```

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
tests/
```

## Evolution rule

New versions merge forward from the previous release by default. No existing capability may disappear silently. Any removal must be explicit, justified, and regression-tested.

See `evolution/baseline-policy.md` and `tests/test_skill_integrity.py`.
