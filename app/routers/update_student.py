from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.model import Student
from app.schemas import StudentCreate, StudentResponse

router = APIRouter(prefix="/api", tags=["Students"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.put("/students/{roll_number}", response_model=StudentResponse)
def update_student(roll_number: str, updated_data: StudentCreate, db: Session = Depends(get_db)):
    # 1. Find the target student row
    student = db.query(Student).filter(Student.roll_number == roll_number).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot update. Student with roll number '{roll_number}' not found."
        )
    
    # 2. Check if they are trying to modify the roll number to one that someone else already owns
    if updated_data.roll_number != roll_number:
        duplicate_check = db.query(Student).filter(Student.roll_number == updated_data.roll_number).first()
        if duplicate_check:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Modification conflict. The new roll number is already assigned to another student."
            )

    # 3. Overwrite the database fields with the incoming schema values
    student.name = updated_data.name
    student.roll_number = updated_data.roll_number
    student.email = updated_data.email
    
    db.commit()
    db.refresh(student)
    
    return student
