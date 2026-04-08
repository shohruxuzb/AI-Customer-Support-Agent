from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from backend.utils.processor import DocumentProcessor
from backend.services.shared import vector_store

router = APIRouter()
processor = DocumentProcessor()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")
    
    # Save temporary file
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process document
        text = processor.extract_text(file_path)
        chunks = processor.chunk_text(text)
        
        # Add to vector store
        vector_store.add_documents(chunks)
        
        return {"message": f"Successfully processed {file.filename}", "chunks": len(chunks)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
