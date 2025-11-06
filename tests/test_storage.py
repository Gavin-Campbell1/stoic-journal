from datetime import date
from pathlib import Path

from stoic_journal.storage import JournalStorage


def test_add_and_fetch_entry(tmp_path: Path) -> None:
    db_path = tmp_path / "journal.sqlite3"
    storage = JournalStorage(db_path)

    storage.add_entry(
        entry_date="2025-11-05",
        prompt="Prompt",
        response="Response",
        quote="Quote",
        quote_source="Source",
    )

    row = storage.get_entry_by_date("2025-11-05")
    assert row is not None
    assert row["response"] == "Response"
    assert row["quote_source"] == "Source"


def test_list_entries_orders_desc(tmp_path: Path) -> None:
    storage = JournalStorage(tmp_path / "journal.sqlite3")
    storage.add_entry(
        entry_date="2025-11-04",
        prompt="Prompt A",
        response="Response A",
        quote="Quote A",
    )
    storage.add_entry(
        entry_date="2025-11-05",
        prompt="Prompt B",
        response="Response B",
        quote="Quote B",
    )

    rows = list(storage.list_entries())
    assert [row["entry_date"] for row in rows] == ["2025-11-05", "2025-11-04"]
