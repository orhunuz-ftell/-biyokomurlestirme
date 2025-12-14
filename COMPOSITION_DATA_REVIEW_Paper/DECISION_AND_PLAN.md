# Bio-oil Composition Data Availability Review Paper - Strategic Decision & Plan

**Date:** December 14, 2025
**Status:** Planning Phase
**Project Type:** NEW paper (separate from completed ML paper)

---

## STRATEGIC DECISION

**We are creating a SEPARATE paper focused on bio-oil composition data availability and reporting practices in pyrolysis literature.**

This is DISTINCT from the completed ML-focused review paper at:
`C:\@biyokomurlestirme\RSER_Review_Paper\RSER_Manuscript_COMPLETE.docx`

### Why This Paper Matters

**Target Audience:** ML researchers who will cite this for data collection methodology

**PhD Thesis Context:**
- PhD theme: ML-based biomass pyrolysis prediction
- This publication: Covers the data collection phase for ML training
- Relationship: Foundation work that enables the ML research

**User's Database:**
- 70 experimental samples collected from 14 studies (from TİK reports)
- Purpose: Train ML models
- Also examined additional studies beyond the 70 samples

**Available Literature:**
- 41 PDFs in `C:\@biyokomurlestirme\biyyag_ftir\` and subfolders
- These papers were reviewed during data collection process

---

## INITIAL ASSESSMENT - Publication Potential

### Evidence from Example Paper Analysis

**Paper Examined:** Hu et al. (2023) - Journal of Analytical and Applied Pyrolysis
- File: `C:\@biyokomurlestirme\biyyag_ftir\1-huEtAl.pdf`

**Key Findings:**
1. **Data Availability Statement:** "No data was used for the research described in the article"
2. **What WAS Shared:**
   - Ultimate analysis (C, H, O, N, S)
   - Proximate analysis (volatiles, fixed carbon, ash)
   - Compound-class totals (aromatics %, oxygenates %, aliphatics %)
3. **What was NOT Shared:**
   - Individual compound values (no benzene, toluene, xylene concentrations)
   - GC-MS chromatograms
   - Raw data repository (no GitHub, Zenodo, Figshare)
4. **Measurement Type:** Semi-quantitative only (a.u./mg - peak area ratios, NOT weight %)

**Conclusion:** This exemplifies the "composition data crisis" - even recent papers (2023) in reputable journals provide only shallow composition data.

### Publication Potential Assessment

**YES - This is publishable IF:**
We can demonstrate a SYSTEMATIC PATTERN across the 41 PDFs showing:
- ~80-90% of studies share only compound-class data
- Few studies share individual compound concentrations
- Minimal raw data repository usage
- Nomenclature and standardization issues

**Paper Value:**
- Documents systematic gap in composition data reporting
- Quantifies the data availability crisis
- Explains barriers to ML model development
- User's 70-sample database demonstrates manual curation effort required
- Provides roadmap for improving data sharing practices

---

## CRITICAL QUESTIONS (Must Answer Before Paper Type Decision)

### Question 1: Detail Level of Your 70 Samples
**What we need to know:**
- Do your 70 samples have individual compound data? (e.g., acetic acid wt%, phenol wt%, guaiacol wt%)
- Or only compound-class totals? (e.g., acids %, phenols %, aromatics %)
- Are measurements quantitative (wt%) or semi-quantitative (peak areas)?

**Why this matters:**
- If detailed → Can publish as "curated database paper"
- If shallow → Focus on "data availability crisis" paper

**Where to check:** TİK-2, TİK-3, TİK-4 reports referenced in RSER paper

### Question 2: How Many of 41 PDFs Share Detailed Composition?
**What we need to assess:**
- Scan 5-10 representative PDFs
- Count how many provide individual compound data
- Estimate percentage with different data detail levels

**Data Detail Levels:**
- Level 1: Bio-oil yield only (no composition)
- Level 2: Compound-class totals (aromatics %, acids %)
- Level 3: Individual compounds (acetic acid, phenol, guaiacol)
- Level 4: Full GC-MS chromatogram sharing

### Question 3: Source of Your 70 Samples
**Clarification needed:**
- Are these YOUR OWN experimental results?
- Or extracted from literature (manual curation)?
- Or a mix of both?

**Why this matters:**
- Own experiments → Stronger contribution (new data generated)
- Literature extraction → Still valuable (demonstrates curation difficulty)

---

## THREE POTENTIAL PAPER SCENARIOS

### Scenario A: Data Availability Crisis Review Paper
**IF:** Most PDFs (>70%) share only shallow data (Level 1-2)

**Paper Type:** Critical review / perspective paper

**Main Message:** "The biomass pyrolysis field has a composition data crisis that blocks ML advancement"

**Structure:**
1. Introduction: ML needs detailed composition data
2. Systematic Assessment: Survey of 41 papers showing data gaps
3. Barriers Analysis: Why researchers don't share (analytical cost, no incentive, no standards)
4. Case Study: User's 70-sample database as example of manual curation needed
5. Recommendations: Data sharing standards, repository usage, incentives

**Target Journals:**
- Renewable and Sustainable Energy Reviews (RSER)
- Energy & Fuels
- Journal of Analytical and Applied Pyrolysis

**Estimated Impact:** High (addresses field-wide problem)

### Scenario B: Curated Database Paper
**IF:** User's 70 samples have detailed individual compound data (Level 3-4)

**Paper Type:** Data paper / resource paper

**Main Message:** "We provide the first curated, standardized bio-oil composition database for ML training"

**Structure:**
1. Introduction: Need for standardized databases
2. Database Construction: 70 samples from 14 studies, curation methodology
3. Data Description: Variables, coverage, quality control
4. Validation: ML model trained on database as proof-of-concept
5. Data Availability: Full dataset on Zenodo/Figshare with DOI

**Target Journals:**
- Scientific Data (Nature)
- Data in Brief (Elsevier)
- Bioresource Technology Reports

**Estimated Impact:** Very high (reusable dataset, high citation potential)

### Scenario C: Hybrid Approach (RECOMMENDED)
**Paper Type:** Review + Database

**Main Message:** "We document the composition data crisis AND provide a solution via curated database"

**Structure:**
1. Introduction: ML potential limited by data availability
2. Systematic Gap Analysis: Assessment of 41 papers (80%+ shallow data)
3. Database Construction: Our solution - 70-sample curated dataset
4. Nomenclature Standardization: How we addressed naming inconsistencies
5. ML Demonstration: Models trained on our database
6. Recommendations: Field-wide data sharing standards

**Target Journals:**
- Fuel (Q1, IF~7)
- Energy Conversion and Management (Q1, IF~10)
- Bioresource Technology (Q1, IF~11)

**Estimated Impact:** Highest (problem + solution, addresses urgent need)

**Why this is RECOMMENDED:**
- Combines critical analysis with constructive contribution
- Stronger than crisis-only paper (not just complaining)
- More impactful than database-only paper (provides context)
- User has BOTH components (41 PDFs for review + 70 samples for database)

---

## RELATIONSHIP TO COMPLETED ML PAPER

**ML Paper (already complete):**
- File: `C:\@biyokomurlestirme\RSER_Review_Paper\RSER_Manuscript_COMPLETE.docx`
- Focus: ML algorithms, missing data imputation, model performance
- Word count: ~10,300 words
- Status: Ready for internal review → submission

**Composition Data Paper (this project):**
- Focus: Bio-oil composition data availability, curation, standardization
- Relationship: Upstream problem that ML paper addresses downstream
- Citation strategy: ML paper can cite this paper for "data challenges" context

**Publishing Order:**
- Option 1: Submit both simultaneously to different journals (no conflict)
- Option 2: Submit composition paper first (3-6 months), cite it in ML paper revision
- Option 3: Submit ML paper first, reference composition paper as "in preparation"

**No Content Overlap:** ML paper focuses on algorithmic solutions; composition paper focuses on data availability problem. Complementary, not redundant.

---

## NEXT STEPS (Phases)

### Phase 1: PDF Scanning & Assessment (1-2 days)
**Goal:** Determine typical data detail level across literature

**Tasks:**
1. Scan 10 representative PDFs from `biyyag_ftir` folder
2. For each, record:
   - Data detail level (1-4 scale)
   - Individual compounds reported (if any)
   - Data availability statement
   - Measurement type (quantitative vs semi-quantitative)
3. Calculate percentages for each level
4. Identify best-case examples (if any share Level 3-4 data)

**Deliverable:** Data assessment spreadsheet

### Phase 2: Your 70-Sample Database Review (1 day)
**Goal:** Understand detail level of user's curated dataset

**Tasks:**
1. Review TİK-2, TİK-3, TİK-4 reports
2. Document variables in your 70-sample database:
   - Compound-class totals? (acids %, phenols %)
   - Individual compounds? (acetic acid, guaiacol)
   - Quantitative measurements? (wt%)
3. Count samples with complete composition data
4. Identify gaps/missingness patterns

**Deliverable:** Database description document

### Phase 3: Paper Type Decision (1 day)
**Goal:** Choose Scenario A, B, or C based on Phase 1-2 findings

**Decision Matrix:**
| Your 70 Samples | Literature (41 PDFs) | Recommended Scenario |
|-----------------|---------------------|---------------------|
| Detailed (Level 3-4) | Mostly shallow (<30% detailed) | C - Hybrid (BEST) |
| Detailed (Level 3-4) | Mixed (30-70% detailed) | B - Database |
| Shallow (Level 1-2) | Mostly shallow (<30% detailed) | A - Crisis Review |

### Phase 4: Paper Structure & Outline (2-3 days)
**Goal:** Create detailed manuscript outline

**Tasks:**
1. Define sections (Introduction, Methods, Results, Discussion, Recommendations)
2. Allocate word counts (target: 6,000-8,000 words)
3. Plan figures:
   - Data availability heatmap (41 PDFs × data detail levels)
   - Nomenclature inconsistency examples
   - Database coverage diagram (if Scenario B/C)
4. Plan tables:
   - Systematic assessment of 41 papers
   - Database schema (if Scenario B/C)

### Phase 5: Writing & Figure Creation (1-2 weeks)
**Goal:** Complete first draft

**Timeline depends on:** Scenario chosen, database complexity, figure requirements

---

## DATA SOURCES

### Literature PDFs (41 papers)
**Location:** `C:\@biyokomurlestirme\biyyag_ftir\` + subfolders
**Purpose:**
- Systematic assessment of data sharing practices
- Identify nomenclature inconsistencies
- Benchmark your database against literature

**Analysis Required:**
- Full read: 10-15 papers (representative sample)
- Quick scan: All 41 (data availability, composition detail level)

### Your 70-Sample Database
**Source:** 14 studies (from TİK reports)
**Purpose:**
- ML model training data
- Example of curated database (if detailed)
- Case study of manual curation effort (if extracted from literature)

**Need to Determine:**
- Origin: Own experiments vs literature extraction?
- Detail level: Compound-class vs individual compounds?
- Completeness: % samples with full composition data?

### TİK Reports (Reference)
**Files:** TİK-2, TİK-3, TİK-4 (mentioned in RSER paper)
**Purpose:**
- Detailed documentation of your database
- Methodology for data extraction
- Statistical analysis already performed

---

## SUCCESS CRITERIA

**This paper will be considered successful if:**

1. **Novel Contribution:** First systematic assessment of bio-oil composition data availability in literature
2. **Quantitative Evidence:** >70% of studies share only shallow data (Level 1-2)
3. **Practical Impact:** Database enables ML researchers to train models (if Scenario B/C)
4. **Field Standards:** Recommendations lead to improved data sharing practices
5. **High Citation Potential:** Every future ML-pyrolysis paper cites this for data challenges/solutions

**Target Journal Metrics:**
- Q1 journal (top 25% in Energy or Chemical Engineering)
- Impact Factor > 7
- Acceptance rate: 25-35%

**Realistic Timeline:**
- Draft completion: 2-3 weeks
- Internal review: 1 week
- Submission: Early January 2026
- Review process: 2-3 months
- Publication: Mid-2026

---

## RISKS & MITIGATION

### Risk 1: Your 70 Samples Have Only Shallow Data
**Impact:** Cannot do Scenario B (database paper)
**Mitigation:** Focus on Scenario A (crisis review) - still highly publishable
**Probability:** Medium (need to check TİK reports)

### Risk 2: Many PDFs Actually Share Detailed Data
**Impact:** "Crisis" narrative weakens
**Mitigation:** Pivot to "standardization problem" - even if data exists, it's not reusable due to nomenclature issues
**Probability:** Low (Hu et al. example suggests crisis is real)

### Risk 3: Overlap with Existing Reviews
**Impact:** Reviewers cite similar prior work
**Mitigation:** Search literature for existing composition data reviews (likely none exist - this is novel angle)
**Action:** Perform literature search before Phase 4

### Risk 4: 41 PDFs Too Small Sample
**Impact:** Reviewers request larger systematic review
**Mitigation:**
- Justify sample size (representative of your database sources)
- OR expand to 70-100 papers if needed (feasible, just takes time)
**Probability:** Medium

---

## FINAL RECOMMENDATION

**Proceed with Scenario C (Hybrid Approach) planning by default:**
- Most flexible: Adapts to findings from Phase 1-2
- Highest impact: Problem + solution
- Uses all available resources: 41 PDFs + 70 samples

**Immediate next action when continuing:**
Start Phase 1 (scan 10 PDFs to assess data detail levels)

**This paper has strong publication potential** because:
1. Novel angle (no prior composition data availability reviews)
2. Urgent problem (blocks ML advancement)
3. Quantitative evidence (systematic assessment)
4. Practical contribution (database or recommendations)
5. User has all necessary resources (PDFs + samples)

---

**Status:** READY TO BEGIN PHASE 1 when you return to this project

**Last Updated:** December 14, 2025
