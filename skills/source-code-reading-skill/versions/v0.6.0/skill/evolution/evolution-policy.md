# 演进策略 · Evolution Policy

目标：让技能可以被反馈改进，同时**不允许失控的自我修改和能力丢失**。

## 四级演进

```text
L1 当前任务的就地修正
L2 可复用病例
L3 候选规则
L4 已采纳规范变更
```

只有 L4 才改变规范 Skill。模型可以生成 candidate rule，但不能静默修改 normative rules。

## 安全闭环

```text
结果
 ↓
人 / 项目反馈
 ↓
失败分类
 ↓
Case
 ↓
Candidate Rule
 ↓
Gold Regression
 ↓
Human / Project Approval
 ↓
Adopted Rule
```

## 版本纪律：merge，不是 rewrite

```text
上一版
  ↓
Capability inventory
  ↓
Baseline comparison
  ↓
Minimal additive merge
  ↓
Integrity regression
  ↓
Semantic regression
  ↓
CHANGELOG
  ↓
新版本
```

### 必须保留

- baseline 文件；
- 人可读能力清单；
- 知识源、病例、示例、模板和测试等持久资产；
- 过去已被验证的负例与 anti-pattern。

### 删除协议

任何 removal 必须：

```yaml
removal:
  path: ""
  capability: ""
  reason: ""
  replacement: ""
  regression_evidence: []
  approved: false
```

## Anti-pattern learning

反复失败必须命名并入库，例如：

```text
giant-diagram
pointer-is-ownership
call-graph-is-flow
enum-is-state-machine
lock-means-protection
architecture-from-directories
view-without-core-question
unsupported-design-intent
source-location-spam
```

## External learning

外部资料可以触发 candidate rule，但采纳前必须在目标源码上回放，并通过既有 gold/failure 回归。

更多细节见 `evolution/baseline-policy.md`、`case-learning.md`、`feedback-taxonomy.md`、`rule-proposal.md`、`regression.md`。
