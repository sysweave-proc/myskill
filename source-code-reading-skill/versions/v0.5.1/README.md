# v0.5.1

**主题**：非回归修复 ｜ **规模**：50 文件 / 3,441 行 ｜ `SKILL.md` 的 `version: 0.5.1`

## 本版变化

**六个版本里唯一一次「复制基线 + 增量合并」**——不重新生成整包，而是先 `cp -a` 一份完整的 v0.4 当基线，再往上打补丁。v0.4 基线 **35/35 全部保留**。

补丁做了三件事：

1. **恢复**在 v0.3→v0.4 丢失的 2 个文件：`references/tracing/exploration-policy.md`、`knowledge-sources/README.md`
2. **覆写** `SKILL.md`（插入渐进执行闸门、Core-vs-Extensions 边界、`## Evolution` 里补上「非回归不变量」）与 `README.md`
3. **新增** 11 个文件，核心是：
   - `references/execution-progressive.md`——Gate 0~6 + L0~L3 渐进深度 + 反过度设计
   - `references/extension-boundary.md`——Core / Extensions / Knowledge sources / Evolution 四层边界
   - `evolution/baseline-policy.md`——**合并式演进（merge, not rewrite）；删任何东西必须留 reason / replacement / regression evidence**
   - `evolution/capability-inventory.md`、`evolution/approved-removals.yaml`
   - `templates/capability-inventory.yaml`、`templates/evolution-change.yaml`
   - `examples/progressive-execution-example.md`（用 PostgreSQL Buffer Lookup 走一遍闸门）
   - `CHANGELOG.md`、`EVOLUTION_AUDIT.md`
   - 之后又追加 `evolution/v0.4-baseline-manifest.yaml`（35 个基线文件的 SHA-256）、`evolution/approved-changes.yaml`（白名单：`SKILL.md` / `README.md` / `knowledge-sources/README.md`）、`tests/test_skill_integrity.py`（SHA-256 比对 + 白名单）

## 目录

| 路径 | 内容 |
|---|---|
| `skill/` | 技能包文件树（50 个文件，可直接阅读） |
| `source.zip` | 原始 zip（权威字节，勿改） |
| `conversation/` | 对话材料：`conversation.md` 逐轮全文 · `raw-data.json` 页面内嵌数据 · `snapshot.html` 页面快照 |

## 备注

- frontmatter 仍是从 v0.4 继承的 `description: >-`，仍过不了官方校验器——**这一版修了能力回归，却没碰这个从 v0.1 就存在的描述符问题**，说明它确实是一次「只解决被指出问题」的最小增量修复。
- 本版对话中有 **102 条**工具回显被 ChatGPT 抹掉（`redacted`），是六个版本里最多的。
- 立项依据见 [`../../docs/evolution-audit.md`](../../docs/evolution-audit.md)。
