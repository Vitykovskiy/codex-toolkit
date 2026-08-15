---
name: codex-orchestration-pact
description: Apply the lean Codex custom-agent orchestration protocol. Use only when the user explicitly requests orchestration or delegation, an applicable mandatory skill or AGENTS.md requires subagents, or the task requires coordinated independent work.
---

# Codex Orchestration Pact

Read `references/complex-task-orchestration.md` — the sole canonical orchestration pact.

Use only these globally registered role names: `scout`, `analyst`, `architect`, `decomposer`, `mechanical`, `developer`, `reviewer`, and `integration_reviewer`.

For a handoff command, read `references/continuity/create-handoff.md`. For a resume command, read `references/continuity/resume-orchestration.md`. Use the canonical files under `references/templates/` when those procedures require templates.

Preserve the canonical reference without weakening. Do not silently substitute a model or role.

When active, root is only the process dispatcher and finite-state controller. Subject-matter facts, requirements, architecture, decomposition, implementation, verification, and review belong exclusively to their registered role owners. Runtime state is file-backed under `.codex/tmp/tasks/<task-id>/`.
