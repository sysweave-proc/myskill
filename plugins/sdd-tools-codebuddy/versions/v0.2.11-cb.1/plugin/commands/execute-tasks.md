---
description: 波次式自主执行任务 / Wave-based autonomous task execution
argument-hint: "[task-id] [--task-group <group>] [--retries <n>] [--max-parallel <n>]"
allowed-tools: ["Task", "TaskOutput", "TaskStop", "Read", "Write", "Glob", "Grep", "Bash", "AskUserQuestion", "TaskList", "TaskGet", "TaskUpdate"]
---

Run the **execute-tasks** workflow with: $ARGUMENTS

1. **Load the skill and follow it exactly:**
   - Read `${CODEBUDDY_PLUGIN_ROOT}/skills/execute-tasks/SKILL.md`
   - If that path is not resolvable, glob `**/agent-alchemy-sdd-tools/skills/execute-tasks/SKILL.md`

2. **Arguments:** optional `[task-id]` to run one specific task; `--task-group <group>` filters by `metadata.task_group`; `--retries <n>` (default 3); `--max-parallel <n>` (default 5, overrides the settings file).

3. **Not the same as `/run-tasks`:** this is the single-orchestrator executor (per-task agents + shared `execution_context.md`). `/run-tasks` is the Agent-Teams engine (wave-lead → context manager → executors) in the same plugin. Use this one by default; switch to `/run-tasks` when you want team-based waves, `--phase` filtering, or `--dry-run`.

4. **Resilience:** session state lives in `.codebuddy/sessions/__live_session__/`; an interrupted run resumes from the next unblocked wave instead of restarting.
