# v0.1

**主题**：六阶段框架成型（起点） ｜ **规模**：15 文件 / 1,601 行 ｜ `SKILL.md` 的 `version: 0.1.0`

## 本版变化

起点版本。把「读懂大型 C/C++ 项目」拆成六阶段流程，产出第一份完整技能包：

```
Scope & Explore → Knowledge Model → Pattern Recognition
→ Traceability → Representation & Document → Validation & Orchestration
```

## 目录

| 路径 | 内容 |
|---|---|
| `package/` | 技能包文件树（15 个文件，可直接阅读） |
| `source.zip` | 原始 zip（权威字节，勿改） |
| `conversation/` | 对话材料：`conversation.md` 逐轮全文 · `raw-data.json` 页面内嵌数据 · `snapshot.html` 页面快照 |

## 包内构成

```
SKILL.md   README.md
references/   knowledge-model.md · document-policy.md
              patterns/pattern-catalog.md
              representation/representation-policy.md
              tracing/{trace-policy, claim-verification, exploration-policy}.md
              validation/validation-policy.md
templates/    source-reading-note.md · knowledge-model.yaml · review-report.md
examples/     buffer-manager-plan.yaml · lock-manager-plan.yaml
```

## 备注

- frontmatter 用 `description: >-`，官方校验器会报 `Description cannot contain angle brackets`（这是 v0.1~v0.4、v0.5.1 六个版本的通病）。
- 本版对话中有 **4 条**工具回显被 ChatGPT 自己抹掉（`redacted`）；页面里的 `sandbox:/mnt/data/...` 链接不可下载。
