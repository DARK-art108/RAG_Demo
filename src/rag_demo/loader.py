from pathlib import Path
from langchain_core.documents import Document

def load_md_documents(source_dir: Path) -> list[Document]:
    """ Load markdown files from the source directory """
    try:
        docs: list[Document] = []
        for path in sorted(source_dir.glob("*.md")):
            content = path.read_text(encoding="utf-8")
            docs.append(
                Document(
                    page_content = content,
                    metadata = {"source": str(path), 
                    "doc_type":"policy", 
                    "doc_name":path.stem}         
                        )
                )
            return docs
    except Exception as e:
        raise ValueError(f"Error loading documents: {e}")
