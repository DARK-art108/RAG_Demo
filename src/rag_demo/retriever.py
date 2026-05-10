from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from rag_demo.config import settings
from rag_demo.logger import init_logger
from rag_demo.loader import load_md_documents
from langsmith import traceable



from langchain_community.retrievers import BM25Retriever

logger = init_logger()
def get_vectorstore() -> Chroma:
    """Get the vectorstore from the config
    Returns:
        Chroma: The vectorstore
    Raises:
        ValueError: If the vectorstore cannot be created
    """
    try:
        embedding_model = HuggingFaceEmbeddings(model_name=settings.embedding_model)
        return Chroma(
            collection_name=settings.collection_name,
            embedding_function=embedding_model,
            persist_directory=settings.persist_dir,
        )
    except Exception as e: 
        raise ValueError(f"Error getting vectorstore: {e}")

def basic_smilarity_retrieval(query:str, k: int | None = None) -> list[Document]:
    vs = get_vectorstore()
    return vs.similarity_search(query, k=k or settings.top_k)

def mmr_retrieval(query:str, k: int | None = None) -> list[Document]:
    vs = get_vectorstore()
    return vs.max_marginal_relevance_search(query, k=k or settings.top_k)

def simple_keyword_score(doc: Document, query: str) -> int:
    tokens = [token.strip().lower() for token in query.split() if token.strip()]
    doc_text = doc.page_content.lower()
    return sum(1 for token in tokens if token in doc_text)


def rerank_docs(query: str, docs: list[Document]) -> list[Document]:
    ranked = sorted(docs, key=lambda doc: simple_keyword_score(doc, query), reverse=True)
    return ranked[: settings.rerank_top_k]

def hybrid_retrieval(query:str) -> list[Document]:
    #dense retrieval
    docs = basic_smilarity_retrieval(query, k=settings.top_k)
    docs.extend(mmr_retrieval(query, k=settings.top_k))

    raw = get_vectorstore().get()
    logger.info(f"Raw documents: {raw}")
    #corpus = load_md_documents(settings.data_dir)

    corpus = [
        Document(page_content=text, metadata=meta)
        for text, meta in zip(raw["documents"], raw["metadatas"])
    ]

    bm25_retriever = BM25Retriever.from_documents(corpus)
    bm25_retriever.k = settings.top_k
    docs.extend(bm25_retriever.invoke(query))


    merged: dict[str, Document] = {}
    for doc in docs:
            key = f"{doc.metadata.get('source', '')}:{hash(doc.page_content)}"
            merged[key] = doc

    unique_docs = list(merged.values())
    logger.info(f"Unique documents: {unique_docs}")

    try:
        return rerank_docs(query, unique_docs)
    except NameError as e:
        logger.error(f"Error reranking documents: {e}")
        return unique_docs[:settings.top_k]




