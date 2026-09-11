# Codex toolkit

Use [communication](skills/codex-communication-pact/SKILL.md) for user-facing and internal messages. User-facing output follows the user's language; internal agent prose uses concise English.

## Delivery

The [portable route table](skills/codex-orchestration-pact/SKILL.md#portable-route-table) owns routing. Existing `agents/*.toml` own configured model and reasoning values. Keep this file as navigation and repository boundaries, not another route or model table.

Apply a ready instruction/profile specification as one connected editing task. File count, the word "optimization", and an iteration number do not require planning agents or strict dispatch. Use only the pacts relevant to the requested artifact.

Use existing tools. Creating auxiliary automation or measurement infrastructure requires a separate direct user request for that deliverable. An agent-created assignment, forecast saving, or unavailable check does not grant that permission. Ordinary implementation code within a requested product change is not auxiliary process infrastructure.

## Repository boundaries

`skills/` and `agents/` are canonical sources. Preserve public names, paths, unrelated edits and `backup/**`. Keep one skill version under [versioning](docs/versioning.md), and document actual delivery changes in [CHANGELOG](CHANGELOG.md).

Installations, dependencies, hooks, external services, consumer-repository changes, commits, tags, pushes and PRs need their applicable user authorization. An instruction edit does not authorize installing or exercising the edited procedures.

## Verification status

Follow the task's explicit execution limits. For authorized verification, use the optional project check documented in [README](README.md#необязательная-структурная-проверка). When the user excludes tests or verification, leave them unrun and report that boundary; do not replace them with an unsolicited validator or reviewer.

Implementation, independent approval and runtime observation are different facts. Never mark an unperformed check as passed or implementation completion as independent approval.
