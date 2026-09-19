# PostgreSQL 源码笔记 · 02 逐行精读：MemoryContextInit()

- 位置：`src/backend/utils/mmgr/mcxt.c:345-398`（函数体 `:362-398`，共 37 行）
- 所属主线：C 进程与内存模型（子线 C2 内存模型）
- 定位：整个内存上下文体系的**唯一地基函数**
- 建立时间：2026-09-19

---

## 1. 为什么从这个函数开始

`src/backend/main/main.c:114`：

```c
MyProcPid = getpid();
MemoryContextInit();
```

这是 `main()` 里**最早**被调用的子系统之一，注释写着「Fire up essential subsystems: error and memory management」——
错误处理和内存管理是其余一切代码的前置条件。

调用时机（`mcxt.c:353-357` 注释）：

> In normal multi-backend operation, this is called once during postmaster startup, and not at all by individual backend startup (since the backends inherit an already-initialized context subsystem by virtue of being forked off the postmaster). But in an EXEC_BACKEND build, each process must do this for itself.

即：**普通模式下只有 postmaster 调用一次**，所有子进程通过 `fork` 直接继承已建好的上下文森林。
这也解释了为什么这个函数不需要考虑并发——它在单进程阶段就完成了。

---

## 2. 函数原文与逐行注解

```c
361: void
362: MemoryContextInit(void)
363: {
364: 	Assert(TopMemoryContext == NULL);
365:
366: 	/*
367: 	 * First, initialize TopMemoryContext, which is the parent of all others.
368: 	 */
369: 	TopMemoryContext = AllocSetContextCreate((MemoryContext) NULL,
370: 											 "TopMemoryContext",
371: 											 ALLOCSET_DEFAULT_SIZES);
372:
373: 	/*
374: 	 * Not having any other place to point CurrentMemoryContext, make it point
375: 	 * to TopMemoryContext.  Caller should change this soon!
376: 	 */
377: 	CurrentMemoryContext = TopMemoryContext;
378:
379: 	/*
380: 	 * Initialize ErrorContext as an AllocSetContext with slow growth rate ---
381: 	 * we don't really expect much to be allocated in it. More to the point,
382: 	 * require it to contain at least 8K at all times. This is the only case
383: 	 * where retained memory in a context is *essential* --- we want to be
384: 	 * sure ErrorContext still has some memory even if we've run out
385: 	 * elsewhere! Also, allow allocations in ErrorContext within a critical
386: 	 * section. Otherwise a PANIC will cause an assertion failure in the error
387: 	 * reporting code, before printing out the real cause of the failure.
388: 	 *
389: 	 * This should be the last step in this function, as elog.c assumes memory
390: 	 * management works once ErrorContext is non-null.
391: 	 */
392: 	ErrorContext = AllocSetContextCreate(TopMemoryContext,
393: 										 "ErrorContext",
394: 										 8 * 1024,
395: 										 8 * 1024,
396: 										 8 * 1024);
397: 	MemoryContextAllowInCriticalSection(ErrorContext, true);
398: }
```

### `:364` 只能初始化一次

```c
Assert(TopMemoryContext == NULL);
```

用 `Assert` 而非 `ereport(ERROR)`，理由是这是**内部编码契约**：只有启动路径会调它，
重复调用属于代码 bug，不是运行时可恢复的错误。注意 `Assert` 在非 `USE_ASSERT_CHECKING` 构建下会被编译掉，
所以**生产构建里这行不存在**——它保护的是开发者，不是用户。

同时这也确立了 `TopMemoryContext` 的**单例**性质。

### `:369-371` 建立树根

```c
TopMemoryContext = AllocSetContextCreate((MemoryContext) NULL,
										 "TopMemoryContext",
										 ALLOCSET_DEFAULT_SIZES);
```

**三个要点：**

**① 父上下文传 `NULL`** —— 这是它成为树根的方式。
`utils/mmgr/README:110-117` 解释了为什么需要父子关系：
如果所有上下文彼此独立，就难以追踪、尤其难以在错误路径上回收；
而这套父子树让「删一个上下文 = 连带删掉整棵子树」成立。
README 同时指出理论上可以有多棵树，但**实践上只有 `TopMemoryContext` 一个根**。

**② `AllocSetContextCreate` 是宏，不是函数**（`src/include/utils/memutils.h:118-131`）：

```c
#ifdef HAVE__BUILTIN_CONSTANT_P
#define AllocSetContextCreate(parent, name, ...) \
	(StaticAssertExpr(__builtin_constant_p(name), \
					  "memory context names must be constant strings"), \
	 AllocSetContextCreateInternal(parent, name, __VA_ARGS__))
#else
#define AllocSetContextCreate \
	AllocSetContextCreateInternal
#endif
```

宏壳子加了一道**编译期静态断言**：上下文名字必须是常量字符串。
`memutils.h:118-121` 的注释说明这是有意的破坏性变更——动态名字已不再支持，
需要变量标识时改用 `MemoryContextSetIdentifier()`。
好处是上下文名字可以**不占运行时存储**（直接指向 `.rodata` 里的字面量），省内存也便于调试。

真正的实现在 `utils/mmgr/aset.c:347` `AllocSetContextCreateInternal()`。

**③ `ALLOCSET_DEFAULT_SIZES` 的真实取值**（`memutils.h:157-161`）：

```c
#define ALLOCSET_DEFAULT_MINSIZE   0
#define ALLOCSET_DEFAULT_INITSIZE  (8 * 1024)
#define ALLOCSET_DEFAULT_MAXSIZE   (8 * 1024 * 1024)
#define ALLOCSET_DEFAULT_SIZES \
	ALLOCSET_DEFAULT_MINSIZE, ALLOCSET_DEFAULT_INITSIZE, ALLOCSET_DEFAULT_MAXSIZE
```

对应 `AllocSetContextCreateInternal()` 的三个 size 参数（`memutils.h:112-116`）：

| 参数 | 值 | 含义 |
| --- | --- | --- |
| `minContextSize` | `0` | 不预先保留块，首次分配时才向 `malloc` 要 |
| `initBlockSize` | `8K` | 第一个块 8K，此后逐块翻倍 |
| `maxBlockSize` | `8M` | **单个块**大小上限（不是上下文容量上限） |

> 容易读错的一点：`maxBlockSize` 限制的是**块**的大小，不是整个上下文能占多少。
> 上下文可以挂很多块，8M 只是「不会再要更大的单块」。
> 另外 `README:464-468` 提到：reset 时第一个块不还给 `malloc` 而是清空复用，避免 malloc 抖动——
> 这正是为 per-tuple 上下文的高频 reset 做的优化。

### `:377` 给 Current 一个兜底值

```c
CurrentMemoryContext = TopMemoryContext;
```

注释直接点明：`Caller should change this soon!`

为什么必须先指过去？因为 `palloc()` 是**隐式依赖 `CurrentMemoryContext`** 的
（`README:36-40`：palloc implicitly allocates space in that context）。
`CurrentMemoryContext` 在任何时刻都不能为 `NULL`，否则第一次 `palloc` 就崩。

但这是**临时安全值**，不是推荐值。`README:185-192` 明确警告：

> Allocating here is essentially the same as "malloc", because this context will never be reset or deleted. ...
> **Avoid allocating stuff here unless really necessary, and especially avoid running with CurrentMemoryContext pointing here.**

原因很直接：`TopMemoryContext` 永不回收，在它上面分配 = 永久泄漏。
所以 `:377` 是「先保证不崩」，真正的上下文由后续启动流程替换掉。

### `:392-396` ErrorContext 故意「不成长」

```c
ErrorContext = AllocSetContextCreate(TopMemoryContext,
									 "ErrorContext",
									 8 * 1024,
									 8 * 1024,
									 8 * 1024);
```

与 `TopMemoryContext` 用 `ALLOCSET_DEFAULT_SIZES` 形成鲜明对比——这里三个参数**全是 8K 硬编码**。

注释（`:380-387`）给了理由，拆开看是两条：

1. **「require it to contain at least 8K at all times」**
   `minContextSize = 8K` 意味着创建时就保留一个 8K 块（`README:459-462`）。
2. **「we want to be sure ErrorContext still has some memory even if we've run out elsewhere」**

这是全篇最精妙的一处设计。想清楚这个循环依赖：

- 系统 OOM 了，需要**报错**；
- 报错需要（临时）分配内存；
- 但如果报错依赖的上下文也去向 `malloc` 要内存——**而系统正是因为没有内存才 OOM 的**——就会失败。

所以 `ErrorContext` 必须在**启动时就**把 8K 拿在手里，之后不再依赖 `malloc`。
`minContextSize = initBlockSize = maxBlockSize = 8K` 的组合同时表达了两件事：
**给我一块保命内存**，以及**别指望它长大**（注释：`we don't really expect much to be allocated in it`）。

README 把结论说得很清楚（`:253-258`）：

> We arrange to have a few KB of memory available in it at all times. In this way, we can ensure that some memory is available for error recovery even if the backend has run out of memory otherwise.
> **This allows out-of-memory to be treated as a normal ERROR condition, not a FATAL error.**

即：这 8K 换来的能力是「OOM 可以优雅报错并回滚，而不是直接杀掉后端」。

### `:389-391` 顺序是强制的

```c
* This should be the last step in this function, as elog.c assumes memory
* management works once ErrorContext is non-null.
```

`ErrorContext` 的非空状态 = 「内存管理体系已可用」的信号，
`elog.c`（错误报告）依赖这个信号。因此**这一句必须是函数的最后一步**，不能提前。

注意 `:389` 和 `:385-387` 的注释都在讲同一件事的两面：
`ErrorContext` 既要是「最后建的」，又要是「能在 critical section 里分配的」。

### `:397` 唯一一处「走后门」

```c
MemoryContextAllowInCriticalSection(ErrorContext, true);
```

实现极简，`mcxt.c:746-751`：

```c
void
MemoryContextAllowInCriticalSection(MemoryContext context, bool allow)
{
	Assert(MemoryContextIsValid(context));
	context->allowInCritSection = allow;
}
```

只是给上下文的 `allowInCritSection` 标志位赋值。但**为什么需要这个标志**，注释（`mcxt.c:739-743`）说得明白：

> Normally, memory allocations are not allowed within a critical section, because a failure would lead to PANIC. There are a few exceptions to that, like allocations related to debugging code that is not supposed to be enabled in production. This function can be used to exempt specific memory contexts from the assertion in palloc().

规则是：**critical section 内禁止分配内存**——因为进入 critical section 意味着「此刻出错只能 PANIC」，
而分配可能失败，失败就 PANIC。

而这里恰恰要**违反规则**，原因在 `:386-387` 的注释：

> Otherwise a PANIC will cause an assertion failure in the error reporting code, **before printing out the real cause of the failure**.

翻译成因果链就是：

```
系统 PANIC → 要打印真实原因 → 打印需要分配内存 → palloc 断言「critical section 里不许分配」
          → 真实原因还没打出来，先因断言失败而挂掉 ✗
```

所以必须给 `ErrorContext` 开一个精确的例外：**允许它在 critical section 内分配**，
从而保证最坏情况下也能把错误原因吐出来。

这条「后门」的存在本身就是一个可迁移的教训：
**当一个规则（禁止 critical section 内分配）威胁到诊断能力时，必须为诊断路径留出受控例外，否则系统会在最需要信息的时候吞掉信息。**

---

## 3. 四步顺序的必然性

| 步 | 代码 | 为什么必须在这个位置 |
| --- | --- | --- |
| 1 | `TopMemoryContext = ...` (`:369`) | 树根，后面两个上下文都要挂在它下面 |
| 2 | `CurrentMemoryContext = TopMemoryContext` (`:377`) | `palloc` 隐式依赖它，必须**立刻**非空（此后才允许有任何分配） |
| 3 | `ErrorContext = ...` (`:392`) | 报错能力的前提；注释两次强调必须是最后一步 |
| 4 | `AllowInCriticalSection(ErrorContext)` (`:397`) | 保证第 3 步的能力在 critical section 内也成立 |

这四步**不可交换**，且第 1-4 步都在 `main.c:114` 这一行内完成，之后整个进程才「敢于」使用 `elog`。

---

## 4. 谁不在这里被初始化

`memutils.h:52-57` 的注释点出：

> Standard top-level memory contexts.
> **Only TopMemoryContext and ErrorContext are initialized by MemoryContextInit() itself.**

其余全局上下文（`PostmasterContext`、`CacheMemoryContext`、`MessageContext`、
`TopTransactionContext`、`CurTransactionContext`、`PortalContext`）都由各自的模块在更晚的时候创建。

`README:200-202` 补充了一个很有用的事实：

> The postmaster has only TopMemoryContext, PostmasterContext, and ErrorContext --- the remaining top-level contexts are set up in each backend during startup.

即 **postmaster 进程只有 3 个顶级上下文**，事务级/消息级那些是每个 backend 起来时才建的。
这直接呼应本篇 §1：子进程继承的是「三件套」这个最小可用集，不是完整的森林。

---

## 5. 核对结果（原「遗留问题」已全部还清）

| 原问题 | 结论 | 位置 |
| --- | --- | --- |
| `MemoryContextSwitchTo()` / `CurrentMemoryContext` 位置 | 头文件里的 `static inline` + 全局变量定义 | `palloc.h:136-144`、`mcxt.c:161` |
| `palloc()` 的 critical section 断言 | `AssertNotInCriticalSection(context)` | `mcxt.c:1397`，宏定义在 `:193-199` |
| `PostmasterContext` 创建点 | postmaster 启动时创建，子进程里删除 | `postmaster.c:535`（+ 惰性创建 `postinit.c:227-230`） |
| `AllocSetContextCreateInternal()` 如何建块 | 见 §5.3 | `aset.c:347-489` |

### 5.1 `MemoryContextSwitchTo` 是头文件里的 inline 函数

`src/include/utils/palloc.h:136-144`：

```c
#ifndef FRONTEND
static inline MemoryContext
MemoryContextSwitchTo(MemoryContext context)
{
	MemoryContext old = CurrentMemoryContext;

	CurrentMemoryContext = context;
	return old;
}
#endif
```

`:129-134` 的注释解释了 `#ifndef FRONTEND` 的由来：某些前端程序（如 `pg_controldata`）
会经 `postgres.h` 引入这个头文件，个别编译器无法处理这种 inline 定义，所以在前端构建时隐藏掉。

`CurrentMemoryContext` 本身：声明在 `palloc.h:59`，定义在 `mcxt.c:161`。
`palloc.h:54-58` 给了一条使用警告：

> `CurrentMemoryContext` is the default allocation context for palloc().
> **Avoid accessing it directly!** Instead, use `MemoryContextSwitchTo()` to change the setting.

注意措辞的精确性：**直接读它不是错误，直接写它才是**——
写入会绕过「先记住旧上下文」的约定，而 `MemoryContextSwitchTo()` 的返回值正是为了让调用者能切回去。

### 5.2 「critical section 内禁止分配」的完整闭环

`mcxt.c:1390-1397`：

```c
void *
palloc(Size size)
{
	/* duplicates MemoryContextAlloc to avoid increased overhead */
	void	   *ret;
	MemoryContext context = CurrentMemoryContext;

	Assert(MemoryContextIsValid(context));
	AssertNotInCriticalSection(context);
```

而 `AssertNotInCriticalSection` 的定义就在同文件 `mcxt.c:193-199`：

```c
/*
 * You should not do memory allocations within a critical section, because
 * an out-of-memory error will be escalated to a PANIC. To enforce that
 * rule, the allocation functions Assert that.
 */
#define AssertNotInCriticalSection(context) \
	Assert(CritSectionCount == 0 || (context)->allowInCritSection)
```

**到这里，本篇开头 `MemoryContextInit` 里那两行终于完全闭环了：**

```
mcxt.c:397   MemoryContextAllowInCriticalSection(ErrorContext, true)
               → context->allowInCritSection = true                    (mcxt.c:750)
                                                          ↓
mcxt.c:1397  palloc() → AssertNotInCriticalSection(context)
               → Assert(CritSectionCount == 0 || (context)->allowInCritSection)   (mcxt.c:199)
```

即：**§2 里那次「开后门」写下的标志位，正是在 `palloc` 里被读取并放行的地方。**
`CritSectionCount == 0` 覆盖常规情况（不在 critical section 里就随便分配），
`allowInCritSection` 则是给 `ErrorContext` 留的例外通道——两者任一成立即放行。

一个小小的 `bool` 字段，就把「critical section 内禁止分配」与「PANIC 时必须能报错」这对矛盾解开了。
这也再次印证 `02` 篇的结论：**这个例外是精确的、有明确边界的，而不是把规则整体放宽。**

### 5.3 `AllocSetContextCreateInternal()` 与那 8K 的物理来源

`aset.c:346-489`，几个关键点：

**① 参数校验全是 `Assert`**（`:377-386`），注释 `:366-369` 交代了原因：

> Once these were regular runtime tests and elog's, but in practice Asserts seem sufficient because **nobody varies their parameters at runtime**.

即「历史上是运行时检查，后来降级为断言，因为实践中没人在运行时改这些参数」。
这是一条很有参考价值的判断：**当某个不变式在实践中从未被违反，把它从运行时检查降级为开发期断言
是合理的成本取舍——但前提是「从未被违反」这个事实要真实成立。**

校验要求 `minContextSize` 要么为 0、要么至少 1024 且不超过 `maxBlockSize`（`:382-385`）。

**② 上下文本身也有 free list 可复用**（`:388-430`）。
参数若正好匹配 `ALLOCSET_DEFAULT_SIZES` 或 `ALLOCSET_SMALL_SIZES`，就去对应 free list 取一个已释放的上下文复用，
只更新 `maxBlockSize`（注释 `:389-390`：`We do not need to demand a match of maxBlockSize.`），
再调 `MemoryContextCreate()` 重装头部。

**这顺带回答了「`MemoryContextCreate()`（`mcxt.c:1152`）被谁调用」** —— `aset.c:419` 就是其中一个调用点。

**③ 首块大小与 `minContextSize` 的关系**（`:432-438`）：

```c
firstBlockSize = MAXALIGN(sizeof(AllocSetContext)) +
	ALLOC_BLOCKHDRSZ + ALLOC_CHUNKHDRSZ;
if (minContextSize != 0)
	firstBlockSize = Max(firstBlockSize, minContextSize);
else
	firstBlockSize = Max(firstBlockSize, initBlockSize);
```

**这就是 §2 所说「那 8K 被攥在手里」的物理来源：**
因为 `ErrorContext` 的 `minContextSize = 8K ≠ 0`，首块大小取 `Max(头部开销, 8K)`，
然后在 `:444` 通过**一次 `malloc(firstBlockSize)`** 就把它要到手。

对照 `TopMemoryContext`：它的 `minContextSize = 0`，于是走 `else` 分支，
首块大小取 `Max(头部开销, initBlockSize=8K)`。

> **两个上下文的首块都是 8K，却是两个不同分支算出来的。**
> 区别不在数值，而在 `minContextSize` 是否为 0：
> 为 0 表示「可以只给最小块」，非 0 表示「**无论如何先给我这么多**」。
> 这正是 `README:459-462` 所说「an aset.c context will always contain at least one block,
> of size `minContextSize` if that is specified, otherwise `initBlockSize`」的代码实现。

**④ 两处 OOM 处理**（`:444-454`）：`malloc` 失败时，
**先 `if (TopMemoryContext) MemoryContextStats(TopMemoryContext);` 打印内存分布**，
再抛 `ERROR` 并带上失败的上下文名字。这又是「尽力留下诊断信息」的一次体现——
与本篇 `:389-391` 里 ErrorContext 存在的理由一脉相承。

**⑤ 一条防泄漏纪律**（`:456-459`）：

> Avoid writing code that can fail between here and `MemoryContextCreate`; we'd leak the header/initial block if we ereport in this stretch.

即从 `malloc` 成功到 `MemoryContextCreate` 完成之间**不允许存在任何可能报错的代码**，
否则已到手的块就泄漏了。**「先拿资源、再注册，中间不留失败点」——这类顺序约束在 PG 里反复出现。**

**⑥ `PostmasterContext` 的创建与销毁**

- **创建**：`postmaster.c:535`（在 `PostmasterMain()` 内），注释 `:529-534` 说明用途：

  > By default, palloc() requests in the postmaster will be allocated in the `PostmasterContext`, which is space that can be **recycled by backends**. Allocated data that needs to be available to backends should be allocated in `TopMemoryContext`.

  即它是「postmaster 的工作区」，**fork 出去的子进程可以把它整个删掉以回收空间**；
  而需要留给子进程用的数据则必须放在 `TopMemoryContext`。
- **惰性创建**：`postinit.c:227-230`（`load_hba()` / `load_ident()` 需要它）。
- **销毁**：几乎每个子进程都在启动早期删它——
  `backend_startup.c:118-122`、`bgworker.c:757-761`、`auxprocess.c:46-50`、
  `syslogger.c:221-225`、`autovacuum.c:420-424`、`slotsync.c:1573-1577`，
  以及普通 backend 在 `postgres.c:4388-4392`（`InitPostgres` 完成后）删除。

> 特别值得记的是 `backend_startup.c:118-121` 的注释：
> `We can't delete it just yet, though, because InitPostgres will need the HBA data.`
>
> **这组调用点恰好印证了 `mmgr/README:194-199` 的说法**：
> `PostmasterContext` 在 backend 起来后可以删除，以释放从 postmaster 继承来的内存；
> 但在认证完成前不能删，因为 HBA 数据还在里面。
> 从「谁来删、什么时候删」这组事实上，能直接看出 `fork` 继承模型的实际代价与回收时机。

---

## 6. 一句话总结

`MemoryContextInit()` 用 37 行做了一件事：
**把「内存分配」从一个可能失败的动作，变成系统可以依赖其永不失败的地基**——
靠的是一棵只挂两个节点的上下文树、一个永不为空的 `CurrentMemoryContext`，
以及一块 8K 的、专门用来在无法分配内存时还能说话的内存。
