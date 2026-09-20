---
description: 生成本次会话的变更报告 / Generate a session change report
argument-hint: [scope-or-description]
allowed-tools: ["Read", "Write", "Glob", "Grep", "Bash", "AskUserQuestion"]
---

Run the **document-changes** workflow with this scope: $ARGUMENTS

1. **Load the skill and follow it exactly:**
   - Read `${CODEBUDDY_PLUGIN_ROOT}/skills/document-changes/SKILL.md`
   - If that path is not resolvable, glob `**/agent-alchemy-dev-tools/skills/document-changes/SKILL.md`

2. **Scope:** `$ARGUMENTS` optionally names the report scope (e.g. `"auth refactor"`). If empty, infer it from commit messages or changed file paths.

3. **Stop early if there is nothing to report** — the workflow requires a git repository and actual changes; do not fabricate a report.
