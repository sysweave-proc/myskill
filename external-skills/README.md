# external-skills · 上游市场镜像留档

> ⚠️ **这里的资产不是本仓资产。** 本目录只放**未改动的上游原文**，用于离线比对与上游更新追踪，不由本仓维护、不参与运行。
> 分工：**实际在用的 skill 在顶层 [`skills/`](../skills/)**（可改、带回灌安装位的方法）；**本目录是留档**（只读，必须与上游一致）。

## 里面是什么

上游 [`sequenzia/agent-alchemy`](https://github.com/sequenzia/agent-alchemy)（MIT · Stephen Sequenzia）的**整包镜像**，也是仓根 `plugins/` 下 5 个移植包的上游比对基线。

```
external-skills/
├── README.md                              本文件
└── agent-alchemy-marketplace/             上游市场镜像（5 插件 + 注册表）
    ├── README.md                          （本地文档：市场总览、逐个插件详解、版本对照表）
    ├── .claude-plugin/marketplace.json    市场注册表（版本号的 source of truth）
    └── core-tools/  claude-tools/  sdd-tools/  tdd-tools/  dev-tools/
```

| 基线项 | 值 |
|---|---|
| 基准 commit | `fc1a336b8267e70579af8517d14718e626824e54`（上游日期 2026-05-31） |
| 归档日期 | 2026-09-19 |
| 状态 | 归档当日与上游逐文件零差异；**之后没有自动机制**，是否过期只能人工查（见下） |

**判别口径**：根下是 `agents/` + `hooks/` + `skills/` 三件套 = **插件包**，不是 skill，而是 skill 的容器，不能当 skill 安装。
市场共 9 个插件，这里只归档 5 个 + 注册表；未收录的 3 个（`opencode-tools` / `cs-tools` / `git-tools`）理由见市场 README。

## 怎么知道它过期了

上游不会通知本仓，需要人工**对版本号**。基准版本见 [市场镜像 README · 版本对照表](agent-alchemy-marketplace/README.md)。

```bash
curl -sSL "https://raw.githubusercontent.com/sequenzia/agent-alchemy/main/.claude-plugin/marketplace.json" \
  | python3 -c "import sys,json; [print(p['name'], p.get('version')) for p in json.load(sys.stdin)['plugins']]"
```

任一插件版本号与对照表不一致 → 上游已更新，重下对应包目录替换，并更新上表的**基准 commit、归档日期、状态**。

> **版本号有盲区**：上游可能改了内容却不提版本号（基准 commit 那条 `docs(skills): …` 就动了 `core-tools` 的 `technical-diagrams` 和 `dev-tools` 的 `docs-manager`，是否伴随版本号变更无法从本地判断）。要补这个漏，多跑一行 commit 哨兵，与上文「基准 commit」比对：
>
> ```bash
> curl -sS https://api.github.com/repos/sequenzia/agent-alchemy/commits/main \
>   | python3 -c "import sys,json;print(json.load(sys.stdin)['sha'])"
> ```

**本地有没有被误改**：本目录已纳入 git，`git status` / `git diff` 就是最准确的漂移检测——内容改动、**以及可执行位的变化**都会出现在 `git diff` 里，所以不需要另存指纹。

## 使用须知

**两条硬规则**，改了就会坏：

1. **不给上游目录改名** —— 上游包无 `plugin.json`，Claude Code 按目录名推导插件名；改名会让 `插件名:agent` 这类引用失配。
2. **包内结构一律原样** —— `skills/` / `agents/` / `hooks/` 是插件规范的默认发现位置，改名即全部扫不到。

**已知的 2 处本地偏差**（都是结构性差异，被镜像的内容全为原样）：

| # | 位置 | 偏差 | 说明 |
|---|---|---|---|
| 1 | `core-tools/PROVENANCE.md` | 本地新增，上游无 | 溯源记录。故对 `core-tools/` 做 `diff -rq` 会**稳定地多出这 1 行**，属预期，不是污染 |
| 2 | `.claude-plugin/` | 比上游少一层 | 上游路径是 `<repo>/.claude-plugin/marketplace.json`；镜像拍平了上游的 `claude/` 一层，引用时按「镜像根」理解 |
