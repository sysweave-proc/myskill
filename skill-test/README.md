# skill-test（外部 skill 实测区）

**用真实源码库实测新装 skill 的产物暂存区** —— 产出物是笔记，不是 skill 资产，因此不进顶层的资产总览。

## 实测配置

| 项 | 值 |
|---|---|
| 日期 | 2026-09-19 |
| 被测源码库 | `/home/zhq/mydisk/github/postgres` |
| 版本 | PostgreSQL 19beta2（版本判定依据 `configure.ac:20`） |
| 参与 skill | `codebase-analysis`（出地图）、`deep-read`（出地形）、手写骨架 |

实测时为避免语义重叠互相抢自动触发，自建的同类 skill 曾被临时移出 `~/.codebuddy/skills/`。被测的三个外部 skill 中，`codebase-reading` / `deep-read` 现在 [`../skills/`](../skills/) 下，`codebase-analysis` 已删除（它只是插件内部的一个 skill）。

## 产物

| 产物 | 说明 |
|---|---|
| [`postgres-notes/`](postgres-notes/) | PostgreSQL 源码阅读笔记库，两条主线共 6 篇；入口见其 `README.md` |

## 已知缺口（下一轮可追）

- `postgres-notes/process-memory/01` 引用的 **`00` 篇总览不存在**；该篇的子线编号为 `C1/C2/C3`，暗示存在 `A/B/C…` 字母主线体系，但 `A`/`B` 无迹可寻。属**待补，不臆造**。
- 6 篇均为 skill 原始产出，**篇头块与元数据尚未按 `source-notes-authoring` 规范统一**，「还账」类过程产物仍内嵌在正文各节。
