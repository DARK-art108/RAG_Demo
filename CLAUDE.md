# CLAUDE.md

Context for [Claude Code](https://claude.com/product/claude-code) and similar assistants working in this repository.

## Purpose

Python **RAG demo**: LangChain + Chroma + HuggingFace sentence-transformers embeddings, exposed via **FastAPI**. Sample documents are Markdown files in `data/knowledge_base/`. Indexing persists a Chroma store under `data/chroma/` (gitignored).

## Commands

- Sync deps: `uv sync`
- Run API with reload: `uv run python main.py` (default [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs))
- Custom port: `PORT=9000 uv run python main.py`
- Optional dev extras: `uv sync --extra dev`

## Layout conventions

- **Src layout:** importable package is `rag_demo` under `src/rag_demo/`. `main.py` prepends `src` to `sys.path` and `PYTHONPATH` so Uvicorn reload subprocesses resolve `rag_demo.api:app`.
- **Imports:** use `from rag_demo....` inside the package, not `from src.rag_demo....`.

## Configuration

- `src/rag_demo/config.py` — Pydantic `Settings` (paths, embedding model id, Chroma collection name, Groq-related fields).
- Secrets: copy `.env.example` to `.env`; never commit `.env`. Keys: `GROQ_API_KEY`, optional `GROQ_MODEL` (and `CHATGROQ_API_KEY` alias supported in code).

## API surface (current)

- `GET /healthz` — health JSON.
- `POST /index_events` — builds/refreshes vector store from `data/knowledge_base/*.md` via `build_vectorstore()`.

## When changing behavior

- **Indexer / embeddings:** heavy first import; keep API imports light where possible.
- **Ports:** default `8000` via `PORT` env in `main.py`; local docs must use **HTTP**, not HTTPS.
- **Do not** commit `.venv`, `.env`, or `data/chroma/`.

## Testing suggestions

After edits, smoke-check: `uv run python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path('src').resolve())); import rag_demo.api; print('ok')"` or hit `/healthz` with curl.
