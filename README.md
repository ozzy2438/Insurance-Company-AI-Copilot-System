# MTM Copilot Command Centre

Static demo interface for an internal insurance-company AI copilot command center.

## What It Includes

- Overview dashboard with KPI cards and governance alerts
- Copilot chat interface wired to a local Ollama endpoint
- Prompt library for frontline teams
- Experiment registry for AI use cases

## Run Locally

This project is a single static page.

Start a local server from the repo root:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

## Ollama Requirement

The chat panel expects a local Ollama instance at:

- `http://localhost:11434/api/tags`
- `http://localhost:11434/api/chat`

Expected model:

- `deepseek-r1:14b`

Example startup:

```bash
ollama run deepseek-r1:14b
```

## Notes

- This is a demo/training environment and does not use real member data.
- The UI relies on external CDNs for React, ReactDOM, Babel, Tailwind CSS, and Google Fonts.
- AI responses should be reviewed by a human before operational use.
