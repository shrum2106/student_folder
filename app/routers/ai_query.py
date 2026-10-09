import sqlite3 
from fastapi import APIRouter, HTTPException
from langchain_ollama import ChatOllama
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["AI Query"])

# Initialize the lightweight local model (Make sure to run: ollama pull llama3.2:1b)
llm = ChatOllama(model="llama3.2:1b", temperature=0)

class QueryRequest(BaseModel):
    question: str

@router.post("/query-students")
def ask_student_database(request: QueryRequest):
    """
    Reads records directly from students.db using sqlite3 and feeds them to 
    the local llama3.2:1b model to answer administrative queries.
    """
    try:
        # 1. Open a direct connection to your local SQLite file
        # Since the app boots from root, the file path is './students.db'
        conn = sqlite3.connect("./students.db")
        cursor = conn.cursor()
        
        # 2. Fetch all registered students from the students table
        cursor.execute("SELECT id, name, roll_number, email FROM students")
        rows = cursor.fetchall()
        conn.close()
        
    except sqlite3.OperationalError as db_err:
        raise HTTPException(
            status_code=500, 
            detail=f"Database reading error. Ensure students.db exists. Details: {str(db_err)}"
        )

    # 3. Format the data rows cleanly into a plain text block for the LLM
    context = "Here is the current list of registered students in our database:\n"
    if not rows:
        context += "No student records are currently found in the database.\n"
    else:
        for row in rows:
            context += f"- ID: {row[0]}, Name: {row[1]}, Roll Number: {row[2]}, Email: {row[3]}\n"

    # 4. Design the system instructions and user prompt boundary
    system_prompt = (
        "You are an intelligent administrative assistant for a Student Management System.\n"
        "Using the database context provided below, accurately answer the user's question.\n"
        "If the context does not contain the information needed to answer, politely state that it isn't available.\n\n"
        f"Database Context:\n{context}\n\n"
        f"User Question: {request.question}\n\n"
        "Answer:"
    )

    # 5. Invoke your local model and capture the text output response
    try:
        response = llm.invoke(system_prompt)
        return {
            "question": request.question,
            "ai_response": response.content
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not connect to Ollama. Ensure 'ollama serve' is working and model is pulled. Details: {str(e)}"
        )
