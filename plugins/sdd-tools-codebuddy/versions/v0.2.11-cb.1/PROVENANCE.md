# 改造产物溯源与基线指纹 (PROVENANCE)

> 本文件是 **`v0.2.11-cb.1` 冻结基准**的权威记录，用于日后校准：上游更新后重跑改造，与本基准比对即可定位差异。
> 本文件位于 `plugin/` **之外**，因此**不参与**包指纹计算（规避「把自身 md5 写进自身」的自引用问题）。

## 一、权威坐标

| 项 | 值 |
|---|---|
| **上游仓库** | `https://github.com/sequenzia/agent-alchemy` |
| **上游作者** | Stephen Sequenzia (sequenzia@gmail.com) |
| **上游许可证** | MIT |
| **上游插件名** | `agent-alchemy-sdd-tools` |
| **上游插件版本** | `0.2.11` |
| **上游包内路径** | `claude/sdd-tools/` |
| **上游 commit** | `fc1a336b8267e70579af8517d14718e626824e54`（2026-05-31） |
| **本地上游镜像** | [`../../../../external-skills/agent-alchemy-marketplace/sdd-tools/`](../../../../external-skills/agent-alchemy-marketplace/sdd-tools/)（41 文件，零改写） |
| **上游包指纹** | `d05f987a0964c02cd90b512a7234fba2` |
| **本产物版本** | **`0.2.11-cb.1`**（`<上游版本>-cb.<改造修订号>`） |
| **本产物目标平台** | CodeBuddy（CodeBuddy 插件体系） |
| **本产物包指纹** | **`7bd5a590e650a9c9b97aae5152baf596`** |
| **改造日期** | 2026-09-20 |
| **转换规则全文** | [`../../docs/CONVERSION.md`](../../docs/CONVERSION.md) |

## 二、版本号约定

| 位置 | 字段 | 含义 |
|---|---|---|
| `plugin/.codebuddy-plugin/plugin.json` | `version` | **产物版本**，权威 = `0.2.11-cb.1` |
| `plugin/skills/*/SKILL.md` | `version` | **上游来源版本** = `0.2.11`，仅作溯源；上游技能原本无此字段，为改造时补入 |

`-cb.N` 中的 `N` 只在**上游版本不变、而本产物需修订**时递增；上游版本变化时改为 `<新上游版本>-cb.1`。

## 三、逐文件对照（本产物 → 上游）

`md5` 为本产物文件的值；与上游关系分三类：**逐字节一致** / **已改写** / **本产物新增**。

| 本产物文件 | md5 | 与上游关系 |
|---|---|---|
| `.codebuddy-plugin/plugin.json` | `fb92d7f357745a4a5cd4ffec4b7c25e8` | 本产物新增 |
| `DEEP-DIVE.md` | `0e94ba34b7faa784251692c307dadd4a` | 已改写（上游架构分析，路径已本地化） |
| `README.md` | `2982d71ed32ff3f251458fc43673c1cc` | 已改写（换成本产物的使用手册） |
| `agents/codebase-explorer.md` | `f9cd6ef5944d3f6209d119aa2998dbf6` | 已改写 |
| `agents/context-manager.md` | `fc69027521d1e5612bbdaa6512fac507` | 已改写 |
| `agents/researcher.md` | `00b8aec5f2495f4a6bdacf60a390e298` | 已改写 |
| `agents/spec-analyzer.md` | `49019c5e260bafc46861bf489f59a2ff` | 已改写 |
| `agents/task-executor-v2.md` | `22855249e02bed4cc06e7c9e88993b30` | 已改写 |
| `agents/task-executor.md` | `ab49c28e778570fc6fd76e411f74fbb0` | 已改写 |
| `agents/wave-lead.md` | `145065c32f295772c6b71bf4be27cd48` | 已改写 |
| `commands/analyze-spec.md` | `597689981f509f4df260fc964e88d05a` | 本产物新增（COMMAND） |
| `commands/create-spec.md` | `9bb2756e43f9f149f46da2f708083232` | 本产物新增（COMMAND） |
| `commands/create-tasks.md` | `0892e519428797ed46694d762df187a6` | 本产物新增（COMMAND） |
| `commands/execute-tasks.md` | `32c8d3745155ff1b2fc1951de274181b` | 本产物新增（COMMAND） |
| `commands/run-tasks.md` | `42d575e6484ef87d77695d64fffddb03` | 本产物新增（COMMAND） |
| `hooks/auto-approve-session.sh` | `3c773151afb7b2f3eb40a4aad757240a` | 已改写 |
| `hooks/hooks.json` | `8d55d3cb38bb51166ef0bfa9c2685ca4` | 已改写（删除 SessionStart 建链条目） |
| `hooks/verify-task-completion.sh` | `e73120dd0b1f3b4eb5ea278f7c54010b` | 逐字节一致 |
| `skills/analyze-spec/SKILL.md` | `c05b2e2c275c1c0b36f25214aa03722b` | 已改写 |
| `skills/analyze-spec/references/analysis-criteria.md` | `f9eccae56335937920e854f2e1e5f4c2` | 逐字节一致 |
| `skills/analyze-spec/references/common-issues.md` | `4fb952239af0d0e63c010eba03b8d62d` | 逐字节一致 |
| `skills/analyze-spec/references/html-review-guide.md` | `0ea5f92131e509ee1782966ab3d1d094` | 逐字节一致 |
| `skills/analyze-spec/references/report-template.md` | `238fab37eee7d6779d3f9f3c0bc60b0a` | 逐字节一致 |
| `skills/analyze-spec/templates/review-template.html` | `655316e9b241e75140e61af7f59b34c6` | 逐字节一致 |
| `skills/create-spec/SKILL.md` | `30e7403b2802376467da23b5efe9bdfc` | 已改写 |
| `skills/create-spec/references/codebase-exploration.md` | `f63aadf8a0c5e64c6954c46b11ce03c5` | 已改写 |
| `skills/create-spec/references/complexity-signals.md` | `3fb49ba4b736c77bd54e04bc7d250707` | 逐字节一致 |
| `skills/create-spec/references/interview-questions.md` | `e01f3a1a5a820f21d7f84c5f485f5146` | 逐字节一致 |
| `skills/create-spec/references/recommendation-format.md` | `29cd4289ad4435a038016b0a71bac3e7` | 逐字节一致 |
| `skills/create-spec/references/recommendation-triggers.md` | `97775fe7f52ff411aebc065f3729794e` | 逐字节一致 |
| `skills/create-spec/references/templates/detailed.md` | `cd3b28d085286252748bf8a571c9bc14` | 逐字节一致 |
| `skills/create-spec/references/templates/full-tech.md` | `7b50dd3d006bc1121c4fe480639420ce` | 逐字节一致 |
| `skills/create-spec/references/templates/high-level.md` | `bf5b0b430b58ecba36fc41d32c97aed0` | 逐字节一致 |
| `skills/create-tasks/SKILL.md` | `f5fdf7e4e8946d323ef70d7ade47691d` | 已改写 |
| `skills/create-tasks/references/decomposition-patterns.md` | `a9e210e0ff87bc0372320ff1fcbd4479` | 逐字节一致 |
| `skills/create-tasks/references/dependency-inference.md` | `c73340383ec8adc295f755367e6ae87b` | 逐字节一致 |
| `skills/create-tasks/references/testing-requirements.md` | `11a276f3bd0198a8a8a746c52ac3e1d6` | 逐字节一致 |
| `skills/execute-tasks/SKILL.md` | `b68f8dd26ab1040841c6b3ead95d90cc` | 已改写 |
| `skills/execute-tasks/references/execution-workflow.md` | `aea85b8a5e7f805343f88244c613754f` | 已改写 |
| `skills/execute-tasks/references/orchestration.md` | `9f682ae4cbfb52094d93ca38b8e1f429` | 已改写 |
| `skills/execute-tasks/references/verification-patterns.md` | `b7f97daa008ee7cd0964a4a7f53a9b99` | 已改写 |
| `skills/execute-tasks/scripts/poll-for-results.sh` | `bdde066206af13e7ae01d866c3693681` | 已改写 |
| `skills/run-tasks/SKILL.md` | `24b1d90843452c7fd49f168ce4787e75` | 已改写 |
| `skills/run-tasks/references/communication-protocols.md` | `a5067d74f89c91a1534da885ebd14a5d` | 已改写 |
| `skills/run-tasks/references/orchestration.md` | `69823fcddc5ebe89e2256921f6386731` | 已改写 |
| `skills/run-tasks/references/verification-patterns.md` | `16d11e36278c1f427d5abba9d996b985` | 已改写 |

**计数**：逐字节一致 **16** ｜ 已改写 **24** ｜ 本产物新增 **6** ｜ 合计 **46**。

**未移植 1 项**：`hooks/resolve-cross-plugins.sh`（Claude Code 插件缓存布局的短名符号链接机制，
CodeBuddy 平铺市场不需要；`hooks.json` 的 `SessionStart` 条目随之删除，其余三个事件全部保留）。
上游 41 个文件中 **40 个有对应**（= 逐字节一致 16 + 已改写 24）；`README.md` 路径相同但内容已换成使用手册，计入「已改写」。

## 四、完整性校验

### 1. 包指纹

算法（**只覆盖 `plugin/`，不含本文件与 `source.zip`**，故无自引用问题）：

```bash
cd versions/v0.2.11-cb.1/plugin
find . -type f | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32
# → 7bd5a590e650a9c9b97aae5152baf596
```

> `LC_ALL=C` 不可省：不同 locale 的 `sort` 排序不同，换环境会算出不同指纹。

### 2. 上游基线

```bash
cd ../../../../external-skills/agent-alchemy-marketplace/sdd-tools
find . -type f ! -name PROVENANCE.md | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32
# → d05f987a0964c02cd90b512a7234fba2（应等于顶层 README 记录的 sdd-tools 指纹）
```

### 3. 一键校准

```bash
bash versions/v0.2.11-cb.1/verify.sh
```
