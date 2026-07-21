from dataclasses import dataclass


@dataclass(frozen=True)
class AddStudentCommand:
    student_id: str
    full_name: str
    age: int
    gender: str
    major: str
    gpa: float
