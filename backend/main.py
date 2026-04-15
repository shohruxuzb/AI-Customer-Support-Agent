from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.schemas import ChatRequest, ChatResponse
from backend.services.document_loader import extract_text_from_bytes
from backend.services.embeddings import chunk_text, generate_embeddings
from backend.services.vector_store import vector_store
from backend.services.rag import run_rag_pipeline

app = FastAPI(title="AI Customer Support Agent API", version="1.0")

# Add CORS middleware for Streamlit connection if running on different ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")
    
    try:
        content = await file.read()
        
        # 1. Extract text
        text = extract_text_from_bytes(content, file.filename)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Document contains no extractable text.")
            
        # 2. Chunk text
        chunks = chunk_text(text)
        
        if not chunks:
            raise HTTPException(status_code=400, detail="Could not create chunks from document.")
            
        # 3. Embed text
        embeddings = generate_embeddings(chunks)
        
        # 4. Store in vector DB
        vector_store.add_texts(chunks, embeddings)
        
        return {
            "message": f"Successfully processed {file.filename}",
            "chunks_added": len(chunks)
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    try:
        answer = run_rag_pipeline(request)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")
