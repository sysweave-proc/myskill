# Example execution sequence

```text
User question
  ↓
Scope: "Explain TupleTableSlot's object relationships and tuple ownership"
  ↓
Orient: executor/tuptable + slot-related types
  ↓
Minimum model: Slot → TupleTableSlot / TupleTableSlotOps / tuple storage
  ↓
Pattern: Structural + Lifecycle
  ↓
Trace: constructors, tuple store fields, materialization/release paths
  ↓
Represent: one entity/management view + a small lifecycle note
  ↓
Validate: verify ownership claims and cleanup paths
  ↓
Stop
```

Only after this should a new question trigger a second loop, such as execution flow, deforming, or memory ownership.
