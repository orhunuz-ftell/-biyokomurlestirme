# REVERSE ML PREDICTION: SYNGAS → BIO-OIL COMPOSITION

**Project**: PhD Thesis - Bio-oil Steam Reforming ML Models
**Date**: November 30, 2025
**Objective**: Predict bio-oil composition from reformer output and process conditions

---

## OVERVIEW

### The Inverse Problem

**What we're solving**:

```
GIVEN:
  - Syngas composition (H₂, CO, CO₂, CH₄, H₂O) - measured from reformer
  - Process conditions (T, P, S/C) - known operating parameters

FIND:
  - Bio-oil composition (Aromatics, Acids, Alcohols, Furans, Phenols, Ketones)
```

### Why This Matters

**Applications**:
1. **Feedstock Identification**: "What bio-oil produced this syngas?"
2. **Quality Control**: Verify bio-oil composition without wet chemistry
3. **Process Optimization**: Find ideal bio-oil blend for target H₂ production
4. **Real-time Monitoring**: Track bio-oil variations during operation

---

## DATA SOURCE

**Database**: BIOOIL (SQL Server)
**Tables**:
- `ReformerSimulation` - Input parameters
- `ReformerOutput` - Syngas composition
- `Biooil` - Bio-oil composition

**Dataset Size**: 3,150 simulations
- 70 unique bio-oil compositions
- 45 process condition combinations (5×T, 3×P, 3×S/C)

**Quality**: All thermodynamically validated (professor review passed)

---

## QUICK START

### 1. Load Data

```python
import pandas as pd
import pyodbc

# Load from exported CSV
df = pd.read_csv('../reformer_only_model/output/reformer_ml_dataset.csv')

# Or load directly from database
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-DRO84HP\\SQLEXPRESS;'
    'DATABASE=BIOOIL;'
    'Trusted_Connection=yes'
)

query = """
SELECT
    s.Temperature_C, s.Pressure_bar, s.SC_Ratio,
    o.H2_molpercent, o.CO_molpercent, o.CO2_molpercent,
    o.CH4_molpercent, o.H2O_molpercent,
    b.aromatics, b.acids, b.alcohols, b.furans, b.phenols, b.[aldehyde&ketone]
FROM ReformerSimulation s
JOIN ReformerOutput o ON s.SimulationID = o.SimulationID
JOIN Biooil b ON s.BiooilID = b.BiooilId
WHERE s.ConvergenceStatus = 'Converged'
"""

df = pd.read_sql(query, conn)
```

### 2. Train Baseline Model

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# Define features
X_cols = ['Temperature_C', 'Pressure_bar', 'SC_Ratio',
          'H2_molpercent', 'CO_molpercent', 'CO2_molpercent',
          'CH4_molpercent', 'H2O_molpercent']

y_cols = ['aromatics', 'acids', 'alcohols', 'furans', 'phenols', 'aldehyde&ketone']

# Prepare data
df_clean = df.dropna()
X = df_clean[X_cols]
y = df_clean[y_cols]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
for i, col in enumerate(y_cols):
    r2 = r2_score(y_test[col], y_pred[:, i])
    mae = mean_absolute_error(y_test[col], y_pred[:, i])
    print(f"{col:20s} | R² = {r2:.3f} | MAE = {mae:.2f}%")
```

### 3. Make Predictions

```python
# Example: Predict bio-oil from syngas measurement
new_sample = pd.DataFrame({
    'Temperature_C': [750],
    'Pressure_bar': [5],
    'SC_Ratio': [2.0],
    'H2_molpercent': [32.97],
    'CO_molpercent': [7.84],
    'CO2_molpercent': [15.06],
    'CH4_molpercent': [0.37],
    'H2O_molpercent': [38.40]
})

biooil_pred = model.predict(new_sample)

print("\nPredicted Bio-oil Composition:")
for i, component in enumerate(y_cols):
    print(f"  {component:20s}: {biooil_pred[0, i]:6.2f}%")
```

---

## IMPLEMENTATION ROADMAP

See **IMPLEMENTATION_PLAN.md** for detailed 8-phase plan:

1. **Phase 1**: Data Preparation - Load, clean, split, EDA
2. **Phase 2**: Baseline Models - Linear, Random Forest, XGBoost
3. **Phase 3**: Deep Learning - MLP, constrained models
4. **Phase 4**: Advanced Techniques - Bayesian, CVAE, PINN
5. **Phase 5**: Hyperparameter Tuning - Grid search, Bayesian optimization
6. **Phase 6**: Model Evaluation - Metrics, visualization, test set
7. **Phase 7**: Deployment - Save models, prediction interface, inverse design
8. **Phase 8**: Thesis Documentation - Results, figures, discussion

---

## EXPECTED PERFORMANCE

**Baseline (Random Forest)**:
- R² = 0.7-0.8
- MAE = 3-4%

**Deep Learning (MLP)**:
- R² = 0.8-0.85
- MAE = 2-3%

**Ensemble**:
- R² = 0.85-0.9
- MAE < 2.5%

---

## KEY CHALLENGES

### 1. Non-Uniqueness
Different bio-oils may produce similar syngas → multiple valid solutions

**Solution**:
- Bayesian models for uncertainty quantification
- Probabilistic predictions with confidence intervals

### 2. Constraint Satisfaction
Bio-oil components must sum to 100%

**Solution**:
- Softmax output layer (neural networks)
- Post-processing normalization
- Custom loss functions

### 3. Limited Training Data
Only 70 unique bio-oil compositions

**Solution**:
- Data augmentation (if applicable)
- Regularization to prevent overfitting
- Cross-validation for robust evaluation

---

## FOLDER STRUCTURE

```
ml_reverse_prediction/
├── data/
│   ├── raw/                    # CSV exports from database
│   ├── processed/              # Cleaned datasets
│   └── exploratory/            # EDA outputs
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_baseline_models.ipynb
│   ├── 03_deep_learning.ipynb
│   ├── 04_evaluation.ipynb
│   └── 05_inverse_design.ipynb
├── src/
│   ├── data_loader.py
│   ├── models/
│   ├── evaluation.py
│   └── predictor.py
├── models/                     # Saved trained models
├── output/
│   ├── figures/
│   └── metrics/
├── README.md                   # This file
├── IMPLEMENTATION_PLAN.md      # Detailed plan
└── requirements.txt
```

---

## DEPENDENCIES

```
# Core
numpy>=1.21.0
pandas>=1.3.0
scipy>=1.7.0

# Machine Learning
scikit-learn>=1.0.0
xgboost>=1.5.0
tensorflow>=2.8.0
keras>=2.8.0

# Bayesian/Probabilistic
tensorflow-probability>=0.15.0

# Optimization
optuna>=2.10.0
keras-tuner>=1.1.0

# Visualization
matplotlib>=3.4.0
seaborn>=0.11.0

# Database
pyodbc>=4.0.32

# Utilities
joblib>=1.1.0
pyyaml>=5.4.0
```

---

## USAGE EXAMPLES

### Example 1: Feedstock Identification

```python
# Measured syngas from plant
syngas_measured = {
    'Temperature_C': 750,
    'Pressure_bar': 5,
    'SC_Ratio': 2.0,
    'H2_molpercent': 32.5,
    'CO_molpercent': 8.1,
    'CO2_molpercent': 14.8,
    'CH4_molpercent': 0.4,
    'H2O_molpercent': 39.0
}

# Predict bio-oil
biooil = predictor.predict(**syngas_measured)

# Compare with database
most_similar = find_closest_biooil(biooil, database)
print(f"Most likely bio-oil: ID {most_similar['id']}")
print(f"Similarity: {most_similar['similarity']:.1%}")
```

### Example 2: Inverse Design

```python
# Target: Maximize H2 production
target_H2 = 35.0  # mol%

# Optimize bio-oil composition
optimal_biooil = inverse_optimizer.optimize(
    target_H2=target_H2,
    process_conditions={'T': 800, 'P': 5, 'SC': 4.0}
)

print("Optimal Bio-oil Composition:")
print(f"  Aromatics: {optimal_biooil['aromatics']:.1f}%")
print(f"  Alcohols: {optimal_biooil['alcohols']:.1f}%")
print("  ...")
```

### Example 3: Sensitivity Analysis

```python
# How does prediction change with small syngas variations?
sensitivity = analyze_sensitivity(
    base_syngas={'H2': 32.5, 'CO': 8.0, ...},
    perturbation=0.5  # ±0.5 mol%
)

print("Sensitivity to H2 variation:")
print(f"  ΔH2 = +0.5% → ΔAromatics = {sensitivity['H2']['aromatics']:+.2f}%")
```

---

## VALIDATION STRATEGY

### Cross-Validation
5-fold cross-validation for hyperparameter selection

### Hold-out Test Set
15% of data never seen during training

### Physical Constraints Check
- All components ≥ 0%
- Sum of components = 100% ± 2%

### Comparison with Cantera
Forward prediction: Use predicted bio-oil → run Cantera → compare with original syngas

---

## THESIS CONTRIBUTIONS

### Scientific Novelty
1. First ML-based inverse model for bio-oil steam reforming
2. Demonstration of non-uniqueness in bio-oil-to-syngas mapping
3. Physics-informed constraints for thermodynamic consistency

### Practical Impact
1. Real-time bio-oil quality monitoring
2. Optimization framework for desired product composition
3. Reduced need for expensive bio-oil characterization

### Methodological Advances
1. Handling compositional constraints in neural networks
2. Uncertainty quantification for inverse problems
3. Integration of ML with thermodynamic simulations

---

## NEXT STEPS

**Immediate**:
1. Load and explore reformer dataset
2. Check data quality and missing values
3. Train Random Forest baseline

**Short-term**:
1. Implement deep learning models
2. Add constraint handling
3. Hyperparameter tuning

**Long-term**:
1. Experimental validation (if data available)
2. Real-time monitoring system
3. Integration with process control

---

## CONTACT & REFERENCES

**Project**: PhD Thesis - Biomass Pyrolysis Bio-oil ML Prediction
**Database**: BIOOIL on DESKTOP-DRO84HP\SQLEXPRESS
**Related Folders**:
- `reformer_only_model/` - Cantera simulation code
- `cantera_generation/` - Original mechanism files

**Status**: READY TO START
**Estimated Time**: 7 weeks for complete implementation

---

**Let's begin with Phase 1: Data Preparation!**
