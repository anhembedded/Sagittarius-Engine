from dataclasses import dataclass


@dataclass(frozen=True)
class SearchStudentsQuery:
    term: str  # Search term for filtering by name or student ID
