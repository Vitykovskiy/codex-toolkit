# Assignment and dispatch

Apply the [mode boundary](../../SKILL.md#dispatcher-invariant). In ordinary coordination, send a bounded outcome, applicable original text/source references, relevant dependencies, permitted changes, criteria and stopping condition. Reuse current context and source locations; no separate assignment file or repeated task formulation is required. The recipient verifies applicable originals and evidence rather than treating the assignment as a replacement source.

In `dispatcher_only`, keep launches separate from subject-owned assignments. The launch contains only role/basic instruction, unchanged original text/reference, task root, assignment ID/attempt and dependency references. Subject scope, criteria and predecessor content stay with subject owners.

Example strict launch; placeholders are references, not a task reformulation:

```text
Role: reviewer. Perform the independent review defined by your role.
Original request: sources/U001.md
Task root: <task_root>
Assignment: R01, attempt 1; assignments/R01.yaml
Dependencies: A01, reports/A01.yaml
Read the original request and applicable project rules, locate required predecessor artifacts, and record your working task before dependent work.
```

Each subject owner reads applicable primary requirements and necessary evidence, checking identity and currency. Use the following as a guide when an assignment needs elaboration; only strict work requires a recorded working task in its existing subject artifact. This is not a new schema:

Working task: the role's outcome, grounded in the original request.
Sources: original request and applicable rule locations; distinguish exact quotes from your formulation.
Scope and dependencies: authorized responsibility, work files and required predecessor artifacts.
Criteria and limits: source-backed acceptance, evidence and execution restrictions.
Delegation basis, when delegated: the bounded result and why a separate context helps under [Context boundaries](../../SKILL.md#context-boundaries).
Return contract: conclusion, addressable primary evidence, relevant snapshot and material gaps needed by the next subject owner; keep large intermediate material at its source.
Stop or reconsider: satisfied criteria, an exact blocker or a changed dependency that invalidates the planned continuation.
Gaps: unread inputs, conflicts and known currency.

This formulation does not replace the original request or authorize new scope. Later agents use the same primary sources and reuse current evidence; reviewers independently inspect original criteria and foreign results. Missing required access blocks dependent work. New auxiliary process tooling requires the user's separate direct request.

For useful parallel work, prepare dependency gates, stable snapshot references, nonconflicting write ownership and shared-resource identifiers under [Parallel execution](../parallel-execution.md). Each assignment names its implementation or review responsibility; implementation integration belongs to developer. Only strict root receives a routing projection without subject content.

In `dispatcher_only`, preserve existing identity, attempt, goal version, required snapshot, dependencies, shared resources, write-set, artifact_path and permitted transitions. A subject owner prepares assignment content; root forwards references without opening it. A ready specification goes directly to its executor; architect may prepare assignments for a material decision, and decomposer fills a missing execution graph only when useful. Reuse a current graph rather than adding another planning pass.

Ordinary results are concise inline conclusions with evidence, checks and gaps unless a file is assigned or needed for durable access. Formal approval keeps the canonical [report](report.md); strict work writes it atomically and returns only the [envelope](../../../codex-long-orchestration/references/templates/envelope.md). No owner independently approves its own result.
