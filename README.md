# RAG Demo

A small **retrieval-augmented generation (RAG)** demo using [LangChain](https://python.langchain.com/), [ChromaDB](https://www.trychroma.com/), [FastAPI](https://fastapi.tiangolo.com/), and [sentence-transformers](https://www.sbert.net/) embeddings. Policy-style Markdown lives under `data/knowledge_base/`; the API can build a persisted vector store you can later wire to a query/LLM flow.

**Upstream repo:** [https://github.com/DARK-art108/RAG_Demo](https://github.com/DARK-art108/RAG_Demo)

## Requirements

- Python **3.12+**
- [uv](https://docs.astral.sh/uv/) (recommended) or another tool that respects `pyproject.toml` / `uv.lock`

## Quick start

```bash
git clone https://github.com/DARK-art108/RAG_Demo.git
cd RAG_Demo
uv sync
cp .env.example .env
# Edit .env and set GROQ_API_KEY (and optional GROQ_MODEL) for later LLM steps.
```

Run the API (default **http** port **8000**):

```bash
uv run python main.py
```

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

Use **`http://`**, not `https://`, for local Uvicorn.

Override port:

```bash
PORT=9000 uv run python main.py
```

## API

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/healthz` | Liveness check |
| `POST` | `/index_events` | Load Markdown from `data/knowledge_base/`, chunk, embed, persist to Chroma under `data/chroma/` |

Configuration (paths, model names, Groq settings) is in `src/rag_demo/config.py` and can be influenced by environment variables (see `.env.example`).

## Project layout

```
├── main.py              # Dev entrypoint: sets PYTHONPATH for src layout, runs Uvicorn
├── pyproject.toml       # Dependencies and setuptools src layout (package under src/)
├── src/rag_demo/        # Application package
│   ├── api.py           # FastAPI app
│   ├── config.py        # Settings
│   ├── loader.py        # Markdown loading
│   └── indexer.py       # Split, embed, Chroma persist
├── data/knowledge_base/ # Sample .md sources for indexing
└── notebooks/           # Optional experiments
```

## Development notes

- Install in editable mode (optional): `uv pip install -e .` from the repo root.
- If you run `uvicorn rag_demo.api:app` directly, set `PYTHONPATH=src` or install the package so `rag_demo` resolves.
- Generated Chroma files under `data/chroma/` are ignored by git (see `.gitignore`).

## License

Add a `LICENSE` file if you intend to open-source this repo under specific terms.
