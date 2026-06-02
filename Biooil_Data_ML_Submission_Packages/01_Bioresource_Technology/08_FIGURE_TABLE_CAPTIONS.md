# Figure and Table Plan

Bioresource Technology allows a maximum of 6 figures and/or tables unless justified. Use this compact set.

## Figures

Figure 1. Integrated workflow from literature-derived bio-oil composition records to SQL curation, Cantera reforming simulations, inverse machine learning, and soft-sensor interpretation.

Suggested source: redraw from `tik5/figures/tik5_figure_b03_soft_sensor_workflow.png` and TIK4 workflow notes.

Figure 2. SQL composition-data completeness map showing missingness across the 70 `Biooil` records and major compound classes.

Suggested source: regenerate from SQL audit values.

Figure 3. Cantera reformer simulation design showing six surrogate bio-oil groups, process-condition grid, and syngas outputs.

Suggested source: redraw from TIK4 Cantera section and `TIK_RAPOR_REFORMER_MODEL.md`.

Figure 4. Model comparison for inverse prediction of six bio-oil composition groups.

Suggested source: `reverse_ml_biooil_to_product/ml_reverse_prediction/output/figures/model_comparison_r2.png`

Figure 5. Feature-importance interpretation showing syngas composition as the dominant signal.

Suggested source: `reverse_ml_biooil_to_product/ml_reverse_prediction/output/figures/feature_importance.png`

Figure 6. Row-wise model performance versus BiooilID holdout behavior.

Suggested source: combine `tik5/figures/tik5_figure_b05_split_comparison.png` and `tik5/figures/tik5_figure_b06_biooilid_r2.png`.

## Tables

If the 6 item limit is strict, move these tables to supplementary material.

Table S1. SQL database table counts and data sources.

Table S2. Bio-oil composition missingness by class.

Table S3. ML model performance by component.

Table S4. BiooilID holdout performance by component.

