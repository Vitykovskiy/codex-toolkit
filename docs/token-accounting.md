# Локальный учёт token usage

`tools/token_usage.py` читает только offline JSONL в нормализованной схеме `token_usage/v1`. Он не вызывает API, модель, billing service или provider SDK и не выводит цены, latency, эффективность либо effective model.

Каждая непустая строка — JSON object с `schema`, непустыми `scope`, `request_id`, `coverage` (`complete`, `partial` или `unknown`), `outcome`, `aggregate_of` и `usage`. `usage` — `null` либо object с неотрицательными `input_tokens` и `output_tokens`. Необязательные `cached_input_tokens` и `reasoning_tokens` обязаны иметь соответствующую семантику `included` или `separate`: `included` уже входят в базовые input/output и второй раз не суммируются; `separate` добавляются один раз. Поэтому известный logical total равен input + output + только отдельные категории.

`aggregate_of` содержит request ID дочерних запросов того же scope. Если все дети доступны, агрегирующий parent исключается из суммы: суммируются дети. Прямой или длинный cycle `aggregate_of` отклоняется как unsupported, поэтому не может молча дать complete zero total. Отсутствующий ребёнок, `usage: null`, `partial`/`unknown` coverage запрещают выдавать known subtotal за полный total. Результат тогда содержит `logical_tokens_known`, `logical_tokens_total: null`, coverage и notes. Идентичный повтор одного `(scope, request_id)` идемпотентен; конфликтующий повтор — ошибка. Failed call, resume и compaction — обычные outcomes и учитываются при наличии usage. При нуле `accepted` отношение `logical_tokens_per_accepted` равно `null`.

Пример ручной арифметики: запрос с input 10, output 5, cached 4 `included` и reasoning 3 `included` даёт 15. Второй запрос с input 2, output 1 и cached 7 `separate` даёт 10. Итого 25 logical tokens; при двух accepted запросах — 12.5 на accepted. Это синтетический пример, не provider mapping и не доказательство экономии.

Нативный, SDK, provider или OTel payload без явно преобразованной и подтверждённой схемы не поддерживается: CLI возвращает `status: unsupported`. Raw provider trace, version и доказательство mapping остаются отдельными входами; этот инструмент не угадывает их семантику.
