from fastapi import APIRouter

# This builds the placeholder route layout for your AI search
router = APIRouter(prefix="/api", tags=["RAG AI Search"])

@router.get("/rag/ask")
def ask_rag_placeholder():
    return {"message": "RAG router is working from base.py!"}
