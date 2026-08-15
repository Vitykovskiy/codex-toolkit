# Codex toolkit instructions

## Mandatory skills

- Apply skill `codex-communication-pact` for every task and every user-facing message.
- Apply skill `codex-orchestration-pact` only when the user explicitly requests orchestration or delegation, an applicable mandatory skill or `AGENTS.md` requires subagents, or the task is genuinely complex under that pact.
- Apply skill `codex-development-pact` to code, test, configuration, and agent-profile work.
- Apply skill `codex-documentation-pact` to documentation, durable instructions, pact metadata, and migration maps.
- Apply skill `codex-ui-analysis-pact` only to UI analysis or UI documentation.

## Preservation rules

- Treat `backup/**` as immutable source evidence.
- Preserve canonical pact text without shortening, paraphrasing, reordering, deduplication, or weakening.
- Keep obvious project-specific rules unchanged in backup sources and move them to detailed project `AGENTS.md` only in a separately assigned task.
- Keep project customization and project rules out of all pact skills and compatibility shims.
- Keep absolute project paths and machine-specific toolkit paths out of permanent instructions, skills, maps, and agent profiles.
- Keep toolkit content canonical; install global skills and agents only through directory junctions.
- Use only `gpt-5.6-sol`, `gpt-5.6-terra`, and `gpt-5.6-luna` in custom-agent profiles. Never silently substitute a model or role.
- Do not add permanent validators, checkers, hooks, install scripts, or generated runtime state.
- Do not commit, push, open a PR, publish, or modify product repositories without explicit user permission.
- Do not treat this toolkit as a plugin. Codex `0.144.4` plugin API does not register custom agents.
