# Assignment and dispatch

Apply the [mandatory dispatcher invariant](../../SKILL.md#dispatcher-invariant). Keep dispatcher launches separate from subject-owned assignments. A launch contains only the role and basic role instruction, original user text verbatim or its exact reference, task root, task/assignment ID, attempt and dependency identifiers/references. Never add a dispatcher summary, selected requirements, inferred scope, criteria or predecessor report text. The recipient finds that material itself.

Example launch; placeholders are references, not a task reformulation:

```text
Role: reviewer. Perform the independent review defined by your role.
Original request: sources/U001.md
Task root: <task_root>
Assignment: R01, attempt 1; assignments/R01.yaml
Dependencies: A01, reports/A01.yaml
Read the original request and applicable project rules, locate required predecessor artifacts, and record your working task before dependent work.
```

Each subject owner independently reads primary requirements and necessary dependency reports, checks identity and currency, and records its own formulation in the existing assignment/result artifact or ordinary working context. Use this layout as a prose guide, not a new machine schema:

Working task: the role's outcome, grounded in the original request.
Sources: original request and applicable rule locations; distinguish exact quotes from your formulation.
Scope and dependencies: authorized responsibility, work files and required predecessor artifacts.
Criteria and limits: source-backed acceptance, evidence and execution restrictions.
Gaps: unread inputs, conflicts and known currency.

This formulation does not replace the original request or authorize new scope. Later agents ground their tasks independently in the same primary sources. A scout finds rules; an executor finds necessary predecessor reports; a reviewer finds original criteria and foreign evidence. Missing or ambiguous access is blocked, not a reason for dispatcher relay. New auxiliary process tooling requires the user's separate direct request.

In `dispatcher_only`, preserve existing identity, attempt, goal version, required snapshot, dependencies, shared resources, write-set, artifact_path and permitted transition. A subject owner prepares assignment content; root forwards references without opening it. A ready specification goes directly to its executor; architect may prepare assignments for a material decision, and standalone decomposer remains optional.

The owner writes its [report](report.md); strict work writes it atomically and returns only the [envelope](../../../codex-long-orchestration/references/templates/envelope.md). Ordinary dispatch keeps dependency material accessible at existing task locations and returns only a routing receipt, without adopting the full strict schema. Direct ordinary work may remain inline. No owner independently approves its own result.
