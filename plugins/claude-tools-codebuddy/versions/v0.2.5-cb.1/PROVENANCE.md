# 改造产物溯源与基线指纹 (PROVENANCE)

> 本文件是 **`v0.2.5-cb.1` 冻结基准**的权威记录，用于日后校准：上游更新后重跑改造，与本基准比对即可定位差异。
> 本文件位于 `plugin/` **之外**，因此**不参与**包指纹计算（规避「把自身 md5 写进自身」的自引用问题）。

## 一、权威坐标

| 项 | 值 |
|---|---|
| **上游仓库** | `https://github.com/sequenzia/agent-alchemy` |
| **上游作者** | Stephen Sequenzia (sequenzia@gmail.com) |
| **上游许可证** | MIT |
| **上游插件名** | `agent-alchemy-claude-tools` |
| **上游插件版本** | `0.2.5` |
| **上游包内路径** | `claude/claude-tools/` |
| **上游 commit** | `fc1a336b8267e70579af8517d14718e626824e54`（2026-05-31） |
| **本地上游镜像** | [`../../../../external-skills/agent-alchemy-marketplace/claude-tools/`](../../../../external-skills/agent-alchemy-marketplace/claude-tools/)（9 文件，零改写） |
| **上游包指纹** | `37c98b0026d9d87e376684c7a4bd147b` |
| **本产物版本** | **`0.2.5-cb.1`**（`<上游版本>-cb.<改造修订号>`） |
| **本产物目标平台** | CodeBuddy（CodeBuddy 插件体系） |
| **本产物包指纹** | **`1d0bc4896dff9d49d39a0becd9acbf59`** |
| **改造日期** | 2026-09-20 |
| **转换规则全文** | [`../../docs/CONVERSION.md`](../../docs/CONVERSION.md) |

## 二、版本号约定

| 位置 | 字段 | 含义 |
|---|---|---|
| `plugin/.codebuddy-plugin/plugin.json` | `version` | **产物版本**，权威 = `0.2.5-cb.1` |
| `plugin/skills/*/SKILL.md` | `version` | **上游来源版本** = `0.2.5`，仅作溯源；上游技能原本无此字段，为改造时补入 |

`-cb.N` 中的 `N` 只在**上游版本不变、而本产物需修订**时递增；上游版本变化时改为 `<新上游版本>-cb.1`。

> 上游原技能的 `last-verified: 2026-03-07 / 2026-03-09` 字段未保留（CodeBuddy skill frontmatter 无此字段），
> 这两个日期改记于此：**`claude-code-tasks` 上游最后核对日 2026-03-07；`claude-code-teams` 为 2026-03-09**。

## 三、逐文件对照（本产物 → 上游）

`md5` 为本产物文件的值；与上游关系分三类：**逐字节一致** / **已改写** / **本产物新增**。

| 本产物文件 | md5 | 与上游关系 |
|---|---|---|
| `.codebuddy-plugin/plugin.json` | `9bb0a99595f902002e86819b6cfcb985` | 本产物新增 |
| `README.md` | `f570f8da120fdb4d7cd0d2c6c92ae6f3` | 已改写（换成本产物的使用手册） |
| `skills/claude-code-tasks/SKILL.md` | `39717f5a5034b1bec3bc2a56be4ad9df` | 已改写（+移植说明段） |
| `skills/claude-code-tasks/references/anti-patterns.md` | `83907bd42c9bc5dad48839dbeac6ef4a` | 已改写 |
| `skills/claude-code-tasks/references/task-patterns.md` | `26cdfff1c499756df0c2cdf2e762e55a` | 已改写 |
| `skills/claude-code-teams/SKILL.md` | `be298eb74fbbaeea1f5df953c693e5bd` | 已改写（+移植说明段） |
| `skills/claude-code-teams/references/.gitkeep` | `d41d8cd98f00b204e9800998ecf8427e` | 逐字节一致（空文件） |
| `skills/claude-code-teams/references/hooks-integration.md` | `58f3479767748f31bd93585dde45bc9e` | 已改写 |
| `skills/claude-code-teams/references/messaging-protocol.md` | `ad7e897787246f564fcf0158c5007bd1` | 已改写 |
| `skills/claude-code-teams/references/orchestration-patterns.md` | `b8f41fb5de640d2695b281b7a1db04df` | 已改写 |

**计数**：逐字节一致 **1** ｜ 已改写 **8** ｜ 本产物新增 **1** ｜ 合计 **10**。

**未移植 0 项**：上游 9 个文件**全部有对应**（`README.md` 路径相同但内容换成使用手册，计入「已改写」）。

## 四、完整性校验

### 1. 包指纹

算法（**只覆盖 `plugin/`，不含本文件与 `source.zip`**，故无自引用问题）：

```bash
cd versions/v0.2.5-cb.1/plugin
find . -type f | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32
# → 1d0bc4896dff9d49d39a0becd9acbf59
```

> `LC_ALL=C` 不可省：不同 locale 的 `sort` 排序不同，换环境会算出不同指纹。

### 2. 上游基线

```bash
cd ../../../../external-skills/agent-alchemy-marketplace/claude-tools
find . -type f ! -name PROVENANCE.md | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32
# → 37c98b0026d9d87e376684c7a4bd147b（应等于顶层 README 记录的 claude-tools 指纹）
```

### 3. 一键校准

```bash
bash versions/v0.2.5-cb.1/verify.sh
```
