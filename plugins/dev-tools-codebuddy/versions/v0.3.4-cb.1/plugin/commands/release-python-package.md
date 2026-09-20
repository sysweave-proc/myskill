---
description: Python 包发布流程（uv + ruff）/ Python package release workflow
argument-hint: [version-override]
allowed-tools: ["Read", "Edit", "Bash", "AskUserQuestion", "Glob", "Task"]
---

Run the **release** workflow with version override: $ARGUMENTS

1. **Load the skill and follow it exactly:**
   - Read `${CODEBUDDY_PLUGIN_ROOT}/skills/release-python-package/SKILL.md` (skill `name: release`)
   - If that path is not resolvable, glob `**/agent-alchemy-dev-tools/skills/release-python-package/SKILL.md`

2. **Version:** `$ARGUMENTS` is an optional version override (e.g. `1.0.0`). If empty, the version is calculated from changelog entries.

3. **Fail fast:** stop immediately when a pre-flight or verification step fails (wrong branch, dirty working tree, failing tests). Never skip a gate to get the release through.
