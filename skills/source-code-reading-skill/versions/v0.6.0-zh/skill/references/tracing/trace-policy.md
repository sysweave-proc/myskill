# Trace 规范

## 以 Claim 为中心进行追踪

只追踪足以证明或限定一个 Claim 的源码。

```text
Claim
 ↓
定义证据
 ↓
使用/修改证据
 ↓
相关调用方/被调用方，或状态/生命周期证据
 ↓
当 Claim 已经被证明时停止
```

## Trace 深度

```text
D1 Local（局部事实）
D2 Structural（跨符号语义）
D3 System（架构/运行时解释）
```

局部事实使用 D1；跨符号语义使用 D2；架构/运行时解释使用 D3。

## Source Anchor

优先记录：

```text
仓库 + revision
路径
限定符号
字段/表达式
代码区域
```

行号范围可用于辅助导航，但不要把行号范围作为唯一身份标识。

## Trace 类型

```text
definition
reference
read
write
call
return
state-transition
lifecycle
ownership
synchronization
resource-management
architecture-mapping
```

这些标识是规范中的机器可识别术语，应保持原样。

## Trace 扩展

只有当当前证据无法回答 `open_question` 时，才继续扩大追踪范围。

## 边界

如果更深层的实现确实存在，但与当前 Claim 无关，应记录 `trace_boundary`。

## 冲突

当注释/文档与实现不一致时，应同时保留两类证据，并明确标记冲突。
