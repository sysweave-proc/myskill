# Claim 验证

## Claim 状态

```text
SUPPORTED
PARTIALLY_SUPPORTED
UNVERIFIED
CONFLICTING
```

## 认识论标签

### FACT

可以直接从源码或权威的目标项目文档中观察到。

### INFERENCE

由多个事实推导得到。

### INTERPRETATION

对理由/设计意图的解释，但该意图不能由代码直接确立。

## 验证规则

1. 每个实质性 Claim 至少有一个证据锚点。
2. 关于语义的 Claim 通常需要多个证据点：定义 + 读/写或行为。
3. Ownership 需要生命周期证据。
4. 同步 Claim 需要受保护状态和访问上下文。
5. 状态 Claim 需要迁移证据，而不仅仅是字段名称。
6. 设计意图 Claim 需要注释/设计文档支持，否则必须明确标注为 interpretation。
7. 架构 Claim 需要从高层概念映射到源码/运行时事实的证据。

## 置信度

```text
HIGH   — 有强源码证据直接证明
MEDIUM — 由多个事实形成的稳定推断
LOW    — 具有合理性，但证据不完整
```

## 示例

```yaml
claim:
  statement: "content_lock protects page contents"
  type: FACT
  confidence: HIGH
  evidence:
    - LockBuffer()
    - page access between lock/unlock
```

## 无证据 Claim 的修复

```text
不受支持 → 搜索读者/写者/调用方 → 更新证据 → 重新评估
                                  ↓
                              仍不受支持
                                  ↓
                              限定表述或删除
```
