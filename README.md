# myskill

个人 Skill 资产仓。**一个 Skill 一个顶层目录**，每个目录自带 README 说明其结构与来龙去脉。

## Skill 索引

| Skill | 说明 | 版本 |
|---|---|---|
| [`source-code-reading-skill/`](source-code-reading-skill/) | 面向大型 C/C++ 项目的「源码阅读知识建模」技能包：`versions/` 存七版演进（含原始 zip、解压产物、对话原始材料），顶层 `skill-ds/` 存非谱系的对照版（v0.6.0 的合并输入） | v0.1 → v0.6.0 |

> **变动记录**：原顶层 `skill-ds/` 已移入 `source-code-reading-skill/skill-ds/`（它不属于版本谱系，保留作 v0.6.0 的对照与输入材料）；`skill-ds-chatgpt/` 已删除（质量不达标）。
>
> **v0.6.0 post-freeze 修复**（2 项，均已实测）：`SKILL.md` 的 `description: >-` → `|-`（原写法令官方校验器七版全 fail，改后 `Skill is valid!`）；`tests/test_skill_integrity.py` 增加基线目录存在性/非空守卫（原版传错路径会假通过）。因此 `versions/v0.6.0/skill/` 与其 `source.zip` 不再逐字节一致，记录见该版 `README.md` 备注与 `skill/CHANGELOG.md`。

## 目录约定

新增 Skill 时按下面这套结构建目录，并登记到上面的索引表：

```
<skill-name>/
├── README.md           技能说明：这是什么、版本谱系、已知问题
├── versions/           一版一个目录，进去就能看全
│   └── vX.Y/
│       ├── README.md       本版说明：主题、变化、包内构成
│       ├── skill/        该版交付产物（文件树，可读）
│       ├── source.zip      该版原始打包（权威字节，勿改）
│       └── conversation/   该版的讨论过程（会话全文、原始数据、页面快照）
├── <对照目录>/          可选：不属于版本谱系的对照产物（读后重写、他源再表达等），与 versions/ 平铺
└── docs/               跨版本的审计报告、设计说明等
```

约定：**按版本聚合**，而不是按文件类型分散——想知道「某一版是什么」，进一个目录就够；`skill/` 与 `source.zip` 是同一份内容的两种形态（解压 vs 压缩原件）。
