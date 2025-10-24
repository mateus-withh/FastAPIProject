from app.models import Student


# Banco de dados em memória
students_db = []

# Inicializar com um registro
initial_student = Student(id=1, name="Seu Nome Completo", email="seu.email@example.com")
students_db.append(initial_student)


def get_next_id():
    if students_db:
        return max(student.id for student in students_db) + 1
    return 1
