---
name: codex-long-orchestration
description: Run explicit strict dispatcher workflows with durable state, role-owned reports, and independent acceptance.
---

# Long orchestration

Use `dispatcher_only` only for an explicit strict dispatcher or a resumed strict workflow. File count, a normal fix/review pair, ordinary stages and continuity do not activate it.

**Mandatory:** preserve the [dispatcher invariant](../codex-orchestration-pact/SKILL.md#dispatcher-invariant). A task retold by the dispatcher accumulates distortions at successive relays. At every stage root forwards only a role, basic instruction, original text verbatim or its exact reference, and task/assignment/dependency identifiers. Root reads no subject file, prepared assignment or agent report, including excerpts or summaries, and never formulates or changes the task. No fallback or recovery waives this boundary.

Root launches the next permitted role, waits for native completion, checks routing metadata and runtime sender, and records its own compact state. Subject owners independently find primary requirements and predecessor reports, formulate and record their own working tasks, decide subject scope, and prepare needed assignments or revisions. A ready specification goes directly to its executor; architect may prepare a graph for a real decision, and decomposer remains optional for explicitly requested standalone or legacy work.

Use [Project requirements](../codex-orchestration-pact/SKILL.md#project-requirements) in each subject role before dependent decisions. The scout collects unknown or scattered rules when needed; later roles find its result themselves. Root does not transfer selected rules. Honor the [verification-means rule](../codex-orchestration-pact/SKILL.md#general-rule-for-verification-means); excluded checks remain unrun and completion is not independent approval.

Subject owners apply the common [packet boundaries](../codex-orchestration-pact/SKILL.md#scope-and-profiles), [source/context recovery](../codex-orchestration-pact/SKILL.md#context) and [acceptance evidence](../codex-orchestration-pact/SKILL.md#execution-and-acceptance). Their existing reports retain missing criteria and supporting observations; these obligations never authorize root to inspect subject evidence.

Roles atomically write their own full reports and return only compact routing envelopes. The independent reviewer checks source currency, dependencies, report correlation and foreign evidence, and accepts only supported results. Root checks the envelope without opening any referenced artifact. Routing metadata must identify the next role and assignment without requiring root to inspect a file; use the [dispatcher mode](references/dispatcher-mode.md) and [envelope](references/templates/envelope.md) contract.

Root keeps one current process state and resumes the first incomplete permitted launch without reissuing accepted work. Apply [Progress and efficiency](../codex-orchestration-pact/SKILL.md#progress-and-efficiency): show approximate completion from owner-confirmed plan totals and route stalls, repetition, excessive verification and plan/goal drift to the existing decision owner while work is active. Keep only current process fields and prepared transition references; recovery preserves the dispatcher invariant. A missing role, artifact access or safe transition is an exact checkpoint, not expanded authority. Keep generated process prose concise English and preserve exact source wording and machine values.
