# Source Audit and Submission Strategy

Date: 31 May 2026

Working title family:

Data availability constraints and deep learning-based inverse prediction of bio-oil composition from steam reforming syngas

## Submission order

1. Bioresource Technology
2. Energy and AI
3. Fuel Processing Technology

## Why the two publication lines should be combined

The composition-data review alone is currently not strong enough as a standalone database or data article. The SQL dataset is useful, but it is incomplete, class-level, and not a raw GC-MS or compound-level repository. The reverse machine-learning work is stronger as an original research contribution, but it needs a defensible explanation of why the input data are limited and why data stewardship matters.

The combined article should therefore be framed as:

> A data-curated, thermodynamically validated inverse modeling study that uses the documented scarcity and inconsistency of reusable bio-oil composition data as motivation for a syngas-based soft sensor.

The review/data-availability part becomes the problem framing and data-quality analysis. The reverse ML part becomes the main original contribution.

## Sources used

Primary local sources:

- `OrhunUzdiyem_tik4.docx`: latest TIK source specified by the user; used for thesis aim, Cantera method, MLP architecture, model comparison, and future MPC framing.
- `TIK_RAPOR_REFORMER_MODEL.md`: used for reformer-only Cantera simulation details, 3,150 simulations, thermodynamic checks, and database schema.
- `reverse_ml_biooil_to_product/ml_reverse_prediction/FINAL_REPORT.md`: used for final ML model performance and manuscript claims.
- `reverse_ml_biooil_to_product/ml_reverse_prediction/ML_WORK_SUMMARY.md`: used for data cleaning, 1,350 clean samples, model split, and feature statistics.
- `reverse_ml_biooil_to_product/optimization_control_mpc/results/metrics/biooil_id_holdout_metrics.json`: used for group-holdout generalization audit.
- `reverse_ml_biooil_to_product/optimization_control_mpc/TIK5_REPORT_DRAFT.md`: used only as a supporting source for BiooilID holdout and MPC/soft-sensor integration.
- `COMPOSITION_DATA_REVIEW_Paper/CALISMA_DURUMU_SQL_UYUMLULUK_VE_SUBMISSION_CHECKLIST.md`: used for SQL data audit and submission requirements.
- `SystematicLiteratureReview.docx`: used as a narrative source for bio-oil composition reporting and data stewardship framing.

Official journal sources checked:

- Bioresource Technology Guide for Authors: https://www.sciencedirect.com/journal/bioresource-technology/publish/guide-for-authors
- Energy and AI Guide for Authors: https://www.sciencedirect.com/journal/energy-and-ai/publish/guide-for-authors
- Fuel Processing Technology Guide for Authors: https://www.sciencedirect.com/journal/fuel-processing-technology/publish/guide-for-authors

## Local evidence base

SQL data audit:

- `Biooil`: 70 class-level composition records.
- `Reference`: 19 total references; `Biooil` records linked to 14 distinct references.
- 43 distinct biomass names are linked through `Biooil -> Experiment -> Biomass -> Reference`.
- Pyrolysis temperature range in linked records: 300-850 degC.
- 10-class complete records in `Biooil`: 0/70.
- Six-core-class complete records: 30/70.
- Individual marker fields are sparse: guaiacol, syringol, and catechol are each present in 5/70 records; N-containing is present in 7/70 records.
- Composition sums with NULL treated as zero range from 11.07 to 103.49, average 87.82.
- `Biooil_Mutlak`: 18 complete subclass rows, but sums are 30.94-48.64, average 39.87, so this is not a complete whole-oil composition layer.
- Sampaio et al. 2025 review-derived entries should be flagged as secondary-source records, not primary experimental records.

Simulation and ML evidence:

- Reformer-only Cantera simulation generated 3,150 thermodynamic cases.
- After target-completeness cleaning, 1,350 ML-ready samples remained.
- These 1,350 samples come from 30 unique bio-oil compositions and 45 process condition combinations.
- Inputs: reformer temperature, pressure, steam-to-carbon ratio, H2, CO, CO2, CH4, and H2O.
- Targets: aromatics, acids, alcohols, furans, phenols, and aldehydes/ketones.
- Best row-wise test model: MLP, average R2 = 0.863, average MAE = 4.03%.
- Component R2 values for the MLP: aromatics 0.942, acids 0.877, alcohols 0.853, furans 0.897, phenols 0.762, aldehydes/ketones 0.849.
- Baselines: linear regression R2 = 0.332, random forest R2 = 0.571, XGBoost R2 = 0.603.
- Weighted ensemble R2 = 0.797, below the MLP.
- BiooilID holdout audit: 24 train BiooilIDs, 6 held-out BiooilIDs; 1,080 train samples, 270 test samples.
- BiooilID holdout showed strong generalization for aromatics and acids but weak behavior for alcohols. This must be presented as a limitation, not hidden.

## Core claim that is safe

The safe manuscript claim is:

> Literature-derived bio-oil composition data are sufficiently informative to train a thermodynamically constrained inverse soft sensor within the represented data domain, but incomplete reporting and limited composition diversity impose clear generalization limits for unseen bio-oils.

## Claims to avoid

Do not claim:

- A complete compound-level bio-oil database was created.
- Raw GC-MS data were curated.
- The MLP result proves universal generalization to any new bio-oil.
- The 1,350 ML samples are independent experimental observations.
- The BiooilID holdout result confirms the same performance as the row-wise split.

## Required pre-upload decisions

These are the only items that cannot be completed without author confirmation:

- Final author list and order.
- Corresponding author email, postal address, and phone.
- Funding statement.
- Repository DOI or private/shared data location.
- Final manual graphical abstract image. Elsevier policies do not allow generative AI-created graphical abstracts or figures; the prepared brief must be redrawn manually by the author/designer.

