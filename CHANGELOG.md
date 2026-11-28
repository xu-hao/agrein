# Changelog

## Unreleased

- Ship the concise trigger-only `AGENTS.md` instruction as a canonical root
  `AGENTS.snippet.md`; the quickstart includes it directly, tests keep it
  byte-identical to the `README.md` snippet, and the strict Antigravity payload
  check validates it alongside the skills (`#20`).

## 0.1.1 (2026-11-22)

- Update `epic-queue` and its GitHub sub-issue reference to derive explicit
  dependency DAGs from contract, code, and state prerequisites (separating hard
  contract dependencies from mergeable shared-file overlaps), run downstream
  read-only feasibility probes and contract derivations upfront in parallel
  against `main`, dispatch every ready interior or leaf frontier node, and
  recompute the frontier with `git merge-base --is-ancestor` checks whenever
  `main` advances (`#7`).
- Onboard `gardenia` managed `AGENTS.md` workflow block and `gardenia.toml`
  repository profile while preserving `agrein`-specific plugin contracts
  outside the managed markers (`#5`).

## 0.1.0 (2026-11-16)

- Initial MIT release of agrein (ag + rein, *“a grain”*) for Codex, Claude Code,
  and Antigravity using shared Agent Skills discovery.
- Add `ticket-delivery` for single-ticket issue tracking, isolated worktrees,
  complete-log behavioral verification, squash-safe `git cherry` cleanup, and
  concise completion handoffs.
- Add `epic-queue` for native GitHub sub-issues, upfront queue triage, sequential
  foreground rulings vs. parallel isolated subagent workers, and delta-only
  handbacks.
- Add `bug-investigation` for evidence-first reproduction, general problem-class
  diagnosis, `origin/main` verification of pre-existing failures, producer fixes,
  and failing behavioral regression tests.
- Add `owner-escalation` for standalone concrete before/after rulings, explicit
  per-operation live approval gates, and four-section decision handoffs.
- Add contributor packaging tests, read-only native validation, and Sphinx docs.
