# 改造产物溯源与基线指纹 (PROVENANCE)

> 本文件是 **`v0.3.4-cb.1` 冻结基准**的权威记录，用于日后校准：上游更新后重跑改造，与本基准比对即可定位差异。
> 本文件位于 `plugin/` **之外**，因此**不参与**包指纹计算（规避「把自身 md5 写进自身」的自引用问题）。

## 一、权威坐标

| 项 | 值 |
|---|---|
| **上游仓库** | `https://github.com/sequenzia/agent-alchemy` |
| **上游作者** | Stephen Sequenzia (sequenzia@gmail.com) |
| **上游许可证** | MIT |
| **上游插件名** | `agent-alchemy-dev-tools` |
| **上游插件版本** | `0.3.4` |
| **上游包内路径** | `claude/dev-tools/` |
| **上游 commit** | `fc1a336b8267e70579af8517d14718e626824e54`（2026-05-31） |
| **本地上游镜像** | [`../../../../external-skills/agent-alchemy-marketplace/dev-tools/`](../../../../external-skills/agent-alchemy-marketplace/dev-tools/)（25 文件，零改写） |
| **上游包指纹** | `a9c9403919c7a3154afc000922a2f00b` |
| **本产物版本** | **`0.3.4-cb.1`**（`<上游版本>-cb.<改造修订号>`） |
| **本产物目标平台** | CodeBuddy（CodeBuddy 插件体系） |
| **本产物包指纹** | **`b2fd971573a6b02078c6bb5e3edb5323`** |
| **改造日期** | 2026-09-20 |
| **转换规则全文** | [`../../docs/CONVERSION.md`](../../docs/CONVERSION.md) |

## 二、版本号约定

| 位置 | 字段 | 含义 |
|---|---|---|
| `plugin/.codebuddy-plugin/plugin.json` | `version` | **产物版本**，权威 = `0.3.4-cb.1` |
| `plugin/skills/*/SKILL.md` | `version` | **上游来源版本** = `0.3.4`，仅作溯源；上游技能原本无此字段，为改造时补入 |

`-cb.N` 中的 `N` 只在**上游版本不变、而本产物需修订**时递增；上游版本变化时改为 `<新上游版本>-cb.1`。

## 三、逐文件对照（本产物 → 上游）

`md5` 为本产物文件的值；与上游关系分三类：**逐字节一致** / **已改写** / **本产物新增**。

| 本产物文件 | md5 | 与上游关系 |
|---|---|---|
| `.codebuddy-plugin/plugin.json` | `b5b0a7f05dece66d2ab5a4b815f96736` | 本产物新增 |
| `README.md` | `ffd708a73769d5e77bfc4305538033fc` | 已改写（换成本产物的使用手册，替换上游同名说明） |
| `agents/bug-investigator.md` | `e975b2198ed9c2f12167ec39c8563a12` | 已改写 |
| `agents/changelog-manager.md` | `0ba7fb116183fa84f9cd1085cb1c32cf` | 已改写 |
| `agents/code-reviewer.md` | `ed6e1b64bd58fc38f7410dc8331de6b7` | 已改写 |
| `agents/docs-writer.md` | `2343236778b8e3d7d59132350e16d06f` | 已改写 |
| `commands/bug-killer.md` | `85739fa27cdd0b28834d91b02f547684` | 本产物新增（上游 `user-invocable` skill 的 command 化） |
| `commands/docs-manager.md` | `a572192331b0575fb0262fe2b93f1e3a` | 本产物新增 |
| `commands/document-changes.md` | `dcbff91802ed32c0aa35b1bec313ca22` | 本产物新增 |
| `commands/feature-dev.md` | `119791d55a3a8e97badb805273ed4f44` | 本产物新增 |
| `commands/release-python-package.md` | `09c2fbc371f678b5903756e8632d802a` | 本产物新增 |
| `skills/architecture-patterns/SKILL.md` | `53945d2fd1e9292677873e2709af5f4e` | 已改写 |
| `skills/bug-killer/SKILL.md` | `d02591b1905bf816e511a0f80c4f4f74` | 已改写 |
| `skills/bug-killer/references/general-debugging.md` | `93c0d0702b4294ae984570959fe38613` | 逐字节一致 |
| `skills/bug-killer/references/python-debugging.md` | `74243a5e65bf58cb8d77c59832ee5e9c` | 逐字节一致 |
| `skills/bug-killer/references/typescript-debugging.md` | `d09d31010c4db5909d24a49603514223` | 逐字节一致 |
| `skills/changelog-format/SKILL.md` | `9588b7fb62e994c74fb56d776db07957` | 已改写 |
| `skills/changelog-format/references/entry-examples.md` | `41a9648af8b5bca179d3be76d72ba7fb` | 逐字节一致 |
| `skills/code-quality/SKILL.md` | `7e92d2f6f7fcbbfade954b739577898f` | 已改写 |
| `skills/docs-manager/SKILL.md` | `a29f3de5da350d8a74f5786bdb19d83a` | 已改写 |
| `skills/docs-manager/references/change-summary-templates.md` | `34c68dfe43770a077b44be68a846a5f4` | 逐字节一致 |
| `skills/docs-manager/references/markdown-file-templates.md` | `7d10a19c16f3ca6b8d3ae969a43eaae8` | 逐字节一致 |
| `skills/docs-manager/references/mkdocs-config-template.md` | `067f55f8fb2c0fd31bf5ff054d0c8614` | 逐字节一致 |
| `skills/document-changes/SKILL.md` | `6ac0936f1f5cc4a9a671abf78c836dae` | 已改写 |
| `skills/feature-dev/SKILL.md` | `967e50b2657dcef61e75af756e5b13eb` | 已改写 |
| `skills/feature-dev/references/adr-template.md` | `932adac42626f6ba37dc42869f797064` | 逐字节一致 |
| `skills/feature-dev/references/changelog-entry-template.md` | `90fe6663ddad8509b1662da3bc26440b` | 逐字节一致 |
| `skills/project-learnings/SKILL.md` | `5a41a46bca7a82c88718c498d4a8ec76` | 已改写 |
| `skills/release-python-package/SKILL.md` | `377bb82a72b398a3f5d22386eba04ae5` | 已改写 |

**计数**：逐字节一致 **9** ｜ 已改写 **14** ｜ 本产物新增 **6** ｜ 合计 **29**。

**未移植 2 项**：`hooks/hooks.json`、`hooks/resolve-cross-plugins.sh`（Claude Code 插件缓存布局的短名符号链接机制，CodeBuddy 平铺市场不需要；详见 CONVERSION 第五节）。

上游 25 个文件中，**23 个有对应**（`hooks/hooks.json`、`hooks/resolve-cross-plugins.sh` 不在内）；
`README.md` 路径相同但内容已换成本产物的使用手册，故计入「已改写」。校验：23 = 逐字节一致 9 + 已改写 14。

## 四、完整性校验

### 1. 包指纹

算法（**只覆盖 `plugin/`，不含本文件与 `source.zip`**，故无自引用问题）：

```bash
cd versions/v0.3.4-cb.1/plugin
find . -type f | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32
# → b2fd971573a6b02078c6bb5e3edb5323
```

> `LC_ALL=C` 不可省：不同 locale 的 `sort` 排序不同，换环境会算出不同指纹。

### 2. 上游基线

```bash
cd ../../../../external-skills/agent-alchemy-marketplace/dev-tools
find . -type f ! -name PROVENANCE.md | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32
# → a9c9403919c7a3154afc000922a2f00b（应等于顶层 README 记录的 dev-tools 指纹）
```

### 3. 一键校准

```bash
bash versions/v0.3.4-cb.1/verify.sh
```
