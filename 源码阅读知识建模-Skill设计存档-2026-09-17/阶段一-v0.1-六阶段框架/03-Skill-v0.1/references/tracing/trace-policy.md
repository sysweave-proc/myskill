# Trace Policy

## Goal

Create a bounded, evidence-driven path from a claim to source code.

## Source identity

Prefer:

```text
repository + revision + path + qualified symbol + field/code region
```

Line range is secondary.

## Trace types

### Definition trace

Concept → definition.

### Usage trace

Definition/field → readers/consumers.

### Mutation trace

Field/state/resource → writers.

### Call trace

Caller → callee.

### Data trace

Object → field → next object/consumer.

### Lifecycle trace

Create → initialize → publish → acquire/use → release → destroy.

### Synchronization trace

Shared state → protection primitive → acquire/release/wait/wake sites.

## Trace depth

### D1 Local

Current symbol only.

### D2 Structural

Current symbol plus related structs/fields/callers/callees/managers/locks.

### D3 System

Cross-module or cross-layer evidence needed to close the claim.

## Expansion rule

Expand one step only when it resolves an explicit unknown.

```text
Unknown
  ↓
Search related evidence
  ↓
Re-evaluate claim
  ↓
Stop when supported
```

## Stopping rules

Stop when:

- the claim is directly proven;
- the inference chain is closed;
- the next layer is outside the defined scope and unnecessary.

Record a trace boundary when stopping at an architectural interface.

## Anti-patterns

Do not:

- follow every call recursively;
- use line numbers as the only identity;
- treat any pointer as ownership;
- infer intent solely from names;
- attach an evidence location without stating what it demonstrates.
