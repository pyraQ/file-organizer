# File Organizer

This repository implements a FastAPI backend, LangGraph-enabled ingestion pipeline, lightweight MetaDB/VectorDB adapters, and a Tauri + React desktop UI.

## Layout
- `server/`: FastAPI app, ingestion pipeline, LangGraph workflow, and database adapters.
- `app/`: Tauri + React frontend with drag-and-drop ingestion, queue visualization, and search UI.
- `docs/`: Architecture overview.

## Backend
1. Install dependencies:
   ```bash
   pip install -r server/requirements.txt
   ```
2. Run the API:
   ```bash
   uvicorn server.main:app --reload
   ```
3. OpenAPI contract lives in `server/openapi.yaml`.

## Frontend
1. Install dependencies:
   ```bash
   cd app && npm install
   ```
2. Launch Vite dev server:
   ```bash
   npm run dev
   ```
3. Tauri desktop shell is configured in `app/src-tauri/tauri.conf.json` and can be started with `npm run tauri`.

## Tests
Backend tests are available via `pytest` in `server/tests`.
