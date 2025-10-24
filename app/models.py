from pydantic import BaseModel, EmailStr
from typing import Optional


class Student(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr


class StudentCreate(BaseModel):
    name: str
    email: EmailStr
