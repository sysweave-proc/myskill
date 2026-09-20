---
description: 规格质量体检（矛盾/遗漏/歧义）/ Analyze a spec for quality issues
argument-hint: "[spec-path]"
allowed-tools: ["AskUserQuestion", "Task", "Read", "Glob", "TaskCreate", "TaskUpdate", "TaskList"]
---

Run the **analyze-spec** workflow on: $ARGUMENTS

1. **Load the skill and follow it exactly:**
   - Read `${CODEBUDDY_PLUGIN_ROOT}/skills/analyze-spec/SKILL.md`
   - If that path is not resolvable, glob `**/agent-alchemy-sdd-tools/skills/analyze-spec/SKILL.md`

2. **Spec path is required:** if `$ARGUMENTS` is empty, ask the user which spec file to analyze (`specs/*.md`).

3. **Two outputs:** a markdown report (`{name}.analysis.md`) and a reviewable HTML report (`{name}.analysis.html`, built from `skills/analyze-spec/templates/review-template.html`). Walk the user through Critical/Warning findings before offering to create fix tasks.

4. **Fix tasks (optional):** findings can be turned into tasks grouped as `spec-fixes-{spec-name}`, then executed via `/run-tasks --task-group spec-fixes-{spec-name}`.
