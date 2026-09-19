---
name: codex-orchestration-pact
description: Select a minimal coordination route with bounded scope and independent acceptance where required.
---

# Orchestration pact

Use this pact for requested orchestration or actual coordination. A ready local edit can be performed directly. Select the route once; revise it only for a material change in scope, evidence or responsibility.

## General rule for verification means

Every role — orchestrator, architect, developer and reviewer — implements the requested result. Creating new unit, integration or other tests, validators, check scripts, or other auxiliary automation to verify implementation or maintain the process is outside orchestration. Create such means only on the user's separate direct request to create them.

An assignment, another agent's plan, or the expected usefulness of a means does not replace that request. A temporary script, one-off checking code, and a new test case in an existing test file are also new verification means. Do not rewrite existing tests around an implementation to obtain a passing result. Product code requested by the user remains permitted implementation; a product fix or improvement alone is not an authorization to build verification infrastructure.

Existing checks, normal code reading, and independent review remain permitted within the task. Run existing permitted checks when relevant, and report unrun work honestly. Manual checking is permitted, but do not introduce a mandatory manual acceptance, user confirmation, or universal browser stage. Preserve checks explicitly required by the user. Source review is not runtime observation.

## Portable route table

| Work | Route |
|---|---|
| Ready text, instruction or mechanical configuration edit | One owner, including the current root in ordinary mode. Independent review only when the task contract or semantic risk requires it and the user permits it. |
| Connected behaviour change | One `developer`, then one independent `reviewer`. The developer resolves ordinary local implementation questions. |
| Truly independent outcomes | Coarse assignments by responsibility, at most two simultaneous writers, then one sufficient batch review. |
| Material technical decision uncertainty | One `architect` consultation that may also prepare executable assignments and write-sets. |
| A specific unanswered source or requirements question | Direct relevant reading, or one `scout` / `analyst` assignment when delegated investigation is needed. |
| Explicit strict request or continuation of active strict state | [Long orchestration](../codex-long-orchestration/SKILL.md) with role-owned reports and independent acceptance. |
| Explicit product-quality campaign | [Product quality](../codex-product-quality/SKILL.md) with its stated scope and stopping point. |

File count, a normal fix/review pair, broad wording, an iteration number, or persistence between sessions do not activate strict mode. Ordinary continuity needs the current goal, completed work, remaining work, constraints and next step in the existing state location. Strict mode remains for an explicitly requested route or active strict task. A ready specification does not need an analyst, architect or decomposer to restate it. `decomposer` remains an explicitly requested standalone or legacy-import capability, not a mandatory relay; an architect may prepare technical decomposition when needed.

## Scope and profiles

An assignment carries the goal, exact requirements, permitted changes, existing criteria, required evidence and execution limits. Keep it short; include the useful fact itself when small, not only a path that forces another read. Do not copy the whole parent conversation or peer reports.

Use existing profiles with their configured model and reasoning values. `reviewer_fast` handles only provably literal non-semantic edits. `integration_reviewer` replaces ordinary review when a named security or cross-part criterion requires it. Astra profiles require a direct applicable user request. A retry, complexity or a child-created assignment does not supply authorization.

## Execution and acceptance

The orchestrator owns organization: package size, order, dependencies, and a response to stagnation within the user's goal. It may read the necessary parts of results to assess progress, reorder independent work, and split an oversized package while preserving requirements, constraints and total scope. Each package has a complete, checkable result. Deliver a completed part for required review and integration while retaining unfinished work.

Subject roles own technical decisions, implementation and review. The orchestrator neither substitutes a technical executor nor gives independent approval to its own work. A material technical decision stays with the appropriate role; independent acceptance stays with a reviewer. In `dispatcher_only`, this separation remains while the orchestrator may perform the allowed organizational reading.

One sufficient independent review covers the requirements, implementation, related risks and relevant connections. Add another reviewer only for an explicitly named uncovered criterion. Return a defect to the same owner and reviewer; reread the changed evidence and affected dependencies, not the entire history. After two attempts without confirmed progress, change the organization of work rather than repeat the same assignment. No new counters, KPI, logs or monitoring means are introduced.

Retain the existing six-key report and acceptance contract. Batch approval identifies every assignment, attempt, goal version and required snapshot. No self-approval, duplicate or stale acceptance, incomplete result, or missing required evidence is valid. A formatting correction to a report does not restart implementation or invalidate still-current evidence. A scope escape, missing required evidence, or stale acceptance remains a substantive review issue.

Ordinary work uses inline results unless a file is an explicit deliverable. Strict work writes the canonical report atomically and returns only its envelope. Wait through native completion or blocking tools. Reuse a relevant owner context for a narrow fix; create a new context for a different responsibility. Do not create agents just to summarize, translate, poll or repackage another agent's result.

## Context

Read relevant files and ranges; expand when needed for correctness. Reuse unchanged evidence without deleting its provenance. Load conditional references only when their conditions apply.

Keep stable instructions stable, with task-specific material after them where the client permits. Use existing provider caching only; add no cache service or unsupported settings. Native context inheritance and cache reuse are not proven by prompt wording. Missing usage remains unknown and does not trigger building a meter.
