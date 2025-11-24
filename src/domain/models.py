from dataclasses import dataclass

# Domain models adapted to the exam: Student and Evaluation

@dataclass
class Student:
    id: int
    code: str
    nombre: str
    attendance: bool


@dataclass
class Evaluation:
    id: int
    student_id: int
    score: float
    weight: float