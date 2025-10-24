from fastapi import FastAPI, HTTPException
from app.models import Student, StudentCreate
from app.database import students_db, get_next_id

app = FastAPI(title="Student API", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Student API is running!"}


@app.get("/students", response_model=list[Student])
async def get_all_students():
    """Listar todos os alunos"""
    return students_db


@app.get("/students/{student_id}", response_model=Student)
async def get_student_by_id(student_id: int):
    """Buscar aluno por ID"""
    student = next((s for s in students_db if s.id == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.post("/students", response_model=Student)
async def create_student(student: StudentCreate):
    """Criar novo aluno"""
    # Verificar se email já existe
    if any(s.email == student.email for s in students_db):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_student = Student(
        id=get_next_id(),
        name=student.name,
        email=student.email
    )
    students_db.append(new_student)
    return new_student