# Source Code Reading Skill v0.5

This version focuses on **execution discipline** rather than adding more theory.

The most important change is the staged-gate protocol: the Agent must stop at each layer once the current question is sufficiently explained, and only deepen when an unresolved question forces it to.

## Intended architecture

```text
Source Understanding System
├── Core Skill
│   ├── staged execution + gates
│   ├── architecture foundation
│   ├── canonical knowledge model
│   ├── pattern recognition
│   ├── traceability
│   ├── representation policy
│   └── validation
├── Capability Extensions
│   ├── static analysis
│   ├── runtime observation
│   ├── performance analysis
│   ├── test analysis
│   └── diagram rendering
├── Knowledge Sources
│   └── standards / methods / tool docs / project examples
└── Evolution
    ├── cases
    ├── feedback
    ├── anti-patterns
    └── regression
```

## What is deliberately not in the core

Tool manuals, exhaustive diagram catalogs, vendor-specific workflows, perf/BPF/VTune procedures, and project-specific rules should remain extensions or knowledge sources.

## Default operating behavior

Start small → build model → choose pattern → trace → represent → validate → deepen only if needed.
