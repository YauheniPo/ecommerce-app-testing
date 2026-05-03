# Obsidian + MCP для этого проекта

## 1. Vault в Obsidian

1. Obsidian → **Open folder as vault** → выберите каталог `vault` в корне репозитория `ecommerce-app-testing`.
2. Community plugins → установите и включите **Local REST API** ([плагин](https://github.com/coddingtonbear/obsidian-local-rest-api)).
3. В настройках плагина скопируйте **API key** и базовый URL (часто `https://127.0.0.1:27124`). Убедитесь, что Obsidian запущен, пока работаете с MCP.

Проверка: в браузере откройте URL из плагина; в ответе должен быть признак живого API (например статус ok в JSON плагина).

## 2. Переменные для Cursor MCP

В **корне репозитория** создайте **`.env`** по **`.env.example`**. Имена переменных:

- **`OBSIDIAN_API_KEY`** — ключ плагина Local REST API.
- **`OBSIDIAN_API_URL`** — базовый URL API (часто `https://127.0.0.1:27124`); в preload копируется в **`OBSIDIAN_BASE_URL`**, если последний не задан.
- **`OBSIDIAN_VAULT_NAME`** — имя хранилища в Obsidian (для людей и документации; текущий MCP-пакет может не читать эту переменную).

Дополнительно можно задать **`OBSIDIAN_BASE_URL`** в `.env` или в `.cursor/mcp.json` → `mcpServers.obsidian.env`.

## 3. MCP в Cursor

Сервер **`obsidian`**: **`node -r .cursor/obsidian-mcp-register.cjs`** (читает **`.env`** через **dotenv**, алиасы ключей) затем **`@beshkenadze/mcp-obsidian/dist/stdio.js`**. В preload также задаётся **`globalThis.__bundlerPathsOverrides`** для **thread-stream**: в сборке `1.2.0` зашит неверный **`__dirname`** (`/home/runner/...`), без override падает **`Cannot find module ... thread-stream/lib/worker.js`**.

В корне: **`npm install`** (`@beshkenadze/mcp-obsidian`, **`dotenv`**). В **`.cursor/mcp.json`** для `obsidian` заданы **`LOG_TO_STDERR=true`** и **`LOG_LEVEL=error`**: иначе pino пишет в **stdout** и ломает JSON-RPC MCP; в сборке `1.2.0` ещё и **`getPackageVersion`** бьёт в несуществующий путь CI.

Пакет **`@oleksandrkucherenko/mcp-obsidian`** без **Bun** не использовать.

После изменений `.env` или `mcp.json` перезапустите Cursor или переподключите MCP.
