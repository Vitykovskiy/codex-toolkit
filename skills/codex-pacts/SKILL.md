---
name: codex-pacts
description: Compatibility shim for legacy instructions that name the former aggregate Codex pact skill. Use only to route to the separate communication and orchestration pact skills; this shim contains no pact text.
---

# Codex Pacts Compatibility Shim

Apply skill `codex-communication-pact` for every task.

Apply skill `codex-orchestration-pact` only when the user explicitly requests orchestration or delegation, an applicable mandatory skill or `AGENTS.md` requires subagents, or the task is genuinely complex under the orchestration pact.

This shim contains no canonical pact text and no project customization.
