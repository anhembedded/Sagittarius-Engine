from dataclasses import dataclass

@dataclass
class CSVRow:
    id: str
    name: str
    score: int
