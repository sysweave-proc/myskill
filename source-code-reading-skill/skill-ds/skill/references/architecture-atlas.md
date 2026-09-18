# 架构地基 · System Atlas

## 为什么必须先有它

面对 Linux / PostgreSQL / MySQL，最常见的失败模式不是"某个函数没读懂"，而是：

```text
局部知识很多（函数认识、struct 认识、流程也画了不少）
        ↓
但回答不了"整个系统为什么这样组织"
        ↓
笔记越写越像一堆互不相干的切片
```

System Atlas 是整个知识模型的坐标系。**任何主题，如果说不清"我在系统的哪里"，就不算被理解。**

## Atlas 的最小内容

```text
System Context                  系统边界与外部参与者
Architecture Spine              5–12 个高层元素
Critical Scenarios / Paths      跨子系统的端到端行为
Subsystem Map                   子系统职责与接口
Cross-cutting Concerns          横向关注点
Architecture ↔ Source Mappings  高层概念到源码符号的映射
Open Architecture Questions     已知的架构级未知
```

## 四层抽象 A0–A4

| 层 | 名称 | 内容 |
|---|---|---|
| A0 | System context | 边界、外部角色、外部依赖 |
| A1 | Architecture spine | 5–12 个宽粒度子系统/层，**不要试图枚举整个仓库** |
| A2 | Capability / mechanism | 子系统内部稳定的能力 |
| A3 | Runtime path / scenario | 跨子系统的端到端行为 |
| A4 | Source realization | 核心实体、符号、字段、代码区域 |

选主脊的标准：**职责互不重叠、接口稳定**。排除项：每个源码目录、每个库依赖、每个后台 worker、每个辅助函数。

## 重构方法（要的是 as-built，不是 as-designed）

对大型既有系统，架构往往只被部分记录，而且"设计意图"与"实际实现"会漂移。用八步法：

```text
1 提出架构假设
2 收集源码事实
3 抽取架构候选
4 聚类/聚合
5 重建场景与运行时路径
6 把高层元素映射到源码证据
7 模型与源码对照
8 精化
```

- **自上而下的输入**（官方文档、设计文档、公开 API、构建/模块边界、既有术语）= **假设**，不是证明；
- **自下而上的输入**（符号引用、调用/依赖图、AST、数据流/控制流、生命周期形态、运行时入口、同步与资源所有权）= **证据**。

映射要显式：

```yaml
mapping:
  high_level_element: Buffer Manager
  source_symbols: [BufferDesc, ReadBuffer_common, BufferAlloc]
  source_paths: [src/backend/storage/buffer]
  runtime_paths: [Page Read Path]
  evidence: []
```

## 静态架构 ≠ 运行时架构

两者不是同一张图，关系类型必须分开：

```text
static_depends_on
runtime_calls
runtime_sends_to
runtime_triggers
runtime_consumes
```

```text
静态：Executor → Storage
运行时：Backend → Executor
        Checkpointer → Storage
        IO Worker → Storage
```

把源码依赖和运行时因果混在一起的图，读起来一定错位。

## 边界与外部系统

架构图不能只画"PostgreSQL"这一个盒子。至少支持四类元素：

```text
Internal / Boundary / Interface / External
```

外部包括 OS、Filesystem、Kernel、CPU、Network、Disk、Client、Compiler、Libraries、Plugin、Extension。研究 IO 时：

```text
PostgreSQL → filesystem → kernel VFS → block layer → NVMe
```

这条链本身就是核心知识，不是背景介绍。

## 关键路径是一等知识对象

它把本来孤立的子系统连起来。典型类别：

```text
request/query path      transaction path      data read path
data write path         recovery path         background maintenance path
startup/shutdown path
```

## 反模式

```text
directory-tree-as-architecture
single giant architecture diagram
architecture inferred from naming alone
architecture frozen after the first draft
architecture claims without scenario validation
```

## 自检：Atlas 有没有用

好的 Atlas 必须能回答：

1. 某个主题位于哪里？
2. 哪些主要路径会用到它？
3. 它依赖哪些邻接子系统？
4. 读者能不能从架构缩放到源码再缩回来？
5. 它能不能解释至少一个端到端的代表场景？

## 知识缺口要显式记录

关键路径上缺失的节点，即使没有缺文件，也是知识缺口：

```text
Path: A → B → C → D
Known: A ✓ B ✓ C ? D ✓
Gap: C
```

把它记成 `open_question` / `knowledge_gap`，**不要用猜出来的关系把洞填平**。
