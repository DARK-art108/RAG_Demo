"""This module has the modals for the RAG pipeline"""

from pydantic import BaseModel, Field

class RAGRequest(BaseModel):
    question: str = Field(..., min_length=3)
    strategy: str = Field(default="hybrid")

class RAGResponse(BaseModel):
    strategy: str
    question: str
    answer: str
    sources: list[str]