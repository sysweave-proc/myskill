# agent-alchemy-dev-tools · 使用手册

日常开发流程：功能开发 / 修 bug / 代码评审 / 文档 / changelog / 发版。

> 本文件是**使用手册**，不属于上游移植内容（上游 `README.md` 未移植）。
> 上游来源：`sequenzia/agent-alchemy` → `agent-alchemy-dev-tools` v0.3.4，commit `fc1a336b`，MIT。
> **跨插件依赖**：本插件复用 core-tools 的 `code-architect` / `code-explorer` agent 与
> `deep-analysis` / `language-patterns` / `technical-diagrams` skill —— core-tools 必须装在**同一个市场**里。

---

## 一、30 秒上手

插件**没有"启动"这个动作**，入口就是下面五条命令：

| 我要做什么 | 输入 | 它实际会做什么 |
|---|---|---|
| 开发一个新功能 | `/feature-dev 给设置页加暗色主题切换` | 7 阶段：理解需求 → 探索代码 → 提问 → 出 2-3 套架构方案 → 实现 → 3 个评审代理独立评审 → 总结 |
| 修一个 bug | `/bug-killer 登录后偶发 500，日志见 error.log` | 假设日志 → 复现 → 取证 → 确认根因 → 带证明地修 → 回归测试 → 复盘 |
| 写/更新文档 | `/docs-manager 给这个项目生成 MkDocs 站点` | 交互确认格式 → 探测项目 → 分析代码 → 出文档计划给你批 → 派 `docs-writer` 生成 → 校验落地 |
| 记录本次改动 | `/document-changes auth 重构` | 读 git 变更 → 生成一份 markdown 变更报告（新增/修改/删除 + 摘要） |
| 发一个 Python 包 | `/release-python-package 1.2.0` | 9 步发布：分支/工作区/测试闸门 → 算版本 → 更新 changelog → 打 tag |

**不想记命令**就直接说人话，`description` 里的中文触发词会让模型自动加载对应 skill：

```
这段代码为什么一并发就崩？帮我查一下
给这个仓库补一套 MkDocs 文档
```

---

## 二、打完后会看到什么

### `/feature-dev`（7 阶段，必须跑完）

```
Phase 1 Discovery            → 复述需求，AskUserQuestion 确认
Phase 2 Codebase Exploration → 加载 deep-analysis 探索相关区域
Phase 3 Clarifying Questions → 把歧义问掉
Phase 4 Architecture Design  → 并行派 2-3 个 code-architect（来自 core-tools）出竞品方案
Phase 5 Implementation       → 按选定方案落地
Phase 6 Quality Review       → 并行派 3 个 code-reviewer 独立评审
Phase 7 Summary              → 总结 + changelog 条目
```

### `/bug-killer`（5 阶段，**先取证再改码**）

```
Phase 1 Triage & Reproduction → 复现 + 决定走 quick 还是 deep 轨道（--deep 直接进 deep）
Phase 2 Investigation         → 分语言取证（python / typescript / general 调试手册）
Phase 3 Root Cause Analysis   → 假设逐个证伪，确认根因
Phase 4 Fix & Verify          → 带证明的修复 + 回归测试 + 质量检查
Phase 5 Wrap-up & Report      → 复盘；命中项目特有经验时写进 CODEBUDDY.md
```

### 其余三条

- `/docs-manager` 支持两种形态（MkDocs 站点 / 独立 markdown）与三种动作（generate / update / change-summary）。
- `/document-changes` 只在 git 仓库且有真实改动时产出报告，否则**提前停止**，不编造。
- `/release-python-package` **fail fast**：分支不对、工作区不干净、测试不过，任一条立即停。

---

## 三、怎么判断"整个插件"在工作

关键信号：**有没有派生多个子代理**。

| 现象 | 含义 |
|---|---|
| `/feature-dev` 派出了 `code-architect` / `code-reviewer` 子代理 | ✅ 完整生效 |
| `/bug-killer --deep` 派出了 `code-explorer` / `bug-investigator` | ✅ 完整生效 |
| 全程只有它自己埋头读写文件，**没有任何子代理** | ❌ agent 未加载，退化成单线程 —— 见排错 |

> `code-architect` / `code-explorer` 来自 **core-tools**，不在本包内。只用裸名寻址（CodeBuddy 生态的
> `subagent_type` 不带插件前缀）；若运行时解析不到，`feature-dev` 会退化为自己内联做架构设计。

---

## 四、排错

| 现象 | 原因 | 处理 |
|---|---|---|
| 打 `/feature-dev` 没反应 | 插件没加载 | `/plugin list` 确认出现 `agent-alchemy-dev-tools@<市场名>`；没有就先 `/plugin marketplace add <市场目录>` 再**完全重启** CodeBuddy |
| 派生 `code-architect` 报找不到 agent | core-tools 没装在同一市场 | 在本市场同时启用 `agent-alchemy-core-tools` |
| 读 `${CODEBUDDY_PLUGIN_ROOT}/../agent-alchemy-core-tools/...` 失败 | 运行时不展开变量，或两个插件不在同一市场 | 技能正文已写兜底：用 Glob 搜 `**/agent-alchemy-core-tools/skills/**` 按名字定位 |
| 没看到任何弹窗提问 | 当前运行时不支持 `AskUserQuestion` | 退化成文字提问，功能不丢，只是体验不同 |
| `/release-python-package` 一上来就停 | 不在 main 分支 / 工作区脏 / 测试未过 | 这是设计如此（fail fast），按提示处理后重跑 |

---

## 五、这个包里有什么

```
agent-alchemy-dev-tools/
├── commands/   5 个命令入口：/feature-dev、/bug-killer、/docs-manager、
│                     /document-changes、/release-python-package
├── skills/     9 个：feature-dev、bug-killer、docs-manager、document-changes、
│                     release-python-package（name: release）、
│                     architecture-patterns、code-quality、project-learnings、changelog-format
├── agents/     4 个：code-reviewer（评审）、bug-investigator（取证）、
│                     changelog-manager（changelog）、docs-writer（文档/图表）
└── README.md   本手册
```

**4 个 skill 不是入口**（`user-invocable: false`）：`architecture-patterns`、`code-quality`、
`project-learnings`、`changelog-format` —— 它们分别被 `feature-dev` / `bug-killer` 在相应阶段加载。

**上游的 `resolve-cross-plugins.sh` hook 未移植**：那是为 Claude Code 的「插件缓存 + 版本子目录」
布局做的短名符号链接机制；CodeBuddy 本地市场是平铺结构，跨插件引用直接写带组织前缀的兄弟目录名
（`../agent-alchemy-core-tools/...`）即可解析，无需 SessionStart 建链。
