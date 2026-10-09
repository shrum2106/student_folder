from pydantic import BaseModel, EmailStr
from typing import Optional

# 1. Shared attributes used when creating or reading data
class StudentBase(BaseModel):
    name: str
    roll_number: str
    email: EmailStr  # Automatically validates that inputs are real email formats

# 2. Schema used when receiving data from a user request (Creating a student)
class StudentCreate(StudentBase):
    pass  # Inherits name, roll_number, and email automatically

# 3. Schema used when sending data back to the user response (Reading a student)
class StudentResponse(StudentBase):
    id: int  # Includes the database primary key ID

    # Tells Pydantic to read database data models (SQLAlchemy) smoothly
    model_config = {"from_attributes": True}
