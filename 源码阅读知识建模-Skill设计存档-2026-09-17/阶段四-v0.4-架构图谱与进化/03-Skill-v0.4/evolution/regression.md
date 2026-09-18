# Regression Policy

## Purpose

Prevent a local improvement from damaging previously accepted behavior.

## Regression suite

At minimum maintain representative gold cases for:

```text
Structural
Lifecycle
Flow
State
Concurrency
Data Path
Resource
Recovery
Architecture
```

For each new diagram rule, replay at least:

```text
one positive case
one borderline case
one previous failure
one unrelated case
```

## Result classes

```text
PASS
IMPROVED
NO_CHANGE
REGRESSION
AMBIGUOUS
```

## Adoption rule

A candidate rule is not adopted when it introduces a material regression in a canonical gold case without an explicit decision to change that gold case.

## Regression report

```yaml
regression:
  proposal: ""
  cases:
    - id: ""
      result: PASS | REGRESSION | AMBIGUOUS
      note: ""
  summary: ""
  decision: adopt | revise | reject
```

