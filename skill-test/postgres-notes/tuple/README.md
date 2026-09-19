# 元组（tuple）表示与生命周期

> 一句话定位：**「一个元组」在 PostgreSQL 里不是一种东西，而是一族按「离磁盘多远」排列的表示**——本类回答它们各是什么、在哪一层被抽象掉、由谁终结。
> 一句话总结：**「元组是什么」由 `TupleDesc` 回答，「元组在哪、谁释放」由 `TupleTableSlotOps` 回答；两件事被刻意拆开，代价是资源所有权全靠手工维护。**
> 使用方式：`01` 拿地图（边界与阅读路线），`02` 看地形（真实调用链与生命周期）。**先 01 后 02**。

- 源码：`/home/zhq/mydisk/github/postgres`（PostgreSQL 19beta2）
- 建立时间：2026-09-19
- 篇数：2（地图 1 + 地形 1）

---

## 1. 篇索引

| 篇 | 内容 | 对应问题 |
| --- | --- | --- |
| [`01`](01-元组表示分层-地图.md) | **地图**：四段抽象 / 七种表示 / 11 个回调的 `TupleTableSlotOps` 虚表 / 三处跨文件不变量 | `tuple` 一族由哪些表示构成？抽象发生在哪一层？阅读边界画在哪？ |
| [`02`](02-元组生命周期-逐行.md) | **地形**：5 类生产点 / 4 个分层终止器 / 3 种传递载体 / `MINIMAL_TUPLE_OFFSET` 这个支点 / 落盘的两次形态剥离 | 一个元组从诞生到消失走哪条路？谁终结它？模块之间靠什么传递？ |

## 2. 全景图

```
① 磁盘 / 页内          行指针 ItemIdData + 一段字节（HeapTupleHeaderData 开头）      itemid.h / htup_details.h
        ↓ 零拷贝
② 物理表示             HeapTupleData（管理壳，含事务头） │ MinimalTupleData（瘦身版，无事务头）
                        └─ 靠 t_hoff + MINIMAL_TUPLE_OFFSET(=8) 伪装成同一布局
        ↓
③ 描述层「怎么解释」    TupleDescData + CompactAttribute（19beta2 新增的紧凑缓存）    tupdesc.h
        ↓
④ 执行器抽象「在哪、谁释放」  TupleTableSlot（tts_values[] / tts_isnull[]）
                        └─ TupleTableSlotOps 11 个回调：四种内置实现            tuptable.h / execTuples.c
```

**两根正交的轴**（读这一层最容易混的地方）：

| 轴 | 取值 | 判断依据 |
| --- | --- | --- |
| **形态** | virtual / HeapTuple / MinimalTuple / 页内 HeapTuple | `tts_ops` 指明槽类型，再看 `hslot->tuple` / `mslot->mintuple` 是否为 NULL |
| **内存归属** | 自持 / 依赖外部（页、别的上下文） | `TTS_SHOULDFREE` + `BufferHeapTupleTableSlot.buffer` 是否有效 |

**两轴不联动**——最反直觉的组合是「virtual 形态 × 自持」：`TTSOpsVirtual` 槽被物化之后**依然没有物理元组**，只是它引用的字节搬进了自己的上下文。所以「物化改变的是**内存归属**，不是**形态**」。

## 3. 关键文件表

| 文件 | 职责 |
| --- | --- |
| `src/include/access/htup_details.h` | 元组头结构、infomask 位定义、全部访问宏、三个 `MINIMAL_TUPLE_*` 偏移宏 |
| `src/include/access/htup.h` | `HeapTupleData` / `HeapTuple` / `MinimalTuple` 指针层 |
| `src/backend/access/common/heaptuple.c` | `heap_form_tuple` / `heap_form_minimal_tuple` / `heap_getattr` / 全部释放函数 |
| `src/include/executor/tuptable.h` | `TupleTableSlot` + `TupleTableSlotOps` + 四种 slot 结构体 |
| `src/backend/executor/execTuples.c` | 四种 ops 实例、`slot_deform_heap_tuple`、全部 slot API |
| `src/include/access/tupdesc.h` | `CompactAttribute` / `TupleDescData`（19beta2 新增紧凑缓存） |
| `src/backend/utils/sort/tuplesortvariants.c`、`tuplestore.c` | 溢出到临时文件时的落盘格式 |

## 4. 与相邻主题的边界

| 本类管什么 | 隔壁管什么 |
| --- | --- |
| 元组的表示分层、生产与释放、模块间传递载体、落盘格式 | 进程、内存上下文、共享内存 → [`../process-memory/`](../process-memory/) |
| — | **有意排除**（见 `01` 篇 §Analysis Methodology）：索引元组（`IndexTuple` / `itup.h`）、TOAST 压缩与解压（`detoast.c`）、catalog 读取路径、各 slot 转换函数的实现细节 |

> `01` 是一份**地图篇**。按 `source-notes-authoring` 与 `repo-wiki-authoring` 的边界约定，宏观地图本属后者；此处是用户确认保留在库内的**有意例外**——它只画「元组这一层」的边界，不做模块级全景。

## 5. 阅读建议

1. **`01` 的 Recommendations 是 `02` 的任务书**：它选定的下一个精读点是 `heap_form_tuple`（唯一的「从 `Datum[]` 造物理元组」出口）与 `slot_deform_heap_tuple`（执行器侧的对照点）——正好是同一套布局规则的正反两面，`02` 覆盖了这两个点。
2. **`01` 先建立「有几种表示」的地图，再读 `02` 的真实调用链**，否则会在 `heap → minimal → 裸数据体` 的两次形态剥离里迷路。
3. **`02` 的 §Critical Logic 4 是本类最值钱的一节**：它纠正了「物化 = 把指针指向的 tuple 整理成私有内存」这个常见直觉。

## 6. 待办

| 项 | 依据 | 状态 |
| --- | --- | --- |
| 排序/物化路径携带 TOAST 外部指针为何安全 | `02` 篇 R7（`src/backend/utils/sort/` 全目录 0 命中） | **`[待验证]`**，已给出两条候选追查入口 |
| `slot_deform_heap_tuple` 三条分段路径的等价性 | `02` 篇遗留问题表 | 未读 |
| `tts_virtual_clear` 释放 `vslot->data` 的确切条件 | `02` 篇遗留问题表 | 未读 |
