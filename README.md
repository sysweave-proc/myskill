# myskill

个人 Skill 资产仓。**一个 Skill 一个顶层目录**，每个目录自带 README 说明其结构与来龙去脉。

## Skill 索引

| Skill | 说明 | 版本 |
|---|---|---|
| [`source-code-reading-skill/`](source-code-reading-skill/) | 面向大型 C/C++ 项目的「源码阅读知识建模」技能包，含六版演进、原始 zip、解压产物与对话原始材料 | v0.1 → v0.5.1 |

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
└── docs/               跨版本的审计报告、设计说明等
```

约定：**按版本聚合**，而不是按文件类型分散——想知道「某一版是什么」，进一个目录就够；`skill/` 与 `source.zip` 是同一份内容的两种形态（解压 vs 压缩原件）。
