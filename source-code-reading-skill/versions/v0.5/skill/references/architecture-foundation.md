# Architecture Foundation

## Goal

Provide enough system context that topic notes do not become isolated islands.

## Incremental construction

Build the Atlas in this order:

```text
1. Architecture spine
2. Current topic coordinate
3. One or two critical paths
4. Neighboring subsystem relations
5. Cross-cutting concerns only when required
```

Do not attempt full repository architecture reconstruction as a prerequisite for every topic.

## Architecture coordinate

```yaml
architecture_position:
  system: ""
  subsystem: ""
  layer: ""
  concerns: []
  mechanisms: []
  paths: []
  upstream: []
  downstream: []
  neighboring_topics: []
```

## Architecture vs implementation

Store separately when useful:

```yaml
architecture_fact:
  documented: "..."
  observed: "..."
  status: aligned | partially_aligned | divergent | unknown
  evidence: []
```

The source repository is authoritative for implementation behavior; architecture documents are evidence of intended structure.
