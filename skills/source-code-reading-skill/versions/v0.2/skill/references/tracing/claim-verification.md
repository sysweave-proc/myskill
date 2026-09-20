# Claim Verification

## Claim classes

### FACT

Directly observable from source.

Example:

```text
BufferAlloc() calls StrategyGetBuffer().
```

### INFERENCE

Derived from multiple source facts.

Example:

```text
The fast path avoids the main lock-table lookup for some requests.
```

### INTERPRETATION

An explanation of likely design rationale.

Example:

```text
This may reduce shared-path contention for common requests.
```

## Verification table

| Claim type | Minimum evidence |
|---|---|
| symbol exists | definition |
| field meaning | definition + readers/writers |
| flow step | control-flow/call evidence |
| state transition | state write + transition condition |
| ownership | allocation/transfer/release evidence |
| lock protection | shared state + lock boundary |
| design rationale | explicit comments/design docs or cautious inference |

## Confidence

Use:

- HIGH — directly proven;
- MEDIUM — strong inference from multiple facts;
- LOW — plausible but not fully established.

Low-confidence claims should be phrased explicitly as uncertain.

## Missing evidence

Use:

```text
UNVERIFIED
```

when evidence is insufficient. Do not silently convert uncertainty into prose certainty.
