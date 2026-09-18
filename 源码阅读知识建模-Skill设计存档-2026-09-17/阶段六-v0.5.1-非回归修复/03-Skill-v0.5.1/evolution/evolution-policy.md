# Evolution Policy

## Goal

Improve the skill without allowing uncontrolled self-modification.

## Four levels

```text
L1 Current-task correction
L2 Reusable case
L3 Candidate rule
L4 Adopted skill change
```

## Safe loop

```text
Generated result
   ↓
Human/project feedback
   ↓
Failure classification
   ↓
Case record
   ↓
Candidate rule
   ↓
Regression against gold cases
   ↓
Human/project approval
   ↓
Rule adoption
```

## Rule proposal requirements

A proposal must include:

```text
problem
trigger
bad behavior
desired behavior
rationale
evidence cases
regression cases
possible side effects
status
```

## Never auto-promote

An Agent may generate a candidate rule, but must not silently modify the normative skill rules. Adoption should be explicit in the engineering workflow.

## Anti-pattern learning

Recurring failures should be named and stored. Examples:

```text
giant-diagram
pointer-is-ownership
call-graph-is-flow
source-location-spam
unsupported-design-intent
architecture-from-directories
view-without-core-question
```

## External learning

External sources can trigger candidate rules, but target-source replay is mandatory before adoption.
