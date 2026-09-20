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
