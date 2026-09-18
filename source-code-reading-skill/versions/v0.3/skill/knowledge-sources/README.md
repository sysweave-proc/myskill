# knowledge-sources/

This directory is the external-learning registry for the Source Code Reading Skill.

The registry is intentionally split from the main Skill rules:

```text
Skill rules
    = what the agent should do

Knowledge sources
    = where the agent can learn why a rule exists,
      what a notation means, and how mature systems use it
```

## Files

- `index.yaml` — machine-readable resource registry.
- `resource-advisor.md` — when/how the agent should consult resources and how to turn them into rules.

## Resource roles

### Methodology

Teaches abstraction and representation choices:

```text
SEI Views & Beyond
C4
arc42
UML
Structured Design
Nassi–Shneiderman
JSP
HIPO
```

### Renderer

Teaches what a concrete notation/tool can actually express:

```text
Mermaid
PlantUML
Graphviz
Structurizr
```

### Analysis backend

Teaches how to extract or verify source facts:

```text
Clang AST / LibTooling
CodeQL
Doxygen
Sourcegraph
```

### Domain guardrail

Teaches C/C++ and systems semantics:

```text
C++ Core Guidelines
Linux locking
Linux Kernel Memory Model
```

### Project examples

Teaches how mature projects expose real source architecture:

```text
PostgreSQL
Linux kernel
Structurizr pattern catalog
arc42 worked examples
```

## Maintenance rule

When adding a source, record:

```text
what it teaches
when to query it
what it must not be used for
what facts it may directly support
what Skill rule it should influence
```

A URL without a learning role is not a useful Skill dependency.
