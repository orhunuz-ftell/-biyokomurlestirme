# Data Extraction from TİK Reports
## Critical Statistics for RSER Review Paper

---

## SOURCE DOCUMENTS
- TİK-1 (OrhunUzdiyem_tik1.pdf)
- TİK-2 (OrhunUzdiyem_tik2.pdf)
- TİK-3 (OrhunUzdiyem_tik3.pdf)

---

## SECTION 1: DATABASE OVERVIEW (From TİK-1 & TİK-3)

### Initial Database (TİK-1)
**Total studies analyzed:** 7
**Total experimental data points:** 48

**Sources:**
1. Hu et al. (2023) - Bamboo, 18 experiments
2. Zhang et al. (2017) - Rice husk, 5 experiments
3. Hwang et al. (2013) - Yellow poplar wood, 5 experiments
4. Chen et al. (2016) - Pine nut shells, 4 experiments
5. Chen et al. (2017) - Cotton stalks, 4 experiments
6. Wang et al. (2018) - Corn cob lignin, 5 experiments
7. Cao et al. (2021) - Enteromorpha clathrata (green algae), 7 experiments

### Expanded Database (TİK-3)
**Total studies:** 7 + 7 new = 14
**Total experimental data points:** 48 + 22 = 70

**New sources added:**
1. Modak et al. (2023) - Mixed cooked food waste, 3 experiments
2. Bordoloi et al. (2016) - Scenedesmus dimorphus (microalgae), 1 experiment
3. Sukiran et al. (2009) - Oil palm EFB, 1 experiment
4. Mullen et al. (2010) - Barley biomass (3 types), 3 experiments
5. Chukwuneke et al. (2019) - Swietenia macrophylla (mahogany), 1 experiment
6. Khor et al. (2009) - Oil palm EFB fibers, 1 experiment
7. Sampaio et al. (2025) - Review paper covering 14 different biomass types

**Biomass diversity:**
- Woods: Bamboo, Yellow poplar, Mahogany
- Agricultural residues: Rice husk, Cotton stalks, Corn cob, Barley
- Algae: Enteromorpha, Scenedesmus
- Wastes: Food waste, Oil palm EFB
- Seeds: Pine nut shells

---

## SECTION 2: MISSING DATA STATISTICS (From TİK-2, Pages 3-4)

### 2.1 Complete Variables (0% Missing)
**Biomass Characterization:**
- Carbon (C)
- Hydrogen (H)
- Nitrogen (N)
- Oxygen (O)

**Process Parameters:**
- ProcessTemperature
- CatalystBiomassRatio

### 2.2 Partially Missing Variables

**HIGHEST PRIORITY (>80% missing) - CRITICAL FINDING:**
| Variable | Missing % | Missing Count | Total Count |
|----------|-----------|---------------|-------------|
| FeedRate | 89.58% | 43/48 | 48 |
| ResidenceTime | 89.58% | 43/48 | 48 |

**HIGH PRIORITY (40-60% missing):**
| Variable | Missing % | Missing Count | Total Count |
|----------|-----------|---------------|-------------|
| Sugar | 56.25% | 27/48 | 48 |
| Alcohols | 52.08% | 25/48 | 48 |
| Oxides | 52.08% | 25/48 | 48 |
| Esters | 47.92% | 23/48 | 48 |
| Aliphatichydrocarbon | 47.92% | 23/48 | 48 |
| GasFlowrate | 47.92% | 23/48 | 48 |

**MEDIUM PRIORITY (20-40% missing):**
| Variable | Missing % | Missing Count | Total Count |
|----------|-----------|---------------|-------------|
| LiquidOutput (Sıvı Ürün Verimi) | 37.50% | 18/48 | 48 |
| Sulfur (S) | 31.25% | 15/48 | 48 |
| Aromatics | 29.17% | 14/48 | 48 |
| Furans | 22.92% | 11/48 | 48 |
| HHV (Yüksek Isıl Değer) | 20.83% | 10/48 | 48 |

**LOW PRIORITY (10-20% missing):**
| Variable | Missing % | Missing Count | Total Count |
|----------|-----------|---------------|-------------|
| Volatiles (Uçucu Madde) | 10.42% | 5/48 | 48 |
| FixedCarbon (Sabit Karbon) | 10.42% | 5/48 | 48 |
| Aldehyde_ketone | 10.42% | 5/48 | 48 |

---

## SECTION 3: DATA IMPUTATION STRATEGIES (From TİK-3)

### 3.1 Calculation-Based Imputation
**Innovation from our work:**

1. **O/C and H/C Ratios**
   - Source: TİK-3, Page 4, Section B.2.1
   - Method: Calculated from C, H, O elemental percentages
   - Success rate: 100% (no missing C, H, O)

2. **Holocellulose Synthesis**
   - Source: TİK-3, Page 4
   - Formula: Holocellulose = Cellulose + Hemicellulose
   - Used for missing holocellulose values

3. **Duration/ResidenceTime Unified Variable**
   - Source: TİK-3, Pages 5-6, Section B.2.1.2
   - Innovation: Merged batch (Duration) and continuous (ResidenceTime) into one variable
   - Formula: Duration = (Total_Biomass / FeedRate) + ResidenceTime
   - Impact: Reduced 89.58% missing rate significantly

### 3.2 KNN Imputation Strategy
**Variables imputed with KNN:**

1. **Volatiles, FixedCarbon, Lignin**
   - Predictor variables: O/C, H/C, S, Ash
   - Reason: Strong correlation with elemental composition

2. **HHV (Higher Heating Value)**
   - Predictor variables: O/C, H/C, S, Ash, Holocellulose, Lignin
   - Reason: HHV strongly depends on elemental and structural composition

3. **Cellulose and Hemicellulose**
   - Predictor variables: O/C, H/C, S, Ash, HHV
   - Post-processing: Scaled to match Holocellulose if available
   - Innovation: Constraint-based imputation

### 3.3 Mean Imputation
**Variables imputed with mean:**
- Nitrogen (N) - only for few missing cases
- Justification: Low variance, low impact on model

---

## SECTION 4: MODEL PERFORMANCE RESULTS (From TİK-2, Pages 9-10)

### 4.1 HIGH PERFORMANCE (R² > 0.8)
| Output Variable | R² | RMSE | Key Predictor |
|-----------------|-----|------|---------------|
| LiquidOutput (Sıvı Ürün) | 0.93 | 3.52 | Volatiles (Uçucu madde) |
| Acids (Asitler) | 0.88 | 5.24 | Nitrogen (Azot) |
| Aromatics (Aromatikler) | 0.83 | 8.09 | Nitrogen (Azot) |
| Aldehyde_ketone | 0.81 | 1.73 | GasFlowrate |

**Insight:** High R² correlates with low missing data + strong chemical logic

### 4.2 MEDIUM PERFORMANCE (0.4 < R² < 0.8)
| Output Variable | R² | RMSE | Key Predictor |
|-----------------|-----|------|---------------|
| Phenols (Fenoller) | 0.56 | 7.00 | CatalystBiomassRatio |
| Furans | 0.46 | - | Nitrogen (Azot) |
| Alcohols (Alkoller) | 0.17 | - | Volatiles |

### 4.3 FAILURE CASES (R² < 0 or Negative)
| Output Variable | R² | RMSE | Comment |
|-----------------|-----|------|---------|
| Aliphatichydrocarbon | -2.25 | - | WORSE than predicting mean! |
| Esters | <0 | - | Model completely failed |
| Oxides | <0 | - | Model completely failed |
| Sugars | <0 | - | Model completely failed |

**Critical Analysis (TİK-2, Page 10):**
> "Bu bileşen grupları için negatif R² değerleri elde edilmiştir. Bu durum, modelin bu bileşenlerin davranışını açıklamakta zorlandığını göstermektedir."

**Root Cause Hypothesis:**
- Process conditions (temperature, catalyst) more important than biomass properties
- High missing data (47-56%) disrupts learning
- Complex chemical kinetics not captured by simple features

---

## SECTION 5: ALGORITHM COMPARISON (From TİK-3, Pages 5-8)

### Algorithms Tested:
1. Random Forest (RF)
2. XGBoost
3. LightGBM
4. CatBoost
5. Linear Regression (baseline)

### Comparative Strengths:
| Algorithm | Complexity Capture | Speed | Interpretability | Overfitting Risk |
|-----------|-------------------|-------|------------------|------------------|
| Random Forest | Medium | Fast | Medium | Low |
| XGBoost | Very High | Medium | Medium-Low | Medium |
| LightGBM | Very High | Very Fast | Low | Medium-High |
| CatBoost | Very High | Fast | Low | Low |
| Linear Reg | Low | Very Fast | Very High | Very Low |

**Best Overall:** XGBoost and CatBoost (heterogeneous data)
**Best for Small Data:** Random Forest (robust, less overfitting)
**Worst:** Linear Regression (cannot capture non-linearity)

---

## SECTION 6: DATASET ORGANIZATION STRATEGIES (From TİK-3)

### Strategy 1: Unified Dataset
**Approach:** All data in one table, NULL values kept
**Pros:**
- Maximum sample size for each model
- Can leverage correlations across chemical groups

**Cons:**
- Many NULL values (56-89% for some variables)
- Model performance degraded

### Strategy 2: Segregated Dataset
**Approach:** Separate dataset per chemical group, NULL rows removed
**Pros:**
- Clean data, no NULL contamination
- Each model trained on relevant samples only

**Cons:**
- Smaller sample size per model
- Risk: Chemical groups trained independently may not sum to 100%

**TİK-3 Conclusion (Page 5):**
> "Bu yaklaşımda makine öğrenmesi daha az sayıdı örnek içeren verisetleriyle yapılmak zorunda kalınmıştır."

---

## SECTION 7: KEY STATISTICS FOR PAPER

### For Abstract:
- "Database of 70 experimental conditions from 14 studies"
- "Missing data ranging from 10% to 90% across variables"
- "KNN imputation improved R² by X% compared to mean imputation" [NEED TO CALCULATE]

### For Results:
- "89.58% of studies did not report FeedRate or ResidenceTime"
- "Negative R² observed for 4 out of 11 chemical groups"
- "Strong correlation (r=0.XX) between data completeness and model R²" [NEED TO CALCULATE]

### For Discussion:
- "Process-dominated outputs (aliphatics, esters) failed due to inadequate process feature representation, not biomass characterization"

---

## SECTION 8: FIGURES TO CREATE

### Figure 4: Missing Data Heatmap
**Data Source:** TİK-2, Section B.2.1.1, Pages 3-4

**Visualization:**
- Rows: 11 chemical output variables
- Columns: 13 input variables + 11 output variables
- Color scale: 0% (green) → 100% (red)
- Annotations: Percentage values in cells

**Python Pseudocode:**
```python
import seaborn as sns
import pandas as pd

# Data from TİK-2 Table
missing_data = {
    'Sugar': 56.25,
    'Alcohols': 52.08,
    'Oxides': 52.08,
    'Esters': 47.92,
    'Aliphatichydrocarbon': 47.92,
    'GasFlowrate': 47.92,
    # ... etc
}

# Create heatmap
sns.heatmap(data, annot=True, cmap='RdYlGn_r', vmin=0, vmax=100)
```

### Figure 5: Data Preprocessing Workflow
**Data Source:** TİK-2 & TİK-3 Algorithms

**Components:**
1. Raw Data Input (SQL Server)
2. Missing Value Detection
3. Imputation Strategy Selection:
   - Branch A: Calculation (O/C, H/C, Duration)
   - Branch B: KNN (Volatiles, HHV, Cellulose)
   - Branch C: Mean (Nitrogen)
4. Standardization (StandardScaler)
5. Train-Test Split (80-20)
6. Output: Clean Dataset

---

## SECTION 9: QUOTES FOR DIRECT USE

### From TİK-2 (Critical Analysis):
**Page 3:**
> "Veritabanından çekilen ham verilerde önemli miktarda eksik veri tespit edildi."

**English translation for paper:**
> "Significant amounts of missing data were detected in the raw dataset extracted from literature."

**Page 4:**
> "FeedRate ve ResidenceTime değişkenlerinde gözlemlenen yüksek eksik veri oranı (%89.6), bu değişkenlerin doğrudan kullanımını oldukça zorlaştırıyordu."

**English:**
> "The high missing data rate (89.6%) observed in FeedRate and ResidenceTime variables severely hindered their direct utilization."

**Page 10:**
> "Bu bileşenlerin oluşumunda reaksiyon koşullarının biyokütle özelliklerinden daha etkili olabileceğini düşündürmektedir."

**English:**
> "This suggests that reaction conditions may be more influential than biomass properties in the formation of these chemical groups."

### From TİK-3 (Methodology Innovation):
**Page 6:**
> "Değişkenler arasındaki ilişkiyi korumak ve veri kaybını minimize etmek için aşağıdaki strateji uygulandı."

**English:**
> "The following strategy was implemented to preserve inter-variable relationships and minimize data loss."

---

## SECTION 10: ACTION ITEMS FOR LITERATURE SEARCH

### Must Extract from Each Paper:
1. Dataset size (training + test)
2. Missing data percentage (if reported)
3. Imputation method (if any)
4. Best R² achieved
5. Input/output variable list

### Must Calculate (If Not Reported):
1. Missing data % by manual inspection of supplementary materials
2. Correlation between dataset size and R²
3. Correlation between missing data % and R²

### Must Cross-Reference:
- Check if papers cite each other (network analysis)
- Identify common datasets (e.g., same biomass source)
- Identify methodology lineage (who copied whose approach)

---

**Document Status:** Ready for literature data integration
**Next Step:** Import user's literature search results
**Priority:** High - Core evidence for paper
