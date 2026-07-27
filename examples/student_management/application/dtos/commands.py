# Clean Architecture - Application DTOs (Commands)
from dataclasses import dataclass


@dataclass(frozen=True)
class AddStudentCommand:
    student_id: str
    full_name: str
    age: int
    gender: str
    major: str
    gpa: float


@dataclass(frozen=True)
class UpdateStudentCommand:
    id: str
    student_id: str
    full_name: str
    age: int
    gender: str
    major: str
    gpa: float


@dataclass(frozen=True)
class DeleteStudentCommand:
    id: str


@dataclass(frozen=True)
class GenerateReportCommand: ...
