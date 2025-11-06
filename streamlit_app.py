"""Streamlit interface for the Stoic Journal project."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import streamlit as st

from stoic_journal import JournalApp
from stoic_journal.models import Quote
from stoic_journal.quotes import fetch_quote

DEFAULT_DB_PATH = Path.home() / ".stoic_journal" / "journal.sqlite3"
RECENT_LIMIT = 5


@st.cache_data(ttl=3600)
def load_quote() -> Quote:
    """Cache quote retrieval so we do not hit the API repeatedly."""
    return fetch_quote()


def get_app(db_path: Path) -> JournalApp:
    """Memoize the JournalApp instance per database path."""
    cache_key = "journal_app"
    if cache_key not in st.session_state or st.session_state.get("db_path") != str(db_path):
        st.session_state[cache_key] = JournalApp(db_path=db_path)
        st.session_state["db_path"] = str(db_path)
    return st.session_state[cache_key]


def main() -> None:
    st.set_page_config(page_title="Stoic Journal", page_icon=":notebook_with_decorative_cover:")
    st.title("Stoic Journal")

    st.sidebar.header("Settings")
    db_path_input = st.sidebar.text_input(
        "Database location",
        value=str(DEFAULT_DB_PATH),
        help="Journal entries are saved in this SQLite file.",
    )
    db_path = Path(db_path_input).expanduser()
    app = get_app(db_path)

    today = date.today()
    existing = app.storage.get_entry_by_date(today.isoformat())

    st.subheader("Today's Reflection")
    st.write(app.prompt)

    if existing:
        quote_text = existing["quote"]
        quote_author = existing["quote_source"]
        default_response = existing["response"]
        st.info(f"Entry already saved for {today.isoformat()}. Editing will overwrite it.")
    else:
        quote = load_quote()
        quote_text = quote.text
        quote_author = quote.author
        default_response = ""

    st.markdown("> **Stoic thought for today**")
    st.markdown(f"> {quote_text}")
    if quote_author:
        st.markdown(f"_— {quote_author}_")

    with st.form("journal_form"):
        response = st.text_area("Your reflection", value=default_response, height=200)
        allow_overwrite = st.checkbox("Overwrite existing entry", value=bool(existing))
        submitted = st.form_submit_button("Save Entry")

    if submitted:
        if not response.strip():
            st.warning("Write a reflection before saving.")
        else:
            try:
                app.record_entry(
                    response=response,
                    quote=quote_text,
                    quote_source=quote_author,
                    entry_date=today,
                    allow_overwrite=allow_overwrite,
                )
            except ValueError as exc:
                st.error(str(exc))
            else:
                st.success(f"Entry saved for {today.isoformat()}.")

    st.divider()
    st.subheader("Recent entries")
    entries = app.summary(limit=RECENT_LIMIT)
    if not entries:
        st.write("No entries yet. Your history will appear here after you save.")
    else:
        for entry in entries:
            with st.expander(entry.entry_date.isoformat(), expanded=False):
                st.markdown(f"**Quote:** {entry.quote}")
                if entry.quote_source:
                    st.markdown(f"_— {entry.quote_source}_")
                st.markdown("**Reflection:**")
                st.write(entry.response)


if __name__ == "__main__":
    main()
