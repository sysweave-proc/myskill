---
description: 波次式自主执行 TDD 任务对 / Wave-based autonomous TDD task execution
argument-hint: "[--task-group <group>] [--max-parallel <n>] [--retries <n>]"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Task", "TaskOutput", "TaskStop", "AskUserQuestion", "TaskCreate", "TaskGet", "TaskList", "TaskUpdate"]
---

Run the **execute-tdd-tasks** workflow with: $ARGUMENTS

1. **Load the skill and follow it exactly:**
   - Read `${CODEBUDDY_PLUGIN_ROOT}/skills/execute-tdd-tasks/SKILL.md`
   - If that path is not resolvable, glob `**/agent-alchemy-tdd-tools/skills/execute-tdd-tasks/SKILL.md`

2. **Flags:** `--task-group <group>` filters tasks by `metadata.task_group`; `--max-parallel <n>` caps per-wave parallelism (default 5); `--retries <n>` sets retry attempts for failed/partial tasks (default 3). Flags override the settings file.

3. **Routing:** TDD task pairs go to the `tdd-executor` agent (6-phase RED-GREEN-REFACTOR); non-TDD tasks route to the `task-executor` agent from the sibling `agent-alchemy-sdd-tools` plugin. If that agent cannot be resolved, execute non-TDD tasks inline.

4. **Resilience:** session state lives in `.codebuddy/sessions/__live_session__/` and the run is resumable — on interruption, continue from the next unblocked wave instead of restarting.
