# Document Policy

## Purpose

A source-reading document is a **view of the verified knowledge graph**, optimized for a particular question and reader.

## Recommended skeleton

```text
# Title

> Core Question

## System position

## 一句话模型

## 1. 核心对象

## 2. 核心路径 / 行为

## 3. 状态 / 生命周期

## 4. 并发 / 资源 / 约束

## 5. 关键实现

## 6. 源码导读

## 7. 关键结论

## 8. 下一步阅读
```

Only include sections supported by the pattern profile.

## System position

For large systems, show the zoom path:

```text
System → Subsystem → Path → Topic
```

This should orient, not repeat the whole architecture atlas.

## One-sentence model

Give the smallest accurate mental model before detail.

## Primary View

Place the dominant representation near the point where the reader needs it.

## Object cards

Use compact cards for important entities:

```text
### BufferDesc

职责：...
关键字段：...
管理者：...
生命周期：...
```

## Source snippets

Use short, purposeful snippets. The snippet must have a reason: structure, branch, transition, lock, ownership, cleanup, or other decisive evidence.

## Source navigation

Every important topic should have a path such as:

```text
Current concept
  → current symbol
  → next symbol
  → why to continue
```

## Cross-chapter links

Prefer canonical references instead of duplicating definitions. A note should feel like one window into a shared graph.

## Style

Prefer exact source names, condition-oriented prose, concise paragraphs, tables for compact properties, and diagrams only when they reduce cognitive load.

Avoid source dumps, boilerplate, praise-heavy prose, unsupported intent claims, and diagram-as-decoration.

