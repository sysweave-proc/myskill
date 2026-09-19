# myskill

个人 Skill 资产仓。**一个 Skill 一个顶层目录**，每个目录自带 README 说明其结构与来龙去脉。

## Skill 索引

| Skill | 说明 | 版本 |
|---|---|---|
| [`source-code-reading-skill/`](source-code-reading-skill/) | 面向大型 C/C++ 项目的「源码阅读知识建模」技能包：`versions/` 存七版演进（含原始 zip、解压产物、对话原始材料），顶层 `skill-ds/` 存非谱系的对照版（v0.6.0 的合并输入） | v0.1 → v0.6.0 |
| [`repo-wiki-authoring/`](repo-wiki-authoring/) | 面向任意大型代码库的「仓库级宏观文档（地图）」技能包：产出子系统 wiki（固定 10 节骨架 + mermaid + 源码坐标 `file://path#Lx-Ly`）与横切知识卡；源自 `notes-hub` 体系，与 `source-code-reading-skill` 同域但**不同源、不互相派生** | v0.2.0（单版，无谱系） |

> **变动记录**：原顶层 `skill-ds/` 已移入 `source-code-reading-skill/skill-ds/`（它不属于版本谱系，保留作 v0.6.0 的对照与输入材料）；`skill-ds-chatgpt/` 已删除（质量不达标）。
>
> **2026-09-19 目录变动**：新增 `skill-test/`（外部 skill 实测区，产物为其下的 `postgres-notes/`）；原 `_disabled-skills/source-code-reading/` 删除——与本仓 `source-code-reading-skill/versions/v0.6.0-zh/skill/` 逐字节一致（`diff -rq` 差异 0 条），属冗余副本。
>
> **2026-09-19 停用区收尾**：`repo-wiki-authoring` 从 `_disabled-skills/` 恢复到 `~/.codebuddy/skills/`，并进一步**提升为顶层 skill 目录** [`repo-wiki-authoring/`](repo-wiki-authoring/)（`diff -rq` 两次校验均差异 0 条）；`source-notes-authoring` 按用户要求删除——曾判为「无副本、不可恢复」，**当日复查推翻该判定**：本机 `rm` 实为「移入回收站」的包装函数，回收站 `source-notes-authoring.24` 与删除版内容一致（逐文件 diff 行数 139/169/97/89 全同），**可随时取回**。`_disabled-skills/` 目录本身已按用户要求整体删除，其台账要点并入本条。
>
> **2026-09-19 外部 skill 备份**：新增 [`external-skills/`](external-skills/)——把当日安装的**外部** skill 原样复制留档，并记录内容指纹基线，**供日后检查上游是否更新**（其 frontmatter 均无 `version`，只能比指纹）。
>
> **2026-09-19 外部依赖整包入库**：`codebase-analysis` 非自足包，其依赖的上游插件 `agent-alchemy-core-tools` **v0.2.3**（26 文件）同期原样入库，与上游 `claude/core-tools/` 逐文件 blob SHA 校验一致。
>
> **2026-09-19 外部资产区收口（二次定稿）**：`external-skills/` 最终定型为 `skills/`（本机安装的独立 skill，叶）＋ [`agent-alchemy-marketplace/`](external-skills/agent-alchemy-marketplace/)（上游市场整包镜像，容器）。**三处调整**：① `codebase-analysis` 从 `skills/` 移出——它只是插件内的一个 skill，上游原件在镜像内，重复留档无意义，且已确认后续不使用；② 早期独立归档 `agent-alchemy-core-tools/` 并入镜像 `core-tools/`；③ 撤销 `CATALOG.md`（索引职责归 `external-skills/README.md`，避免两处口径漂移）。镜像扩为 **6 插件 ＋ 1 VS Code 扩展 ＋ 市场注册表**，并补齐两处**真实断链**：`claude-tools`（`sdd-tools` 27 处跨插件引用）与 `.claude-plugin/marketplace.json`（`plugin-tools` 5 处引用）。
>
> **2026-09-19 基线可复算化**：外部区指纹口径统一为 `find . -type f ! -name PROVENANCE.md | LC_ALL=C sort | xargs md5sum | md5sum`，并**作废全部历史指纹值**——旧值既受 `sort` 的 locale 影响（换环境不可复现），又有一个「把自身 md5 写进自身」的自引用失效值。同日重下上游 `main` 全量 `diff -rq`：6 插件 + 扩展 + 注册表**零差异**，`core-tools` 26 个上游文件 `md5sum -c` 26/26 通过，上游 HEAD 仍为 `fc1a336b`（2026-05-31，未更新）。
>
> **v0.6.0 post-freeze 修复**（2 项，均已实测）：`SKILL.md` 的 `description: >-` → `|-`（原写法令官方校验器七版全 fail，改后 `Skill is valid!`）；`tests/test_skill_integrity.py` 增加基线目录存在性/非空守卫（原版传错路径会假通过）。因此 `versions/v0.6.0/skill/` 与其 `source.zip` 不再逐字节一致，记录见该版 `README.md` 备注与 `skill/CHANGELOG.md`。

## 目录约定

新增 Skill 时按下面这套结构建目录，并登记到上面的索引表：

```
<skill-name>/
├── README.md           技能说明：这是什么、版本谱系、已知问题
├── versions/           一版一个目录，进去就能看全
│   └── vX.Y/
│       ├── README.md       本版说明：主题、变化、包内构成
│       ├── skill/        该版交付产物（文件树，可读）
│       ├── source.zip      该版原始打包（权威字节，勿改）
│       └── conversation/   该版的讨论过程（会话全文、原始数据、页面快照）
├── <对照目录>/          可选：不属于版本谱系的对照产物（读后重写、他源再表达等），与 versions/ 平铺
└── docs/               跨版本的审计报告、设计说明等
```

约定：**按版本聚合**，而不是按文件类型分散——想知道「某一版是什么」，进一个目录就够；`skill/` 与 `source.zip` 是同一份内容的两种形态（解压 vs 压缩原件）。

**从未按版本冻结过的 skill 可省去 `versions/`**：把本体直接放顶层 `skill/`，并在自己的 README 里写明为何没有版本谱系（如 [`repo-wiki-authoring/`](repo-wiki-authoring/)）。

## 其他目录（非 Skill）

以下目录不出现在上面的 Skill 索引表里，因为它们是**运维区**或**实测产物**，不是 Skill 资产：

| 目录 | 说明 |
|---|---|
| [`external-skills/`](external-skills/) | **外部资产备份区（不是本仓资产）**，一级两类：`skills/` = 本机安装的独立 skill 原样留档（可安装单元，叶；现为 `codebase-reading` / `deep-read`）；[`agent-alchemy-marketplace/`](external-skills/agent-alchemy-marketplace/) = 上游市场整包镜像（容器，不可直接装；6 插件 + 1 VS Code 扩展 + 市场注册表）。含**可复算的逐包指纹基线 + 基准 commit**，**需定期检查上游是否更新**；上游已定位为 [`sequenzia/agent-alchemy`](https://github.com/sequenzia/agent-alchemy)。全部口径、已知本地偏差、更新检查命令见其 `README.md` |
| [`skill-test/`](skill-test/) | 外部 skill 实测区：2026-09-19 用 `codebase-analysis` / `codebase-reading` / `deep-read` 实测的落盘结果；产物为 [`skill-test/postgres-notes/`](skill-test/postgres-notes/)（PostgreSQL 19beta2 源码阅读笔记，两条主线共 6 篇） |

> **环境提醒**：本机的 `rm` 是包装函数（`rm() { "${CODEBUDDY_SAFE_DELETE_BIN_DIR}/rm" "$@"; }`），行为是**移入回收站**而非真删；跨文件系统（`/mnt/disk` ↔ `/`）时甚至不留 `.trashinfo`。所以「删掉」未必等于内容消失——核查删除结果时要看实际，而不是看命令返回；要真删需用 `/usr/bin/rm` 并清理回收站里对应副本。
