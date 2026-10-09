# Student Management System API with Local Ollama RAG

A FastAPI-based student record management system with SQLite storage and a local AI RAG extension powered by Ollama.

## Setup Instructions

1. **Clone the project repository**
2. **Create and Activate a Virtual Environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. **Install Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Pull Local AI Model:**
   ```powershell
   ollama pull llama3.2:1b
   ```

## Running the Server
Execute the application from the root folder:
```powershell
python -m uvicorn main:app --reload
```
Open your browser to test the endpoints: `http://127.0.0`
