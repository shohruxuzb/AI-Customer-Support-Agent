import io
from pypdf import PdfReader

def extract_text_from_bytes(file_bytes: bytes, filename: str) -> str:
    """
    Extracts text from a given file representation based on its extension.
    """
    if filename.lower().endswith(".pdf"):
        return _extract_text_from_pdf(file_bytes)
    elif filename.lower().endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")
    else:
        raise ValueError("Unsupported file format. Please upload a .pdf or .txt file.")

def _extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Helper function to extract text from a PDF memory bytes using PyPDF.
    """
    pdf_file = io.BytesIO(file_bytes)
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text
