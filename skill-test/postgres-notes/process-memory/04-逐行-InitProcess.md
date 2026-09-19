# PostgreSQL 源码笔记 · 04 逐行精读：InitProcess()

- 位置：`src/backend/storage/lmgr/proc.c:388-573`（函数体 `:392-573`，共 182 行）
- 所属主线：C 进程与内存模型（**C1 进程模型 × C3 共享内存的交汇点**）
- 定位：一个后端进程**从「操作系统进程」变成「数据库进程」**的那一刻
- 建立时间：2026-09-19

---

## 1. 为什么读这个函数

`01` 篇把 `InitProcess()` 标为「C1 与 C3 的交汇点」，这一定位在函数头注释（`proc.c:388-390`）里得到确认：

> `InitProcess` -- initialize a per-process PGPROC entry for this backend

它做的事很简单：**从共享内存的 free list 里取一个 `PGPROC` 槽位，初始化它，并把自己登记进去。**

但它是必须逐行读的，因为三种问题正好都挤在这里：

1. **进程模型** —— 进程如何获得「数据库身份」（不是 pid，而是 `PGPROC` 槽位）
2. **共享内存** —— 多进程如何安全地分配/回收共享槽位
3. **两者之间的耦合不变量** —— 哪一步之前不能做什么，答错了就是并发 bug

---

## 2. 前置：`PGPROC` 是什么

看结构体注释（`src/include/storage/proc.h:156-183`）：

> Each backend has a PGPROC struct in shared memory. There is also a list of currently-unused PGPROC structs that will be reallocated to new backends.
>
> Note: twophase.c also sets up a **dummy PGPROC struct for each currently prepared transaction**. ... A prepared transaction PGPROC can be distinguished from a real one at need by the fact that it has **pid == 0**.

三个要点：

- `PGPROC` **住在共享内存里**，所以它是「别的进程能看见你」的载体。
- 它同时是**可回收资源**：有一个 free list 供新后端取用（`InitProcess` 就是来取它的）。
- 它还被**借用**来表示两阶段提交的已准备事务——这种「假进程」靠 `pid == 0` 区分。

结构体字段按块分组（`proc.h:195-385`），与 `InitProcess` 的初始化代码**一一对应**：

| 分组 | 位置 | 关键字段 |
| --- | --- | --- |
| 后端身份 | `:195-218` | `pid` `backendType` `databaseId` `roleId` `statusFlags` |
| 事务与快照 | `:220-255` | `vxid` `xid` `xmin` `subxids` |
| 进程间发信号 | `:258-276` | `procLatch` `sem` `pendingRecoveryConflicts` |
| LWLock 等待 | `:278-294` | `lwWaiting` `lwWaitMode` |
| 锁管理器数据 | `:296-335` | `waitLock` `myProcLocks[]` `fpLockBits` |
| 同步复制等待 | `:337-349` | `waitLSN` `syncRepState` |
| 组 XID 清除 | `:351-364` | `procArrayGroupMember` |
| 组事务状态更新 | `:366-378` | `clogGroupMember` |
| 状态上报 | `:380-384` | `wait_event_info` |

两个值得先记住的机制：

**① cache line 对齐防伪共享**（`proc.h:186-190`）：

```c
/*
 * Align the struct at cache line boundaries.  This is just for
 * performance, to avoid false sharing.
 */
alignas(PG_CACHE_LINE_SIZE)
```

**② 「镜像字段」**（`proc.h:173-182`）：部分字段会被镜像到更紧凑的 `ProcGlobal` 数组里，
下标是 `PGPROC->pgxactoff`，**两份副本必须保持一致**。
而注释特别强调：

> NB: The pgxactoff indexed value can *never* be accessed without holding locks.

这是理解后面那些 `locks` 操作的前提。

---

## 3. 逐行注解

### 段 A：两个前置断言（`:394-404`）

```c
394: 	dlist_head *procgloballist;
395:
396: 	/*
397: 	 * ProcGlobal should be set up already (if we are a backend, we inherit
398: 	 * this by fork() or EXEC_BACKEND mechanism from the postmaster).
399: 	 */
400: 	if (ProcGlobal == NULL)
401: 		elog(PANIC, "proc header uninitialized");
402:
403: 	if (MyProc != NULL)
404: 		elog(ERROR, "you already exist");
```

**注意两个错误级别不同，这是刻意的：**

| 条件 | 级别 | 理由 |
| --- | --- | --- |
| `ProcGlobal == NULL` | **PANIC** | 共享内存头都没建好，整个实例状态不可信，无法安全继续 |
| `MyProc != NULL` | **ERROR** | 只是「我这个进程重复初始化了」，属于可恢复的局部错误 |

注释 `:397-398` 还顺带交代了共享内存的继承方式：**后端不是自己建的 `ProcGlobal`，
而是从 postmaster 那里通过 `fork()`（普通模式）或 `EXEC_BACKEND` 机制继承来的**。
这与 `02` 篇 `MemoryContextInit` 的继承模型完全一致——
**postmaster 把所有全局结构建好，子进程继承**，这是 PG 多进程架构的统一范式。

### 段 B：先「报到」，再动共享内存（`:406-412`）

```c
406: 	/*
407: 	 * Before we start accessing the shared memory in a serious way, mark
408: 	 * ourselves as an active postmaster child; this is so that the postmaster
409: 	 * can detect it if we exit without cleaning up.
410: 	 */
411: 	if (IsUnderPostmaster)
412: 		RegisterPostmasterChildActive();
```

这一段的顺序意识很强：**在「认真访问共享内存」之前**先向 postmaster 报到。
理由是让 postmaster 有能力检测「子进程没清理干净就退出了」。

`IsUnderPostmaster` 的判断则说明这个函数也服务于**非 fork 场景**
（单用户模式、bootstrap），那时没有 postmaster 需要报到。

> 可迁移的教训：**在开始可能失败的工作之前，先让自己处于「可被监督」的状态。**
> 这样失败时监督者才能区分「正常结束」和「异常死亡」。

### 段 C：按进程类型选 free list（`:414-425`）

```c
414: 	/*
415: 	 * Decide which list should supply our PGPROC.  This logic must match the
416: 	 * way the freelists were constructed in ProcGlobalShmemInit().
417: 	 */
418: 	if (AmAutoVacuumWorkerProcess() || AmSpecialWorkerProcess())
419: 		procgloballist = &ProcGlobal->autovacFreeProcs;
420: 	else if (AmBackgroundWorkerProcess())
421: 		procgloballist = &ProcGlobal->bgworkerFreeProcs;
422: 	else if (AmWalSenderProcess())
423: 		procgloballist = &ProcGlobal->walsenderFreeProcs;
424: 	else
425: 		procgloballist = &ProcGlobal->freeProcs;
```

**注释 `:415-416` 是整个函数最该划重点的一句：**

> This logic must match the way the freelists were constructed in `ProcGlobalShmemInit()`.

这是一条**跨文件的隐式契约**：这里的「选哪个 list」必须和 `ProcGlobalShmemInit()` 里
「怎么造这些 list」严格对应。两处不一致 → 槽位被还到错误的 list → 资源池错乱。

而这种耦合**编译器帮不上忙**（两处都是普通的 if-else），所以作者把它写成了注释警告。

> 这是本函数最脆弱的一处。读这类代码时，凡是看到「must match」「keep in sync」这类注释，
> 都要意识到：**这里没有机制保证，只有纪律。**

四类进程各有专属池，缺省落 `freeProcs`（普通后端）。

### 段 D：加锁取槽位，并「顺手」学一个参数（`:427-461`）

```c
427: 	/*
428: 	 * Try to get a proc struct from the appropriate free list.  If this
429: 	 * fails, we must be out of PGPROC structures (not to mention semaphores).
430: 	 *
431: 	 * While we are holding the spinlock, also copy the current shared
432: 	 * estimate of spins_per_delay to local storage.
433: 	 */
434: 	SpinLockAcquire(&ProcGlobal->freeProcsLock);
435:
436: 	set_spins_per_delay(ProcGlobal->spins_per_delay);
437:
438: 	if (!dlist_is_empty(procgloballist))
439: 	{
440: 		MyProc = dlist_container(PGPROC, freeProcsLink, dlist_pop_head_node(procgloballist));
441: 		SpinLockRelease(&ProcGlobal->freeProcsLock);
442: 	}
443: 	else
444: 	{
...
451: 		SpinLockRelease(&ProcGlobal->freeProcsLock);
452: 		if (AmWalSenderProcess())
453: 			ereport(FATAL,
454: 					(errcode(ERRCODE_TOO_MANY_CONNECTIONS),
455: 					 errmsg("number of requested standby connections exceeds \"max_wal_senders\" (currently %d)",
456: 							max_wal_senders)));
457: 		ereport(FATAL,
458: 				(errcode(ERRCODE_TOO_MANY_CONNECTIONS),
459: 				 errmsg("sorry, too many clients already")));
460: 	}
```

**四个要点：**

**① 四类 free list 共用一把锁。** 注意锁是 `ProcGlobal->freeProcsLock`，
不是 `procgloballist` 自带的锁——**所有池子用同一把自旋锁保护**。
这样实现简单（不用管锁的归属），代价是不同池的分配会互相争抢。

**② 「顺手」拷贝 `spins_per_delay`（`:436`）—— 搭便车的优化。**
注释 `:431-432` 明说：既然已经持有这把自旋锁，就把共享的自旋延迟估计值拷到本地。
一次临界区做两件事，省掉一次独立的同步。

这行的存在本身就说明一件事：**自旋锁临界区是稀缺资源，值得「顺便」把能做的都做掉。**

> `spins_per_delay` 是 PG 的自适应自旋调节参数——自旋多久才让出 CPU，由历史表现动态估算。
> 之所以要「共享估算、本地使用」，是因为自旋发生在没有共享内存访问的紧循环里，
> 每次都去共享内存读会抵消自旋的意义。

**③ `dlist_container` 从链表节点反推出宿主结构体**（`:440`）：

```c
MyProc = dlist_container(PGPROC, freeProcsLink, dlist_pop_head_node(procgloballist));
```

`freeProcsLink` 是 `PGPROC` 内嵌的链表节点（`proc.h:192-193`）。
宏定义在 `src/include/lib/ilist.h:587-596`：

```c
/*
 * Return the containing struct of 'type' where 'membername' is the dlist_node
 * pointed at by 'ptr'.
 *
 * This is used to convert a dlist_node * back to its containing struct.
 */
#define dlist_container(type, membername, ptr)								\
	(StaticAssertVariableIsOfTypeMacro(ptr, dlist_node *),						\
	 StaticAssertVariableIsOfTypeMacro(((type *) NULL)->membername, dlist_node),	\
	 ((type *) ((char *) (ptr) - offsetof(type, membername))))
```

三部分各司其职：

| 部分 | 作用 |
| --- | --- |
| 第 1 条静态断言 | 编译期确认 `ptr` 真的是 `dlist_node *` |
| 第 2 条静态断言 | 编译期确认 `type` 里确实有个名叫 `membername` 的 `dlist_node` 字段 |
| 表达式 | 节点地址**减去 `offsetof(type, membername)`**，还原宿主结构体的起始地址 |

**所以运行时开销是零**（`offsetof` 与指针减法都在编译期折叠），
**而类型写错会在编译期被挡住**——两条 `StaticAssertVariableIsOfTypeMacro` 是纯赚的。

这属于**侵入式链表**（intrusive list）的经典取舍：
`PGPROC` 不必为「被挂进 free list」额外分配节点，链表指针直接嵌在结构体里。
代价是**一个对象同一时刻只能挂在一个链表上**——所以 `PGPROC` 里有多个链表节点字段
（`freeProcsLink`、`waitLink`、`syncRepLinks`、`lockGroupLink`…），各管一摊。

**④ 池子空了 → `FATAL`，而且两个 `ereport` 没有 `else`（`:452-459`）。**
先给 walsender 一条更具体的错误消息（提到 `max_wal_senders`），再兜底通用的
`sorry, too many clients already`（这句是 PG 用户最眼熟的报错之一）。

注意这里**不需要写 `else`**，因为 `ereport(FATAL, ...)` 永不返回。
这是 PG 代码里的常见写法，但读的时候要意识到：
**控制流没有真的"继续往下"，是靠 FATAL 的长跳转语义中断的。**

顺带：注释 `:428-429` 说拿不到槽位就等于「`PGPROC` 用完了（更别说信号量了）」——
因为 `PGPROC` 和信号量是配套分配的（见 `:550` 的 `MyProc->sem`）。
这提示**槽位数量就是 `max_connections` 等参数落地成物理资源的地方**。

### 段 E：一致性校验与「谁负责初始化哪些字段」（`:461-532`）

```c
461: 	MyProcNumber = GetNumberFromPGProc(MyProc);
462:
463: 	/*
464: 	 * Cross-check that the PGPROC is of the type we expect; if this were not
465: 	 * the case, it would get returned to the wrong list.
466: 	 */
467: 	Assert(MyProc->procgloballist == procgloballist);
468:
469: 	/*
470: 	 * Initialize all fields of MyProc, except for those previously
471: 	 * initialized by ProcGlobalShmemInit.
472: 	 */
```

**`:461` 揭示了一套双重表示**：`PGPROC` 既用**指针**（`MyProc`）也用**编号**（`MyProcNumber`）标识。

为什么需要编号？因为共享内存里的数组要按整数下标索引（例如 `pgxactoff` 指向的镜像数组）。
指针在共享内存里跨进程有效，但**数组下标更紧凑、也便于做原子操作**（`proc.h:232-236` 说明
`vxid.procNumber` 对普通后端就等于 `GetNumberFromPGProc(proc)`，与 `:480` 的赋值互相印证）。

**`:467` 的 `Assert` 是对段 C 那条脆弱契约的运行时守卫**：
如果我取到的槽位不属于我预期的池子，将来释放时就会还错地方。
生产构建里 `Assert` 会被编译掉，所以**这只是开发期的安全带，不是运行时保证**——
再次印证「这里只有纪律」。

**`:469-471` 的注释划出了一条责任边界：**

| 谁初始化 | 哪些字段 |
| --- | --- |
| `ProcGlobalShmemInit()`（共享内存创建时，一次性） | 结构性字段，如 `procgloballist`、`pgxactoff`、`sem`、`fpLockBits`、`fpRelId` |
| **`InitProcess()`（本函数，每个进程一次）** | 所有「进程私有的、每轮复用都必须重置的」状态 |

这正是 `:473-532` 那一大段的性质：**不是「首次初始化」，而是「重置」**。
因为槽位是从 free list 取来的，可能是**上一个进程用过的**（甚至是崩溃进程留下的）。
看这些赋值全都是「回到无效值」：

```c
473: 	dlist_node_init(&MyProc->freeProcsLink);
474: 	MyProc->waitStatus = PROC_WAIT_STATUS_OK;
475: 	MyProc->fpVXIDLock = false;
476: 	MyProc->fpLocalTransactionId = InvalidLocalTransactionId;
477: 	MyProc->xid = InvalidTransactionId;
478: 	MyProc->xmin = InvalidTransactionId;
479: 	MyProc->pid = MyProcPid;
...
483: 	MyProc->databaseId = InvalidOid;    /* will be filled in later */
484: 	MyProc->roleId = InvalidOid;
```

**三处细节：**

- `:479 MyProc->pid = MyProcPid;` —— **`03` 篇的接缝在这里闭合**：
  `fork_process.c:70` 取到的 pid，此刻被发布进共享内存。
  从这一行起，其他进程才知道「这个槽位对应操作系统里的哪个进程」。
- `:482 databaseId and roleId will be filled in later` —— 这两个字段此刻还不知道，
  要等 `InitPostgres()` 连接上具体数据库后才填。
  **也就是说：`InitProcess()` 完成时，进程已「存在」但还不知道自己服务哪个库。**
- `:489-491`：
  ```c
  489: 	/* NB -- autovac launcher intentionally does not set IS_AUTOVACUUM */
  490: 	if (AmAutoVacuumWorkerProcess())
  491: 		MyProc->statusFlags |= PROC_IS_AUTOVACUUM;
  ```
  只有 autovacuum **worker** 打这个标记，**launcher 故意不打**。
  这类「故意不做什么」的注释往往是踩过坑之后补的，比「做了什么」更值得读。

- `:498-506` 在 `USE_ASSERT_CHECKING` 下断言 `myProcLocks[]` 全空：

  ```c
  /* Last process should have released all locks. */
  for (i = 0; i < NUM_LOCK_PARTITIONS; i++)
  	Assert(dlist_is_empty(&(MyProc->myProcLocks[i])));
  ```

  这是**对「上一个使用者」的交叉验证**。同一个断言在 `ProcKill()`
  （`proc.c:945-947`）也出现了一次——**进出两端各查一遍**，
  任何一端失衡都会被开发构建抓住。

### 段 F：交出自己的「睡眠权」——全函数最重要的一段（`:534-543`）

```c
534: 	/*
535: 	 * Acquire ownership of the PGPROC's latch, so that we can use WaitLatch
536: 	 * on it.  That allows us to repoint the process latch, which so far
537: 	 * points to process local one, to the shared one.
538: 	 */
539: 	OwnLatch(&MyProc->procLatch);
540: 	SwitchToSharedLatch();
541:
542: 	/* now that we have a proc, report wait events to shared memory */
543: 	pgstat_set_wait_event_storage(&MyProc->wait_event_info);
```

**这两行是「一个进程从私有变成可被唤醒」的分界点。**

先理清 `Latch` 的两种形态：

- **进程本地 latch**：每个进程最开始都有的一个 latch，**只有自己能等**，别人碰不到。
- **共享 latch**（`MyProc->procLatch`）：住在共享内存里，**任何持有指针的进程都能 signal 它**。

`OwnLatch()` 让我认领 `PGPROC` 里那个共享 latch；
`SwitchToSharedLatch()` 把全局的 `MyLatch` 从「本地那个」**重新指向**「共享那个」。

于是从这一行之后：

```
别的进程 signal(MyProc->procLatch)
   → 我这边正在 WaitLatch(MyLatch) —— 而 MyLatch 就是它
   → 我被唤醒 ✓
```

**在这一行之前，任何进程想唤醒我都是不可能的**，因为我不在共享内存里有任何「可被信号的东西」。

所以这短短两行改变的是进程的**可寻址性**：从这一刻起，
「等待锁」、「等待同步复制」、「等待 latch」这些跨进程协调才第一次成为可能。

紧跟着的 `:543` 又是同一件事的另一面：把等待事件的存放位置也切到共享内存，
这样 `pg_stat_activity` 之类的视图才能看到我**此刻卡在哪**。
两句合起来就是：**先让自己能被唤醒，再让自己能被看见。**

> 这两行是全篇最该记住的：它解释了为什么后面 `:561` 能立刻调 `InitLWLockAccess()`——
> 因为「等锁」依赖 latch，而 latch 刚刚才就绪。**顺序不是随手写的，是被依赖链锁死的。**

### 段 G：收尾——重置、登记清理、解锁链（`:545-572`）

```c
545: 	/*
546: 	 * We might be reusing a semaphore that belonged to a failed process. So
547: 	 * be careful and reinitialize its value here.  (This is not strictly
548: 	 * necessary anymore, but seems like a good idea for cleanliness.)
549: 	 */
550: 	PGSemaphoreReset(MyProc->sem);
551:
552: 	/*
553: 	 * Arrange to clean up at backend exit.
554: 	 */
555: 	on_shmem_exit(ProcKill, 0);
556:
557: 	/*
558: 	 * Now that we have a PGPROC, we could try to acquire locks, so initialize
559: 	 * local state needed for LWLocks, and the deadlock checker.
560: 	 */
561: 	InitLWLockAccess();
562: 	InitDeadLockChecking();
563:
564: #ifdef EXEC_BACKEND
...
570: 	if (IsUnderPostmaster)
571: 		AttachSharedMemoryStructs();
572: #endif
```

**① `:550` 重置信号量，理由是「槽位可能来自崩溃进程」。**
注释很诚实地承认 `This is not strictly necessary anymore`——
但仍然做了，因为「干净」比「省一次调用」重要。
**这里体现的是对「槽位复用」这个事实的持续警惕。**

**② `:555` 注册退出清理 —— 与 `ProcKill()` 配对。**
`on_shmem_exit(ProcKill, 0)` 把 `ProcKill`（`proc.c:924`）挂到共享内存退出回调上。
于是「取槽位」和「还槽位」被绑定成一对，**不可能只做一半**。

`ProcKill()` 里有个很说明问题的防御（`proc.c:934-936`）：

```c
/* not safe if forked by system(), etc. */
if (MyProc->pid != (int) getpid())
	elog(PANIC, "ProcKill() called in child process");
```

用 `MyProc->pid` 与当前 `getpid()` 比对——**而这正是 `:479` 刚写进去的值**。
换言之，段 E 写进去的 pid 除了给别人看，还承担了**自我身份校验**的功能。
这正是 `03` 篇留下的那个 fork 陷阱在这里的落地：如果进程被 `system()` 等意外 fork，
子进程退出时会走到同一套清理逻辑，靠这个断言立刻发现。

`ProcKill()` 里还有一句关于时序的注释（`proc.c:971-973`）值得一并记下：

> `DisownLatch()` must happen before our PGPROC can appear on a freelist: a newly-forked backend that pops our slot and calls `OwnLatch()` would PANIC on a still-owned latch.

即**归还顺序有硬约束**：必须先放弃 latch 的所有权，槽位才能回到 free list，
否则新后端取到槽位后 `OwnLatch()` 会因「latch 已被占有」而 PANIC。
段 F 的 `OwnLatch()` 和这里的 `DisownLatch()` 构成一对，中间夹着 `:435` 的加锁归还。

**③ `:561-562` 两个初始化放在最后，注释给了理由：**

> Now that we have a PGPROC, **we could try to acquire locks**

**「能取锁」是 `InitProcess` 之前与之后的分界线。** 而这两件事都依赖这个前提。

**④ `:570-571` EXEC_BACKEND 下的额外一步，理由同样在注释里：**

> (We couldn't do this until now because **it needs LWLocks**.)

即便在另一种构建模式下，约束也是同一条：**先有 `PGPROC`，才谈得上 LWLock，才谈得上挂接共享结构。**

---

## 4. 三阶段「诞生」：`InitProcess` 不是终点

`InitProcess()` 结束时，进程**还没完全活过来**。后面还有两步，都由代码里的注释明确交代：

```c
575: /*
576:  * InitProcessPhase2 -- make MyProc visible in the shared ProcArray.
577:  *
578:  * This is separate from InitProcess because we can't acquire LWLocks until
579:  * we've created a PGPROC, but in the EXEC_BACKEND case ProcArrayAdd won't
580:  * work until after we've done AttachSharedMemoryStructs.
581:  */
582: void
583: InitProcessPhase2(void)
584: {
585: 	Assert(MyProc != NULL);
590: 	ProcArrayAdd(MyProc);
595: 	on_shmem_exit(RemoveProcFromArray, 0);
596: }
```

**为什么要拆成两个函数？** 注释 `:578-580` 给出了纯技术原因：
`ProcArrayAdd` 需要 LWLock，LWLock 需要 `PGPROC`，
而 `PGPROC` 需要先 `AttachSharedMemoryStructs()`（仅 EXEC_BACKEND）。
**依赖链有分支，所以只能在代码层面拆开表达。**

于是完整的诞生是三步：

| 阶段 | 函数 | 由谁调用 | 进程状态 |
| --- | --- | --- | --- |
| 1 | `InitProcess()` | `BackendMain()` → `backend_startup.c:116` | 拿到槽位、有了身份、**能被信号唤醒了**——但别人在共享数据里还看不见我 |
| 2 | `InitProcessPhase2()` | `InitPostgres()` → `postinit.c:740` | `ProcArrayAdd` ——**进入 ProcArray，从此出现在别人的快照计算里** |
| 3 | `InitPostgres()` 后续 | 同上 | 填 `databaseId` / `roleId` ——**知道自己服务哪个库、以谁的身份** |

对照本函数 `:483` 的注释 `databaseId and roleId will be filled in later`，
这条链就闭合了。**「存在」和「可见」在 PG 里是两件事**，这个区分是理解并发行为的钥匙。

另外注意第 1 步的调用位置：`InitProcess()` 在 `PostgresMain()` **之前**执行
（`backend_startup.c:116` vs `:124`），而不是在 `PostgresMain()` 内部。
这与 §3 段 G 的结论互相印证：**主循环一开跑就需要取锁，所以 `PGPROC` 必须先就位。**

`ProcArrayAdd()` 的实际动作（`storage/ipc/procarray.c:463-...`）也验证了「可见」的含义：

```c
463: void
464: ProcArrayAdd(PGPROC *proc)
465: {
466: 	int			pgprocno = GetNumberFromPGProc(proc);
467: 	ProcArrayStruct *arrayP = procArray;
...
472: 	LWLockAcquire(ProcArrayLock, LW_EXCLUSIVE);
473: 	LWLockAcquire(XidGenLock, LW_EXCLUSIVE);
...
487: 	/*
488: 	 * Keep the procs array sorted by (PGPROC *) so that we can utilize
489: 	 * locality of references much better. ...
```

三个要点：

- **一次要拿两把 LWLock**（`ProcArrayLock` + `XidGenLock`），注释 `:471` 指向 `ProcGlobal` 处的说明。
- 数组**按 `PGPROC *` 指针值排序**以改善遍历时的缓存局部性（注释 `:487-494`）。
  这里又一次出现了「为性能做的、不显然的约定」。
- 还有一处 `sorry, too many clients already`（`:482-484`），
  与 `InitProcess` `:457-459` 那处重复。注释 `:478-480` 自己承认这是防御性的：

  > This really shouldn't happen, since there is a fixed supply of PGPROC structs too, and so we should have failed earlier.

  **即：因为 `PGPROC` 数量是死的，槽位用完在 `InitProcess` 就报错了，这里本不该触发。
  留着它是为了万一不变式被破坏时给出可定位的失败，而不是静默越界。**

---

## 5. 四个可迁移的设计要点

**① 用一把锁保护一个资源池族，并在临界区里「搭便车」**

`freeProcsLock` 保护全部四类 free list（`:434`），且在持锁期间顺手拷贝
`spins_per_delay`（`:436`）。前者是简化，后者是优化——
**临界区是稀缺资源，能合并的工作就合并。**

**② 资源来自复用池时，初始化的本质是「重置」**

`:469-532` 那一大段的性质不是「初始化」而是「清零上一个使用者留下的状态」，
所以注释专门点明「除了 `ProcGlobalShmemInit` 已经初始化过的那些」——
**必须清楚哪些字段是「一次性结构性」的、哪些是「每轮必须重置」的。**
`PGSemaphoreReset`（`:550`）是同一思路的另一种体现。

**③ 依赖链决定代码顺序，注释负责把顺序说清楚**

本函数里每一处顺序都非偶然，且**作者都写了注释**：

| 顺序 | 约束 | 注释位置 |
| --- | --- | --- |
| 先报到，再动共享内存 | 让 postmaster 能发现异常退出 | `:407-409` |
| 先 `OwnLatch`，才能 `InitLWLockAccess` | 等锁依赖 latch | `:535-538` / `:558-559` |
| 先 `PGPROC`，才能 `AttachSharedMemoryStructs` | 挂接共享结构需要 LWLock | `:567-568` |
| 先 `DisownLatch`，槽位才能回 free list | 否则新后端 `OwnLatch` 会 PANIC | `proc.c:971-973` |

**④ 跨文件契约靠注释而非机制**

`:415-416` 那句 `This logic must match the way the freelists were constructed in ProcGlobalShmemInit()`
是全篇最脆弱的地方。配套的 `:467 Assert` 只在开发构建里存在。
**读代码时看到这类注释，就该知道这是维护中的高风险区。**

---

## 6. 核对结果（原「遗留问题」已全部还清）

| 原问题 | 结论 | 位置 |
| --- | --- | --- |
| `ProcGlobalShmemInit()` 如何构造 free list | **契约成立**，但见 §6.1 的重要补充 | `proc.c:232-363` |
| `ProcKill()` 完整逻辑 | 已读完，见 §6.2 | `proc.c:924-1071` |
| `AmXxxProcess()` 宏 | 全是 `MyBackendType` 的比较 | `miscadmin.h:388-407` |
| `dlist_container` | 已补入 §3 段 D ③ | `ilist.h:587-596` |
| `spins_per_delay` 算法 | 指数移动平均 | `s_lock.c:218` |
| `ProcArrayAdd` 如何「可见」 | 已补入 §4 | `procarray.c:463-494` |

### 6.1 那条跨文件契约：**成立，但比注释描述的更微妙**

构造侧（`ProcGlobalShmemInit()`，`proc.c:336-359`）是按**数组下标区间**划分：

```c
336: 		if (i < MaxConnections)
339: 			dlist_push_tail(&ProcGlobal->freeProcs, &proc->freeProcsLink);
340: 			proc->procgloballist = &ProcGlobal->freeProcs;
342: 		else if (i < MaxConnections + autovacuum_worker_slots + NUM_SPECIAL_WORKER_PROCS)
345: 			dlist_push_tail(&ProcGlobal->autovacFreeProcs, &proc->freeProcsLink);
346: 			proc->procgloballist = &ProcGlobal->autovacFreeProcs;
348: 		else if (i < MaxConnections + autovacuum_worker_slots + NUM_SPECIAL_WORKER_PROCS + max_worker_processes)
351: 			dlist_push_tail(&ProcGlobal->bgworkerFreeProcs, &proc->freeProcsLink);
352: 			proc->procgloballist = &ProcGlobal->bgworkerFreeProcs;
354: 		else if (i < MaxBackends)
357: 			dlist_push_tail(&ProcGlobal->walsenderFreeProcs, &proc->freeProcsLink);
358: 			proc->procgloballist = &ProcGlobal->walsenderFreeProcs;
```

消费侧（`InitProcess:418-425`）是按**运行时进程类型**选择：

| 消费侧判断 | 目标 list | 构造侧区间 |
| --- | --- | --- |
| `AmAutoVacuumWorkerProcess() \|\| AmSpecialWorkerProcess()` | `autovacFreeProcs` | `[MaxConnections, +autovacuum_worker_slots+NUM_SPECIAL_WORKER_PROCS)` |
| `AmBackgroundWorkerProcess()` | `bgworkerFreeProcs` | `[…, +max_worker_processes)` |
| `AmWalSenderProcess()` | `walsenderFreeProcs` | `[…, MaxBackends)` |
| 其余 | `freeProcs` | `[0, MaxConnections)` |

**逐项对照，顺序与语义完全一致，契约成立。**

但这里有个注释没点破的关键差别：
**构造侧用「下标位置」决定归属，消费侧用「进程类型」决定归属。**
两者能对上，靠的是一条隐含前提——**下标区间必须按 `BackendType` 的用途来布局**。
换句话说，如果哪天调整了 `PGPROC` 数组的区间划分（比如把 walsender 挪到 autovac 前面），
构造侧改了、消费侧不改，`Assert(MyProc->procgloballist == procgloballist)`（`:467`）
在**开发构建**里会拦住你；**生产构建**里则不会有任何提示。

**这就是 §3 段 C 说「这里没有机制保证，只有纪律」的确切含义。**
契约成立，但它的保障强度取决于构建选项。

### 6.2 `ProcKill()` 的完整闭环（`proc.c:924-1071`）

把 §3 段 G 没读完的后半补全，归还路径是这样的：

| 步 | 动作 | 位置 |
| --- | --- | --- |
| 1 | 校验 `MyProc->pid != getpid()` → PANIC | `:934-936` |
| 2 | 离开 sync rep 队列、释放所有 LWLock | `:939`、`:956` |
| 3 | **`SwitchBackToLocalLatch()` + `DisownLatch()`** | `:981-982` |
| 4 | 解开锁组关系，决定 `push_leader` / `push_self` | `:997-1038` |
| 5 | `MyProc = NULL; MyProcNumber = INVALID_PROC_NUMBER;` | `:1043-1044` |
| 6 | **标记槽位不再使用**：`pid = 0`、`vxid.procNumber = INVALID_PROC_NUMBER` | `:1046-1049` |
| 7 | 加 `freeProcsLock`，把槽位推回各自的 `procgloballist` | `:1051-1065` |
| 8 | **更新共享的 `spins_per_delay` 估计值** | `:1067-1068` |

**四处值得单记：**

**① `:1047 proc->pid = 0;` 与 `proc.h:163-164` 的约定对上了。**
结构体注释说「已准备事务的 PGPROC 靠 `pid == 0` 区分」，
而这里正是「槽位被释放」的标记方式。**同一个哨兵值同时表示「无主」和「假进程」**——
因为对「谁在用这个槽位」这个问题，两者的答案都是「没有真实进程」。

**② 推回 free list 时 leader 和 self 用了不同端**（`:1055` vs `:1064`）：

```c
dlist_push_head(leader->procgloballist, &leader->freeProcsLink);   /* leader */
dlist_push_tail(procgloballist, &proc->freeProcsLink);             /* self   */
```

**头尾的区别是有意的**：leader 的槽位是被「顺带」归还的（最后一个 follower 退出时替它还），
而自己的槽位是正常归还。用不同端能避免「刚还回去就被立刻复用」——
不过注释没有解释这一点，属于**从代码能看出差异、但意图需要存疑**的地方。这里如实记录，不做断言。

**③ `:1040-1041` 的 `pgstat_reset_wait_event_storage()` 被刻意延后。**
`:975-979` 的注释说明了理由：要保证 `wait_event_info` 在我们的 `PGPROC` 槽位
「仍可能被观察到时」保持可见。这是「先保证可观测性，再做清理」的取舍。

**④ `spins_per_delay` 的读写配对闭合了。**
读在 `InitProcess:436`，写在 `ProcKill:1068`，算法在 `storage/lmgr/s_lock.c:218`：

```c
218: update_spins_per_delay(int shared_spins_per_delay)
219: {
220: 	/*
221: 	 * We use an exponential moving average with a relatively slow adaption
```

即**用指数移动平均缓慢自适应**。为什么要用共享值 + 本地副本这一对？
因为自旋发生在紧循环里，每次都读共享内存会抵消自旋本身的意义——
于是「进临界区时拷一次，出临界区时才更新一次」。

同一模式在 `InitAuxiliaryProcess:645` 和 `AuxiliaryProcKill:1118` 也重复出现，
说明这是 PG 里一条稳定的惯例。

### 6.3 `AmXxxProcess()` 宏：一行比较，但依赖一个全局量

`src/include/miscadmin.h:388-407`：

```c
388: #define AmAutoVacuumLauncherProcess() (MyBackendType == B_AUTOVAC_LAUNCHER)
389: #define AmAutoVacuumWorkerProcess()	(MyBackendType == B_AUTOVAC_WORKER)
390: #define AmBackgroundWorkerProcess() (MyBackendType == B_BG_WORKER)
391: #define AmWalSenderProcess()        (MyBackendType == B_WAL_SENDER)
392: #define AmLogicalSlotSyncWorkerProcess() (MyBackendType == B_SLOTSYNC_WORKER)
...
405: #define AmSpecialWorkerProcess() \
406: 	(AmAutoVacuumLauncherProcess() || \
407: 	 AmLogicalSlotSyncWorkerProcess())
```

全部只是对全局量 `MyBackendType` 的比较。而这个全局量在哪里被设置？
**`postmaster_child_launch()` 的子进程分支，`launch_backend.c:225`：**

```c
223: 	if (pid == 0)				/* child */
224: 	{
225: 		MyBackendType = child_type;
```

**于是 §3 段 C 那个四路分支的输入，是 fork 之后第一件事就定下来的。**
这解释了为什么 `InitProcess()` 能可靠地按进程类型选池子：
调用它时 `MyBackendType` 早就确定了。

`proc.h:513-519` 还给 `AmSpecialWorkerProcess()` 补了一段背景：

> We set aside some extra PGPROC structures for "special worker" processes, which are full-fledged backends (they can run transactions) but are unique animals that there's never more than one of. Currently there are two such processes: the autovacuum launcher and the slotsync worker.

**「完整后端能力、但全局唯一」**——这就是 `NUM_SPECIAL_WORKER_PROCS` 和
`AmSpecialWorkerProcess()` 这个分类存在的理由，也解释了它为什么和 autovacuum worker 共用 `autovacFreeProcs`。

---

## 7. 一句话总结

`InitProcess()` 用 182 行完成了一次身份转换：
从 free list 上取一个可能被崩溃进程用过的槽位、把它重置干净、
写下自己的 pid、**交出本地 latch 换成共享 latch（从此可被唤醒）**、
最后把清理函数挂上退出钩子——
顺序上的每一步都被依赖链锁死，而注释把每一条约束都写在了现场。
