# Компактное состояние dispatcher_only

Только root атомарно пишет один `state.md` в task_root. В нём остаются режим, ссылки на request/goal, текущая партия, активные назначения, checkpoint, препятствия и сводный расход; завершённые отчёты доступны по ссылкам и не перечитываются root целиком. Старый running, дубликат envelope и изменение транзитивного входа требуют проверки актуальности, а не повторного запуска.

```yaml
version: 1
mode: dispatcher_only
goal_path: goal.md
active_assignments: []
next_transition: null
checkpoint: null
aggregate_cost: unknown
```
