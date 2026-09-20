# 案例学习

## 案例结构

有价值的案例应该保存完整的决策上下文，而不只是最终 Markdown。

```text
Case
├── task
├── source context
├── architecture position
├── knowledge model
├── pattern profile
├── representation plan
├── generated document
├── feedback
├── failure analysis
├── correction
└── learned rule(s)
```

## Gold case

经过人工/项目审查、适合用于回归测试的结果。

## Failure case

暴露出可重复弱点的结果。Failure case 只有在记录了失败原因时才真正有价值。

## Case similarity

使用以下维度检索相似案例：

```text
系统领域
核心问题
Pattern
表达族
关系类型
源码语言
失败类型
```

不要仅凭词汇相似度就把两个案例视为语义相似。
