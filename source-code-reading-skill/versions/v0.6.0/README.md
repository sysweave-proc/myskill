# v0.6.0

**主题**：认知 × 工程 合并发版 ｜ **规模**：59 文件 / 4,418 行 ｜ `SKILL.md` 的 `version: 0.6.0`

## 本版变化

v0.1 ~ v0.5.1 六版都是**同一场会话在六个时刻冻结**下来的产物；**v0.6.0 不是**。

它是 [`v0.5.1`](../v0.5.1/) 与 [`../../skill-ds/`](../../skill-ds/)（另一次「模型自己读完会话后重新收敛」的再表达版）的**增量合并件**，在本地生成，所以本目录**没有 `conversation/`**——合并的依据与过程改由包内两个文件承担：

| 文件 | 作用 |
|---|---|
| `skill/MERGE_DECISION.md` | 完整合并决策记录：输入资产盘点、A~G 七项决策、冲突处理规则、非回归核对清单、后续演进流程 |
| `skill/MERGE_MANIFEST.yaml` | 机器可读的合并清单：两个来源的角色定位、被排除的 `skill-ds-chatgpt`、合并策略、新增能力列表 |

合并的取舍可以用一句话概括：

```text
v0.5.1   = 完整工程资产（图法目录、知识源注册、cases、回归、模板、测试）
skill-ds = 更强的认知协议（五类知识、Cognitive Spine、六阶段×七闸门、L0–L3、情境化知识）
               ↓ 增量合并（保基线文件、保能力、不许静默删除）
v0.6.0   = 可执行、可追溯、可回归、可持续演进的源码阅读 Skill
```

关键决策：

- **以 v0.5.1 作文件基线**（决策 A）：从完整资产集增量演进，而不是在 skill-ds 的十余个文件上重搭。
- **以 skill-ds 的 Cognitive Core 重写 `SKILL.md`**（决策 B），主轴为：
  五类知识 → Cognitive Spine → System Atlas → 六阶段 × 七闸门 → L0–L3 → Pattern → Traceability → Representation → Validation → Evolution。
- **深资产全部保留**（决策 C / E）：完整图法目录 `references/diagrams/diagram-catalog.md` 未被压缩，只在新规则里回答「何时需要这种语义」。
- **重复内容不双轨运行**（决策 D）：同一知识点**只保留一个权威规范**，新出现的入口页只做导航与决策，不另立规则。
- **情境提升为正式附着层**（决策 F）：`references/situated-knowledge.md` 进入核心执行协议，而非可选附录。
- **演进视为运行时闭环**（决策 G）：Agent 可以提案，不能静默改规范。

## 文件增量

对比 [`v0.5.1/skill/`](../v0.5.1/skill/)：**50 个文件一个不少**（0 删除），+9 新增、9 覆写。

**新增 9 个**

| 文件 | 定位 |
|---|---|
| `MERGE_DECISION.md` | 合并决策记录（本版独有） |
| `MERGE_MANIFEST.yaml` | 合并清单（本版独有） |
| `references/situated-knowledge.md` | **新规范**：版本/构建/性能/决策/学习路径/冲突/变更影响 |
| `references/architecture-atlas.md` | 快速入口卡 → `architecture-model.md` / `architecture-reconstruction.md` |
| `references/patterns.md` | 快速入口卡 → `patterns/pattern-catalog.md` |
| `references/representation.md` | 快速入口卡 → `representation/representation-policy.md` |
| `references/traceability.md` | 快速入口卡 → `tracing/` |
| `references/validation.md` | 快速入口卡 → `validation/validation-policy.md` |
| `tests/test_merged_capabilities.py` | 合并后能力的语义检查 |

**覆写 9 个**：`SKILL.md`、`README.md`、`CHANGELOG.md`、`EVOLUTION_AUDIT.md`、`references/knowledge-model.md`、`evolution/capability-inventory.md`、`evolution/evolution-policy.md`、`evolution/approved-changes.yaml`、`evolution/approved-removals.yaml`

## 目录

| 路径 | 内容 |
|---|---|
| `skill/` | 技能包文件树（59 个文件，可直接阅读） |
| `source.zip` | 原始 zip（内层根目录 `source-code-reading-skill-v0.6.0/`，权威字节，勿改） |

## 备注

- **本版没有 `conversation/`**，这是与其他六版唯一的结构差别：它不是会话冻结产物。
- 包内出现「`*-policy.md` / `*-catalog.md`（规范）+ `architecture-atlas.md` 等（快速入口）」成对文件，是决策 D 的刻意产物——入口页末尾都显式回指规范位置（例：`traceability.md` → `references/tracing/`）。
- `SKILL.md` 的 `description` 仍是 `>-` 折叠式块标量（继承六版写法），但文本内不含尖括号。
- 交付校验：`skill/tests/test_skill_integrity.py`（对 v0.4 基线做 SHA-256 比对 + 白名单）与 `skill/tests/test_merged_capabilities.py`（合并能力语义检查）。
