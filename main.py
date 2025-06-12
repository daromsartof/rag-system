from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from services.chroma_service import ChromaService
from services.embedding_service import EmbeddingService
from services.document_processor import DocumentProcessor
import uvicorn
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
import os
from pathlib import Path

# Create data directory if it doesn't exist
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

PROMPT_TEMPLATE = """
You are a knowledgeable assistant. Use the following retrieved context to answer the user question accurately and comprehensively.

[BEGIN CONTEXT]
{context}
[END CONTEXT]

Instructions:
- Use only the information in the context to generate your answer.
- If the context does not contain enough information, respond with: "The available context does not provide a sufficient answer."
- Be concise, factual, and clear.
- Avoid speculation or making up information.

User Question:
{question}

Answer:

"""

def query_rag(query_text: str):
    embedding_service = EmbeddingService()
    chroma = embedding_service.get_chroma()
    db = chroma.getDb()

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=1)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    print(context_text)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    ollama_host = os.getenv("OLLAMA_HOST", "localhost")
    print(f"http://{ollama_host}:11434")
    model = OllamaLLM(model="deepseek-r1:latest", base_url=f"http://{ollama_host}:11434")

    response_text = model.invoke(prompt)

    print(response_text)
    return response_text


app = FastAPI()

class QueryRequest(BaseModel):
    query: str


@app.get("/")
def main_endpoint():
    try:
        return {"detail": "Hello, World!"}
    except Exception as e:
        print(e)    
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def query_endpoint(request: QueryRequest):
    try:
        result = query_rag(request.query)
        return {"result": result}
    except Exception as e:
        print(e)    
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add-documents")
async def add_documents(file: UploadFile = File(...)):
    try:
        file_path = DATA_DIR / file.filename
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Process the document using our new document processor
        document_processor = DocumentProcessor()
        documents = document_processor.process_file(str(file_path))
        
        # Add documents to Chroma
        embedding_service = EmbeddingService()
        embedding_service.add_document_to_chroma(documents)
        
        return {"message": "Documents added successfully"}
    except Exception as e:
        # Clean up file in case of error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3038, reload=True) 
