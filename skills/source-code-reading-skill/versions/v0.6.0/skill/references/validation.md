# 校验 · Validation 快速入口

## V1–V6

```text
V1 Structural
V2 Semantic
V3 Traceability
V4 Representation
V5 Reader / Navigation
V6 Architecture Consistency
```

### 返修路由

```text
scope/context missing → Stage 1
knowledge missing     → Stage 2
wrong pattern         → Stage 3
unsupported claim     → Stage 4
bad representation    → Stage 5
cross-layer mismatch  → Stage 6, then earliest affected stage
```

### 交付前三问

```text
1. 概念 → 关系 → 源码，这条路径走得通吗？
2. 每个主视图元素都能回到源码吗？
3. 有没有“我猜的”却没标出来？
```

完整规范见 `references/validation/validation-policy.md`。
