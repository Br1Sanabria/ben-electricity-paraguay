# Command Guide and Verified Outputs

This guide explains the purpose of every shell command and SQL example in the README and records the output captured by running them against the repository database.

## Test environment

- Date: 2026-10-31
- Operating system shell: Windows PowerShell
- Python: 3.14.8
- SQLite access: Python’s built-in `sqlite3` module. The `sqlite3` command-line program was not installed in the test environment.
- Working directory: the repository root

All commands and queries below completed successfully. The database was rebuilt before the SQL examples were run.

## 1. Rebuild the SQLite database

**Intent:** translate maintained metadata and analysis notes, re-export the original `Datos BEN` worksheet to CSV, then rebuild the portable SQLite database from the repository’s CSV and JSON files.

Run from the repository root:

```bash
python scripts/build_database.py
```

**Captured output:**

```text
editions: 6
published_comparisons: 107
edition_observations: 60
annual_comparisons: 38
historical_latest_series: 6
revision_audit: 24
ben2025_indicators: 5
comparison_results: 5
summary_metrics: 5
regulatory_evidence: 10
SQLite database created: db\ben_electricity.sqlite
```

The row counts describe the tables written to `db/ben_electricity.sqlite`. The command exited with code `0`.

## 2. Query the published BEN 2025 comparison table

**Intent:** compare the values published in BEN 2025 for 2024 and 2025. `label_en` provides a readable English label; `label_original` preserves the published Spanish wording. Negative values retain the signs used in the source table.

```sql
SELECT edition_id, base_year, end_year, indicator_code,
       label_en, label_original, value_base_gwh, value_end_gwh,
       published_change_percent
FROM published_comparisons
WHERE edition_id = 'BEN2025'
ORDER BY indicator_code;
```

**Captured response — 20 rows:**

| edition_id | base_year | end_year | indicator_code | label_en | label_original | value_base_gwh | value_end_gwh | published_change_percent |
| --- | ---: | ---: | --- | --- | --- | ---: | ---: | ---: |
| BEN2025 | 2024 | 2025 | consumption_commercial_public_services | Commercial and public services | Comercial y Servicios Públicos | 4949.6 | 5228.4 | 5.6 |
| BEN2025 | 2024 | 2025 | consumption_industry | Industrial | Industrial | 2921.9 | 3059.6 | 4.7 |
| BEN2025 | 2024 | 2025 | consumption_other_sectors | Other sectors | Otros sectores | 9500.3 | 12024.3 | 26.6 |
| BEN2025 | 2024 | 2025 | consumption_residential | Residential | Residencial | 7064.4 | 7425.6 | 5.1 |
| BEN2025 | 2024 | 2025 | consumption_unspecified | Other unspecified | Otros no especificados | 4550.7 | 6796.0 | 49.3 |
| BEN2025 | 2024 | 2025 | domestic_supply_demand | SUPPLY / DOMESTIC DEMAND | OFERTA / DEMANDA INTERNA | 19486.7 | 22509.5 | 15.5 |
| BEN2025 | 2024 | 2025 | exports | Exports | Exportación | -15998.1 | -15539.3 | -2.9 |
| BEN2025 | 2024 | 2025 | final_consumption | FINAL CONSUMPTION | CONSUMO FINAL | 19486.7 | 22509.5 | 15.5 |
| BEN2025 | 2024 | 2025 | generation_ande | ANDE | ANDE | 768.2 | 697.6 | -9.2 |
| BEN2025 | 2024 | 2025 | generation_ande_hydro_solar | Hydropower + Solar | Hidroeléctrica + Solar | 767.7 | 695.7 | -9.4 |
| BEN2025 | 2024 | 2025 | generation_autoproducers | Autoproducers | Autoproductores | 281.4 | 286.4 | 1.8 |
| BEN2025 | 2024 | 2025 | generation_binational | Binational hydropower plants | Binacionales | 41669.0 | 44585.1 | 7.0 |
| BEN2025 | 2024 | 2025 | generation_gross | Gross generation | Generación Bruta | 42718.6 | 45569.1 | 6.7 |
| BEN2025 | 2024 | 2025 | generation_power_plants | Power plants | Centrales eléctricas | 42437.2 | 45282.7 | 6.7 |
| BEN2025 | 2024 | 2025 | generation_thermal | Thermal | Térmica | 0.5 | 1.9 | 322.2 |
| BEN2025 | 2024 | 2025 | imports | Imports | Importación | 0.0 | 0.0 |  |
| BEN2025 | 2024 | 2025 | losses_distribution | Distribution | Distribución | -5725.9 | -5892.8 | 2.9 |
| BEN2025 | 2024 | 2025 | losses_total | Total losses | Pérdidas Totales | -6940.1 | -7191.5 | 3.6 |
| BEN2025 | 2024 | 2025 | losses_transmission | Transmission | Transmisión | -1214.2 | -1298.7 | 7.0 |
| BEN2025 | 2024 | 2025 | own_use_power_sector | Power-plant consumption / ANDE self-consumption | Consumo en centrales / autoconsumo ANDE | -293.7 | -328.8 | 12.0 |

## 3. Query generation by publication edition and reference year

**Intent:** follow gross generation while keeping the edition that published each value separate from the year the value describes. Repeated reference years show how later BEN editions may restate earlier values.

```sql
SELECT edition_id, reference_year, label, value, unit, locator, status
FROM edition_observations
WHERE indicator_code = 'generation'
ORDER BY reference_year, edition_id;
```

**Captured response — 10 rows:**

| edition_id | reference_year | label | value | unit | locator | status |
| --- | ---: | --- | ---: | --- | --- | --- |
| BEN2021 | 2020 | Gross generation | 46373.0 | GWh | Electricity balance comparison; p. 9 | Value published in BEN 2021; 2021–2020 comparative balance. |
| BEN2021 | 2021 | Gross generation | 40576.2 | GWh | Electricity balance comparison; p. 9 | 2021 preliminary; data cutoff 2022-07-31. |
| BEN2022 | 2021 | Gross generation | 40576.2 | GWh | Electricity balance comparison; p. 14 | Comparative value in BEN 2022; matches BEN 2021. |
| BEN2022 | 2022 | Gross generation | 43880.8 | GWh | Electricity balance comparison; p. 14 | 2022 preliminary; cutoff 2023-07-31; table follows the SIEN series. |
| BEN2023 | 2022 | Gross generation | 44109.6 | GWh | Table 3; p. 28 | 2022 values restated under siePARAGUAY; gross generation includes autoproducers. |
| BEN2023 | 2023 | Gross generation | 53041.7 | GWh | Table 3; p. 28 | 2023 preliminary; data cutoff 2024-07-31. |
| BEN2024 | 2023 | Gross generation | 53041.7 | GWh | Table 3; p. 48 | 2023 aggregate values reproduced in BEN 2024. |
| BEN2024 | 2024 | Gross generation | 42676.2 | GWh | Table 3; p. 48 | 2024 preliminary; data cutoff 2025-07-31. |
| BEN2025 | 2024 | Gross generation | 42718.6 | GWh | Table 3; p. 49 | 2024 value revised in the BEN 2025 edition. |
| BEN2025 | 2025 | Gross generation | 45569.1 | GWh | Table 3; p. 49 | 2025 preliminary; data cutoff 2026-07-31. |

## 4. Query revisions to final consumption

**Intent:** compare final-consumption values for the same reference year across two editions and show the absolute change. A zero change means both editions report the same value.

```sql
SELECT reference_year, from_edition_id, from_value_gwh,
       to_edition_id, to_value_gwh, change_gwh, note
FROM revision_audit
WHERE indicator_code = 'consumption'
ORDER BY reference_year, from_edition_id;
```

**Captured response — 4 rows:**

| reference_year | from_edition_id | from_value_gwh | to_edition_id | to_value_gwh | change_gwh | note |
| ---: | --- | ---: | --- | ---: | ---: | --- |
| 2021 | BEN2021 | 13706.1 | BEN2022 | 13706.1 | 0.0 | The 2021 values match in BEN 2021 and BEN 2022. |
| 2022 | BEN2022 | 14432.6 | BEN2023 | 14661.5 | 228.9 | BEN 2023 reports 2022 under siePARAGUAY and includes autoproducers in gross generation; the change should not be read as a statistical revision alone. |
| 2023 | BEN2023 | 15993.6 | BEN2024 | 15993.6 | 0.0 | The 2023 aggregates are reproduced unchanged in BEN 2024. |
| 2024 | BEN2024 | 19444.2 | BEN2025 | 19486.7 | 42.5 | BEN 2025 revises 2024 flows, including an updated residential estimate. |

## Reproduce the SQL results

The SQL blocks can be run in any SQLite client against `db/ben_electricity.sqlite`. In the test environment, the same statements were executed through Python’s standard-library `sqlite3` module because the SQLite command-line program was unavailable. No third-party Python package was needed.

The original Spanish labels and source notes shown in the first query are intentional: their English equivalents are stored in adjacent fields ending in `_en`.
