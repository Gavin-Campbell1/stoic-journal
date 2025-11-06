from datetime import date
from pathlib import Path

import pytest

from stoic_journal.app import JournalApp
from stoic_journal.storage import JournalStorage


def test_record_entry_and_summary(tmp_path: Path) -> None:
    db_path = tmp_path / "journal.sqlite3"
    app = JournalApp(db_path=db_path)

    app.record_entry(
        response="First note",
        quote="Stay calm",
        quote_source="Marcus Aurelius",
        entry_date=date(2025, 11, 4),
    )
    app.record_entry(
        response="Second note",
        quote="Practice virtue",
        quote_source="Epictetus",
        entry_date=date(2025, 11, 5),
    )

    entries = app.summary()
    assert [entry.entry_date.isoformat() for entry in entries] == [
        "2025-11-05",
        "2025-11-04",
    ]
    assert entries[0].quote_source == "Epictetus"


def test_record_entry_prevents_duplicates(tmp_path: Path) -> None:
    app = JournalApp(db_path=tmp_path / "journal.sqlite3")
    entry_date = date(2025, 11, 5)
    app.record_entry(response="Test", quote="Quote", entry_date=entry_date)

    with pytest.raises(ValueError):
        app.record_entry(response="Again", quote="Quote", entry_date=entry_date)


def test_allow_overwrite_updates_entry(tmp_path: Path) -> None:
    db_path = tmp_path / "journal.sqlite3"
    app = JournalApp(db_path=db_path)
    app.record_entry(response="Original", quote="Quote", entry_date=date(2025, 11, 5))

    app.record_entry(
        response="Updated",
        quote="Quote",
        entry_date=date(2025, 11, 5),
        allow_overwrite=True,
    )

    storage = JournalStorage(db_path)
    row = storage.get_entry_by_date("2025-11-05")
    assert row["response"] == "Updated"
