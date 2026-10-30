#!/usr/bin/env python3
"""Build the portable SQLite database from the repository's CSV files."""

from __future__ import annotations

import csv
import json
import sqlite3
from decimal import Decimal
from pathlib import Path
from typing import Any

from extract_comparisons import extract_rows


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "db" / "ben_electricidad.sqlite"


def text(value: Any) -> str | None:
    if value is None:
        return None
    result = str(value).strip()
    return result if result else None


def integer(value: Any) -> int | None:
    value = text(value)
    return int(value) if value is not None else None


def number(value: Any) -> float | None:
    value = text(value)
    return float(Decimal(value)) if value is not None else None


def edition_id(value: Any) -> str | None:
    value = text(value)
    if value is None:
        return None
    if value.upper().startswith("BEN"):
        return value.upper()
    return f"BEN{int(value)}"


def read_csv(relative_path: str) -> list[dict[str, str]]:
    with (ROOT / relative_path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_published_comparisons() -> None:
    rows = extract_rows()
    output = ROOT / "data" / "source" / "published_comparisons.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def insert_many(
    connection: sqlite3.Connection, sql: str, rows: list[tuple[Any, ...]]
) -> None:
    connection.executemany(sql, rows)


def comparison_result_rows(results: dict[str, Any]) -> list[tuple[Any, ...]]:
    rows = []
    for comparison, item in results.get("comparisons", {}).items():
        rows.append(
            (
                comparison,
                integer(item.get("start_year")),
                integer(item.get("end_year")),
                number(item.get("export_change_gwh")),
                number(item.get("export_contraction_gwh")),
                number(item.get("national_market_growth_gwh")),
                number(item.get("national_market_contribution_percent")),
                json.dumps(item.get("balance_change_percent", {}), ensure_ascii=False),
                json.dumps(item.get("balance_residual_gwh", {}), ensure_ascii=False),
                json.dumps(item.get("demand_generation_percent", {}), ensure_ascii=False),
                json.dumps(item.get("loss_share_percent", {}), ensure_ascii=False),
                number(item.get("loss_share_change_pp")),
                json.dumps(item.get("export_flow_components_gwh", {}), ensure_ascii=False),
                json.dumps(
                    item.get("export_flow_components_percent", {}), ensure_ascii=False
                ),
            )
        )
    return rows


def summary_metric_rows(results: dict[str, Any]) -> list[tuple[Any, ...]]:
    values: dict[str, tuple[str, str | None]] = {}
    for metric, value in results.get(
        "latest_vintage_endpoint_change_percent_2020_2025", {}
    ).items():
        values[f"latest_vintage_endpoint_change_percent_2020_2025.{metric}"] = (
            str(value),
            "%",
        )
    for metric in (
        "ida_share_unspecified_percent",
        "ida_share_final_consumption_percent",
    ):
        if metric in results:
            values[metric] = (str(results[metric]), "%")
    return [
        (path, value_text, number(value_text), unit)
        for path, (value_text, unit) in values.items()
    ]


def main() -> None:
    write_published_comparisons()
    schema = (ROOT / "schema.sql").read_text(encoding="utf-8")
    results = json.loads((ROOT / "data" / "derived" / "results.json").read_text(
        encoding="utf-8"
    ))

    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    DATABASE.unlink(missing_ok=True)
    with sqlite3.connect(DATABASE) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(schema)

        editions = read_csv("data/editions.csv")
        insert_many(
            connection,
            "INSERT INTO editions VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    row["edition_id"],
                    integer(row["publication_year"]),
                    row["publisher"],
                    row["report_title"],
                    text(row["source_url"]),
                    text(row["source_catalog_url"]),
                    text(row["notes"]),
                )
                for row in editions
            ],
        )

        insert_many(
            connection,
            """INSERT INTO published_comparisons (
                edition_id, base_year, end_year, indicator_code, label_original,
                value_base_gwh, value_end_gwh, published_change_percent,
                source_file, printed_page, data_status_note
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                (
                    row["edition_id"],
                    integer(row["base_year"]),
                    integer(row["end_year"]),
                    row["indicator_code"],
                    row["label_original"],
                    number(row["value_base_gwh"]),
                    number(row["value_end_gwh"]),
                    number(row["published_change_percent"]),
                    text(row["source_file"]),
                    text(row["printed_page"]),
                    text(row["data_status_note"]),
                )
                for row in read_csv("data/source/published_comparisons.csv")
            ],
        )

        insert_many(
            connection,
            """INSERT INTO edition_observations (
                observation_id, reference_year, edition_id, indicator_code, label,
                unit, value, source_key, locator, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                (
                    row["observation"],
                    integer(row["year"]),
                    edition_id(row["edition"]),
                    row["variable"],
                    row["label"],
                    row["unit"],
                    number(row["value"]),
                    row["source_key"],
                    row["locator"],
                    text(row["status"]),
                )
                for row in read_csv("data/observations/edition_observations.csv")
            ],
        )

        insert_many(
            connection,
            """INSERT INTO annual_comparisons (
                comparison, indicator_code, label, unit, start_year, end_year,
                start_value, end_value, source_edition_id, locator
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                (
                    row["comparison"],
                    row["variable"],
                    row["label"],
                    row["unit"],
                    integer(row["start_year"]),
                    integer(row["end_year"]),
                    number(row["start_value"]),
                    number(row["end_value"]),
                    edition_id(row["source_key"]),
                    row["locator"],
                )
                for row in read_csv("data/derived/annual_comparisons.csv")
            ],
        )

        insert_many(
            connection,
            """INSERT INTO historical_latest_series VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                (
                    integer(row["year"]),
                    row["observation"],
                    number(row["generation_gwh"]),
                    number(row["exports_gwh"]),
                    number(row["consumption_gwh"]),
                    number(row["consumption_to_generation_percent"]),
                    edition_id(row["source_key"]),
                    row["locator"],
                    text(row["status"]),
                )
                for row in read_csv("data/derived/historical_latest_series.csv")
            ],
        )

        insert_many(
            connection,
            """INSERT INTO revision_audit (
                reference_year, indicator_code, label, from_observation_id,
                from_edition_id, from_value_gwh, to_observation_id, to_edition_id,
                to_value_gwh, change_gwh, source_from, source_to, note
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                (
                    integer(row["year"]),
                    row["variable"],
                    row["label"],
                    row["from_observation"],
                    edition_id(row["from_edition"]),
                    number(row["from_value_gwh"]),
                    row["to_observation"],
                    edition_id(row["to_edition"]),
                    number(row["to_value_gwh"]),
                    number(row["change_gwh"]),
                    row["source_from"],
                    row["source_to"],
                    text(row["note"]),
                )
                for row in read_csv("data/derived/revision_audit.csv")
            ],
        )

        insert_many(
            connection,
            "INSERT INTO ben2025_indicators VALUES (?, ?, ?, ?, ?, ?)",
            [
                (
                    row["indicator"],
                    row["label"],
                    row["unit"],
                    number(row["value"]),
                    edition_id(row["source_key"]),
                    row["locator"],
                )
                for row in read_csv("data/derived/ben2025_indicators.csv")
            ],
        )

        insert_many(
            connection,
            """INSERT INTO comparison_results VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )""",
            comparison_result_rows(results),
        )
        insert_many(
            connection,
            "INSERT INTO summary_metrics VALUES (?, ?, ?, ?)",
            summary_metric_rows(results),
        )

        insert_many(
            connection,
            "INSERT INTO regulatory_evidence VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    row["id"],
                    row["function"],
                    row["source_key"],
                    row["locator"],
                    row["evidence_status"],
                    row["observation"],
                    row["inference_limit"],
                )
                for row in read_csv("data/context/evidencia_regulatoria.csv")
            ],
        )

        for table in (
            "editions",
            "published_comparisons",
            "edition_observations",
            "annual_comparisons",
            "historical_latest_series",
            "revision_audit",
            "ben2025_indicators",
            "comparison_results",
            "summary_metrics",
            "regulatory_evidence",
        ):
            count = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"{table}: {count}")

    print(f"Base SQLite creada: {DATABASE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
