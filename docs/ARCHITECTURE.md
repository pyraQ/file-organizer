# File Organizer Architecture

## Backend (server/)
- **FastAPI** application (`server/main.py`) exposes endpoints defined in `server/openapi.yaml`.
- **Configuration** is centralized in `server/core/config.py` with sensible defaults for storage and vector settings.
- **Ingestion pipeline** (`server/ingestion/`) handles parsing, hashing, file storage, LangGraph workflow execution, and queueing.
- **Workflow** integration via `server/workflows/langgraph.py` produces embeddings and enriches metadata.
- **Persistence** uses lightweight in-memory adapters: `server/db/metadb.py` for metadata and `server/db/vectordb.py` for vector similarity.
- **Schemas** for requests/responses live in `server/schemas.py` and mirror the OpenAPI specification.

## Frontend (app/)
- **Tauri + React** scaffold (`app/package.json`, `app/src-tauri/`) gives a desktop shell around a Vite React UI.
- **Drag-and-drop ingestion** (`DragDropArea`) surfaces enqueue behavior.
- **Queue visualization** (`QueueVisualization`) displays pending items.
- **Search panel** (`SearchPanel`) offers semantic search UI plumbing and result rendering.

## Data Flow
1. Users drop or select files in the Tauri UI.
2. The UI invokes backend ingestion (`POST /ingest/files`) to enqueue and process files.
3. The FastAPI pipeline copies the file to storage, parses metadata, hashes content, and runs the LangGraph workflow to generate embeddings.
4. Metadata lands in MetaDB; embeddings are stored in VectorDB.
5. Search queries (`POST /search`) generate an embedding and return ranked hits with metadata for display in the UI.
