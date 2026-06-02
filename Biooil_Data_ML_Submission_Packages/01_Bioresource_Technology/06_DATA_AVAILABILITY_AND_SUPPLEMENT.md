# Data Availability and Supplementary Material

## Data availability statement

The cleaned data tables, data dictionary, simulation scripts, machine-learning scripts, trained model metadata, and model-performance summaries will be deposited in a public repository before submission. The repository DOI will be inserted here after deposition.

Temporary local source location:

- SQL Server database: `BIOOIL`
- Composition audit: `COMPOSITION_DATA_REVIEW_Paper/CALISMA_DURUMU_SQL_UYUMLULUK_VE_SUBMISSION_CHECKLIST.md`
- Bio-oil composition CSV: `reverse_ml_biooil_to_product/data/biooil_reference_data/biooil_compositions_30.csv`
- Reformer ML dataset: `reverse_ml_biooil_to_product/reformer_only_model/output/reformer_ml_dataset.csv`
- Clean reverse-ML dataset: `reverse_ml_biooil_to_product/ml_reverse_prediction/data/processed/reformer_data_clean.csv`
- ML metrics: `reverse_ml_biooil_to_product/ml_reverse_prediction/output/metrics/`
- BiooilID holdout metrics: `reverse_ml_biooil_to_product/optimization_control_mpc/results/metrics/biooil_id_holdout_metrics.json`

## Recommended repository contents

- `data/raw_sql_exports/`
- `data/processed/reformer_data_clean.csv`
- `data/processed/biooil_compositions_30.csv`
- `metadata/data_dictionary.csv`
- `metadata/source_reference_table.csv`
- `scripts/cantera_generation/`
- `scripts/ml_training/`
- `scripts/validation/`
- `results/model_metrics/`
- `results/figures/`
- `README.md`
- `LICENSE`

## Supplementary files

Supplementary File S1. SQL-derived bio-oil composition audit table.

Supplementary File S2. Data dictionary for bio-oil classes, reformer inputs, syngas outputs, and ML targets.

Supplementary File S3. Cantera simulation settings and surrogate species mapping.

Supplementary File S4. Model hyperparameters and performance metrics.

Supplementary File S5. BiooilID holdout validation results.

## Data limitation note

The SQL-derived composition layer is class-level and literature-derived. It is not a raw GC-MS repository. Records derived from secondary review sources should be flagged or excluded in primary-source-only sensitivity analyses.

