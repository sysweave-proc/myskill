---
description: 走一遍 RED-GREEN-REFACTOR 循环 / Full RED-GREEN-REFACTOR TDD cycle
argument-hint: <feature-description|task-id|spec-section>
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Task", "AskUserQuestion", "TaskGet", "TaskList", "TaskUpdate"]
---

Run the **tdd-cycle** workflow on: $ARGUMENTS

1. **Load the skill and follow it exactly:**
   - Read `${CODEBUDDY_PLUGIN_ROOT}/skills/tdd-cycle/SKILL.md`
   - If that path is not resolvable, glob `**/agent-alchemy-tdd-tools/skills/tdd-cycle/SKILL.md`

2. **Input:** `$ARGUMENTS` is a feature description, a task ID, or a spec section. If empty, ask the user what to build before planning.

3. **Confirm the plan first**, then run autonomously: the workflow presents its TDD plan for confirmation before entering the RED-GREEN-REFACTOR phases. Do not skip the RED phase — the test must fail for the right reason before implementation starts.
