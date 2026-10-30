#!/usr/bin/env python3
"""Translate repository metadata and analysis notes into English."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from translations import (
    EDITION_NOTE_TRANSLATIONS,
    INFERENCE_LIMIT_TRANSLATIONS,
    LABEL_TRANSLATIONS,
    LOCATOR_TRANSLATIONS,
    PUBLISHER_TRANSLATIONS,
    REGULATORY_FUNCTION_TRANSLATIONS,
    REGULATORY_OBSERVATION_TRANSLATIONS,
    REPORT_TITLE_TRANSLATIONS,
    RESULT_COMPONENT_TRANSLATIONS,
    REVISION_NOTE_TRANSLATIONS,
    STATUS_TRANSLATIONS,
)


ROOT = Path(__file__).resolve().parents[1]


def translate_csv(
    relative_path: str,
    column_maps: dict[str, dict[str, str]],
    fieldnames: list[str] | None = None,
) -> None:
    path = ROOT / relative_path
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = list(fieldnames or reader.fieldnames or [])
        rows = list(reader)

    for row in rows:
        for column, translations in column_maps.items():
            value = row.get(column, "")
            if value in translations:
                row[column] = translations[value]

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def translate_editions() -> None:
    path = ROOT / "data" / "editions.csv"
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    columns = [
        "edition_id",
        "publication_year",
        "publisher",
        "publisher_original",
        "report_title",
        "report_title_original",
        "source_url",
        "source_catalog_url",
        "notes",
    ]
    for row in rows:
        publisher_original = row.get("publisher_original") or row["publisher"]
        title_original = row.get("report_title_original") or row["report_title"]
        row["publisher_original"] = publisher_original
        row["publisher"] = PUBLISHER_TRANSLATIONS.get(
            publisher_original, publisher_original
        )
        row["report_title_original"] = title_original
        row["report_title"] = REPORT_TITLE_TRANSLATIONS.get(
            title_original, title_original
        )
        row["notes"] = EDITION_NOTE_TRANSLATIONS.get(row.get("notes", ""), row.get("notes", ""))

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def translate_results_json() -> None:
    path = ROOT / "data" / "derived" / "results.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    def walk(value: Any, key: str | None = None) -> Any:
        if isinstance(value, dict):
            translated = {}
            for child_key, child_value in value.items():
                new_key = RESULT_COMPONENT_TRANSLATIONS.get(child_key, child_key)
                translated[new_key] = walk(child_value, child_key)
            return translated
        if isinstance(value, list):
            return [walk(item, key) for item in value]
        if isinstance(value, str):
            if key == "locator":
                return LOCATOR_TRANSLATIONS.get(value, value)
            if key == "status":
                return STATUS_TRANSLATIONS.get(value, value)
        return value

    path.write_text(
        json.dumps(walk(data), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def translate_data() -> None:
    """Translate maintained CSV/JSON text fields, preserving original source fields."""
    translate_editions()
    translate_csv(
        "data/derived/annual_comparisons.csv",
        {"label": LABEL_TRANSLATIONS, "locator": LOCATOR_TRANSLATIONS},
    )
    translate_csv(
        "data/derived/ben2025_indicators.csv",
        {"label": LABEL_TRANSLATIONS, "locator": LOCATOR_TRANSLATIONS},
    )
    translate_csv(
        "data/derived/historical_latest_series.csv",
        {"locator": LOCATOR_TRANSLATIONS, "status": STATUS_TRANSLATIONS},
    )
    translate_csv(
        "data/derived/revision_audit.csv",
        {
            "label": LABEL_TRANSLATIONS,
            "source_from": LOCATOR_TRANSLATIONS,
            "source_to": LOCATOR_TRANSLATIONS,
            "note": REVISION_NOTE_TRANSLATIONS,
        },
    )
    translate_csv(
        "data/observations/edition_observations.csv",
        {
            "label": LABEL_TRANSLATIONS,
            "locator": LOCATOR_TRANSLATIONS,
            "status": STATUS_TRANSLATIONS,
        },
    )
    translate_csv(
        "data/context/regulatory_evidence.csv",
        {
            "function": REGULATORY_FUNCTION_TRANSLATIONS,
            "locator": LOCATOR_TRANSLATIONS,
            "observation": REGULATORY_OBSERVATION_TRANSLATIONS,
            "inference_limit": INFERENCE_LIMIT_TRANSLATIONS,
        },
    )
    translate_results_json()


if __name__ == "__main__":
    translate_data()
