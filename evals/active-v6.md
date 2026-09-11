# Active v6 — synthetic token-orchestration preparation

Active set: `T01`–`T08` in [cases.jsonl](cases.jsonl); [fixture notes](fixtures/w17/README.md) define only synthetic local inputs. These cases prepare evaluation of authorization, routing, context/retry, evidence filtering, accounting and structured artifact validation. They are not executed runs and do not supersede historical v3 material.

Evaluator receives case expectations, grader rubric and traces outside tested project. Tested agent receives only case `prompt` and fixture files. Absence of complete client/tool traces is `unable_to_verify`, never proof that a forbidden skill, model, tool call or file read did not occur.

Runtime experiment gate: `scope: not_set`, `snapshot: not_set`, `repeat_count: not_set`, `stop_rule: not_set`, `budget: not_set`, `practically_significant_threshold: not_set`, `quality_non_inferiority: not_set`, `readiness: false`. No model, subagent, paid API or benchmark run is authorized by this protocol.

When separately authorized, compare only a preselected comparable case set with identical declared model, effort, tools and input snapshots. Record failures, aborts, retries, review, compaction and preparation cost separately; cold and warm cache are separate conditions. Stop on exhausted approved budget, shared environment failure without a new discriminating hypothesis, invariant breach or lost comparability. Insufficient observations are inconclusive and never a positive efficiency result.
