# Документация для агента (индекс)

Одна точка входа: **спеки**, **рабочие правила агента**, **контекст продукта** и **карта кода** — всё в `vault/` или по ссылкам ниже. Дублировать длинные тексты в чат не нужно: открывайте файлы по ссылкам.

## Быстрый порядок работы

1. **[AGENTS.md](../../AGENTS.md)** (корень репозитория) — контракт агента, **`just`**, ссылки сюда; для **Cursor** — правила в **`.cursor/rules/linea-supply-agent.mdc`**.
2. **Этот файл** — что читать по задаче (спеки, инженерные правила).
3. **[README.md](../README.md)** — как устроен vault и куда писать заметки.
4. После смены архитектуры кода — обновить **[structure/index.md](../structure/index.md)**; суть правки — в **[daily-changes/index.md](../daily-changes/index.md)**.

## Спецификации и стандарты (в vault)

| Тема | Файл |
|------|------|
| Ошибки, логирование, RFC 7807, трассировка | [error-handling-and-logging-standards.md](../context/technical-spec/error-handling-and-logging-standards.md) |

Новые текстовые спеки добавляйте в **`vault/context/technical-spec/`**, строку в таблицу — в [technical-spec/index.md](../context/technical-spec/index.md).

## Инженерный workflow (агент)

| Тема | Файл |
|------|------|
| Рефакторинг, push, `gh`, Sourcegraph, security summary | [agent-engineering.md](./agent-engineering.md) |

## Контекст продукта и карта кода (vault)

| Раздел | Назначение |
|--------|------------|
| [context/index.md](../context/index.md) | Термины, ТЗ, встречи |
| [structure/index.md](../structure/index.md) | Где лежит клиент, сервер, пути в репо |
| [daily-changes/index.md](../daily-changes/index.md) | Дневник изменений |
| [SETUP.md](../SETUP.md) | Obsidian Local REST API, `.env`, MCP |

## Справочники вне vault (код, автоматизация)

| Тема | Файл |
|------|------|
| Быстрый старт, дерево репозитория | [README.md](../../README.md) |
| Команды `just` | [justfile](../../justfile) |
| Backend: стиль, API | [backend/AGENTS.md](../../backend/AGENTS.md) |
| Frontend: TS, Vite | [frontend/AGENTS.md](../../frontend/AGENTS.md) |
| CI | [`.github/workflows/`](../../.github/workflows/) |
| Локально: все шаги проверки с итогом по каждому (check, тесты, lint, build, e2e) | **`just ci-all-steps`** → [`scripts/ci-all-steps.sh`](../../scripts/ci-all-steps.sh) |
| Команды агента в Cursor | [`.cursor/rules/linea-supply-agent.mdc`](../../.cursor/rules/linea-supply-agent.mdc) |

## Obsidian

Внутри Obsidian те же файлы: wiki-ссылки вида `[[context/index]]`, `[[structure/index]]` из корня vault; этот индекс — **`agent/index`**.
