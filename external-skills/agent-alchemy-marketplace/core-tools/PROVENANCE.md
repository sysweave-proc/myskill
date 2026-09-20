# 上游溯源记录 (PROVENANCE)

> 本文件由下载流程自动生成，用于**复核原始基线**。落盘文件未经任何改写。

## 权威坐标

| 项 | 值 |
|---|---|
| 仓库 | `https://github.com/sequenzia/agent-alchemy` |
| 作者 | Stephen Sequenzia (sequenzia@gmail.com) |
| 许可证 | MIT |
| marketplace | `agent-alchemy` |
| **插件名** | **`agent-alchemy-core-tools`** |
| 插件版本 | `v0.2.3` |
| 包内路径 | `claude/core-tools/` |
| 分支 | `main` |
| **commit** | `fc1a336b8267e70579af8517d14718e626824e54` |
| commit 日期 | `2026-05-31T22:30:00Z` |
| 下载日期 | `2026-09-19` |

## 获取方式（任选其一，结果应一致）

```bash
# A. 直接下 zip（本次采用）
curl -sSL -o aa.zip https://codeload.github.com/sequenzia/agent-alchemy/zip/refs/heads/main

# B. 走 skills CLI
npx skills add sequenzia/agent-alchemy --skill codebase-analysis

# C. 走 claudepluginhub
npx claudepluginhub sequenzia/agent-alchemy --plugin agent-alchemy-core-tools
```

## 完整性校验

### 1. 逐文件 md5

> 注：本文件（`PROVENANCE.md`）**不参与校验** —— 它是本地新增的溯源记录，上游 `claude/core-tools/` 无此件；且把自身 md5 写入自身属自引用，必然失效。故下列清单只含 **26 个上游文件**。

```
be60b3c6b9494f7f8535ce5ed5eb2c99 *./README.md
90d0ca53ed98cb184972215a8951966c *./agents/code-architect.md
1b0ffea33a42060c94a4bf063348fc32 *./agents/code-explorer.md
f7ce1056d888aed50e0b36fc457f260f *./agents/code-synthesizer.md
edef6a973004d0d8411807abf57febed *./agents/interview-researcher.md
06ae603715a639752999b53c22c7d76a *./hooks/auto-approve-da-session.sh
c2dae6526052c3af349150360ab7b7d1 *./hooks/hooks.json
056e498ac2834ca051238594a4be8690 *./skills/codebase-analysis/SKILL.md
e4cf51cd8ae2da88f620c2aaf2a7bd77 *./skills/codebase-analysis/references/actionable-insights-template.md
97d339eb24238bc2413f3fcde49183aa *./skills/codebase-analysis/references/report-template.md
60051fe5e5d74a86a375cedf37f19308 *./skills/deep-analysis/SKILL.md
e4b1a3c9cd76d15a643b72dcb927e75c *./skills/interview-me/SKILL.md
0bf3888c6ba6a71ae246f98eb1a92c1f *./skills/interview-me/references/question-bank.md
dcbeee15bfd22a090981738a5f671183 *./skills/interview-me/references/research-triggers.md
41ba795003aede8151870f0dbdc7966e *./skills/interview-me/references/templates/implementation-plan.md
9ad0f02ae0295330ff3b8a6fa7226514 *./skills/interview-me/references/templates/report-detailed.md
d294c0d3b44da6ea682d9b9614990533 *./skills/interview-me/references/templates/report-summary.md
8822ed493e3098c2db14811a588ca5ad *./skills/language-patterns/SKILL.md
08d5f69780ceb3a568f933e8f01b5cf8 *./skills/project-conventions/SKILL.md
4ceea9793958bd4bd19db4cf42df082d *./skills/technical-diagrams/SKILL.md
97c7ee027324a90558045bc7f7ddbeaf *./skills/technical-diagrams/references/c4-diagrams.md
2e2bafd51924a820f6d06ca59800d420 *./skills/technical-diagrams/references/class-diagrams.md
877dd8b0b83649b724551f3c28359565 *./skills/technical-diagrams/references/er-diagrams.md
a77e92266bd1701bb900df9c4f51df93 *./skills/technical-diagrams/references/flowcharts.md
604ee672520557967d097e60659f04f4 *./skills/technical-diagrams/references/sequence-diagrams.md
4ec3c45abf0874316def0430f177977c *./skills/technical-diagrams/references/state-diagrams.md
```

### 2. 包指纹（算法：`find . -type f ! -name PROVENANCE.md | LC_ALL=C sort | xargs md5sum | md5sum`）

```
808192241ec2c53ced9bd83227279279
```

> ⚠️ 两个口径细节缺一不可：`! -name PROVENANCE.md` 排除自引用件；`LC_ALL=C` 固定排序 locale（否则换环境算出的值不同——同一目录实测两种排序结果就不一样）。
> 本文件此前记录的 `efe0cbbaa5bb79a4dc402ac130769442` 因上述两个原因**不可复现，已作废**。

### 3. 文件计数

```
上游文件: 26（本文件 PROVENANCE.md 为本地新增，不计入）
磁盘文件: 27
```

## 复核命令

```bash
# 重新下载上游并比对（差异为空即一致）
curl -sSL -o /tmp/aa.zip https://codeload.github.com/sequenzia/agent-alchemy/zip/refs/heads/main
unzip -q /tmp/aa.zip -d /tmp/aa
diff -rq /tmp/aa/agent-alchemy-main/claude/core-tools ./
```

## 校验结论

- 26 个文件与上游 `claude/core-tools/` **逐字节一致**，差异标记 `0`。
- **零改写**：无适配、无补丁、无删改。
- 因此可作为后续移植改造的**原始基线**。
