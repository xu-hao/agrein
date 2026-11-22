# Skills and native packaging

All four workflows use Agent Skills Markdown with YAML `name` and `description`
frontmatter, keeping each skill scoped to one activation trigger while pushing
operational detail into progressive references:

- [ticket-delivery](https://github.com/xu-hao/agrein/blob/main/skills/ticket-delivery/SKILL.md)
  tracks single-ticket work before editing, isolates execution in a dedicated
  `git worktree`, captures complete test logs without truncating pipes, lands
  with `Closes #N`, cleans up safely with `git cherry`, and closes with a concise
  handoff.
- [Worktrees and cleanup](https://github.com/xu-hao/agrein/blob/main/skills/ticket-delivery/references/worktrees-and-cleanup.md)
  covers ticket-scoped isolation paths, full-log capture, and squash-safe cleanup.
- [epic-queue](https://github.com/xu-hao/agrein/blob/main/skills/epic-queue/SKILL.md)
  wires native GitHub parent/sub-issue relationships, derives an explicit
  dependency DAG upfront to batch owner questions, runs read-only feasibility
  probes and contract derivations in parallel against `main` while serializing
  owner rulings, and dispatches every ready DAG frontier node (interior or leaf)
  to dedicated workers with delta-only handbacks.
- [Native GitHub sub-issues and worker briefs](https://github.com/xu-hao/agrein/blob/main/skills/epic-queue/references/github-sub-issues.md)
  shows numeric `.id` attachment, dependency DAG frontier buckets, `main`-advance
  ancestry checks, and worker brief fields.
- [bug-investigation](https://github.com/xu-hao/agrein/blob/main/skills/bug-investigation/SKILL.md)
  measures and reproduces defects before editing, steps back to the general
  problem class, proves pre-existing failure claims against `origin/main`, fixes
  invalid internal producers rather than consumer fallbacks, and locks in a
  failing behavioral test first.
- [owner-escalation](https://github.com/xu-hao/agrein/blob/main/skills/owner-escalation/SKILL.md)
  reserves owner prompts for unsettled product/policy rules, presents standalone
  jargon-free choices with exact before/after states and option costs, enforces
  per-operation live approval gates, and structures four-section decision handoffs.
- [Worked rulings, approval gates, and handoffs](https://github.com/xu-hao/agrein/blob/main/skills/owner-escalation/references/worked-rulings-and-gates.md)
  provides a complete worked question, the live-operation approval table, and
  handoff examples.

## One payload, three wrappers

| Host | Metadata | Shared content |
| --- | --- | --- |
| Codex | `plugin.json` and `.agents/plugins/marketplace.json` | `skills/*/SKILL.md` |
| Claude Code | `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` | `skills/*/SKILL.md` |
| Antigravity | `.antigravity-plugin/plugin.json` | `skills/*/SKILL.md` |

The marketplace source `./` resolves to the repository root. Default skill discovery
loads the exact same four folders for every host; no per-host skill path override
is needed. `CLAUDE.md` is a contributor-instruction symlink to `AGENTS.md`, not another
skill or plugin payload. Manifests share the plugin name and release version.

The formats and native install paths follow the official
[Codex plugin guide](https://developers.openai.com/plugins/build/plugins),
[Claude Code manifest reference](https://code.claude.com/docs/en/plugins-reference),
and [Antigravity plugin guide](https://antigravity.google/docs/build-plugins).

## Capability and authorization boundaries

Native clients own discovery and activation. Installation alone does not guarantee
that an agent invokes a skill; use the project trigger in [Quickstart](quickstart.md).
These instructions do not enforce actions at the host's tool boundary, create a
scheduler, add a GitHub integration, or grant new permissions.

Native epic relationships need GitHub access. Dedicated workers need a host with
subagent support. If a capability is missing, report it and settle an alternative
execution plan. Do not claim native parenting or delegation happened without it.
An assigned leaf worker executes its own ticket directly. Ready DAG frontier
nodes and upfront read-only probes can run concurrently; unsettled owner rulings
run sequentially in the foreground.

Explicit owner instructions and canonical project contracts govern execution.
Read-only work, ticket maintenance, and workstation setup need no change ticket.
Changed-state exchanges end with a handoff; read-only answers finish directly.
