from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from services.document_service import DocumentService
from services.chroma_service import ChromaService
class EmbeddingService:
    def __init__(self):
        self.document_service = DocumentService()
        self.chroma = ChromaService(embedding_function=self.get_embedding_function())
        pass
    def get_embedding_function(self):
        return OllamaEmbeddings(model="nomic-embed-text")
    

    def get_chroma(self):
        return self.chroma
    
    def add_document_to_chroma(self):
        documents =  self.document_service.load_documents()
        chunks = self.document_service.split_documents(documents)
        db = self.chroma.getDb()

        chunks_with_ids = self.document_service.calculate_chunk_ids(chunks)

        existing_items = db.get(include=[])
        existing_ids = set(existing_items["ids"])
        print(f"Number of existing documents in DB: {len(existing_ids)}")

        new_chunks = [
            chunk for chunk in chunks_with_ids
            if chunk.metadata["id"] not in existing_ids
        ]

        if new_chunks:
            print(f"👉 Adding new documents: {len(new_chunks)}")
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)
        else:
            print("✅ No new documents to add")