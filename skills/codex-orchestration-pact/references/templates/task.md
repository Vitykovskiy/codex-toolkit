# Assignment

An ordinary assignment carries only the role, literal goal, relevant inputs, allowed scope, and checks. It does not require a graph, decomposer, persistent state, file report, or envelope.

In `dispatcher_only`, an assignment also names its ID/profile, exact write-set, criteria, dependencies and shared resources, `artifact_path`, and one permitted next transition. A ready user specification may be copied mechanically with its literal goal, scope, and checks. The architect may supply a graph and write-set; `decomposer` is optional and remains compatible for explicitly requested decomposition or legacy import.

The owner may choose relevant tests and a related test or documentation file inside the approved scope. A normal fix returns to the same owner. Public-contract changes or scope expansion require one decision owner. The owner never accepts its own result. A strict role atomically writes its report and returns only the [envelope](../../../codex-long-orchestration/references/templates/envelope.md).
