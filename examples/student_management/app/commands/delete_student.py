from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteStudentCommand:
    id: str  # Unique system ID (UUID)
