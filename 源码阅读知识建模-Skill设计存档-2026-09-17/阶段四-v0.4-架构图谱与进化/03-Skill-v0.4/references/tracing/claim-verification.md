# Claim Verification

## Claim states

```text
SUPPORTED
PARTIALLY_SUPPORTED
UNVERIFIED
CONFLICTING
```

## Epistemic labels

### FACT
Directly observable from source or authoritative target-project documentation.

### INFERENCE
Derived from multiple facts.

### INTERPRETATION
An explanation of rationale/design intent not directly established by code.

## Verification rules

1. Every substantial claim has at least one evidence anchor.
2. Claims about semantics usually require multiple evidence points: definition + reads/writes or behavior.
3. Ownership requires lifetime evidence.
4. Synchronization claims require the protected state and access context.
5. State claims require transition evidence, not only a field name.
6. Design-intent claims require comments/design documentation or must be explicitly qualified as interpretation.
7. Architecture claims require mapping evidence from high-level concepts to source/runtime facts.

## Confidence

```text
HIGH   — directly demonstrated by strong source evidence
MEDIUM — stable inference from multiple facts
LOW    — plausible but evidence incomplete
```

## Example

```yaml
claim:
  statement: "content_lock protects page contents"
  type: FACT
  confidence: HIGH
  evidence:
    - LockBuffer()
    - page access between lock/unlock
```

## Unsupported claim repair

```text
Unsupported → search readers/writers/callers → update evidence → re-evaluate
                                  ↓
                         still unsupported
                                  ↓
                         qualify or remove
```

