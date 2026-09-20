---
description: 自适应访谈并产出结构化报告 / Adaptive interview
argument-hint: "[topic-or-context-file]"
allowed-tools: ["AskUserQuestion", "Task", "Read", "Write", "Glob", "Grep", "Bash"]
---

Run the **interview-me** workflow with this context: $ARGUMENTS

1. **Load the skill and follow it exactly:**
   - Read `${CODEBUDDY_PLUGIN_ROOT}/skills/interview-me/SKILL.md`
   - If that path is not resolvable, glob `**/agent-alchemy-core-tools/skills/interview-me/SKILL.md`

2. **Context argument:** treat `$ARGUMENTS` as the optional `context` argument — a file path (`.md`, `.txt`) or inline text that pre-loads context about the topic. If it is empty, run the interview without pre-loaded context.

3. **Every user-facing question must go through `AskUserQuestion`** — never ask via plain text. Plain text is reserved for round summaries, research findings, and the final path confirmation.

4. **Complete all phases** — settings check, initial framing, adaptive interview, interleaved research dispatch, pre-compilation summary, and output compilation. The workflow is not complete until the markdown artifact has been written to disk.
