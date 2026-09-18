# Validation Policy

## V1 Structural

Check:

- core question exists;
- mental model exists;
- primary view exists when needed;
- source navigation exists for substantial topics;
- conclusions are explicit.

## V2 Semantic

Check:

- every important diagram edge is source-supported;
- ownership is proven, not inferred from pointers;
- state transitions have real triggers;
- lock protection names the protected state;
- data path distinguishes copy/reference/move when important;
- flow diagrams do not overstate parallel or deferred execution.

## V3 Traceability

For each important claim:

```text
Claim → Evidence → Source Anchor
```

Flag unsupported claims as `UNVERIFIED` or remove them.

## V4 Representation

Check:

- primary view matches dominant pattern;
- diagrams are not over-detailed;
- graph/prose/code have distinct jobs;
- there is no call-graph/flow confusion;
- state/lifecycle are not conflated.

## V5 Reader/navigation

A reader should be able to answer:

- what is this?
- what are the core entities?
- how do they relate?
- how does the main operation proceed?
- what are the important states/lifecycle rules?
- what concurrency constraints matter?
- where is the real source?
- what should I read next?

## Revision routing

```text
Missing evidence       → explore / trace
Wrong knowledge model  → model
Wrong pattern          → pattern
Poor expression        → representation/document
Style-only issue       → document
```

Limit revision loops to a small bounded number and prefer targeted repair.
