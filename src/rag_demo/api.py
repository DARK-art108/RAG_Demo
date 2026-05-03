from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from rag_demo.indexer import build_vectorstore

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