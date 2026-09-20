# 改造对照说明（Claude Code → CodeBuddy）：tdd-tools

> 上游基线：[`agent-alchemy-tdd-tools` v0.2.1](../../../external-skills/agent-alchemy-marketplace/tdd-tools/)（commit `fc1a336b`，MIT，Stephen Sequenzia）
> 本文件记录**每一处改写**及其理由，便于日后上游更新时增量同步。
> 通用映射的理由与证据链（CodeBuddy 原语实测、`subagent_type` 裸名、hook 输出格式）见
> [`core-tools-codebuddy/docs/CONVERSION.md`](../../core-tools-codebuddy/docs/CONVERSION.md) 第一、二节，本文件不重复举证。

---

## 一、总体结论

`tdd-tools` 是"有流程 + 有 hook + 有跨插件依赖"的一档，比 dev-tools 复杂、比 sdd-tools 简单。
**RED-GREEN-REFACTOR 六阶段、测试评分表（`test-rubric.md`）、波次并行、失败重试、断点续跑全链路保留**。

| 改造幅度 | 数量 |
|---|---|
| 逐字节一致 | **4** |
| 已改写 | **16** |
| 本产物新增 | **6** |
| 未移植 | **1**（`hooks/resolve-cross-plugins.sh`） |

---

## 二、通用映射（与 core-tools 一致）

| 类别 | Claude Code（上游） | CodeBuddy（本产物） |
|---|---|---|
| 插件清单 | `.claude-plugin/plugin.json` | `.codebuddy-plugin/plugin.json` |
| 插件根变量 | `${CLAUDE_PLUGIN_ROOT}` | `${CODEBUDDY_PLUGIN_ROOT}` |
| 项目规则文件 | `CLAUDE.md` | `CODEBUDDY.md` |
| 目录约定 | `.claude/…` | `.codebuddy/…` |
| 斜杠入口 | skill 的 `user-invocable: true` | `commands/*.md` |
| 插件内 agent 引用 | `agent-alchemy-tdd:tdd-executor` | 裸名 `tdd-executor` |

## 三、本插件特有的三类改写

### 1. 跨插件路径加组织前缀

| 上游 | 本产物 |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/../core-tools/skills/language-patterns/SKILL.md` | `${CODEBUDDY_PLUGIN_ROOT}/../agent-alchemy-core-tools/skills/language-patterns/SKILL.md` |
| `${CLAUDE_PLUGIN_ROOT}/../core-tools/skills/project-conventions/SKILL.md` | `${CODEBUDDY_PLUGIN_ROOT}/../agent-alchemy-core-tools/skills/project-conventions/SKILL.md` |
| `${CLAUDE_PLUGIN_ROOT}/../sdd-tools/skills/execute-tasks/scripts/poll-for-results.sh` | `${CODEBUDDY_PLUGIN_ROOT}/../agent-alchemy-sdd-tools/skills/execute-tasks/scripts/poll-for-results.sh` |

理由：CodeBuddy 本地市场是 `plugins/<插件全名>/` **平铺**结构，兄弟目录名即带组织前缀的插件全名；
上游那种短名要靠 SessionStart hook 建软链（下一步就是它）。

### 2. 环境变量：`CLAUDE_CODE_TASK_LIST_ID` → `TASK_LIST_ID`

上游用 `~/.claude/tasks/{CLAUDE_CODE_TASK_LIST_ID}/execution_pointer.md` 记录"当前任务列表的落盘目录"。
该变量由 Claude Code 运行时注入；CodeBuddy 未确认有同名变量，故：

- 变量名改为 `TASK_LIST_ID`（与文件内另一处 `{TASK_LIST_ID}` 写法统一）
- 在 `skills/execute-tdd-tasks/SKILL.md` 首次出现处补一句：
  「`{TASK_LIST_ID}` = 当前任务列表的标识（`TaskList` 可见）；若当前运行时不暴露该标识，
  用任务列表名或 `default` 作为目录名，并保持全程一致」
- 目录本身 `.claude/tasks/` → `.codebuddy/tasks/`（该目录由插件自己的技能创建，非运行时内置）

> 被替换的只有 1 处（`execute-tdd-tasks/SKILL.md`）+ 1 处参考文件。属于**降级但可用**的改写，
> 不是能力删除：中断续跑仍靠 `execution_pointer.md`，只是标识来源不再依赖特定环境变量。

### 3. hooks：保留自动放行，删除建链

| 文件 | 处理 |
|---|---|
| `hooks/auto-approve-session.sh` | **保留**。`.claude/sessions/` → `.codebuddy/sessions/`（9 处）、
`$HOME/.claude/tasks/` → `$HOME/.codebuddy/tasks/`（1 处）；注释里的 "Claude Code" → "CodeBuddy"；
审批输出 JSON 与退出码语义**完全不变** |
| `hooks/hooks.json` | `PreToolUse` 条目保留（`${CODEBUDDY_PLUGIN_ROOT}` 替换）；
**`SessionStart` 条目删除**（它只用来调建链脚本） |
| `hooks/resolve-cross-plugins.sh` | **不移植** —— 读 `~/.claude/plugins/installed_plugins.json`，
并假定 `<org>/<plugin>/<version>` 的插件缓存布局；CodeBuddy 平铺市场下是死代码 |

---

## 四、5 个 skill 的逐项改动

统一处理：

1. **frontmatter 重建**：只保留 `name` / `description` / `version` / `allowed-tools`
   - 删除 `user-invocable`、`disable-model-invocation`、`argument-hint`、`arguments:` 块
     （`execute-tdd-tasks` 的 3 个 `arguments:` 定义改由 command 的 `argument-hint` + 正文承载）
   - `allowed-tools` 原样保留（`execute-tdd-tasks` 的 YAML 数组压成逗号串，写法对齐生态内其它 skill）
   - 补 `version: 0.2.1`
2. **description 增补中文触发词**（5 个 skill 全部；上游只有英文触发词）
3. **路径与命名替换**：`${CODEBUDDY_PLUGIN_ROOT}`、`.codebuddy/`、跨插件前缀、裸名 agent/命令引用
   （`/agent-alchemy-sdd:create-tasks` → `/create-tasks`；`agent-alchemy-tdd:execute-tdd-tasks` → `/execute-tdd-tasks`）

| skill | 额外处理 |
|---|---|
| `execute-tdd-tasks` | `TASK_LIST_ID` 说明补入（见三.2）；`.codebuddy/tasks/`、`.codebuddy/sessions/` 全量替换 |
| `analyze-coverage` | `references/coverage-patterns.md` 内亦有 `.claude/` 路径（已改写，故该参考文件不再是"逐字节一致"） |
| `generate-tests` | 2 处 core-tools 跨插件路径；`references/framework-templates.md` 有路径改写 |
| `tdd-cycle` | 2 处 core-tools 跨插件路径；`references/tdd-workflow.md`、`references/test-rubric.md` 有路径改写 |
| `create-tdd-tasks` | 命令引用去插件前缀（`/create-tasks`、`/execute-tdd-tasks`）；2 份参考文件**逐字节未改** |

---

## 五、3 个 agent 的改动

统一处理：

1. `description` 改写为「**Use this agent when …** + **Examples:**」形态，末尾追加**中文触发**一行
2. 新增 `color`：`tdd-executor`=purple、`test-reviewer`=red、`test-writer`=green
3. `tools` 由 YAML 数组改为**逗号串**；`model` 原样保留（`opus` / `sonnet`）
4. `skills:` 预加载字段删除 → 正文顶部「**Required knowledge loading**」段，用 `Read` 加载同样的
   `${CODEBUDDY_PLUGIN_ROOT}/../agent-alchemy-core-tools/skills/{language-patterns,project-conventions}/SKILL.md`，
   并给出 Glob 兜底 —— **能力等价**

| Agent | `skills:` 原值 | 本产物加载 |
|---|---|---|
| `tdd-executor` | `language-patterns`、`project-conventions` | 同上两份（正文段） |
| `test-writer` | `language-patterns`、`project-conventions` | 同上两份（正文段） |
| `test-reviewer` | 无 | 无（仅统一处理） |

---

## 六、新增的 5 个 command

上游 5 个 skill **全部**标为 `user-invocable: true`，故对应新增 5 个 command：

| Command | 参数 | 封装要点 |
|---|---|---|
| `/tdd-cycle` | `<feature-description｜task-id｜spec-section>` | 强调"先给计划确认，再自主跑"；RED 必须是正确原因失败 |
| `/generate-tests` | `<spec-path｜task-id｜file-path>` | 说明模式自动判定 + 框架自动识别 + `test-writer` 并行 |
| `/create-tdd-tasks` | `[--task-group <group>]` | 前置依赖 `/create-tasks`；输出契约（每个实现任务前必须配对测试任务） |
| `/execute-tdd-tasks` | `[--task-group] [--max-parallel] [--retries]` | 三个 flag 语义 + TDD/非 TDD 分流 + 可续跑 |
| `/analyze-coverage` | `[<project-path>] [--spec] [--threshold]` | 参数语义 + 输出必须是"补测建议"而非纯百分比 |

---

## 七、上游更新时的同步清单

```bash
# 1. 重新下载上游，比对 tdd-tools
cd "$HOME" && curl -sSL -o aa.zip "https://codeload.github.com/sequenzia/agent-alchemy/zip/refs/heads/main"
python -c "import zipfile; zipfile.ZipFile('aa.zip').extractall('aa_new')"
diff -rq aa_new/agent-alchemy-main/claude/tdd-tools \
        /home/zhq/mydisk/myskill/external-skills/agent-alchemy-marketplace/tdd-tools

# 2. 若上游有变更：更新镜像 → 按本文第二/三节逐类重放 → 新版本目录 <新上游版本>-cb.1
#    重放要点：路径变量 / .claude//CLAUDE.md / 跨插件路径加前缀 /
#              TASK_LIST_ID 改名与说明 / frontmatter 重建并补中文触发 / 重建 5 个 command /
#              hooks.json 删 SessionStart

# 3. 复核：本产物应始终保持 0 处以下残留
grep -rn 'CLAUDE_PLUGIN_ROOT\|\.claude/\|CLAUDE\.md\|agent-alchemy-[a-z-]*:\|CLAUDE_CODE' \
  /home/zhq/mydisk/myskill/plugins/tdd-tools-codebuddy/versions/*/plugin

# 4. 校准 + 安装
bash /home/zhq/mydisk/myskill/plugins/tdd-tools-codebuddy/versions/v0.2.1-cb.1/verify.sh
bash /home/zhq/mydisk/myskill/plugins/tdd-tools-codebuddy/install.sh
```
