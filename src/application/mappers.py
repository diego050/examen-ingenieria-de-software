# src/application/mappers.py
from typing import Dict, Any
from src.domain.models import Student, Evaluation


class StudentMapper:
    """Maps Student domain model to/from DTOs (Data Transfer Objects)."""

    @staticmethod
    def to_dict(student: Student) -> Dict[str, Any]:
        return {
            "id": student.id,
            "code": student.code,
            "nombre": student.nombre,
            "attendance": student.attendance,
        }

    @staticmethod
    def to_student(data: Dict[str, Any]) -> Student:
        return Student(
            id=data.get("id"),
            code=data["code"],
            nombre=data["nombre"],
            attendance=data.get("attendance", True),
        )

    @staticmethod
    def to_list(students: list) -> list:
        return [StudentMapper.to_dict(s) for s in students]


class EvaluationMapper:
    """Maps Evaluation domain model to/from DTOs."""

    @staticmethod
    def to_dict(evaluation: Evaluation) -> Dict[str, Any]:
        return {
            "id": evaluation.id,
            "student_id": evaluation.student_id,
            "score": evaluation.score,
            "weight": evaluation.weight,
        }

    @staticmethod
    def to_evaluation(data: Dict[str, Any]) -> Evaluation:
        return Evaluation(
            id=data.get("id"),
            student_id=data["student_id"],
            score=float(data["score"]),
            weight=float(data["weight"]),
        )

    @staticmethod
    def to_list(evaluations: list) -> list:
        return [EvaluationMapper.to_dict(e) for e in evaluations]
