# Electricity Data from Paraguay’s National Energy Balance (BEN)

This repository provides a queryable, traceable dataset of electricity figures extracted from and analyzed across editions of Paraguay’s National Energy Balance (*Balance Energético Nacional*, BEN). The initial release covers BEN 2020 through BEN 2025.

## Coverage

- 6 BEN editions, 2020–2025.
- 107 rows transcribed from published electricity comparison tables.
- 60 balance observations with publication edition and reference year kept separate, from BEN 2021–BEN 2025.
- 38 year-over-year comparisons, 24 cross-edition revision records, 6 latest-vintage historical values, and 5 additional BEN 2025 indicators.
- 10 regulatory-evidence records, stored separately from BEN energy data.

The source extraction includes the 2019–2020 pair from BEN 2020 and annual pairs through 2024–2025 from BEN 2025. The consolidated analysis tables begin with BEN 2021.

## Repository contents

| Path | Contents |
| --- | --- |
| `db/ben_electricity.sqlite` | SQLite database ready to download and query. |
| `data/editions.csv` | Edition metadata, English and original publisher/report names, and source links. |
| `data/source/published_comparisons.csv` | Transcribed published values with original Spanish labels and English translations. |
| `data/observations/edition_observations.csv` | Balance observations by publication edition, reference year, and indicator. |
| `data/derived/annual_comparisons.csv` | Year-over-year comparisons used in the analysis. |
| `data/derived/historical_latest_series.csv` | Latest available edition value for each reference year. |
| `data/derived/revision_audit.csv` | Changes to the same reference-year value across editions. |
| `data/derived/ben2025_indicators.csv` | Additional indicators from BEN 2025. |
| `data/derived/results.json` | Full precision results and analysis notes. |
| `data/context/regulatory_evidence.csv` | Regulatory evidence related to the analysis, separate from energy data. |
| `sources/source_extraction_ben_electricity.xlsx` | Original supplied workbook, retained unchanged for provenance. |
| `schema.sql` | SQLite relational schema. |
| `scripts/` | Extraction, translation, and database rebuild scripts. |
| `COMMAND_GUIDE.md` | Intent and captured output for every README command and SQL example. |

Documentation, identifiers, database column names, analysis labels, and operational notes are in English. Fields ending in `_original` preserve the Spanish wording found in the source material. `label_en` provides an English translation alongside each published comparison label.

## SQLite tables

| Table | Initial rows | Purpose |
| --- | ---: | --- |
| `editions` | 6 | Edition metadata, including original and translated publisher/report names. |
| `published_comparisons` | 107 | Published comparison values, preserving original labels and providing English translations. |
| `edition_observations` | 60 | Balance values tied to both the edition that publishes them and the year they describe. |
| `annual_comparisons` | 38 | Paired levels used for year-over-year comparisons. |
| `historical_latest_series` | 6 | Latest available edition value for each reference year. |
| `revision_audit` | 24 | Differences across editions for the same indicator and reference year. |
| `ben2025_indicators` | 5 | Additional indicators reported or analyzed for BEN 2025. |
| `comparison_results` | 5 | Calculated comparison results, including JSON breakdowns. |
| `summary_metrics` | 5 | Scalar summary metrics. |
| `regulatory_evidence` | 10 | Documentary regulatory evidence with stated inference limits. |

Derived outputs retain their source edition and locator. `published_comparisons` preserves the source sign and label. `edition_observations` uses the positive magnitudes adopted by the analysis to close the electricity balance.

## Example queries

Published comparison values, with the English label and the original Spanish label:

```sql
SELECT edition_id, base_year, end_year, indicator_code,
       label_en, label_original, value_base_gwh, value_end_gwh,
       published_change_percent
FROM published_comparisons
WHERE edition_id = 'BEN2025'
ORDER BY indicator_code;
```

Generation by publication edition and reference year:

```sql
SELECT edition_id, reference_year, label, value, unit, locator, status
FROM edition_observations
WHERE indicator_code = 'generation'
ORDER BY reference_year, edition_id;
```

Consumption revisions across editions:

```sql
SELECT reference_year, from_edition_id, from_value_gwh,
       to_edition_id, to_value_gwh, change_gwh, note
FROM revision_audit
WHERE indicator_code = 'consumption'
ORDER BY reference_year, from_edition_id;
```

## Rebuild the database

Python 3 is required. The scripts use only the Python standard library.

```bash
python scripts/build_database.py
```

The command translates the maintained metadata and analysis notes, exports the `Datos BEN` worksheet from the original workbook to `data/source/published_comparisons.csv`, and rebuilds `db/ben_electricity.sqlite` from the repository’s CSV and JSON files.

See [`COMMAND_GUIDE.md`](COMMAND_GUIDE.md) for the intent and verified output of this command and each SQL example above.

## Provenance and treatment

- Official PDFs are linked rather than redistributed. `editions.csv` links to the Vice Ministry of Mines and Energy’s historical catalog and to available official reports.
- The supplied workbook is retained unchanged. Published Spanish labels, page notes, and data-status notes are preserved in `_original` fields with English translations beside them.
- CSV exports round GWh values to one decimal place and percentages to two decimal places to remove Excel floating-point residue. The original workbook remains available for review.
- Blank source fields remain blank; they are not converted to zero.
- Year-over-year changes are calculated within the edition that publishes each pair. `historical_latest_series` selects the latest available edition for each reference year; it should not be used to chain a single annual growth rate because later editions revise earlier values.
- BEN 2023 expands generation coverage and updates earlier values. BEN 2024 and BEN 2025 also revise previous years. These changes are listed in `revision_audit`.
- Comparable sector detail in the analysis covers 2023–2025. Categories and coverage differ in earlier editions.
- Balance closure allows a tolerance of up to 0.3 GWh for rounding, as documented in the analysis material.
- Some BEN 2020 printed-page locators still require verification. Direct PDF links for BEN 2020 and BEN 2021 were unavailable when this repository was prepared; the official catalog and the references stored in the extraction are retained.
- Regulatory evidence is not an exhaustive inventory or legal audit. Each record states its inference limits.

## Official sources

- [Historical BEN catalog — Vice Ministry of Mines and Energy](https://minasyenergia.mopc.gov.py/index.php?FontSize=font-large&Itemid=816&id=2069&option=com_content&view=article)
- [BEN 2022 Statistical Summary (*Resumen Estadístico*)](https://minasyenergia.mopc.gov.py/pdf/balance2022/BEN%202022_Estadistico_VF.pdf)
- [BEN 2023 Analytical Report (*Analítico*)](https://minasyenergia.mopc.gov.py/pdf/balance2023/BEN%202023_Analitico%20VF.pdf)
- [BEN 2024 Paraguay report](https://minasyenergia.mopc.gov.py/pdf/balance2024/BEN%202024_Paraguay.pdf)
- [MOPC announcement on BEN 2025 results](https://mopc.gov.py/consumo-de-electricidad-supera-por-primera-vez-al-de-biomasa-solida-en-2025/)

## GitHub repository

The public repository is [`Br1Sanabria/ben-electricity-paraguay`](https://github.com/Br1Sanabria/ben-electricity-paraguay). It contains the SQLite database, query-ready CSV files, schema, rebuild scripts, and source material retained for provenance.
