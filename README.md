# RAG Demo

A small **retrieval-augmented generation (RAG)** demo using [LangChain](https://python.langchain.com/), [ChromaDB](https://www.trychroma.com/), [FastAPI](https://fastapi.tiangolo.com/), and [sentence-transformers](https://www.sbert.net/) embeddings. Policy-style Markdown under `data/knowledge_base/` is chunked, embedded, and written to a local Chroma store under `data/chroma/` via the API. Groq-backed generation can be wired in next using settings from `config.py`.

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
# Set GROQ_API_KEY (and optional GROQ_MODEL) when you add chat/query endpoints.
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
PORT=9000 uv run python main.py   # custom port
```

## API

| Method | Path | Description |
|--------|------|---------------|
| `GET` | `/healthz` | Liveness: `{"status":"ok"}` |
| `POST` | `/index_events` | Reads `data/knowledge_base/*.md`, splits with `RecursiveCharacterTextSplitter`, embeds with `HuggingFaceEmbeddings`, adds documents to Chroma at `settings.persist_dir` |

Paths, collection name, embedding model id, and Groq defaults live in **`src/rag_demo/config.py`** (overridable via env; see **`.env.example`**).

## Project layout

```
├── main.py                 # Prepends src/ to sys.path + PYTHONPATH; runs Uvicorn reload
├── pyproject.toml          # Dependencies; setuptools package-dir = src
├── uv.lock
├── CLAUDE.md               # Notes for AI assistants (Claude Code, etc.)
├── src/rag_demo/
│   ├── api.py              # FastAPI app + OpenAPI metadata
│   ├── config.py           # Pydantic Settings + dotenv
│   ├── loader.py           # Markdown → LangChain Documents
│   ├── indexer.py          # build_vectorstore(): split, embed, Chroma
│   ├── retriever.py        # Reserved for retrieval helpers
│   ├── generator.py        # Reserved for LLM / Groq generation
│   └── pipeline.py         # Reserved for end-to-end RAG orchestration
├── data/knowledge_base/    # Sample *.md corpora
└── notebooks/              # Optional experiments
```

## Development

- **Editable install (optional):** `uv pip install -e .`
- **CLI uvicorn without `main.py`:** `PYTHONPATH=src uvicorn rag_demo.api:app --reload --host 0.0.0.0 --port 8000`
- **Gitignored:** `.venv/`, `.env`, `data/chroma/` (generated index)
- **Dev dependencies:** `uv sync --extra dev` (Jupyter, ipykernel)

## Troubleshooting

- **`ModuleNotFoundError: rag_demo`** — Run from repo root with `uv run python main.py`, or set `PYTHONPATH=src`, or `uv pip install -e .`.
- **Browser “invalid HTTP response”** — Use `http://` only; avoid another process bound to the same port (`lsof -i :8000`).
- **First `/index_events` is slow** — sentence-transformers and Chroma warm-up; subsequent calls are faster.

## License

Add a `LICENSE` file when you choose a license for this project.
