---
description: Session hygiene for long builds: HANDOFF a brief, CONVENTIONS from the code, REFRESH an existing brief.
allowed-tools: Read, Bash, Write, Edit, Grep, Glob
argument-hint: handoff [topic: <t> goal: <g>] | conventions | refresh [brief path]
---
Invoke the `context-forge` skill with this input: **$ARGUMENTS**

- `handoff` with no detail: run HANDOFF, extracting the topic and goal
  from the current session yourself; create the brief under
  `.zcode/handoffs/`.
- `handoff topic: <t> goal: <g>`: run HANDOFF with the given topic and
  goal pre-filled into the scaffold.
- `conventions`: run CONVENTIONS on the project root; merge into
  AGENTS.md under the marked fence, flag conflicts instead of
  overwriting.
- `refresh [path]`: run REFRESH on the newest file in
  `.zcode/handoffs/`, or on the given path.
