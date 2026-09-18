# 演进策略 · Evolution Policy

## 目标

让技能可以被反馈改进，同时**不允许失控的自我修改**。

## 四个层级

```text
L1 当前任务的就地修正
L2 可复用的病例
L3 候选规则
L4 已采纳的技能变更
```

只有 L4 才改规范。L1 只在当前任务里生效，不能顺手上调。

## 安全闭环

```text
产出结果
  ↓
人 / 项目反馈
  ↓
失败分类
  ↓
病例记录
  ↓
候选规则
  ↓
对 gold case 回归
  ↓
人 / 项目批准
  ↓
规则采纳
```

**模型可以生成候选规则，但绝不能静默改写规范规则。**

## 候选规则提案必须包含

```text
problem            问题
trigger            触发条件
bad behavior       当前坏行为
desired behavior   期望行为
rationale          理由
evidence cases     支撑病例
regression cases   回归病例
possible side effects
status
```

## 反模式学习

反复出现的失败要被命名并入库：

```text
giant-diagram                 一张图画尽
pointer-is-ownership          指针当所有权
call-graph-is-flow            调用图当流程
enum-is-state-machine         枚举当状态机
lock-means-protection         看到锁就说保护了什么
architecture-from-directories 目录名推架构
view-without-core-question    无核心问题的视图
unsupported-design-intent     无证据的设计意图
source-location-spam          行号堆砌
```

## 外部学习

外部资料可以触发候选规则，但**采纳前必须在目标源码上回放**。

## 版本纪律：合并式演进，不是重写式演进

```text
上一版
  ↓
能力清单（capability inventory）
  ↓
与基线逐文件/逐能力比对
  ↓
最小增量补丁
  ↓
完整性回归
  ↓
语义回归
  ↓
CHANGELOG
  ↓
发版
```

### 必需检查

1. **能力盘点**：记录基线的能力、参考集、模板、病例、示例、测试；
2. **文件保留**：基线文件必须仍然存在，除非在显式移除记录中列出；
3. **能力保留**：文件在 ≠ 能力在——必须同时比对文件清单与人可读的能力清单；
4. **最小补丁**：只改最小相关段落，不为"精简包"重写无关参考；
5. **移除协议**：任何移除都要记录

```yaml
removal:
  path: ""
  capability: ""
  reason: ""
  replacement: ""
  regression_evidence: []
  approved: false
```

6. **回归**：至少跑完整性测试 + 语义回归集。

### 什么算回归

```text
知识源注册表消失
gold / failure 病例消失
图法目录丢失关键语义区分
追踪深度或结论校验消失
文档规范弱到无法指导一篇笔记
架构 ↔ 主题 ↔ 源码 的整合不再显式
```

### 版本号规则

以"恢复丢失行为"为主要目的的修正版用 `x.y.1`。

### 动机案例（为什么写死这条纪律）

曾有一版为了强调"分阶段执行"而从零重建整包：35 个文件重建成 12 个，
`knowledge-sources/`、`evolution/`、`cases/`、`references/diagrams/` **整体消失**。
那不是演进，是回归——它违反了"新版本应在既有知识资产上演进，而不是用新抽象重新生成整个系统"。
