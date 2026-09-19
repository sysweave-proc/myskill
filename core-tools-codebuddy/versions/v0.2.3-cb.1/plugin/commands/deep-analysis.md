---
description: 深度分析代码库 / Deep multi-agent codebase analysis
argument-hint: [analysis-context or focus-area]
allowed-tools: ["Read", "Glob", "Grep", "Bash", "Task", "TeamCreate", "TeamDelete", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet", "SendMessage", "AskUserQuestion"]
---

Run the **deep-analysis** workflow on: $ARGUMENTS

1. **Load the skill and follow it exactly:**
   - Read `${CODEBUDDY_PLUGIN_ROOT}/skills/deep-analysis/SKILL.md`
   - If that path is not resolvable, glob `**/agent-alchemy-core-tools/skills/deep-analysis/SKILL.md` and read it from there

2. **Analysis context:**
   - If `$ARGUMENTS` is non-empty, use it verbatim as the analysis context (feature area, question, or exploration goal)
   - If empty, use "general codebase understanding"

3. **Invocation mode:** this is a **direct invocation** by the user, so approval of the team plan is gated by `direct-invocation-approval` (default: `true`). Settings are read from `.codebuddy/agent-alchemy.local.md` under the `deep-analysis` section.

4. **Complete all 6 phases** — reconnaissance, dynamic planning, review & approval, team assembly, parallel exploration, synthesis, then session archive and team teardown. Do not stop early.
