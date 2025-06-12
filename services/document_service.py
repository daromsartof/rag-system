from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentService:
    def __init__(self):
        self.DATA_PATH = "data"
        pass
    
    def load_documents(self) -> list[Document]:
        loader = PyPDFDirectoryLoader(self.DATA_PATH)
        return loader.load()
    
    def split_documents(self, documents: list[Document]) -> list[Document]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False,
        )
        return splitter.split_documents(documents)
    
    def calculate_chunk_ids(self, chunks: list[Document]) -> list[Document]:
        last_page_id = None
        current_chunk_index = 0

        for chunk in chunks:
            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")
            current_page_id = f"{source}:{page}"

            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0

            chunk.metadata["id"] = f"{current_page_id}:{current_chunk_index}"
            last_page_id = current_page_id

        return chunks
