# Validation 规范

## Validation 层次

### V1 Structural（结构）

- 核心问题存在；
- 在适用时存在架构位置；
- 在有帮助时存在主要视图；
- 存在源码导航；
- 在有帮助时提供下一步阅读入口。

### V2 Semantic（语义）

- 实体关系有证据支持；
- 不把 ownership 与 reference 混淆；
- 不把 flow 与 call graph 混淆；
- 状态迁移确实存在；
- 同步所保护的目标确实存在；
- 数据移动在重要时区分 copy/reference。

### V3 Traceability（可追溯性）

每一个重要 Claim 都必须能够解析为：

```text
Claim → Evidence → Source Anchor
```

### V4 Representation（表达）

- 主要表达方式与主导 Pattern 匹配；
- 图没有承载过多信息；
- 图没有重复正文；
- Renderer 能表达所选择的语义；
- 需要精确性时使用专业工具。

### V5 Reader / Navigation（读者/导航）

读者应该能够回答：

```text
我在哪里？
核心机制是什么？
为什么重要？
哪条 Path 使用它？
源码在哪里？
接下来应该读什么？
```

### V6 Architecture Consistency（架构一致性）

- topic 坐标能够解析到当前 Atlas；
- 源码证据如果与架构冲突，必须存在已记录的 conflict；
- critical path 不存在未解释的缺口。

## 修订路由

Validation 失败后，应回到最小的修复阶段：

```text
缺少范围/上下文       → Stage 1
缺少知识模型          → Stage 2
抽象/Pattern 错误     → Stage 3
Claim 缺乏证据        → Stage 4
图/文档表达错误       → Stage 5
跨层不一致            → Stage 6，必要时再回到更早阶段
```
