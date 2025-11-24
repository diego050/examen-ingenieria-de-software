# src/domain/ports.py

from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Student, Evaluation


# Repository port for Students
class StudentRepository(ABC):

    @abstractmethod
    def find_by_id(self, student_id: int) -> Optional[Student]:
        pass

    @abstractmethod
    def get_all(self) -> List[Student]:
        pass

    @abstractmethod
    def save(self, student: Student) -> Student:
        pass


# Repository port for Evaluations
class EvaluationRepository(ABC):

    @abstractmethod
    def find_by_student_id(self, student_id: int) -> List[Evaluation]:
        pass

    @abstractmethod
    def save(self, evaluation: Evaluation) -> Evaluation:
        pass