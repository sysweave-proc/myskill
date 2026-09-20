# 改造对照说明（Claude Code → CodeBuddy）：dev-tools

> 上游基线：[`agent-alchemy-dev-tools` v0.3.4](../../../external-skills/agent-alchemy-marketplace/dev-tools/)（commit `fc1a336b`，MIT，Stephen Sequenzia）
> 本文件记录**每一处改写**及其理由，便于日后上游更新时增量同步。
> 通用映射的理由与证据链（CodeBuddy 原语实测）见 [`core-tools-codebuddy/docs/CONVERSION.md`](../../core-tools-codebuddy/docs/CONVERSION.md) 第一、二节，本文件不重复举证。

---

## 一、总体结论

`dev-tools` 比 `core-tools` 简单一档：**没有 hook（除建链脚本）、没有会话目录约定、没有配置读盘**，
改动几乎全部落在路径变量与 frontmatter 层。**流程正文一字未删**。

| 改造幅度 | 数量 |
|---|---|
| 逐字节一致 | **9** |
| 已改写 | **14** |
| 本产物新增 | **6** |
| 未移植 | **2**（`hooks/hooks.json`、`hooks/resolve-cross-plugins.sh`） |

---

## 二、通用映射（与 core-tools 一致）

| 类别 | Claude Code（上游） | CodeBuddy（本产物） |
|---|---|---|
| 插件清单 | `.claude-plugin/plugin.json` | `.codebuddy-plugin/plugin.json` |
| 插件根变量 | `${CLAUDE_PLUGIN_ROOT}` | `${CODEBUDDY_PLUGIN_ROOT}` |
| 项目规则文件 | `CLAUDE.md` | `CODEBUDDY.md` |
| 目录约定 | `.claude/…` | `.codebuddy/…` |
| 斜杠入口 | skill 的 `user-invocable: true` | `commands/*.md` |
| 插件内 agent 引用 | `agent-alchemy-core-tools:code-architect` | 裸名 `code-architect` |

`dev-tools` 特有的两处：

| 类别 | 上游写法 | 本产物写法 | 理由 |
|---|---|---|---|
| **跨插件文件路径** | `${CLAUDE_PLUGIN_ROOT}/../core-tools/skills/…` | `${CODEBUDDY_PLUGIN_ROOT}/../agent-alchemy-core-tools/skills/…` | CodeBuddy 本地市场是 `plugins/<插件全名>/` **平铺**结构，兄弟目录名即插件全名（带 `agent-alchemy-` 前缀）；上游那种短名要靠 SessionStart hook 建符号链接 |
| **`resolve-cross-plugins.sh`** | 每次会话启动，在插件缓存里为同级插件建短名软链 | **不移植** | 该脚本读 `~/.claude/plugins/installed_plugins.json` 并假定 `<org>/<plugin>/<version>` 的缓存布局；平铺市场下不需要，保留反而是死代码 |

---

## 三、9 个 skill 的逐项改动

统一处理（9 个 skill 全部）：

1. **frontmatter 重建**：只保留 `name` / `description` / `version` / `allowed-tools`
   - 删除 `user-invocable`（CodeBuddy skill frontmatter 无此字段，入口由 `commands/` 承担）
   - 删除 `disable-model-invocation`（同上）
   - 删除 `argument-hint`（改由 command 承载）
   - 删除 `model: haiku`（`release` 技能原有；CodeBuddy skill 层不支持模型声明，语义交由 command/agent 承载）
   - 新增 `version: 0.3.4`（上游来源版本，仅作溯源）
2. **description 增补中文触发词** —— 上游 description 只有英文（`Use when asked "fix this bug"…`），
   中文语境下几乎不会被命中；本产物在末尾追加一行 `中文触发（用户这样说时使用）：…`，与英文触发词并列。
   > 这条是**本改造体系的约定**（非上游内容），core-tools 首版只在 3 个命令型 skill 上做了，本版扩到全部 9 个 skill。
3. **`CLAUDE.md` → `CODEBUDDY.md`**（`project-learnings` 的写入目标，共 8 处）
4. **跨插件路径改写**（`feature-dev` / `docs-manager`）

| skill | 额外处理 |
|---|---|
| `feature-dev` | 4 处路径改写（`deep-analysis` ×1、`language-patterns` ×1、`technical-diagrams` ×1）+ agent 引用去前缀（`code-architect` ×3 处） |
| `bug-killer` | agent 引用去前缀（`code-explorer` ×2）；`project-learnings` 加载路径随变量改名 |
| `docs-manager` | `deep-analysis` 跨插件路径 ×1；3 处 `references/` 加载路径随变量改名 |
| `document-changes` | 仅 frontmatter |
| `release-python-package` | 仅 frontmatter（含删除 `model: haiku`）；`changelog-manager` 为裸名引用，无需改 |
| `architecture-patterns` / `code-quality` / `changelog-format` | **纯知识文件，正文逐字未改**，仅 frontmatter |
| `project-learnings` | `CLAUDE.md` → `CODEBUDDY.md`（8 处）+ 「project-level `.claude/` 目录」→ `.codebuddy/` |

---

## 四、4 个 agent 的改动

统一处理：

1. frontmatter 规范化
   - `description` 改写为「**Use this agent when …** + **Examples:**」形态（CodeBuddy agent 触发规范），
     末尾同样追加**中文触发**一行
   - 新增 `color`（CodeBuddy agent 规范里的视觉标识）：`bug-investigator`=orange、`changelog-manager`=green、
     `code-reviewer`=red、`docs-writer`=blue
   - `tools` 由 YAML 数组改为**逗号串**（与生态内其它 agent 写法一致）
   - `model` 原样保留（`sonnet` / `opus`）
2. `skills:` 预加载字段删除 → 改为正文顶部「**Required knowledge loading**」段，用 `Read` 加载同一份 skill 文件，**能力等价**

| Agent | 额外处理 |
|---|---|
| `docs-writer` | 原 `skills: [technical-diagrams]` → 正文改为读 `${CODEBUDDY_PLUGIN_ROOT}/../agent-alchemy-core-tools/skills/technical-diagrams/SKILL.md`，并给出 Glob 兜底 |
| 其余 3 个 | 仅上述统一处理（正文逐字未改） |

---

## 五、hooks：有意不移植

上游 `hooks/hooks.json` 只有一个 `SessionStart` 钩子，调 `resolve-cross-plugins.sh`。
该脚本的作用：在插件缓存目录里为同级插件创建**短名软链**，让 `${CLAUDE_PLUGIN_ROOT}/../core-tools/…` 这类写法能解析。

CodeBuddy 走的是「本地市场目录 + `plugins/<插件全名>/` 平铺」布局，本产物直接把引用写成
`../agent-alchemy-core-tools/…`，**无需建链**。因此：

- 删除 `hooks/hooks.json`、`hooks/resolve-cross-plugins.sh`
- 插件**不含任何 hook** —— 也就没有"依赖 `jq`"这类运行时前提
- 若日后发现运行时会把插件复制到带版本号的缓存目录（`../` 不再指向市场 `plugins/`），
  再按 core-tools 的办法补一个等价建链脚本（届时进 `v0.3.4-cb.2`）

---

## 六、新增的 5 个 command

上游把 5 个 skill 标为 `user-invocable: true`；CodeBuddy 的对应能力由 `commands/` 提供：

| Command | 对应 skill | 封装要点 |
|---|---|---|
| `/feature-dev` | `feature-dev` | `$ARGUMENTS` = 功能描述；提示 Phase 4/6 的跨插件 agent；要求跑完 7 阶段 |
| `/bug-killer` | `bug-killer` | 解析 `--deep`；强调"先取证再改码"；提示 Phase 5 会派 `project-learnings` |
| `/docs-manager` | `docs-manager` | 参数为空/歧义时走 Phase 1 交互发现，不许猜；给出跨插件 `deep-analysis` 的兜底路径 |
| `/document-changes` | `document-changes` | 无 git 仓库 / 无改动时**提前停止**，不许编造报告 |
| `/release-python-package` | `release-python-package`（skill `name: release`） | 命令名沿用上游 README 的 `/release-python-package`；强调 fail-fast，不许跳过闸门 |

---

## 七、上游更新时的同步清单

```bash
# 1. 重新下载上游，比对 dev-tools
cd "$HOME" && curl -sSL -o aa.zip "https://codeload.github.com/sequenzia/agent-alchemy/zip/refs/heads/main"
python -c "import zipfile; zipfile.ZipFile('aa.zip').extractall('aa_new')"
diff -rq aa_new/agent-alchemy-main/claude/dev-tools \
        /home/zhq/mydisk/myskill/external-skills/agent-alchemy-marketplace/dev-tools

# 2. 若上游有变更：更新镜像 → 按第二节映射表逐类重放改动 → 新版本目录 <新上游版本>-cb.1
#    重放要点：路径变量 / .claude//CLAUDE.md / 跨插件路径加前缀 / agent 去前缀 /
#              skill+agent frontmatter 重建并补中文触发 / 重建 5 个 command

# 3. 复核：本产物应始终保持 0 处以下残留
grep -rn 'CLAUDE_PLUGIN_ROOT\|\.claude/\|CLAUDE\.md\|agent-alchemy-[a-z-]*:' \
  /home/zhq/mydisk/myskill/plugins/dev-tools-codebuddy/versions/*/plugin

# 4. 校准 + 安装
bash /home/zhq/mydisk/myskill/plugins/dev-tools-codebuddy/versions/v0.3.4-cb.1/verify.sh
```
