# 改造对照说明（Claude Code → CodeBuddy）：sdd-tools

> 上游基线：[`agent-alchemy-sdd-tools` v0.2.11](../../../external-skills/agent-alchemy-marketplace/sdd-tools/)（commit `fc1a336b`，MIT，Stephen Sequenzia）
> 本文件记录**每一处改写**及其理由，便于日后上游更新时增量同步。
> 通用映射的理由与证据链（CodeBuddy 原语实测、`subagent_type` 裸名、hook 输出格式）见
> [`core-tools-codebuddy/docs/CONVERSION.md`](../../core-tools-codebuddy/docs/CONVERSION.md) 第一、二节，本文件不重复举证。

---

## 一、总体结论

`sdd-tools` 是本系列里**最大的一个插件**（41 上游文件，12,716 行），也是最"重"的一个：
5 skill / 7 agent / 3 hook 事件 / 5 份 references / 1 份 HTML 模板 / 1 个轮询脚本。

关键判定：上游 `run-tasks` 的整个执行引擎建立在这两条假设上 ——

1. 运行时提供 **Agent Teams 原语**（`TeamCreate` / `Task(name:, team_name:)` / `SendMessage` / `TeamDelete`）；
2. 运行时提供 **Task 原语**（`TaskCreate` / `TaskGet` / `TaskList` / `TaskUpdate` / `TaskOutput` / `TaskStop`）。

这两条在 CodeBuddy 中**都成立**（证据见 core-tools 的 CONVERSION 第一节）。因此本产物
**没有把"团队执行"降级为"串行 task 调用"** —— 三层架构（Orchestrator → Wave Lead → Context Manager/Executors）、
拓扑分波、并行度封顶、三级重试、中断恢复全部按原样落地。

| 改造幅度 | 数量 |
|---|---|
| 逐字节一致 | **16** |
| 已改写 | **24** |
| 本产物新增 | **6** |
| 未移植 | **1**（`hooks/resolve-cross-plugins.sh`） |

---

## 二、通用映射（与 core-tools 一致）

| 类别 | Claude Code（上游） | CodeBuddy（本产物） |
|---|---|---|
| 插件清单 | `.claude-plugin/plugin.json` | `.codebuddy-plugin/plugin.json` |
| 插件根变量 | `${CLAUDE_PLUGIN_ROOT}` | `${CODEBUDDY_PLUGIN_ROOT}` |
| 项目规则文件 | `CLAUDE.md` | `CODEBUDDY.md` |
| 目录约定 | `.claude/…` | `.codebuddy/…`（含 `~/.claude/tasks/`、`.claude/teams/`） |
| 斜杠入口 | skill 的 `user-invocable: true` | `commands/*.md` |
| agent / 命令引用 | `agent-alchemy-sdd:run-tasks` | 裸名 `run-tasks` |

---

## 三、三类本插件特有的改写

### 1. 跨插件依赖：`claude-tools` 是硬依赖（26 处）

上游把"任务/团队原语"的说明放在**兄弟插件** `claude-tools` 里，`sdd-tools` 通过
`${CLAUDE_PLUGIN_ROOT}/../claude-tools/...` 读取，共 **26 处**（另 1 处读 `../core-tools`）。

| 上游 | 本产物 |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/../claude-tools/skills/claude-code-tasks/SKILL.md` | `${CODEBUDDY_PLUGIN_ROOT}/../agent-alchemy-claude-tools/skills/claude-code-tasks/SKILL.md` |
| `${CLAUDE_PLUGIN_ROOT}/../claude-tools/skills/claude-code-teams/…` | `${CODEBUDDY_PLUGIN_ROOT}/../agent-alchemy-claude-tools/skills/claude-code-teams/…` |
| `${CLAUDE_PLUGIN_ROOT}/../core-tools/skills/technical-diagrams/SKILL.md` | `${CODEBUDDY_PLUGIN_ROOT}/../agent-alchemy-core-tools/skills/technical-diagrams/SKILL.md` |

理由：CodeBuddy 本地市场是 `plugins/<插件全名>/` **平铺**结构，兄弟目录名即带组织前缀的插件全名；
上游那种短名要靠 SessionStart hook 建软链。**因此 `claude-tools-codebuddy` 必须先装进同一市场**，
否则 `run-tasks` 与 `create-tasks` 的规划/执行链是断的。

### 2. 环境变量：`CLAUDE_CODE_TASK_LIST_ID` → `TASK_LIST_ID`（4 处）

与 `tdd-tools` 同款处理（理由与差别见 [`tdd-tools-codebuddy/docs/CONVERSION.md`](../../tdd-tools-codebuddy/docs/CONVERSION.md) 第二节）：

- 变量改名 → `TASK_LIST_ID`；目录 `.claude/tasks/` → `.codebuddy/tasks/`
- 在两处**首次出现处**（`skills/execute-tasks/SKILL.md` 第 6 项、`skills/execute-tasks/references/orchestration.md` 第 6 步）
  补一句「`{TASK_LIST_ID}` = 当前任务列表的标识（`TaskList` 可见）；运行时不暴露该标识时，
  用任务列表名或常量 `default` 作为目录名，并保持全程一致」

> 属于**降级但可用**的改写，不是能力删除：中断续跑仍靠 `execution_pointer.md`，只是标识来源不再依赖特定环境变量。

### 3. hooks：保留质量闸门，删除建链

| 文件 | 处理 |
|---|---|
| `hooks/auto-approve-session.sh` | **保留**。`.claude/sessions/` → `.codebuddy/sessions/`（9 处）、
`$HOME/.claude/tasks/` → `$HOME/.codebuddy/tasks/`；审批输出 JSON 与退出码语义不变 |
| `hooks/verify-task-completion.sh` | **原文未改（逐字节一致）** —— 它只用 `jq` 读 hook 输入 + 按仓库类型跑测试，
不涉及任何 Claude 专有路径。这就是本插件的**执行质量闸门**：带 `metadata.spec_path` 的任务标记完成时跑测试，失败则 `exit 2` 阻止完成 |
| `hooks/hooks.json` | `PreToolUse` / `TaskCompleted` / `TeammateIdle` **三个事件原样保留**（仅变量替换）；
**删除 `SessionStart`**（它只用来调建链脚本） |
| `hooks/resolve-cross-plugins.sh` | **不移植** —— 读 `~/.claude/plugins/installed_plugins.json` 并假定 Claude 的插件缓存布局；CodeBuddy 平铺市场下是死代码 |

> 注意 `TeammateIdle` 是 **prompt 型 hook**（不是 command 型）：它是一段发给模型的自然语言自检指令
> （"你是不是执行者？TASK RESULT 和 CONTEXT CONTRIBUTION 都发了吗？"）。CodeBuddy 的 hook 体系同样支持
> prompt 型，故原样保留。

---

## 四、5 个 skill 的逐项改动

统一处理：

1. **frontmatter 重建**：只保留 `name` / `description` / `version` / `allowed-tools`
   - 删除 `user-invocable`、`disable-model-invocation`、`argument-hint`、`arguments:` 块
     （`analyze-spec` 1 个 / `create-spec` 1 个 / `create-tasks` 2 个 / `execute-tasks` 4 个参数定义，
     全部改由 command 的 `argument-hint` + 正文承载）
   - `allowed-tools` 数组压成逗号串（`execute-tasks`、`run-tasks` 原本是数组）
   - 补 `version: 0.2.11`
2. **description 增补中文触发词**（5 个 skill 全部；上游只有英文触发词）
3. **路径与命名替换**（见第二节通用映射与第三节）

| skill | 额外处理 |
|---|---|
| `analyze-spec` | 命令引用去前缀（`/run-tasks --task-group spec-fixes-…`）；**4 份 references 与 HTML 模板 `templates/review-template.html` 全部逐字节未改** |
| `create-spec` | 只有 `references/codebase-exploration.md` 因含 `claude-tools` 引用被改写；**其余 4 份 references + 3 份 `templates/*.md` 逐字节未改** |
| `create-tasks` | **3 份 references 全部逐字节未改**；`task_group` 与 `--task-group` 的契约不变 |
| `execute-tasks` | `TASK_LIST_ID` 说明补入；3 份 references（`execution-workflow.md`、`orchestration.md`、`verification-patterns.md`）含 `.claude/` 路径（已改写）；`scripts/poll-for-results.sh` 仅注释里的示例路径被改（轮询逻辑逐字未动） |
| `run-tasks` | 命令引用去前缀；3 份 references（`communication-protocols.md`、`orchestration.md`、`verification-patterns.md`）含 `claude-tools` / `.claude/` 引用（已改写） |

---

## 五、7 个 agent 的改动

统一处理：

1. `description` 改写为「**Use this agent when …** + **Examples:**」形态，末尾追加**中文触发**一行
2. 新增 `color`：`codebase-explorer`=cyan、`context-manager`=yellow、`researcher`=blue、
   `spec-analyzer`=magenta、`task-executor`=green、`task-executor-v2`=orange、`wave-lead`=red
3. `tools` 由 YAML 数组改为**逗号串**；`model` 原样保留（`sonnet` / `opus`）
4. `skills:` 预加载字段删除 → 正文顶部「**Required knowledge loading**」段，用 `Read` 加载同一份 skill

| Agent | 额外处理 |
|---|---|
| `spec-analyzer` | 原 `skills: [analyze-spec]` → 正文读 `${CODEBUDDY_PLUGIN_ROOT}/skills/analyze-spec/SKILL.md`（**同插件**路径） |
| `task-executor` | 原 `skills: [execute-tasks]` → 正文读 `${CODEBUDDY_PLUGIN_ROOT}/skills/execute-tasks/SKILL.md` |
| `researcher` | **保留上游的多行 `\|` description 与 5 个 `<example>` 块**，只在其中追加中文触发行；
`tools` 去掉写死的 `mcp__context7__*`，改为 `WebSearch, WebFetch` + 正文「可选 Context7」段（与 core-tools 的 `interview-researcher` 同款处理） |
| `wave-lead` | **保留上游的长 `\|` description**（它本身就是对职责的完整描述），只追加中文触发行；改 `tools` 数组为逗号串并补 `color` |
| `codebase-explorer` / `context-manager` / `task-executor-v2` | 仅上述统一处理（正文逐字未改） |

---

## 六、新增的 6 个文件（5 command + 1 清单）

上游把 4 个 skill 标为 `user-invocable: true`，故新增 4 个 command；**另补 1 个 `/run-tasks`**：

| Command | 对应 skill | 封装要点 |
|---|---|---|
| `/create-spec` | `create-spec` | 三档深度与扩容预算；`codebase-explorer`/`researcher` **仅在用户明确要求时**启用；必须落盘 |
| `/analyze-spec` | `analyze-spec` | 规格路径必填；md + HTML 双产出；发现先逐条确认再谈建任务 |
| `/create-tasks` | `create-tasks` | 首次分解 vs `task_uid` 合并的差异；`task_group` 是 `--task-group` 过滤的键 |
| `/execute-tasks` | `execute-tasks` | 与 `/run-tasks` 的分工对比（避免用户选错引擎） |
| `/run-tasks` | `run-tasks` | **上游漏标 `user-invocable: true`**，但其 README 命令表与 `analyze-spec` 正文都以 `/run-tasks` 形式引用它 —— 判定为上游疏漏，本产物补上命令入口（记录于此，便于上游修正后比对） |
| `.codebuddy-plugin/plugin.json` | —— | 插件清单 |

---

## 七、上游更新时的同步清单

```bash
# 1. 重新下载上游，比对 sdd-tools
cd "$HOME" && curl -sSL -o aa.zip "https://codeload.github.com/sequenzia/agent-alchemy/zip/refs/heads/main"
python -c "import zipfile; zipfile.ZipFile('aa.zip').extractall('aa_new')"
diff -rq aa_new/agent-alchemy-main/claude/sdd-tools \
        /home/zhq/mydisk/myskill/external-skills/agent-alchemy-marketplace/sdd-tools

# 2. 若上游有变更：更新镜像 → 按本文第二~五节逐类重放 → 新版本目录 <新上游版本>-cb.1
#    重放要点：路径变量 / .claude//CLAUDE.md / claude-tools 与 core-tools 路径加前缀 /
#              TASK_LIST_ID 改名与说明 / frontmatter 重建并补中文触发 /
#              researcher 与 wave-lead 的 description 结构保留 / 重建 5 个 command /
#              hooks.json 删 SessionStart（其余三个事件保留）

# 3. 复核：本产物应始终保持 0 处以下残留
grep -rn 'CLAUDE_PLUGIN_ROOT\|\.claude/\|CLAUDE\.md\|agent-alchemy-[a-z-]*:\|CLAUDE_CODE' \
  /home/zhq/mydisk/myskill/plugins/sdd-tools-codebuddy/versions/*/plugin

# 4. 校准 + 安装（务必先装 claude-tools 到同一市场）
bash /home/zhq/mydisk/myskill/plugins/claude-tools-codebuddy/install.sh
bash /home/zhq/mydisk/myskill/plugins/sdd-tools-codebuddy/versions/v0.2.11-cb.1/verify.sh
bash /home/zhq/mydisk/myskill/plugins/sdd-tools-codebuddy/install.sh
```
