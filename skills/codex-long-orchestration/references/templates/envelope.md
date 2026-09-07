# Envelope dispatcher_only

Это короткое процессное извещение, а не полный отчёт. Оно содержит ID/попытку, профиль, статус, путь собственного отчёта и существующий следующий переход; root проверяет форму, путь, runtime-отправителя и разрешённое ребро, не читая предметное содержание. При `status: approved` обязательный `accepts` связывает approval с конкретным принимаемым результатом в форме `<assignment_id>/<attempt>`; суффикс `@<snapshot>` добавляется, только когда снимок обязателен для этой передачи. Для прочих статусов `accepts` равен `null`.

Если результат относится к blocker, `finding_id` — его устойчивый ID, а `progress` — ровно `confirmed`, `none` или `unknown`; для результата без blocker оба поля равны `null`. `confirmed` сообщает только независимый reviewer после материальной ожидаемой проверки; новый diff или объяснение не являются progress. При `none` или `unknown` поле `no_progress` обязательно содержит непустые `missing_input` и `next_check`; иначе оно равно `null`. Root переносит эти короткие сведения в state и не выводит их из полного отчёта.

```yaml
status: completed
artifact: reports/A01.yaml
assignment_id: A01
attempt: 1
profile: developer
accepts: null
finding_id: null
progress: null
no_progress: null
next_transition: assignments/R01.yaml
```
