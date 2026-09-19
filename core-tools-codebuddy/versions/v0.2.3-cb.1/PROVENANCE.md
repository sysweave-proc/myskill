# 改造产物溯源与基线指纹 (PROVENANCE)

> 本文件是 **`v0.2.3-cb.1` 冻结基准**的权威记录，用于日后校准：上游更新后重跑改造，与本基准比对即可定位差异。
> 本文件位于 `plugin/` **之外**，因此**不参与**包指纹计算（上游那版 PROVENANCE.md 把自身 md5 写进自身，属自引用，本产物规避了该问题）。

## 一、权威坐标

| 项 | 值 |
|---|---|
| **上游仓库** | `https://github.com/sequenzia/agent-alchemy` |
| **上游作者** | Stephen Sequenzia (sequenzia@gmail.com) |
| **上游许可证** | MIT |
| **上游插件名** | `agent-alchemy-core-tools` |
| **上游插件版本** | `0.2.3` |
| **上游包内路径** | `claude/core-tools/` |
| **上游 commit** | `fc1a336b8267e70579af8517d14718e626824e54`（2026-05-31） |
| **本地上游镜像** | [`../../../external-skills/agent-alchemy-marketplace/core-tools/`](../../../external-skills/agent-alchemy-marketplace/core-tools/)（26 文件，零改写） |
| **上游包指纹** | `808192241ec2c53ced9bd83227279279` |
| **本产物版本** | **`0.2.3-cb.1`**（`<上游版本>-cb.<改造修订号>`） |
| **本产物目标平台** | CodeBuddy（CodeBuddy Code 插件体系） |
| **本产物包指纹** | **`2a25c41b8b418c0e1b1967053412d66e`** |
| **改造日期** | 2026-09-19 |
| **转换规则全文** | [`../../docs/CONVERSION.md`](../../docs/CONVERSION.md) |

## 二、版本号约定

| 位置 | 字段 | 含义 |
|---|---|---|
| `plugin/.codebuddy-plugin/plugin.json` | `version` | **产物版本**，权威 = `0.2.3-cb.1` |
| `plugin/skills/*/SKILL.md` | `version` | **上游来源版本** = `0.2.3`，仅作溯源；上游技能原本无此字段，为改造时补入 |

`-cb.N` 中的 `N` 只在**上游版本不变、而本产物需修订**时递增；上游版本变化时改为 `<新上游版本>-cb.1`。

## 三、逐文件对照（本产物 → 上游）

`md5` 为本产物文件的值；与上游关系分三类：**逐字节一致** / **已改写** / **本产物新增**。

| 本产物文件 | md5 | 与上游关系 |
|---|---|---|
| `.codebuddy-plugin/plugin.json` | `e9eea71d149367055a4ea63adb679878` | 本产物新增 |
| `README.md` | `576e80961b82fe5d5311195db7a00645` | 已改写（本产物的使用手册，替换上游同名说明） |
| `agents/code-architect.md` | `8a0cc9c4f0b68ea4800c29f370954e3a` | 已改写 |
| `agents/code-explorer.md` | `8123c3ac81e4b338c18151223bf37a3a` | 已改写 |
| `agents/code-synthesizer.md` | `b52e0f268c68c16357687ea7bf2b6ef6` | 已改写 |
| `agents/interview-researcher.md` | `c304961985902192a9b745e23097c691` | 已改写 |
| `commands/codebase-analysis.md` | `6ba90ba952e833317e0d20066d50a6d6` | 本产物新增 |
| `commands/deep-analysis.md` | `760d289e3a81d632ba12d01b0144f5e0` | 本产物新增 |
| `commands/interview-me.md` | `d9a35db664e9b4446fc6758a7a3a2064` | 本产物新增 |
| `hooks/auto-approve-da-session.sh` | `fdca7948aa6e0627266f6b490010dfdd` | 已改写 |
| `hooks/hooks.json` | `66b53ce68273e7e6b39dfd5377277d27` | 已改写 |
| `skills/codebase-analysis/SKILL.md` | `8612ea43cf3157f43ce6a2d19af1431a` | 已改写 |
| `skills/codebase-analysis/references/actionable-insights-template.md` | `0c707187f260ea3bd8c56a4e75ef0330` | 已改写 |
| `skills/codebase-analysis/references/report-template.md` | `97d339eb24238bc2413f3fcde49183aa` | 逐字节一致 |
| `skills/deep-analysis/SKILL.md` | `17e779d166777743fded49c02bf023d7` | 已改写 |
| `skills/interview-me/SKILL.md` | `8f5b14d90be7bfe8d7799c5e852d42e1` | 已改写 |
| `skills/interview-me/references/question-bank.md` | `0bf3888c6ba6a71ae246f98eb1a92c1f` | 逐字节一致 |
| `skills/interview-me/references/research-triggers.md` | `dcbeee15bfd22a090981738a5f671183` | 逐字节一致 |
| `skills/interview-me/references/templates/implementation-plan.md` | `41ba795003aede8151870f0dbdc7966e` | 逐字节一致 |
| `skills/interview-me/references/templates/report-detailed.md` | `9ad0f02ae0295330ff3b8a6fa7226514` | 逐字节一致 |
| `skills/interview-me/references/templates/report-summary.md` | `d294c0d3b44da6ea682d9b9614990533` | 逐字节一致 |
| `skills/language-patterns/SKILL.md` | `3b05593d24375b19fd2ab33e973c98a0` | 已改写 |
| `skills/project-conventions/SKILL.md` | `aa8967c0f3118f6708fedcb66093c9a3` | 已改写 |
| `skills/technical-diagrams/SKILL.md` | `87c0119d6f8708dad0067faead8510e1` | 已改写 |
| `skills/technical-diagrams/references/c4-diagrams.md` | `97c7ee027324a90558045bc7f7ddbeaf` | 逐字节一致 |
| `skills/technical-diagrams/references/class-diagrams.md` | `2e2bafd51924a820f6d06ca59800d420` | 逐字节一致 |
| `skills/technical-diagrams/references/er-diagrams.md` | `877dd8b0b83649b724551f3c28359565` | 逐字节一致 |
| `skills/technical-diagrams/references/flowcharts.md` | `a77e92266bd1701bb900df9c4f51df93` | 逐字节一致 |
| `skills/technical-diagrams/references/sequence-diagrams.md` | `604ee672520557967d097e60659f04f4` | 逐字节一致 |
| `skills/technical-diagrams/references/state-diagrams.md` | `4ec3c45abf0874316def0430f177977c` | 逐字节一致 |

**计数**：逐字节一致 **12** ｜ 已改写 **14** ｜ 本产物新增 **4** ｜ 合计 **30**。

上游 26 个文件**全部有对应，无未移植项**。其中 `README.md` 路径相同但内容已换成本产物的**使用手册**，故计入「已改写」；上游那份面向 Claude 侧的 skill/agent 清单不再保留。

## 四、完整性校验

### 1. 包指纹

算法（**只覆盖 `plugin/`，不含本文件与 `source.zip`**，故无自引用问题）：

```bash
cd versions/v0.2.3-cb.1/plugin \
  && find . -type f | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32
```

结果应为：

```
2a25c41b8b418c0e1b1967053412d66e
```

> ⚠️ `LC_ALL=C` 不可省 —— 否则排序随 locale 变化，换环境算出的值不同（上游仓 README 曾因此作废五个历史指纹值）。

### 2. 存档件

| 文件 | 说明 | md5 |
|---|---|---|
| `source.zip` | `plugin/` 的权威打包（30 文件） | `cff8f4e02048a665a6be947d65e0c3ad` |

> `zip` 会写入时间戳，**重新打包得到不同 md5 属正常**。因此校验以「解包后内容指纹 == `2a25c41b8b418c0e1b1967053412d66e`」为准，不以 zip 自身 md5 为准。

### 3. 文件计数

```
plugin/ 内文件: 30
本版目录内文件: 34  = plugin/ 30 + README.md + PROVENANCE.md + source.zip + verify.sh
```

## 五、复核与校准命令

一键校准（推荐）：

```bash
bash versions/v0.2.3-cb.1/verify.sh
```

手工复核（在 `core-tools-codebuddy/` 目录下执行；其中 C 项改为在仓库根目录执行）：

```bash
# A. 基准本体是否被改动
cd versions/v0.2.3-cb.1/plugin && find . -type f | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32
#    → 应输出 2a25c41b8b418c0e1b1967053412d66e

# B. 存档与本体是否一致
mkdir -p /tmp/zipcheck && unzip -qo versions/v0.2.3-cb.1/source.zip -d /tmp/zipcheck \
  && (cd /tmp/zipcheck/plugin && find . -type f | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32)

# C. 上游基线是否仍与记录一致（在仓库根目录 /home/zhq/mydisk/myskill 执行）
cd external-skills/agent-alchemy-marketplace/core-tools \
  && find . -type f ! -name PROVENANCE.md | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32
#    → 应输出 808192241ec2c53ced9bd83227279279

# D. 改造幅度复算（12 / 14 / 4）
#    见 verify.sh 的第 3 项输出
```

## 六、校验结论

- `plugin/` 30 个文件中，**12 个与上游逐字节一致**（`references/` 参考库与模板中的 12 份），**14 个按需求改写**，**4 个为新增**（插件清单 + 3 个斜杠命令）；上游 26 个文件全部有对应，**无未移植项**。
- 改写**未触及任何流程逻辑** —— `deep-analysis` 的 6 阶段、团队原语（`TeamCreate` / `TaskCreate` / `SendMessage`）、任务依赖与状态守卫、断点续传、缓存 TTL、错误降级矩阵、Mermaid 参考库均原样继承。逐项依据见 [`../../docs/CONVERSION.md`](../../docs/CONVERSION.md)。
- 因此本基准可作为**后续改造的校准锚点**：任何对产物的改动都应反映为本文件指纹的变更，并记录到下一版版本目录。

## 七、修订记录（重新冻结）

本基准在 2026-09-19 首次冻结后共做过 **2 次修订**，均**就地重新冻结**（未另立 `v0.2.3-cb.2`）：

- **修订 1** —— 核查 CodeBuddy 生态的**真实调用签名**时发现两处保真缺陷（见下表）。
- **修订 2** —— 按用户要求新增**使用手册** `README.md`（同路径替换上游那份面向 Claude 侧的说明），组件本体零改动。

| # | 缺陷 | 证据 | 修正 |
|---|---|---|---|
| 1 | agent 引用沿用了 Claude 的带插件前缀写法 `agent-alchemy-core-tools:<agent>`（共 4 处：`codebase-analysis/SKILL.md` ×2、`codebase-analysis/references/actionable-insights-template.md` ×2） | 全生态实测 `subagent_type` 取值**均为裸名**（`bg-scan` / `python-pro` / `ml-engineer` / `general-purpose` / `fork` …），无一处带插件前缀；官方 `plugin-dev` 文档亦写明「Single plugin: `agent-name`」 | 改为裸名 `code-architect` / `code-explorer` |
| 2 | 派队友只传 `team_name`，未显式传 `name` | CodeBuddy 生态的建队流程显式传 `name:` + `team_name:` + `max_turns:`（`ardot-design-generator`）；`security-scan` 亦以裸名 `subagent_type` 调度 | `deep-analysis` Phase 3 改为显式传 `name`；「Agent Coordination」补一条约定 |

**修订史**（旧值均不可再复现，保留仅作对照；哈希为便于阅读做了截断）：

| 修订 | 内容 | 包指纹（前 → 后） | `source.zip`（前 → 后） | 改造幅度（前 → 后） |
|---|---|---|---|---|
| 1 | agent 引用去插件前缀（4 处）；派队友补显式 `name` | `10b4ab24…3bab` → `e69d8497…4b1c` | `a0b9fd29…f0ca` → `664c172a…e0f6` | 13 / 12 / 4 → 12 / 13 / 4 |
| 2 | 新增使用手册 `README.md` | `e69d8497…4b1c` → `2a25c41b…d66e` | `664c172a…e0f6` → `cff8f4e0…c3ad` | 12 / 13 / 4 → **12 / 14 / 4** |

**残留不确定点**（未被证伪，但也无拼写级证据，已做软化处理，非遗漏）：

| 点 | 现状 | 处理 |
|---|---|---|
| `TaskUpdate` 的依赖字段名（上游写 `addBlockedBy`） | CodeBuddy 生态确有「共享任务列表 + 指派 + blocked by」语义（`ardot-design-generator` 工作流在用），但**未找到参数拼写级证据** | `deep-analysis` 第 3 步已加括注：若该字段名不同，用运行时的等价依赖字段表达 |
| 团队工具名的呈现 | 生态文档里称 `Agent` 工具（ardot）、`Task(subagent_type: ...)`（security-scan）；参数 `name` / `team_name` / `max_turns` 一致 | 保留上游 "Task tool" 措辞；语义与参数已核对一致 |
