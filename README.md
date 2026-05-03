# Linea Supply — e-commerce demo

Full-stack **FastAPI + React (TypeScript)** demo with SQLite and **`just`**-based automation. Use **Cursor** locally; project rules load from [`.cursor/rules/linea-supply-agent.mdc`](.cursor/rules/linea-supply-agent.mdc).

**Cursor (AI agent):** read [AGENTS.md](AGENTS.md), then [vault/agent/index.md](vault/agent/index.md) (specs + workflow). Vault overview: [vault/README.md](vault/README.md). Day-to-day commands: [DEVELOPMENT.md](DEVELOPMENT.md) and [justfile](justfile).

<img width="1290" height="1016" alt="Screenshot 2025-10-03 at 12 32 11 PM" src="https://github.com/user-attachments/assets/214b7e59-8168-446b-adef-bd481b586d64" />

## How to use this repo

Follow the [Quick Start](#quick-start). With `just dev` running, open [http://localhost:3001](http://localhost:3001). For agent-oriented notes see [DEVELOPMENT.md](DEVELOPMENT.md).

## Project Structure

```
.
├── .cursor/            # Cursor rules (agent workflow) + MCP config
├── .devcontainer/      # VS Code Dev Container configuration
├── .github/            # GitHub workflows and CI configuration
├── backend/            # FastAPI backend
│   ├── app/            # Application source code
│   ├── alembic/        # Database migrations
│   ├── pyproject.toml  # Python dependencies (managed by uv)
│   ├── main.py         # FastAPI entry point
│   ├── AGENTS.md       # Agent documentation for backend
│   └── store.db        # SQLite database file
├── frontend/           # React frontend (TypeScript/Vite)
│   ├── src/            # React components and pages
│   │   ├── api/        # API client and types
│   │   ├── components/ # Reusable UI components
│   │   ├── context/    # React Context providers
│   │   ├── hooks/      # Custom React hooks
│   │   ├── mockDB/     # Mock data for development
│   │   ├── pages/      # Page-level components
│   │   └── theme/      # Chakra UI theme configuration
│   ├── public/         # Static assets
│   ├── package.json    # Node.js dependencies
│   ├── vite.config.ts  # Vite configuration
│   ├── eslint.config.js # ESLint configuration
│   ├── AGENTS.md       # Agent documentation for frontend
├── vault/              # Obsidian KB + product/agent docs (start at vault/agent/index.md; vault/README.md, vault/SETUP.md)
├── logs/               # Service logs (dev-headless mode)
├── justfile            # Development automation commands
├── package.json        # Root package.json for shared dependencies
├── settings.json       # Workspace settings
├── AGENTS.md           # Agent documentation for overall project
├── DEVELOPMENT.md      # Cursor / just / dev container notes
└── README.md           # README
```

## Quick Start

### Option 1: Dev Container (recommended)

The fastest way to get started: Podman (or Docker) plus VS Code. If the container fails to build, check the Dev Containers log and [.devcontainer/README.md](.devcontainer/README.md).

**What you need:**

If you have any of these preinstalled, make sure to update them before proceeding!

- VS Code [download](https://code.visualstudio.com/download)
  
- Podman Desktop ([download](https://podman-desktop.io/))
  - Once installed, open it up and follow through the prompts to install `podman`
  - When you get to the [virtual machine](https://podman-desktop.io/docs/podman/creating-a-podman-machine) setup, make sure you dedicate at least 4 cores and 10gb of RAM
  - Once installed and ready, you should see this in your Mac menu bar:
    <img width="233" height="124" alt="image" src="https://github.com/user-attachments/assets/bf18d324-e182-496d-91a3-696b05c3dbd7" />
    
- VS Code [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

- Change the VS Code setting: `"dev.containers.dockerPath": "docker"` to `"dev.containers.dockerPath": "podman"`
  - Access settings in VS Code: <img width="316" height="276" alt="image" src="https://github.com/user-attachments/assets/4ae8e373-3d92-45ae-a9e5-ef59c25c0aa0" />  
  - Type in the search box `dev.containers.dockerPath`
  - Change the box "Dev > Containers: Docker Path" from `docker` to `podman`: <img width="462" height="100" alt="image" src="https://github.com/user-attachments/assets/48673050-6f63-4760-bb54-4af7cc83242c" />

- Homebrew (optional if you want to install the GitHub CLI) `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- GitHub CLI `gh` (optional): `brew install gh`

**Code Setup:**

- Open VS Code
- Open the terminal:
  <img width="281" height="57" alt="image" src="https://github.com/user-attachments/assets/c8f9f2b3-36e0-42ed-915a-71321c3a42cc" />
- Enter the command below:

```bash
git clone https://github.com/sourcegraph/ecommerce-app.git
```

- From File -> Open Folder, open the `ecommerce-app` folder in VS Code: <img width="296" height="181" alt="image" src="https://github.com/user-attachments/assets/85ffef79-a913-4ed1-850f-cdffadec5d0c" />

- Authenticate to GitHub (optional)

```bash
gh auth login
```


- Click the remote window menu in the lower left corner:
  <img width="360" height="131" alt="image" src="https://github.com/user-attachments/assets/e1635d07-9162-4126-b889-6c0a40d4753a" />
- In the menu that pops up, select "Reopen in Container":
  <img width="624" height="274" alt="image" src="https://github.com/user-attachments/assets/07d17a3d-0101-4eeb-93dc-08c53ead9926" />
- Wait a few minutes, the first build takes a few minutes, then it will be cached and near instant in the future

- Start the app from the integrated terminal: `just dev` (or `just dev-headless` for background + `just logs` / `just stop`)

Access the application on your local browser (ports will automatically be forwarded):

- Frontend: [http://localhost:3001](http://localhost:3001)
- Backend API: [http://localhost:8001](http://localhost:8001)

**Reverting Changes**

As you work with this repo, you can revert any changes made by selecting all files changed and discarding them (indicated by a number showing in the source control sidebar:

<img width="49" height="153" alt="image" src="https://github.com/user-attachments/assets/11c34995-cfca-4395-8fa5-cadacb048d6f" />

The most foolproof way to reset is to delete the entire `ecommerce-app` repo and run `git clone https://github.com/sourcegraph/ecommerce-app.git` again.

**Next steps**

Once the UI loads at [http://localhost:3001](http://localhost:3001), see [DEVELOPMENT.md](DEVELOPMENT.md) for CI and Cursor. To reopen later: VS Code → open the repo folder → **Reopen in Container**.

**What's included in the dev container**

Python 3.13, Node.js 22, dependencies, GitHub CLI, and VS Code extensions listed in [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json). See [.devcontainer/README.md](.devcontainer/README.md) for details and troubleshooting.

### Option 2: Local Installation

For direct installation on your host machine:

1. Install the prerequisites and clone the project:

```bash
# Install homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install just
brew install just

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Install python
uv python install 3.13 --default

# Install node
brew install node

# Install gh CLI and authenticate
brew install gh
gh auth login
```

```bash
# Verify you have the required tools
source $HOME/.local/bin/env
just --version
python --version
uv --version
node --version
```

```bash
git clone https://github.com/sourcegraph/ecommerce-app.git
cd ecommerce-app
```

2. Install dependencies:

```bash
just install-all      # Install all dependencies (backend, frontend)
```

3. Run the application:

```bash
just dev             # Start both services with native hot-reload using concurrently
```

Access the application:

- Frontend: http://localhost:3001
- Backend API: http://localhost:8001

## Development Commands

### Lifecycle Commands

```bash
just dev              # Start both services (native hot-reload, interactive)
just dev-headless     # Start both services in background (for agentic development)
just stop             # Stop headless services
just dev-backend      # Start only backend
just dev-frontend     # Start only frontend
```

### Seed Database

```bash
just seed             # Populate database with sample data (only needed if database changes)
```

### Manual Development (individual services)

Install dependencies (if not already done):

```bash
just install-all      # All dependencies (backend, frontend)
```

Run services individually (if needed):

```bash
just dev-backend      # Start only backend
just dev-frontend     # Start only frontend
```

### Quality

```bash
# backend
just check            # Run linting (ruff) and type checking (mypy)

# formatting
just format           # Format backend (ruff) and frontend (prettier) code

# frontend
just lint             # Lint frontend TypeScript
cd frontend && npm run format:check  # Check frontend formatting without changes
```

#### Pre-Push Validation (Recommended)

Before pushing to CI, ensure all checks pass locally to avoid CI failures:

```bash
# One-time setup (if not done already)
just install-all      # Install all dependencies

# Run complete CI pipeline locally
just ci               # Runs: format check, lint, types, frontend build (mirrors CI)
```

`just ci` runs the same checks as the GitHub Actions CI pipeline:

1. **Backend**: Ruff format check, Ruff lint, MyPy
2. **Frontend**: Prettier check, ESLint, production build

### Build & Deployment

```bash
just build            # Build frontend for production
cd frontend && npm run build  # Alternative frontend build
```

### Database Management

```bash
just reset-db         # Reset SQLite database
just db-shell         # Open SQLite CLI
just migrate-create "message"  # Create new migration
just migrate-up       # Apply migrations
just migrate-down     # Rollback migration
```

### Monitoring & Debugging

```bash
just health           # Check service health
just logs             # View last 100 lines from backend and frontend logs
just logs-follow      # Follow both logs live (Ctrl+C to exit)
```

**Headless Development Workflow:**  
When using `just dev-headless` for agentic development, services run in the background and log to `logs/backend.log` and `logs/frontend.log`. Use `just logs` to inspect output and `just stop` to stop the services.

### Source

Based on the [ecommerce-demo repo](https://github.com/ViaxCo/ecommerce-demo).
