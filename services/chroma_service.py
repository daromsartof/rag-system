from langchain_chroma import Chroma
import os
import shutil

CHROMA_PATH = "chroma"

class ChromaService():
    def __init__(self, embedding_function):
        self.db =  Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function
    )
        
    def getDb(self):
        return self.db 
    
    def clear_database():
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)