import sqlite3
from datetime import date
from pathlib import Path
from typing import Any


def connect(db_path: str) -> sqlite3.Connection:
    parent = Path(db_path).expanduser().resolve().parent
    parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS turns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        session_id TEXT NOT NULL,
        day TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('user','assistant')),
        content TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_turns_session_day ON turns(session_id, day, id)")
    conn.commit()
    return conn


def add_turn(db_path: str, student_id: str, session_id: str, role: str, content: str) -> None:
    with connect(db_path) as conn:
        conn.execute("INSERT INTO turns(student_id, session_id, day, role, content) VALUES(?,?,?,?,?)",
                     (student_id, session_id, date.today().isoformat(), role, content))
        conn.commit()


def get_today_history(db_path: str, student_id: str, session_id: str, limit: int = 12) -> list[dict[str, Any]]:
    with connect(db_path) as conn:
        rows = conn.execute(
            "SELECT role, content, created_at FROM turns WHERE student_id=? AND session_id=? AND day=? ORDER BY id DESC LIMIT ?",
            (student_id, session_id, date.today().isoformat(), limit)
        ).fetchall()
    return [dict(row) for row in reversed(rows)]
