import os
import PyPDF2
import textwrap
from typing import List

class DocumentProcessor:
    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extracts text from PDF or TXT files."""
        extension = os.path.splitext(file_path)[1].lower()
        
        if extension == '.pdf':
            return DocumentProcessor._extract_from_pdf(file_path)
        elif extension == '.txt':
            return DocumentProcessor._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {extension}")

    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text

    @staticmethod
    def _extract_from_txt(file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Splits text into smaller chunks with overlap.
        Simple recursive character splitting for now.
        """
        if not text:
            return []
            
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap
            
        return [c.strip() for c in chunks if c.strip()]
