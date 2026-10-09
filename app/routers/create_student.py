from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Look up one level out of routers to find database, model, and schemas
from app.database import SessionLocal
from app.model import Student
from app.schemas import StudentCreate, StudentResponse

# Define the isolated sub-router
router = APIRouter(prefix="/api", tags=["Students"])

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# The POST route to create a student record
@router.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.roll_number == student.roll_number).first()
    if db_student:
        raise HTTPException(
            status_code=400, 
            detail="A student with this roll number is already registered."
        )
    
    new_student = Student(
        name=student.name,
        roll_number=student.roll_number,
        email=student.email
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return new_student

Add create student router
