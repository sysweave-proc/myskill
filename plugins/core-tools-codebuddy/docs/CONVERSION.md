# 改造对照说明（Claude Code → CodeBuddy）

> 上游基线：[`agent-alchemy-core-tools` v0.2.3](../../../external-skills/agent-alchemy-marketplace/core-tools/)（commit `fc1a336b`，MIT，Stephen Sequenzia）
> 本文件记录**每一处改写**及其理由，便于日后上游更新时增量同步。

---

## 一、结论先行：为什么这次能高保真移植

改造前最大的未知是「Coordinator 层能否保留」。实测结论：**能**。

CodeBuddy 生态中以下原语真实存在且语义与 Claude Code 一致：

| 原语 | 证据 |
|---|---|
| `TeamCreate` / `TeamDelete` | `cb_teams_marketplace/plugins/ai-hedge-fund/rules/*.md`（"必须使用 TeamCreate 并行执行"）、`ardot-design-generator/skills/.../slides-agent-teams-workflow.md`（完整建队→派活→关停流程） |
| `TaskCreate` / `TaskUpdate` / `TaskList` / `TaskGet` | `cb_teams_marketplace/plugins/sheetagent/agents/sheet-agent.md` §4.4 |
| `Task(subagent_type:, team_name:)` | 同上两处 + `pr-review-toolkit`、`agent-team-agile-workflow` |
| `SendMessage`（含 `recipient: "main"` 回流、`shutdown_request`） | `codebuddy-plugins-official/plugins/security-scan/agents/bg-scan.md` |
| `AskUserQuestion` | 官方插件 `allowed-tools` 中出现 24 次（如 `hookify/commands/configure.md`） |
| `PreToolUse` hook 的 `hookSpecificOutput.permissionDecision` | `plugin-dev/skills/hook-development/examples/*.sh`、`hookify/core/rule_engine.py` |

因此 `deep-analysis` 的 **6 阶段流程、hub-and-spoke 拓扑、任务依赖、状态守卫、断点续传、缓存 TTL、错误降级矩阵全部原样保留**，没有降级为"串行 task 调用"。

---

## 二、通用映射表

| 类别 | Claude Code（上游） | CodeBuddy（本产物） | 说明 |
|---|---|---|---|
| 插件清单 | `.claude-plugin/plugin.json` | `.codebuddy-plugin/plugin.json` | 目录名不同 |
| 插件根变量 | `${CLAUDE_PLUGIN_ROOT}` | `${CODEBUDDY_PLUGIN_ROOT}` | 官方 doc 明确支持在 commands/agents/skills/hooks 中使用 |
| 会话与配置目录 | `.claude/sessions/…`、`.claude/agent-alchemy.local.md` | `.codebuddy/sessions/…`、`.codebuddy/agent-alchemy.local.md` | 全量替换 |
| 项目规则文件 | `CLAUDE.md` | `CODEBUDDY.md` | CodeBuddy 的规则文件（见官方 `code-reviewer` agent 的措辞）；`AGENTS.md` 保留 |
| 斜杠入口 | skill 的 `user-invocable: true` | `commands/*.md` | CodeBuddy 的 skill frontmatter 无 `user-invocable` 字段 |
| 模型分层 | `model: opus/sonnet` | 不变 | CodeBuddy agent 支持同枚举（`inherit/sonnet/opus/haiku`） |
| MCP 工具名 | `mcp__context7__*` | 不写死，改为"可选 + WebFetch/WebSearch 兜底" | CodeBuddy 的 MCP 命名带插件前缀（`mcp__plugin_<plugin>_<server>__<tool>`），写死会随环境变化失效 |
| Hook 事件与输出 | `PreToolUse` + `permissionDecision` | 不变 | 格式兼容，脚本逻辑零改动 |
| **插件内 agent 引用** | `agent-alchemy-core-tools:code-architect`（Claude 命名空间写法） | **裸名** `code-architect` | 全生态 `subagent_type` 实测取值无一处带插件前缀（`bg-scan`/`python-pro`/`general-purpose`/`fork`…）；官方 `plugin-dev` 文档亦写「Single plugin: `agent-name`」 |
| **团队派活调用** | `Task` + `team_name`（队友名靠约定） | `Task` + `subagent_type` + **`name`** + `team_name`（`max_turns` 可选） | CodeBuddy 生态建队流程显式传 `name`；`name` 是 `SendMessage(recipient: "explorer-N")` 能寻址到队友的前提 |

---

## 三、6 个 skill 的逐项改动

### 1. `deep-analysis`（协调层，**核心**）

**正文流程逻辑全部保留** —— 6 阶段、动态焦点区、分级审批、团队装配、状态守卫指派、监控循环、结构完备性检查、综合、缓存与归档、错误降级矩阵、会话恢复策略表均未删改。

改动共 5 处：
- frontmatter：删除 `argument-hint` / `user-invocable` / `disable-model-invocation`，加 `version`
- `.claude/` → `.codebuddy/`（21 处）
- `CLAUDE.md` → `CODEBUDDY.md`（recon 阶段的文档读取目标）
- **Phase 3 派队友补显式 `name`** —— 上游只传 `team_name`、队友名靠约定；CodeBuddy 生态的建队流程显式传 `name` + `team_name` + `max_turns`，而 `SendMessage(recipient: "explorer-2")` 要能寻址到队友，`name` 必须显式给出
- **`TaskUpdate` 依赖字段加等价性括注** —— CodeBuddy 确有「共享任务列表 + 指派 + blocked by」语义，但未找到 `addBlockedBy` 的拼写级证据，故改为「或运行时等价的依赖字段」

### 2. `codebase-analysis`

- frontmatter 同上处理
- `${CLAUDE_PLUGIN_ROOT}` → `${CODEBUDDY_PLUGIN_ROOT}`（4 处）
- `CLAUDE.md` → `CODEBUDDY.md`（3 处）
- 新增「Reference loading」段：给出变量未展开时的兜底定位方式
- **agent 引用去插件前缀**（4 处：本 skill ×2 + `references/actionable-insights-template.md` ×2）—— 上游写 `agent-alchemy-core-tools:code-architect`，但在 CodeBuddy 中全生态 `subagent_type` 实测均为**裸名**，故改为 `code-architect` / `code-explorer`。该参考文件因此由「逐字节一致」变为「已改写」

### 3. `interview-me`

- frontmatter 同上；原有的 `arguments:` YAML schema 移除（改由 command 承载 `argument-hint`）
- `${CODEBUDDY_PLUGIN_ROOT}` 替换（9 处）、`.claude/` → `.codebuddy/`（1 处）
- "Claude Code's plan mode" → "CodeBuddy's Plan mode"
- `AskUserQuestion` 全部保留（CodeBuddy 真实存在此工具）；「4 问/次」上限说明保留

### 4. `language-patterns` / 5. `project-conventions`

纯知识文件，**正文逐字未改**。仅 frontmatter 去掉两个无效字段并加 `version`；`project-conventions` 的约定来源列表把 `CLAUDE.md` 换成 `CODEBUDDY.md`。

### 6. `technical-diagrams`

- frontmatter：`description: >-`（折叠标量）压成单行，去掉两个无效字段
- 引用路径 2 处改变量；新增 Reference loading 兜底段
- 6 份 Mermaid 图型参考（`references/*.md`，约 1,586 行）**逐字复制**

---

## 三之二、中文触发词约定（本改造体系，**适用于全部 agent-alchemy 移植包**）

上游所有 `description` 都只有英文触发词（`Use when asked "fix this bug"…`）。中文语境下用户不会说
这些词，命中率因此很低。**本改造体系在移植时统一追加一行中文触发句**，形态固定为：

```
中文触发（用户这样说时使用）：<用户可能说出的 5~8 个中文说法，用「、」分隔>。
```

规则：

| 项 | 约定 |
|---|---|
| 位置 | 追加在英文 description **末尾**，同一行（单行 description）或同一缩进块的最后一行（折叠/块标量） |
| 适用对象 | **全部 skill 与全部 agent**，不区分"命令型"与"知识库型"（知识库 skill 也会被模型在语境下自动加载） |
| 写法 | 写**用户会说的话**，不写功能名词。反例：`中文触发：项目约定`；正例：`这个项目有什么约定、命名/代码风格怎么跟现有保持一致` |
| 禁止 | 不改写英文原文、不删除英文触发词、不动正文 |

**执行历史**：

- `v0.2.3-cb.1`：只给 3 个命令型 skill（`deep-analysis` / `codebase-analysis` / `interview-me`）加了 —— **覆盖不全**
- `v0.2.3-cb.2`（本版）：补齐 3 个知识库 skill + 4 个 agent，**6 skill + 4 agent 全覆盖**
- 后续移植的 dev-tools / tdd-tools / claude-tools / sdd-tools 各包**一律按本约定从首版起全覆盖**

## 四、4 个 agent 的改动

统一处理：
1. frontmatter 补齐 CodeBuddy 必填/推荐字段：`name`、`description`、`model`、`color`、`tools`
   - `color` 为 CodeBuddy agent 规范中的必填视觉标识 → 新增（explorer=cyan / synthesizer=yellow / architect=magenta / researcher=blue）
   - `description` 改写为「Use this agent when … + Examples」形态（CodeBuddy 触发规范）
   - `tools` 由 YAML 数组改为逗号串（与 `security-scan/agents/bg-scan.md` 的写法一致）
2. 删除 `skills:` 字段（CodeBuddy agent frontmatter 对预加载 skill 支持不明确）→ 改为正文顶部显式「Required knowledge loading」段，用 `Read` 加载同样的 skill 文件，**能力等价**
3. `.claude/` → `.codebuddy/`（`code-synthesizer` 的 3 处会话路径）

| Agent | 额外处理 |
|---|---|
| `code-explorer` | 预加载 `project-conventions` + `language-patterns` |
| `code-synthesizer` | 预加载 `project-conventions` + `language-patterns` + `technical-diagrams` |
| `code-architect` | 预加载 `technical-diagrams` |
| `interview-researcher` | ✓ 保留多行 `description: |` 与 3 个 `<example>`；`tools` 去掉写死的 `mcp__context7__*`，改为 `WebSearch, WebFetch` + 正文「可选 Context7」段 |

> **未降级**：`SendMessage` / `TaskUpdate` / `TaskGet` / `TaskList` 全部保留在 `tools` 中 —— 团队协作能力原样继承。

---

## 五、hook 的改动

| 文件 | 改动 |
|---|---|
| `hooks/hooks.json` | 仅 `${CLAUDE_PLUGIN_ROOT}` → `${CODEBUDDY_PLUGIN_ROOT}` |
| `hooks/auto-approve-da-session.sh` | `.claude/sessions/` → `.codebuddy/sessions/`（9 处）；注释里的 "Claude Code" → "CodeBuddy"；**审批输出 JSON 与退出码语义不变** |

依赖：`jq`（解析 hook 输入）。未装 `jq` 时脚本会静默 `exit 0`（无意见），退化为正常审批流，不会阻断执行。

---

## 六、新增的 3 个 command

上游把 `/deep-analysis`、`/codebase-analysis`、`/interview-me` 作为 `user-invocable` skill 暴露；CodeBuddy 的这个能力由 `commands/` 提供，故新增三个薄封装：

| Command | 作用 |
|---|---|
| `/deep-analysis [context]` | 载入 skill 全文并按 6 阶段执行；声明为 direct invocation（受 `direct-invocation-approval` 约束） |
| `/codebase-analysis [context]` | 载入 skill 并按 3 阶段执行；声明为 skill-invoked 模式（团队计划自动批准） |
| `/interview-me [topic-or-file]` | 载入 skill；强调「所有面向用户的提问必须走 AskUserQuestion」与「必须落盘产物」 |

---

## 七、上游更新时的同步清单

```bash
# 1. 重新下载上游，比对 core-tools
cd "$HOME" && curl -sSL -o aa.zip "https://codeload.github.com/sequenzia/agent-alchemy/zip/refs/heads/main"
python -c "import zipfile; zipfile.ZipFile('aa.zip').extractall('aa_new')"
diff -rq aa_new/agent-alchemy-main/claude/core-tools \
        /home/zhq/mydisk/myskill/external-skills/agent-alchemy-marketplace/core-tools

# 2. 若上游有变更，按本文件第二节映射表逐类重放改动
# 3. 复核：本产物应始终保持 0 处 CLAUDE_PLUGIN_ROOT / .claude/ / CLAUDE.md
grep -rn 'CLAUDE_PLUGIN_ROOT\|\.claude/\|CLAUDE\.md' /home/zhq/mydisk/myskill/plugins/core-tools-codebuddy/versions/*/plugin
```
