# Codex toolkit

Use [communication](skills/codex-communication-pact/SKILL.md) for user-facing and internal messages. User-facing output follows the user's language; internal agent prose uses concise English.

## Delivery

The [portable route table](skills/codex-orchestration-pact/SKILL.md#portable-route-table) owns routing. Existing `agents/*.toml` own configured model and reasoning values. Keep this file as navigation and repository boundaries, not another route or model table.

Apply a ready instruction/profile specification as one connected editing task. File count, the word "optimization", and an iteration number do not require planning agents or strict dispatch. Use only the pacts relevant to the requested artifact.

For changes to durable agent instructions, profiles, tool descriptions or routing, apply the [documentation pact's scoped instruction audit](skills/codex-documentation-pact/references/documentation-pact.md#аудит-агентских-инструкций) as part of authoring and any already-required review. Ordinary product changes do not trigger an audit of the toolkit.

Subject owners read applicable user and project rules before dependent work, including direct work without delegation; use [Project requirements](skills/codex-orchestration-pact/SKILL.md#project-requirements). Ordinary coordination uses bounded assignments, original sources and concise inline results; root may read relevant evidence. Only explicit `dispatcher_only` or active strict continuation uses reference-only routing and role-owned reports under the [mode boundary](skills/codex-orchestration-pact/SKILL.md#dispatcher-invariant).

Use existing tools. Creating auxiliary automation or measurement infrastructure requires a separate direct user request for that deliverable. An agent-created assignment, forecast saving, or unavailable check does not grant that permission. Ordinary implementation code within a requested product change is not auxiliary process infrastructure.

## Repository boundaries

`skills/` and `agents/` are canonical sources. Preserve public names, paths, unrelated edits and `backup/**`. The only release number lives in [CHANGELOG](CHANGELOG.md); [versioning](docs/versioning.md) describes how to read it.

Installations, dependencies, hooks, external services, consumer-repository changes, commits, tags, pushes and PRs need their applicable user authorization. An instruction edit does not authorize installing or exercising the edited procedures.

## Verification status

Follow the task's explicit execution limits. Use existing permitted checks and ordinary reading; when excluded or unavailable, leave them unrun and report that boundary. The common verification-means rule is in the [orchestration pact](skills/codex-orchestration-pact/SKILL.md#general-rule-for-verification-means).

Implementation, independent approval and runtime observation are different facts. Never mark an unperformed check as passed or implementation completion as independent approval.
