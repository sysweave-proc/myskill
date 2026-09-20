# Exploration Policy

## Start from the user's question

Do not begin by reading the entire file. Define the exact question first.

## Search sequence

A typical sequence:

```text
1. Find target symbol
2. Read definition and local comments
3. Find references
4. Inspect key fields and related types
5. Inspect direct callers/callees
6. Search readers/writers for key fields
7. Search allocation/free or lock/state operations as relevant
8. Expand cross-module only if required
```

## Context expansion

```text
L0 Target symbol
L1 Direct definition
L2 Direct references
L3 Related structures/fields
L4 Relevant control flow
L5 Runtime/lifecycle/synchronization
L6 Cross-module
```

Do not automatically traverse all levels.

## Open questions

Maintain an internal list:

```yaml
open_questions:
  - question:
    importance: high | medium | low
    related_symbols: []
    status: open | investigating | resolved | blocked
```

Every expansion should close or refine at least one open question.

## Conflict handling

When comments/docs and implementation appear inconsistent, retain both evidence sets and mark the conflict. Do not force a false reconciliation.
