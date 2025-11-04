# Stoic Journal
Capture a quick morning reflection alongside a daily Stoic quote.

## Quick start
1. Ensure Python 3.11+ is installed.
2. Optionally create and activate a virtual environment.
3. Run the app:
   ```bash
   python -m stoic_journal
   ```
   or show five recent entries:
   ```bash
   python -m stoic_journal list --limit 5
   ```

The first run creates a SQLite database at `~/.stoic_journal/journal.sqlite3`. Use `--db-path` to override the location.

## How it works
- Fetches a daily quote from public Stoic quote APIs with a built-in offline fallback.
- Prompts you with a short reflection question and collects a multi-line response.
- Stores the entry date, quote, and reflection in SQLite so you can review past notes.

## Automating the morning prompt
- **Windows Task Scheduler:** create a basic task that runs `python -m stoic_journal` at your preferred time. Choose "Start a program" and point to your Python interpreter; pass `-m stoic_journal` as the argument.
- **macOS/Linux cron:** add a crontab entry such as `0 7 * * * /usr/bin/env python -m stoic_journal` to trigger it daily at 7 a.m.

## Extending
- Adjust the prompt text by editing `DEFAULT_PROMPT` in `stoic_journal/journal.py`.
- Add more offline quotes in `stoic_journal/quotes.py`'s `FALLBACK_QUOTES` list.
- Build additional commands on top of the `JournalApp` class for summaries or exports.
