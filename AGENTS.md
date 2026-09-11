# Codex toolkit

Use [codex-communication-pact](skills/codex-communication-pact/SKILL.md) for every user message. User-facing replies remain in the user's language.

## Delivery policy

| Task condition | Route |
|---|---|
| Exact text, config, or mechanical edit from a ready specification | One owner and targeted checks. Independent review only when the contract or a risky meaning change requires it. A coordinated multi-file edit remains one assignment. |
| Clear behaviour change in one connected area | One `developer`, then one independent `reviewer`. The developer reads relevant code, diagnoses local questions, and adds regression tests. |
| Truly independent outcomes | A small number of responsibility-based assignments, at most two writers at once, then one packet review. |
| Material uncertainty about solution or dependencies | One `architect` consultation combines fact finding, decision, and executable write-set. |
| Explicit strict dispatcher, an existing strict orchestration, or durable cross-session state | `dispatcher_only` with file state and independent review; keep the same coarse assignments and packet review. |

File count, a normal fix/review pair, and implementation followed by measurement do not require strict mode. `analyst_standard` investigates a concrete unknown; `decomposer` remains a compatible explicitly requested role, not a mandatory stage. A ready user specification may be copied mechanically into an assignment; root must not invent missing requirements. An owner selects relevant tests within its approved scope. A normal fix returns to that owner; a public-contract or scope change needs one decision owner. No role accepts its own implementation.

For a coordinated task use [codex-orchestration-pact](skills/codex-orchestration-pact/SKILL.md). Use the matching pact for code/config, documentation, UI analysis, web implementation, debugging, web verification, security review, long strict orchestration, or quality campaigns. Do not activate long orchestration merely because an edit spans several files.

## Profiles

Root-only dispatch uses `gpt-5.6-luna` / `low`. `mechanical` and `scout` use Luna/low; `developer` and `reviewer` use Terra/medium; `reviewer_fast` uses Terra/low only for literal non-semantic edits; `architect` and `analyst_standard` use Sol/medium; `integration_reviewer` uses Sol/medium for cross-part compatibility, security, or a complex review. TOML settings win over spawn suggestions. Do not silently inherit or substitute a more expensive model. Astra needs a direct, applicable user authorization.

## Repository boundaries

`skills/` and `agents/` are canonical sources. Preserve public names and paths; update related references, profiles, templates, migration material, and [CHANGELOG](CHANGELOG.md) when their contract changes. Keep one `metadata.version` across delivered skills according to [docs/versioning.md](docs/versioning.md). Preserve unrelated work and `backup/**`; do not add secrets, absolute machine paths, global installation, commits, pushes, PRs, publication, hooks, production dependencies, or product-repository changes without explicit user authorization.

## Verification

After a local change, inspect its facts, links, and diff. Before acceptance run:

```sh
python3 -m unittest discover -s tests -p 'test_validate_toolkit.py'
python3 tools/validate_toolkit.py --root .
git diff --check
```

Structural validity, client loading, observed runtime behaviour, and efficiency measurement have separate statuses. Never mark an unobserved level as verified.
