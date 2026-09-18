# 可追溯性 · Traceability

## 以结论为中心的追踪

只追到"能证明或限定这条结论"为止：

```text
Claim
 ↓
定义证据
 ↓
使用/修改证据
 ↓
相关的调用者/被调用者，或状态/生命周期证据
 ↓
结论被证明即停
```

## 追踪深度

```text
D1 Local       局部事实
D2 Structural  跨符号语义
D3 System      架构/运行时解释
```

D1 用局部事实，D2 用跨符号语义，D3 用架构/运行时解释——**深度与结论尺度匹配，不额外加深**。

## 源码锚点

优先级从高到低：

```text
仓库 + 版本
路径
限定符号名
字段/表达式
代码区域
```

**行区间只作为导航辅助，不作为唯一身份。** 代码会演进，符号名比行号长寿。

## 追踪类型

```text
definition  reference  read  write  call  return
state-transition  lifecycle  ownership  synchronization
resource-management  architecture-mapping
```

## 展开原则

- 只有当现有证据答不上当前未解问题时才展开；
- 记录 `trace_boundary`：下面还有更深的实现，但与当前结论无关；
- 当注释/文档与实现冲突时，**同时保留两份证据并标记冲突**，不要强行调和。

## 未解问题清单

探索时维护：

```yaml
open_questions:
  - question: ""
    importance: high | medium | low
    related_symbols: []
    status: open | investigating | resolved | blocked
```

**每一次展开都必须消掉或细化至少一个未解问题。** 没有消掉问题的展开就是闲逛。

## 证据的五种来源

| 证据类型 | 说明 |
|---|---|
| Source | 目标源码本身 |
| Documentation | 目标项目的官方文档/设计文档 |
| Static analysis | AST、调用图、数据流、依赖抽取 |
| Runtime observation | gdb、perf、tracepoint、ftrace、bpftrace、VTune、DTrace、日志 |
| Test | 测试用例证明某条状态迁移、边界条件或异常路径确实存在 |

区分这两句话：

```text
"代码可能这么执行"        ← 静态证据
"这个 workload 下确实这么执行" ← 运行时证据
```

## 结论状态与认知标签

```text
SUPPORTED / PARTIALLY_SUPPORTED / UNVERIFIED / CONFLICTING
```

- `FACT`：源码或目标项目权威文档可直接观测；
- `INFERENCE`：由多条事实推导；
- `INTERPRETATION`：对动机/设计意图的解释，代码本身不能直接证明。

## 校验规则

1. 每条实质结论至少一个证据锚点；
2. 语义结论通常要多点证据：定义 + 读/写或行为；
3. ownership 需要生命周期证据；
4. 同步结论需要指出被保护状态与访问上下文；
5. 状态结论需要迁移证据，不能只有字段名；
6. 设计意图结论需要注释/设计文档，否则必须显式标为 INTERPRETATION；
7. 架构结论需要从高层概念到源码/运行时事实的映射证据。

## 置信度（四因子，不只是高/中/低）

```yaml
claim:
  confidence: medium
  because:
    direct_source: yes
    runtime_verified: no
    version: 17
    inference_depth: 2
```

这样读者能知道：**"这条我很有把握，但它只在 PG 17 上验证过。"**

## 不支持时的修复路径

```text
不支持 → 查读/写方、调用者 → 更新证据 → 重新评估
                              ↓ 仍不支持
                        降级限定 或 删除
```
