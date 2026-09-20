# 改造产物溯源与基线指纹 (PROVENANCE)

> 本文件是 **`v0.2.1-cb.1` 冻结基准**的权威记录，用于日后校准：上游更新后重跑改造，与本基准比对即可定位差异。
> 本文件位于 `plugin/` **之外**，因此**不参与**包指纹计算（规避「把自身 md5 写进自身」的自引用问题）。

## 一、权威坐标

| 项 | 值 |
|---|---|
| **上游仓库** | `https://github.com/sequenzia/agent-alchemy` |
| **上游作者** | Stephen Sequenzia (sequenzia@gmail.com) |
| **上游许可证** | MIT |
| **上游插件名** | `agent-alchemy-tdd-tools` |
| **上游插件版本** | `0.2.1` |
| **上游包内路径** | `claude/tdd-tools/` |
| **上游 commit** | `fc1a336b8267e70579af8517d14718e626824e54`（2026-05-31） |
| **本地上游镜像** | [`../../../../external-skills/agent-alchemy-marketplace/tdd-tools/`](../../../../external-skills/agent-alchemy-marketplace/tdd-tools/)（21 文件，零改写） |
| **上游包指纹** | `fcfafcbfd6d2b114663a85675b0648a6` |
| **本产物版本** | **`0.2.1-cb.1`**（`<上游版本>-cb.<改造修订号>`） |
| **本产物目标平台** | CodeBuddy（CodeBuddy 插件体系） |
| **本产物包指纹** | **`9a3e892b6b6deb735d87164667592cfa`** |
| **改造日期** | 2026-09-20 |
| **转换规则全文** | [`../../docs/CONVERSION.md`](../../docs/CONVERSION.md) |

## 二、版本号约定

| 位置 | 字段 | 含义 |
|---|---|---|
| `plugin/.codebuddy-plugin/plugin.json` | `version` | **产物版本**，权威 = `0.2.1-cb.1` |
| `plugin/skills/*/SKILL.md` | `version` | **上游来源版本** = `0.2.1`，仅作溯源；上游技能原本无此字段，为改造时补入 |

`-cb.N` 中的 `N` 只在**上游版本不变、而本产物需修订**时递增；上游版本变化时改为 `<新上游版本>-cb.1`。

## 三、逐文件对照（本产物 → 上游）

`md5` 为本产物文件的值；与上游关系分三类：**逐字节一致** / **已改写** / **本产物新增**。

| 本产物文件 | md5 | 与上游关系 |
|---|---|---|
| `.codebuddy-plugin/plugin.json` | `2856f8dc6f569157bd84fefe8b2b38cb` | 本产物新增 |
| `README.md` | `91303fa9c9c487548f398e40e5f6f2d6` | 已改写（换成本产物的使用手册） |
| `agents/tdd-executor.md` | `781c59b5277e911c2261045caa14fd9e` | 已改写 |
| `agents/test-reviewer.md` | `64e389a401ca2bd99e1faa55129ed8a2` | 已改写 |
| `agents/test-writer.md` | `1f3607f663a8dc1af8e09e344c4657b1` | 已改写 |
| `commands/analyze-coverage.md` | `786bee3494f684f11fe59b7a4aa9ac3d` | 本产物新增 |
| `commands/create-tdd-tasks.md` | `c413d100b3c7432a53be53e681a51a42` | 本产物新增 |
| `commands/execute-tdd-tasks.md` | `f844be13c95867ce62e3d1ca6fe5ce89` | 本产物新增 |
| `commands/generate-tests.md` | `0f3ca22ffba1c9da80c37dc9d16e29f6` | 本产物新增 |
| `commands/tdd-cycle.md` | `536220ca1af84dd6788e8f905b4578db` | 本产物新增 |
| `hooks/auto-approve-session.sh` | `1a5c0d79f33f47d672563578b2b3651d` | 已改写 |
| `hooks/hooks.json` | `7ba2590a4b5bfcbdba7afd3836d0d984` | 已改写（删除 SessionStart 建链条目） |
| `skills/analyze-coverage/SKILL.md` | `0addd5e844a52378a7a95e07f9635d6e` | 已改写 |
| `skills/analyze-coverage/references/coverage-patterns.md` | `28751283ad3cee41eefe7c08c1ad1823` | 已改写 |
| `skills/create-tdd-tasks/SKILL.md` | `9b82639fb325a714537fbf052a53b9ed` | 已改写 |
| `skills/create-tdd-tasks/references/tdd-decomposition-patterns.md` | `89398a483d04d27d6d2b94910278155b` | 逐字节一致 |
| `skills/create-tdd-tasks/references/tdd-dependency-rules.md` | `20460e2f6716099e39cf662e4f142517` | 逐字节一致 |
| `skills/execute-tdd-tasks/SKILL.md` | `94bae53b88490de1cec3bc15fc01eb4a` | 已改写 |
| `skills/execute-tdd-tasks/references/tdd-execution-workflow.md` | `d4853187032bb3cd341de3bbc1fd0d51` | 已改写 |
| `skills/execute-tdd-tasks/references/tdd-verification-patterns.md` | `75db4492726dba8d485cd8338fc5e3c9` | 逐字节一致 |
| `skills/generate-tests/SKILL.md` | `e7e693cc381c25940d82d20585c7d423` | 已改写 |
| `skills/generate-tests/references/framework-templates.md` | `f849fe7e09cd40fbdbe7b6856184cdcf` | 已改写 |
| `skills/generate-tests/references/test-patterns.md` | `a56ab30ac34f97d8719622540c2e050c` | 逐字节一致 |
| `skills/tdd-cycle/SKILL.md` | `c036a887ab8e92989ead26a1944bbe46` | 已改写 |
| `skills/tdd-cycle/references/tdd-workflow.md` | `6638b57f8d2b5e7a270d9588149241d5` | 已改写 |
| `skills/tdd-cycle/references/test-rubric.md` | `d53f8bc8e66b64050e8e8596d7699755` | 已改写 |

**计数**：逐字节一致 **4** ｜ 已改写 **16** ｜ 本产物新增 **6** ｜ 合计 **26**。

**未移植 1 项**：`hooks/resolve-cross-plugins.sh`（Claude Code 插件缓存布局的短名符号链接机制，CodeBuddy 平铺市场不需要；详见 CONVERSION 第五节）。因此 `hooks/hooks.json` 也随之删掉了 `SessionStart` 条目，只保留 `PreToolUse`。

上游 21 个文件中 **20 个有对应**（= 逐字节一致 4 + 已改写 16）；`README.md` 路径相同但内容已换成使用手册，故计入「已改写」。

## 四、完整性校验

### 1. 包指纹

算法（**只覆盖 `plugin/`，不含本文件与 `source.zip`**，故无自引用问题）：

```bash
cd versions/v0.2.1-cb.1/plugin
find . -type f | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32
# → 9a3e892b6b6deb735d87164667592cfa
```

> `LC_ALL=C` 不可省：不同 locale 的 `sort` 排序不同，换环境会算出不同指纹。

### 2. 上游基线

```bash
cd ../../../../external-skills/agent-alchemy-marketplace/tdd-tools
find . -type f ! -name PROVENANCE.md | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32
# → fcfafcbfd6d2b114663a85675b0648a6（应等于顶层 README 记录的 tdd-tools 指纹）
```

### 3. 一键校准

```bash
bash versions/v0.2.1-cb.1/verify.sh
```
