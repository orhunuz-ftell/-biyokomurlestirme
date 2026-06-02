# Data Repository Package

Purpose: deposit this folder, or a cleaned version of it, to a public repository before journal submission.

Recommended repository title:

Curated bio-oil composition and steam-reforming inverse prediction dataset

## Contents to include

The local package contains or should contain:

- Cleaned bio-oil composition table for the six target groups.
- Cleaned reverse-ML reformer dataset.
- SQL audit summary tables under `data/sql_exports/`.
- Cantera mechanism and simulation scripts.
- ML model training and evaluation scripts.
- Row-wise model metrics.
- BiooilID holdout validation metrics.
- Figure-generation scripts or source figures.
- Data dictionary.
- Source manifest.

## Data statement draft

The curated composition tables, reformer simulation dataset, data dictionary, source manifest, model metrics, and analysis scripts are available at [repository DOI to be inserted after deposition]. The original SQL database is not deposited as a live database file; instead, manuscript-relevant SQL exports and processed CSV files are provided to ensure reproducibility without machine-specific SQL Server dependencies.

## Important limitations

- The composition data are literature-derived and class-level.
- The package is not a raw GC-MS or chromatogram repository.
- Some SQL records come from secondary review sources and should be flagged in the source table.
- The 1,350 ML samples are simulation-expanded cases from 30 unique model-ready bio-oil compositions, not 1,350 independent experimental bio-oils.

## SQL exports included

- `sql_table_counts.csv`
- `biooil_missingness.csv`
- `biooil_core_completeness.csv`
- `biooil_composition_sums.csv`
- `biooil_composition_sum_summary.csv`
- `biooil_reference_counts.csv`
- `biooil_joined_source_rows.csv`
- `reference_source_classification_template.csv`

The `reference_source_classification_template.csv` file must be manually verified before deposition because source type cannot be inferred perfectly from SQL metadata alone.

## Suggested license

Use one of the following after author approval:

- CC BY 4.0 for data and documentation.
- MIT or BSD-3-Clause for code.
