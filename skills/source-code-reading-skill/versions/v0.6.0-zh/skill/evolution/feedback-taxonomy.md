# 反馈分类法

在修改规则之前，先对反馈进行分类。

```text
F1 Accuracy
F2 Missing Knowledge
F3 Wrong Architecture Position
F4 Wrong Pattern
F5 Wrong Relationship Semantics
F6 Wrong Representation
F7 Wrong Granularity
F8 Wrong Source Anchor
F9 Redundancy
F10 Readability
F11 Navigation
F12 Unsupported Interpretation
F13 Missing Constraint/Invariant
F14 Cross-view inconsistency
```

## 诊断问题

对于“图画得不好”，内部应依次询问：

```text
方法是否错误？
实体集合是否错误？
边的语义是否错误？
粒度是否错误？
布局是否错误？
是否缺少读者上下文？
是否需要形式化语义？
```

把反馈转换成结构化 Case，而不是模糊的偏好描述。
