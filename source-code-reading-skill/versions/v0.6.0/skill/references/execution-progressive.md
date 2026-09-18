# Progressive Execution Policy

## Purpose

Prevent an Agent from spending its budget reconstructing the whole repository before it can answer the current source-reading question.

## Canonical order

```text
Scope → Orient → Minimum Model → Pattern → Trace → Representation → Validate
                                                     ↓
                                           expand only on evidence gap
```

The six canonical reasoning stages remain unchanged; these are entry/exit controls.

## Gates

| Gate | Minimum output | Exit condition |
|---|---|---|
| Scope | question + boundary | target is 1–3 sentences |
| Orient | system location | can answer “where is this?” |
| Minimum model | smallest sufficient graph | no blocking unknown |
| Pattern | dominant comprehension question | representation goal is clear |
| Trace | evidence-backed claims | central claims trace to source |
| Representation | compact useful views | concept → relation → source is navigable |
| Validation | checked result | no known central contradiction |

## Depth levels

- L0: orientation
- L1: local model
- L2: source trace
- L3: cross-cutting architecture

Default is L1. Deepening requires a named unresolved question.

## Anti-overengineering

Do not:

- read the whole repository by default;
- build the complete architecture before a current task has a reason for it;
- enumerate every entity or edge;
- generate every possible diagram;
- consult external sources when target evidence already answers the question;
- duplicate the same explanation across graph, prose, and code.

## Re-entry

```text
Missing context/evidence → Scope/Explore or Trace
Wrong model             → Knowledge Model
Wrong pattern           → Pattern Recognition
Bad visual/document     → Representation & Document
Cross-view inconsistency→ Validation + minimum affected stage
```
