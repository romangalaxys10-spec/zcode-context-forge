# Context Forge

<p align="center">
  <a href="https://z.ai/subscribe?ic=R0K78RJKNW"><img alt="z.ai coding plans - 10% OFF coupon" src="https://img.shields.io/badge/z.ai%20coding%20plans-10%25%20OFF%20coupon-blueviolet" /></a>
  <a href="https://zcode.z.ai/invite/ALWM9JUA"><img alt="Try ZCode free" src="https://img.shields.io/badge/Try%20ZCode-free%20invite-0969da" /></a>
</p>

Session hygiene for long builds: hand the context off, or pull it back
out, without quality loss.

## Why

Long sessions die two ways. The build hits a session boundary and the
next session re-derives the decisions from scratch, silently breaking
one. Or the project rules live in the heads of the people who wrote
them, so every new session guesses at style and ends up inconsistent.
Context Forge covers both: a dated handoff brief for resuming, and
code-derived conventions with evidence for new sessions.

## How it works

| Command | Output |
| ---- | ---- |
| HANDOFF | `.zcode/handoffs/<date>-<topic>.md` with goal, decisions (reason + evidence), invariants, file map, current state, next steps, open questions |
| CONVENTIONS | project rules merged into AGENTS.md, each with file:line evidence; conflicts flagged, never silently overwritten |
| REFRESH | an existing brief updated in place, with an appended update log |

Shared rule: a brief is facts extracted from the session and the code,
never invented. Every claim carries a pointer; what cannot be pointed
to moves to open questions.

## Install

Option A (self-installable marketplace):

1. Download or clone this repo folder to your machine.
2. Open ZCode, Plugin Marketplace, Add, Add Plugin Marketplace.
3. Paste the path to this folder and pick `context-forge`.
4. Install.

Option B (manual): copy this folder into your ZCode workspace `plugins/`
directory and restart ZCode.

## Try it

```
/context-forge handoff topic: checkout-flow goal: finish the coupon code path
```

Expected result: a fresh `.zcode/handoffs/2026-10-29-checkout-flow.md`
with every template section filled from the session, each claim
pointing at file:line or the user request, plus the single next step.

## Requirements

- Python 3 (stdlib only, for `brief_scaffold.py`)

---

<p align="center">
  <a href="https://z.ai/subscribe?ic=R0K78RJKNW"><img alt="z.ai coding plans - 10% OFF coupon" src="https://img.shields.io/badge/z.ai%20coding%20plans-10%25%20OFF%20coupon-blueviolet" /></a>
  <a href="https://zcode.z.ai/invite/ALWM9JUA"><img alt="Try ZCode free" src="https://img.shields.io/badge/Try%20ZCode-free%20invite-0969da" /></a>
</p>

## License

MIT
