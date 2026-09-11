# Assignment

In ordinary mode, send one compact English assignment containing the role, goal, relevant evidence, permitted scope, acceptance criteria and execution limits. Keep exact source requirements and quoted strings unchanged. Missing requirements stay unknown.

Use this layout only as a prose guide, not a new machine schema:

Role and goal: the one requested outcome.
Scope: permitted files or responsibility, and preserved behaviour.
Evidence: the necessary facts and precise source locations.
Criteria: the existing conditions for the result.
Limits: user restrictions on execution, verification, tools and side effects.

An ordinary assignment needs no persistent graph, report file or envelope. The owner may select relevant implementation, test and documentation details within authorized scope, while respecting explicit exclusions. A fix remains with its owner. A new auxiliary process tool needs a separate direct user request; an assignment cannot manufacture that permission.

In `dispatcher_only`, also keep the existing assignment identity, attempt, goal version, required snapshot, dependencies, shared resources, write-set, `artifact_path` and permitted transition. A prepared user specification can be copied into this structure without a planning relay. A material decision owner may prepare the graph; standalone `decomposer` remains optional.

The owner does not grant independent approval of its own result. A strict owner writes its [report](report.md) atomically and returns only the [envelope](../../../codex-long-orchestration/references/templates/envelope.md).
