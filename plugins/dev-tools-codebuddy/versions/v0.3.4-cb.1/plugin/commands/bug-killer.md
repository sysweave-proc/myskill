---
description: 系统化 bug 排查（假设驱动）/ Systematic hypothesis-driven debugging
argument-hint: [bug-description-or-error] [--deep]
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Task", "AskUserQuestion", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet", "SendMessage"]
---

Investigate and fix this bug: $ARGUMENTS

1. **Load the skill and follow it exactly:**
   - Read `${CODEBUDDY_PLUGIN_ROOT}/skills/bug-killer/SKILL.md`
   - If that path is not resolvable, glob `**/agent-alchemy-dev-tools/skills/bug-killer/SKILL.md` and read it from there

2. **`--deep` flag:** if `$ARGUMENTS` contains `--deep`, skip triage routing and go directly to the deep track.

3. **Discipline:** investigation must precede any code change. Every hypothesis goes into the hypothesis journal, and no fix is applied before the root cause is confirmed with evidence.

4. **Complete ALL 5 phases** — triage & reproduction, investigation, root cause analysis, fix & verify, wrap-up & report. Phase 5 also dispatches `project-learnings` when a project-specific insight was found.
