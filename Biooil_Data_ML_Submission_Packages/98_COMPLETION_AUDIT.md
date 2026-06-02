# Completion Audit

Date: 31 May 2026

Objective:

Prepare separate sequential submission folders and shared submission files for Bioresource Technology, Energy and AI, and Fuel Processing Technology using the available SQL/data, ML reports, and TIK reports.

## Requirement-by-requirement status

1. Separate folders for the three target journals

Status: Completed.

Evidence:

- `01_Bioresource_Technology/`
- `02_Energy_and_AI/`
- `03_Fuel_Processing_Technology/`

2. Same core submission files for each journal

Status: Completed as editable drafts.

Evidence: each journal folder contains 11 Markdown files and 11 DOCX files:

- `00_SUBMISSION_README`
- `01_TITLE_PAGE`
- `02_ANONYMIZED_MANUSCRIPT`
- `03_COVER_LETTER`
- `04_HIGHLIGHTS`
- `05_GRAPHICAL_ABSTRACT_BRIEF`
- `06_DATA_AVAILABILITY_AND_SUPPLEMENT`
- `07_DECLARATIONS`
- `08_FIGURE_TABLE_CAPTIONS`
- `09_SUBMISSION_CHECKLIST`
- `10_REFERENCES_DRAFT`

3. Use of TIK reports

Status: Completed.

Evidence:

- `00_SOURCE_AUDIT_AND_STRATEGY.md` lists `OrhunUzdiyem_tik4.docx` as the primary TIK source.
- TIK4-derived elements are used in the manuscript drafts: thesis aim, six bio-oil groups, Cantera workflow, MLP architecture, model-comparison results, and MPC/soft-sensor framing.
- TIK5 outputs are used as supporting evidence for BiooilID holdout and soft-sensor limitations.

4. Use of SQL/data

Status: Completed.

Evidence:

- `04_Data_Repository_Package/data/sql_exports/` contains SQL-derived CSV exports:
  - `sql_table_counts.csv`
  - `biooil_missingness.csv`
  - `biooil_core_completeness.csv`
  - `biooil_composition_sums.csv`
  - `biooil_composition_sum_summary.csv`
  - `biooil_reference_counts.csv`
  - `biooil_joined_source_rows.csv`
  - `reference_source_classification_template.csv`
- Manuscripts use SQL-derived claims: 70 class-level records, 30 six-core-complete records, 0 ten-class-complete records, and BiooilID/source limitations.

5. Use of ML reports

Status: Completed.

Evidence:

- Manuscripts use ML results from `FINAL_REPORT.md` and `ML_WORK_SUMMARY.md`: 3,150 Cantera cases, 1,350 model-ready samples, 30 unique bio-oil compositions, MLP R2 = 0.863, MAE = 4.03%, baseline comparisons, and ensemble behavior.
- Repository package includes row-wise and holdout metrics under `04_Data_Repository_Package/metrics/`.
- Repository package includes ML scripts under `04_Data_Repository_Package/scripts/ml_reverse_prediction/`.

6. Journal-specific adaptation

Status: Completed as draft packages.

Evidence:

- Bioresource Technology version emphasizes bioresource technology, data stewardship, thermochemical conversion, and double-anonymized submission.
- Energy and AI version emphasizes AI soft sensing, inverse modeling, data-aware validation, and group-aware generalization.
- Fuel Processing Technology version emphasizes fuel-processing soft sensor, steam reforming, syngas quality, and hydrogen-oriented conversion.

7. Submission-ready status

Status: Not fully upload-ready without author action.

Evidence:

- Title pages and declarations still contain author/contact/funding placeholders.
- Data availability statements still require a repository DOI or URL.
- Bioresource Technology requires a manually created graphical abstract image; only a compliant design brief is prepared because Elsevier does not allow generative AI-created graphical abstracts.
- Final reference verification in a reference manager is still required.

## Remaining author-side blockers

These are not inferable safely from the worktree:

1. Final author list and order.
2. Corresponding author email, postal address, and phone.
3. Funding statement.
4. Repository DOI/URL after deposition.
5. Manual graphical abstract image for Bioresource Technology.
6. Final confirmation of whether secondary-source SQL rows should be excluded, included, or used only in sensitivity analysis.

