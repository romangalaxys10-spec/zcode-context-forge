# Changelog

## 0.1.0 - 2026-10-29

- Initial release: session hygiene for long builds with three commands:
  HANDOFF (dated brief under `.zcode/handoffs/` covering goal, decisions
  with reasons, invariants, file map, current state, next steps, open
  questions), CONVENTIONS (code-derived rules merged into AGENTS.md,
  each with file:line evidence), and REFRESH (in-place update of an
  existing brief with an appended update log).
- Every claim in a brief carries a pointer; unpointed claims move to
  open questions instead of being invented.
- `brief_scaffold.py`: stdlib scaffold that creates the dated handoff
  file from CLI args and refuses to overwrite a non-empty file without
  `--force`.
