from pydantic import BaseModel
from rag_demo.generator import build_answer
from rag_demo.models import RAGRequest, RAGResponse
from rag_demo.retriever import (
    hybrid_retrieval,
    rerank_docs,
    basic_smilarity_retrieval,
    mmr_retrieval,
)
from rag_demo.logger import init_logger

logger = init_logger()


def run_rag_pipeline(question: str, strategy: str = "hybrid") -> RAGResponse:
    try:
        if strategy == "hybrid":
            docs = hybrid_retrieval(question)
        elif strategy == "basic":
            docs = basic_smilarity_retrieval(question)
        elif strategy == "mmr":
            docs = mmr_retrieval(question)
        else:
            raise ValueError(f"Invalid strategy: {strategy}")
        answer = build_answer(question, docs)
        return RAGResponse(strategy=strategy, question=question, answer=answer, sources=[doc.metadata.get("source", "") for doc in docs])
    except Exception as e:
        logger.error(f"Error running RAG pipeline: {e}")
        return RAGResponse(strategy=strategy, question=question, answer="An error occurred while running the RAG pipeline.", sources=[])