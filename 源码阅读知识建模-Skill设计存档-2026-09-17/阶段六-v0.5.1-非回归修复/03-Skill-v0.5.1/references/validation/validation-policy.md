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
