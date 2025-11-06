"""SQLite storage helpers for the Stoic Journal app."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Iterable, Optional


SCHEMA = """
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_date TEXT NOT NULL UNIQUE,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL,
    quote TEXT NOT NULL,
    quote_source TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


class JournalStorage:
    """Lightweight wrapper around SQLite for storing journal entries."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @contextmanager
    def _connection(self) -> Generator[sqlite3.Connection, None, None]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _initialize(self) -> None:
        with self._connection() as conn:
            conn.executescript(SCHEMA)

    def add_entry(
        self,
        entry_date: str,
        prompt: str,
        response: str,
        quote: str,
        quote_source: Optional[str] = None,
        *,
        overwrite: bool = False,
    ) -> int:
        with self._connection() as conn:
            statement = (
                """
                INSERT OR REPLACE INTO entries (entry_date, prompt, response, quote, quote_source)
                VALUES (?, ?, ?, ?, ?)
                """
                if overwrite
                else """
                INSERT INTO entries (entry_date, prompt, response, quote, quote_source)
                VALUES (?, ?, ?, ?, ?)
                """
            )
            cursor = conn.execute(
                statement,
                (entry_date, prompt, response, quote, quote_source),
            )
            return int(cursor.lastrowid)

    def get_entry_by_date(self, entry_date: str) -> Optional[sqlite3.Row]:
        with self._connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM entries WHERE entry_date = ?",
                (entry_date,),
            )
            return cursor.fetchone()

    def list_entries(self, limit: Optional[int] = None) -> Iterable[sqlite3.Row]:
        query = "SELECT * FROM entries ORDER BY entry_date DESC"
        params: tuple = ()
        if limit is not None:
            query += " LIMIT ?"
            params = (limit,)

        with self._connection() as conn:
            cursor = conn.execute(query, params)
            yield from cursor.fetchall()
