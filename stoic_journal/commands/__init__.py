"""Typer-powered CLI commands for the Stoic Journal project."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path
from textwrap import fill
from typing import Optional

import typer

from ..app import JournalApp
from ..models import Quote
from ..quotes import fetch_quote

DEFAULT_DB_PATH = Path.home() / ".stoic_journal" / "journal.sqlite3"
WRAP_WIDTH = 80

cli = typer.Typer(help="Capture reflections alongside daily Stoic quotes.")


def _load_app(db_path: Path) -> JournalApp:
    return JournalApp(db_path=db_path.expanduser())


def _render_quote(quote: Quote) -> None:
    typer.echo("\nToday's Stoic quote:\n")
    typer.echo(fill(f"\"{quote.text}\"", width=WRAP_WIDTH))
    if quote.author:
        typer.echo(f"\n- {quote.author}")
    typer.echo()


def _capture_response() -> str:
    typer.echo(
        "\nTake a couple of minutes to jot down your thoughts. "
        "Press Enter twice when you are finished.\n"
    )
    lines: list[str] = []
    while True:
        try:
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            return ""
        if not line:
            break
        if not line.strip():
            break
        lines.append(line.rstrip())

    return "\n".join(lines).strip()


def write_entry(
    db_path: Path,
    entry_date: Optional[date] = None,
    force: bool = False,
) -> int:
    """Core implementation shared by CLI and programmatic entry creation."""
    today = entry_date or date.today()
    app = _load_app(db_path)

    if not force and app.has_entry_for(today):
        typer.echo(
            f"An entry already exists for {today.isoformat()}. Use --force to overwrite."
        )
        return 1

    quote = fetch_quote()
    _render_quote(quote)
    typer.echo(fill(app.prompt, width=WRAP_WIDTH))

    response = _capture_response()
    if not response:
        typer.echo("No response captured. Entry skipped.")
        return 2

    app.record_entry(
        response=response,
        quote=quote.text,
        quote_source=quote.author,
        entry_date=today,
        allow_overwrite=force,
    )
    typer.echo(f"\nEntry saved for {today.isoformat()}.\n")
    return 0


def list_recent_entries(db_path: Path, limit: int = 5) -> int:
    """Shared logic for listing entries."""
    app = _load_app(db_path)
    entries = app.summary(limit=limit)
    if not entries:
        typer.echo("No journal entries found yet.")
        return 0

    for entry in entries:
        typer.echo(f"{entry.entry_date.isoformat()}:")
        typer.echo(fill(f"Quote: {entry.quote}", width=WRAP_WIDTH))
        if entry.quote_source:
            typer.echo(f"Source: {entry.quote_source}")
        typer.echo(fill(f"Reflection: {entry.response}", width=WRAP_WIDTH))
        typer.echo("-" * 40)
    return 0


@cli.command()
def write(
    db_path: Path = typer.Option(
        DEFAULT_DB_PATH,
        "--db-path",
        help=f"Location of the SQLite database (default: {DEFAULT_DB_PATH})",
    ),
    entry_date: Optional[date] = typer.Option(
        None,
        "--date",
        formats=["%Y-%m-%d"],
        help="ISO formatted date for the entry (default: today).",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Allow overwriting an existing entry for the provided date.",
    ),
) -> None:
    """Log today's journal entry."""
    raise typer.Exit(code=write_entry(db_path=db_path, entry_date=entry_date, force=force))


@cli.command("list")
def list_entries(
    db_path: Path = typer.Option(
        DEFAULT_DB_PATH,
        "--db-path",
        help=f"Location of the SQLite database (default: {DEFAULT_DB_PATH})",
    ),
    limit: int = typer.Option(
        5,
        "--limit",
        help="Number of entries to display.",
    ),
) -> None:
    """Display recent journal entries."""
    raise typer.Exit(code=list_recent_entries(db_path=db_path, limit=limit))
