---
description: 文档管理（MkDocs / 独立 markdown）/ Documentation management workflow
argument-hint: [action-or-description]
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Task", "AskUserQuestion", "TeamCreate", "TeamDelete", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet", "SendMessage"]
---

Run the **docs-manager** workflow for: $ARGUMENTS

1. **Load the skill and follow it exactly:**
   - Read `${CODEBUDDY_PLUGIN_ROOT}/skills/docs-manager/SKILL.md`
   - If that path is not resolvable, glob `**/agent-alchemy-dev-tools/skills/docs-manager/SKILL.md`

2. **Actions:** `$ARGUMENTS` encodes the action (generate / update / change-summary) and scope. If it is empty or ambiguous, run Phase 1 interactive discovery via `AskUserQuestion` instead of guessing.

3. **Cross-plugin dependency:** Phase 3 loads `deep-analysis` from the sibling plugin `agent-alchemy-core-tools` (`${CODEBUDDY_PLUGIN_ROOT}/../agent-alchemy-core-tools/skills/deep-analysis/SKILL.md`); if that path does not resolve, glob `**/agent-alchemy-core-tools/skills/deep-analysis/SKILL.md`.

4. **Complete all applicable phases** — interactive discovery, project detection & setup, codebase analysis, documentation planning (user-approved), documentation generation (via `docs-writer` agents), integration & finalization.
