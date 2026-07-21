from dataclasses import dataclass


@dataclass(frozen=True)
class GetStudentQuery:
    id: str  # Unique system ID (UUID)
