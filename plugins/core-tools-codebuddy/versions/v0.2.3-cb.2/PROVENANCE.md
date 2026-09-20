# 改造产物溯源与基线指纹 (PROVENANCE) —— v0.2.3-cb.2

> 本文件是 **`v0.2.3-cb.2`** 的权威记录。它是 `v0.2.3-cb.1`（首版冻结基准）的**增量修订版**，
> **上游版本未变**（仍为 `0.2.3`），按 `README.md` 的约定递增 `cb.N`。
> 本文件位于 `plugin/` **之外**，不参与包指纹计算。

## 一、权威坐标

| 项 | 值 |
|---|---|
| **上游仓库** | `https://github.com/sequenzia/agent-alchemy` |
| **上游作者 / 许可证** | Stephen Sequenzia ｜ MIT |
| **上游插件名 / 版本** | `agent-alchemy-core-tools` ｜ `0.2.3` |
| **上游包内路径** | `claude/core-tools/` |
| **上游 commit** | `fc1a336b8267e70579af8517d14718e626824e54`（2026-05-31） |
| **本地上游镜像** | [`../../../../external-skills/agent-alchemy-marketplace/core-tools/`](../../../../external-skills/agent-alchemy-marketplace/core-tools/)（26 文件，零改写） |
| **上游包指纹** | `808192241ec2c53ced9bd83227279279` |
| **上一版（不再改动）** | [`../v0.2.3-cb.1/`](../v0.2.3-cb.1/)，包指纹 `2a25c41b8b418c0e1b1967053412d66e` |
| **本产物版本** | **`0.2.3-cb.2`** |
| **本产物目标平台** | CodeBuddy |
| **本产物包指纹** | **`e44a2692f51dc2cd3cc6828d5760bece`** |
| **改造日期** | 2026-09-20 |
| **转换规则全文** | [`../../docs/CONVERSION.md`](../../docs/CONVERSION.md) |

## 二、本版改了什么：把中文触发词补齐

`v0.2.3-cb.1` 只给 **3 个命令型 skill**（`deep-analysis` / `codebase-analysis` / `interview-me`）
的 `description` 追加了中文触发词，**漏了另外 7 个**（3 个知识库 skill + 4 个 agent）。
本版补齐，使 **core-tools 全部 6 个 skill + 4 个 agent 的 description 都含中英双语触发词**。

| 文件 | 补的中文触发场景（摘要） |
|---|---|
| `skills/language-patterns/SKILL.md` | TypeScript/Python/React 怎么写更地道、语言习惯用法、最佳实践 |
| `skills/project-conventions/SKILL.md` | 这个项目有什么约定、命名/目录/代码风格怎么跟现有一致 |
| `skills/technical-diagrams/SKILL.md` | 画架构图/时序图/流程图/类图/ER 图、用 Mermaid、配色看不清 |
| `agents/code-architect.md` | 出实现方案、设计架构、要几套方案对比、改动怎么落地、有哪些风险 |
| `agents/code-explorer.md` | 把这个模块摸清楚、追执行路径、找相关文件、代码怎么组织 |
| `agents/code-synthesizer.md` | 把几份探索结果合并、结论有冲突帮我定、查漏补缺 |
| `agents/interview-researcher.md` | 帮我查这个方向的资料、有哪些现成做法、合规与最佳实践 |

**改动方式**：只动 `description` 一行（追加中文触发句），**正文一字未改**；agent 的 `description`
是折叠标量 / 块标量，中文触发行按同样缩进追加在最后一行描述之后、`model:` 之前。

## 三、与 cb.1 的差异（本版校准口径）

| 关系 | 数量 |
|---|---|
| 与 `v0.2.3-cb.1/plugin` **逐字节一致** | **22** |
| 与 `v0.2.3-cb.1/plugin` **已改写**（本版改动） | **8** |
| 本产物新增 | **0** |
| 合计 | **30** |

> `v0.2.3-cb.1/plugin` 的包指纹必须始终仍为 `2a25c41b8b418c0e1b1967053412d66e` —— 基准不动是本版存在的前提。

| 本产物文件（相对 cb.1 已改写） | md5 |
|---|---|
| `.codebuddy-plugin/plugin.json` | `a86364d59ad824f4c7989571655a040f` |
| `agents/code-architect.md` | `4a915dee6b962cca1d9cd746359ab955` |
| `agents/code-explorer.md` | `a9f31ec38285b988b49ec00c3aad3a9d` |
| `agents/code-synthesizer.md` | `224d0570fffeb857e6b2f7581bcedde7` |
| `agents/interview-researcher.md` | `9cd3212273bacb96c7305323303001f8` |
| `skills/language-patterns/SKILL.md` | `707132ddda1119d0ade4085b77651eee` |
| `skills/project-conventions/SKILL.md` | `8d294c3207c771f0c346d81cfd45901f` |
| `skills/technical-diagrams/SKILL.md` | `046577ad008920f5d516300ebb356211` |

其余 22 个文件的 md5 见 [`../v0.2.3-cb.1/PROVENANCE.md`](../v0.2.3-cb.1/PROVENANCE.md) 第三节（未改动，故不重复列）。

## 四、与上游的关系（不变）

与 `v0.2.3-cb.1` 相同：**逐字节一致 12 ｜ 已改写 14 ｜ 本产物新增 4 ｜ 未移植 0**。
本版改动的 7 个 description 文件本来就在「已改写」集合内（cb.1 时是因 frontmatter 规范化与中文触发），
故分类计数不变，只是"已改写"的具体内容多了一次中文触发的追加。

## 五、完整性校验

### 1. 包指纹

```bash
cd versions/v0.2.3-cb.2/plugin
find . -type f | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32
# → e44a2692f51dc2cd3cc6828d5760bece
```

### 2. 一键校准

```bash
bash versions/v0.2.3-cb.2/verify.sh
```

校验四件事：cb.2 本体指纹、cb.2 存档、**cb.1 基准未被改动**、cb.2 与 cb.1 的 23/7/0 差异，
以及上游基线指纹。
