# Figure captions and manual insertion list

The figures are intentionally not embedded. Insert each file manually at the matching placeholder in `07_CACE_MANUSCRIPT_REVISED.md` and upload each final figure separately to the journal system.

## Main manuscript figures

### Figure 1

**Caption:** Overall workflow from literature-derived bio-oil compositions to Cantera simulation, inverse model training, and syngas-based soft sensing.

**Recommended source:** `C:\@biyokomurlestirme\diagram-1-ana-sistem.png`

**Alternative source:** `C:\@biyokomurlestirme\tik5\figures\tik5_figure_b03_soft_sensor_workflow.png`

### Figure 2

**Caption:** Cantera data-generation workflow, including surrogate-feed construction, operating-condition assignment, equilibrium calculation, validation, and database storage.

**Recommended source:** `C:\@biyokomurlestirme\diagram-2-cantera-simulasyon.png`

### Figure 3

**Caption:** Standard MLP architecture with eight inputs, three hidden layers, and six bio-oil composition outputs.

**Recommended source:** `C:\@biyokomurlestirme\diagram-3-mlp-mimarisi.png`

### Figure 4

**Caption:** Test-set comparison of the standard MLP, baseline models, constrained MLP, and ensemble strategies using mean R², RMSE, and MAE.

**Recommended source:** `C:\@biyokomurlestirme\diagram-6-performans-ensemble.png`

**Data-derived alternative:** `C:\@biyokomurlestirme\reverse_ml_biooil_to_product\ml_reverse_prediction\output\figures\model_comparison_r2.png`

### Figure 5

**Caption:** Random-forest feature importance for syngas measurements and reformer operating conditions.

**Recommended source:** `C:\@biyokomurlestirme\diagram-7-ozellik-onemi.png`

**Data-derived alternative:** `C:\@biyokomurlestirme\reverse_ml_biooil_to_product\ml_reverse_prediction\output\figures\feature_importance.png`

### Figure 6

**Caption:** Proposed use of the inverse soft sensor in a future monitoring and MPC workflow.

**Recommended source:** `C:\@biyokomurlestirme\diagram-5-ters-tahmin.png`

## Optional supplementary figures

- Hydrogen-production process context: `C:\@biyokomurlestirme\diagram-8-hidrojen-uretim-prosesi.png`
- Model-training workflow: `C:\@biyokomurlestirme\diagram-4-egitim-sureci.png`
- Predicted versus actual values: `C:\@biyokomurlestirme\reverse_ml_biooil_to_product\ml_reverse_prediction\output\figures\predicted_vs_actual_random_forest.png` (use only if regenerated for the standard MLP)
- Residual plot: `C:\@biyokomurlestirme\reverse_ml_biooil_to_product\ml_reverse_prediction\output\figures\residuals_random_forest.png` (use only if clearly labeled as the random-forest baseline)

## Figure preparation checks

- Replace Turkish labels with English labels before submission.
- Ensure every plotted R² value matches the TİK 4 results used in the manuscript.
- Use `Figure_1`, `Figure_2`, etc. as separate upload filenames.
- Prefer vector PDF/EPS for diagrams; use at least 300 dpi for raster plots.
- Keep fonts, class names, units, colors, and decimal precision consistent.
- Do not use the TİK 5 BiooilID R² plot in this manuscript version.
