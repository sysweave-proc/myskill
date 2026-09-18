# source-code-reading-skill

面向大型 C/C++ 项目的「源码阅读知识建模」技能包 —— **七版演进 + 一个中文交付版**：v0.1 ~ v0.5.1 是同一场会话在六个时刻冻结的**原始产物**（不是从会话正文重建的），v0.6.0 是**增量合并件**，v0.6.0-zh 是它的**中文化交付版**。

## 这是什么

一套以 Agent Skill 形式交付的源码理解方法论。核心主张：不要直接写 Markdown 总结，而是先建一张**单一、可追溯的系统知识模型**，再把它投影成图、表、文档。

```
重建架构模型 → 追踪运行路径 → 规范知识图谱 → 识别主导理解模式
→ 选有证据支撑的表达方式 → 生成可导航的阅读文档 → 校验 → 从反馈中学习
```

前六版是**同一场对话在六个分享时刻**冻结下来的完整技能包，逐版叠加演进；v0.6.0 换个方式演进——
以 v0.5.1 为文件基线，把 `skill-ds/` 的认知协议**增量并进来**。

## 目录

**一个版本一个目录，进去就能看全**：「这一版讨论了什么、包长什么样、原始 zip 在哪」都在同一个 `versions/vX.Y/` 里。

```
source-code-reading-skill/
├── versions/
│   ├── v0.1/  v0.2/  v0.3/  v0.4/  v0.5/  v0.5.1/  v0.6.0/
│   │   ├── README.md       本版说明：主题、变化、包内构成、已知缺陷
│   │   ├── skill/        该版技能包文件树（可直接阅读 / diff）
│   │   ├── source.zip      该版原始 zip（权威字节，勿改）
│   │   └── conversation/   该版的讨论过程
│   │       ├── conversation.md   逐轮对话全文
│   │       ├── raw-data.json     分享页内嵌的完整会话对象
│   │       └── snapshot.html     分享页原始 HTML
│   ├── v0.6.0-zh/         中文交付版：v0.6.0 的中文化 + 13 项交付修复与加固
│   │   ├── README.md       本版说明：基准判定、修复清单、校验结果、已知边界
│   │   ├── skill/         中文技能包文件树（可用版，61 文件）
│   │   ├── source.zip      本版打包件（= skill/，权威字节）
│   │   ├── source-code-reading.skill   官方格式分发包（= skill/）
│   │   └── original-delivery/  交付的原始中文 zip（未修，仅作留证）
│   └── …                  v0.6.0 无 conversation/，其过程记录在包内 skill/MERGE_DECISION.md
├── skill-ds/              非谱系产物：读后重写版，v0.6.0 的 cognitive_execution_source
│   ├── README.md          来龙去脉、七条主张、与 v0.5.1 的取舍
│   └── skill/             技能包本体
├── docs/
│   └── evolution-audit.md  v0.1–v0.5 演进审计（v0.5.1 的立项依据）
└── README.md
```

- `skill/` 与 `source.zip` 是同一份内容的两种形态（解压 vs 压缩原件）。
- `conversation/` 里 `conversation.md` 的正文**逐字取自** `raw-data.json`（校验过：六个版本共 33,439 行正文，0 例外出自原料），但它不收录 `raw-data.json` 里的 `content.thoughts`（模型内部思考）与 `message.metadata.*`（引用来源、搜索结果 URL）——那两类不是对话正文。

## 版本谱系

| 版本 | 主题 | 文件数 | 行数 | 本版变化 |
|---|---|---|---|---|
| v0.1 | 六阶段框架 | 15 | 1,601 | 起点：把「读懂大型 C/C++ 项目」拆成六阶段流程，产出首个完整技能包 |
| v0.2 | 图表表达 | 17 | 3,022 | +2 新增、3 覆写：图画法谱系与「传统画法 vs Mermaid」取舍规则 |
| v0.3 | 外部知识源自学 | 21 | 4,345 | 新增 `knowledge-sources/` 外部资源注册表（30 条） |
| v0.4 | 架构图谱与进化 | 35 | 2,662 | **整包重写**：架构成为一等公民（System Atlas）、Path 升为一级知识对象、新增 `evolution/` + `cases/` |
| v0.5 | 执行闸门与瘦身 | 12 | 748 | **整包重写并大幅瘦身**（-66% 文件、-72% 行数）：包内只留执行协议（Gate 0~6、L0~L3、反过度设计） |
| v0.5.1 | 非回归修复 | 50 | 3,441 | 回到 v0.4 基线**增量合并**：恢复丢失资产 + 补渐进执行闸门与「不许静默丢能力」的演进纪律 |
| v0.6.0 | 认知 × 工程合并 | 59 | 4,418 | **合并件**（非会话冻结）：以 v0.5.1 为文件基线，并入 `skill-ds` 的认知协议；+9 新增 / 9 覆写 / **0 删除** |
| v0.6.0-zh | 中文化交付 | 61 | 4,700 | v0.6.0 的**完整中文化**（基准是**冻结原件**，非补丁版）+ 13 项交付修复与加固（frontmatter 校验、受控标识统一、**触发面重写**、新增**术语表**、撞号消歧、**去除全部跨 skill 引用**）；+2 新增（`TRANSLATION_NOTE.md`、`references/glossary.md`）/ 0 删除 |

**关键转折**：`v0.4 → v0.5` 是**回归**而非演进——35 个文件重建成 12 个，`knowledge-sources/`、`evolution/`、`cases/`、`references/diagrams/` 整体消失。`v0.5.1` 修回了它，并把「**新版本默认必须是 merge，不是 rewrite；删任何东西都要留下 reason / replacement / regression evidence**」固化成硬约束。

**v0.6.0 是这条硬约束的第一次正面兑现**：59 个文件里 v0.5.1 的 50 个**一个没删**，只做 +9 新增 / 9 覆写；合并决策逐条记在包内 `skill/MERGE_DECISION.md`。

## 已知问题

1. **frontmatter 过不了官方校验器 —— 根因已定位，v0.6.0 已修**（用 `skill-creator/scripts/quick_validate.py` 逐版实测）：
   - **根因**：问题不在描述正文。校验器以 `re.search(r'description:\s*(.+)', frontmatter)` 取描述，`\s*` 跨不过折叠块标量指示符 `>-` 里的 `>`，因此取到的 description 就是字面量 `>-`，必然命中 `Description cannot contain angle brackets (< or >)`。此前「描述文本不含尖括号所以可能通过」的推断不成立。
   - v0.1 / v0.2 / v0.3 / v0.4 / v0.5.1 用 `description: >-` → 同一根因；为保住各版冻结字节，**不回溯修改**。
   - v0.5 把 `description` 整个删掉、换成 `summary`，报 `Missing 'description' in frontmatter`。
   - v0.6.0 **已修**：`SKILL.md` 改为 `description: |-`，实测输出 `Skill is valid!`（描述正文未改一字）；已安装的 user skill 已同步。该修复为 post-freeze patch，故 `versions/v0.6.0/skill/` 与其 `source.zip` 不再逐字节一致，详见 `versions/v0.6.0/README.md` 备注。
   - **订正（2026-09-18 实测）**：上面这条「已修」对当时的校验器成立，但**当前** `quick_validate.py` 已把允许键收紧为 `{name, description, license, allowed-tools, metadata}`，顶层 `version` 会被直接判非法（`Unexpected key(s) ... version`），且**先于** description 检查——所以 v0.1–v0.6.0 **全部**仍然过不了校验，这次的阻塞项与 `>-` 无关。`versions/v0.6.0-zh/` 已修（`version` 移入 `metadata.version`）；各原版仍不回溯修改，以保住冻结字节。
2. **v0.4 的行尾与其他版本不齐**：其文件以单个 `\n` 结尾。早前从会话正文重建的那一版给每个文件多补了一个结尾空行，这正是 v0.4 行数出现 2,662 与 2,697 两个口径的原因。

## 保真度校验（已完成）

此前曾从会话正文「重建」过这六个版本（重建产物见 git 提交 `ab1f147`）。现用本仓的原始 zip 逐字节比对：

| 版本 | 文件数 | 字节完全相同 | 仅差结尾换行 | 真实差异 |
|---|---|---|---|---|
| v0.1 | 15 | 15 | 0 | 0 |
| v0.2 | 17 | 17 | 0 | 0 |
| v0.3 | 21 | 18 | 0 | 3 |
| v0.4 | 35 | 0 | 35 | 0 |
| v0.5 | 12 | 12 | 0 | 0 |
| v0.5.1 | 50 | 49 | 0 | 1 |
| **合计** | **150** | **111** | **35** | **4** |

4 处真实差异的性质：

- **v0.3 的 3 处**（`README.md`、`SKILL.md`、`knowledge-sources/resource-advisor.md`）：纯**空行位置**不同，文本内容一致。
- **v0.5.1 的 1 处**（`evolution/v0.4-baseline-manifest.yaml`）：重建版用了 Windows 反斜杠路径（`cases\failures\README.md`），原始版是正斜杠（`cases/failures/README.md`）——该文件是在本地 Windows 上重跑生成的。
- **v0.4 的 35 个文件**：仅差一个结尾换行。

**结论：重建版没有一处改写或编造内容**；全部差异都来自行尾、空行、路径分隔符这一层的转写损耗。
