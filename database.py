from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent / "students.db"

STUDENTS = [
    ("22CS045", "Dhanushya", "Computer Science", 85, 72, 90, 78),
    ("22CS046", "Rahul", "Computer Science", 65, 70, 68, 72),
    ("22CS047", "Priya", "Information Technology", 92, 88, 95, 90),
    ("22CS048", "Arun", "Information Technology", 55, 60, 58, 62),
    ("22CS049", "Meena", "Computer Science", 78, 85, 80, 88),
]


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                python INTEGER NOT NULL CHECK (python BETWEEN 0 AND 100),
                database INTEGER NOT NULL CHECK (database BETWEEN 0 AND 100),
                ai INTEGER NOT NULL CHECK (ai BETWEEN 0 AND 100),
                web INTEGER NOT NULL CHECK (web BETWEEN 0 AND 100)
            )
            """
        )
        connection.executemany(
            """
            INSERT INTO students (
                student_id, name, department, python, database, ai, web
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(student_id) DO UPDATE SET
                name = excluded.name,
                department = excluded.department,
                python = excluded.python,
                database = excluded.database,
                ai = excluded.ai,
                web = excluded.web
            """,
            STUDENTS,
        )
        connection.commit()


def get_student(student_id: str) -> dict[str, Any] | None:
    normalized_id = student_id.strip().upper()
    with connect() as connection:
        row = connection.execute(
            """
            SELECT student_id, name, department, python, database, ai, web
            FROM students
            WHERE student_id = ?
            """,
            (normalized_id,),
        ).fetchone()
    return dict(row) if row else None


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized at: {DB_PATH}")
