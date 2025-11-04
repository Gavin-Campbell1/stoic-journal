"""Fetches Stoic quotes from the web with an offline fallback."""

from __future__ import annotations

import json
import random
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Optional


API_URLS = [
    "https://stoic-quotes.com/api/quote",
    "https://stoicquotesapi.com/v1/api/quotes/random",
]

FALLBACK_QUOTES = [
    (
        "You have power over your mind-not outside events. Realize this, and you will find strength.",
        "Marcus Aurelius",
    ),
    ("We suffer more often in imagination than in reality.", "Seneca"),
    ("First say to yourself what you would be; and then do what you have to do.", "Epictetus"),
    (
        "If it is not right, do not do it, if it is not true, do not say it.",
        "Marcus Aurelius",
    ),
    ("No man is free who is not master of himself.", "Epictetus"),
]


@dataclass(frozen=True)
class Quote:
    text: str
    author: Optional[str] = None


def _parse_payload(payload: dict) -> Optional[Quote]:
    text = payload.get("text") or payload.get("body")
    author = payload.get("author") or payload.get("title") or payload.get("source")

    if not text:
        return None

    return Quote(text=text.strip(), author=author.strip() if author else None)


def fetch_quote(timeout: float = 5.0) -> Quote:
    """Attempt to fetch a quote from public APIs, falling back to local data."""
    for url in API_URLS:
        try:
            with urllib.request.urlopen(url, timeout=timeout) as response:
                payload = json.load(response)
                if isinstance(payload, list) and payload:
                    quote = _parse_payload(payload[0])
                else:
                    quote = _parse_payload(payload)
                if quote:
                    return quote
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            continue

    text, author = random.choice(FALLBACK_QUOTES)
    return Quote(text=text, author=author)
