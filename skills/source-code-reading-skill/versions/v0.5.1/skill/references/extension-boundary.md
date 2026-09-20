# Core Skill vs Extensions

## Principle

The core Skill should encode stable reasoning rules, not every concrete tool.

## Core

- six-stage reasoning protocol;
- progressive execution gates;
- canonical knowledge model;
- architecture/path/topic/source integration;
- pattern recognition;
- claim/evidence/traceability;
- representation policy;
- validation;
- evolution/non-regression rules.

## Capability extensions

Tool-specific capabilities belong outside the normative core, for example:

```text
Clang AST / LibTooling
CodeQL
Sourcegraph
Doxygen
perf / BPF
VTune
static-analysis backends
runtime tracing backends
```

Extensions may emit evidence that is consumed by the core model. They must not silently redefine source semantics.

## Knowledge sources

Methodology, standards, renderer docs, language guidance, and mature project examples belong under `knowledge-sources/`. They teach method and tool capability; the target repository remains authoritative for target implementation facts.

## Evolution assets

Feedback, gold cases, failure cases, candidate rules, and regression results belong under `cases/` and `evolution/`.
