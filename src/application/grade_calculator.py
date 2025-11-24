"""Grade calculator module implementing the exam requirements.

Provides a GradeCalculator class that:
- registers evaluations (grade + weight) per student
- registers whether the student reached minimum attendance
- supports an "all years teachers" flag to grant extra points
- calculates final grade and returns a detailed breakdown

Design notes:
- Grades are assumed on a numeric scale (e.g., 0-20). The implementation is
  agnostic on the exact scale; extra/penalty points are applied additively.
- Max evaluations per student is enforced (10).
- Methods are deterministic and fast (satisfying RNF03/RNF04).
"""
from typing import Dict, List, Optional


class Evaluation:
    def __init__(self, score: float, weight: float) -> None:
        self.score = float(score)
        self.weight = float(weight)


class GradeCalculator:
    """Calculator for final grades per student.

    Usage:
      gc = GradeCalculator(max_evaluations=10, attendance_penalty=1.0, extra_points=0.5)
      gc.add_evaluation(student_id, score, weight)
      gc.set_attendance(student_id, True/False)
      gc.set_all_years_teachers(True/False)
      result = gc.calculate_final(student_id)

    The returned `result` is a dict with keys:
      - weighted_average: float
      - attendance_penalty: float (points subtracted, 0 if none)
      - extra_points: float (points added, 0 if none)
      - final_grade: float (weighted_average - attendance_penalty + extra_points)
      - details: a dict with evaluations and weights for traceability
    """

    def __init__(self, *, max_evaluations: int = 10, attendance_penalty: float = 1.0, extra_points: float = 0.5):
        self.max_evaluations = int(max_evaluations)
        self.attendance_penalty = float(attendance_penalty)
        self.default_extra_points = float(extra_points)

        # Internal storage
        self._evaluations: Dict[str, List[Evaluation]] = {}
        self._attendance: Dict[str, bool] = {}
        # Global flag controlled by teachers (RF03)
        self.all_years_teachers: bool = False
        # Optionally allow per-student override of extra points
        self._extra_per_student: Dict[str, float] = {}

    def add_evaluation(self, student_id: str, score: float, weight: float) -> None:
        """Register an evaluation (score and its percentage weight) for a student.

        weight is expressed as a percentage (e.g., 40 for 40%). The method enforces
        the maximum number of evaluations per student (RNF01).
        """
        sid = str(student_id)
        if sid not in self._evaluations:
            self._evaluations[sid] = []
        if len(self._evaluations[sid]) >= self.max_evaluations:
            raise ValueError(f"Maximum number of evaluations ({self.max_evaluations}) exceeded for student {sid}")
        self._evaluations[sid].append(Evaluation(score=score, weight=weight))

    def set_attendance(self, student_id: str, has_reached_minimum: bool) -> None:
        """Record whether the student met the minimum attendance requirement."""
        self._attendance[str(student_id)] = bool(has_reached_minimum)

    def set_all_years_teachers(self, flag: bool) -> None:
        """Set the global policy that allows awarding extra points."""
        self.all_years_teachers = bool(flag)

    def set_extra_points_for_student(self, student_id: str, points: float) -> None:
        """Optionally set a custom extra-points value for a specific student."""
        self._extra_per_student[str(student_id)] = float(points)

    def _get_extra_points(self, student_id: str) -> float:
        if str(student_id) in self._extra_per_student:
            return self._extra_per_student[str(student_id)]
        return self.default_extra_points if self.all_years_teachers else 0.0

    def calculate_final(self, student_id: str) -> Dict:
        """Calculate the final grade for `student_id` and return a detailed breakdown.

        Raises ValueError when there are no evaluations registered or weights sum to 0.
        """
        sid = str(student_id)
        evals = self._evaluations.get(sid, [])
        if not evals:
            raise ValueError(f"No evaluations registered for student {sid}")

        total_weight = sum(ev.weight for ev in evals)
        if total_weight <= 0:
            raise ValueError("Total weight must be greater than 0")

        # Weighted average (normalize weights so they sum to 100 if they don't)
        weighted_sum = sum(ev.score * ev.weight for ev in evals)
        weighted_average = weighted_sum / total_weight

        # Attendance penalty
        attended = self._attendance.get(sid, True)
        attendance_penalty = 0.0 if attended else float(self.attendance_penalty)

        # Extra points
        extra_points = float(self._get_extra_points(sid))

        final_grade = weighted_average - attendance_penalty + extra_points

        # For determinism, round results to a sensible number of decimals
        weighted_average = round(weighted_average, 4)
        attendance_penalty = round(attendance_penalty, 4)
        extra_points = round(extra_points, 4)
        final_grade = round(final_grade, 4)

        # Build details for RF05
        details = {
            "evaluations": [{"score": ev.score, "weight": ev.weight} for ev in evals],
            "total_weight": total_weight,
            "weighted_sum": weighted_sum,
        }

        return {
            "weighted_average": weighted_average,
            "attendance_penalty": attendance_penalty,
            "extra_points": extra_points,
            "final_grade": final_grade,
            "details": details,
        }
