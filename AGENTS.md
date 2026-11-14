# Contributing to xu-hao/agrein

- This repository is a pure two-skill, three-host plugin. Preserve shared `skills/`
  discovery across Codex, Claude Code, and Antigravity; do not add a Python runtime
  package or duplicate host-specific skill copies.
- Use the repository's `skills/ticket-and-epic/SKILL.md` workflow for tracked changes
  and `skills/handoff-and-escalation/SKILL.md` for owner rulings, operation gates,
  and final handoffs. An assigned leaf worker implements its ticket directly.
- Track changes before implementation. Develop, test, and commit in a dedicated
  ticket worktree from `origin/main`; keep the primary checkout read-only during
  development. Name external environments, scratch artifacts, and logs by ticket.
- Keep all examples, docs, issues, and PRs self-contained to `xu-hao/agrein`.
  Cite tickets with a sentence explaining their work. Record settled general
  rules in canonical docs immediately; resolve engineering choices in-session.
- For bugs, reproduce with a failing behavioral test before production changes.
  Verify observable packaging and failure behavior, not prose phrase matches.
- Run `./scripts/check` with the ticket environment on `PATH`; use `agc run` and
  `agc land` when available. PRs must include `Closes #N`. Keep generated output
  untracked, review the final diff, and clean merged ticket artifacts.
- Landing approved PRs follows repository gates. Each release, deployment,
  package upload, host/service installation, or state reset needs explicit owner
  authorization; honor approval already granted for the exact operation.
