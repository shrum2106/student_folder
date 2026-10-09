from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.model import Student

router = APIRouter(prefix="/api", tags=["Students"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.delete("/students/{roll_number}", status_code=status.HTTP_200_OK)
def delete_student(roll_number: str, db: Session = Depends(get_db)):
    # 1. Search for the student entry in students.db
    student = db.query(Student).filter(Student.roll_number == roll_number).first()
    
    # 2. If the student doesn't exist, raise a 404 error
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot delete. Student with roll number '{roll_number}' not found."
        )
    
    # 3. Delete from the database file and save the transaction
    db.delete(student)
    db.commit()
    
    return {"status": "success", "message": f"Student profile with roll number '{roll_number}' deleted successfully."}
