# Содержание

База знаний проекта **Linea Supply** (in-repo vault в каталоге репозитория). В Obsidian: **Open folder as vault** → каталог `vault`.

- **[[agent/index|Документация для агента — индекс]]** — спеки, workflow, ссылки в корень репозитория (читать первым для задач «по документации»).
- [[context/index|context]] — глобальная информация о проекте: ТЗ, термины, требования, записи встреч; нормативные спеки в [[context/technical-spec/index|technical-spec]].
- [[daily-changes/index|daily-changes]] — сводки изменений в коде и в этой базе знаний.
- [[structure/index|structure]] — структура приложения: клиент, сервер, где что лежит. Актуализируйте при каждом существенном изменении кода.
- [[SETUP|Подключение Obsidian и MCP]] — плагин Local REST API, `.env`, Cursor.

## Для агентов

- В каждом разделе есть **index** с описанием и правилами работы с разделом.
- Крупные заметки дробите на отдельные файлы и добавляйте ссылки в соответствующий **index**.
- После правок базы знаний добавьте строку в [[daily-changes/index|daily-changes]] (формат — внутри того раздела).

**Поток задачи (когда доступен Obsidian MCP):** начните с этого файла; затем по ссылкам только в [[context/index|context]], [[structure/index|structure]], [[daily-changes/index|daily-changes]]; после изменений кода обновите [[structure/index|structure]] при смене архитектуры и зафиксируйте суть в [[daily-changes/index|daily-changes]]. Подключение плагина и MCP: [[SETUP|SETUP]].

Стабильные правила репозитория — в корневом **`AGENTS.md`** и в **Cursor**: **`.cursor/rules/linea-supply-agent.mdc`** (на уровень выше `vault/`); здесь — продуктовый контекст и живая карта кода.
