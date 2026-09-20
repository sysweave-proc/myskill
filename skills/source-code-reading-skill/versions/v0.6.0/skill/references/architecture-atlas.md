# Architecture Atlas · 操作卡

System Atlas 是源码阅读知识模型的持久坐标系。它不是“一张完整大图”，而是一组可被主题挂载的稳定坐标。

## 最小结构

```text
System Context
Architecture Spine
Subsystem Map
Critical Scenarios / Paths
Cross-cutting Concerns
Architecture ↔ Source mappings
Open Architecture Questions
```

## 使用原则

1. 大型系统优先加载已有 Atlas；没有时按需重构。
2. A1 Architecture Spine 只保留约 5–12 个高层元素。
3. 主题必须能回答“它在哪、被哪条路径使用、依赖谁”。
4. Atlas 是图，不是严格树。
5. 新证据可以修订甚至推翻旧坐标；保留冲突原因。

## 主题坐标

```yaml
architecture_position:
  system: ""
  subsystem: ""
  layer: ""
  mechanisms: []
  paths: []
  concerns: []
  upstream: []
  downstream: []
  neighboring_topics: []
```

详细规范见 `references/architecture-model.md` 与 `references/architecture-reconstruction.md`。
