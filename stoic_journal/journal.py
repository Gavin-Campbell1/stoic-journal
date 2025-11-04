"""High level journaling workflow helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional

from .db import JournalDatabase


DEFAULT_PROMPT = (
    "Take a deep breath, consider today's Stoic teaching, and jot down a quick reflection. "
    "What stands out to you and how will you carry it forward today?"
)


@dataclass(frozen=True)
class JournalEntry:
    entry_date: date
    prompt: str
    response: str
    quote: str
    quote_source: Optional[str] = None


class JournalApp:
    """Coordinates journaling prompts with database persistence."""

    def __init__(self, db_path: Path, prompt: str = DEFAULT_PROMPT) -> None:
        self.db = JournalDatabase(db_path)
        self.prompt = prompt

    def has_entry_for(self, entry_date: date) -> bool:
        return self.db.get_entry_by_date(entry_date.isoformat()) is not None

    def record_entry(
        self,
        response: str,
        quote: str,
        quote_source: Optional[str] = None,
        entry_date: Optional[date] = None,
        prompt: Optional[str] = None,
        allow_overwrite: bool = False,
    ) -> int:
        entry_date = entry_date or date.today()
        iso_date = entry_date.isoformat()
        prompt_text = prompt or self.prompt

        if not allow_overwrite and self.has_entry_for(entry_date):
            raise ValueError(f"An entry already exists for {iso_date}.")

        return self.db.add_entry(
            entry_date=iso_date,
            prompt=prompt_text,
            response=response.strip(),
            quote=quote.strip(),
            quote_source=quote_source.strip() if quote_source else None,
        )

    def summary(self, limit: Optional[int] = None) -> list[JournalEntry]:
        entries = []
        for row in self.db.list_entries(limit=limit):
            entries.append(
                JournalEntry(
                    entry_date=date.fromisoformat(row["entry_date"]),
                    prompt=row["prompt"],
                    response=row["response"],
                    quote=row["quote"],
                    quote_source=row["quote_source"],
                )
            )
        return entries
