---
name: context-forge
description: >
  Use at session boundaries on a long build: HANDOFF to compact the
  session into a resumable brief, CONVENTIONS to extract project rules
  from the code, REFRESH to update an existing handoff. Keep a fresh
  session from losing quality.
---

# Context Forge

Three commands. All three share one rule: a brief is facts extracted
from the session and the code, never invented. Every claim carries a
pointer (file:line, commit, or "session: user request at <time>").
A claim without a pointer gets a `?` next to it and moves to
"Open questions".

All output lives under `.zcode/` in the project root.

## Command: HANDOFF

Goal: a fresh session can resume the build without quality loss, in
one read.

1. Create the file with the scaffold script (refuses to overwrite a
   non-empty file without `--force`):

   ```bash
   python3 skills/context-forge/scripts/brief_scaffold.py \
     --topic "<short-topic>" --goal "<one-sentence goal>" \
     [--refresh .zcode/handoffs/<date>-<topic>.md]
   ```

   Default target: `.zcode/handoffs/<YYYY-MM-DD>-<topic>.md`.

2. Fill every template section from session evidence:
   - **Goal**: the one sentence from the user's original request,
     verbatim where possible, with a pointer to the request.
   - **Decisions made**: list each decision with its reason and where
     it is visible in the code (file:line or commit). Skip decisions
     you cannot locate; move them to open questions.
   - **Invariants / constraints**: rules the build must keep true
     (API shape, perf budget, "no new dependencies", ...) with the
     pointer where the rule is stated.
   - **File map**: every file touched in the session, one line each:
     path, what was done, current state (clean / dirty / WIP). Get the
     dirty/WIP list from `git status --porcelain` when available.
   - **Current state**: what runs, what does not, and how you know
     (command + observed output, trimmed).
   - **Next steps**: ordered, each ending at a verifiable state
     ("test X passes", "user confirms Y").
   - **Open questions**: everything without a pointer, plus anything
     you deferred.

3. Trim the brief to under 150 lines. A longer brief is not a
   handoff, it is a dump.

4. Tell the user the file path and the single next step.

## Command: CONVENTIONS

Goal: AGENTS.md (or the project's equivalent) states the rules the
code actually follows, each with evidence, so new sessions stop
guessing.

1. Read the codebase structure first: `Glob` for the source layout,
   entry points, test files, one error-handling site, one API
   boundary.
2. Derive candidate rules in these buckets:
   - naming (file, variable, test names)
   - structure (where new code of each kind goes)
   - test patterns (framework, assertion style, fixture convention)
   - error handling (throw/return, log-and-swallow sites)
3. For each rule, capture `file:line` evidence. A rule with fewer
   than 2 supporting sites goes under "Observed, unconfirmed" instead
   of the conventions list.
4. Merge into `AGENTS.md` under a clearly marked section
   (`<!-- context-forge: conventions -->` fence), keeping existing
   content. When a new rule contradicts an old one, keep the old rule
   and raise the conflict as an open question; do not silently
   overwrite user-written rules.
5. Report: how many rules landed, where, and which conflicts you
   flagged.

## Command: REFRESH

Goal: an existing handoff stays true after more work.

1. Find the target: newest file in `.zcode/handoffs/`, or the one the
   user named.
2. Re-run the HANDOFF extraction for the sections that changed
   (typically File map, Current state, Next steps; Decisions when a
   new choice was made).
3. Update those sections in place. Keep a `## Update log` section at
   the bottom and append one dated line per refresh: what changed,
   with pointers.
4. Do not delete prior content except where it is superseded; a
   superseded line gets `~~struck~~` and a pointer to the replacement.

## Guardrails

- Never invent a file, decision, or constraint to fill a section.
  An empty section reads "none found" and moves on.
- Never merge CONVENTIONS rules that contradict explicit user or
  AGENTS.md rules without flagging the conflict.
- The scaffold refuses to overwrite a non-empty brief without
  `--force`; treat a refused overwrite as "refresh that file instead".
- A brief you cannot back with pointers is not a brief; say what is
  missing.

## Script notes

`scripts/brief_scaffold.py` is stdlib-only and cross-OS. It creates
the dated handoff file with the template sections pre-filled from CLI
args (`--topic`, `--goal`), creates `.zcode/handoffs/` if needed, and
exits 0 (created), 3 (refused: target exists and is non-empty, use
`--force`), 4 (bad arguments).
