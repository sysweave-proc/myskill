# Resource Advisor

## Purpose

Choose external material only when the internal skill rules or target-source evidence are insufficient for the current decision.

## Decision table

| Need | First source class | Example resources | Expected extracted rule |
|---|---|---|---|
| architecture viewpoints | standards/methodology | ISO 42010, SEI V&B | concern/viewpoint/view selection |
| architecture zoom | methodology | C4, Structurizr | abstraction depth / one model, many views |
| documentation organization | methodology | arc42, SEI | section and cross-cutting organization |
| distinguish structure vs control | historical method | Yourdon/Constantine, NS | structure_vs_control_flow |
| data-centric program modeling | methodology | JSP, DFD | data_structure_first / dataflow semantics |
| renderer capability | official tool docs | Mermaid, PlantUML, Graphviz | renderer selection |
| C++ ownership vocabulary | language guidance | C++ Core Guidelines | ownership guardrails |
| source graph extraction | analysis tools | Clang, CodeQL, Doxygen, Sourcegraph | source-analysis backend choice |
| concurrency semantics | system docs | Linux locking, LKMM | synchronization/order guardrails |
| project-native example | mature project docs | PostgreSQL | project-specific navigation conventions |

## When to consult

Consult when:

```text
rule ambiguity
method selection uncertainty
unfamiliar diagram notation
renderer limitation
analysis precision problem
new recurring failure pattern
```

Do not consult merely to decorate a document with citations.

## How to extract a lesson

Do not copy a paragraph into the skill. Convert the source into:

```text
Principle
Trigger
Do / Don't
Example
Boundary
Candidate Rule
```

## Authority boundaries

- External methodology defines the method.
- Official renderer docs define tool capability.
- Target source defines target implementation facts.
- Human-approved project cases define local preferences.

## Learning loop

```text
External source
   ↓
Principle extraction
   ↓
Candidate rule
   ↓
Target-source test
   ↓
Case / regression
   ↓
Adopt or reject
```

