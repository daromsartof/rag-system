from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredExcelLoader,
    UnstructuredImageLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader
)
from langchain_core.documents import Document
from pathlib import Path
import os

class DocumentProcessor:
    def __init__(self):
        self.supported_extensions = {
            '.pdf': PyPDFLoader,
            '.txt': TextLoader,
            '.csv': CSVLoader,
            '.xlsx': UnstructuredExcelLoader,
            '.xls': UnstructuredExcelLoader,
            '.jpg': UnstructuredImageLoader,
            '.jpeg': UnstructuredImageLoader,
            '.png': UnstructuredImageLoader,
            '.doc': UnstructuredWordDocumentLoader,
            '.docx': UnstructuredWordDocumentLoader,
            '.ppt': UnstructuredPowerPointLoader,
            '.pptx': UnstructuredPowerPointLoader
        }

    def get_loader_for_file(self, file_path: str):
        """Get the appropriate loader for a given file."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {ext}")
        return self.supported_extensions[ext]

    def process_file(self, file_path: str) -> list[Document]:
        """Process a single file and return its documents."""
        try:
            loader_class = self.get_loader_for_file(file_path)
            loader = loader_class(file_path)
            return loader.load()
        except Exception as e:
            raise Exception(f"Error processing file {file_path}: {str(e)}")

    def process_directory(self, directory_path: str) -> list[Document]:
        """Process all supported files in a directory."""
        all_documents = []
        directory = Path(directory_path)

        for file_path in directory.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                try:
                    documents = self.process_file(str(file_path))
                    all_documents.extend(documents)
                except Exception as e:
                    print(f"Warning: Could not process {file_path}: {str(e)}")
                    continue

        return all_documents 