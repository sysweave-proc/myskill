# 情境化知识 · Situated Knowledge

前面几份参考文件解决"怎么读、怎么建模、怎么表达"。这份解决**一个活着的系统**额外需要的东西：
知识不是脱离时间、构建、权衡而存在的。缺了以下维度，模型一年后就会变成"一堆不知道还成不成立的结论"。

## 1. 时间维度：架构不是静态的

真实系统是：

```text
Version N → Version N+1 → 架构变了 → 代码变了 → 行为变了
```

所以知识对象要能带上版本：

```text
Entity@Version   Relation@Version   Architecture@Version   Path@Version
introduced / deprecated / replaced / refactored / moved
```

否则必然出现"这个结论到底适用于哪个版本？"的尴尬。

## 2. 构建 / 配置变体

**源码不等于构建出来的程序。** `#ifdef`、平台、编译选项、插件、存储引擎都会改变实际行为。

```text
Code exists  ≠  Code compiled  ≠  Code reachable  ≠  Code active
```

记录构建上下文：

```yaml
build_context:
  compiler:
  platform:
  arch:
  build_type:
  defines:
  enabled_modules:
```

## 3. 性能作为一种关注点

对数据库/OS/存储，性能不是"架构的附带说明"。它有自己的链条：

```text
Query → Lock → Hash → Memory → NUMA → Cache → IO
latency · contention · cache locality · remote memory
bandwidth · queueing · IO depth · CPU migration
```

把它记为 `Performance Concern`，并允许关联 Path / Resource / CPU / Memory / Cache / NUMA / Lock / IO。

## 4. 决策与理由（Why 不该靠猜）

`FACT / INFERENCE / INTERPRETATION` 还不够。把"为什么这样设计"结构化：

```text
Decision
├── Problem
├── Constraint
├── Alternative
├── Choice
├── Consequence
└── Evidence
```

例：为什么用分区锁而不是单一全局锁——约束是高并发查找，代价是元数据/查找复杂度上升。
**没有 Evidence 的 Decision 必须标成 INTERPRETATION。**

## 5. 学习路径：另一种图

知识之间的"先学什么"关系，是一张独立的图：

```text
System Architecture → Process Model → Memory Model
→ Buffer Manager → Buffer Lookup → Buffer State
```

给每个主题标注：

```yaml
learning:
  prerequisites: []
  unlocks: []
  recommended_depth: L0 | L1 | L2 | L3
```

这样技能才能回答："你已经掌握 A，因此现在最适合继续读 B。"

## 6. 知识冲突模型

现实中经常是文档说 A、源码说 B、测试说 C、旧版本说 D。这不是简单的"哪个是真的"，而可能是：

```text
different version     different build     different runtime path
documentation drift   historical behavior
```

**保留冲突，不要覆盖。** 把冲突记录成实体的属性，并归因到上面某一类原因。

## 7. 变更影响

```text
源码变化 → 受影响的符号 → 受影响的结论 → 受影响的架构 → 受影响的文档/图
```

```text
哪些 Topic 受影响？
哪些 Path 受影响？
哪些图需要重画？
哪些结论失效？
哪些文档需要重新校验？
```

有了这一条，技能就从"源码阅读工具"迈向"活着的代码知识系统"。

## 8. 与五个维度的关系

以上维度不是新增第六类知识，而是把五类知识**放回情境**：

| 情境维度 | 落在哪一类 |
|---|---|
| 版本 / 时间 | Evolution |
| 构建变体 | Evolution + Evidence（决定"active"与否） |
| 性能 | Behavior + Constraint |
| 决策/理由 | Constraint + Evidence |
| 学习路径 | Structure（跨主题的另一种图） |
| 冲突 | Evidence |
| 变更影响 | Evolution |
