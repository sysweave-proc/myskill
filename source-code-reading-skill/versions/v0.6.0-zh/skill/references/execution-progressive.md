# 渐进式执行规范

## 目的

防止 Agent 在能够回答当前源码阅读问题之前，就消耗预算去重构整个仓库。

## 规范顺序

```text
Scope → Orient → Minimum Model → Pattern → Trace → Representation → Validate
                                                     ↓
                                           仅在存在证据缺口时扩展
```

六个规范推理阶段保持不变；这些阶段同时承担进入/退出控制。

## 闸门

| Gate | 最小输出 | 退出条件 |
|---|---|---|
| Scope | 问题 + 边界 | 目标可以用 1–3 句话描述 |
| Orient | 系统位置 | 能回答“它在哪里？” |
| Minimum model | 足够小的最小图 | 不存在阻塞性未知 |
| Pattern | 主导理解问题 | 表达目标明确 |
| Trace | 有证据支持的 Claim | 核心 Claim 能追溯到源码 |
| Representation | 紧凑且有用的视图 | 概念 → 关系 → 源码可导航 |
| Validation | 已检查的结果 | 没有已知的核心矛盾 |

## 深度级别

- L0 Orientation（定位）；
- L1 Local model（局部模型）；
- L2 Source trace（源码追踪）；
- L3 Cross-cutting（跨切面架构）。

默认从 L1 开始。继续深入必须有明确命名的未解决问题。

## 反过度设计

不要：

- 默认读完整个仓库；
- 在当前任务尚未产生需求之前就构建完整架构；
- 枚举所有实体或边；
- 生成所有可能的图；
- 目标证据已经回答问题时还去查外部资料；
- 在图、正文和代码中重复同一解释。

## 重新进入

```text
缺少上下文/证据     → Scope/Explore 或 Trace
模型错误             → Knowledge Model
Pattern 错误         → Pattern Recognition
视觉/文档表达错误    → Representation & Document
跨视图不一致         → Validation + 最小受影响阶段
```
