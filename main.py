from fastapi import FastAPI
from app.database import engine, Base
from app.routers import api_router 

app = FastAPI(title="Student Management System API with Gemini RAG")

# Keep database schema creation active on startup
Base.metadata.create_all(bind=engine)

# Include the central master router package module
app.include_router(api_router)

@app.get("/", tags=["General"])
def root():
    return {"message": "Welcome to your Student Management API Backend!"}




### paste this to see this homepage 127.0.0.1:8000/docs
