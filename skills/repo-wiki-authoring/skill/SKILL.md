---
name: repo-wiki-authoring
description: "Author a repository-level architecture / system-design documentation set for ANY large codebase: a nested topic tree of 'map' pages (overall layering, module boundaries and responsibilities, data-flow panoramas, dependency direction) plus cross-cutting knowledge cards, where every claim carries a source coordinate (file path + line range). Use when the user asks to 生成或复刻仓库 wiki、整个项目的架构文档、系统设计文档、架构概览、模块职责说明、repo wiki、architecture overview、system design docs，或要把一个大仓库（几万到几十万行）写成地图式导航文档。SCOPE BOUNDARY (hard): this is MACRO documentation only — it must NOT absorb or restate single-mechanism deep-dives (real call chains, 'why this design' reasoning, per-step semantics). Those belong to the repo's source-reading notes; the two stay cleanly divided and cross-linked, never merged."
metadata:
  version: 0.2.0
  scope: "global / cross-project (any repository)"
  canonical: "notes-hub/infra/skills/repo-wiki-authoring/ (git 正本)；~/.codebuddy/skills/repo-wiki-authoring/ (安装产物)"
  worked-example: "optional — if a `wiki/` layer is archived in a project of the notes-hub repo, read it as a full-scale sample (e.g. notes-hub/projects/mysql/wiki/repowiki/: 211 content pages + topic cards + module cards). The templates below are complete without it."
---

# Repo Wiki Authoring

Produce the **top-down, map-first** documentation family for any repository: what the code is divided into, who owns what, how data flows through it, and where the source coordinates are.

Applies to **any** large project (C/C++, Rust, Go, Java, Python, monorepos…). Nothing here is language- or project-specific; only the worked example happens to come from one codebase.

## Scope boundary (read this first)

Two documentation families coexist around a codebase and **must not be mixed**. This skill is strictly the first one:

| | **This skill — macro docs (map)** | **Source-reading notes (terrain)** |
|---|---|---|
| Direction | top-down: 先地图后细节 | bottom-up: 先心智模型后实现 |
| Unit | subsystem / cross-cutting theme / module | one single mechanism |
| Answers | 这块代码干什么、边界在哪、数据怎么流、依赖朝哪 | 为什么这样设计、每一步发生什么、改一行会怎样 |
| Coordinates | **coarse spans** (`#L24-123`, within the file) | **file + symbol names** + real call chains（行号非必需） |
| Figures | mermaid (layering / sequence / state / dependency) | data-flow, state machine, indented call-tree |
| Depth | stops at "what & where" | goes to "why & how" |

Rules that follow from the boundary:
- Do **not** write mechanism deep-dives here. If a page needs to explain "why this design instead of the obvious alternative", that content belongs in the notes — link to it instead.
- Do **not** duplicate an explanation across both. **Each fact has exactly one authoritative home**; the other side links to it.
- If the target repo already has a notes repo (look for a `*-notes` repo — or, in the `notes-hub` repo, a `projects/<name>/` directory — containing an `AGENTS.md`), read that method first, then keep this skill's output complementary and cross-linked.

## Two product families — know which one you are writing

| | `content/**` (仓库 wiki) | `knowledge/**` (知识卡) |
|---|---|---|
| Shape | One page = one subsystem; nested topic dirs, 3–4 levels | One doc = one **cross-cutting** theme (错误处理/日志/配置/构建…) or one **module** |
| Head | `<cite>` 引用文件清单 | YAML frontmatter (`kind/name/category/scope/source_files`) |
| Skeleton | 10 fixed H2 sections (see template) | Topic: 4–5 fixed sections. Module: 5 fixed files |
| Figures | Many `mermaid` blocks, each followed by `图表来源` | Almost none; text + tables |
| Provenance | `[path:start-end](file://path#Lx-Ly)` per figure and per section | frontmatter `source_files` + inline `` `path` `` |

Default when the user just says "整个项目架构/系统设计文档" → produce **`content/**`** first (it is the map), then optionally a few `knowledge/**` cards for genuinely cross-cutting themes.

## Non-negotiable invariants

1. **Every claim carries a coordinate.** A sentence without a `file://path` reference, a figure without `图表来源`, or a section without `章节来源` is a bug.
2. **Fixed skeletons.** Do not invent section names. The 10-section content skeleton and the 4–5-section card skeleton are contracts — a reader navigates by them.
3. **One figure = one question.** `mermaid` type must match the question: layering → `graph TB`, data flow over time → `sequenceDiagram`, state/lifecycle → `flowchart TD` or `stateDiagram-v2`, type hierarchy → `classDiagram`, dependencies → `graph LR`.
4. **Coordinates are coarse on purpose — but they must stay inside the file.** Line ranges are "the relevant span" (`#L24-123`), not a precise symbol location; precision belongs to the source-reading notes, the wiki optimizes for navigability. Coarse never means "past EOF": `#L1-200` on a 60-line file is a dead anchor. Clamp the end to the file's real line count (whole file → `#L1-L<lines>`), and keep the label and the `#Lx-Ly` fragment numerically identical.
5. **Paths are repo-root-relative**, always as `file://<relpath>`, never absolute.
6. **Cover the whole repo.** If a top-level directory has no page, the map is broken.

## Workflow

Read `references/generation-workflow.md` and follow its 6 steps. In short: scan tree → cut into modules → plan the two catalog trees (write a `prompt` + `dependent_files` per page) → read sources and write each page from its template → backfill coordinates → validate with the checklist.

Prefer generating page-by-page with real `read_file` evidence; do not batch-invent content for pages you have not read sources for.

This workflow repeats for every page, so it is the one place that can trip **platform rate limits** (429 / "model access restricted"). Treat pacing as an execution convention, not as content judgement: keep concurrency narrow (1–3 pages per batch, no huge parallel tool bursts), write each page to disk the moment it is finished (the write **is** the checkpoint — `progress_status` exists for exactly this), and on a rate-limit error back off and retry the **same** batch; never fail the whole pipeline, and never mark a page `completed` when its request failed. Details in `references/generation-workflow.md` §4b.

## Bundled references

- `references/content-page-template.md` — the 10-section page skeleton, citation/coordinate syntax, mermaid selection table, mandatory closing placeholders.
- `references/knowledge-card-template.md` — `_index.yaml` / `_module.yaml` schemas, the 5-file module card, the topic-card frontmatter and section skeleton.
- `references/generation-workflow.md` — module modeling, catalog planning, per-page `prompt`/`dependent_files` conventions, validation checklist, and expected scale.
- `scripts/_validate_*.py` — runnable validation of the produced wiki: full-set acceptance (skeleton / coordinates / provenance / cross-references), coordinate audit, single-chapter check, semantic sampling, and name-staleness screening.

## Maintenance

This is a **cross-project** skill (L1 infra of the `notes-hub` repo). Its single source of truth lives in git, not on one machine:

- **仓库正本**: `notes-hub/infra/skills/repo-wiki-authoring/`
- **本机安装产物**: `~/.codebuddy/skills/repo-wiki-authoring/`（agent 实际加载这里）

User-level skills are **not** cloud-synced by the product; this git copy is the only mechanism that crosses machines. Edit the copy under `skills/repo-wiki-authoring/skill/`, then re-install it to the local skill directory:

```bash
cp -r skills/repo-wiki-authoring/skill/. ~/.codebuddy/skills/repo-wiki-authoring/
```

（若已在本机改好，反向拷贝回收，避免两处漂移。）
