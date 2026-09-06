# Фрагмент для корневого AGENTS.md потребителя

Пример ниже копируется в корневой AGENTS.md после проверенного импорта. Пути внутри блока рассчитаны от корня проекта, а не от этого файла шаблона. Удаляйте неприменимые пункты только вместе с проверкой зависимостей выбранного комплекта; процедуру project-local подключения оператор читает в документации исходного снимка toolkit, которая не является runtime-зависимостью потребителя.

```markdown
## Процедуры

Применяй [коммуникацию](.agents/skills/codex-communication-pact/SKILL.md) к каждому сообщению; прочитай один раз и повторно при изменении. Остальные процедуры выбирай по ситуации; доступность каталога не требует загрузки всего его текста.

- Изменение/функциональное ревью/проверка кода: [разработка](.agents/skills/codex-development-pact/SKILL.md).
- Долговременные тексты: [документация](.agents/skills/codex-documentation-pact/SKILL.md).
- Анализ интерфейса: [UI-анализ](.agents/skills/codex-ui-analysis-pact/SKILL.md).
- Реализация принятого веб-сценария: [web-implementation](.agents/skills/codex-web-implementation/SKILL.md).
- Диагностика либо разрешённое исправление: [debugging](.agents/skills/codex-debugging/SKILL.md); режим диагностики сохраняет исходники.
- Проверка работающего UI: [web-verification](.agents/skills/codex-web-verification/SKILL.md).
- Проверка заданной границы доверия: [security-review](.agents/skills/codex-security-review/SKILL.md).
- Координация назначений: [orchestration](.agents/skills/codex-orchestration-pact/SKILL.md).
- Root-диспетчер, несколько предметных итераций, handoff незавершённой оркестрации: [long-orchestration](.agents/skills/codex-long-orchestration/SKILL.md), обязательный dispatcher_only.
- Кампания качества/выбор следующей партии: [product-quality](.agents/skills/codex-product-quality/SKILL.md), включая long-orchestration и quality_owner. Разовая проверка известного состояния не запускает кампанию.

Обычную локальную задачу root может выполнять самостоятельно. В dispatcher_only root ведёт процесс и запускает существующие принятые назначения; предметные решения, собственные полные файловые отчёты и независимую приёмку выполняют роли. Root получает только envelope; fallback, handoff и финальная проверка не расширяют его полномочий. Роли не запускают подагентов. Недоступная роль/запись — процессный блокер.

Upstream в .agents/skills сохраняй по байтам; проектные правила и charter/preferences держи отдельно со ссылками на источники. Происхождение импорта — .agents/SOURCE.md и .agents/upstream.sha256; адаптации — .agents/LOCAL-ADAPTATIONS.md. Локальные источники не подменяй глобальными одноимёнными. Runtime задачи — в проверенном безопасном task-root; перед записью проверь ссылки и Git-контекст .agents/.codex. Исходники отслеживаются, .codex/tmp игнорируется. Команды приложения и разрешения определяются самим проектом.
```
