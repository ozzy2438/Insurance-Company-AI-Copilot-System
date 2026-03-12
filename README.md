# Member Operations Copilot Command Centre

A production-style AI adoption platform for member services and insurance operations, designed to show how copilots can be introduced safely, governed properly, and scaled with measurable business value across frontline teams.

This project was built to go beyond a chatbot demo. It models what an internal AI transformation platform could look like in environments such as roadside assistance, claims, and contact centre operations, where teams need faster decision-making, better access to knowledge, stronger governance, and visible performance outcomes.



https://github.com/user-attachments/assets/51336081-fc56-423d-a08d-3e0e84bf70fe


## The Problem It Solves

In many service organisations, AI pilots fail for the same reasons:

- Prompts are created ad hoc and are not governed
- knowledge is fragmented across teams, documents, and workflows
- experiments are run without a clear register, ownership model, or scale decision process
- frontline teams get AI outputs without enough context, traceability, or human review boundaries
- leaders cannot see whether AI usage is improving real operational KPIs

This project addresses those issues by combining copilot workflows, knowledge assets, governance controls, experiment tracking, and KPI visibility inside one operating system.

## What The Platform Does

The platform provides a transformation operating system for AI adoption across member-service workflows:

- `Overview`: executive view of adoption health, governance posture, live experiments, alerts, and KPI movement
- `Copilot Workspace`: role-based AI workbench for roadside, claims, and contact centre scenarios with case context, citations, risk flags, and human review points
- `Experiment Portfolio`: a structured register of pipeline, in-flight, and completed AI experiments with ownership, impact evidence, and decision status
- `Governance & Risk`: visible review controls, policy boundaries, privacy follow-ups, and human-in-the-loop checkpoints
- `Knowledge Hub`: reusable prompts, playbooks, policies, and workflow assets designed for governed reuse
- `Adoption Academy`: enablement tracks, coaching content, and adoption support for frontline teams and managers
- `Impact & KPIs`: measurable outcomes tied to service quality, productivity, reuse, and readiness to scale

## Why It Is Valuable

This is designed to reflect how AI should work in a real business, not just how it looks in a demo.

The platform is intended to help organisations:

- reduce hanRle time by giving frontline users pre-assembled case context and approved next-step guidance
- improve first-contact quality through structured policy and workflow support
- reduce repeated admin effort with reusable drafting and handover workflows
- scale AI more safely by attaching every use case to governance, evidence, and review controls
- increase adoption confidence through approved prompts, enablement assets, and visible operating metrics
- improve trust by logging copilot runs, dCcisions, and review actions in an auditable backend

The synthetic operating model in the sandbox reflects sample impact patterns such as:

- up to `16%` reduction in handle time in roadside workflows
- a `6-point` uplift in first-contact resolution in claims intake
- around `21%` lower admin effort in contact-centre handover workflows

These figures are synthetic portfolio data, included to demonstrate how the impact would be measured and communicated in a real rollout.

## How It Works

Unlike a frontend-only concept, this project includes a backend-driven architecture that simulates how a real organisation would operationalise AI safely.

The backend is responsible for:

- persona-aware access control
- synthetic member, policy, case, and interaction data assembly
- governed scenario retrieval
- copilot run creation
- citation and risk-flag generation
- human review guidance
- experiment and governance action logging
- audit trail visibility

The frontend consumes typed APIs and presents the system as a transformation product rather than a standalone AI chat tool.

## Product Scope

The current sandbox models:

- roadside assistance operations
- insurance and claims workflows
- member contact centre scenarios
- prompt and knowledge asset governance
- AI experiment tracking and scale decisions
- KPI-based adoption and impact measurement
- optional local LLM enhancement via Ollama

## Tech Stack

### Frontend

- `React`
- `TypeScript`
- `Vite`
- `React Router`

### Backend

- `FastAPI`
- `SQLAlchemy 2`
- `SQLite`
- `Pydantic`
- `Alembic`
- `OpenAPI`

### AI / Runtime

- synthetic backend orchestration by default
- optional local `Ollama` integration for live draft enhancement

## Run Locally

Install frontend dependencies:

```bash
npm install
```

Create a Python `3.13` virtual environment and install backend dependencies:

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

In a second terminal, start the frontend:

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

FastAPI docs:

```text
http://localhost:8001/docs
```

Production build:

```bash
npm run build
```

## Optional Live Local AI

Live local mode in the Copilot Workspace expects Ollama at:

- `http://localhost:11434/api/tags`
- `http://localhost:11434/api/chat`

Expected model:

- `deepseek-r1:14b`

Example startup:

```bash
ollama run deepseek-r1:14b
```

If Ollama is not available, the platform still works end-to-end using backend-driven synthetic orchestration.

## Important Notes

- This is a portfolio prototype, not a claimed client deployment.
- All member, policy, and case records are synthetic.
- The project is designed to demonstrate enterprise AI adoption thinking: governance, enablement, experimentation, workflow integration, and measurable value.
- AI-generated outputs should always remain subject to human review before operational use.
