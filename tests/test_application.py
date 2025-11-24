import pytest
from src.application.services import StudentService
from src.application.mappers import StudentMapper, EvaluationMapper
from src.domain.models import Student, Evaluation
from src.domain.ports import StudentRepository, EvaluationRepository


class FakeStudentRepository(StudentRepository):
    def __init__(self, students=None):
        self._students = students or []
        self._id = 1

    def get_all(self):
        return self._students

    def save(self, student):
        if student.id is None:
            student.id = self._id
            self._id += 1
            self._students.append(student)
        else:
            # update
            for i, s in enumerate(self._students):
                if s.id == student.id:
                    self._students[i] = student
                    break
        return student

    def find_by_id(self, student_id):
        return next((s for s in self._students if s.id == student_id), None)


class FakeEvaluationRepository(EvaluationRepository):
    def __init__(self, evaluations=None):
        self._evaluations = evaluations or []
        self._id = 1

    def find_by_student_id(self, student_id):
        return [e for e in self._evaluations if e.student_id == student_id]

    def save(self, evaluation):
        if evaluation.id is None:
            evaluation.id = self._id
            self._id += 1
            self._evaluations.append(evaluation)
        return evaluation


def test_student_lifecycle_and_grade():
    student_repo = FakeStudentRepository()
    eval_repo = FakeEvaluationRepository()
    service = StudentService(student_repo, eval_repo)

    # Create student
    s = service.crear_estudiante('CODE1', 'Test Student', attendance=True)
    assert s.id is not None

    # Add evaluations
    e1 = service.agregar_evaluacion(s.id, 12, 50)
    e2 = service.agregar_evaluacion(s.id, 18, 50)
    assert e1.id is not None and e2.id is not None

    # Calculate grade
    res = service.calcular_nota_final(s.id)
    assert res['final_grade'] == 15.0


def test_set_attendance_updates_student():
    student_repo = FakeStudentRepository()
    eval_repo = FakeEvaluationRepository()
    service = StudentService(student_repo, eval_repo)

    s = service.crear_estudiante('CODE2', 'Alumno', attendance=True)
    service.set_attendance(s.id, False)
    updated = student_repo.find_by_id(s.id)
    assert updated.attendance is False


def test_mappers():
    s = Student(id=1, code='C1', nombre='Al', attendance=True)
    sd = StudentMapper.to_dict(s)
    assert sd['code'] == 'C1'

    e = Evaluation(id=1, student_id=1, score=14.0, weight=100)
    ed = EvaluationMapper.to_dict(e)
    assert ed['score'] == 14.0