# codebase-reading

**外部来源、本机在用的 skill**：以目标 / 一条执行流为入口的体系化理解方法，产出五件套文档。

## 是什么

| 项 | 内容 |
|---|---|
| 干什么 | **以目标 / 一条执行流为入口，体系化理解**并成稿，产出五件套：`README`（索引与进度）/ `code-reading`（方法论 + 发现 + 术语表）/ `architecture`（C4 架构图，正文展开 L1–L3）/ `api-flow`（执行流追踪）/ `key-modules`（模块详析） |
| 怎么干 | **目标先行**：先定一个具体目的（改 bug / 加功能 / 安全审计）再读；成功标准是「能讲清执行流、能放心改代码」，不是读完每个文件 |
| 定位 | **体系化理解方法**：以目标 / 一条执行流为入口，理解过程本身由它支撑，五件套是产物；**不做全覆盖、不强制行号**；深度到模块级，函数级细节用 `deep-read` |
| 包内 | `skill/SKILL.md` + `skill/references/`（`methodology.md`、`terminology-building.md`、`tool-checklist.md`） |

## 能力（精确描述）

**一句话**：**以目标 / 一条执行流为入口的体系化理解方法**——理解过程本身由它支撑，五件套是产物；不做全覆盖、不强制行号；深度止于模块级，函数级细节交给 `deep-read`。

四层深度阶梯：`repo-wiki-authoring`（地图）→ **本 skill（体系化理解 + 成稿）** → `/deep-analysis`（模块级精读，团队并行）→ `deep-read`（函数 / 语句级取证）。

### 工作机制（`SKILL.md` Quick Start + `references/methodology.md` 11 步）

| # | 环节 | 实质 |
|---|---|---|
| 1 | 定目标 | 一句话目标（改 bug / 加功能 / 安全审计）；拒绝「理解整个代码库」 |
| 2 | **先跑起来** | 读 README / CONTRIBUTING → 构建 → 跑一个测试或示例；running code transforms reading from **guessing to verification** |
| 3 | 画 C4 粗图 | L1 Context / L2 Containers / L3 Components；只要够导航，不求好看 |
| 4 | 追**一条**真实链路 | Web / Async / CLI-Batch 三类模式；推荐 debugger + 断点 + 日志实走一遍 |
| 5 | 测试当可执行文档 | 读测试理解行为；没测试先写 **characterization tests** 记录现状再改 |
| 6 | Git 考古 | `git blame` / `log` / PR 讨论 —— 回答「为什么这么写」 |
| 7 | 读 PR / code review | 借助他人的背景与取舍说明，加速理解意图与回滚方式 |
| 8 | 工具清单 | `references/tool-checklist.md` |
| 9 | **术语表** | 从第一天起增量维护，不是事后补 |
| 10 | 模块深潜按优先级 | 核心 / 支撑 / 辅助三级，不全会读 |
| 11 | 下一步行动 | 哪些要懂、哪些能改、怎么验证 |

### 产出：固定五件套（`code-reading/`）

`README.md`（索引与进度）· `code-reading.md`（方法论 + 发现 + 术语表）· `architecture.md`（C4）· `api-flow.md`（执行流）· `key-modules.md`（模块详析），并明确**渐进披露**——专门文档按需加载。

### 内置实战资产

- **`references/tool-checklist.md`**（479 行）：ripgrep / git grep / IDE 检索；`git blame|log|bisect|follow` 考古；按语言（Rust / Python / JS-TS / Go）的构建 / 测试 / lint / doc / 依赖命令；调试器与 profiler、日志 tracing、静态与依赖分析；「找入口 / 找函数 / 找类定义 / 找 TODO」速查。
- **`references/terminology-building.md`**（429 行）：术语表 **5 步法**（初采 → 深挖 → 分类 → 富化上下文 → 维护）、按域与抽象层级分类、与架构图 / `api-flow` / 模块分析 / 测试交叉引用、反模式与校验清单。条目含定义 / 用途 / 上下文 / 代码引用 / 关系 / 示例 / 缩写展开。

### 能力边界

- **证据强度**：结论以结构化描述为主，`文件:行号` 是 when helpful、**不强制**（对比 `deep-read`：每条必须锚行号）。
- **范围控制**：靠「目标 + 优先级」**软控制**，**没有文件数闸门**（对比 `deep-read`：< 50 文件硬闸）。
- **不做运行时分析**：流程建议你跑起来、下断点，但 skill 自身不做执行与性能验证。
- **不做设计取舍**：只做阅读理解与成稿，不出架构决策建议。
- **案例偏 OCR**：术语与示例大量取自 OCR 项目（Detection / Recognition / CLS / CTC / NMS、坐标系）；工具清单覆盖 Rust / Python / JS-TS / Go。
- **内部小不一致**：文档结构注释写 `architecture.md` 为 C4 Level 1-4，正文只定义到 Level 3。

## 来源与本地改动

- 从本机安装位 `~/.codebuddy/skills/codebase-reading/` 回收的副本
- **上游未定位**：在上游 `agent-alchemy` 全仓（含 `agent-tools/`、`ported/`）按目录名与全文检索均无命中，无原件可比
- **本地改动（2 处，均在 `description`）**：追加中文触发词（上游只有英文触发词）；追加末尾一行定位句
- **已修复（2026-09-20）**：`description` 末尾原有的本地定位句曾把本 skill 说成「只做成稿、不适用于从陌生库起步」，与本体**冲突**——英文 `description` 首条用途即 "Understanding a new or unfamiliar codebase quickly"，正文 Quick Start 就是从陌生库起步。已改写为「定位是目标驱动的阅读方法论 + 成稿骨架：管『怎么读』与『按什么结构写』」，并回灌 `~/.codebuddy/skills/codebase-reading/`（`diff -rq` 无输出）

## 维护

`skill/` 就是安装形态，改完回灌安装位：

```bash
cp -r skills/codebase-reading/skill/. ~/.codebuddy/skills/codebase-reading/
diff -rq skills/codebase-reading/skill ~/.codebuddy/skills/codebase-reading   # → 无输出
```
