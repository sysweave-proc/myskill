# 回归规范

## 目的

防止局部改进破坏之前已经接受的行为。

## 回归套件

至少维护覆盖以下模式的代表性 Gold Case：

```text
Structural
Lifecycle
Flow
State
Concurrency
Data Path
Resource
Recovery
Architecture
```

每新增一条图表规则，至少重新执行：

```text
一个正例
一个边界案例
一个历史失败案例
一个无关案例
```

## 结果类别

```text
PASS
IMPROVED
NO_CHANGE
REGRESSION
AMBIGUOUS
```

## 采纳规则

如果候选规则在规范 Gold Case 中引入实质性回归，则不能直接采纳，除非已经明确决定修改该 Gold Case。

## 回归报告

```yaml
regression:
  proposal: ""
  cases:
    - id: ""
      result: PASS | REGRESSION | AMBIGUOUS
      note: ""
  summary: ""
  decision: adopt | revise | reject
```
