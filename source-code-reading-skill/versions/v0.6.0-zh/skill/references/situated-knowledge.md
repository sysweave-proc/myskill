# 情境化知识 · Situated Knowledge

活系统的知识必须带上下文，否则一年后无法判断结论是否仍成立。

## 1. 版本 / 时间

```text
Entity@Revision
Relation@Revision
Architecture@Revision
Path@Revision
```

记录 `introduced / deprecated / replaced / refactored / moved` 等变化。

## 2. 构建 / 配置变体

```text
Code exists ≠ Code compiled ≠ Code reachable ≠ Code active
```

建议记录：

```yaml
build_context:
  compiler:
  platform:
  arch:
  build_type:
  defines:
  enabled_modules:
```

## 3. 性能 Concern

性能不是普通附注，而是对 OS/数据库/存储尤其重要的横切关注点：

```text
latency · contention · locality · bandwidth · queueing
CPU migration · cache · NUMA · lock · IO
```

允许它关联 Path / Resource / CPU / Memory / Cache / NUMA / Lock / IO。

## 4. Decision / Rationale

```text
Decision
├── Problem
├── Constraint
├── Alternative
├── Choice
├── Consequence
└── Evidence
```

没有证据支持的设计动机只能作为 `INTERPRETATION`。

## 5. Learning Path

知识之间还有“先学什么”的关系：

```text
Architecture → Process Model → Memory Model
→ Buffer Manager → Buffer Lookup → Buffer State
```

```yaml
learning:
  prerequisites: []
  unlocks: []
  recommended_depth: L0 | L1 | L2 | L3
```

## 6. Conflict

不要简单覆盖：

```text
different version
 different build
 different runtime path
 documentation drift
 historical behavior
```

保留冲突并记录其来源与适用范围。

## 7. Change Impact

```text
源码变化
  ↓
受影响符号
  ↓
受影响结论
  ↓
受影响架构 / Path
  ↓
受影响文档 / 图
```

细节可以继续挂入 Evolution 资产。
