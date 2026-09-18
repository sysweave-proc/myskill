# 知识源选择矩阵

```text
架构 concern？
  → ISO 42010 / SEI / C4 / arc42

需要正式 UML 语义？
  → OMG UML

需要区分结构与 flow？
  → Yourdon/Constantine / NS

需要遗留系统层次 + IPO？
  → HIPO

需要数据结构优先的建模？
  → JSP

需要图表渲染？
  → Mermaid / PlantUML / Graphviz

需要一个模型 + 多个视图？
  → Structurizr

需要精确的 C/C++ 符号关系？
  → Clang AST

需要精确的源码级 dataflow / query？
  → CodeQL / Clang Dataflow

需要生成的定位图？
  → Doxygen

需要大型仓库导航？
  → Sourcegraph

需要 C++ ownership 词汇？
  → C++ Core Guidelines

需要 Linux 并发/内存顺序示例？
  → Linux locking / LKMM

需要 PostgreSQL 原生示例？
  → PostgreSQL developer/coding docs
```

始终遵守 `index.yaml` 中定义的权威边界。
