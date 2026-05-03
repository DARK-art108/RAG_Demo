from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag_demo.config import settings
from rag_demo.loader import load_md_documents

def build_vectorstore() -> Chroma:
    try:
        raw_docs = load_md_documents(settings.data_dir)
        splitter = RecursiveCharacterTextSplitter(chunk_size=700, 
        chunk_overlap=120,
        separators=["\n##", "\n\n", "\n", " ", "", "\n###"],
        )
        chunks = splitter.split_documents(raw_docs)

        #define embedding model
        embedding_model = HuggingFaceEmbeddings(model_name=settings.embedding_model)

        vectorestore = Chroma(
            collection_name=settings.collection_name,
            embedding_function=embedding_model,
            persist_directory=settings.persist_dir,
        )
        vectorestore.add_documents(chunks)
        #vectorestore.persist()
        return vectorestore
    except Exception as e:
        raise ValueError(f"Error building vectorstore: {e}")
    


