from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateStudentCommand:
    id: str  # Unique system ID (UUID)
    student_id: str
    full_name: str
    age: int
    gender: str
    major: str
    gpa: float
