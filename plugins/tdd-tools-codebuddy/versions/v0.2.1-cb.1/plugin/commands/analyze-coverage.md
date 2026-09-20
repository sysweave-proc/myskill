---
description: 分析测试覆盖率并给出补测建议 / Analyze test coverage and find gaps
argument-hint: "[<project-path>] [--spec <spec-path>] [--threshold <percentage>]"
allowed-tools: ["Read", "Glob", "Grep", "Bash", "AskUserQuestion"]
---

Run the **analyze-coverage** workflow on: $ARGUMENTS

1. **Load the skill and follow it exactly:**
   - Read `${CODEBUDDY_PLUGIN_ROOT}/skills/analyze-coverage/SKILL.md`
   - If that path is not resolvable, glob `**/agent-alchemy-tdd-tools/skills/analyze-coverage/SKILL.md`

2. **Arguments:** `[<project-path>]` defaults to the current working directory; `--spec <spec-path>` scopes the gap analysis to a spec's requirements; `--threshold <percentage>` sets the pass/fail bar.

3. **Output:** coverage summary plus prioritized, actionable gap recommendations (which branches/behaviors are untested and what test to add) — not just a raw percentage.
