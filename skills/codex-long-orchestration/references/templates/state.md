# Компактное состояние dispatcher_only

Только root атомарно пишет один `state.md` в task_root. В нём остаются режим, ссылки на request/goal, текущая партия, активные назначения, checkpoint, препятствия и сводный расход; все предметные файлы и отчёты остаются по ссылкам, root не читает ни их содержимое, ни фрагменты. См. [обязательный инвариант диспетчера](../../../codex-orchestration-pact/SKILL.md#dispatcher-invariant). State содержит только процессные поля и ссылки, без пересказа задачи и предметных выводов. Старый running, дубликат envelope и изменение транзитивного входа требуют проверки процессных метаданных; актуальность предметных входов проверяет назначенная роль до зависимой работы.

`cost` хранит известное состояние разрешённого расхода, а не журнал событий или сборщик токенов. Перед запуском root читает один актуальный снимок `cost` и фиксирует идентификатор набора; параллельные назначения набора делят его остаток и его резервы. `cumulative` сохраняется между сессиями, стратегиями и партиями. `increments` с устойчивым ключом описывают только приращения названной области; значение из него переносится в `cumulative` не более одного раза. Любой ненаблюдаемый лимит, расход, остаток или резерв равен `unknown`, а не нулю.

Для каждого активного или неразрешённого blocker state хранит устойчивый `finding_id`, а не только его отображаемое имя: ID нарушенного критерия, если он передан как процессное поле, последнее `progress` (`confirmed`, `none` или `unknown`), `consecutive_without_confirmed_progress` и, при `none`/`unknown`, `no_progress.missing_input` и `no_progress.next_check`. Root переносит эти поля из envelope; `none` и `unknown` увеличивают счётчик, `confirmed` обнуляет его. Смена сессии, assignment или имени finding сохраняет запись с тем же `finding_id`; неудачная диагностика не создаёт новый ID. После двух последовательных попыток без подтверждённого прогресса root вызывает существующего владельца решения по тем же исходным ссылкам; state сохраняет только ссылку и разрешённые поля подготовленного им перехода, без самостоятельного выбора стратегии.

```yaml
version: 1
mode: dispatcher_only
goal_path: goal.md
request_sources: [sources/U001.md]
active_assignments: []
next_transition: null
checkpoint: null
cost:
  authority: not_set
  limit: not_set
  cumulative:
    tokens_spent: unknown
    subject_assignments: 0
    continuations: 0
  increments: []
  launch_set:
    id: null
    known_remaining: unknown
    reservations: []
blockers:
  - finding_id: F01
    criterion: A09
    progress: none
    consecutive_without_confirmed_progress: 1
    no_progress:
      missing_input: "Результат целевой проверки"
      next_check: "R01"
```
