# v0.6.0-zh

**主题**：v0.6.0 的完整中文化 + 交付修复 + 术语与触发面加固 ｜ **规模**：61 文件 / 4,700 行（47 `*.md` / 12 `*.yaml` / 2 `*.py`）

## 本版是什么

不是新一版方法论，而是 [`../v0.6.0/`](../v0.6.0/) 的**中文交付版**。主张、规范强度与 v0.6.0 一致；改动集中在语言、交付缺陷、术语唯一性与触发面。

| | |
|---|---|
| 内容基准 | `../v0.6.0/source.zip`（**冻结原件**，不是 post-freeze 补丁版） |
| 语言策略 | 正文中文；`System` / `Path` / `Claim` / `Evidence` / `Source Anchor` / `Pattern` / `Renderer` 等承担规范语义或机器识别作用的术语保留英文，首次出现给中文解释 |
| 术语准绳 | `skill/references/glossary.md`——**唯一**的中英对照与正名来源，一个概念只有一个英文原名和一个中文正名 |
| 未动的东西 | 目录结构、文件名、规范 ID、关系名、YAML 键名、测试接口 |

**翻译基准的判定依据**（三条，可复核）：

| 证据 | 冻结 `source.zip` | 补丁版 `skill/` | 本版 |
|---|---|---|---|
| `SKILL.md` frontmatter | 顶层 `version:` + `description: >-` | `metadata.version` + `\|-` | 同冻结版 |
| `CHANGELOG.md` | 25 行，无 `Fixed (post-freeze patch)` 段 | 42 行，有 | 26 行，无 |
| `tests/test_skill_integrity.py` 守卫 | 无 | 有 | 无 |

因此本版 `CHANGELOG.md` 比 v0.6.0 少一段，**不是漏译**，是忠实对应冻结原件。

## 交付修复与加固（13 项）

逐条留痕在包内 `skill/TRANSLATION_NOTE.md` 的「交付后修订记录」。

| # | 位置 | 问题 | 处理 |
|---|---|---|---|
| 1 | `SKILL.md` frontmatter | 顶层 `version` 键 → 官方校验器直接判非法；`>-` 是 v0.6.0 已修项的旧写法 | `version` 移入 `metadata.version`；改 `\|-` |
| 2 | `SKILL.md` §10 第 5、17 条 | 漏译 | 译中 |
| 3 | `references/knowledge-model.md` §7 第 3–6 条 | 漏译，且与 `SKILL.md` §10 同位条目措辞不一致 | 译中并对齐 |
| 4 | `tests/__pycache__/` | 随包携带 `*.pyc` | 删除 |
| 5 | `templates/source-reading-note.md` 篇头 | `**Core Question**` 会被逐字带进成品笔记 | 改 `**核心问题**` |
| 6 | `evolution/evolution-policy.md` 的 yaml 块 | 顶层键 `removal:` 被译为 `移除:`，与同块子键及 `templates/evolution-change.yaml` 自相矛盾 | 改回 `removal:` |
| 7 | `references/tracing/trace-policy.md`、`references/validation/validation-policy.md`、`references/execution-progressive.md`、`references/tracing/exploration-policy.md` | **受控标识双轨**：这些文件把标识译成了纯中文（`D1 局部`、`V1 结构`、`L0：定位`、`L0 目标符号`），而 `SKILL.md` 与快速入口页保留英文标识 | 统一为「英文标识 + 中文释义」：`D1 Local（局部事实）`、`V1 Structural（结构）`、`L0 Orientation（定位）` |
| 8 | `SKILL.md` frontmatter（`description` / `metadata`） | **无触发面**：描述只讲方法论，没有「用户说什么话时该用本技能」，也没有边界声明 | 重写为「是什么 + `This skill should be used when the user asks to …`（中英触发词）+ `SCOPE BOUNDARY`」三段式，并补 `metadata.scope / canonical / companion` |
| 9 | 新增 `references/glossary.md`（＋ `SKILL.md` §0 指针） | 全包没有术语表：`Concern`、`Path`、`Mechanism` 等受控术语无定义、可多义使用 | 逐条给出「英文原名 / 中文正名 / 定义 / 权威位置」，并单列消歧章：`Concern` 的四种角色、三套 `L` 编号、`Path` vs `Flow` 等 |
| 10 | `references/tracing/exploration-policy.md` | 上下文扩展顺序梯子写作 `L0–L6`，与 `SKILL.md` §5 的深度等级 `L0–L3` **撞号** | 改为 `C0–C6`；`L1–L4` 演进四级保持不变，改由术语表说明三者区别 |
| 11 | 打包方式 | 交付物只有自定的 `source.zip` | 用官方 `package_skill.py` 产出 `source-code-reading.skill`，与 `source.zip` 并存；自检清单登记新增资产 |
| 12 | `SKILL.md` frontmatter —— **撤回第 8 项的一半** | 第 8 项写的 `SCOPE BOUNDARY` **点名了另外两个 skill**（`source-notes-authoring` / `repo-wiki-authoring`），并加了 `metadata.companion` | 删除对其它 skill 的**具名引用**；边界声明改为按**交付物类型**划界（不点名）；移除 `metadata.companion`。Skill 必须自包含 |
| 13 | `README.md`、`MERGE_DECISION.md`、`MERGE_MANIFEST.yaml` | 包内**出处记录**仍以专名引用 `skill-ds`（v0.6.0 合并的两个输入之一） | 专名中性化为「**再表达件**」（机器可读处 `cognitive-reexpression` / `cognitive-reexpression-variant`）。**只换专名，语义不动**：两个输入、各自强项、合并事实全部保留 |

**第 1 项是关键**：官方 `quick_validate.py` 允许的 frontmatter 键为 `{name, description, license, allowed-tools, metadata}`，顶层 `version` 会被直接判非法。此项**同时影响 `../v0.6.0/` 原版与已安装的 user skill**，不限于本中文版。

**第 8 项是触发率的落点**：同场两个 companion skill（`source-notes-authoring` / `repo-wiki-authoring`）都写了 `Use when …` + `SCOPE BOUNDARY`，只有本技能两个都没有——描述是触发层唯一可见文本，原描述没有描述任何触发场景。依据 `skill-creator` 指南重写，并补 `metadata.companion` 把三者路由关系写进元数据。

## 校验结果

```text
quick_validate.py                  → Skill is valid!
tests/test_merged_capabilities.py  → PASS（16 项资产检查 + 11 项核心标记）
source.zip  与  skill/             → 逐文件完全一致
source-code-reading.skill          → 官方 package_skill.py 产出，内部根目录 source-code-reading/
```

语义精度抽检（对照 `../v0.6.0/skill/`）：

| 检查项 | 结果 |
|---|---|
| 行内反引号标识丢失 | 0 处 |
| 数字 / 阈值不一致 | 0 处 |
| 强模态弱化（`must`/`never`/`only` → 必须/永远/只…） | 0 处 |
| YAML 键名被译 | 仅上表第 6 项一处，已修 |
| 正文行数偏差 >25% 的文件 | 0 个 |
| 受控标识（`D1–D3` / `V1–V6` / `L0–L3` / `C0–C6`）跨文件写法 | 已统一（第 7、10 项） |

## 目录

```text
versions/v0.6.0-zh/
├── README.md                    本文件
├── skill/                       中文技能包文件树（61 文件，可直接安装 / 阅读 / diff）
├── source.zip                   本版打包件（= skill/，权威字节）
├── source-code-reading.skill    官方格式分发包（= skill/，供安装/分发）
└── original-delivery/
    └── source-code-reading-skill-v0.6.0-zh.zip   交付的原始中文 zip（未修，保持原样，仅作留证）
```

- **与其它版本不同**：本版 `source.zip` **就是可用于安装的修正版**。因为它不是「会话冻结原件」，而是「交付件」；原始交付件因此另存于 `original-delivery/`，不覆盖、不改动。
- `source.zip` 是本仓约定（与其它版本对齐）；`source-code-reading.skill` 是官方分发格式。两者内容相同、便于不同用途，**若嫌冗余可只保留其一**。
- 本版没有 `conversation/`：它不是会话冻结产物（同 v0.6.0）。

## 已知边界

1. **仍缺 v0.6.0 的 post-freeze 第 2 项修复**：`tests/test_skill_integrity.py` 未加「基线/候选目录存在且非空」守卫。该项只影响发版流程自检的可靠性，不影响运行时使用；需要时可从 `../v0.6.0/skill/tests/test_skill_integrity.py` 同步。
2. **`test_skill_integrity.py` 对中文版按定义过不去**：它以 v0.4 基线做 SHA-256 逐字节比对，而翻译必然改变每个被译文件的字节，于是全部落入「未批准的基线内容变更」。该测试服务于「合并发版」流程，不应作为中文变体的交付判据。
3. **还剩一处「同号不同义」（EN 原件即有）**：`SKILL.md` §5 的深度等级 `L0–L3` 与 `SKILL.md` §13.1 的演进四级 `L1–L4` 仍共用 `L` 前缀。二者轴不同（理解深度 / 技能自身演进等级），且演进编号跨 `SKILL.md`、`evolution/evolution-policy.md` 与历史记录 `MERGE_DECISION.md`，改名会牵动历史记录，故本次**不改号**，改由术语表 §10.2 明确区分。扩展顺序梯子撞号（原 `L0–L6`）已在第 10 项修掉。
4. **受控标识的统一方向**：第 7 项修复后，包内标识一律采用「英文标识 + 中文释义」（`D1 Local（局部事实）`、`V1 Structural（结构）`、`L0 Orientation（定位）`）。若后续新增内容，请沿用该形式，并先在 `references/glossary.md` 登记。
