# Member Operations Copilot Command Centre

Portfolio prototype of an internal AI adoption and operations platform that helps frontline teams use copilots safely, consistently, and measurably across member-service workflows.

## What It Includes

- Routed `Vite + React + TypeScript` application
- `FastAPI + SQLite` synthetic backend with persona-aware API contracts
- Transformation OS shell with team switching across roadside, claims, and member contact contexts
- Overview, Copilot Workspace, Experiment Portfolio, Governance, Knowledge Hub, Adoption Academy, and Impact modules
- Backend-driven synthetic sandbox covering personas, members, policies, cases, interactions, assets, experiments, governance reviews, copilot runs, and audit events
- Optional local Ollama enhancement inside the Copilot Workspace, with safe backend fallback

## Run Locally

Install frontend dependencies:

```bash
npm install
```

Create a Python 3.13 virtual environment and install backend dependencies:

```bash
/opt/homebrew/bin/python3.13 -m venv .venv313
./.venv313/bin/pip install -r backend/requirements.txt
```

Seed the synthetic sandbox:

```bash
./.venv313/bin/python -m backend.scripts.seed_db
```

Start the backend API:

```bash
./.venv313/bin/python -m backend.scripts.run_api
```

In a second terminal, start the Vite dev server:

```bash
npm run dev
```

Then open:

```text
http://localhost:5173
```

Production build:

```bash
npm run build
```

FastAPI docs:

```text
http://localhost:8001/docs
```

## Ollama Requirement

Live local mode in the Copilot Workspace expects a local Ollama instance at:

- `http://localhost:11434/api/tags`
- `http://localhost:11434/api/chat`

Expected model:

- `deepseek-r1:14b`

Example startup:

```bash
ollama run deepseek-r1:14b
```

## Notes

- This is a portfolio concept / demo environment and does not use real member data.
- The default experience runs against a synthetic backend so the app behaves more like a real internal platform than a static frontend mock.
- Live AI remains a secondary capability; the backend still owns context assembly, citations, risk flags, human review points, and audit logging.
- AI responses should be reviewed by a human before operational use.
