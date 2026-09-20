# Resource Advisor

## 目的

只有当内部 Skill 规则或目标源码证据不足以支持当前决策时，才选择外部材料。

## 决策表

| 需求 | 首选来源类别 | 示例资源 | 预期提取的规则 |
|---|---|---|---|
| 架构视图 | 标准/方法论 | ISO 42010、SEI V&B | concern/viewpoint/view 选择 |
| 架构缩放 | 方法论 | C4、Structurizr | 抽象深度 / 一份模型多种视图 |
| 文档组织 | 方法论 | arc42、SEI | 章节与跨切面组织 |
| 区分结构与控制 | 历史方法 | Yourdon/Constantine、NS | structure_vs_control_flow |
| 数据中心的程序建模 | 方法论 | JSP、DFD | data_structure_first / dataflow 语义 |
| Renderer 能力 | 官方工具文档 | Mermaid、PlantUML、Graphviz | Renderer 选择 |
| C++ ownership 词汇 | 语言指南 | C++ Core Guidelines | ownership 防护规则 |
| 源码图提取 | 分析工具 | Clang、CodeQL、Doxygen、Sourcegraph | 源码分析后端选择 |
| 并发语义 | 系统文档 | Linux locking、LKMM | 同步/顺序防护规则 |
| 项目原生示例 | 成熟项目文档 | PostgreSQL | 项目特定导航规范 |

## 何时查询

在以下情况下查询：

```text
规则存在歧义
方法选择不确定
不熟悉某种图表记法
Renderer 存在能力限制
分析精度存在问题
出现新的重复性失败模式
```

不要仅仅为了给文档添加引用而查询。

## 如何提取经验

不要把来源中的一整段文字复制进 Skill。应将其转换为：

```text
原则
触发条件
应该做 / 不应该做
示例
边界
候选规则
```

## 权威边界

- 外部方法论定义方法；
- 官方 Renderer 文档定义工具能力；
- 目标源码定义目标实现事实；
- 人工批准的项目案例定义本项目偏好。

## 学习闭环

```text
外部来源
   ↓
提取原则
   ↓
候选规则
   ↓
目标源码测试
   ↓
案例 / 回归
   ↓
采纳或拒绝
```
