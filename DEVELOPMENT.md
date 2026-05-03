# Development (Cursor)

This repo is set up for **local development with Cursor**: project rules in [`.cursor/rules/linea-supply-agent.mdc`](.cursor/rules/linea-supply-agent.mdc), contract in [`AGENTS.md`](AGENTS.md), and the documentation hub in [`vault/agent/index.md`](vault/agent/index.md).

## URLs

With the app running: frontend [http://localhost:3001](http://localhost:3001), backend OpenAPI/Swagger [http://localhost:8001/docs](http://localhost:8001/docs), OpenAPI JSON [http://localhost:8001/openapi.json](http://localhost:8001/openapi.json).

## Commands (`just`)

From the repository root, use **[just](https://github.com/casey/just)** — see [`justfile`](justfile) or run `just --list`.

Typical flow: `just install-all` once, then `just dev` (or `just dev-headless` for background + `just logs` / `just stop`). Optional sample data: `just seed`.

## Docker (Docker Desktop)

Root [`package.json`](package.json) exposes npm scripts that build the dev image from [`.devcontainer/Dockerfile`](.devcontainer/Dockerfile) and run a container with the repo bind-mounted and a Linux volume for `node_modules` (avoids macOS native binaries inside the container).

| Script | Purpose |
|--------|---------|
| `npm run docker:dev` | Build image `linea-supply-dev:local` and start the stack (`npm ci` + `just dev` in the container). |
| `npm run docker:up` | Start (or replace) container only; use after a successful build. |
| `npm run docker:logs` | Follow container logs. |
| `npm run docker:stop` | Remove the `linea-supply-local-demo` container. |

Requires **Docker Desktop** running. Scripts use `$(pwd)` for the bind mount — intended for **macOS/Linux**; on Windows, adjust paths or use WSL from the repo root.

## Dev Container

See [`.devcontainer/README.md`](.devcontainer/README.md). The image includes Python, Node, Ruff, ESLint, and the editor extensions listed in `devcontainer.json`. After **Reopen in Container**, use the same `just` flow as on the host.

## Editor: npm scripts

Workspace [`.vscode/settings.json`](.vscode/settings.json) enables **Run / Debug** CodeLens on `package.json` scripts and NPM Scripts explorer actions. Run docker/just-related scripts from the **repository root** so paths resolve correctly.

## CI

GitHub Actions workflow: [`.github/workflows/ci.yml`](.github/workflows/ci.yml). Local mirror: `just ci`.
