# src/application/services.py

from typing import List
from src.domain.models import Student, Evaluation
from src.domain.ports import StudentRepository, EvaluationRepository
from src.application.grade_calculator import GradeCalculator


class StudentService:
    def __init__(self, student_repo: StudentRepository, evaluation_repo: EvaluationRepository):
        self.student_repo = student_repo
        self.evaluation_repo = evaluation_repo
        # Use the grade calculator for business rules (defaults from implementation)
        self.calculator = GradeCalculator()

    def listar_estudiantes(self) -> List[Student]:
        return self.student_repo.get_all()

    def crear_estudiante(self, code: str, nombre: str, attendance: bool = True) -> Student:
        if not code or not nombre:
            raise ValueError("El código y el nombre del estudiante no pueden estar vacíos.")
        nuevo = Student(id=None, code=code, nombre=nombre, attendance=attendance)
        return self.student_repo.save(nuevo)

    def agregar_evaluacion(self, student_id: int, score: float, weight: float) -> Evaluation:
        # verify student exists
        student = self.student_repo.find_by_id(student_id)
        if not student:
            raise ValueError("El estudiante no existe.")
        eval_obj = Evaluation(id=None, student_id=student_id, score=float(score), weight=float(weight))
        return self.evaluation_repo.save(eval_obj)

    def set_attendance(self, student_id: int, reached: bool) -> Student:
        student = self.student_repo.find_by_id(student_id)
        if not student:
            raise ValueError("El estudiante no existe.")
        student.attendance = bool(reached)
        return self.student_repo.save(student)

    def calcular_nota_final(self, student_id: int) -> dict:
        student = self.student_repo.find_by_id(student_id)
        if not student:
            raise ValueError("El estudiante no existe.")

        evaluations = self.evaluation_repo.find_by_student_id(student_id)
        # Configure calculator for this student
        # Clear calculator internal state by creating a temporary one to ensure determinism
        calc = GradeCalculator()
        calc.set_all_years_teachers(False)

        # Add evaluations to calculator
        sid = str(student_id)
        for ev in evaluations:
            calc.add_evaluation(sid, ev.score, ev.weight)

        # Set attendance in calculator
        calc.set_attendance(sid, student.attendance)

        # Compute and return result
        return calc.calculate_final(sid)