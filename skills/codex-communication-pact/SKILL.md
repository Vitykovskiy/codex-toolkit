---
name: codex-communication-pact
description: Write concise messages and readable user-facing Markdown questions, reports and deliverables, with evidence and explicit uncertainty.
---

# Communication pact

## Audience and language

Use the user's language for replies, questions and progress messages. Match the requested language and detail of user deliverables, documentation, code comments and external messages.

Use concise English for internal assignments, agent messages, process notes, handoffs and internal report prose. A file intended for the user follows the user's language and requested detail, even when an internal role writes it. Keep source requirements and quotations in their original language. Preserve code, identifiers, paths, commands, errors, schema keys, enum values, numbers and units exactly. Do not produce bilingual copies of the same internal content.

## User-facing Markdown

Before authoring, reviewing or handing off a Markdown file for communication with the user, read and apply the [user-facing Markdown contract](references/communication-pact.md#пользовательские-markdown-файлы). It covers questions, blockers, progress updates, reports, decisions and final answers in direct, ordinary and strict workflows, regardless of author or path. A working artifact promoted to user communication meets the same contract.

Make the document self-contained, correctly formatted and proportionately structured, with sufficient evidence and one clear conclusion or requested decision. The subject author checks the actual file before returning its reference; required independent review includes that file. The dispatcher forwards ready references and process facts without reading or rewriting their content. Internal report schemas remain unchanged; their compact receipts are not a user-facing writing template.

## Compression

State the outcome first and each fact once. Use short grammatical sentences and stable technical terms. Omit praise, filler, repeated plans, tool narration and a retelling of the assignment. Do not invent abbreviations or use broken grammar to appear shorter.

Preserve negation, conditions, ordering, evidence, uncertainty and material risks. Separate facts, requirements, inferences and unknowns. Expand wherever compression would obscure a decision or a safety boundary. Do not shorten a requested artifact by deleting required content.

Subject results contain the outcome, useful evidence, verification status and a blocker or next action only when needed. In dispatched workflows, keep those results in accessible owner artifacts; messages to root carry only process metadata and references under the [dispatcher invariant](../codex-orchestration-pact/SKILL.md#dispatcher-invariant). Role-specific receipt patterns live in the [report template](../codex-orchestration-pact/references/templates/report.md); read it when the report contract requires it, not before every message.

Report meaningful progress or a real blocker, not repeated waiting messages. Follow any higher-priority update requirements.

Whenever root dispatches, communicate only process facts and links to role-owned deliverables or prepared questions. Root reads no subject artifact or report and does not rewrite a task, outcome or question. Forward user input verbatim or by exact source reference at every stage. A skipped check remains unrun, not passed.
