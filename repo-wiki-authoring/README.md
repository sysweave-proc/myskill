# repo-wiki-authoring

仓库级**宏观文档（地图）**技能包 —— 面向任意大型代码库，产出「一个子系统一页 / 一个横切主题一张卡」的仓库 wiki：分层、模块职责与边界、数据流全景、依赖方向，每条论断都带源码坐标（`file://路径#Lx-Ly`）。

与同仓 [`source-code-reading-skill/`](../source-code-reading-skill/) 并列存放，但**不同谱系**（见下「与相邻 skill 的关系」）。

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
repo-wiki-authoring/
├── README.md          本文件
└── skill/             当前版技能本体（= 安装到 ~/.codebuddy/skills/ 的那一份）
    ├── SKILL.md                        技能定义：边界、不变量、工作流、维护方式
    └── references/
        ├── content-page-template.md    10 节页面骨架、引用/坐标语法、mermaid 选型表
        ├── knowledge-card-template.md  `_index.yaml` / `_module.yaml` schema、模块卡 5 文件、主题卡骨架
        └── generation-workflow.md      模块建模、目录规划、逐页 `prompt`/`dependent_files` 约定、验收清单
```

**没有 `versions/`**：这个 skill 从未按版本冻结过（见「已知问题」第 1 条），历史状态也没有留档，故不虚构版本谱系。这与 `source-code-reading-skill/` 的「一版一目录」形态不同，属刻意取舍。

## 与相邻 skill 的关系

| Skill | 关系 | 现状 |
|---|---|---|
| [`source-code-reading-skill/`](../source-code-reading-skill/) | **同仓并列，不同谱系**：那是一个面向大型 C/C++ 项目的「六阶段源码阅读知识建模」技能包（v0.1 → v0.6.0-zh 八版演进），方法来自另一场会话；本 skill 属 `notes-hub` 体系的宏观文档技能，方法不同源、不互相派生 | 在本仓顶层并列 |
| `source-notes-authoring` | **同一代码库文档族的另一半（微观）**：它写「一个机制 = 一篇」的地形成文（真实调用链 + 文件/符号名），本 skill 写「地图」（子系统 + 粗坐标）。两者**硬分工、不重叠、互相链接** | 已于 2026-09-19 从本仓删除；内容仍可从本机回收站取回，原委见顶层 [`README.md`](../README.md) 的「变动记录」 |
| 本机在装的外部 skill `codebase-analysis` / `codebase-reading` / `deep-read` | **能力相邻但不替代**：`codebase-analysis` 只产**单份**勘探报告，不产 wiki 主题树与知识卡；`codebase-reading` 产「一个代码库 → 一套五件套」 | 与本 skill 同时安装，触发时按「是否要主题树 + 坐标 + 知识卡」区分 |

> `SKILL.md` 的「Scope boundary」一节把这条边界写成了硬规则：宏观页里不写「为什么这样设计」，那属于源码笔记；同一个事实只允许有一个权威落点，另一边只链接不复述。

## 来源与沿革

```bash
~/.codebuddy/skills/repo-wiki-authoring/          # 原始安装位（agent 实际加载这里）
  → 2026-09-19  为给新装的外部 skill 腾出干净测试环境，停用移出至 _disabled-skills/
  → 2026-09-19  按用户要求恢复安装到 ~/.codebuddy/skills/
  → 2026-09-19  提升为本仓顶层 skill 目录（本目录）
  → 2026-09-19  _disabled-skills/ 目录整体删除（现已无此目录）
```

- 回收站里曾积压 **5 个不同内容状态**的历史副本（2026-09-12 / 09-13 / 09-16 / 09-18 / 09-19），均为同 4 文件、frontmatter 一律写 `version: 0.2.0`（从未升号）；按指示**未收进 `versions/`**，并已**彻底清除**：本机 `rm` 是「移入回收站」的包装，第一次删除只把它们嵌套进了回收站（`repo-wiki-authoring.*.2`），复核后用 `/usr/bin/rm` 连同 `.trashinfo` 一次清空（共 130 项）。历史状态据此**不可再恢复**，本仓只保留最终状态。
- 升级/同步方式（`SKILL.md` 的 Maintenance 节）：仓库正本声明为 `notes-hub/infra/skills/repo-wiki-authoring/`，用 `notes.sh install | status | export` 双向同步；**本机无 `notes-hub`**，所以本仓 `skill/` 就是本机唯一副本，改完记得回灌安装位：

```bash
cp -r repo-wiki-authoring/skill/. /root/.codebuddy/skills/repo-wiki-authoring/
diff -rq repo-wiki-authoring/skill /root/.codebuddy/skills/repo-wiki-authoring   # → 无输出
```

## 校验

`skill/` 的 frontmatter 已过官方校验器（`skill-creator/scripts/quick_validate.py`）：

```bash
python3 <skill-creator>/scripts/quick_validate.py repo-wiki-authoring/skill
# → Skill is valid!
```

（`source-code-reading-skill/` 各版之所以过不了，是 `description: >-` 与顶层 `version` 键的问题；本 skill 用的是 `description` 普通标量 + `metadata.version`，不踩这两个坑。）

## 已知问题

1. **`version: 0.2.0` 从未升号**：5 个历史状态内容不同却同号，**不能靠版本号判断新旧**；本仓只保留最终状态，中间态无留档。
2. **`canonical` 指向本机不存在的 `notes-hub`**：`SKILL.md` 的 Maintenance 节把 git 正本写在 `notes-hub/infra/skills/repo-wiki-authoring/`，该仓库不在本机；本仓 `skill/` 是唯一可离线取用的副本。
3. **图与坐标的规模未见实测**：本仓没有该 skill 的 `wiki/` 全量产出样例（`SKILL.md` 里提到的 worked example 在 `notes-hub` 项目的 `wiki/repowiki/`），本仓无法自证其大规模产出效果。
