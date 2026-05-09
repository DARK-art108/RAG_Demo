import os 
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from rag_demo.config import settings

"""This module has the generator for the RAG pipeline"""

ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system",
        "You are a careful banking policy assistant. Answer only from the provided "
        "context. If the context does not contain enough information, say what is "
        "missing and do not invent policy details. Keep answers concise and cite "
        "which source index ([1], [2], ...) you used when relevant.",
        ),
        ("human", "{question}\n\nContext: {context}\n\nAnswer:")
    ]
)


def format_context(docs: list[Document]) -> str:
    "Format context example : [1] /path/to/doc1.md: ... [2] /path/to/doc2.md: ..."
    context_parts = []
    for idx, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "unknown")
        context_parts.append(f"[{idx}] {source}:\n{doc.page_content}")
    return "\n".join(context_parts)


def _groq_api_key() -> str | None:
    key = os.getenv("GROQ_API_KEY") or os.getenv("CHATGROQ_API_KEY") or settings.groq_api_key
    return key.strip() if key and str(key).strip() else None


def _groq_model_name() -> str:
    env_model = (os.getenv("GROQ_MODEL") or "").strip()
    return env_model or settings.groq_model


def _get_llm() -> ChatGroq:
    try:
        api_key = _groq_api_key()
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set")
        model_name = _groq_model_name()
        return ChatGroq(
            model=model_name,
            api_key=api_key,
            temperature=0.1,
            max_retries=2,
        )
    except Exception as e:
        raise ValueError(f"Error getting LLM: {e}")


def build_answer(question:str, docs: list[Document]) -> str:
    if not docs:
        return (
            "I could not find anuyb policy context for this question. Please try again with a different question."

        )

    context = format_context(docs)
    llm = _get_llm()
    chain = ANSWER_PROMPT | llm 
    message = chain.invoke(
        {"question": question, "context": context}
    )
    content = message.content
    if isinstance(content, str):
        return content.strip()
    return str(content).strip()
