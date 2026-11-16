---
name: owner-escalation
description: >-
  Use when an unsettled product or policy rule needs an owner decision, when
  checking explicit approval before a deployment, release, upload, host
  installation, or state reset, or when writing a full four-section decision or
  incident handoff.
---

# Owner escalation

## Respect the owner vs. engineering boundary

1. Ask the owner **only** for product intent or policy rulings left open by
   existing project contracts. Read canonical documentation and code evidence
   first; apply settled rules directly without re-asking.
2. Resolve engineering forks inside the working session: measure, compare
   established approaches, and choose an implementation consistent with the
   contract. Do not turn ordinary implementation choices into owner prompts.
3. When a general rule is newly settled and the project maintains canonical specs
   or architecture docs, record that general rule in those docs under the tracked
   ticket (not only in chat or an issue comment) before dependent work builds on it.

## Present standalone, jargon-free concrete rulings

Write every owner question in plain language so a reader who was not watching the
session can lift it out and evaluate it standalone—no session-coined vocabulary,
no undefined internal terms, and no bare `#N` references. Always cite tickets as
`#N — one sentence summarizing the actual work`.

Include four elements for each question:

1. **General rule and gap:** the reusable rule being settled and why current
   project contracts leave it open.
2. **Concrete before/after state:** one worked example showing exact rendered
   lines, stored values, or paths before the change and under each option.
3. **Common practice and honest cost:** how teams typically handle the case and
   the concrete tradeoff each option gives up. An option with no real cost is
   already the answer, not a decision.
4. **One single-select choice + recommendation:** materially distinct options
   with the recommended option first and the specific reason it wins here. Never
   bundle independent rulings into a multi-select or ask variants of one question.

See [worked rulings, approval gates, and handoffs](references/worked-rulings-and-gates.md).

## Enforce per-operation live approval gates

Landing an approved PR proceeds once repository gates pass; do not ask for extra
owner confirmation just to merge it.

Deployments, tags/releases, package-index uploads, live host/service
installations, and state resets require **explicit owner approval for each
specific operation**:

- Merge approval does not imply release or deployment approval.
- Approval for one named release does not authorize the next release.
- Check whether the owner already explicitly authorized this exact operation in
  the current session; if so, execute within that scope without asking again.
- Otherwise prepare and validate the concrete artifact first, continue any
  independent authorized work, and stop cleanly at the approval boundary.

## Complete four-section decision and incident handoffs

When ending a changed-state exchange that has open owner rulings, missing
live-operation approvals, or parked infrastructure incidents, complete all four
handoff sections in order (extending the two-section baseline in
[ticket-delivery](../ticket-delivery/SKILL.md)):

### 1. What I did
Describe the resulting behavior, `#N — summary` citations, PR/commit evidence,
and verified vs. unverified claims.

### 2. What is open
List unfinished tickets, parked infrastructure outages (failing operation,
bounded retries attempted, ticket-scoped logs, and resumption condition), or
remaining risks.

### 3. Decisions needed
List only unsettled product/policy rulings or required live-operation approvals.

### 4. Options and recommendation
Restate each open problem so it stands on its own without reading §1 first, list
labelled options with explicit costs, and end with a one-sentence recommendation.
Omit §§3–4 when no owner decision or live-operation approval is needed, and
finish read-only turns directly without handoff headers.
