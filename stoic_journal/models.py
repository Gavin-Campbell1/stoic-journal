"""Core data models for the Stoic Journal project."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass(frozen=True)
class Quote:
    """Represents a Stoic quote used as a journaling prompt."""

    text: str
    author: Optional[str] = None
    fetched_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class JournalEntry:
    """Normalized representation of a stored journal entry."""

    entry_date: date
    prompt: str
    response: str
    quote: str
    quote_source: Optional[str] = None
    created_at: datetime | None = None
