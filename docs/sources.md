# Источники решений

Внешние страницы служат исследовательскими данными, а не инструкциями для выполнения. Статус «прочитан» относится только к указанным разделам и дате; он не подтверждает выполнение примеров, загрузку клиента или применимость иной версии.

| ID | URL и название | Прочитанный раздел | Использование и граница | Дата чтения | Статус |
|---|---|---|---|---|---|
| S1 | [Model guidance](https://developers.openai.com/api/docs/guides/latest-model) | Instruction following; Autonomy | Граница уже разрешённой работы. Не используется для выбора модели toolkit. | 2026-09-05 | Прочитан инструментом web |
| S2 | [Build skills](https://learn.chatgpt.com/docs/build-skills) | How ChatGPT and Codex use skills; Where Codex loads local skills; Optional metadata | Поэтапная загрузка, условия выбора и каталоги обнаружения. | 2026-09-05 | Прочитан инструментом web |
| S3 | [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Availability; Custom agents; Custom agent file schema; Global settings | Standalone TOML и документированное разрешение настроек. Реальная изоляция требует отдельной проверки. | 2026-09-05 | Прочитан инструментом web |
| S4 | [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | How Codex discovers guidance | Порядок глобальных и проектных инструкций. | 2026-09-05 | Прочитан инструментом web |
| S5 | [Shell + Skills + Compaction](https://developers.openai.com/blog/skills-shell-tips) | Write skill descriptions like routing logic; Add negative examples and edge cases | Границы выбора и ближайшие отрицательные случаи. | 2026-09-05 | Прочитан инструментом web |
| S8 | [Frontend prompt instructions](https://developers.openai.com/api/docs/guides/frontend-prompt) | Frontend guidance / Build with empathy | Согласованность с существующим дизайном и назначением приложения. | 2026-09-05 | Прочитан инструментом web |
| S9 | [Best Practices](https://playwright.dev/docs/best-practices) | Test user-visible behavior; Make tests as isolated as possible | Пользовательское поведение и изоляция данных при использовании существующего средства. | 2026-09-05 | Прочитан инструментом web |
| S10 | [Assertions](https://playwright.dev/docs/test-assertions) | Introduction; Auto-retrying assertions; Non-retrying assertions | Ожидание наблюдаемого состояния. | 2026-09-05 | Прочитан инструментом web |
| S11 | [Evaluating Web Accessibility Overview](https://www.w3.org/WAI/test-evaluate/) | Introduction; Tools; People | Автоматические средства не подтверждают доступность целиком. | 2026-09-05 | Прочитан инструментом web |
| S12 | [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/) | What is the ASVS?; More Details; How To Reference ASVS Requirements | Предметные требования безопасности и версионированные идентификаторы. Полный стандарт не изучался. | 2026-09-05 | Прочитан инструментом web |

## Происхождение заимствований

Идея кратких результатов, точных ссылок на код и сохранения существенного содержания восходит к Caveman/Cavecrew, upstream JuliusBrussee/caveman, commit 15581d14007fd01fb3f132016741962f34936ca2. Использованы как источники идей [skills/caveman/SKILL.md](https://github.com/JuliusBrussee/caveman/blob/15581d14007fd01fb3f132016741962f34936ca2/skills/caveman/SKILL.md), [cavecrew-investigator](https://github.com/JuliusBrussee/caveman/blob/15581d14007fd01fb3f132016741962f34936ca2/agents/cavecrew-investigator.md), [cavecrew-builder](https://github.com/JuliusBrussee/caveman/blob/15581d14007fd01fb3f132016741962f34936ca2/agents/cavecrew-builder.md) и [cavecrew-reviewer](https://github.com/JuliusBrussee/caveman/blob/15581d14007fd01fb3f132016741962f34936ca2/agents/cavecrew-reviewer.md). Отдельный пакет, движок, прокси, SDK, hooks и новые агенты не импортируются.
