# Agent Instructions

## Mandatory pacts

- Follow [communication pact](.codex/communication-pact.md) in every response.
- Use `caveman:caveman` unless user asks to disable it.
- For complex or delegated work, follow [orchestration pact](.codex/complex-task-orchestration.md).
- Before changing code, documentation, or UI documentation, read the matching pact in `.codex/`.
- Do not invoke `brainstorming`; decide bounded reversible matters. Ask only for a source conflict, missing authority, or external blocker.

## Start and sources

- Start at `docs/INDEX.md`.
- For implementation read `docs/90-agents/_MOC-agents.md`, `Execution-state`, and only active wave.
- Read specification §§2–3 and 30, then task-relevant sources only; retain at most eight sourced requirements.
- Sources of truth: `TECHNICAL_SPECIFICATION.md`, `contracts/meal-plan.schema.json`, `contracts/openapi.yaml`, and `contracts/nutrients.catalog.json`.
- Examples, diagrams, code, and derived documentation never silently override protected sources; see `docs/_sources/README.md`.

## Key conventions

- Keep calculations, aggregation, semantic validation, canonicalization, and display-number rules in `packages/nutrition-core`.
- Completion mutations derive participant from session; never accept client `memberKey`.
- Identical import is a no-op; changed plans use confirmed atomic CAS replacement.
- Offline state is read-only; imported strings render as text, never `v-html`.
- Implement only v1 scope: no editor, offline mutation queue, notifications, history, or inventory.
- Contract changes update affected types, tests, examples, diagrams, and notes together.
- Preserve existing changes. Report unrelated or unexplained changes; never revert them.

## Documentation

- Follow `docs/00-meta/Documentation-pact.md` and `Update-protocol.md`.
- Update only affected atoms/MOCs in the same change set. Accepted ADRs are immutable; supersede them instead.

## Package manager and checks

Use **pnpm** only. Scripts are available after bootstrap `F0`.

| Task | Command |
| --- | --- |
| Workspace lint | `pnpm --filter <workspace> lint` |
| Workspace typecheck | `pnpm --filter <workspace> typecheck` |
| Focused test | `pnpm --filter <workspace> test -- <test-file>` |
| Wave/release gates | `docs/95-testing/Verification.md` |

Unavailable checks are `not run`, never passed by assumption.

## Agent orchestration

- Ordinary answer, diagnose, change, review, and build tasks stay with root.
- Activate orchestration only on explicit user request, a required skill/instruction, or a `complex` task; then read `.codex/complex-task-orchestration.md`.
- Use at most three subagents, one level deep, with exclusive write-sets. Subagents do not commit.
- Root owns shared contracts, integration, task state, Git, and final gates. Commit, push, and PR require explicit user authorization.
- Persist handoffs, logs, reports, and temporary work only in ignored `.codex/tmp/`; permanent `.codex` materials are tracked.

## Completion and attribution

- No TODOs, placeholders, skipped tests, weakened assertions, or unverified generated files in touched scope.
- AI commits include `Co-Authored-By: <model name> <noreply@openai.com>`.
