---
description: Agent Teams 波次并行执行（支持 --dry-run）/ Agent-Teams based wave execution
argument-hint: "[<task-id>] [--task-group <name>] [--phase <N,M>] [--max-parallel <N>] [--retries <N>] [--dry-run]"
allowed-tools: ["TaskList", "TaskGet", "TaskUpdate", "TaskCreate", "SendMessage", "TaskOutput", "TaskStop", "Task", "AskUserQuestion", "Read", "Write", "Edit", "Glob", "Grep", "Bash"]
---

Run the **run-tasks** workflow with: $ARGUMENTS

1. **Load the skill and follow it exactly:**
   - Read `${CODEBUDDY_PLUGIN_ROOT}/skills/run-tasks/SKILL.md`
   - If that path is not resolvable, glob `**/agent-alchemy-sdd-tools/skills/run-tasks/SKILL.md`

2. **Arguments:** optional positional `<task-id>`; `--task-group <name>`; `--phase <N,M>` (comma-separated phase numbers); `--max-parallel <N>`; `--retries <N>`; `--dry-run` (print the execution plan and stop — no code changes).

3. **Engine shape:** topological wave assignment → each wave gets a `wave-lead` (opus) that builds its own team, spawns a `context-manager` when the wave has ≥3 tasks, dispatches one `task-executor-v2` per task, applies the 3-tier retry model, and reports back; the orchestrator aggregates wave summaries.

4. **Settings:** `.codebuddy/agent-alchemy.local.md` under the `run-tasks.*` namespace (`max_parallel`, `max_retries`, `retry_partial`, `context_manager_threshold`, `wave_lead_model`, `context_manager_model`, `executor_model`). CLI flags override the file, which overrides the defaults. A missing or malformed settings file is never an error.

5. **Knowledge base:** this engine's message protocols and tool conventions come from the sibling plugin `agent-alchemy-claude-tools` (`skills/claude-code-teams/`, `skills/claude-code-tasks/`) — install it in the same marketplace.
