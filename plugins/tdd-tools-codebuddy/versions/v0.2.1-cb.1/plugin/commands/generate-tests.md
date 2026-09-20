---
description: 从验收标准或既有代码生成测试文件 / Generate test files from criteria or code
argument-hint: <spec-path|task-id|file-path>
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Task", "AskUserQuestion", "TaskGet", "TaskList"]
---

Run the **generate-tests** workflow for: $ARGUMENTS

1. **Load the skill and follow it exactly:**
   - Read `${CODEBUDDY_PLUGIN_ROOT}/skills/generate-tests/SKILL.md`
   - If that path is not resolvable, glob `**/agent-alchemy-tdd-tools/skills/generate-tests/SKILL.md`

2. **Mode detection:** the workflow auto-detects the mode from `$ARGUMENTS` — criteria-driven (spec path or task ID) or code-analysis (source file path). Framework is auto-detected (pytest / Jest / Vitest).

3. **Parallelism:** use `test-writer` agents for parallel test-file generation when more than one file is involved; keep generated tests behavior-driven, not implementation-mirroring.
