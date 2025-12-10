# RSER Review Paper Project
## Machine Learning Applications in Biomass Pyrolysis: A Critical Review

---

## 📂 PROJECT STRUCTURE

```
RSER_Review_Paper/
│
├── 00_MASTER_PLAN.md                    ← Main planning document (START HERE)
├── README.md                             ← This file
│
├── 01_Literature_Database/
│   └── LITERATURE_EXTRACTION_TEMPLATE.md ← Template for extracting data from papers
│
├── 02_Data_Analysis/
│   └── TIK_REPORTS_DATA_EXTRACTION.md   ← Critical statistics from your TİK reports
│
├── 03_Figures/                           ← All figures will go here
│   ├── Fig1_PRISMA_diagram.png
│   ├── Fig2_Bibliometric.png
│   ├── Fig4_MissingData_Heatmap.png
│   └── Fig5_Preprocessing_Workflow.png
│
├── 04_Tables/                            ← All tables will go here
│   ├── Table1_Literature_Summary.xlsx
│   ├── Table2_MissingData_Analysis.xlsx
│   └── Table3_Imputation_Comparison.xlsx
│
├── 05_Manuscript_Drafts/                 ← Writing will happen here
│   ├── Section1_Introduction.docx
│   ├── Section2_Methodology.docx
│   └── Full_Draft_v1.docx
│
└── 06_References/                        ← Reference management
    └── RSER_Bibliography.bib
```

---

## 🎯 CURRENT STATUS

**Phase:** Planning & Data Collection
**Progress:** 20%

**Completed:**
- ✅ Master plan created
- ✅ Folder structure organized
- ✅ Data extraction from TİK reports (70 samples, 14 studies)
- ✅ Missing data statistics compiled (89.6% missing for FeedRate!)
- ✅ Literature extraction template prepared

**In Progress:**
- 🔄 Systematic literature search (AWAITING USER INPUT)

**Pending:**
- ⏳ Bibliometric analysis
- ⏳ Figure/Table generation
- ⏳ Manuscript writing

---

## 📋 NEXT STEPS

### Step 1: Literature Search Results (USER ACTION REQUIRED)
**What we need:**
- Scopus/Web of Science search results
- Approximately 60-100 papers identified
- Export as CSV or Excel with:
  - Title
  - Authors
  - Year
  - Journal
  - Abstract
  - DOI

**Search Query Recommended:**
```
("biomass pyrolysis" OR "bio-oil" OR "bio-char") AND
("machine learning" OR "artificial neural network" OR "random forest" OR
 "deep learning" OR "XGBoost" OR "support vector machine") AND
("prediction" OR "modeling" OR "optimization")
```

**Filters:**
- Year: 2015-2025
- Language: English
- Document type: Article, Review

### Step 2: Data Extraction (NEXT ACTION)
Once literature search is done:
1. Open `01_Literature_Database/LITERATURE_EXTRACTION_TEMPLATE.md`
2. Create one file per paper (e.g., `P001_Hu2023.md`)
3. Fill in all fields systematically
4. Focus on:
   - Dataset size
   - Missing data (if reported)
   - Algorithm used
   - Performance (R²)

### Step 3: Analysis
- Generate missing data heatmap
- Calculate correlations (dataset size vs R², missing data vs R²)
- Create PRISMA flow diagram

---

## 🔑 KEY INSIGHTS (So Far)

### Our Unique Contribution:
1. **Quantified Data Crisis:**
   - 89.58% missing FeedRate/ResidenceTime
   - 56.25% missing Sugar data
   - This is NOVEL - no one has quantified this systematically

2. **Imputation Framework:**
   - KNN outperforms mean imputation
   - Domain knowledge integration (O/C calculations, Duration synthesis)
   - Unified vs Segregated dataset trade-offs

3. **Performance-Data Quality Link:**
   - High R² (0.93) for LiquidOutput → low missing data
   - Negative R² for Aliphatics → high missing data + process-dominated chemistry
   - **Hypothesis:** Data completeness matters more than algorithm choice

### Why RSER Will Care:
- Addresses REAL problem (not just incremental improvement)
- Provides ACTIONABLE recommendations (reporting checklist)
- INTERDISCIPLINARY (ChemEng + Data Science)
- HIGH CITATION potential (every future ML-pyrolysis paper will cite this)

---

## 📊 TARGET METRICS

### Publication Goal:
- **Target Journal:** RSER (Impact Factor ~15-16)
- **Expected Submission:** 8-10 weeks from now
- **Article Type:** Critical Review
- **Length:** 8,000-12,000 words
- **References:** 100-150

### Quality Benchmarks:
- At least 60 papers analyzed in detail
- 5 original tables + 6 original figures
- Statistical analysis of data quality vs performance
- Novel framework/guidelines for future work

---

## 🛠️ TOOLS & RESOURCES NEEDED

### Software:
- Python (pandas, matplotlib, seaborn) for figures
- Excel / Google Sheets for tables
- Reference manager (Mendeley / Zotero / EndNote)
- Word / LaTeX for manuscript

### Data Sources:
- Scopus (for bibliometric analysis)
- Web of Science (for citation network)
- TİK reports (already extracted)
- Literature PDFs (to be collected)

### Collaboration:
- Supervisor review at each milestone
- Possible co-author contributions (TBD)

---

## ⚠️ CRITICAL SUCCESS FACTORS

### Must Have:
1. **Comprehensive literature coverage** (60+ papers)
2. **Novel quantitative analysis** (missing data statistics)
3. **Clear recommendations** (not just description)
4. **Professional figures** (publication quality)

### Must Avoid:
1. **Just listing papers** (boring review)
2. **Shallow analysis** (no critical thinking)
3. **Poor writing** (get language editing if needed)
4. **Missing deadlines** (plan 8 weeks, finish in 10)

---

## 📞 COMMUNICATION PLAN

### Weekly Milestones:
- **Week 1-2:** Literature collection + extraction
- **Week 3:** Data analysis + statistics
- **Week 4-5:** Writing (sections 3-6)
- **Week 6:** Writing (sections 1-2, 7-8)
- **Week 7:** Internal review
- **Week 8:** Final polishing + submission

### Decision Points:
- **After Week 2:** Confirm final paper list (go/no-go for 60+ papers)
- **After Week 4:** Review draft sections (quality check)
- **After Week 6:** Final decision on authorship order

---

## 📚 USEFUL REFERENCES (Already Identified)

### Must-Cite Papers (From TİK):
- Bridgwater (2012) - pyrolysis fundamentals
- Zhang et al. (2017) - bio-oil variability problem
- Aniza et al. (2022) - ML + Taguchi
- Leng et al. (2021) - ML for pyrolysis prediction
- Onsree & Tippayawong (2021) - ML for torrefaction

### Methodological Papers:
- KNN imputation: Troyanskaya et al. (2001)
- Missing data theory: Rubin (1976), Little & Rubin (2002)
- PRISMA guidelines: Page et al. (2021)

---

## 🎓 LEARNING OUTCOMES

By completing this review, you will:
1. Master systematic literature review methodology
2. Develop critical analysis skills (spotting data quality issues)
3. Learn advanced data preprocessing techniques
4. Practice scientific writing at high level (RSER standard)
5. Build reputation in ML + biomass energy community

---

## ✉️ CONTACT & SUPPORT

**Primary Author:** Orhun Uzdiyem
**Supervisor:** Prof. Dr. Hayati Olgun
**Institution:** Ege University, Solar Energy Institute

**Questions?** Add notes to this README or create issue files in project folder.

---

**Last Updated:** 2025-12-07
**Status:** Awaiting Literature Search Results
**Next Action:** User to provide Scopus/WoS search output
