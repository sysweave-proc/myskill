# Traceability

## Claim record

```yaml
claim:
  text: "..."
  status: observed | strongly_inferred | hypothesis
  evidence:
    - source_anchor: "path/to/file.c:123-145"
      element: "FunctionOrType"
      kind: field_write | call | allocation | lock | branch | test | docs | runtime
      note: "..."
```

## Evidence hierarchy

For implementation behavior, prefer:

```text
source code
> executable tests / runtime observation
> project docs/design notes
> external methodology
> model memory / generic expectation
```

External material may define notation or general semantics, but it must not replace repository evidence.
