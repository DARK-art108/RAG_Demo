# RAG Demo

A **retrieval-augmented generation (RAG)** demo using [LangChain](https://python.langchain.com/), [ChromaDB](https://www.trychroma.com/), [FastAPI](https://fastapi.tiangolo.com/), and [sentence-transformers](https://www.sbert.net/) embeddings. Policy-style Markdown under `data/knowledge_base/` is chunked, embedded, and stored in a local Chroma index under `data/chroma/` (gitignored). **Groq** powers answer generation; retrieval supports vector similarity, **hybrid** (BM25 + vector via `rank-bm25`), and **MMR**.

**Repository:** [github.com/DARK-art108/RAG_Demo](https://github.com/DARK-art108/RAG_Demo)

## Requirements

- Python **3.12+** (see `.python-version`)
- [uv](https://docs.astral.sh/uv/) — use `uv sync` so `uv.lock` stays the source of truth

## Quick start

```bash
git clone https://github.com/DARK-art108/RAG_Demo.git
cd RAG_Demo
uv sync
cp .env.example .env
# Edit .env: set GROQ_API_KEY (or CHATGROQ_API_KEY) and optional GROQ_MODEL.
```

Start the API (plain **HTTP**, default port **8000**):

```bash
uv run python main.py
```

| URL | Purpose |
|-----|---------|
| [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) | Swagger UI (“Try it out”) |
| [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) | ReDoc |
| [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json) | OpenAPI schema |

Use **`http://`**, not **`https://`**, for local Uvicorn.

```bash
PORT=9000 uv run python main.py   # custom port if 8000 is busy
```

## API

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/healthz` | Liveness: `{"status":"ok"}` |
| `POST` | `/index_events` | Reads `data/knowledge_base/*.md`, splits with `RecursiveCharacterTextSplitter`, embeds with `HuggingFaceEmbeddings`, persists to Chroma at `settings.persist_dir` |
| `POST` | `/rag_events` | Runs RAG: JSON body `{"question": "<text>", "strategy": "hybrid" \| "basic" \| "mmr"}`. Returns answer plus source paths (`RAGResponse`) |

Paths, collection name, embedding model id, retrieval sizes, and Groq defaults live in **`src/rag_demo/config.py`** (overridable via env; see **`.env.example`**).

**Example:**

```bash
curl -s http://127.0.0.1:8000/rag_events \
  -H "Content-Type: application/json" \
  -d '{"question":"Summarize the main policies in the knowledge base.","strategy":"hybrid"}'
```

Index once before querying (or after changing Markdown):

```bash
curl -s -X POST http://127.0.0.1:8000/index_events
```

## Docker

From the repo root:

```bash
docker build -t rag-demo .
docker run --rm -p 8000:8000 --env-file .env rag-demo
```

The image exposes **8000** and runs `python main.py` (same **`PORT`** env semantics as locally).

## Project layout

```
├── main.py                 # Prepends src/ to sys.path + PYTHONPATH; runs Uvicorn reload
├── Dockerfile              # Multi-stage image; PYTHONPATH=/app/src
├── pyproject.toml          # Dependencies; setuptools package-dir = src
├── uv.lock
├── CLAUDE.md               # Notes for AI assistants (Claude Code, etc.)
├── src/rag_demo/
│   ├── api.py              # FastAPI app + routes
│   ├── config.py           # Settings + dotenv
│   ├── loader.py           # Markdown → LangChain Documents
│   ├── indexer.py          # build_vectorstore(): split, embed, Chroma
│   ├── retriever.py        # Similarity, hybrid (BM25 + vector), MMR retrieval
│   ├── generator.py        # Groq-backed answer generation
│   ├── pipeline.py         # run_rag_pipeline(): retrieve → generate
│   ├── models.py           # RAGRequest / RAGResponse
│   └── logger.py           # Logging helper
├── data/knowledge_base/    # Sample *.md corpora
└── notebooks/              # Optional experiments
```

## Development

- **Editable install (optional):** `uv pip install -e .`
- **CLI uvicorn without `main.py`:** `PYTHONPATH=src uvicorn rag_demo.api:app --reload --host 0.0.0.0 --port 8000`
- **Gitignored:** `.venv/`, `.env`, `data/chroma/` (generated index)
- **Dev dependencies:** `uv sync --extra dev` (Jupyter, ipykernel)
- **LangSmith:** optional tracing when LangSmith environment variables are set (see LangSmith docs)

## Troubleshooting

- **`ModuleNotFoundError: rag_demo`** — Run from repo root with `uv run python main.py`, or set `PYTHONPATH=src`, or `uv pip install -e .`.
- **Browser “invalid HTTP response”** — Use `http://` only; avoid another process bound to the same port (`lsof -i :8000`).
- **First `/index_events` or `/rag_events` is slow** — sentence-transformers and Chroma warm-up; subsequent calls are faster.
- **`Could not import rank_bm25`** — Run `uv sync` so `rank-bm25` is installed (required for **hybrid** retrieval).

## License

Add a `LICENSE` file when you choose a license for this project.
