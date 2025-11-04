"""Command line interface for the Stoic Journal app."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path
from textwrap import fill

from .journal import JournalApp
from .quotes import Quote, fetch_quote

DEFAULT_DB_PATH = Path.home() / ".stoic_journal" / "journal.sqlite3"
WRAP_WIDTH = 80


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stoic-journal",
        description="Capture a quick morning reflection alongside a Stoic quote.",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=DEFAULT_DB_PATH,
        help=f"Location of the SQLite database (default: {DEFAULT_DB_PATH})",
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = False

    write_parser = subparsers.add_parser("write", help="Log today's journal entry.")
    write_parser.add_argument(
        "--date",
        type=date.fromisoformat,
        default=date.today().isoformat(),
        help="ISO formatted date for the entry (default: today).",
    )
    write_parser.add_argument(
        "--force",
        action="store_true",
        help="Allow overwriting an existing entry for the provided date.",
    )

    list_parser = subparsers.add_parser("list", help="Show recent entries.")
    list_parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of entries to display (default: 5).",
    )

    return parser


def render_quote(quote: Quote) -> None:
    print("\nToday's Stoic quote:\n")
    print(fill(f"\"{quote.text}\"", width=WRAP_WIDTH))
    if quote.author:
        print(f"\n- {quote.author}")
    print()


def capture_response() -> str:
    print(
        "\nTake a couple of minutes to jot down your thoughts. "
        "Press Enter twice when you are finished.\n"
    )
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line.strip():
            break
        lines.append(line.rstrip())

    return "\n".join(lines).strip()


def handle_write(app: JournalApp, entry_date: date, allow_overwrite: bool) -> int:
    if not allow_overwrite and app.has_entry_for(entry_date):
        print(f"An entry already exists for {entry_date.isoformat()}. Use --force to overwrite.")
        return 1

    quote = fetch_quote()
    render_quote(quote)
    print(fill(app.prompt, width=WRAP_WIDTH))

    response = capture_response()
    if not response:
        print("No response captured. Entry skipped.")
        return 2

    app.record_entry(
        response=response,
        quote=quote.text,
        quote_source=quote.author,
        entry_date=entry_date,
        allow_overwrite=allow_overwrite,
    )
    print(f"\nEntry saved for {entry_date.isoformat()}.\n")
    return 0


def handle_list(app: JournalApp, limit: int) -> int:
    entries = app.summary(limit=limit)
    if not entries:
        print("No journal entries found yet.")
        return 0

    for entry in entries:
        print(f"{entry.entry_date.isoformat()}:")
        print(fill(f"Quote: {entry.quote}", width=WRAP_WIDTH))
        if entry.quote_source:
            print(f"Source: {entry.quote_source}")
        print(fill(f"Reflection: {entry.response}", width=WRAP_WIDTH))
        print("-" * 40)
    return 0


def run(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    db_path: Path = args.db_path.expanduser()
    app = JournalApp(db_path=db_path)

    command = args.command or "write"
    if command == "write":
        raw_date = getattr(args, "date", date.today())
        entry_date = raw_date if isinstance(raw_date, date) else date.fromisoformat(raw_date)
        force = bool(getattr(args, "force", False))
        return handle_write(app, entry_date=entry_date, allow_overwrite=force)
    if command == "list":
        limit = int(getattr(args, "limit", 5))
        return handle_list(app, limit=limit)

    parser.print_help()
    return 0


def main() -> None:
    sys.exit(run())


if __name__ == "__main__":
    main()
