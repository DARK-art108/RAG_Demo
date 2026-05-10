from fastapi import FastAPI, HTTPException
from rag_demo.indexer import build_vectorstore
from rag_demo.models import RAGRequest, RAGResponse
from rag_demo.pipeline import run_rag_pipeline

app = FastAPI(
    title="RAG Demo API",
    description="Interactive docs (Swagger UI) for local API testing.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/index_events")
def index_events() -> dict[str, str]:
    try:
        build_vectorstore()
        return {"status": "Vectorstore built successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error building vectorstore: {e}")


@app.post("/rag_events", response_model=RAGResponse, status_code=200)
def query_rag(payload: RAGRequest) -> RAGResponse:
    try:
        return run_rag_pipeline(payload.question, payload.strategy)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running RAG pipeline: {e}")