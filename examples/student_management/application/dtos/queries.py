# Clean Architecture - Application DTOs (Queries)
from dataclasses import dataclass


@dataclass(frozen=True)
class ListStudentsQuery:
    ...


@dataclass(frozen=True)
class SearchStudentsQuery:
    term: str


@dataclass(frozen=True)
class GetStudentQuery:
    id: str
