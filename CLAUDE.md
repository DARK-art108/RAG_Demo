# CLAUDE.md

Guidance for [Claude Code](https://claude.com/product/claude-code) and similar coding agents in this repo.

## What this is

Python **RAG** app: **FastAPI** + **LangChain** (`RecursiveCharacterTextSplitter`, `HuggingFaceEmbeddings`) + **Chroma** (`langchain-chroma`). Markdown in `data/knowledge_base/*.md` is indexed into `data/chroma/` (gitignored). **`retriever.py`** implements retrieval strategies (similarity, hybrid / BM25 + vector, MMR); **`generator.py`** calls **Groq** for answers; **`pipeline.py`** wires retrieval → generation and returns structured responses.

Remote: **https://github.com/DARK-art108/RAG_Demo**

## Commands

| Task | Command |
|------|---------|
| Install deps | `uv sync` |
| Run API (reload) | `uv run python main.py` |
| Custom port | `PORT=9000 uv run python main.py` |
| Dev extras | `uv sync --extra dev` |
| Uvicorn without main | `PYTHONPATH=src uvicorn rag_demo.api:app --reload --host 0.0.0.0 --port 8000` |
| Docker image | `docker build -t rag-demo .` then `docker run --rm -p 8000:8000 --env-file .env rag-demo` |

Default HTTP port is **`8000`** unless **`PORT`** is set (`main.py`). Swagger: `http://127.0.0.1:<PORT>/docs` (always **HTTP** locally). If startup fails with “address already in use”, pick another **`PORT`** or free the bound port.

## Architecture notes

- **Src layout:** code lives in `src/rag_demo/`. The installable package name is `rag_demo`.
- **`main.py`** inserts `repo_root/src` into `sys.path` and prefixes `PYTHONPATH` so Uvicorn’s **reload worker** can import `rag_demo.api:app` without a prior `pip install -e .`.
- **Imports inside `src/rag_demo/`:** use `from rag_demo....`, never `from src.rag_demo....`.
- **`Dockerfile`:** multi-stage build; copies `src`, `data`, and `main.py`; sets `PYTHONPATH=/app/src`; exposes **8000**.

## Configuration

- **`config.py`:** `Settings` — `data_dir`, `persist_dir`, `collection_name`, `embedding_model`, `top_k`, `rerank_top_k`, `groq_api_key`, `groq_model`, `log_level`. Loaded via `python-dotenv` and env vars.
- **Secrets:** `.env` from `.env.example`; support `GROQ_API_KEY` or `CHATGROQ_API_KEY`. Do not commit `.env` or embed API keys in source.

## Current HTTP API

- `GET /healthz` → `{"status":"ok"}`
- `POST /index_events` → `indexer.build_vectorstore()` (load MD → split → embed → Chroma `add_documents`)
- `POST /rag_events` → `pipeline.run_rag_pipeline(question, strategy)`; body matches **`RAGRequest`**: `question` (string, min length 3), `strategy` (default `"hybrid"`). Strategies: **`hybrid`**, **`basic`** (vector similarity), **`mmr`**. Response: **`RAGResponse`** (`strategy`, `question`, `answer`, `sources`).

## Dependencies worth knowing

- **`rank-bm25`** — used by hybrid retrieval (BM25 + vector); keep it in project deps if hybrid mode is used.
- **`langsmith`** — optional tracing when configured via LangSmith env vars.

## Guardrails for edits

- Do not commit `.venv`, `.env`, or `data/chroma/`.
- Indexing and embedding pull in **torch / sentence-transformers**; imports can be slow—keep unnecessary heavy imports out of cold paths if you refactor.
- **`loader.py`:** loads all `*.md` in `source_dir`; keep `return docs` **outside** the file loop so every document is included.
- Chroma persistence: follow the pattern expected by your pinned `langchain-chroma` version (APIs have changed across versions).

## Quick verification

```bash
curl -s http://127.0.0.1:8000/healthz
# After server is up; from repo root with src on path:
uv run python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path('src').resolve())); import rag_demo.api; print('import ok')"
```

Example RAG call (adjust host/port if needed):

```bash
curl -s http://127.0.0.1:8000/rag_events \
  -H "Content-Type: application/json" \
  -d '{"question":"What is in the knowledge base?","strategy":"hybrid"}'
```
