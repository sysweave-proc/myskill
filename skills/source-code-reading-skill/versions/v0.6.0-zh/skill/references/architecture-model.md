# 架构模型

## 目的

架构模型是整个源码阅读知识图谱的稳定坐标系。

它回答四个不同的问题：

```text
系统上下文      → 系统是什么，它的边界在哪里？
架构主干        → 系统在宏观上如何组织？
运行时路径      → 各部分在什么情况下协同工作？
主题/源码       → 某个具体机制是如何实现的？
```

## 规范图模型

```text
System
 └─contains→ Subsystem
              ├─contains→ Mechanism
              ├─participates_in→ Path
              └─addresses→ Concern

Mechanism
 ├─realized_by→ Entity / Symbol
 ├─participates_in→ Path
 └─depends_on→ Mechanism

Entity / Symbol
 ├─references→ Entity
 ├─modifies→ Entity
 ├─protects→ State
 └─evidenced_by→ SourceRange
```

## 架构层次

### A0 系统上下文
边界、外部参与者、外部依赖。

### A1 架构主干
5–12 个宽粒度子系统或层。不要试图枚举整个仓库。

### A2 能力 / 机制
子系统内部稳定的能力。

### A3 运行时路径 / 场景
跨越多个子系统的端到端行为。

### A4 源码实现
核心实体、符号、字段和代码区域。

## 核心架构关系

```text
contains
refines
depends_on
interfaces_with
participates_in
realized_by
implemented_by
managed_by
owns
cross_cuts
```

只有证据支持时才使用这些关系。

## 主题的架构坐标

每一个主要主题都应该记录：

```yaml
architecture_position:
  system: ""
  subsystem: ""
  layer: ""
  mechanisms: []
  paths: []
  concerns: []
  upstream: []
  downstream: []
  neighboring_topics: []
```

## 不要把架构模型当成僵硬的树

为了可读性，架构主干可以呈现为树状，但规范模型本质上是图。一个主题可以参与多条 Path 和多个 Concern。

## 架构质量测试

只有当 System Atlas 能够回答下面问题时，它才真正有用：

1. 一个主题位于哪里？
2. 哪些主要 Path 使用它？
3. 它依赖哪些相邻子系统？
4. 读者能否从架构缩放到源码，再从源码返回架构？
5. 架构是否至少解释了一条代表性的端到端场景？

## 架构缺口

Critical Path 上缺失一个节点，即使没有任何笔记文件缺失，也属于知识缺口。

```text
Path:
A → B → C → D

Known:
A ✓ B ✓ C ? D ✓

Gap:
C
```

这个缺口应该作为 `open_question` 或 `knowledge_gap` 跟踪，而不是用猜测出来的关系掩盖。
