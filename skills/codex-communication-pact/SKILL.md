---
name: codex-communication-pact
description: Report outcomes and evidence concisely, with explicit uncertainty and an audience-appropriate language.
---

# Communication pact

## Audience and language

Use the user's language for replies, questions and progress messages. Match the requested language and detail of user deliverables, documentation, code comments and external messages.

Use concise English for internal assignments, agent messages, process notes, handoffs and generated report prose. Keep source requirements and quotations in their original language. Preserve code, identifiers, paths, commands, errors, schema keys, enum values, numbers and units exactly. Do not produce bilingual copies of the same internal content.

## Compression

State the outcome first and each fact once. Use short grammatical sentences and stable technical terms. Omit praise, filler, repeated plans, tool narration and a retelling of the assignment. Do not invent abbreviations or use broken grammar to appear shorter.

Preserve negation, conditions, ordering, evidence, uncertainty and material risks. Separate facts, requirements, inferences and unknowns. Expand wherever compression would obscure a decision or a safety boundary. Do not shorten a requested artifact by deleting required content.

Subject results contain the outcome, useful evidence, verification status and a blocker or next action only when needed. In dispatched workflows, keep those results in accessible owner artifacts; messages to root carry only process metadata and references under the [dispatcher invariant](../codex-orchestration-pact/SKILL.md#dispatcher-invariant). Role-specific receipt patterns live in the [report template](../codex-orchestration-pact/references/templates/report.md); read it when the report contract requires it, not before every message.

Report meaningful progress or a real blocker, not repeated waiting messages. Follow any higher-priority update requirements.

Whenever root dispatches, communicate only process facts and links to role-owned deliverables or prepared questions. Root reads no subject artifact or report and does not rewrite a task, outcome or question. Forward user input verbatim or by exact source reference at every stage. A skipped check remains unrun, not passed.
