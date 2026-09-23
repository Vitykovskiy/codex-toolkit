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

## Project requirements

Before a subject decision or change that depends on them, read the applicable original user requirements, project rules and skill limits: DoD, code style and placement, architecture and dependencies, product/API/data/UI contracts, and relevant security, documentation, verification and release conditions. This applies to direct work without delegation as well. Reading this section does not activate orchestration, strict mode or another approval stage. Requirements must be obtained and applied; a separate scout run is not required by default.

Reuse requirements already read and still current for the affected scope. If rules are unknown, scattered across sources or span multiple areas in an orchestrated task, the orchestrator assigns their collection to the existing `scout`, combining it with an ongoing scout assignment when possible. Give the scout the original task, known scope and limits. Complete the relevant collection before dependent analysis, design or changes; independent work may continue. For a simple local edit, its owner reads applicable rules directly. A pure lookup of one fact that does not prepare subject work retains the narrow scout scope. A developer does not spawn agents: read one available source directly or ask the orchestrator for additional investigation.

Start from the original request and applicable `AGENTS.md` / `AGENTS.override.md`, including instructions for affected directories, following their actual discovery and precedence rather than assuming both files apply. Navigate the project's README, contributing guidance, documentation, accepted decisions and configuration by relevance; project-specific names and paths are not universal toolkit requirements. Read the relevant sections, conditions, exceptions and linked normative sources needed to understand them, without loading unrelated documentation. For each applicable rule, retain its wording or an accurate sufficient excerpt, source and section or lines, scope and conditions; preserve force, exceptions, numbers and identifiers. Separate recommendations and history from current rules. Existing code is implementation evidence, not automatic proof of a rule; an internet recommendation is not a project mandate. Scout web searches retain their confidentiality and non-execution limits.

The scout returns the inspected scope, applicable rules and sources, material unread sources, conflicts and unknowns. “Not found in the inspected scope” does not prove global absence. As a prose guide, pass the task and affected scope; each rule with source, scope and conditions; authorization limits; gaps and their effect; and the known source/project revision. This is not a new machine schema. The orchestrator supplies each participant all rules applicable to its assignment, including shared and cross-part constraints. Narrow the scope to the assignment without dropping applicable rules. Put a small set in the assignment; a large set may use a precise, accessible report or section link that the recipient must actually read before dependent work. Include critical execution limits directly. Without shared file access, send the necessary text in an accessible message. A link, a file's existence or another agent's message is not proof that the recipient read the content; an available but unread document is not an unavailable source.

Analysts use the original rules to resolve their assigned uncertainty without replacing user requirements or expanding authority. Architects and decomposers preserve them in decisions and assignments without restating a ready specification merely for this procedure. Developers and mechanical owners read assigned rules, actual work files and applicable local instructions, distinguish implementation choices from normative criteria and report newly discovered scope before dependent changes. Reviewers receive the original goal and current applicable rules from the orchestrator independently of the developer's account; they check the actual changes and affected-path instructions against primary sources, including rules the scout may have missed. `reviewer_fast` does so only for literal non-semantic changes and routes semantic findings to the existing substantive reviewer. Quality owners use project rules alongside confirmed charter/preferences; observations and proposals do not replace a normative source. The corresponding Astra profiles follow the same duties without changing their invocation conditions.

Original project documents and the user request remain authoritative; extracted rules are task working context, not a second rulebook or the scout's private memory. A short ordinary task can keep them in the assignment context. When persistence is needed, use the existing task state and one assigned collection result; in strict mode use the existing report fields, with the envelope only as notification. On resume or agent replacement pass the original goal, relevant rules or a readable exact link, limits and open questions; do not assume inherited chat history. Reuse current extracted rules without a scout rerun just because the session or role changed. A changed scope, source rule or original requirement calls for rechecking the affected subset; uncommitted changes matter, so unchanged HEAD alone does not establish currency. Use available versions, diff and task state, without new hashers or registries. Pass newly discovered rules to the executor and reviewer; a subject owner assesses affected results without voiding unrelated accepted work.

Resolve instruction conflicts by established precedence and scope. Refer unresolved subject ambiguity to the appropriate analyst or architect and a necessary user decision through the orchestrator; pause only dependent work. If a required criterion cannot be evidenced under current execution limits, name the source, conflict and missing evidence without claiming completion. Collecting a DoD does not authorize new tests, validators, check scripts or process automation: the [general rule for verification means](#general-rule-for-verification-means) still applies.

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
