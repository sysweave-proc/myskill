# Knowledge Source Advisor

## Purpose

Use the registry in `index.yaml` as a **learning and method-selection layer**, not as a replacement for source evidence.

The advisor answers:

```text
What do I need to learn?
        ↓
Which external source teaches it?
        ↓
What should I extract from that source?
        ↓
Can the source directly support a claim?
        ↓
What rule should be added to the Skill?
```

## Source precedence

For claims about the target repository:

```text
Target source code
    > target project's official docs/comments/tests
    > project-generated source indexes/graphs
    > external methodologies
```

For notation semantics:

```text
Formal standard / original method
    > official tool documentation
    > mature examples
    > secondary explanation
```

For tool capabilities:

```text
Official tool documentation
    > project examples
    > secondary tutorials
```

External material may teach the agent **how to think**, but it does not override what the target code actually does.

## When the agent should consult external sources

### Trigger A — representation ambiguity

Consult methodology sources when:

```text
multiple diagram families could fit
formal semantics are important
agent is unsure whether two diagram families are actually different
```

Suggested lookup order:

```text
SEI Views & Beyond
→ C4 / arc42
→ UML
→ historical method source
```

### Trigger B — renderer limitation

Consult renderer documentation when:

```text
semantic representation already chosen
but the agent needs to know whether Mermaid/PlantUML/Graphviz can express it
```

Order:

```text
Mermaid
→ PlantUML
→ Graphviz
→ Structurizr
```

Do not change the semantic model just to fit Mermaid syntax.

### Trigger C — source extraction uncertainty

Consult analysis tools when:

```text
grep is ambiguous
macros hide semantics
templates/overloads matter
cross-file references are numerous
dataflow needs verification
exact CFG information is required
```

Suggested escalation:

```text
plain source search
→ Clang AST
→ CodeQL
→ Sourcegraph / indexed navigation
→ project-specific analysis
```

### Trigger D — C/C++ ownership / concurrency ambiguity

Consult:

```text
C++ Core Guidelines
Linux locking / LKMM
```

Use these as vocabulary and reasoning guardrails only. Legacy project code may intentionally use different conventions.

### Trigger E — looking for good examples

Consult mature project examples:

```text
PostgreSQL
Linux kernel
Structurizr pattern catalog
arc42 worked examples
```

Extract **why the view works**, not merely its visual style.

## Source consultation protocol

When an external source is consulted, record:

```yaml
source_consultation:
  source_id:
  question:
  relevant_topic:
  learned:
  rule_candidate:
  direct_fact_scope:
  target_repository_checked: true | false
```

## What to extract

Do not copy the source wholesale. Extract one or more of:

```text
semantic definition
selection rule
constraint
anti-pattern
example pattern
trade-off
renderer capability
analysis technique
```

## What not to extract

Do not convert:

```text
“this notation is commonly used for X”
```

into:

```text
“therefore target code X means this notation”
```

The target code still determines the knowledge model.

## Learning loop

```text
External Source
     ↓
Method / Constraint / Example
     ↓
Candidate Rule
     ↓
Apply to current case
     ↓
Compare with source evidence
     ↓
Keep / reject
     ↓
Add to rule base only after validation
```

## Rule promotion policy

A source observation is not automatically a permanent Skill rule.

Promote it only when at least one of these holds:

```text
1. It is a stable semantic definition from a Tier-1 source.
2. It fixes a repeated failure pattern.
3. It improves at least two historical gold cases.
4. It has a clear anti-pattern that prevents recurring errors.
```

Otherwise keep it as a case-level note.

## Decision tree

```text
Need representation semantics?
    ├─ Architecture / multiple views → SEI / C4 / arc42
    ├─ Formal UML semantics          → OMG UML
    ├─ Historical structured flow   → Nassi–Shneiderman / Yourdon / HIPO / JSP
    └─ Runtime interaction          → UML Sequence / State concepts

Need a renderer?
    ├─ Markdown-first small view     → Mermaid
    ├─ Text-first richer UML         → PlantUML
    ├─ Large directed graph layout  → Graphviz
    └─ C4 model + many consistent views → Structurizr

Need source facts?
    ├─ Simple local lookup            → project search / grep
    ├─ C/C++ AST semantics            → Clang AST
    ├─ Cross-file / dataflow analysis → CodeQL
    ├─ Generated orientation graphs   → Doxygen
    └─ Large-repo semantic navigation → Sourcegraph

Need semantic guardrails?
    ├─ C++ ownership/lifetime         → C++ Core Guidelines
    └─ Kernel concurrency/order       → Linux locking / LKMM
```

## Example: why consult an external source

Suppose a generated diagram contains:

```text
TupleTableSlot → HeapTuple
```

The external registry can help decide whether the relation should be described as `references`,
`contains`, or `owns`, but it cannot establish that the PostgreSQL implementation actually has
that ownership relation. That must be proven by reading the target source and its lifetime paths.

Suppose the problem is:

```text
“这几个对象怎么组织？”
```

Consult structural/view methodologies.

Suppose the problem is:

```text
“这个请求先经过谁，再在哪里分支？”
```

Use control-flow/interaction methodologies.

Suppose the problem is:

```text
“这个字段为什么在这里安全地修改？”
```

Consult concurrency/ownership guardrails and then verify the exact lock/atomic/lifetime path in target source.
