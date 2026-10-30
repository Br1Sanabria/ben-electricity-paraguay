PRAGMA foreign_keys = ON;

CREATE TABLE editions (
    edition_id TEXT PRIMARY KEY,
    publication_year INTEGER NOT NULL,
    publisher TEXT NOT NULL,
    publisher_original TEXT NOT NULL,
    report_title TEXT NOT NULL,
    report_title_original TEXT NOT NULL,
    source_url TEXT,
    source_catalog_url TEXT,
    notes TEXT
);

CREATE TABLE published_comparisons (
    row_id INTEGER PRIMARY KEY,
    edition_id TEXT NOT NULL REFERENCES editions(edition_id),
    base_year INTEGER NOT NULL,
    end_year INTEGER NOT NULL,
    indicator_code TEXT NOT NULL,
    label_original TEXT NOT NULL,
    label_en TEXT NOT NULL,
    value_base_gwh REAL,
    value_end_gwh REAL,
    published_change_percent REAL,
    source_file TEXT,
    printed_page_original TEXT,
    printed_page_en TEXT,
    data_status_note_original TEXT,
    data_status_note_en TEXT
);

CREATE TABLE edition_observations (
    row_id INTEGER PRIMARY KEY,
    observation_id TEXT NOT NULL,
    reference_year INTEGER NOT NULL,
    edition_id TEXT NOT NULL REFERENCES editions(edition_id),
    indicator_code TEXT NOT NULL,
    label TEXT NOT NULL,
    unit TEXT NOT NULL,
    value REAL NOT NULL,
    source_key TEXT NOT NULL,
    locator TEXT NOT NULL,
    status TEXT,
    UNIQUE (observation_id, indicator_code)
);

CREATE TABLE annual_comparisons (
    row_id INTEGER PRIMARY KEY,
    comparison TEXT NOT NULL,
    indicator_code TEXT NOT NULL,
    label TEXT NOT NULL,
    unit TEXT NOT NULL,
    start_year INTEGER NOT NULL,
    end_year INTEGER NOT NULL,
    start_value REAL NOT NULL,
    end_value REAL NOT NULL,
    source_edition_id TEXT NOT NULL REFERENCES editions(edition_id),
    locator TEXT NOT NULL
);

CREATE TABLE historical_latest_series (
    reference_year INTEGER PRIMARY KEY,
    observation_id TEXT NOT NULL,
    generation_gwh REAL NOT NULL,
    exports_gwh REAL NOT NULL,
    consumption_gwh REAL NOT NULL,
    consumption_to_generation_percent REAL NOT NULL,
    source_edition_id TEXT NOT NULL REFERENCES editions(edition_id),
    locator TEXT NOT NULL,
    status TEXT
);

CREATE TABLE revision_audit (
    row_id INTEGER PRIMARY KEY,
    reference_year INTEGER NOT NULL,
    indicator_code TEXT NOT NULL,
    label TEXT NOT NULL,
    from_observation_id TEXT NOT NULL,
    from_edition_id TEXT NOT NULL REFERENCES editions(edition_id),
    from_value_gwh REAL NOT NULL,
    to_observation_id TEXT NOT NULL,
    to_edition_id TEXT NOT NULL REFERENCES editions(edition_id),
    to_value_gwh REAL NOT NULL,
    change_gwh REAL NOT NULL,
    source_from TEXT NOT NULL,
    source_to TEXT NOT NULL,
    note TEXT
);

CREATE TABLE ben2025_indicators (
    indicator_code TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    unit TEXT NOT NULL,
    value REAL NOT NULL,
    source_edition_id TEXT NOT NULL REFERENCES editions(edition_id),
    locator TEXT NOT NULL
);

CREATE TABLE comparison_results (
    comparison TEXT PRIMARY KEY,
    start_year INTEGER NOT NULL,
    end_year INTEGER NOT NULL,
    export_change_gwh REAL,
    export_contraction_gwh REAL,
    national_market_growth_gwh REAL,
    national_market_contribution_percent REAL,
    balance_change_percent_json TEXT NOT NULL,
    balance_residual_gwh_json TEXT NOT NULL,
    demand_generation_percent_json TEXT NOT NULL,
    loss_share_percent_json TEXT NOT NULL,
    loss_share_change_pp REAL,
    export_flow_components_gwh_json TEXT NOT NULL,
    export_flow_components_percent_json TEXT NOT NULL
);

CREATE TABLE summary_metrics (
    metric_path TEXT PRIMARY KEY,
    value_text TEXT NOT NULL,
    value_numeric REAL,
    unit TEXT
);

CREATE TABLE regulatory_evidence (
    evidence_id TEXT PRIMARY KEY,
    function TEXT NOT NULL,
    source_key TEXT NOT NULL,
    locator TEXT NOT NULL,
    evidence_status TEXT NOT NULL,
    observation TEXT NOT NULL,
    inference_limit TEXT NOT NULL
);

CREATE INDEX idx_published_comparisons_edition
    ON published_comparisons(edition_id, base_year, end_year);
CREATE INDEX idx_edition_observations_year_indicator
    ON edition_observations(reference_year, indicator_code);
CREATE INDEX idx_annual_comparisons_period_indicator
    ON annual_comparisons(start_year, end_year, indicator_code);
CREATE INDEX idx_revisions_year_indicator
    ON revision_audit(reference_year, indicator_code);
