# Example: Buffer Manager topic at L1/L2

This example demonstrates **progressive depth** rather than exhaustive coverage.

## Start at L1

```text
Executor / Access Method
        ↓
   Buffer Manager
        ↓
 Buffer Lookup
   ├─ page identity
   ├─ mapping/index structure
   ├─ buffer descriptor
   └─ synchronization
```

At L1, the agent only needs enough symbols to explain the management backbone.

## Move to L2 only for a concrete question

For example:

> How does a page identity become a specific buffer descriptor?

Now trace the lookup path, mapping structure, partition lock, and descriptor access into source.

Do not automatically add replacement policy, WAL interaction, I/O workers, background writer, checkpointing, and performance analysis unless the question requires them.
