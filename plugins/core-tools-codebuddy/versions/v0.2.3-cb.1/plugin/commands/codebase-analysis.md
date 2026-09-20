---
description: 代码库分析报告 / Structured codebase analysis report
argument-hint: [analysis-context or feature-description]
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Task", "AskUserQuestion", "TeamCreate", "TeamDelete", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet", "SendMessage"]
---

Run the **codebase-analysis** workflow on: $ARGUMENTS

1. **Load the skill and follow it exactly:**
   - Read `${CODEBUDDY_PLUGIN_ROOT}/skills/codebase-analysis/SKILL.md`
   - If that path is not resolvable, glob `**/agent-alchemy-core-tools/skills/codebase-analysis/SKILL.md`

2. **Analysis context:** use `$ARGUMENTS` if non-empty, otherwise "general codebase understanding".

3. **Invocation mode:** this skill loads `deep-analysis` as a reusable building block, so the analysis runs in **skill-invoked mode** (team plan auto-approved, `invocation-by-skill-approval` default: `false`).

4. **Complete ALL 3 phases** — deep analysis, reporting, and post-analysis actions. The workflow is not complete until Phase 3 (save report / update docs / address actionable insights) finishes. Do not stop after the report.
