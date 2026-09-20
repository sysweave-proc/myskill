# 可追溯性 · Traceability 快速入口

核心链：

```text
Claim → Evidence → Source Anchor → Trace
```

## 追踪深度

```text
D1 Local
D2 Structural
D3 System
```

## 证据类型

```text
Source
Documentation
Static analysis
Runtime observation
Test
```

## 关键纪律

- 只追到能证明/限定结论为止；
- 每次扩展必须消掉一个 `open_question`；
- 深层实现与当前结论无关时记录 `trace_boundary`；
- 冲突证据同时保留；
- 行号只是导航，仓库 + revision + 符号才是长期身份。

## 认知标签

```text
FACT
INFERENCE
INTERPRETATION
```

以及结论状态：

```text
SUPPORTED
PARTIALLY_SUPPORTED
UNVERIFIED
CONFLICTING
```

详细规则见 `references/tracing/`。
