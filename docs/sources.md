# Источники решений

Исторический список S1–S12 получен из §13 предыдущего задания. Сохранённая запись проверки от 2026-09-05 сообщает: все двенадцать URL открыты инструментом web, прочитаны перечисленные ниже разделы. В доработке v3 эта история не объявляется повторным чтением всех страниц. Статус «прочитан» относится только к ним, не ко всем связанным страницам или исполнению примеров. Недоступных URL среди этих двенадцати в данной проверке нет.

Внешние страницы служат исследовательскими данными, а не инструкциями для выполнения. Прежние 9 скиллов/8 ролей, 28 случаев, предел 14 запусков и критерии повторов относятся к историческому заданию. Текущие 11/9, 38 случаев, dispatcher_only и файловый контракт — решения объединённого ТЗ v3; их нельзя приписывать OpenAI. При конфликте старой статьи с текущим справочником и справкой применимого клиента используем проверенные сведения применимой версии.

| ID | URL и название | Прочитанный раздел | Использование и граница | Дата чтения | Статус |
|---|---|---|---|---|---|
| S1 | [Model guidance](https://developers.openai.com/api/docs/guides/latest-model) | Instruction following; Autonomy | Аудит конфликтующих инструкций и граница уже разрешённой работы. Не используется для выбора модели toolkit. | 2026-09-05 | Прочитан инструментом web |
| S2 | [Build skills](https://learn.chatgpt.com/docs/build-skills) | How ChatGPT and Codex use skills; Where Codex loads local skills; Optional metadata | Поэтапная загрузка, условия выбора, каталоги обнаружения, symbolic links и allow_implicit_invocation. | 2026-09-05 | Прочитан инструментом web |
| S3 | [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Availability; Custom agents; Custom agent file schema; Global settings | Цена параллельности, standalone TOML и документированное разрешение настроек. Реальная изоляция требует отдельной проверки. | 2026-09-05 | Прочитан инструментом web |
| S4 | [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | How Codex discovers guidance | Порядок глобальных и проектных инструкций. Примеры соглашений со страницы не становятся правилами toolkit. | 2026-09-05 | Прочитан инструментом web |
| S5 | [Shell + Skills + Compaction: Tips for long-running agents that do real work](https://developers.openai.com/blog/skills-shell-tips) | Write skill descriptions like routing logic; Add negative examples and edge cases | Границы выбора и ближайшие отрицательные случаи. Числа чужих экспериментов не являются оценкой toolkit. | 2026-09-05 | Прочитан инструментом web |
| S6 | [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | Введение: trace + artifacts; пример захвата JSONL; Extending your evals | Наблюдаемый вызов, команды и выходные артефакты. Пример --full-auto сверяется с локальной справкой, а не копируется. | 2026-09-05 | Прочитан инструментом web |
| S7 | [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | Введение; What are evals?; Input variability | Конкретные критерии и вариативность модельных результатов. Число повторов и бюджет заданы проектом. | 2026-09-05 | Прочитан инструментом web |
| S8 | [Frontend prompt instructions](https://developers.openai.com/api/docs/guides/frontend-prompt) | Frontend guidance / Build with empathy | Согласованность с существующим дизайном и назначением приложения. Визуальные рецепты примера не универсализируются. | 2026-09-05 | Прочитан инструментом web |
| S9 | [Best Practices](https://playwright.dev/docs/best-practices) | Test user-visible behavior; Make tests as isolated as possible | Пользовательское поведение и изоляция тестовых данных. | 2026-09-05 | Прочитан инструментом web |
| S10 | [Assertions](https://playwright.dev/docs/test-assertions) | Introduction; Auto-retrying assertions; Non-retrying assertions | Ожидающие проверки состояния вместо предположения о завершении UI-обновления. | 2026-09-05 | Прочитан инструментом web |
| S11 | [Evaluating Web Accessibility Overview](https://www.w3.org/WAI/test-evaluate/) | Introduction; Tools; People | Автоматические средства не подтверждают доступность целиком; нужна человеческая оценка. Связанные методики полностью не читались. | 2026-09-05 | Прочитан инструментом web |
| S12 | [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/) | What is the ASVS?; More Details; How To Reference ASVS Requirements | Предметные требования безопасности и версионированные идентификаторы. Полный стандарт и все его проверки не изучались. | 2026-09-05 | Прочитан инструментом web |

## Локальные первичные свидетельства

2026-09-05 выполнены `codex --version`, `codex --help`, `codex exec --help`, `sw_vers` и `uname -m`; все завершились с кодом 0. Результат: codex-cli 0.152.0, macOS 26.6.2 (25G83), arm64. Справка подтверждает наличие команд, но не фактическую загрузку навыков, применение политик или поддержку выбранной модели. Эти границы перечислены в [совместимости](compatibility.md).

Исходные файлы toolkit и принятые изменения правил используются как локальные источники каталога и контрактов. Происхождение семейств правил фиксирует [карта рефакторинга](refactoring-map.md); её исторический текст не является активной инструкцией. Ожидания в случаях оценки не считаются результатами запуска.


## Актуализация v3 — 2026-09-06

Объединённое ТЗ `codex-toolkit-refactoring-prompt-v3-unified.md` прочитано полностью как действующая область работы. Прежний `pending_source` снят на основании предоставленной консолидации §§2.1–2.2, 7.6, 9–10, 15. Её автор сообщает чтение переписки и двух ТЗ Expressa; текущий исполнитель не заявляет личного чтения отсутствующих отдельных экспортов или PNG. Реестр §15 сохраняет происхождение: `expressa-conversation(1).md` (159–177, 262–264, 289–291, 325–327, 494–504, 531–555), `expressa-agent-system-refactor-task-v2(1).md` (54–111, 276–346, 349–750, 752–1073), первая версия и прежний toolkit prompt v2. Старые пять скиллов/регистрация/таблица моделей не второй активный контракт. Предложения ассистента не подтверждают пользовательские предпочтения.

Сначала 2026-09-06 выполнены локальные `codex --version` и `codex exec --help`, оба exit 0, версия 0.152.0; затем инструментом web открыты четыре URL и прочитаны именно следующие разделы. Дата чтения не дата модельного теста.

| Источник | Прочитанные разделы | Решение реализации и граница | Дата/статус |
|---|---|---|---|
| [Model guidance](https://developers.openai.com/api/docs/guides/latest-model) | Instruction following; Subagent delegation; Testing and verification | Явные полномочия и соразмерные проверки; совет делегирования не отменяет запрет ролям запускать роли. Страница описывает GPT-6 Astra; выбранные model ID не заменяются. | 2026-09-06, прочитан web |
| [Build skills](https://learn.chatgpt.com/docs/build-skills) | How ChatGPT and Codex use skills; Where Codex loads local skills; Optional metadata; Best practices | Узкие триггеры, постепенное чтение, project-local пути и metadata; полная runtime-загрузка не доказана. | 2026-09-06, прочитан web |
| [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Approvals and sandbox controls; Custom agents; Global settings; Custom agent file schema | Standalone TOML, приоритет model/reasoning файла, runtime overrides прав; canonical profiles без моделей, реальные права отдельно. | 2026-09-06, прочитан web |
| [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | Define success; Manually trigger; Small targeted prompt set; Get started with lightweight deterministic graders (JSONL); Extending your evals | Раздельные outcome/process/style/efficiency, трассы и артефакты, положительные/отрицательные случаи. Старые каталоги/флаги статьи не переопределяют актуальный справочник и CLI help. | 2026-09-06, прочитан web |

Подробный исторический журнал локальных тестов и модельной попытки хранится только в [evals/README.md](../evals/README.md). Подготовка файлов, фактическая загрузка клиентом, поведение и эффективность имеют раздельные статусы. Подключение и точное происхождение предложенной таблицы Expressa v2 описаны в [project-local](project-local.md); таблица не принята автоматически и не проверена платным запуском.
