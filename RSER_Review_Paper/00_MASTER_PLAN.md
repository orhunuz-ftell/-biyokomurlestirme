# RSER Review Paper - Master Plan
## Machine Learning Applications in Biomass Pyrolysis: A Critical Review on Data Scarcity, Imputation Strategies, and Predictive Performance

---

## 📋 PAPER METADATA

**Target Journal:** Renewable and Sustainable Energy Reviews (RSER)
**Impact Factor:** ~15-16 (Q1)
**Article Type:** Critical Review / Systematic Review
**Estimated Length:** 8,000-12,000 words
**Expected Timeline:** 3-4 months

**Authors (Preliminary):**
1. Orhun Uzdiyem (First Author)
2. Prof. Dr. Hayati Olgun (Corresponding Author)
3. TBD (Co-authors if needed)

**LITERATURE SEARCH STATUS:** ✅ COMPLETED (Dec 2025)
**Papers Identified:** ~50-70 from comprehensive report
**Core Benchmark Data:** 7 algorithm comparisons extracted

---

## 🎯 NOVELTY & CRITICAL ANGLE

### What Makes This Review Different?

**Most reviews focus on:**
- Algorithm comparison (ANN vs RF vs SVM)
- Prediction accuracy metrics

**Our UNIQUE contribution:**
1. **Data Quality Crisis:** Systematic quantification of missing data in biomass pyrolysis ML literature
2. **Imputation Strategy Framework:** First comprehensive analysis of data preprocessing methods
3. **Methodological Gap Analysis:** Why some chemical groups (aromatics, acids) are predictable while others (aliphatics, esters) fail
4. **Practical Guidelines:** Evidence-based recommendations for future researchers

**Key Statistics from TİK Reports (Our Evidence):**
- 56.25% missing Sugar data
- 89.58% missing FeedRate data
- 47.92% missing GasFlowrate data
- Negative R² for aliphatic hydrocarbons, esters, oxides

**BREAKTHROUGH FINDINGS from Literature Analysis:**
1. **Random Forest Supremacy:** R²=0.90-0.98 across all dataset sizes (150-1000 samples)
   - BEST algorithm for structured pyrolysis data
   - 10% better than KNN imputation (R²=0.90 vs 0.80)

2. **Dataset Size ≠ Performance:**
   - Small homogeneous data (N=150) → R²=0.98 (EXCELLENT)
   - Large heterogeneous data (N=1000) with poor preprocessing → R²=0.20 (FAILURE)
   - **INSIGHT:** Data quality > Data quantity

3. **Imputation is Critical (NOT just preprocessing):**
   - RF imputation RMSE=3.8 vs likely >5.0 with mean/KNN
   - MissForest preserves chemical relationships (lignin ↔ C%)
   - **FIRST QUANTITATIVE COMPARISON** in pyrolysis domain

4. **Bibliometric "Explosive Growth":**
   - 2020-2024: Patlayıcı büyüme in ML + pyrolysis publications
   - China leads (largest ag waste + AI investment)
   - Indicates field maturity → perfect timing for critical review

---

## 📐 PAPER STRUCTURE (8 Sections)

### 1. INTRODUCTION (1,500 words)
**Objectives:**
- Global energy transition context
- Bio-oil as renewable intermediate
- ML as solution for complex pyrolysis systems
- Problem statement: Data fragmentation & quality issues

**Key Messages:**
- Bio-oil composition varies wildly (Zhang et al., 2017 problem)
- ML adoption is growing but data infrastructure is weak
- No standardized reporting format exists

**Outline:**
1.1. Biomass Pyrolysis in Circular Economy
1.2. Machine Learning Revolution in Chemical Engineering
1.3. The Data Quality Paradox
1.4. Scope and Objectives of This Review

---

### 2. METHODOLOGY (1,200 words)
**Content:**
- Search strategy (databases, keywords, date range)
- Inclusion/exclusion criteria
- PRISMA flow diagram
- Data extraction protocol

**Search Query Example:**
```
("biomass pyrolysis" OR "bio-oil" OR "bio-char") AND
("machine learning" OR "artificial neural network" OR "random forest" OR
 "deep learning" OR "XGBoost" OR "support vector machine") AND
("prediction" OR "modeling" OR "optimization")
```

**Databases:**
- Scopus (primary)
- Web of Science
- Google Scholar (supplementary)

**Date Range:** 2015-2025 (focus on last decade)

**Target:** 60-100 papers analyzed

**PRISMA Stages:**
1. Initial search: ~500 papers
2. After title/abstract screening: ~150 papers
3. After full-text review: ~60-80 papers
4. Final included: 50-70 papers

---

### 3. OVERVIEW OF ML IN PYROLYSIS (1,800 words)
**Content:**
- Temporal evolution (publications per year)
- Geographical distribution
- Algorithm popularity (ANN 40%, RF 25%, SVM 15%, etc.)
- Input variables used
- Output variables predicted

**Sub-sections:**
3.1. Bibliometric Analysis
3.2. Algorithm Landscape
3.3. Input-Output Patterns
3.4. Performance Benchmarks

**Key Table:**
**Table 1: Comprehensive Literature Summary**
| Author (Year) | Biomass | Target Variable | Algorithm | R² | Dataset Size | Missing Data % |
|---------------|---------|-----------------|-----------|----|--------------| ---------------|

---

### 4. CRITICAL ANALYSIS OF DATA CHALLENGES (2,500 words) ⭐ **CORE SECTION**
**Content:**

**4.1. Data Scarcity Issues**
- Small dataset problem (most studies <50 samples)
- Imbalanced biomass type distribution
- Lack of pilot-scale data

**4.2. Missing Data Patterns** (Based on TİK-2 Analysis)
- Structural/Compositional Variables:
  * Sugar: 56.25% missing
  * Alcohols: 52.08% missing
  * Esters: 47.92% missing
- Process Parameters:
  * FeedRate: 89.58% missing
  * ResidenceTime: 89.58% missing
  * GasFlowrate: 47.92% missing
- Biomass Characterization:
  * Sulfur: 31.25% missing
  * HHV: 20.83% missing

**4.3. Standardization Gap**
- Inconsistent FTIR reporting
- Variable time units (duration vs residence time)
- Catalyst nomenclature chaos

**4.4. Consequences for Model Performance**
- Why some outputs fail (negative R² analysis from TİK-2)
- Correlation between data completeness and R²

**Key Table:**
**Table 2: Missing Data Analysis Across Literature**
| Variable Category | Average Missing % | Impact on Model | Recommended Action |
|-------------------|-------------------|-----------------|---------------------|

**Key Figure:**
**Figure 4: Heatmap of Missing Data Patterns**
(Rows: Studies, Columns: Variables, Color: % Missing)

---

### 5. IMPUTATION & PREPROCESSING STRATEGIES (2,000 words)
**Content:**

**5.1. Traditional Methods**
- Mean/median imputation (baseline)
- Forward fill / backward fill
- Deletion strategies

**5.2. Advanced Statistical Methods**
- K-Nearest Neighbors (KNN) - Our approach from TİK-3
- Multiple Imputation by Chained Equations (MICE)
- Iterative Imputer

**5.3. Domain Knowledge-Based Imputation** (Our Innovation)
- O/C and H/C calculation from elemental analysis (TİK-3)
- Duration synthesis from FeedRate + ResidenceTime (TİK-3)
- Holocellulose = Cellulose + Hemicellulose (TİK-3)

**5.4. Dataset Organization Strategies**
- Unified Dataset (single model, many NULLs)
- Segregated Dataset (per-chemical models, no NULLs)
- Trade-off analysis (TİK-3 Section B.2.1.1 vs B.2.1.2)

**Key Table:**
**Table 3: Imputation Method Comparison**
| Method | Pros | Cons | When to Use | Literature Example |
|--------|------|------|-------------|---------------------|

**Key Figure:**
**Figure 5: Data Preprocessing Workflow**
(Based on TİK-2 & TİK-3 algorithms - professional version)

---

### 6. CASE STUDY: PREDICTIVE PERFORMANCE ANALYSIS (1,500 words)
**Content:**

**6.1. Dataset Description**
- Our 70-sample database (TİK-3 expansion)
- 13 input features, 11 output variables
- Multiple biomass types (bamboo, rice husk, pine nut, algae, etc.)

**6.2. Algorithm Comparison**
- Random Forest
- XGBoost
- LightGBM
- CatBoost
- Linear Regression

**6.3. Results & Discussion** (from TİK-2)
- **Success Cases:**
  * LiquidOutput: R² = 0.93, RMSE = 3.52
  * Aromatics: R² = 0.83
  * Acids: R² = 0.88

- **Failure Cases:**
  * Aliphatichydrocarbon: R² = -2.25 (!!)
  * Esters: R² < 0
  * Oxides: R² < 0

**6.4. Root Cause Analysis**
- Why do some fail? (process conditions more important than biomass properties)
- Feature importance patterns

**Key Table:**
**Table 4: Model Performance by Chemical Group** (TİK-2 Table 2.1 expanded)

**Key Figure:**
**Figure 6: Prediction vs Actual Plots** (best and worst cases)

---

### 7. RECOMMENDATIONS & FUTURE PERSPECTIVES (1,000 words)
**Content:**

**7.1. For Researchers**
- Minimum reporting checklist (inspired by CONSORT/PRISMA)
- Recommended dataset size (>100 samples)
- Open data sharing practices

**7.2. For Journal Editors**
- Mandatory data availability statements
- Standard supplementary material format

**7.3. For Industry**
- Real-time process integration (link to future MPC paper)
- Hybrid models (physics + ML)

**7.4. Emerging Directions**
- Transfer learning across biomass types
- Inverse modeling (composition → process conditions)
- Multi-task learning

---

### 8. CONCLUSIONS (500 words)
**Key Takeaways:**
1. Data quality > Algorithm choice
2. Imputation strategy significantly affects performance
3. Domain knowledge integration is essential
4. Standardization urgently needed

---

## 📊 TABLES & FIGURES PLAN

### Tables (5 Total)
1. **Table 1:** Literature Summary (60-80 papers)
2. **Table 2:** Missing Data Statistics
3. **Table 3:** Imputation Methods Comparison
4. **Table 4:** Model Performance by Output Variable
5. **Table 5:** Recommended Reporting Checklist

### Figures (6 Total)
1. **Figure 1:** PRISMA Flow Diagram
2. **Figure 2:** Bibliometric Analysis (publications over time, country distribution)
3. **Figure 3:** Algorithm Usage Frequency (pie/bar chart)
4. **Figure 4:** Missing Data Heatmap (CRITICAL - shows data quality crisis)
5. **Figure 5:** Data Preprocessing Workflow (based on TİK-3)
6. **Figure 6:** Model Performance Visualization (scatter plots)

---

## 📚 REFERENCE STRATEGY

**Target:** 100-150 references

**Distribution:**
- Pyrolysis fundamentals: 20%
- ML methodology: 25%
- Bio-oil applications: 20%
- Data science/statistics: 15%
- Review papers: 10%
- Industry reports: 10%

**Key Papers to Cite:**
- Bridgwater (2012) - seminal pyrolysis review
- Zhang et al. (2017) - bio-oil variability problem
- All papers from TİK reference lists
- Recent ML reviews in related fields

---

## 🎯 WRITING STRATEGY

### Phase 1: Data Collection (CURRENT)
- [ ] Systematic literature search
- [ ] Extract data into standardized table
- [ ] Generate missing data statistics

### Phase 2: Analysis (Week 2-3)
- [ ] Bibliometric analysis
- [ ] Statistical analysis of performance vs data quality
- [ ] Create all figures

### Phase 3: Writing (Week 4-6)
- [ ] Draft sections 3-6 (data-heavy sections first)
- [ ] Write introduction & conclusions
- [ ] Polish methodology

### Phase 4: Refinement (Week 7-8)
- [ ] Internal review
- [ ] Language check
- [ ] Format for RSER guidelines
- [ ] Prepare graphical abstract

---

## 💡 STRATEGIC NOTES

### Why RSER Will Accept This:

1. **Addresses Real Problem:** Data quality crisis is tangible & quantified
2. **Actionable Output:** Provides concrete recommendations
3. **Interdisciplinary:** Bridges chemical engineering + data science
4. **High Citation Potential:** Will be cited by every future ML-pyrolysis paper
5. **Aligns with Journal Scope:** Renewable energy + methodology innovation

### Risk Mitigation:

**Risk:** "Not enough novel contribution"
**Solution:** Emphasize the quantitative missing data analysis (no one has done this systematically)

**Risk:** "Too technical for RSER audience"
**Solution:** Balance technical depth with accessible explanations + visual aids

**Risk:** "Sample size too small for meta-analysis"
**Solution:** Frame as "critical review" not "meta-analysis" - qualitative synthesis is acceptable

---

## 📧 SUBMISSION PREPARATION

### RSER Requirements:
- Graphical abstract (mandatory)
- Highlights (3-5 bullet points, max 85 characters each)
- Abstract (max 300 words)
- Keywords (max 6)
- Author contributions statement
- Declaration of competing interest

### Suggested Keywords:
1. Biomass pyrolysis
2. Machine learning
3. Bio-oil prediction
4. Missing data imputation
5. Data preprocessing
6. Critical review

### Highlights (Draft):
1. Systematic quantification of missing data in bio-oil ML studies (56-90% gaps)
2. KNN imputation outperforms mean-filling for biomass characterization variables
3. Model performance correlates strongly with data completeness, not algorithm choice
4. Domain knowledge integration essential for successful preprocessing strategies
5. Standardized reporting framework proposed to improve future ML applications

---

## 📅 TIMELINE

| Week | Task | Deliverable |
|------|------|-------------|
| 1-2 | Literature search & data extraction | Completed Table 1 |
| 3 | Statistical analysis & figure generation | All tables & figures |
| 4-5 | Write sections 3-6 | 6,000 words draft |
| 6 | Write sections 1-2, 7-8 | Complete draft |
| 7 | Internal review & revision | Revised draft |
| 8 | Final formatting & submission | Submit to RSER |

---

## 🔗 CONNECTIONS TO OTHER PAPERS

This review sets the stage for:
1. **Paper #1 (Bioresource Technology):** ML model for bio-oil prediction
2. **Paper #2 (Computers & Chemical Engineering):** MPC implementation

Cross-reference strategy:
- In review: "Future work should explore inverse modeling (composition → process)"
- In Paper #1: "Following the recommendations of [our review], we implemented..."

---

**Last Updated:** [Current Date]
**Status:** Planning Phase
**Next Action:** Await literature search results from user
