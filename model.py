from sqlalchemy import Column, Integer, String
# Change this line if it has 'app.database'
# Change line 2 from 'from database import Base' to:
from app.database import Base



class Student(Base):
    # This sets the actual name of the table inside your database file
    __tablename__ = "students"

    # Define your table columns/fields
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    roll_number = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
