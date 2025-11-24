import pytest
from src.application.grade_calculator import GradeCalculator


def test_add_and_calculate_basic():
    gc = GradeCalculator()
    # Two evaluations: 12/20 with 50%, 18/20 with 50% => avg = (12*50 + 18*50)/100 = 15
    gc.add_evaluation('s1', 12, 50)
    gc.add_evaluation('s1', 18, 50)
    gc.set_attendance('s1', True)
    res = gc.calculate_final('s1')
    assert res['weighted_average'] == 15.0
    assert res['attendance_penalty'] == 0.0
    assert res['extra_points'] == 0.0
    assert res['final_grade'] == 15.0


def test_attendance_penalty_applied():
    gc = GradeCalculator(attendance_penalty=2.0)
    gc.add_evaluation('s2', 14, 100)
    gc.set_attendance('s2', False)
    res = gc.calculate_final('s2')
    assert res['weighted_average'] == 14.0
    assert res['attendance_penalty'] == 2.0
    assert res['final_grade'] == 12.0


def test_extra_points_when_all_years_true():
    gc = GradeCalculator(extra_points=1.0)
    gc.add_evaluation('s3', 16, 100)
    gc.set_attendance('s3', True)
    gc.set_all_years_teachers(True)
    res = gc.calculate_final('s3')
    assert res['extra_points'] == 1.0
    assert res['final_grade'] == 17.0


def test_max_evaluations_enforced():
    gc = GradeCalculator(max_evaluations=2)
    gc.add_evaluation('s4', 10, 50)
    gc.add_evaluation('s4', 12, 50)
    with pytest.raises(ValueError):
        gc.add_evaluation('s4', 14, 0)


def test_no_evaluations_error():
    gc = GradeCalculator()
    with pytest.raises(ValueError):
        gc.calculate_final('unknown')


def test_custom_extra_points_per_student():
    gc = GradeCalculator(extra_points=0.5)
    gc.add_evaluation('s5', 13, 100)
    gc.set_attendance('s5', True)
    gc.set_all_years_teachers(True)
    # override for student s5
    gc.set_extra_points_for_student('s5', 2.0)
    res = gc.calculate_final('s5')
    assert res['extra_points'] == 2.0
    assert res['final_grade'] == 15.0
