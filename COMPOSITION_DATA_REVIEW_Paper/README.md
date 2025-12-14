# Bio-oil Composition Data Availability Review Paper

**Project Start Date:** December 14, 2025
**Current Status:** Planning Phase
**Target Completion:** Mid-January 2026

---

## Project Overview

This project aims to create a **separate, standalone paper** focused on bio-oil composition data availability and reporting practices in biomass pyrolysis literature. This is **distinct from** the already-completed ML-focused review paper.

### Main Research Question

**"How extensively is detailed bio-oil composition data shared in the pyrolysis literature, and what barriers prevent effective data integration for machine learning applications?"**

### Key Objectives

1. **Systematic Assessment:** Survey 41 biomass pyrolysis papers to quantify composition data detail levels
2. **Gap Identification:** Document the extent of the "composition data crisis" (lack of individual compound data)
3. **Database Contribution:** Showcase our curated 70-sample database as an example or solution
4. **Recommendations:** Propose data sharing standards and best practices for the field

---

## Project Background

### PhD Research Context

- **PhD Theme:** Machine learning-based prediction of biomass pyrolysis products
- **This Paper's Role:** Documents the data collection phase necessary for ML model training
- **Target Audience:** ML researchers who will cite this for data collection methodology

### Why This Paper Matters

**Problem:** Most pyrolysis papers report only shallow composition data (compound-class totals like "aromatics 25%") rather than detailed individual compound concentrations (e.g., "benzene 5.2 wt%, toluene 3.8 wt%"). This prevents:
- Training robust ML models
- Cross-study data integration
- Reproducible research
- Industrial deployment of ML-guided optimization

**Our Contribution:**
- First systematic quantification of this data availability crisis
- Demonstration via our own 70-sample curated database
- Actionable recommendations for improving field practices

---

## Relationship to Completed ML Paper

### ML Paper (Already Complete)
- **Location:** `C:\@biyokomurlestirme\RSER_Review_Paper\`
- **File:** `RSER_Manuscript_COMPLETE.docx`
- **Focus:** ML algorithms, missing data imputation strategies, model performance analysis
- **Status:** Ready for internal review → submission to RSER

### Composition Data Paper (This Project)
- **Location:** `C:\@biyokomurlestirme\COMPOSITION_DATA_REVIEW_Paper\` (this folder)
- **Focus:** Bio-oil composition data availability, curation challenges, standardization issues
- **Status:** Planning phase (see TODO.txt for action plan)

### Key Differences
| Aspect | ML Paper | Composition Data Paper |
|--------|----------|------------------------|
| **Main Topic** | How to build ML models despite missing data | Why composition data is missing/shallow |
| **Contribution** | Algorithmic solutions (imputation, validation) | Data curation methodology + database |
| **Scope** | 70 studies on ML algorithms | 41 studies on data sharing practices |
| **Target Journals** | RSER, Bioresource Technology | Fuel, Energy Conv. Mgmt., Scientific Data |
| **Submission Timeline** | January 2026 | January-February 2026 |

**No Content Overlap:** These are complementary papers. ML paper addresses downstream solutions; composition paper addresses upstream problem.

---

## Data Sources

### 1. Literature Database (41 PDFs)
- **Location:** `C:\@biyokomurlestirme\biyyag_ftir\` and subfolders
- **Content:** Biomass pyrolysis papers collected during user's research
- **Purpose:** Systematic assessment of composition data detail levels

**Example Paper:** Hu et al. (2023) - `1-huEtAl.pdf`
- Shares: Compound-class totals (aromatics %, acids %)
- Does NOT share: Individual compounds, GC-MS chromatograms, raw data
- Data availability: "No data was used for the research described in the article"
- **This exemplifies the problem we're documenting**

### 2. Our Curated Database (70 Samples)
- **Source:** 14 studies (from TİK experimental reports)
- **Purpose:** ML model training data (collected for PhD research)
- **Status:** Need to assess detail level (see Phase 2 in TODO.txt)
- **Potential Use:** Either as case study (demonstrates curation difficulty) or as deliverable (published database)

### 3. TİK Reports (Reference)
- **Files:** TİK-2, TİK-3, TİK-4 (referenced in completed ML paper)
- **Content:** Detailed experimental data and analysis from user's research group
- **Purpose:** Source documentation for our 70-sample database

---

## Three Potential Paper Scenarios

The final paper type will be determined after Phase 1-2 analysis (see DECISION_AND_PLAN.md for details):

### Scenario A: Data Availability Crisis Review
**If:** Most literature (>70%) shares only shallow data

**Paper Type:** Critical review / perspective

**Main Message:** "Biomass pyrolysis has a composition data crisis blocking ML advancement"

**Target Journals:** RSER, Energy & Fuels

---

### Scenario B: Curated Database Paper
**If:** Our 70 samples have detailed individual compound data

**Paper Type:** Data paper / resource paper

**Main Message:** "We provide the first standardized bio-oil composition database for ML training"

**Target Journals:** Scientific Data, Data in Brief

---

### Scenario C: Hybrid Approach ⭐ (RECOMMENDED)
**Paper Type:** Review + Database

**Main Message:** "We document the composition data crisis AND provide a solution via curated database"

**Target Journals:** Fuel, Energy Conversion & Management, Bioresource Technology

**Why Recommended:**
- Combines problem identification with constructive solution
- Highest impact (addresses urgent need + provides reusable resource)
- User has BOTH components (41 PDFs for review + 70 samples for database)

---

## Project Structure

```
COMPOSITION_DATA_REVIEW_Paper/
│
├── README.md                    ← You are here (project overview)
├── DECISION_AND_PLAN.md         ← Strategic decision + assessment + scenarios
├── TODO.txt                     ← Detailed action plan (6 phases)
│
├── 01_Literature_Assessment/    ← To be created in Phase 1
│   ├── PDF_SELECTION.md
│   └── LITERATURE_DATA_ASSESSMENT.xlsx
│
├── 02_Database_Documentation/   ← To be created in Phase 2
│   └── DATABASE_SCHEMA.md
│
├── 03_Manuscript_Drafts/        ← To be created in Phase 5
│   ├── Section1_Introduction.md
│   ├── Section2_Methods.md
│   ├── Section3_Results.md
│   └── [other sections...]
│
├── 04_Figures/                  ← To be created in Phase 5
│   ├── Figure1_Data_Availability_Landscape.png
│   └── [other figures...]
│
├── 05_Tables/                   ← To be created in Phase 5
│   ├── Table1_Literature_Assessment.xlsx
│   └── [other tables...]
│
├── 06_References/               ← To be created in Phase 4
│   └── REFERENCES.bib
│
└── MANUSCRIPT_DRAFT_v1.docx     ← Final deliverable (Phase 5)
```

---

## Workflow Phases

### ✅ Planning Phase (CURRENT)
- [x] Create project folder structure
- [x] Document strategic decision (DECISION_AND_PLAN.md)
- [x] Create action plan (TODO.txt)
- [x] Write project overview (README.md)

### 📋 Phase 1: PDF Scanning (Next, 1-2 days)
- [ ] Select 10 representative PDFs for detailed analysis
- [ ] Scan all 41 PDFs for data detail levels
- [ ] Calculate statistics (% at each detail level)
- [ ] Identify best/worst examples

### 📋 Phase 2: Database Review (1 day)
- [ ] Review TİK reports
- [ ] Document database schema
- [ ] Assess data detail level of 70 samples
- [ ] Clarify data source (own experiments vs literature extraction)

### 📋 Phase 3: Paper Type Decision (0.5 days)
- [ ] Review Phase 1-2 findings
- [ ] Choose Scenario A, B, or C
- [ ] Finalize target journal

### 📋 Phase 4: Manuscript Outline (2-3 days)
- [ ] Define section structure
- [ ] Plan figures (3-5)
- [ ] Plan tables (2-4)
- [ ] Write detailed outline
- [ ] Literature search for existing work

### 📋 Phase 5: Writing & Figures (1-2 weeks)
- [ ] Write all sections (~6,000-8,000 words)
- [ ] Create publication-quality figures
- [ ] Create formatted tables
- [ ] Compile full manuscript

### 📋 Phase 6: Review & Revision (1 week)
- [ ] Self-review
- [ ] Supervisor review (Prof. Olgun)
- [ ] Address feedback
- [ ] Format for target journal
- [ ] Prepare submission package

**Total Timeline:** 3-4 weeks → Target submission mid-January 2026

---

## Key Files

### Strategic Documents
- **DECISION_AND_PLAN.md** - Full strategic analysis, publication potential assessment, three scenarios explained
- **TODO.txt** - Detailed checklist of all tasks organized by phase
- **README.md** - This file (project overview and navigation)

### To Be Created
- **SCENARIO_DECISION.md** - Documents final scenario choice (after Phase 3)
- **MANUSCRIPT_OUTLINE.md** - Detailed section-by-section outline (Phase 4)
- **MANUSCRIPT_DRAFT_v1.docx** - Complete first draft (Phase 5)

---

## Success Criteria

This paper will be considered successful if:

1. ✅ **Novel Contribution:** First systematic assessment of bio-oil composition data availability
2. ✅ **Quantitative Evidence:** Clear statistical documentation of data gaps (target: >70% shallow data)
3. ✅ **Practical Impact:** Database or recommendations that improve field practices
4. ✅ **Publication Quality:** Accepted to Q1 journal (IF > 7)
5. ✅ **Citation Potential:** Becomes standard reference for data challenges in pyrolysis ML

---

## Critical Questions to Answer

Before finalizing paper type, we must determine:

### Question 1: Literature Data Detail Level
**From 41 PDFs, what % share:**
- Level 1: Bio-oil yield only (no composition) → ____%
- Level 2: Compound-class totals (aromatics %, acids %) → ____%
- Level 3: Individual compounds (acetic acid wt%, phenol wt%) → ____%
- Level 4: Full GC-MS chromatogram sharing → ____%

**Answer in:** Phase 1

---

### Question 2: Your Database Detail Level
**Do your 70 samples have:**
- Compound-class totals only? → Yes / No
- Individual compounds? → Yes / No
- If yes, how many compounds? → _____
- Quantitative (wt%) or semi-quantitative (peak area)? → _____

**Answer in:** Phase 2

---

### Question 3: Data Source Clarification
**Your 70 samples are from:**
- Your OWN experiments? → _____ samples
- Literature extraction? → _____ samples
- From which papers/studies? → _____

**Answer in:** Phase 2

---

## Next Actions

**When continuing work on this project:**

1. **Read these files first:**
   - README.md (this file) - for overview
   - DECISION_AND_PLAN.md - for strategic context
   - TODO.txt - for detailed task list

2. **Start Phase 1:**
   - Select 10 representative PDFs from `C:\@biyokomurlestirme\biyyag_ftir\`
   - Create `01_Literature_Assessment/` folder
   - Create `LITERATURE_DATA_ASSESSMENT.xlsx` template
   - Begin scanning PDFs

3. **Ask if needed:**
   - Any questions about the 70-sample database
   - Preferences on paper scenario (A/B/C)
   - Target journal preferences

---

## Contact & Collaboration

**Primary Author:** Orhun Uzdiyem
**Affiliation:** Solar Energy Institute, Ege University
**Supervisor:** Prof. Dr. Hayati Olgun

**Related Work:**
- ML Review Paper: `C:\@biyokomurlestirme\RSER_Review_Paper\RSER_Manuscript_COMPLETE.docx`

---

## References & Resources

**GC-MS Data Sharing Best Practices:**
- FAIR principles (Findable, Accessible, Interoperable, Reusable)
- Scientific Data journal guidelines
- Zenodo, Figshare repository standards

**Similar Data Availability Studies in Other Fields:**
- Genomics: GenBank, NCBI standards
- Chemistry: ChemSpider, PubChem practices
- Materials science: Materials Project

**Target Journal Author Guidelines:**
- Fuel: [https://www.elsevier.com/journals/fuel](https://www.elsevier.com/journals/fuel)
- Energy Conversion and Management: [https://www.elsevier.com/journals/energy-conversion-and-management](https://www.elsevier.com/journals/energy-conversion-and-management)
- Scientific Data: [https://www.nature.com/sdata/](https://www.nature.com/sdata/)

---

**Last Updated:** December 14, 2025
**Project Status:** Planning Complete → Ready for Phase 1 execution
**Estimated Completion:** Mid-January 2026

---

## Quick Start Guide

**If this is your first time returning to this project:**

1. Read this README (5 minutes)
2. Skim DECISION_AND_PLAN.md for strategic context (10 minutes)
3. Open TODO.txt and start Phase 1, Task 1.1 (5 minutes setup)
4. Begin analyzing PDFs!

**Total time to get started:** ~20 minutes

---

**🎯 This project has strong publication potential. All necessary resources are available. Let's document the composition data crisis and provide a solution for the field!**
