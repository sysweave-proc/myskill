# 改造对照说明（Claude Code → CodeBuddy）：claude-tools

> 上游基线：[`agent-alchemy-claude-tools` v0.2.5](../../../external-skills/agent-alchemy-marketplace/claude-tools/)（commit `fc1a336b`，MIT，Stephen Sequenzia）
> 本文件记录**每一处改写**及其理由，便于日后上游更新时增量同步。
> 通用映射的理由与证据链见 [`core-tools-codebuddy/docs/CONVERSION.md`](../../core-tools-codebuddy/docs/CONVERSION.md) 第一、二节。

---

## 一、总体结论

`claude-tools` 是五个包里**唯一"改变立场但不改内容"**的一个：

- 它描述的是 **Claude Code 的 Task / Agent Teams 原语**，而这些原语在 CodeBuddy 中输入法、参数、生命周期**同名同义**；
- 它又是 `sdd-tools` 的**硬依赖**（27 处引用），必须随 sdd-tools 一起落地；
- 因此改造策略是：**参数表、状态机、消息协议、编排模式一律不动**，只替换路径变量与目录约定，
  再把「指代运行时平台的称谓」改为 CodeBuddy，并在正文开头补一段「移植说明」把边界讲清楚。

| 改造幅度 | 数量 |
|---|---|
| 逐字节一致 | **1**（`.gitkeep`，空文件） |
| 已改写 | **8** |
| 本产物新增 | **1**（`plugin.json`） |
| 未移植 | **0** |

---

## 二、通用映射（与 core-tools 一致）

| 类别 | Claude Code（上游） | CodeBuddy（本产物） |
|---|---|---|
| 插件清单 | `.claude-plugin/plugin.json` | `.codebuddy-plugin/plugin.json` |
| 插件根变量 | `${CLAUDE_PLUGIN_ROOT}` | `${CODEBUDDY_PLUGIN_ROOT}` |
| 项目规则文件 | `CLAUDE.md` | `CODEBUDDY.md` |
| 目录约定 | `.claude/…` | `.codebuddy/…` |

---

## 三、两条**有意不改**的边界

改造里最容易"手滑改错"的就是下面两类，本产物**明确保留上游写法**：

### 1. 平台注入的环境变量名 —— 不改

| 位置 | 变量 |
|---|---|
| `skills/claude-code-teams/SKILL.md`（环境变量表） | `CLAUDE_CODE_TEAM_NAME`、`CLAUDE_CODE_AGENT_NAME`、`CLAUDE_CODE_AGENT_TYPE`、`CLAUDE_CODE_TASK_LIST_ID` |
| 其它出现处 | `CLAUDE_TEAMMATE_ID`、`CLAUDE_TEAM_ID` |

理由：这些**不是文档作者自造的标识符，而是运行时注入的变量**。把它们改成 `CODEBUDDY_*` 会变成
「引用一个并不存在的变量」，比保留原名更危险。处理方式改为**加说明**：两份 SKILL.md 的 H1 之后
各有一段「移植说明」，写明"按上游原样引用，是否需要改名以本机运行时实际提供的环境变量为准"。

> 对照：`tdd-tools` 里的 `CLAUDE_CODE_TASK_LIST_ID` **改了名**（→ `TASK_LIST_ID`），
> 因为那里的用法是"拼一个由插件自己创建/读取的目录路径"，改名的同时补了"标识来源"的兜底说明。
> 两者的差别是**语义差别**，不是口径不一致。

### 2. skill 名 `claude-code-tasks` / `claude-code-teams` —— 不改

理由：上游命名；且 `sdd-tools` 有 27 处路径引用（`.../agent-alchemy-claude-tools/skills/claude-code-tasks/SKILL.md`）。
改名会波及跨插件引用，而收益为零 —— 这两个名字描述的正是"这套原语的谱系"。

---

## 四、逐项改动

### 1. 路径与目录（8 个文件命中）

| 替换 | 命中文件 |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}` → `${CODEBUDDY_PLUGIN_ROOT}`（10 处） | 两份 SKILL.md、`hooks-integration.md` |
| `.claude/` → `.codebuddy/` | `claude-code-teams/SKILL.md`、`orchestration-patterns.md`、`messaging-protocol.md` 等 |
| `CLAUDE.md` → `CODEBUDDY.md` | 同上（若有） |
| 平台称谓 "Claude Code" → "CodeBuddy" | 8 个文件中的散文段落（**工具名与参数表不动**） |

### 2. skill frontmatter 重建

```yaml
# 上游
name: claude-code-tasks
description: Reference for Claude Code's 6 Task Management tools — …
user-invocable: false
disable-model-invocation: false
last-verified: 2026-03-07
```

```yaml
# 本产物
name: claude-code-tasks
description: Reference for CodeBuddy's 6 Task Management tools — … 中文触发（用户这样说时使用）：任务怎么建、任务状态怎么流转、…
version: 0.2.5
```

- 删除 `user-invocable` / `disable-model-invocation`（CodeBuddy skill frontmatter 无此字段；
  且两者本来就为 `false`，无入口需求，故**不新增 command**）
- 删除 `last-verified`（无此字段）→ 日期改记在 `PROVENANCE.md` 第二节
- 补 `version: 0.2.5`
- **description 增补中文触发词**（上游只有英文）—— 这两个 skill 虽然不由用户直接调用，
  但仍可能被模型在相关语境下自动加载，中文触发能提高命中率

### 3. 新增「移植说明」段

两份 SKILL.md 的 H1 之后各插入一段引用块，内容为：

- 本文档描述的是 **原语本身**，工具名/参数/状态生命周期/消息协议在 CodeBuddy 中同名同样存在，故按原样保留；
- 少数**平台注入的环境变量名**按上游原样引用，是否需要改名以本机实际环境为准。

这段话是**本产物新增内容**（不计入上游对照），目的是让读者（模型或人）知道哪些是"保证一致的"、
哪些是"需要现场核实的"。

### 4. 新增文件

| 文件 | 说明 |
|---|---|
| `.codebuddy-plugin/plugin.json` | 插件清单（上游由市场注册表提供，无包内清单） |
| `README.md` | 换成本产物的使用手册（上游 README 是面向 Claude 侧的清单说明） |

---

## 五、上游更新时的同步清单

```bash
# 1. 重新下载上游，比对 claude-tools
cd "$HOME" && curl -sSL -o aa.zip "https://codeload.github.com/sequenzia/agent-alchemy/zip/refs/heads/main"
python -c "import zipfile; zipfile.ZipFile('aa.zip').extractall('aa_new')"
diff -rq aa_new/agent-alchemy-main/claude/claude-tools \
        /home/zhq/mydisk/myskill/external-skills/agent-alchemy-marketplace/claude-tools

# 2. 若上游有变更：更新镜像 → 按第四节逐项重放 → 新版本目录 <新上游版本>-cb.1
#    特别注意：勿把 CLAUDE_CODE_* 环境变量名"顺手"改掉（见第三节第 1 条）

# 3. 复核：本产物应始终保持 0 处以下残留
grep -rn 'CLAUDE_PLUGIN_ROOT\|\.claude/\|CLAUDE\.md' \
  /home/zhq/mydisk/myskill/plugins/claude-tools-codebuddy/versions/*/plugin

# 4. 校准 + 安装
bash /home/zhq/mydisk/myskill/plugins/claude-tools-codebuddy/versions/v0.2.5-cb.1/verify.sh
bash /home/zhq/mydisk/myskill/plugins/claude-tools-codebuddy/install.sh
```
