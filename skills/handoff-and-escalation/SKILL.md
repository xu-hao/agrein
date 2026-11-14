---
name: handoff-and-escalation
description: >-
  Use when an owner must settle a product or policy rule, when checking approval
  for a live operation, or when ending an exchange that changed code, docs,
  tickets, infrastructure, or live state. Produce concrete choices and a complete
  four-section handoff; finish read-only exchanges directly.
---

# Handoff and escalation

## Respect the owner boundary

Ask the owner **only** for product or policy rulings left unsettled by canonical
project contracts. Read those contracts and available evidence first. Resolve
engineering forks inside the working session: investigate, measure, compare
established approaches, and choose an implementation consistent with the contract.
Do not turn ordinary implementation choices into owner approvals.

When a general rule is newly settled, record it in the canonical project docs
immediately, under the tracked ticket, before dependent execution. A chat answer
or ticket comment alone must not become the only durable specification. Batch
unsettled epic questions before autonomous execution using
[ticket-and-epic](../ticket-and-epic/SKILL.md).

## Make the ruling concrete

For each question, present:

1. The **general rule** being settled and why existing contracts leave it open.
2. One worked application showing **exact before and after states**: rendered
   lines, stored values, or paths, as appropriate. Avoid abstract labels alone.
3. Common practice and the relevant tradeoff, tied to this example.
4. **One single-select question**, with materially distinct options and a clear
   recommendation. Do not mix independent rulings into one choice or ask several
   versions of the same question.

Use plain language. Cite every ticket as `#N — one sentence summarizing the actual
work`, for example `#42 — isolate ticket scratch directories by issue number`.
Never provide bare ticket numbers or titles alone as a substitute for explaining
the work. See the [escalation and handoff reference](references/escalation-and-handoffs.md)
for a complete worked question and transition rules.

## Apply operation gates

Landing an approved PR proceeds once repository gates pass; do not request an
extra owner confirmation just to merge it. Deployments, releases, package-index
uploads, host/service installations, and state resets require explicit owner
approval **for each operation**. A merge approval does not imply release approval;
a previous release approval does not authorize the next release.

Check whether the owner already explicitly authorized this exact operation in the
current session. If so, carry it out within that scope without asking again.
Otherwise prepare the concrete reviewable result and obtain approval before
executing the live operation. Workstation setup and read-only validation follow
the tracked workflow's exceptions; installing into a live host/service is a
distinct operation. Stop at the missing approval boundary while continuing any
independent authorized work.

## End changed-state exchanges with a handoff

After any exchange that changed code, documentation, tickets, infrastructure, or
live state, end with these four sections in this order:

### 1. What I did

Describe the resulting behavior and concrete ticket work; include useful PR,
commit, release, or validation evidence. Distinguish verified results from claims
that could not be tested.

### 2. What is open

List unfinished work, parked infrastructure incidents, remaining risks, and
dependency status. Say `None.` if everything in scope is complete.

### 3. Decisions needed

List only unsettled owner product/policy rulings or missing explicit operation
approvals, using the concrete question format. Say `None.` when no ruling remains.

### 4. Options and recommendation

Give actionable options and your recommendation for the remaining work. If there
is no remaining work, say that no further action is needed. Do not invent a new
decision to fill this section.

For read-only turns, answer directly without an empty four-section shell. A
progress update inside an ongoing exchange is not a final handoff.
