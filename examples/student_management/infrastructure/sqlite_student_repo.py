# Clean Architecture - Infrastructure Adapter (SQLite Repository)
import sqlite3
from contextlib import contextmanager
from typing import Sequence, Iterator, Optional

from sagittarius_engine.interfaces import IConfig
from examples.student_management.application.contracts.student_repository import IStudentRepository
from examples.student_management.domain.student import Student


class SqliteStudentRepository(IStudentRepository):
    """
    SQLite implementation of IStudentRepository.
    """

    def __init__(self, config: IConfig) -> None:
        self.db_path = config.get("database.path", "students.db")
        self._init_db()

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    id TEXT PRIMARY KEY,
                    student_id TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    major TEXT NOT NULL,
                    gpa REAL NOT NULL
                )
                """
            )

    def _row_to_student(self, row: sqlite3.Row) -> Student:
        return Student(
            id=row["id"],
            student_id=row["student_id"],
            full_name=row["full_name"],
            age=row["age"],
            gender=row["gender"],
            major=row["major"],
            gpa=row["gpa"],
        )

    def add(self, student: Student) -> Student:
        with self._connection() as conn:
            conn.execute(
                """
                INSERT INTO students (id, student_id, full_name, age, gender, major, gpa)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    student.id,
                    student.student_id,
                    student.full_name,
                    student.age,
                    student.gender,
                    student.major,
                    student.gpa,
                ),
            )
        return student

    def update(self, student: Student) -> Student:
        with self._connection() as conn:
            conn.execute(
                """
                UPDATE students
                SET student_id = ?, full_name = ?, age = ?, gender = ?, major = ?, gpa = ?
                WHERE id = ?
                """,
                (
                    student.student_id,
                    student.full_name,
                    student.age,
                    student.gender,
                    student.major,
                    student.gpa,
                    student.id,
                ),
            )
        return student

    def delete(self, uuid: str) -> None:
        with self._connection() as conn:
            conn.execute(
                "DELETE FROM students WHERE id = ? OR student_id = ?",
                (uuid, uuid),
            )

    def get_by_id(self, uuid: str) -> Optional[Student]:
        with self._connection() as conn:
            cursor = conn.execute(
                "SELECT id, student_id, full_name, age, gender, major, gpa FROM students WHERE id = ?",
                (uuid,),
            )
            row = cursor.fetchone()
            return self._row_to_student(row) if row else None

    def get_by_student_id(self, student_id: str) -> Optional[Student]:
        with self._connection() as conn:
            cursor = conn.execute(
                "SELECT id, student_id, full_name, age, gender, major, gpa FROM students WHERE student_id = ?",
                (student_id,),
            )
            row = cursor.fetchone()
            return self._row_to_student(row) if row else None

    def get_all(self) -> Sequence[Student]:
        with self._connection() as conn:
            cursor = conn.execute(
                "SELECT id, student_id, full_name, age, gender, major, gpa FROM students"
            )
            return [self._row_to_student(row) for row in cursor.fetchall()]

    def search(self, term: str) -> Sequence[Student]:
        with self._connection() as conn:
            cursor = conn.execute(
                "SELECT id, student_id, full_name, age, gender, major, gpa FROM students WHERE full_name LIKE ? OR student_id LIKE ?",
                (f"%{term}%", f"%{term}%"),
            )
            return [self._row_to_student(row) for row in cursor.fetchall()]
