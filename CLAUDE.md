# CLAUDE.md

Guidance for [Claude Code](https://claude.com/product/claude-code) and similar coding agents in this repo.

## What this is

Python **RAG** skeleton: **FastAPI** + **LangChain** (`RecursiveCharacterTextSplitter`, `HuggingFaceEmbeddings`) + **Chroma** (`langchain-chroma`). Markdown policies in `data/knowledge_base/*.md` are indexed into `data/chroma/` (gitignored). **`generator.py`**, **`retriever.py`**, and **`pipeline.py`** are placeholders for query, retrieval, and full RAG orchestration.

Remote: **https://github.com/DARK-art108/RAG_Demo**

## Commands

| Task | Command |
|------|---------|
| Install deps | `uv sync` |
| Run API (reload) | `uv run python main.py` |
| Custom port | `PORT=9000 uv run python main.py` |
| Dev extras | `uv sync --extra dev` |
| Uvicorn without main | `PYTHONPATH=src uvicorn rag_demo.api:app --reload --host 0.0.0.0 --port 8000` |

Swagger: `http://127.0.0.1:8000/docs` (always **HTTP** locally).

## Architecture notes

- **Src layout:** code lives in `src/rag_demo/`. The installable package name is `rag_demo`.
- **`main.py`** inserts `repo_root/src` into `sys.path` and prefixes `PYTHONPATH` so Uvicorn’s **reload worker** can import `rag_demo.api:app` without a prior `pip install -e .`.
- **Imports inside `src/rag_demo/`:** use `from rag_demo....`, never `from src.rag_demo....`.

## Configuration

- **`config.py`:** `Settings` — `data_dir`, `persist_dir`, `collection_name`, `embedding_model`, `top_k`, `rerank_top_k`, `groq_api_key`, `groq_model`. Loaded via `python-dotenv` and env vars.
- **Secrets:** `.env` from `.env.example`; support `GROQ_API_KEY` or `CHATGROQ_API_KEY`. Do not commit `.env`.

## Current HTTP API

- `GET /healthz`
- `POST /index_events` → `indexer.build_vectorstore()` (load MD → split → embed → Chroma `add_documents`)

## Guardrails for edits

- Do not commit `.venv`, `.env`, or `data/chroma/`.
- Indexing pulls in **torch / sentence-transformers**; imports can be slow—keep unnecessary heavy imports out of cold paths if you refactor.
- **`loader.py`:** loads all `*.md` in `source_dir`; keep `return docs` **outside** the file loop so every document is included.
- Chroma persistence: follow the pattern expected by your pinned `langchain-chroma` version (APIs have changed across versions).

## Quick verification

```bash
curl -s http://127.0.0.1:8000/healthz
# After server is up; from repo root with src on path:
uv run python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path('src').resolve())); import rag_demo.api; print('import ok')"
```
