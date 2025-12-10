# Literature Data Extraction Template
## For Systematic Review on ML in Biomass Pyrolysis

---

## EXTRACTION PROTOCOL

For each paper, fill in ALL applicable fields. Use "N/A" if not reported.

---

## PAPER IDENTIFICATION

**Paper ID:** [e.g., P001]
**Citation:** [Author(s), Year, Title, Journal, Volume(Issue):Pages]
**DOI:**
**Year Published:**
**Country of Corresponding Author:**

---

## STUDY CHARACTERISTICS

### Biomass Type
- [ ] Wood (specify species: _________)
- [ ] Agricultural residue (specify: _________)
- [ ] Algae (specify: _________)
- [ ] Waste (specify: _________)
- [ ] Multiple types (list: _________)

### Pyrolysis Type
- [ ] Slow pyrolysis
- [ ] Fast pyrolysis
- [ ] Catalytic pyrolysis
- [ ] Hydrothermal liquefaction
- [ ] Other: ___________

### Temperature Range:
Min: _____ °C, Max: _____ °C

### Other Process Conditions Varied:
- [ ] Heating rate (range: _____)
- [ ] Residence time (range: _____)
- [ ] Pressure (range: _____)
- [ ] Catalyst type/loading
- [ ] Particle size
- [ ] Other: ___________

---

## MACHINE LEARNING DETAILS

### Algorithm(s) Used:
- [ ] Artificial Neural Network (ANN/MLP)
- [ ] Random Forest (RF)
- [ ] Support Vector Machine (SVM)
- [ ] XGBoost
- [ ] LightGBM
- [ ] CatBoost
- [ ] Decision Tree
- [ ] Linear Regression
- [ ] Other: ___________

### Best Performing Algorithm:
___________

### Input Variables (Features):
**Biomass Characterization:**
- [ ] Proximate analysis (VM, FC, Ash)
- [ ] Ultimate analysis (C, H, N, O, S)
- [ ] Compositional analysis (Cellulose, Hemicellulose, Lignin)
- [ ] Higher Heating Value (HHV)
- [ ] Particle size
- [ ] Moisture content

**Process Parameters:**
- [ ] Temperature
- [ ] Heating rate
- [ ] Residence time / Duration
- [ ] Pressure
- [ ] Catalyst type/loading
- [ ] Gas flow rate
- [ ] Feed rate

**Other:**
___________

### Output Variables (Targets):
**Product Yields:**
- [ ] Bio-oil yield (wt%)
- [ ] Bio-char yield (wt%)
- [ ] Gas yield (wt%)

**Bio-oil Properties:**
- [ ] HHV
- [ ] pH
- [ ] Density
- [ ] Viscosity
- [ ] Water content
- [ ] Chemical composition (FTIR, GC-MS groups)

**Bio-char Properties:**
- [ ] Carbon content
- [ ] Surface area
- [ ] Pore volume

**Other:**
___________

---

## DATASET INFORMATION

### Dataset Size:
**Total samples:** _____ (experiments)

**Training set:** _____ samples
**Validation set:** _____ samples (if applicable)
**Test set:** _____ samples

### Data Source:
- [ ] Authors' own experiments
- [ ] Literature compilation
- [ ] Public database
- [ ] Mixed

### Missing Data Reported?
- [ ] Yes - Percentage: _____%
- [ ] No
- [ ] Not mentioned

### Missing Data Handling:
- [ ] Not mentioned
- [ ] Deletion (listwise)
- [ ] Mean/median imputation
- [ ] KNN imputation
- [ ] Other: ___________

---

## DATA PREPROCESSING

### Feature Scaling:
- [ ] None
- [ ] Normalization (0-1)
- [ ] Standardization (z-score)
- [ ] Other: ___________

### Feature Selection:
- [ ] None (used all)
- [ ] Correlation analysis
- [ ] PCA
- [ ] Feature importance from model
- [ ] Other: ___________

---

## MODEL PERFORMANCE

### Best Model R²:
___________

### Other Metrics Reported:
- RMSE: _____
- MAE: _____
- MAPE: _____
- Other: _____

### Cross-validation?
- [ ] Yes (k-fold, k=_____)
- [ ] No

---

## MISSING DATA ANALYSIS (For Our Review)

### Which variables had missing data? (Manual check if not reported)
**Biomass Characterization:**
- Proximate: _____% missing
- Ultimate: _____% missing
- Compositional: _____% missing
- HHV: _____% missing

**Process Conditions:**
- Temperature: _____% missing
- Residence time: _____% missing
- Feed rate: _____% missing

**Bio-oil Composition:**
- FTIR data: _____% missing
- GC-MS data: _____% missing
- Specific chemical groups: _____

---

## CRITICAL ASSESSMENT

### Strengths:
1.
2.
3.

### Weaknesses:
1.
2.
3.

### Data Quality Score (1-5):
**1 = Very Poor, 5 = Excellent**

- Dataset size: _____ /5
- Feature completeness: _____ /5
- Reporting transparency: _____ /5
- Preprocessing rigor: _____ /5

**Overall:** _____ /5

---

## NOTES & QUOTES

**Relevant quotes for review:**
-

**Connections to other papers:**
-

**Potential for Table 1:**
- [ ] Include in main summary table
- [ ] Include in supplementary

---

## EXTRACTION METADATA

**Extracted by:** [Your name]
**Date:** [YYYY-MM-DD]
**Confidence:** [High / Medium / Low]
**Follow-up needed:** [Yes/No - what?]

---

## EXAMPLE (Pre-filled from TİK reports)

**Paper ID:** P001
**Citation:** Hu et al. (2023). Enhancement of bio-aromatics from bamboo pyrolysis: Wet torrefaction pretreatment coupled with catalytic fast pyrolysis. Journal of Analytical and Applied Pyrolysis, 169:105818.

**Biomass Type:** Bamboo
**Pyrolysis Type:** Catalytic fast pyrolysis with wet torrefaction pretreatment
**Temperature Range:** 6 different temperature/duration combinations

**Algorithm(s):** Not ML study (experimental only) - EXCLUDE from review

---

**Paper ID:** P002
**Citation:** Aniza et al. (2022). Integrating Taguchi method and artificial neural network for predicting and maximizing biofuel production via torrefaction and pyrolysis. Bioresource Technology, 343:126140.

**Biomass Type:** Not specified clearly
**Algorithm:** ANN (Artificial Neural Network)
**Dataset Size:** Not clear from TİK report
**Input Variables:** Temperature, residence time, etc. (need to check paper)
**Output:** Bio-oil yield
**Best R²:** Not reported in TİK
**Data Quality Score:** Need full text

---

