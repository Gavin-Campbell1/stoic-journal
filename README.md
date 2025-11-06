# Stoic Journal
Capture a quick morning reflection alongside a daily Stoic quote.

## Quick start
1. Ensure Python 3.11+ is installed.
2. Optionally create and activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Capture today's reflection:
   ```bash
   python -m stoic_journal
   ```
   Show the five most recent entries:
   ```bash
   python -m stoic_journal list --limit 5
   ```
5. Prefer a UI? Launch the Streamlit web app:
   ```bash
   streamlit run streamlit_app.py
   ```

The first run creates a SQLite database at `~/.stoic_journal/journal.sqlite3`. Use `--db-path` to override the location.

## How it works
- Fetches a daily quote from public Stoic quote APIs with a built-in offline fallback.
- Prompts you with a short reflection question and collects a multi-line response.
- Stores the entry date, quote, and reflection in SQLite so you can review past notes.

## Automating the morning prompt
- **Windows Task Scheduler:** create a basic task that runs `python -m stoic_journal` at your preferred time. Choose "Start a program" and point to your Python interpreter; pass `-m stoic_journal` as the argument.
- **UPDATE ON AUTOMATION** I have scheduled a daily task that runs at 0700 every day.

## Tests & quality gates
Run the checks recommended in the learning path:
```bash
pytest
# optional extras once configured:
# black stoic_journal tests
# flake8 stoic_journal tests
# mypy stoic_journal
```

## Extending
- Adjust the prompt text by editing `DEFAULT_PROMPT` in `stoic_journal/app.py`.
- Modify persistence by evolving `stoic_journal/storage.py` (migrations, new tables, etc.).
- Add more offline quotes in `stoic_journal/quotes.py`'s `FALLBACK_QUOTES` list.
- Build additional commands in `stoic_journal/commands/` to support exports, streaks, or analytics.
