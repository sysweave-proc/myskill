# Document Policy

## Document purpose

The document is a projection of the verified knowledge model. It is not a replacement for source code.

## Generic structure

```text
# Title

> Core Question

## 一句话模型

## 1. 核心对象

## 2. 核心行为

## 3. 关键状态 / 生命周期

## 4. 并发与约束

## 5. 关键实现

## 6. 源码导读

## 7. 关键结论

## 8. 下一步阅读
```

Only include sections supported by the current pattern profile.

## Core question

Open with what the chapter explains, not a generic project introduction.

## One-sentence model

Give the smallest accurate mental model. Add the primary view only if it materially helps.

## Object cards

For important objects use compact cards:

```text
### BufferDesc

职责：...

关键字段：...

管理者：...

生命周期：...
```

## Fields

Only document fields that participate in the current knowledge model.

## Source navigation

Identify useful source entry points and next hops:

```text
Current concept
  → current symbol
  → next symbol
  → reason to continue
```

## Source snippets

Keep snippets short and purposeful. Typical target is roughly 5–20 lines, but use judgment.

After each important snippet, explain what it proves or illustrates.

## Style

Prefer:

- precise source names;
- condition-oriented prose;
- concise paragraphs;
- tables for compact properties;
- diagrams only when they reduce cognitive load.

Avoid:

- boilerplate introductions;
- exaggerated praise;
- copied source dumps;
- unsupported “why” claims;
- repeating the same explanation across multiple sections.

## Cross-chapter links

Prefer references to canonical explanations instead of duplicating the same entity semantics in every chapter.

## Next reading

A good chapter ends with a practical next-hop list when useful. This is part of source navigation.
