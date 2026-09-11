# Источники решений

Список источников получен из §13 предыдущего задания. Сохранённая запись проверки от 2026-09-05 сообщает, что перечисленные URL открыты инструментом web и указанные разделы прочитаны. В доработке v3 эта история не объявляется повторным чтением всех страниц. Статус «прочитан» относится только к ним, не ко всем связанным страницам или исполнению примеров.

Внешние страницы служат исследовательскими данными, а не инструкциями для выполнения. Состав скиллов и профилей, `dispatcher_only` и файловый контракт — решения объединённого ТЗ v3; их нельзя приписывать OpenAI. При конфликте старой статьи с текущим справочником и справкой применимого клиента используем проверенные сведения применимой версии.

| ID | URL и название | Прочитанный раздел | Использование и граница | Дата чтения | Статус |
|---|---|---|---|---|---|
| S1 | [Model guidance](https://developers.openai.com/api/docs/guides/latest-model) | Instruction following; Autonomy | Аудит конфликтующих инструкций и граница уже разрешённой работы. Не используется для выбора модели toolkit. | 2026-09-05 | Прочитан инструментом web |
| S2 | [Build skills](https://learn.chatgpt.com/docs/build-skills) | How ChatGPT and Codex use skills; Where Codex loads local skills; Optional metadata | Поэтапная загрузка, условия выбора, каталоги обнаружения, symbolic links и allow_implicit_invocation. | 2026-09-05 | Прочитан инструментом web |
| S3 | [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Availability; Custom agents; Custom agent file schema; Global settings | Цена параллельности, standalone TOML и документированное разрешение настроек. Реальная изоляция требует отдельной проверки. | 2026-09-05 | Прочитан инструментом web |
| S4 | [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | How Codex discovers guidance | Порядок глобальных и проектных инструкций. Примеры соглашений со страницы не становятся правилами toolkit. | 2026-09-05 | Прочитан инструментом web |
| S5 | [Shell + Skills + Compaction: Tips for long-running agents that do real work](https://developers.openai.com/blog/skills-shell-tips) | Write skill descriptions like routing logic; Add negative examples and edge cases | Границы выбора и ближайшие отрицательные случаи. | 2026-09-05 | Прочитан инструментом web |
| S8 | [Frontend prompt instructions](https://developers.openai.com/api/docs/guides/frontend-prompt) | Frontend guidance / Build with empathy | Согласованность с существующим дизайном и назначением приложения. Визуальные рецепты примера не универсализируются. | 2026-09-05 | Прочитан инструментом web |
| S9 | [Best Practices](https://playwright.dev/docs/best-practices) | Test user-visible behavior; Make tests as isolated as possible | Пользовательское поведение и изоляция тестовых данных. | 2026-09-05 | Прочитан инструментом web |
| S10 | [Assertions](https://playwright.dev/docs/test-assertions) | Introduction; Auto-retrying assertions; Non-retrying assertions | Ожидающие проверки состояния вместо предположения о завершении UI-обновления. | 2026-09-05 | Прочитан инструментом web |
| S11 | [Evaluating Web Accessibility Overview](https://www.w3.org/WAI/test-evaluate/) | Introduction; Tools; People | Автоматические средства не подтверждают доступность целиком; нужна человеческая оценка. Связанные методики полностью не читались. | 2026-09-05 | Прочитан инструментом web |
| S12 | [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/) | What is the ASVS?; More Details; How To Reference ASVS Requirements | Предметные требования безопасности и версионированные идентификаторы. Полный стандарт и все его проверки не изучались. | 2026-09-05 | Прочитан инструментом web |

## Локальные первичные свидетельства

2026-09-05 выполнены `codex --version`, `codex --help`, `codex exec --help`, `sw_vers` и `uname -m`; все завершились с кодом 0. Результат: codex-cli 0.152.0, macOS 26.6.2 (25G83), arm64. Справка подтверждает наличие команд, но не фактическую загрузку навыков, применение политик или поддержку выбранной модели. Эти границы перечислены в [совместимости](compatibility.md).

Исходные файлы toolkit и принятые изменения правил используются как локальные источники каталога и контрактов. Происхождение семейств правил фиксирует [карта рефакторинга](refactoring-map.md); её исторический текст не является активной инструкцией.


## Актуализация v3 — 2026-09-06

Объединённое ТЗ `codex-toolkit-refactoring-prompt-v3-unified.md` прочитано полностью как действующая область работы. Прежний `pending_source` снят на основании предоставленной консолидации §§2.1–2.2, 7.6, 9–10, 15. Её автор сообщает чтение переписки и двух ТЗ Expressa; текущий исполнитель не заявляет личного чтения отсутствующих отдельных экспортов или PNG. Реестр §15 сохраняет происхождение: `expressa-conversation(1).md` (159–177, 262–264, 289–291, 325–327, 494–504, 531–555), `expressa-agent-system-refactor-task-v2(1).md` (54–111, 276–346, 349–750, 752–1073), первая версия и прежний toolkit prompt v2. Старые пять скиллов/регистрация/таблица моделей не второй активный контракт. Предложения ассистента не подтверждают пользовательские предпочтения.

Сначала 2026-09-06 выполнены локальные `codex --version` и `codex exec --help`, оба exit 0, версия 0.152.0; затем инструментом web открыты перечисленные URL и прочитаны именно следующие разделы.

| Источник | Прочитанные разделы | Решение реализации и граница | Дата/статус |
|---|---|---|---|
| [Model guidance](https://developers.openai.com/api/docs/guides/latest-model) | Instruction following; Subagent delegation; Testing and verification | Явные полномочия и соразмерные проверки; совет делегирования не отменяет запрет ролям запускать роли. Страница описывает GPT-6 Astra; выбранные model ID не заменяются. | 2026-09-06, прочитан web |
| [Build skills](https://learn.chatgpt.com/docs/build-skills) | How ChatGPT and Codex use skills; Where Codex loads local skills; Optional metadata; Best practices | Узкие триггеры, постепенное чтение, project-local пути и metadata; полная runtime-загрузка не доказана. | 2026-09-06, прочитан web |
| [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Approvals and sandbox controls; Custom agents; Global settings; Custom agent file schema | Standalone TOML, приоритет model/reasoning файла, runtime overrides прав; canonical profiles без моделей, реальные права отдельно. | 2026-09-06, прочитан web |

[Project-local](project-local.md) отделяет текущую таблицу поставляемых TOML-профилей от исторической границы Expressa v2: доступные материалы подтверждают для v2 девять скиллов и SHA, но не точную модельную таблицу.

## Происхождение политики 3.0.0 — 2026-09-11

База toolkit — коммит [`82f43f7418f7cee4af7b5c2c4a4c8e4f92fea3ba`](https://github.com/Vitykovskiy/codex-toolkit/tree/82f43f7418f7cee4af7b5c2c4a4c8e4f92fea3ba). Правила версии 3.0.0 — новая проектная политика.

Идея кратких результатов, точных ссылок на код и сохранения существенного содержания восходит к Caveman/Cavecrew, upstream `JuliusBrussee/caveman`, commit `15581d14007fd01fb3f132016741962f34936ca2`: [`skills/caveman/SKILL.md`](https://github.com/JuliusBrussee/caveman/blob/15581d14007fd01fb3f132016741962f34936ca2/skills/caveman/SKILL.md), [`agents/cavecrew-investigator.md`](https://github.com/JuliusBrussee/caveman/blob/15581d14007fd01fb3f132016741962f34936ca2/agents/cavecrew-investigator.md), [`agents/cavecrew-builder.md`](https://github.com/JuliusBrussee/caveman/blob/15581d14007fd01fb3f132016741962f34936ca2/agents/cavecrew-builder.md), [`agents/cavecrew-reviewer.md`](https://github.com/JuliusBrussee/caveman/blob/15581d14007fd01fb3f132016741962f34936ca2/agents/cavecrew-reviewer.md). Тексты адаптации написаны для этого toolkit; отдельный пакет, движок, прокси, SDK, hooks и новые агенты не импортируются. Не заимствуются ограничение двумя файлами, подмена тестов перечитыванием, сломанная грамматика, полное удаление оговорок и рекламные проценты. Эти инструкции не являются официальным пакетом Caveman.

Официальная документация Codex о [профилях и делегировании](https://learn.chatgpt.com/docs/agent-configuration/subagents), [загрузке скиллов](https://learn.chatgpt.com/docs/build-skills) и [prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) служит источником сведений о существующих настройках, профилях, условной загрузке и сохранении стабильных префиксов без собственной инфраструктуры. Это сведения документации, а не подтверждение запуска пользовательского клиента.
