#!/usr/bin/env python3
"""Export the `Datos BEN` worksheet from the supplied source workbook to CSV."""

from __future__ import annotations

import csv
import posixpath
import re
import zipfile
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "sources" / "extraccion_BEN_electricidad_graficos.xlsx"
OUTPUT = ROOT / "data" / "source" / "published_comparisons.csv"
MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"m": MAIN_NS, "r": REL_NS, "p": PKG_REL_NS}

FIELDS = [
    "edition_id",
    "base_year",
    "end_year",
    "indicator_code",
    "label_original",
    "value_base_gwh",
    "value_end_gwh",
    "published_change_percent",
    "source_file",
    "printed_page",
    "data_status_note",
]


def column_index(cell_reference: str) -> int:
    letters = re.match(r"[A-Z]+", cell_reference)
    if not letters:
        raise ValueError(f"Invalid cell reference: {cell_reference}")
    index = 0
    for letter in letters.group(0):
        index = index * 26 + ord(letter) - ord("A") + 1
    return index - 1


def read_cell(cell: ET.Element, shared_strings: list[str]) -> str:
    value = cell.find("m:v", NS)
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        inline = cell.find("m:is", NS)
        return "" if inline is None else "".join(
            item.text or "" for item in inline.iter(f"{{{MAIN_NS}}}t")
        )
    if value is None or value.text is None:
        return ""
    if cell_type == "s":
        return shared_strings[int(value.text)]
    return value.text


def number_text(value: str, places: int) -> str:
    if not value:
        return ""
    number = Decimal(value).quantize(
        Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP
    )
    return format(number, "f")


def workbook_sheet_path(archive: zipfile.ZipFile, sheet_name: str) -> str:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    targets = {item.attrib["Id"]: item.attrib["Target"] for item in relationships}
    sheets = workbook.find("m:sheets", NS)
    if sheets is None:
        raise ValueError("The workbook has no sheet list")
    for sheet in sheets:
        if sheet.attrib.get("name") == sheet_name:
            target = targets[sheet.attrib[f"{{{REL_NS}}}id"]].lstrip("/")
            return target if target.startswith("xl/") else posixpath.normpath(
                posixpath.join("xl", target)
            )
    raise ValueError(f"Worksheet not found: {sheet_name}")


def extract_rows() -> list[dict[str, str]]:
    with zipfile.ZipFile(WORKBOOK) as archive:
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared_strings = [
                "".join(item.text or "" for item in entry.iter(f"{{{MAIN_NS}}}t"))
                for entry in shared_root.findall("m:si", NS)
            ]

        sheet = ET.fromstring(archive.read(workbook_sheet_path(archive, "Datos BEN")))
        sheet_data = sheet.find("m:sheetData", NS)
        if sheet_data is None:
            raise ValueError("The `Datos BEN` worksheet is empty")

        headers: dict[int, str] = {}
        output: list[dict[str, str]] = []
        for row in sheet_data.findall("m:row", NS):
            row_number = int(row.attrib["r"])
            cells = {
                column_index(cell.attrib["r"]): read_cell(cell, shared_strings)
                for cell in row.findall("m:c", NS)
            }
            if row_number == 4:
                headers = {index: value for index, value in cells.items() if value}
                continue
            if row_number < 5 or not cells:
                continue

            source = {header: cells.get(index, "") for index, header in headers.items()}
            if not any(source.values()):
                continue
            year = source["Edición BEN"].strip()
            output.append(
                {
                    "edition_id": f"BEN{year}",
                    "base_year": source["Año base"],
                    "end_year": source["Año final"],
                    "indicator_code": source["Código comparable"],
                    "label_original": source["Rótulo original"],
                    "value_base_gwh": number_text(
                        source["Valor base publicado (GWh)"], 1
                    ),
                    "value_end_gwh": number_text(
                        source["Valor final publicado (GWh)"], 1
                    ),
                    "published_change_percent": number_text(
                        source["Variación publicada (%)"], 2
                    ),
                    "source_file": source["Archivo fuente"],
                    "printed_page": source["Página impresa"],
                    "data_status_note": source["Estado del dato / nota"],
                }
            )
        if not output:
            raise ValueError("No comparison rows were found in the source workbook")
        return output


def main() -> None:
    rows = extract_rows()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    counts = Counter(row["edition_id"] for row in rows)
    print(f"CSV actualizado: {OUTPUT.relative_to(ROOT)}")
    print(f"Renglones exportados: {len(rows)}")
    for edition_id in sorted(counts):
        print(f"{edition_id}: {counts[edition_id]}")


if __name__ == "__main__":
    main()
