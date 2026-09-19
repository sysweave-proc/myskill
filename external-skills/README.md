# external-skills（外部资产归档区 · 上游基准基线）

> ## ⚠️ 这里的资产不是本仓资产
>
> 本目录存放**外部来源**的第三方插件与技能资产，**不是本仓自建、也不由本仓维护**。存进这里只为**离线基准 + 版本比对基线**。
> **它们需要定期检查是否更新**——上游一旦发新版，本备份就会过期，而本仓没有任何自动机制会知道。
> 本目录内的**被备份内容**是**只读**：不要改；agent 实际加载的是 `~/.codebuddy/skills/`，改安装位后如需留档再回收至此。
> （本文件是索引与更新基线，不属于被备份内容。）

归档日期：**2026-09-19**（与安装、校验同日）。

---

## 一、基准坐标（"原版真实"的证据）

| 项 | 值 |
|---|---|
| 上游仓库 | [`github.com/sequenzia/agent-alchemy`](https://github.com/sequenzia/agent-alchemy) |
| 作者 / 许可 | Stephen Sequenzia ／ MIT |
| **基准 commit** | `fc1a336b8267e70579af8517d14718e626824e54` |
| commit 日期 | `2026-05-31T22:30:00Z` |
| 归档日期 | `2026-09-19` |
| 校验方式 | 归档当日重下上游 `main` zip，对全部包做 `diff -rq` 全量比对 |

**校验结论（2026-09-19 实测，全部通过）：**

1. 6 个插件＋扩展＋市场注册表，与上游**逐文件零差异**。
2. `core-tools` 的 26 个上游文件 `md5sum -c` **26/26 OK**。
3. 上游 `commits/main` 仍为 `fc1a336b`——**距今 4 个月未更新**，本基线即最新。
4. 全镜像 `${CLAUDE_PLUGIN_ROOT}` 引用实检：154 处中 125 处解析为真实文件，**29 处经甄别全部为文档示例/占位符**，无隐藏依赖缺口。

---

## 二、目录结构：一级轴只表达「归档来源」

本目录里是**两种不同层级的东西**。规则定死为三条：

1. **一级轴只表达归档来源** —— 本机安装的独立 skill 一组，上游市场镜像整包一件。
2. **不给上游目录改名** —— 插件目录名就是**插件身份**：上游包无 `plugin.json`，Claude Code 按目录名推导插件名，改名会让 `agent-alchemy-core-tools:code-architect` 这类 `插件名:agent` 引用对不上。
3. **包内结构一律原样** —— `skills/` / `agents/` / `hooks/` 是插件规范的**默认发现位置**；改名即多个 skill 全部扫不到。

```
external-skills/                            172 文件
├── README.md                               ← 本文件（索引 + 更新基线）
├── skills/                                  ← A 类 · 本机安装的独立 skill（叶子，根有 SKILL.md）
│   ├── codebase-reading/     SKILL.md + references/ ×3
│   └── deep-read/            SKILL.md + references/ ×1
│
└── agent-alchemy-marketplace/              ← B 类 · 上游市场整包镜像（165 文件）
    ├── README.md                           （本地文档，非上游文件）
    ├── .claude-plugin/marketplace.json     ← 市场注册表（版本号 source of truth）
    ├── core-tools/    26 + PROVENANCE.md
    ├── claude-tools/  9
    ├── sdd-tools/     41
    ├── plugin-tools/  20
    ├── tdd-tools/     21
    ├── dev-tools/     25
    └── extensions/vscode/  20（7 个 JSON Schema，896 行）
```

判别口径（一眼可验）：**根下直接有 `SKILL.md` = 独立 skill；根下是 `agents/` + `hooks/` + `skills/` 三件套 = 插件包。**

换句话说：**插件包不是 skill，是 skill 的容器**，不能当 skill 安装。形态差异**不靠目录名承担**（曾试过给容器加 `plugin-` 前缀，已撤回——那会改动插件身份）。

---

## 三、A 类 · 独立 skill（2 个）

| skill | 文件 | 目录 | 上游 | 包指纹（32 位） |
|---|---|---|---|---|
| `codebase-reading` | 4 | [`skills/codebase-reading/`](skills/codebase-reading/) | **未定位** | `16c4ee8894c8bb63b88f6a521a0e2055` |
| `deep-read` | 2 | [`skills/deep-read/`](skills/deep-read/) | **未定位** | `254ab34c9bb19a554870073eba9b10f0` |

**上游未定位（已确认为否定结论）**：2026-09-19 在上游 `agent-alchemy` 全仓（含 `agent-tools/`、`ported/` 目录）按目录名与全文检索 `codebase-reading` / `deep-read`，**均无命中** —— 二者不属于该市场。

**注意：这两份是从安装位回收的副本，不是上游原样。** 两者 `description` 都追加了中文触发词；`codebase-reading` 另有一个 `metadata.short-description` 字段。二者 frontmatter **都没有 `version`**，所以**无法靠版本号判断新旧，只能靠内容指纹比对**。

> 已知副作用：若安装 `claude-code-schemas` 扩展，该扩展按 Claude schema 校验，`codebase-reading/SKILL.md` 的 `metadata` 字段会被报错（schema 为 `additionalProperties: false`）。`external-skills/skills/` 路径含 `skills` 段，**会**被纳入校验范围。

---

## 四、B 类 · 市场镜像（6 插件 ＋ 1 扩展 ＋ 注册表）

市场共 **9 个插件**，本镜像归档 **6 个**；未归档的 3 个见第五节。

| 包 | 文件 | md 行 | 包指纹（32 位） |
|---|---|---|---|
| [`core-tools/`](agent-alchemy-marketplace/core-tools/) | 26 | 5,774 | `808192241ec2c53ced9bd83227279279` |
| [`claude-tools/`](agent-alchemy-marketplace/claude-tools/) | 9 | 3,033 | `37c98b0026d9d87e376684c7a4bd147b` |
| [`sdd-tools/`](agent-alchemy-marketplace/sdd-tools/) | 41 | 12,716 | `d05f987a0964c02cd90b512a7234fba2` |
| [`plugin-tools/`](agent-alchemy-marketplace/plugin-tools/) | 20 | 11,770 | `237382f5562b8482eb55bdd188ebdad9` |
| [`tdd-tools/`](agent-alchemy-marketplace/tdd-tools/) | 21 | 8,961 | `fcfafcbfd6d2b114663a85675b0648a6` |
| [`dev-tools/`](agent-alchemy-marketplace/dev-tools/) | 25 | 5,699 | `a9c9403919c7a3154afc000922a2f00b` |
| [`extensions/vscode/`](agent-alchemy-marketplace/extensions/vscode/) | 20 | 42 (＋896 行 JSON) | `270378ae664cf8ccf47992f73a956972` |
| [`.claude-plugin/`](agent-alchemy-marketplace/.claude-plugin/) | 1 | — | `bc0236b5d4cbd3baedcda888549e1419` |

**指纹算法（必须逐字照抄，见第六节说明）：**

```bash
cd <包目录> && find . -type f ! -name PROVENANCE.md | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32
```

> `LC_ALL=C` 不是装饰：`sort` 默认按 locale 排序，**换个环境排序结果就不同、指纹随之改变**。历史记录里的值（`f7e9c36c…`、`435ccfc9…`、`610ebe47…` 等）都是 locale 相关口径，**已整体作废**；另有 `efe0cbba…` 属自引用失效，成因见第六节。**本表为唯一有效值。**

上游市场总览、作者背景、各插件逐个详解、跟踪方法见 [该目录的 README](agent-alchemy-marketplace/README.md)。

### 依赖关系（实检结论）

```
sdd-tools ──(read)──> claude-tools        27 处引用，已闭合 ✓
dev-tools ──(read)──> core-tools           4 处引用，已闭合 ✓
plugin-tools ─(read)─> .claude-plugin/marketplace.json   5 处引用，已闭合 ✓
plugin-tools ─(read)─> 其他各包（移植时按需读取）
core-tools ──(read)──> 无包外依赖（唯一外引 Context7 MCP，不在分析链上）
```

---

## 五、市场内**未归档**的 3 个插件

| 插件 | 版本 | 文件/行数 | 未归档理由 |
|---|---|---|---|
| `opencode-tools` | 0.1.3 | 18 / 3,660 | 跨平台移植**范例**（含 Claude↔OpenCode 差异表）。非任何已归档包的依赖，需要时再取 |
| `cs-tools` | 0.1.0 | 11 / 3,471 | 竞赛编程 / LeetCode，与本仓无关 |
| `git-tools` | 0.1.0 | 2 / 159 | Conventional Commits，几乎是空壳 |

> 补齐方式见第七节 A 命令，取 `claude/<插件名>/` 即可。

---

## 六、已知本地偏差（改造前必读，共 3 条）

镜像**内容**全部原样，只有以下 3 处**结构性/元数据**差异，且都可解释：

| # | 位置 | 偏差 | 说明 |
|---|---|---|---|
| 1 | `core-tools/PROVENANCE.md` | **上游无此文件**，本地新增 | 下载流程生成的溯源记录（含逐文件 md5）。因此对 `core-tools/` 做 `diff -rq` 会**稳定地多出这 1 行差异**，属预期，不是污染 |
| 2 | `.claude-plugin/` | **放置层级与上游差一层** | 上游真实路径是 `<repo>/.claude-plugin/marketplace.json`；本镜像拍平了上游的 `claude/` 这一层，故落在 `agent-alchemy-marketplace/.claude-plugin/`。`plugin-tools` 里 `${CLAUDE_PLUGIN_ROOT}/../../.claude-plugin/` 的引用深度因此**少一级**，按"镜像根"理解即可 |
| 3 | `skills/codebase-reading`、`skills/deep-read` | **非上游原样** | 从安装位回收，`description` 已追加本地中文触发词；上游未定位，无原件可比 |

### 指纹算法的两个坑（都曾导致记录出错）

**坑 1 · `sort` 的 locale** —— 这是最隐蔽的一个。`find | sort | xargs md5sum` 把排序后的文件名一起喂给 md5，**排序一变，整包指纹就变**。实测同一目录同一时刻：

```
sdd-tools  默认 sort       4bed8765adc06acdd5cef27e62f7925c
sdd-tools  LC_ALL=C sort   d05f987a0964c02cd90b512a7234fba2   ← 唯一有效口径
```

历史记录里的 `f7e9c36c…`／`435ccfc9…`／`610ebe47…`／`86ead9e4…`／`33c8b817…` 全是在别的环境（记录里留着 `X:/myskill/...` 的 Windows 路径）算的，**在本机不可复现，已整体作废**。今后一律 `LC_ALL=C sort`。

**坑 2 · 自引用的 `PROVENANCE.md`** —— 该文件把"自己的 md5"写在文件内部，写进去那一刻就已失效，算出来的值**永远无法复现**（历史值 `efe0cbbaa5bb79a4dc402ac130769442` 即由此而来）。故整包指纹一律 `! -name PROVENANCE.md`。

**统一口径（唯一有效）**：整包 = `find . -type f ! -name PROVENANCE.md | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32`；需要逐文件粒度时用 `md5sum -c`。本文件全部记录值已按此口径重算。

---

## 七、怎么检查是否更新

```bash
# A. 最权威：重下上游并全量比对（差异只应出现在 PROVENANCE.md）
cd /tmp && curl -sSL -o aa.zip https://codeload.github.com/sequenzia/agent-alchemy/zip/refs/heads/main
python3 -c "import zipfile;zipfile.ZipFile('aa.zip').extractall('aa')"
U=/tmp/aa/agent-alchemy-main
for p in core-tools claude-tools sdd-tools plugin-tools tdd-tools dev-tools; do
  echo "== $p"; diff -rq --exclude=PROVENANCE.md "$U/claude/$p" \
    /home/zhq/mydisk/myskill/external-skills/agent-alchemy-marketplace/$p
done
diff -rq "$U/extensions/vscode" /home/zhq/mydisk/myskill/external-skills/agent-alchemy-marketplace/extensions/vscode
diff -rq "$U/.claude-plugin" /home/zhq/mydisk/myskill/external-skills/agent-alchemy-marketplace/.claude-plugin

# B. 只看上游有没有动过（最省事）
curl -sS https://api.github.com/repos/sequenzia/agent-alchemy/commits/main | python3 -c "import sys,json;print(json.load(sys.stdin)['sha'])"
# 与本文件第一节「基准 commit」比对，不同即上游已更新

# C. 只看本地基线有没有被误改（指纹）
cd /home/zhq/mydisk/myskill/external-skills
for p in skills/codebase-reading skills/deep-read \
         agent-alchemy-marketplace/core-tools agent-alchemy-marketplace/claude-tools \
         agent-alchemy-marketplace/sdd-tools agent-alchemy-marketplace/plugin-tools \
         agent-alchemy-marketplace/tdd-tools agent-alchemy-marketplace/dev-tools \
         agent-alchemy-marketplace/extensions agent-alchemy-marketplace/.claude-plugin; do
  printf '%-52s ' "$p"
  (cd "$p" && find . -type f ! -name PROVENANCE.md | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32)
done
# 与第三、四节表中指纹逐位比对
```

**更新后的动作**：① 覆盖对应包目录；② 更新本文件**基准坐标、指纹表、归档日期**；③ 在第八节「更新记录」加一行。

---

## 八、更新记录

| 日期 | 对象 | 从 → 到 | 依据 |
|---|---|---|---|
| 2026-09-19 | A 类（原 3 个） | 首次备份 | 与安装位 `diff -rq` 一致 |
| 2026-09-19 | B 类 `agent-alchemy-core-tools` | 首次收录（26 文件） | 上游 `claude/core-tools/` 原样下载 |
| 2026-09-19 | 结构归并 | 独立归档 `agent-alchemy-core-tools/` → 并入 `agent-alchemy-marketplace/core-tools/` | 二者内容相同，双份无意义 |
| 2026-09-19 | 删除 `skills/codebase-analysis/` | 有 → 无 | 它只是插件内的一个 skill，原件已在 core-tools 内，重复归档；**已确认后续不使用**，故不留存安装位适配改法 |
| 2026-09-19 | 删除 `CATALOG.md` | 有 → 无 | 索引职责并入本文件，避免两处口径漂移 |
| 2026-09-19 | **补齐 `claude-tools`** | 未收录 → 9 文件 | `sdd-tools` 有 27 处跨插件引用指向它，原为**断链** |
| 2026-09-19 | **补齐 `.claude-plugin/marketplace.json`** | 未收录 → 1 文件 | `plugin-tools` 5 处引用（版本号 source of truth） |
| 2026-09-19 | **全量基准复核** | 记录制 → 实测制 | 重下上游 `diff -rq` 零差异；`md5sum -c` 26/26；上游 HEAD 未变 |
| 2026-09-19 | **指纹口径统一（locale）** | 环境相关 `sort` → **`LC_ALL=C sort`** | 同一目录实测两种排序得出不同指纹，旧值不可复现，全部作废 |
| 2026-09-19 | **指纹口径统一（自引用）** | 含 `PROVENANCE.md` → 一律排除 | 废弃 `efe0cbba…`，全部按新口径重算 |
| 2026-09-19 | 本文档重写 | 与目录实际严重不符 → 对齐现状 | 原版引用已删除的 `CATALOG.md`、`agent-alchemy-core-tools/`、`skills/codebase-analysis/` |

---

## 九、与自建 skill 的边界（安装时注意抢触发）

本仓自建的 `repo-wiki-authoring`（宏观地图）与 `source-code-reading-skill` 系列，和 A 类两个 skill **能力域相邻**，同时挂载时模型可能挑错 skill：

- 本仓自建 skill 的目录是**单数 `skill/`**（如 `repo-wiki-authoring/skill/SKILL.md`），A 类是**复数 `skills/`** —— 这一字之差决定了 `claude-code-schemas` 扩展**只校验 A 类、不校验自建 skill**。
- `codebase-reading` 产出「一个代码库 → 一套五件套」（README / code-reading / architecture / api-flow / key-modules）—— 与「一个机制 = 一篇」的笔记库结构不兼容。

> `core-tools` 内的 `codebase-analysis` **仅作为依赖闭包的一部分归档，已确认不使用**，不参与抢触发权衡。
