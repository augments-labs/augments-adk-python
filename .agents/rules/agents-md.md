---
paths:
  - "AGENTS.md"
  - "CLAUDE.md"
---

# AGENTS.md and CLAUDE.md

- There is exactly one `AGENTS.md`, at the repository root, and it is the
  real instructions file. Never add nested `AGENTS.md` or `CLAUDE.md` files.
- The root `CLAUDE.md` stays a one-line `@AGENTS.md` import. Never turn
  either file into a symlink.
- `AGENTS.md` holds what every session needs: setup, commands, layout,
  workflow, where the rules live, and short **Memories**. Keep it under
  200 lines, in plain, friendly prose with headers and bullets.
- It never records architecture decisions or their history. A rule that
  applies everywhere goes in `.agents/rules/architecture.md`; a rule for part
  of the codebase goes in its own `.agents/rules/<topic>.md` with `paths:`
  front matter; a multi-step procedure becomes a skill in `.agents/skills/`.
- A memory is one or two sentences about something that surprised a
  session and would surprise the next one. Delete memories that stop being
  true.
