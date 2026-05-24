#!/usr/bin/env python3
"""Refresh public research metrics from SINTA.

The website keeps readable fallback numbers in index.html. This script updates
data/metrics.json so GitHub Pages can refresh the displayed metrics without
editing the page markup.
"""

from __future__ import annotations

import json
import re
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen


SINTA_URL = "https://sinta.kemdiktisaintek.go.id/authors/profile/6690720"
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "metrics.json"


class TextOnlyParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if text:
            self.parts.append(text)


def read_page_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", errors="ignore")

    parser = TextOnlyParser()
    parser.feed(html)
    return " ".join(parser.parts)


def parse_h_indexes(text: str) -> dict[str, int]:
    normalized = re.sub(r"\s+", " ", text)
    match = re.search(r"H-Index\s+(\d+)\s+(\d+)\s+(\d+)", normalized, flags=re.I)
    if not match:
        raise RuntimeError("Could not find Scopus, Google Scholar, and WoS H-index values.")

    scopus, scholar, wos = (int(value) for value in match.groups())
    return {
        "scopusHIndex": scopus,
        "scholarHIndex": scholar,
        "wosHIndex": wos,
    }


def main() -> None:
    metrics = parse_h_indexes(read_page_text(SINTA_URL))
    metrics.update(
        {
            "sourceName": "SINTA",
            "sourceUrl": SINTA_URL,
            "lastChecked": date.today().isoformat(),
        }
    )
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
