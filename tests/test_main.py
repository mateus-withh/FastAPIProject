import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import students_db

client = TestClient(app)


class TestStudentAPI:
    def test_root(self):
        """Teste da rota raiz"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Student API is running!"}

    def test_get_all_students_success(self):
        """Teste de sucesso para listar todos os alunos"""
        response = client.get("/students")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0

    def test_get_student_by_id_success(self):
        """Teste de sucesso para buscar aluno por ID"""
        response = client.get("/students/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "name" in data
        assert "email" in data

    def test_get_student_by_id_not_found(self):
        """Teste de falha para buscar aluno por ID inexistente"""
        response = client.get("/students/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Student not found"

    def test_create_student_success(self):
        """Teste de sucesso para criar novo aluno"""
        new_student = {"name": "Novo Aluno", "email": "novo.aluno@example.com"}
        response = client.post("/students", json=new_student)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == new_student["name"]
        assert data["email"] == new_student["email"]
        assert "id" in data

    def test_create_student_duplicate_email(self):
        """Teste de falha para criar aluno com email duplicado"""
        # Primeiro, criar um aluno
        student_data = {"name": "Aluno Teste", "email": "teste.duplicado@example.com"}
        client.post("/students", json=student_data)

        # Tentar criar outro com mesmo email
        response = client.post("/students", json=student_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "Email already registered"

    def test_create_student_invalid_email(self):
        """Teste de falha para criar aluno com email inválido"""
        invalid_student = {"name": "Aluno Inválido", "email": "email-invalido"}
        response = client.post("/students", json=invalid_student)
        assert response.status_code == 422  # Unprocessable Entity
