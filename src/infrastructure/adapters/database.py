# src/infrastructure/adapters/database.py
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import Table, Column, Integer, String, Float, MetaData, select, Boolean, ForeignKey
from src.domain.models import Student as DomainStudent, Evaluation as DomainEvaluation
from src.domain.ports import StudentRepository, EvaluationRepository

# Database table mappings
metadata = MetaData()

students_table = Table(
    'students', metadata,
    Column('id', Integer, primary_key=True),
    Column('code', String(50), unique=True),
    Column('nombre', String(150)),
    Column('attendance', Boolean, default=True)
)

evaluations_table = Table(
    'evaluations', metadata,
    Column('id', Integer, primary_key=True),
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('score', Float),
    Column('weight', Float)
)


class SQLAlchemyStudentRepository(StudentRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[DomainStudent]:
        stmt = select(students_table)
        rows = self.session.execute(stmt).all()
        return [DomainStudent(**row._asdict()) for row in rows]

    def save(self, student: DomainStudent) -> DomainStudent:
        # If student has no id, perform INSERT, otherwise UPDATE existing row.
        if getattr(student, 'id', None) is None:
            stmt = students_table.insert().values(
                code=student.code,
                nombre=student.nombre,
                attendance=student.attendance
            )
            result = self.session.execute(stmt)
            self.session.commit()
            student.id = result.inserted_primary_key[0]
            return student
        else:
            stmt = students_table.update().where(students_table.c.id == student.id).values(
                code=student.code,
                nombre=student.nombre,
                attendance=student.attendance
            )
            self.session.execute(stmt)
            self.session.commit()
            return student

    def find_by_id(self, student_id: int) -> Optional[DomainStudent]:
        stmt = select(students_table).where(students_table.c.id == student_id)
        row = self.session.execute(stmt).first()
        return DomainStudent(**row._asdict()) if row else None


class SQLAlchemyEvaluationRepository(EvaluationRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_by_student_id(self, student_id: int) -> list[DomainEvaluation]:
        stmt = select(evaluations_table).where(evaluations_table.c.student_id == student_id)
        rows = self.session.execute(stmt).all()
        return [DomainEvaluation(**row._asdict()) for row in rows]

    def save(self, evaluation: DomainEvaluation) -> DomainEvaluation:
        stmt = evaluations_table.insert().values(
            student_id=evaluation.student_id,
            score=evaluation.score,
            weight=evaluation.weight
        )
        result = self.session.execute(stmt)
        self.session.commit()
        evaluation.id = result.inserted_primary_key[0]
        return evaluation