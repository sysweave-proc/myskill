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

