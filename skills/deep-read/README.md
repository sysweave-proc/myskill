# deep-read

**外部来源、本机在用的 skill**：逐行读真实源码，回答具体问题。

## 是什么

| 项 | 内容 |
|---|---|
| 干什么 | 回答「这个函数到底在做什么」「这条调用链怎么走」「这个数据结构怎么变」「这个结论在源码里成立吗」——**出事实，不写交付文档** |
| 怎么干 | 6 阶段协议：定范围 → 结构测绘 → 执行流追踪 → 深读 → 模式归纳 → 结构化报告。**每条结论必须落到 `文件:行号`** |
| 原则 | 源码是唯一事实来源：文档会过时、注释会腐烂、函数名会误导。LSP / 代码图谱只用于**定位**，不作依据；图索引命中后必须回源码核对 |
| 包内 | `skill/SKILL.md` + `skill/references/reading-strategies.md` |

## 来源与本地改动

- 从本机安装位 `~/.codebuddy/skills/deep-read/` 回收的副本
- **上游未定位**：在上游 `agent-alchemy` 全仓检索无命中，无原件可比
- **唯一本地改动**：`description` 追加了中文触发词（上游只有英文触发词）

## 维护

`skill/` 就是安装形态，改完回灌安装位：

```bash
cp -r skills/deep-read/skill/. ~/.codebuddy/skills/deep-read/
diff -rq skills/deep-read/skill ~/.codebuddy/skills/deep-read   # → 无输出
```
