# Core Skill 与扩展能力的边界

## 原则

Core Skill 应编码稳定的推理规则，而不是囊括每一个具体工具。

## Core

- 六阶段推理协议；
- 渐进式执行闸门；
- 规范知识模型；
- 架构/路径/主题/源码集成；
- Pattern 识别；
- Claim/Evidence/Traceability；
- 表达规范；
- Validation；
- 演进/非回归规则。

## Capability extensions

工具特定的能力应位于规范核心之外，例如：

```text
Clang AST / LibTooling
CodeQL
Sourcegraph
Doxygen
perf / BPF
VTune
static-analysis backends
runtime tracing backends
```

扩展可以产生供 Core Model 消费的证据，但不得静默地重新定义源码语义。

## Knowledge sources

方法论、标准、Renderer 文档、语言指导以及成熟项目示例属于 `knowledge-sources/`。它们教授方法和工具能力；对于目标实现事实，目标仓库仍然是权威来源。

## Evolution assets

反馈、gold cases、failure cases、候选规则和回归结果属于 `cases/` 与 `evolution/`。
