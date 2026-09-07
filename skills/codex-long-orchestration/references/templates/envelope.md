# Envelope dispatcher_only

Это короткое процессное извещение, а не полный отчёт. Оно содержит ID/попытку, профиль, статус, путь собственного отчёта и существующий следующий переход; root проверяет форму, путь, runtime-отправителя и разрешённое ребро, не читая предметное содержание.

```yaml
status: completed
artifact: reports/A01.yaml
assignment_id: A01
attempt: 1
profile: developer
next_transition: assignments/R01.yaml
```
