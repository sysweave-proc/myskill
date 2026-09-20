---
description: 自适应访谈生成规格文档 / Create a spec via adaptive interview
argument-hint: "[context-file-or-text]"
allowed-tools: ["AskUserQuestion", "Task", "Read", "Write", "Glob", "Grep", "Bash", "TeamCreate", "TeamDelete", "SendMessage"]
---

Run the **create-spec** workflow with this context: $ARGUMENTS

1. **Load the skill and follow it exactly:**
   - Read `${CODEBUDDY_PLUGIN_ROOT}/skills/create-spec/SKILL.md`
   - If that path is not resolvable, glob `**/agent-alchemy-sdd-tools/skills/create-spec/SKILL.md`

2. **Context argument:** `$ARGUMENTS` is optional — either a file path (`.md`, `.txt`) to read or inline text describing what to build. If empty, run the interview without pre-loaded context.

3. **Adaptive interview, not a questionnaire:** pick the depth level (high-level 6-10 / detailed 12-18 / full-tech 18-25 questions), expand automatically when complexity signals are detected (confirm with the user first), and use `AskUserQuestion` for every user-facing question.

4. **Optional side-work:** codebase exploration via the `codebase-explorer` agent, and external research via the `researcher` agent — **only when the user explicitly asks for it**.

5. **Output:** write the spec to `specs/SPEC-{name}.md`. Do not stop before the file is on disk.
