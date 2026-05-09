from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from rag_demo.config import settings

from langchain_community.retrievers import BM25Retriever

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

def hybrid_retrieval(query:str) -> list[Document]:
    #dense retrieval
    docs = basic_smilarity_retrieval(query) #pass 1 we got n results let 5 reuslts
    docs.extend(mmr_retrieval(query, k=settings.top_k)) #pass 2 we are narrow down the results to 3 results

    #sparse retrieval
    bm25_retriever = BM25Retriever.from_documents(docs)
    bm25_retriever.k = settings.top_k
    docs.extend(bm25_retriever.get_relevant_documents(query))
    return docs
