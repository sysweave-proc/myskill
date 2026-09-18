# Trace Policy

## Claim-centered tracing

Trace only enough source to prove or qualify a claim.

```text
Claim
 ↓
Definition evidence
 ↓
Use/mutation evidence
 ↓
Relevant caller/callee or state/lifecycle evidence
 ↓
Stop when the claim is proven
```

## Trace depth

```text
D1 Local
D2 Structural
D3 System
```

Use D1 for local facts, D2 for cross-symbol semantics, and D3 for architecture/runtime explanations.

## Source anchors

Prefer:

```text
repository + revision
path
qualified symbol
field/expression
code region
```

Use line ranges as helpful navigation, not as the only identity.

## Trace types

```text
definition
reference
read
write
call
return
state-transition
lifecycle
ownership
synchronization
resource-management
architecture-mapping
```

## Trace expansion

Expand only when the current evidence does not answer the open question.

## Boundaries

Record `trace_boundary` when deeper implementation exists but is irrelevant to the current claim.

## Conflicts

When comment/documentation and implementation disagree, retain both evidence sources and flag the conflict.
