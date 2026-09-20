---
description: 把规格拆成带依赖与验收标准的任务 / Decompose a spec into dependency-ordered tasks
argument-hint: "[spec-path] [--phase <phases>]"
allowed-tools: ["AskUserQuestion", "Read", "Glob", "Grep", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet"]
---

Run the **create-tasks** workflow on: $ARGUMENTS

1. **Load the skill and follow it exactly:**
   - Read `${CODEBUDDY_PLUGIN_ROOT}/skills/create-tasks/SKILL.md`
   - If that path is not resolvable, glob `**/agent-alchemy-sdd-tools/skills/create-tasks/SKILL.md`

2. **Spec path is required:** if `$ARGUMENTS` is empty, ask the user which spec to decompose.

3. **`--phase <phases>`:** comma-separated phase numbers (e.g. `--phase 1,2`); omit to select interactively or generate all.

4. **Two modes:** *fresh* decomposition, and *merge mode* on re-run — merge uses `task_uid` so completed tasks are never touched, pending tasks are updated to match the new spec, in-progress tasks are skipped, and new requirements become new tasks.

5. **Required metadata:** every task carries acceptance criteria and `task_group` (slug from the spec title) — `task_group` is what `--task-group` filtering in `/run-tasks` and `/execute-tasks` keys off.
