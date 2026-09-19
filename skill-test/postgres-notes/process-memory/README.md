# 主线 C · 进程与内存模型

> 一句话定位：**一个 `postgres` 进程从 `main()` 走到「能被别人唤醒」的全过程**——进程怎么生、内存在哪放、多进程靠什么互相看见。
> 一句话总结：**postmaster 把所有全局结构建好，子进程靠 `fork` 继承；进程的「存在」与「可见」是两件事，前者靠 `PGPROC`，后者靠 `ProcArray`。**
> 使用方式：`01` 是站点图，先读它拿地图；`02` → `03` → `04` 是按依赖链排的逐行精读（地基 → 唯一出口 → 交汇点），可顺序读，也可按需跳。

- 源码：`/home/zhq/mydisk/github/postgres`（PostgreSQL 19beta2）
- 建立时间：2026-09-19
- 篇数：4

---

## 1. 篇索引

| 篇 | 内容 | 对应问题 |
| --- | --- | --- |
| [`01`](01-进程与内存模型-骨架.md) | 三条子线（**C1 进程模型 / C2 内存模型 / C3 共享内存**）的站点图与三处工程点 | 从 `main()` 到一个可服务的后端，入口链上各站点落在哪？ |
| [`02`](02-逐行-MemoryContextInit.md) | `MemoryContextInit()` 逐行——内存体系的唯一地基（37 行） | 内存上下文体系的地基怎么打？为什么 `ErrorContext` 必须**最后**建？ |
| [`03`](03-逐行-fork_process.md) | `fork_process()` 逐行——整个多进程模型的唯一出口（95 行） | 一次 fork 要处理哪些固有陷阱？「解除信号屏蔽」这笔欠账由谁还？ |
| [`04`](04-逐行-InitProcess.md) | `InitProcess()` 逐行——**C1 与 C3 的交汇点**（182 行） | 一个进程如何从「操作系统进程」变成「数据库进程」？ |

## 2. 全景图

```
main() ───────────── 一条进程的三段路 ─────────────
  │
  ├─ C2 内存模型    MemoryContextInit()                      mcxt.c
  │                    └─ TopMemoryContext → CurrentMemoryContext → ErrorContext
  │                       地基：先有「能报错」的能力，才敢做后面的事
  │
  ├─ C1 进程模型    PostmasterMain() → ServerLoop() → postmaster_child_launch()
  │                    └─ fork_process()                     fork_process.c
  │                         清缓冲 + 屏蔽信号 + 刷新 pid + 卸 OOM 保护
  │                         └─ InitProcess()                 proc.c      ← C1 × C3 交汇
  │                               └─ InitProcessPhase2()     procarray.c  「可见」
  │
  └─ C3 共享内存    CreateSharedMemoryAndSemaphores() / ShmemInitStruct()
                       └─ 由 InitProcess() 登记 PGPROC，共享内存才「感知到」这个进程
```

## 3. 关键文件表

| 文件 | 职责 |
| --- | --- |
| `src/backend/utils/mmgr/mcxt.c` | 内存上下文基类与 `MemoryContextInit()` |
| `src/backend/utils/mmgr/README` | 内存上下文官方设计说明（528 行，强烈建议原样读一遍） |
| `src/backend/postmaster/fork_process.c` | `fork()` 的唯一包装 |
| `src/backend/postmaster/postmaster.c` | 服务端主进程、主循环与子进程启动 |
| `src/backend/storage/lmgr/proc.c` | `PGPROC` 的登记（`InitProcess`）与注销（`ProcKill`） |
| `src/backend/storage/ipc/ipci.c`、`shmem.c` | 共享内存创建与按名注册 |
| `src/backend/storage/ipc/procarray.c` | `ProcArrayAdd`——「可见」的实现 |

## 4. 与相邻主题的边界

| 本类管什么 | 隔壁管什么 |
| --- | --- |
| 进程诞生链、内存上下文体系、`PGPROC` 登记与可见性 | 元组表示与生命周期 → [`../tuple/`](../tuple/)；查询处理与前后端协议 → 尚未建 |

## 5. 缺口

| 缺口 | 依据 | 状态 |
| --- | --- | --- |
| **本类缺 `00` 总览篇** | `01` 篇两处引用它（`00 篇 §4`、`00 篇 §5`），且引用内容（`tcop/postgres.c:1195-1204`）在现有素材中查无此处 | 待补，不臆造 |
| 子线字母体系不完整 | `01` 篇用 `C1/C2/C3` 标子线，说明主线有 `A/B/C…` 字母标签，但 `A`/`B` 无迹可寻 | 待查 |
| 各篇内的「核对结果」章节尚未外移 | `01 §5`、`02 §5`、`03 §5`、`04 §6` 各自挂着还账记录 | 下一轮处理 |

## 6. 阅读建议

1. **先读 `01`**——它是唯一一篇「站点走通」深度，给出全局坐标；后面的逐行篇都靠它定位。
2. **`02` → `03` → `04` 是按依赖链排的**：地基（内存）→ 唯一出口（fork）→ 交汇点（登记）。`04` 篇开头明说它是 `01` 篇标注的「C1 与 C3 的交汇点」。
3. **注意篇与篇之间的接缝**：`03` 篇设的 `MyProcPid`，在 `04` 篇被写进共享内存；`04` 篇的「交出本地 latch 换共享 latch」是「能被唤醒」的分界点——这些接缝是这条主线最值钱的部分。
