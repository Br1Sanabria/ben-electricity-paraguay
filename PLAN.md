# Work Plan: Paraguay BEN Electricity Data

## Objective

Prepare a version-controlled GitHub repository with a queryable, traceable database of electricity data extracted from and analyzed across editions of Paraguay’s National Energy Balance (*Balance Energético Nacional*, BEN).

## Initial scope

- Editions covered by the source extraction: BEN 2020 through BEN 2025.
- The source workbook contains 107 numeric rows from comparison tables, including original labels, published values, changes, sources, locators, and notes.
- The consolidated analysis contains 60 balance observations from BEN 2021 through BEN 2025, 38 year-over-year comparisons, 24 revision-audit records, 6 latest-vintage historical values, and 5 additional BEN 2025 indicators.
- Regulatory information from the analysis is stored separately from BEN observations.
- Official PDFs are referenced through source links; the repository retains the original workbook and exported CSV files.

## Task assignments

| Owner | Task | Status |
| --- | --- | --- |
| Agent 1: BEN inventory | Identify editions, tables, fields, row counts, and comparability limits in the source files. | Complete |
| Agent 2: GitHub access | Review the local repository, available tools, and publication requirements without exposing credentials. | Complete; public repository created and write access verified. |
| Agent 3: data architecture | Recommend the data layout, canonical tables, derived results, and update workflow. | Complete |
| Coordinator | Integrate the extraction, create the SQLite schema and rebuild script, document queries, and publish the repository. | Complete; 17 repository paths verified. |

## Deliverables

1. CSV of published comparison tables, preserving original labels, signs, and source notes.
2. CSV of observations by publication edition and reference year, with indicator, unit, and locator.
3. CSV files of derived analysis results, clearly identified as derived data.
4. SQL schema and a standard-library Python script to rebuild the SQLite database.
5. English README with coverage, provenance, limitations, and example queries.
6. Public GitHub repository containing the queryable database and traceability sources.

## Acceptance criteria

- BEN 2020–2025 is represented in the source extraction tables.
- Publication edition and reference year remain distinct; values from different editions are not silently merged.
- Published values retain their signs and source precision; normalized levels and derived calculations remain separate.
- Each row retains its available provenance and locator.
- The SQLite database can be rebuilt from the repository CSV and JSON files, and its structure is documented for queries.
- Scope and comparability warnings from the source analysis remain visible.
- Documentation, identifiers, and analysis labels are in English; original source wording remains available in fields ending in `_original`.

## Work sequence

1. Copy the BEN inputs and source extraction into the repository. **Complete.**
2. Export the main comparison table to CSV and organize analysis CSV files by purpose. **Complete.**
3. Create the SQL schema and SQLite builder. **Complete.**
4. Document the tables, example queries, and update process. **Complete.**
5. Prepare the local Git repository. **Complete.**
6. Publish the content to `Br1Sanabria/ben-electricity-paraguay` and verify the data files. **Complete.**

## Publication decision

The destination is the public repository [`Br1Sanabria/ben-electricity-paraguay`](https://github.com/Br1Sanabria/ben-electricity-paraguay). The initial data commit is `3c8bd3c8863f2617c901f769f11f0c1e8262f472`. The English-language revision contains 19 paths; original source wording remains available in `_original` fields and in the unchanged source workbook.
