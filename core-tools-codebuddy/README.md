# agent-alchemy-core-tools（CodeBuddy 版）

把 [`sequenzia/agent-alchemy`](https://github.com/sequenzia/agent-alchemy) 的 `core-tools` 插件移植到 CodeBuddy。

**按版本聚合**：一版一个目录，进去就能看全；`plugin/` 与 `source.zip` 是同一份内容的两种形态。

| 项 | 内容 |
|---|---|
| 上游 | `agent-alchemy-core-tools` v0.2.3 ｜ commit `fc1a336b`（2026-05-31） |
| 上游原样镜像 | [`../external-skills/agent-alchemy-marketplace/core-tools/`](../external-skills/agent-alchemy-marketplace/core-tools/)（只读基线，零改写） |
| License | MIT（版权归 Stephen Sequenzia） |
| 插件名 | `agent-alchemy-core-tools`（沿用上游，保持跨插件引用一致） |

---

## 一、版本谱系

| 版本 | 上游版本 | 主题 | 状态 | 包指纹 |
|---|---|---|---|---|
| [`v0.2.3-cb.1`](versions/v0.2.3-cb.1/) | `0.2.3` | 首次移植为 CodeBuddy 插件（全功能：skill + agent + command + hook） | **冻结基准** | `10b4ab24ed67f3b34424eaa8ab313bab` |

> `-cb.N` 中的 `N` 只在**上游版本不变、本产物需修订**时递增；上游版本变化时改为 `<新上游版本>-cb.1`。
> 旧版本目录**不再原地修改** —— 校准靠的是"基准不变"，改动一律进新版本目录。

## 二、目录约定

```
core-tools-codebuddy/
├── README.md                      ← 本文件（容器说明：版本谱系、安装、校准）
├── docs/
│   └── CONVERSION.md              ← 跨版本的转换规则：上游→CodeBuddy 映射表 + 上游同步清单
└── versions/
    └── v0.2.3-cb.1/               ← 一个版本一个目录
        ├── README.md                本版说明：主题、包内构成、改动概览
        ├── PROVENANCE.md            逐文件 md5、与上游对照、包指纹（权威记录）
        ├── source.zip               plugin/ 的权威打包存档
        ├── verify.sh                一键校准脚本
        └── plugin/                  ← **交付产物**（CodeBuddy 插件本体，安装这个目录）
            ├── .codebuddy-plugin/plugin.json
            ├── commands/            3 个斜杠命令
            ├── skills/              6 个 skill
            ├── agents/              4 个 agent
            └── hooks/               1 个 PreToolUse hook
```

## 三、安装

### 方式 A：作为插件安装（推荐，全功能）

```bash
PLUGIN=/home/zhq/mydisk/myskill/core-tools-codebuddy/versions/v0.2.3-cb.1/plugin
MKT="$HOME/.codebuddy/plugins/marketplaces/agent-alchemy-local"

# 1. 放入本地市场
mkdir -p "$MKT/plugins" "$MKT/.codebuddy-plugin"
cp -r "$PLUGIN" "$MKT/plugins/agent-alchemy-core-tools"

# 2. 写市场注册表
cat > "$MKT/.codebuddy-plugin/marketplace.json" <<'JSON'
{
  "name": "agent-alchemy-local",
  "description": "本地插件市场",
  "owner": { "name": "local" },
  "plugins": [
    {
      "name": "agent-alchemy-core-tools",
      "description": "代码库分析、多智能体深度探索、交互式访谈（agent-alchemy core-tools 的 CodeBuddy 移植版）",
      "version": "0.2.3-cb.1",
      "source": "./plugins/agent-alchemy-core-tools",
      "license": "MIT"
    }
  ]
}
JSON
```

3. 在 `~/.codebuddy/settings.json` 的 `enabledPlugins` 中加入（保留已有条目，不要整份覆盖）：

```json
{
  "enabledPlugins": {
    "agent-alchemy-core-tools@agent-alchemy-local": true
  }
}
```

然后重启 CodeBuddy。

> 如果 CodeBuddy IDE 提供「添加本地市场 / 从目录安装插件」的界面入口，直接用界面更稳妥 —— 由 IDE 写注册表可避免手写格式差异。以上步骤是按本机已装市场的磁盘结构复刻的。

### 方式 B：只装 skill（退化：无 agent、无 hook）

```bash
cp -r /home/zhq/mydisk/myskill/core-tools-codebuddy/versions/v0.2.3-cb.1/plugin/skills/* ~/.codebuddy/skills/
```

⚠️ 本机 `~/.codebuddy/skills/` 已有一个早前安装的 `codebase-analysis`（上游同名 skill 的旧副本）。安装前先移走，否则命名冲突：

```bash
mv ~/.codebuddy/skills/codebase-analysis ~/.codebuddy/skills/codebase-analysis.bak
```

方式 B 下 `deep-analysis` 会因缺少 `code-explorer` / `code-synthesizer` 子代理而无法组队 —— agent 定义只能靠方式 A 获得。

### hook 依赖

`hooks/auto-approve-da-session.sh` 用 `jq` 解析输入；未安装时静默 `exit 0`（等于"无意见"），退化为正常审批流，**不会阻断执行**：

```bash
sudo dnf install -y jq   # 或 apt-get install -y jq
```

## 四、使用

| 入口 | 作用 |
|---|---|
| `/deep-analysis [上下文或焦点区]` | 6 阶段深读：侦察 → 动态规划 → 评审审批 → 组队 → 并行探索 → 综合；结束归档会话并解散团队 |
| `/codebase-analysis [上下文]` | 3 阶段：深读 → 出报告（含 Mermaid 架构图）→ 后续动作（存报告／更新文档／处理可执行洞察） |
| `/interview-me [主题或上下文文件]` | 自适应访谈（三档深度、主动研究、模板产出），最终落盘 markdown 报告 |

6 个 skill 的 `description` 含中英双语触发词，模型会在相关语境下自动加载；`language-patterns` / `project-conventions` / `technical-diagrams` 属"被加载型"知识库，由上述流程与 4 个 agent 引用。`code-architect` 也可被其他插件（如 dev-tools 的 `feature-dev`）复用。

## 五、配置：`.codebuddy/agent-alchemy.local.md`

放在**项目根目录**（上游读的是 `.claude/agent-alchemy.local.md`）；文件不存在时全部走默认值。

```markdown
## agent-alchemy 配置

- **deep-analysis**:
  - **direct-invocation-approval**: true     # 用户直接 /deep-analysis 时，团队计划是否需人工批准（默认 true）
  - **invocation-by-skill-approval**: false  # 被其他 skill 调用时是否批准（默认 false = 自动批准）
  - **cache-ttl-hours**: 24                  # 探索缓存有效期；0 = 关闭缓存
  - **enable-checkpointing**: true           # 是否逐阶段写 checkpoint（支持中断恢复）
  - **enable-progress-indicators**: true     # 是否显示 [Phase N/6]

- **interview-me**:
  - **default-depth**: detailed              # overview | detailed | deep-dive
  - **default-output-type**: report-detailed # report-detailed | report-summary | implementation-plan | something-else
  - **output-directory**: internal/interviews/
  - **proactive-research-budget**: 3         # 0 = 关闭主动研究
  - **enable-context-argument**: true
  - **slug-collision-strategy**: timestamp-suffix  # timestamp-suffix | prompt
```

运行时产物写入项目内 `.codebuddy/sessions/`：

| 路径 | 内容 |
|---|---|
| `.codebuddy/sessions/__da_live__/` | 进行中会话：`checkpoint.md`、`team_plan.md`、`recon_summary.md`、`explorer-{N}-findings.md`、`progress.md`、`synthesis.md` |
| `.codebuddy/sessions/exploration-cache/` | 探索缓存（`manifest.md` + `synthesis.md` + `recon_summary.md`），按 TTL 复用 |
| `.codebuddy/sessions/da-{timestamp}/` | 已完成会话归档 |
| `.codebuddy/sessions/da-interrupted-{timestamp}/` | 中断后选"重新开始"时的归档 |

## 六、校准与上游同步

**校准**（校验基准本体、存档、上游基线、改造幅度四项）：

```bash
bash core-tools-codebuddy/versions/v0.2.3-cb.1/verify.sh
```

**改产物的正确姿势**：不要原地改 `versions/v0.2.3-cb.1/plugin/` —— 那会让基准失效。
新建 `versions/v0.2.3-cb.2/`（上游版本未变时递增 `cb.N`），把改动后的 `plugin/` 放进去，并按模板补 `README.md`、`PROVENANCE.md`、`source.zip`、`verify.sh`。

**上游更新时**：重下上游 → `diff -rq` 定位变更 → 按 [`docs/CONVERSION.md`](docs/CONVERSION.md) 第二节映射表逐类重放改动 → 新版本号改为 `<新上游版本>-cb.1`。
具体命令见 [`docs/CONVERSION.md`](docs/CONVERSION.md) 第七节。

## 七、已知注意事项

1. **不修改上游镜像** —— `../external-skills/agent-alchemy-marketplace/` 是只读基线；本产物是独立目录，便于 `diff` 与校准。
2. **可选依赖 Context7 MCP** —— 仅 `interview-me` 的主动研究使用，缺失时自动退回 Web/搜索。
3. **`${CODEBUDDY_PLUGIN_ROOT}` 兜底** —— 若运行时不展开该变量，`skills/` 与 `agents/` 内已写明用 Glob 定位或按 skill 本地 `references/` 相对路径读取。
4. **`AGENTS.md`** 在上游是"agent 清单文档"的更新目标之一，本版保留该行为；`CLAUDE.md` 已改为 `CODEBUDDY.md`。
