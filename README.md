# 🧠 SimpleAgent

**SimpleAgent** is a modular AI orchestration framework that routes user prompts through a collection of dynamic tools. It supports automatic tool selection, traceable execution, and editable LLM prompt templates via `instructions.md` — all containerized for consistent local development and deployment.

---

## ✨ Features

- 🔌 **Plug-and-play tools**: Each tool lives in its own folder with a `logic.py`, `tool.json`, and `instructions.md`.
- 🗣️ **LLM fallback support**: If no tool matches, a general LLM is used to handle the request.
- 🧩 **Dynamic routing**: Prompts are split into semantic chunks, each routed to the most confident tool.
- 📋 **Trace panel UI**: Live trace of tool calls, color-coded and displayed alongside responses.
- 🌗 **Dark mode ready**: Tailwind-powered UI for fast customization.
- ⚙️ **Dockerized**: Works cleanly across architectures — including Mac M1/M2+.

---

## 🧱 Folder Structure

```
SimpleAgent/
├── backend/
│   ├── main.py               # FastAPI server
│   ├── orchestrator.py       # Prompt planner, tool runner
│   ├── llm_wrapper.py        # Wrapper for OpenAI or local models
│   └── tools/
│       └── <tool-name>/
│           ├── logic.py
│           ├── tool.json
│           └── instructions.md
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── PromptInput.tsx
│   │   │   └── TracePanel.tsx
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── index.html
├── docker-compose.yml
└── README.md
```

---

## 🚀 Running It

### First Time Setup

```bash
# Start fresh (removes containers and volumes)
docker compose down -v

# Build without cache to avoid stale cross-arch artifacts
docker compose build --no-cache

# Run the full stack
docker compose up
```

### Access

- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend API: [http://localhost:8000/ask](http://localhost:8000/ask)

---

## ⚠️ macOS ARM (M1/M2) Quirks

You **must** avoid contaminating Linux Docker containers with macOS/ARM-native files (especially `node_modules`).

### Rules:

- ✅ Use `.dockerignore` to exclude `node_modules/` and lockfiles generated on Mac
- ✅ Always rebuild dependencies **inside** the container
- ✅ Use `npm ci --include=optional` or `pnpm install` during Dockerfile execution
- 🚫 Do not bind-mount `./frontend:/app` — only mount specific subfolders (`src/`, `index.html`, etc.)

### Gotchas:

- `esbuild`, `rollup`, and `vite` break if built for macOS but run in Linux containers
- Rebuild your lockfile from scratch if switching platforms

---

## 🔧 Tool Template

Each tool must include:

### `tool.json`

```json
{
  "name": "Motivational Quotes",
  "module": "tools.motivation.logic",
  "function": "generate_motivation",
  "arguments": { "text": "str" },
  "requires": ["llm"],
  "keywords": ["motivate", "encourage", "inspire"]
}
```

### `instructions.md`

```
Provide a motivational message for the following context:

{text}
```

### `logic.py`

The tool reads `instructions.md`, replaces `{text}`, and uses `llm_helper()` to get a response.

---

## 🧠 Future Ideas

- [ ] Tool-level vector search hints
- [ ] Support for external tool services (HTTP, file system, SMB mounts)
- [ ] Persistent session + trace history
- [ ] Agent-to-agent chaining with rerouting

---

## 📜 License

MIT — Build your own agents and give them feelings.
