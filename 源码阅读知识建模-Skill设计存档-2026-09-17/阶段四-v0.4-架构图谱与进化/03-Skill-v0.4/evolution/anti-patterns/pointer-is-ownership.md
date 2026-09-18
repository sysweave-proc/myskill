# Anti-pattern: Pointer Means Ownership

**Symptom:** `A *b` is rendered as `A owns B`.

**Repair:** trace allocation, lifetime, release, transfer, and reference conventions before asserting ownership.

