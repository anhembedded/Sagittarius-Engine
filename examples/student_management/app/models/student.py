# Student Domain Model
from dataclasses import dataclass


class StudentException(Exception):
    ...


class EmptyNameError(StudentException):
    ...


class InvalidAgeError(StudentException):
    ...


class InvalidGPAError(StudentException):
    ...


class DuplicateStudentIDError(StudentException):
    ...


class StudentNotFoundError(StudentException):
    ...


@dataclass
class Student:
    id: str
    student_id: str
    full_name: str
    age: int
    gender: str
    major: str
    gpa: float

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.full_name or not self.full_name.strip():
            raise EmptyNameError("Name cannot be empty.")
        if self.age <= 0 or self.age > 150:
            raise InvalidAgeError("Age must be between 1 and 150.")
        if self.gpa < 0.0 or self.gpa > 4.0:
            raise InvalidGPAError("GPA must be between 0.0 and 4.0.")
