# Case Learning

## Case structure

A useful case stores the full decision context, not just the final Markdown.

```text
Case
├── task
├── source context
├── architecture position
├── knowledge model
├── pattern profile
├── representation plan
├── generated document
├── feedback
├── failure analysis
├── correction
└── learned rule(s)
```

## Gold case

A human/project-reviewed result that is suitable for regression.

## Failure case

A result that exposes a repeatable weakness. Failure cases are valuable only when the failure reason is recorded.

## Case similarity

Retrieve similar cases using:

```text
system domain
core question
pattern
representation family
relationship type
source language
failure type
```

Do not treat lexical similarity alone as semantic similarity.
