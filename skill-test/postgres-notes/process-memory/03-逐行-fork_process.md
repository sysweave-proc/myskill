# PostgreSQL 源码笔记 · 03 逐行精读：fork_process()

- 位置：`src/backend/postmaster/fork_process.c:26-128`（函数体 `:32-126`，共 95 行）
- 所属主线：C 进程与内存模型（子线 C1 进程模型）
- 定位：**整个服务端多进程模型的唯一出口**
- 建立时间：2026-09-19

---

## 1. 为什么读这个函数

`01` 篇的站点图里，`postmaster_child_launch()`（`launch_backend.c:205`）最终会落到这里。
它的文件头注释（`fork_process.c:1-11`）直接说明了它的定位：

> A simple wrapper on top of fork(). This does not handle the EXEC_BACKEND case; it might be extended to do so, but it would be considerably more complex.

两句话给出两个关键信息：

1. **它是 `fork()` 的包装**——所以它要处理的不是业务逻辑，而是 fork 本身的各种坑。
2. **不管 `EXEC_BACKEND`**——该模式下子进程用 `exec` 重新加载而不是继承内存，
   所以根本不需要 fork 语义上的这些包装。这也解释了为什么整个文件被包在 `#ifndef WIN32`（`:25` 与 `:128`）里：
   Windows 没有 `fork()`，只能走 `EXEC_BACKEND` 路线。

**返回契约**（`:27-30`）完全沿用 `fork()`：

| 返回值 | 含义 |
| --- | --- |
| `-1` | fork 失败 |
| `0` | 在**子进程**中 |
| `> 0` | 在**父进程**中，值为子进程 pid |

外加一条额外约束：**fork 期间信号是屏蔽的，所以子进程必须自己解除屏蔽**。

---

## 2. 函数原文与逐行注解

```c
32: pid_t
33: fork_process(void)
34: {
35: 	pid_t		result;
36: 	const char *oomfilename;
37: 	sigset_t	save_mask;
38:
39: #ifdef LINUX_PROFILE
40: 	struct itimerval prof_itimer;
41: #endif
42:
43: 	/*
44: 	 * Flush stdio channels just before fork, to avoid double-output problems.
45: 	 */
46: 	fflush(NULL);
47:
48: #ifdef LINUX_PROFILE
49:
50: 	/*
51: 	 * Linux's fork() resets the profiling timer in the child process. If we
52: 	 * want to profile child processes then we need to save and restore the
53: 	 * timer setting.  This is a waste of time if not profiling, however, so
54: 	 * only do it if commanded by specific -DLINUX_PROFILE switch.
55: 	 */
56: 	getitimer(ITIMER_PROF, &prof_itimer);
57: #endif
58:
59: 	/*
60: 	 * We start postmaster children with signals blocked.  This allows them to
61: 	 * install their own handlers before unblocking, to avoid races where they
62: 	 * might run the postmaster's handler and miss an important control
63: 	 * signal. With more analysis this could potentially be relaxed.
64: 	 */
65: 	sigprocmask(SIG_SETMASK, &BlockSig, &save_mask);
66: 	result = fork();
67: 	if (result == 0)
68: 	{
69: 		/* fork succeeded, in child */
70: 		MyProcPid = getpid();
71: #ifdef LINUX_PROFILE
72: 		setitimer(ITIMER_PROF, &prof_itimer, NULL);
73: #endif
74:
75: 		/*
76: 		 * By default, Linux tends to kill the postmaster in out-of-memory
77: 		 * situations, because it blames the postmaster for the sum of child
78: 		 * process sizes *including shared memory*.  (This is unbelievably
79: 		 * stupid, but the kernel hackers seem uninterested in improving it.)
80: 		 * Therefore it's often a good idea to protect the postmaster by
81: 		 * setting its OOM score adjustment negative (which has to be done in
82: 		 * a root-owned startup script).  Since the adjustment is inherited by
83: 		 * child processes, this would ordinarily mean that all the
84: 		 * postmaster's children are equally protected against OOM kill, which
85: 		 * is not such a good idea.  So we provide this code to allow the
86: 		 * children to change their OOM score adjustments again.  Both the
87: 		 * file name to write to and the value to write are controlled by
88: 		 * environment variables, which can be set by the same startup script
89: 		 * that did the original adjustment.
90: 		 */
91: 		oomfilename = getenv("PG_OOM_ADJUST_FILE");
92:
93: 		if (oomfilename != NULL)
94: 		{
95: 			/*
96: 			 * Use open() not stdio, to ensure we control the open flags. Some
97: 			 * Linux security environments reject anything but O_WRONLY.
98: 			 */
99: 			int			fd = open(oomfilename, O_WRONLY, 0);
100:
101: 			/* We ignore all errors */
102: 			if (fd >= 0)
103: 			{
104: 				const char *oomvalue = getenv("PG_OOM_ADJUST_VALUE");
105: 				int			rc;
106:
107: 				if (oomvalue == NULL)	/* supply a useful default */
108: 					oomvalue = "0";
109:
110: 				rc = write(fd, oomvalue, strlen(oomvalue));
111: 				(void) rc;
112: 				close(fd);
113: 			}
114: 		}
115:
116: 		/* do post-fork initialization for random number generation */
117: 		pg_strong_random_init();
118: 	}
119: 	else
120: 	{
121: 		/* in parent, restore signal mask */
122: 		sigprocmask(SIG_SETMASK, &save_mask, NULL);
123: 	}
124:
125: 	return result;
126: }
```

### `:46` `fflush(NULL)` —— 一个经典 fork 陷阱

```c
fflush(NULL);
```

注释只说 "to avoid double-output problems"，但**为什么会有双重输出**值得展开：

```
父进程 stdio 缓冲区里有未刷出的数据（比如刚 printf 了一行但没换行）
        ↓ fork()
父子两个进程各持有一份完全相同的缓冲区副本
        ↓ 双方各自退出时都会 flush
同一份数据被打印两次 ✗
```

注意参数是 `NULL` 而不是某个具体流——这是 C 标准规定的用法：**刷新所有已打开的**输出流。
放在 fork 之前，保证 fork 那一刻缓冲区是空的，从根上消灭这个问题。

> 可迁移的教训：`fork()` 复制的是**内存**，包括任何「还没对外生效的内部状态」。
> stdio 缓冲只是最典型的一个；互斥锁状态、随机数生成器状态（见 `:117`）都属于同一类问题。

### `:56` 保存 profiling 计时器（仅 `LINUX_PROFILE`）

```c
getitimer(ITIMER_PROF, &prof_itimer);
```

注释解释得很清楚：Linux 的 `fork()` 会在子进程里重置 profiling 计时器，
所以想在子进程里继续 profiling 就必须先存后恢复。

有意思的是注释自己承认这是浪费：

> This is a waste of time if not profiling, however, so only do it if commanded by specific `-DLINUX_PROFILE` switch.

于是整段被 `#ifdef` 包住。**这是一个「为极少数场景付出的代价必须可关闭」的编码取向**——
PG 代码里大量出现这种「默认路径零开销」的写法。

### `:65` fork 前先屏蔽信号

```c
sigprocmask(SIG_SETMASK, &BlockSig, &save_mask);
result = fork();
```

`sigprocmask(SIG_SETMASK, &BlockSig, &save_mask)` 做两件事：
把当前信号屏蔽字**整体替换**为 `BlockSig`，同时把旧屏蔽字保存到 `save_mask`。

**为什么要屏蔽？** 注释 `:60-63` 说明是防一种竞态：

```
fork 返回 → 子进程内存里有 postmaster 安装的信号处理器
          → 子进程还没来得及装自己的处理器，信号就到了
          → 跑的是 postmaster 的处理器 ✗
             （可能语义不对，更糟的是可能「错过」一个关键控制信号）
```

先屏蔽、后 fork，就保证了子进程在执行到「装上自己的处理器」之前，
**任何信号都不会被投递**。这是个干净利落的解法：把不确定的时间窗消除掉。

注释最后一句也很坦诚——`With more analysis this could potentially be relaxed`，
承认这是偏保守的选择。

### `:70` 子进程刷新自己的 pid

```c
MyProcPid = getpid();
```

`MyProcPid` 是进程级全局变量，在 `main.c:113` 被赋成 postmaster 自己的 pid。
`fork()` 之后子进程继承的是**父进程的旧值**，所以必须重新取。

行数很少，但它是 03 篇和 04 篇之间的接缝：
**这个值稍后会在 `InitProcess()` 里被写进共享内存**（`storage/lmgr/proc.c:479`：`MyProc->pid = MyProcPid;`），
从此其他进程才能看见「这个 pgproc 槽位属于哪个操作系统进程」。

### `:91-114` OOM 分数调整 —— 全篇最「人类」的注释

先看 `PGPROC` 侧的呼应：`ProcKill()` 第 935 行有一句防御：

```c
/* not safe if forked by system(), etc. */
if (MyProc->pid != (int) getpid())
	elog(PANIC, "ProcKill() called in child process");
```

这段注释（`:75-90`）解释了为什么 kernel 会对 postmaster 下手：

> Linux tends to kill the postmaster in out-of-memory situations, because it blames the postmaster for the sum of child process sizes **including shared memory**.

因果链是：

```
OOM killer 要给「最该杀的进程」打分
   → postmaster 被算成「占用 = 自己 + 所有子进程 + 共享内存」
   → 共享内存被重复计数到 postmaster 头上
   → postmaster 得分最高，被杀
   → 但它恰恰是「杀掉会导致整个实例挂掉」的那个进程 ✗
```

注释里 PG 开发者显然有情绪（`This is unbelievably stupid, but the kernel hackers seem uninterested in improving it.`），
但给出的解决方案很务实：

| 步 | 做法 | 谁做 |
| --- | --- | --- |
| 1 | 把 postmaster 的 OOM 分数调成负值（受保护） | **必须由 root 拥有的启动脚本**做 |
| 2 | 但子进程会**继承**这个保护 | 内核行为 |
| 3 | 所以子进程要**自己把保护调回来** | 就是这段代码 |

第 3 步由两个环境变量驱动（`:91` `:104`），仍由同一个启动脚本设置：

- `PG_OOM_ADJUST_FILE`：写哪个文件（通常是 `/proc/self/oom_score_adj`）
- `PG_OOM_ADJUST_VALUE`：写什么值，缺省 `"0"`

在**子进程**分支里写文件，所以 `self` 指向子进程自己——刚好达到「只撤销子进程的保护」的效果。

两个细节值得单记：

**① 为什么用 `open()` 而不是 stdio**（`:96-98`）：

> Use open() not stdio, to ensure we control the open flags. Some Linux security environments reject anything but O_WRONLY.

即某些 Linux 安全环境（如带 LSM 的加固系统）会拒绝非 `O_WRONLY` 的写打开。
用 stdio 没法控制 `open` 标志，所以下探到系统调用层。**这是从真实环境中长出来的代码，不是教科书。**

**② 明确忽略所有错误**（`:101`）：

```c
/* We ignore all errors */
if (fd >= 0) { ... }
...
(void) rc;
```

`(void) rc;` 是对「故意丢弃返回值」的显式声明，避免编译器告警。
理由也站得住：OOM 打分只是**尽力而为的优化**，它失败绝不该导致连接建立失败。
**「优化项失败不能影响主流程」**——这条原则在这里被执行得很干净。

### `:117` 重新初始化随机数（**当前已是空函数**）

```c
pg_strong_random_init();
```

这里调用点的注释只写了一句：`do post-fork initialization for random number generation`。

**但这一节我写错过，必须纠正。**
最初的版本我按历史原因解读为「fork 后必须重新播种 PRNG，否则父子会产出相同的随机序列」。
实际去看实现（`src/port/pg_strong_random.c`）会发现：**PG 19 里这个函数已经是空函数。**

```c
58: void
59: pg_strong_random_init(void)
60: {
61: 	/* No initialization needed */
62: }
```

三个平台的实现全都只写了一句 `No initialization needed`——
OpenSSL 版在 `:58`，WIN32 版在 `:105`，`/dev/urandom` 版在 `:144`。
文件头注释（`:28-47`）交代了原因：

> Before `pg_strong_random` is called in any process, the generator must first be initialized by calling `pg_strong_random_init()`. **Initialization is a no-op for all supported randomness sources, it is kept to maintain backwards compatibility with extensions.**
>
> We rely on **system facilities** for actually generating the numbers. We support a number of sources:
> 1. OpenSSL's `RAND_bytes()`　2. Windows' `CryptGenRandom()`　3. `/dev/urandom`

即：**随机数不再由 PG 维护进程内的 PRNG 状态，而是每次向操作系统的 CSPRNG 索取。**
既然进程内没有状态，也就不存在「fork 后状态被复制一份」的问题，自然无需在 fork 后重新播种。

那为什么还留着这个调用？注释自己给了答案：**向后兼容扩展**——
第三方扩展可能仍在调用 `pg_strong_random_init()`，保留空实现才不会破坏它们。

> **这是一个值得单独记下的教训样本。**
> 「fork 后重播种 PRNG」在历史上确实必需，所以**调用点的注释至今仍保留着当年的措辞**。
> 这说明：**注释描述的是「这行代码当初为什么被放在这里」，不等于「它现在还在做什么」。**
> 判断当前行为必须回到实现，不能只看调用点。
> 我在第一版里正是只读了调用点就下了结论——这正是「还账」这一步的价值。

不过这个位置仍然说明了一件成立的事：
**`fork()` 会完整复制进程内状态，凡是「持有跨进程状态」的东西都必须在此处理。**
PG 对随机数采取的策略是「干脆不持有状态」，从根上填掉了这个坑；
而 `:46` 面对的 stdio 缓冲是进程内状态且无法不持有，所以仍必须显式 `fflush(NULL)`。

### `:119-123` 父进程恢复信号屏蔽——故意的**不对称**

```c
else
{
	/* in parent, restore signal mask */
	sigprocmask(SIG_SETMASK, &save_mask, NULL);
}
```

**这是全函数最容易被读漏的地方。** 对比两个分支：

| 分支 | 信号屏蔽字处理 |
| --- | --- |
| 父进程（`:122`） | **恢复**为 `save_mask` |
| 子进程 | **不恢复**，继续保持屏蔽 |

这个不对称是**故意**的，而且正是文件头契约（`:29-30`）的落实：

> Signals are blocked while forking, so **the child must unblock**.

即：`fork_process()` 把「何时解除屏蔽」的决定权**交还给子进程**，
因为只有子进程自己知道「我的信号处理器装好了没有」。
它把「先屏蔽再 fork」这个机制，从「一个实现细节」提升成了**明确的调用约定**。

> 可迁移的教训：一个函数在父/子两条路径上承担不同责任时，
> 必须把「另一方欠我一个动作」写进契约（这里是函数注释），否则调用者必然踩坑。

### `:125` 单一返回出口

```c
return result;
```

整个函数没有在子进程分支里 `exit()`，也没有 `return 0`，
而是**统一返回 `result`**，让调用者自己去判断「我在谁的身体里」。

好处是 `fork_process()` 完全不预设调用者要做什么——
它只负责「把 fork 这件事做对」，不负责「子进程接下来干什么」。
职责边界很干净。

---

## 3. 三个可迁移的设计要点

**① 单一出口 + 集中处理 fork 的固有陷阱**

`fork()` 有一串容易忘的配套动作：刷缓冲、屏蔽信号、刷新 pid、重播种随机数、调整 OOM 分。
把它们全部收进一个函数，意味着**只要调用者走了这个入口，就不可能漏掉任何一项**。
这比在每个调用点写一遍可靠得多。

这里集中了 5 项：
`:46` fflush → `:65` 信号屏蔽 → `:70` 刷新 pid → `:91-114` OOM 调分 → `:117` fork 后随机数初始化。

> 但第 5 项如今已是空实现（见下面 `:117` 一节）——**调用点仍然存在于清单中，行为却已经消失**。
> 这恰好说明为什么这份清单必须在「还账」时逐条回到实现去核对。

**② 父/子职责分离，并把「欠账」写进契约**

父子分支的处理**故意不同**，且差异写在函数头注释里（`:29-30`）。
调用者读注释就知道：**子进程分支返回后，信号仍然是屏蔽的，我必须自己解除。**

**③ 优化项一律 best-effort**

OOM 调分失败、写文件失败，全部静默忽略（`:101` `:111`）。
判断标准是：**这件事失败了会不会影响「能不能建立连接」？**
不会 → 就不许把错误往上抛。

---

## 4. 与前篇的呼应

| 呼应点 | 位置 |
| --- | --- |
| `MyProcPid` 在此设置，在 `InitProcess()` 发布到共享内存 | `fork_process.c:70` → `storage/lmgr/proc.c:479` |
| `ProcKill()` 校验 `MyProc->pid != getpid()`，正是对 fork 语义的防御 | `storage/lmgr/proc.c:934-936` |
| 槽位在 fork **之前**分配的策略（`01` 篇已记录）与此处 fork 形成整体 | `postmaster.c:3589-3598` |

---

## 5. 遗留问题（已全部还清）

| 原问题 | 结论 | 位置 |
| --- | --- | --- |
| `BlockSig` 定义与内容 | 定义 + `pqinitmask()` 初始化 | `libpq/pqsignal.c:22-24`、`:41-99` |
| 子进程何时解除屏蔽 | **两阶段**，见下 | `miscinit.c:153-156`、`tcop/postgres.c:4348` |
| `pg_strong_random_init()` 实现 | **空函数**，仅为兼容扩展保留 | `src/port/pg_strong_random.c:58-61` |
| `postmaster_child_launch()` 如何二选一 | `#ifdef EXEC_BACKEND` 分支编译 | `launch_backend.c:217-222` |

### `BlockSig` 到底是什么（`pqsignal.c:22-24`、`:41-99`）

三个全局信号集在 `pqinitmask()` 里一次建好：

| 集合 | 构造方式 | 含义 |
| --- | --- | --- |
| `UnBlockSig` | `sigemptyset()`（`:43`） | 空集 = **不屏蔽任何信号** |
| `BlockSig` | `sigfillset()` 后逐个 `sigdelset`（`:48`、`:56-87`） | 屏蔽一切，**除了永不该屏蔽的** |
| `StartupBlockSig` | 基于 `BlockSig` 再去掉 SIGTERM / SIGQUIT / SIGALRM（`:89-98`） | 收 startup packet 期间用 |

从 `BlockSig` 里被摘掉的信号（`:56-87`）是：
`SIGTRAP`、`SIGABRT`、`SIGILL`、`SIGFPE`、`SIGSEGV`、`SIGBUS`、`SIGSYS`、`SIGCONT`。

看这份名单就能明白筛选标准：**全是同步异常（程序自己出错触发的）和进程控制信号**。
`SIGSEGV`、`SIGFPE` 这类信号如果被屏蔽，程序出错时就变成了「挂起」而不是「当场崩掉」，
调试和故障定位会彻底失效——所以它们在 `:52-53` 的注释里被归为 `should never be blocked`。

### 子进程究竟在哪里解除屏蔽（两阶段）

对照 `02` 篇 `MemoryContextInit` 的两阶段初始化，这里也是分两步、由不同模块负责：

**第一步：只解除 `SIGQUIT`** —— `utils/init/miscinit.c:146-156`，在 `InitPostmasterChild()` 内：

```c
/*
 * Every postmaster child process is expected to respond promptly to
 * SIGQUIT at all times.  Therefore we centrally remove SIGQUIT from
 * BlockSig and install a suitable signal handler.  ...
 * All other blockable signals remain blocked for now.
 */
pqsignal(SIGQUIT, SignalHandlerForCrashExit);
sigdelset(&BlockSig, SIGQUIT);
sigprocmask(SIG_SETMASK, &BlockSig, NULL);
```

注释把边界说得很明确：**`All other blockable signals remain blocked for now.`**
即这一步只保证「子进程随时能被 SIGQUIT 快速杀死」，其余照旧屏蔽。

**第二步：整体解除** —— `tcop/postgres.c:4344-4348`，在 `PostgresMain()` 内：

```c
/* Early initialization */
BaseInit();

/* We need to allow SIGINT, etc during the initial transaction */
sigprocmask(SIG_SETMASK, &UnBlockSig, NULL);
```

注意用的是 `UnBlockSig`（空集）——**一次性解除全部屏蔽**。
时机选在 `BaseInit()` 之后，理由是「初始事务期间需要允许 SIGINT 等」，
即到这时代码已经具备安全处理中断的能力了。

> 所以 `fork_process()` 留下的那笔「欠账」，实际是**由 `InitPostmasterChild()` 先部分偿还（仅 SIGQUIT）、
> 再由 `PostgresMain()` 全额还清**的。
> 这也解释了为什么函数头只写「子进程必须解除屏蔽」而不指定具体位置——
> **解除屏蔽的正确时机取决于子进程要走哪条业务路径，只能由它自己决定。**

---

## 6. 一句话总结

`fork_process()` 用 95 行把「创建一个对的后代进程」这件事做成了**不可遗漏的清单**：
stdio 先清空、信号先屏蔽、pid 先刷新、OOM 保护先卸掉——
然后把「何时解除屏蔽」这件只有子进程自己知道的事，作为契约明确交还给调用者。

> 还账时的一个副产品：清单里第 5 项（fork 后随机数初始化）如今已是空实现。
> **清单本身没变，变的是我们对每一行的理解**——这正是必须回源核对的理由。
