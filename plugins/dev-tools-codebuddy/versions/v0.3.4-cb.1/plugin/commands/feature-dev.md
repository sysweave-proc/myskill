---
description: 功能开发全流程（探索→提问→架构→实现→评审）/ Full 7-phase feature development workflow
argument-hint: [feature-description]
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Task", "AskUserQuestion", "TeamCreate", "TeamDelete", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet", "SendMessage"]
---

Run the **feature-dev** workflow for: $ARGUMENTS

1. **Load the skill and follow it exactly:**
   - Read `${CODEBUDDY_PLUGIN_ROOT}/skills/feature-dev/SKILL.md`
   - If that path is not resolvable, glob `**/agent-alchemy-dev-tools/skills/feature-dev/SKILL.md` and read it from there

2. **Feature description:** `$ARGUMENTS` is the feature to build. If it is empty, ask the user what to build before starting Phase 1.

3. **Cross-plugin agents:** Phase 4 spawns `code-architect` agents and Phase 6 spawns `code-reviewer` agents. `code-architect` lives in the sibling plugin `agent-alchemy-core-tools` but is addressed by its bare name; if the runtime cannot resolve it, fall back to doing the architecture work inline.

4. **Complete ALL 7 phases** — discovery, codebase exploration, clarifying questions, architecture design, implementation, quality review, summary. Do not stop before Phase 7.
