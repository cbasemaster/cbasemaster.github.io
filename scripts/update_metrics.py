#!/usr/bin/env python3
"""Refresh public research metrics from Google Scholar and SINTA.

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
GOOGLE_SCHOLAR_URL = "https://scholar.google.com/citations?user=NxSJRlYAAAAJ&hl=en"
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "metrics.json"


class TextOnlyParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if text:
            self.parts.append(text)


def read_page_html(url: str) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="ignore")


def read_page_text(url: str) -> str:
    html = read_page_html(url)

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


def parse_google_scholar_metrics(html: str) -> dict[str, int]:
    values = re.findall(r'<td class="gsc_rsb_std">([0-9.,]+)</td>', html)
    if len(values) < 6:
        raise RuntimeError("Could not find Google Scholar citation metrics.")

    parsed = [int(re.sub(r"\D", "", value)) for value in values[:6]]
    return {
        "scholarCitations": parsed[0],
        "scholarHIndex": parsed[2],
        "scholarI10Index": parsed[4],
    }


def main() -> None:
    metrics: dict[str, object] = {}
    if OUTPUT_PATH.exists():
        try:
            metrics = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            metrics = {}

    refreshed = False
    try:
        sinta_metrics = parse_h_indexes(read_page_text(SINTA_URL))
        metrics.setdefault("scopusHIndex", sinta_metrics["scopusHIndex"])
        metrics.setdefault("scholarHIndex", sinta_metrics["scholarHIndex"])
        metrics["wosHIndex"] = sinta_metrics["wosHIndex"]
        refreshed = True
    except (OSError, RuntimeError):
        pass

    try:
        metrics.update(parse_google_scholar_metrics(read_page_html(GOOGLE_SCHOLAR_URL)))
        metrics["scholarLastChecked"] = date.today().isoformat()
        refreshed = True
    except (OSError, RuntimeError):
        pass

    metrics.update(
        {
            "sourceName": "Google Scholar / Scopus (Elsevier) / SINTA",
            "sourceUrl": GOOGLE_SCHOLAR_URL,
        }
    )
    if refreshed:
        metrics["lastChecked"] = date.today().isoformat()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(metrics, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
