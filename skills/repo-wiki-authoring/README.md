# repo-wiki-authoring

仓库级**宏观文档（地图）**技能包 —— 面向任意大型代码库，产出「一个子系统一页 / 一个横切主题一张卡」的仓库 wiki：分层、模块职责与边界、数据流全景、依赖方向，每条论断都带源码坐标（`file://路径#Lx-Ly`）。

## 这是什么

一套以 Agent Skill 形式交付的**仓库 wiki 写作方法论**，核心是两族产物的硬分工：

| | `content/**`（仓库 wiki） | `knowledge/**`（知识卡） |
|---|---|---|
| 形态 | 一页 = 一个子系统；嵌套主题目录 3~4 层 | 一文档 = 一个**横切**主题（错误处理 / 日志 / 配置 / 构建…）或一个模块 |
| 骨架 | **固定 10 节** H2 结构 | 主题卡 4~5 节；模块卡 5 个固定文件 |
| 图 | 大量 `mermaid`，每张图后跟 `图表来源` | 几乎无图，文本 + 表格 |
| 溯源 | 每图 / 每节都带 `[path:start-end](file://path#Lx-Ly)` | frontmatter `source_files` + 行内 `` `path` `` |

三条不可动的规矩：**每句都有坐标**、**骨架不许自创**（读者靠它导航）、**坐标可以粗但必须在文件内**（`#L1-200` 打在一个 60 行文件上就是死锚点）。

## 目录

```
skills/repo-wiki-authoring/
├── README.md          本文件
└── skill/             当前版技能本体（= 安装到 ~/.codebuddy/skills/ 的那一份）
    ├── SKILL.md                        技能定义：边界、不变量、工作流、维护方式
    └── references/
        ├── content-page-template.md    10 节页面骨架、引用/坐标语法、mermaid 选型表
        ├── knowledge-card-template.md  `_index.yaml` / `_module.yaml` schema、模块卡 5 文件、主题卡骨架
        └── generation-workflow.md      模块建模、目录规划、逐页 `prompt`/`dependent_files` 约定、验收清单
```

**没有 `versions/`**：这个 skill 从未按版本冻结过，历史状态也没有留档，故不虚构版本谱系。

## 与相邻 skill 的关系

| Skill | 关系 |
|---|---|
| [`source-code-reading-skill/`](../source-code-reading-skill/) | **同仓并列，不同谱系**：那是面向大型 C/C++ 项目的「六阶段源码阅读知识建模」技能包；本 skill 属 `notes-hub` 体系的宏观文档技能，方法不同源、不互相派生 |
| 外部 skill `codebase-reading` / `deep-read` | **能力相邻但不替代**：`codebase-reading` 产「一个代码库 → 一套五件套」，不产 wiki 主题树与知识卡 |

> `SKILL.md` 的「Scope boundary」一节把这条边界写成了硬规则：宏观页里不写「为什么这样设计」，那属于源码笔记；同一个事实只允许有一个权威落点，另一边只链接不复述。

## 使用与维护

本仓 `skill/` 是唯一副本（`SKILL.md` 声明的正本在 `notes-hub`，该仓库不在本机），改完必须回灌安装位：

```bash
cp -r skills/repo-wiki-authoring/skill/. ~/.codebuddy/skills/repo-wiki-authoring/
diff -rq skills/repo-wiki-authoring/skill ~/.codebuddy/skills/repo-wiki-authoring   # → 无输出
```

`skill/` 的 frontmatter 已过官方校验器：`Skill is valid!`

## 已知问题

1. **`version: 0.2.0` 从未升号** —— 历史上有多个内容不同的状态同号，**不能靠版本号判断新旧**；本仓只保留最终状态，中间态无留档。
2. **`canonical` 指向本机不存在的 `notes-hub`** —— 本仓 `skill/` 是唯一可离线取用的副本。
3. **图与坐标的规模未见实测** —— 本仓没有该 skill 的 `wiki/` 全量产出样例（`SKILL.md` 提到的 worked example 在 `notes-hub` 项目的 `wiki/repowiki/`），无法自证大规模产出效果。
