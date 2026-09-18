# knowledge-sources/

该目录是 Source Code Reading Skill 的外部学习注册表。

该注册表与 Skill 主规则刻意分离：

```text
Skill rules
    = Agent 应该做什么

Knowledge sources
    = Agent 可以从哪里学习某条规则为什么存在、某种记法是什么意思，以及成熟系统如何使用它
```

## 文件

- `index.yaml` — 机器可读的资源注册表。
- `resource-advisor.md` — Agent 何时/如何查阅资源，以及如何把资源内容转化为规则。

## 资源角色

### Methodology

教授抽象与表达选择：

```text
SEI Views & Beyond
C4
arc42
UML
Structured Design
Nassi–Shneiderman
JSP
HIPO
```

### Renderer

说明具体记法/工具实际上能够表达什么：

```text
Mermaid
PlantUML
Graphviz
Structurizr
```

### Analysis backend

教授如何提取或验证源码事实：

```text
Clang AST / LibTooling
CodeQL
Doxygen
Sourcegraph
```

### Domain guardrail

教授 C/C++ 与系统语义：

```text
C++ Core Guidelines
Linux locking
Linux Kernel Memory Model
```

### Project examples

教授成熟项目如何暴露真实源码架构：

```text
PostgreSQL
Linux kernel
Structurizr pattern catalog
arc42 worked examples
```

## 维护规则

新增资源时必须记录：

```text
它教授什么
什么时候查询它
什么时候不得使用它
它可以直接支持哪些事实
它应该影响哪条 Skill 规则
```

只有 URL、没有学习角色的资源，不构成有用的 Skill 依赖。

## v0.5.1 维护说明

该注册表属于持久化 Skill 资产集的一部分，在版本演进过程中不得消失。除非经过明确批准并完成回归测试，否则必须保留它。
