# 外部知识源 · Knowledge Sources

外部资料不是链接收藏夹，而是技能的"**老师**"：只有在核心规则或目标源码证据不足以做当前决定时才去请教。

## 什么时候查

```text
规则含糊
方法选择没把握
不熟悉某种记号
渲染器表达不了
分析精度不够
出现新的反复性失败
```

**不要为了"给文档加引用"去查。** 查是为了做决定。

## 决策表

| 需求 | 首选来源类别 | 例子 | 期望提炼出的规则 |
|---|---|---|---|
| 架构视点 | 标准/方法论 | ISO 42010、SEI V&B | concern/viewpoint/view selection |
| 架构缩放 | 方法论 | C4、Structurizr | 抽象层次、一份模型多种视图 |
| 文档组织 | 方法论 | arc42 | 章节与横向关注点组织 |
| 区分结构与控制 | 历史方法 | Yourdon/Constantine、Nassi-Shneiderman | structure_vs_control_flow |
| 数据为中心建模 | 方法论 | JSP、DFD | data_structure_first、dataflow 语义 |
| 渲染器能力 | 官方工具文档 | Mermaid、PlantUML、Graphviz | renderer selection |
| C++ 所有权词汇 | 语言指南 | C++ Core Guidelines | ownership guardrails |
| 源码图抽取 | 分析工具 | Clang、CodeQL、Doxygen、Sourcegraph | backend choice |
| 并发语义 | 系统文档 | Linux locking、LKMM | synchronization/order guardrails |
| 项目原生范例 | 成熟项目文档 | PostgreSQL | 项目特定的导航惯例 |

## 注册 schema

每个资源登记：

```yaml
id:
name:
category: methodology | standard | renderer | analysis_tool | project_example | language_semantics | archival
authority: Tier-1 | Tier-2 | ...
url:
verification:
teaches:            它教什么
query_when:         什么时候查
do_not_use_when:    什么时候别用
direct_fact_scope:  能直接作为事实依据的范围
extract_to_rules:   应提炼成哪些规则
```

## 如何提炼（不要抄段落）

```text
Principle  原理
Trigger    触发
Do / Don't 正反
Example    例子
Boundary   边界
Candidate Rule 候选规则
```

## 权威边界

```text
外部方法论      定义"方法"
渲染器官方文档  定义"工具能力"
目标源码        定义"目标实现事实"
人批准的项目病例 定义"本地偏好"
```

外部资料**可以**定义记号语义、教方法论、给正反例、建议分析技术、说明工具能力；
**不可以**推翻目标仓库事实、在没有目标证据时证明目标行为、或仅凭外观把渲染器语法当成形式记号。

## 学习闭环

```text
外部资料 → 提炼原理 → 候选规则 → 目标源码回放 → 病例/回归 → 采纳或否决
```
