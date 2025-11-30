# MACHINE LEARNING REVERSE PREDICTION - IMPLEMENTATION PLAN
## Predict Bio-oil Composition from Syngas Output + Process Conditions

**Date**: November 30, 2025
**Author**: PhD Project Planning
**Objective**: Train ML models to predict bio-oil composition from reformer output and operating conditions

---

## EXECUTIVE SUMMARY

### Problem Statement

**Forward Problem** (Already solved with Cantera):
```
INPUT: Bio-oil composition + T, P, S/C
   ↓ (Cantera simulation)
OUTPUT: Syngas composition (H₂, CO, CO₂, CH₄, H₂O)
```

**Reverse Problem** (This ML project):
```
INPUT: Syngas composition + T, P, S/C
   ↓ (Machine Learning)
OUTPUT: Bio-oil composition (Aromatics, Acids, Alcohols, Furans, Phenols, Ketones)
```

### Why This Is Valuable

**Practical Application**:
1. **Feedstock Identification**: Given measured syngas, identify what bio-oil was used
2. **Process Optimization**: Find bio-oil composition that produces desired syngas
3. **Quality Control**: Verify bio-oil composition in real-time from reformer output
4. **Inverse Design**: Design bio-oil blends for target H₂ production

**Scientific Novelty**:
- First application of inverse ML to bio-oil reforming
- Demonstrates feasibility of composition inference from products
- Enables optimization without iterative simulation

### Expected Challenges

**Challenge 1: Non-Uniqueness**
- Different bio-oils may produce similar syngas
- Solution: Probabilistic models, Bayesian inference

**Challenge 2: Process Conditions Confound**
- Temperature/pressure/S/C also affect syngas
- Solution: Include process conditions as inputs to ML

**Challenge 3: Constraint Satisfaction**
- Bio-oil composition must sum to 100%
- Each component 0-100%
- Solution: Use softmax output layer or post-processing normalization

---

## PHASE 1: DATA PREPARATION

### 1.1 Load and Clean Dataset

**Source**: Reformer-only model database (3,150 simulations)

**Input Features** (9 total):
- `Reformer_Temperature_C` (5 levels: 650, 700, 750, 800, 850)
- `Reformer_Pressure_bar` (3 levels: 5, 15, 30)
- `Steam_to_Carbon_Ratio` (3 levels: 2.0, 4.0, 6.0)
- `H2_molpercent` (syngas output)
- `CO_molpercent` (syngas output)
- `CO2_molpercent` (syngas output)
- `CH4_molpercent` (syngas output)
- `H2O_molpercent` (syngas output)
- (Optional: `C2H4_molpercent`, `C2H6_molpercent`)

**Target Variables** (6 bio-oil components):
- `Biooil_Aromatics_pct` (0-100%)
- `Biooil_Acids_pct` (0-100%)
- `Biooil_Alcohols_pct` (0-100%)
- `Biooil_Furans_pct` (0-100%)
- `Biooil_Phenols_pct` (0-100%)
- `Biooil_Aldehydes_Ketones_pct` (0-100%)

**Constraint**: Σ(bio-oil components) ≈ 100%

**Data Quality Steps**:
```python
# 1. Handle missing values
df_clean = df.dropna(subset=input_features + target_features)

# 2. Remove outliers (if any)
# Based on professor review: all data is thermodynamically valid

# 3. Check constraint satisfaction
df_clean['biooil_sum'] = df_clean[target_features].sum(axis=1)
print(f"Bio-oil sum range: {df_clean['biooil_sum'].min():.2f} - {df_clean['biooil_sum'].max():.2f}")

# 4. Normalize if needed (some bio-oils may not sum to exactly 100%)
df_clean[target_features] = df_clean[target_features].div(
    df_clean['biooil_sum'], axis=0
) * 100
```

### 1.2 Exploratory Data Analysis

**Correlation Analysis**:
```python
import seaborn as sns
import matplotlib.pyplot as plt

# Correlation between syngas composition and bio-oil components
corr_matrix = df_clean[input_features + target_features].corr()

# Visualize
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix: Syngas vs Bio-oil Composition')
plt.savefig('output/correlation_matrix.png')
```

**Key Questions**:
- Which syngas species correlate most with bio-oil composition?
- Is there multicollinearity among inputs?
- Are there distinct clusters of bio-oil types?

**Feature Importance (Preliminary)**:
```python
from sklearn.ensemble import RandomForestRegressor

# Quick feature importance check
rf = RandomForestRegressor(n_estimators=50, random_state=42)
rf.fit(X_train, y_train['Biooil_Aromatics_pct'])

importance = pd.DataFrame({
    'feature': input_features,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

print(importance)
```

Expected: H₂, CO ratios and temperature will be most important.

### 1.3 Train-Validation-Test Split

**Strategy**: Stratified split to ensure all bio-oil types represented

```python
from sklearn.model_selection import train_test_split

# 70% train, 15% validation, 15% test
X = df_clean[input_features]
y = df_clean[target_features]

X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.15, random_state=42
)

X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.176, random_state=42  # 0.176 * 0.85 ≈ 0.15
)

print(f"Train: {len(X_train)} samples")
print(f"Validation: {len(X_val)} samples")
print(f"Test: {len(X_test)} samples")
```

**Expected sizes** (for 3,150 total):
- Train: 2,205 samples
- Validation: 473 samples
- Test: 472 samples

---

## PHASE 2: BASELINE MODELS

### 2.1 Linear Regression (Baseline)

**Purpose**: Establish lower bound performance

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Train separate model for each bio-oil component
models_lr = {}
metrics_lr = {}

for component in target_features:
    # Train
    model = LinearRegression()
    model.fit(X_train, y_train[component])

    # Predict
    y_pred = model.predict(X_val)

    # Evaluate
    metrics_lr[component] = {
        'R2': r2_score(y_val[component], y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_val[component], y_pred)),
        'MAE': mean_absolute_error(y_val[component], y_pred)
    }

    models_lr[component] = model

# Print results
for comp, metrics in metrics_lr.items():
    print(f"{comp:30s} | R²={metrics['R2']:.3f} | RMSE={metrics['RMSE']:.2f} | MAE={metrics['MAE']:.2f}")
```

**Expected Performance**: R² = 0.3-0.5 (poor, due to non-linearity)

### 2.2 Random Forest (Strong Baseline)

**Purpose**: Capture non-linear relationships

```python
from sklearn.ensemble import RandomForestRegressor

models_rf = {}
metrics_rf = {}

for component in target_features:
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train[component])
    y_pred = model.predict(X_val)

    metrics_rf[component] = {
        'R2': r2_score(y_val[component], y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_val[component], y_pred)),
        'MAE': mean_absolute_error(y_val[component], y_pred)
    }

    models_rf[component] = model
```

**Expected Performance**: R² = 0.6-0.8

### 2.3 Gradient Boosting (XGBoost)

**Purpose**: Often best for tabular data

```python
from xgboost import XGBRegressor

models_xgb = {}
metrics_xgb = {}

for component in target_features:
    model = XGBRegressor(
        n_estimators=200,
        max_depth=10,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train[component],
              eval_set=[(X_val, y_val[component])],
              early_stopping_rounds=20,
              verbose=False)

    y_pred = model.predict(X_val)

    metrics_xgb[component] = {
        'R2': r2_score(y_val[component], y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_val[component], y_pred)),
        'MAE': mean_absolute_error(y_val[component], y_pred)
    }

    models_xgb[component] = model
```

**Expected Performance**: R² = 0.7-0.85

---

## PHASE 3: DEEP LEARNING MODELS

### 3.1 Multi-Layer Perceptron (MLP)

**Architecture**:
```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Normalize inputs
from sklearn.preprocessing import StandardScaler

scaler_X = StandardScaler()
X_train_scaled = scaler_X.fit_transform(X_train)
X_val_scaled = scaler_X.transform(X_val)

scaler_y = StandardScaler()
y_train_scaled = scaler_y.fit_transform(y_train)
y_val_scaled = scaler_y.transform(y_val)

# Model architecture
model_mlp = keras.Sequential([
    layers.Dense(128, activation='relu', input_dim=len(input_features)),
    layers.BatchNormalization(),
    layers.Dropout(0.3),

    layers.Dense(64, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.2),

    layers.Dense(32, activation='relu'),
    layers.Dropout(0.1),

    layers.Dense(6)  # Output: 6 bio-oil components
])

model_mlp.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='mse',
    metrics=['mae']
)

# Train
history = model_mlp.fit(
    X_train_scaled, y_train_scaled,
    validation_data=(X_val_scaled, y_val_scaled),
    epochs=200,
    batch_size=32,
    callbacks=[
        keras.callbacks.EarlyStopping(patience=20, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(patience=10, factor=0.5)
    ],
    verbose=1
)

# Evaluate
y_pred_scaled = model_mlp.predict(X_val_scaled)
y_pred = scaler_y.inverse_transform(y_pred_scaled)
```

**Expected Performance**: R² = 0.75-0.90

### 3.2 MLP with Constraint Layer (Softmax Output)

**Purpose**: Ensure bio-oil components sum to 100%

```python
# Custom architecture with softmax constraint
model_constrained = keras.Sequential([
    layers.Dense(128, activation='relu', input_dim=len(input_features)),
    layers.BatchNormalization(),
    layers.Dropout(0.3),

    layers.Dense(64, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.2),

    layers.Dense(32, activation='relu'),
    layers.Dropout(0.1),

    layers.Dense(6, activation='softmax')  # Ensures sum = 1.0
])

# Scale targets to 0-1 range (proportions)
y_train_prop = y_train.div(y_train.sum(axis=1), axis=0)
y_val_prop = y_val.div(y_val.sum(axis=1), axis=0)

model_constrained.compile(
    optimizer='adam',
    loss='kullback_leibler_divergence',  # Good for probability distributions
    metrics=['mae']
)

history = model_constrained.fit(
    X_train_scaled, y_train_prop,
    validation_data=(X_val_scaled, y_val_prop),
    epochs=200,
    batch_size=32,
    callbacks=[
        keras.callbacks.EarlyStopping(patience=20, restore_best_weights=True)
    ]
)

# Predictions automatically sum to 1.0, scale back to 0-100%
y_pred_prop = model_constrained.predict(X_val_scaled)
y_pred = y_pred_prop * 100
```

### 3.3 Ensemble Model

**Combine best models**:
```python
# Weighted average of predictions
y_pred_ensemble = (
    0.3 * y_pred_xgb +
    0.3 * y_pred_mlp +
    0.4 * y_pred_constrained
)

# Ensure sum to 100%
y_pred_ensemble = y_pred_ensemble.div(y_pred_ensemble.sum(axis=1), axis=0) * 100
```

---

## PHASE 4: ADVANCED TECHNIQUES

### 4.1 Bayesian Neural Network (Uncertainty Quantification)

**Purpose**: Provide confidence intervals for predictions

```python
import tensorflow_probability as tfp

# Probabilistic model
model_bayesian = keras.Sequential([
    layers.Dense(128, activation='relu'),
    tfp.layers.DenseVariational(64, activation='relu'),
    tfp.layers.DenseVariational(32, activation='relu'),
    tfp.layers.DenseVariational(6)  # Outputs mean and variance
])

# Train with variational inference
# Returns: mean prediction ± uncertainty
```

**Output**:
```
Aromatics: 32.5% ± 2.1%  (95% confidence)
Acids:     10.8% ± 1.5%
...
```

### 4.2 Conditional Variational Autoencoder (CVAE)

**Purpose**: Model the distribution of bio-oils given syngas

**Architecture**:
```python
# Encoder: Syngas → Latent space
encoder_input = keras.Input(shape=(9,))  # Syngas + T,P,S/C
x = layers.Dense(64, activation='relu')(encoder_input)
x = layers.Dense(32, activation='relu')(x)

z_mean = layers.Dense(16)(x)
z_log_var = layers.Dense(16)(x)

# Sampling layer
z = Sampling()([z_mean, z_log_var])

# Decoder: Latent space → Bio-oil composition
decoder_input = keras.Input(shape=(16,))
x = layers.Dense(32, activation='relu')(decoder_input)
x = layers.Dense(64, activation='relu')(x)
decoder_output = layers.Dense(6, activation='softmax')(x)  # Bio-oil proportions

# CVAE model
encoder = keras.Model(encoder_input, [z_mean, z_log_var, z])
decoder = keras.Model(decoder_input, decoder_output)
cvae = CVAE(encoder, decoder)

# Train
cvae.compile(optimizer='adam')
cvae.fit(X_train_scaled, y_train_prop, epochs=100, batch_size=32)

# Sample multiple bio-oil compositions for given syngas
z_samples = np.random.normal(size=(100, 16))  # 100 samples
biooil_samples = decoder.predict(z_samples)  # 100 possible bio-oils
```

**Advantage**: Can generate multiple plausible bio-oil compositions for ambiguous cases

### 4.3 Physics-Informed Neural Network (PINN)

**Purpose**: Incorporate thermodynamic constraints

```python
# Custom loss function with physics constraints
def physics_loss(y_true, y_pred, X_input):
    # Standard prediction loss
    mse_loss = tf.reduce_mean(tf.square(y_true - y_pred))

    # Physics constraint 1: Sum to 100%
    sum_constraint = tf.reduce_mean(tf.square(tf.reduce_sum(y_pred, axis=1) - 100))

    # Physics constraint 2: Non-negative
    negative_penalty = tf.reduce_mean(tf.nn.relu(-y_pred))

    # Physics constraint 3: Atom balance (carbon conservation)
    # (Requires calculating carbon atoms from predictions)

    total_loss = mse_loss + 0.1*sum_constraint + 1.0*negative_penalty
    return total_loss
```

---

## PHASE 5: HYPERPARAMETER TUNING

### 5.1 Grid Search for Random Forest

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(
    RandomForestRegressor(random_state=42),
    param_grid,
    cv=5,
    scoring='neg_mean_squared_error',
    n_jobs=-1
)

grid_search.fit(X_train, y_train['Biooil_Aromatics_pct'])
print(f"Best params: {grid_search.best_params_}")
```

### 5.2 Bayesian Optimization for Neural Networks

```python
from keras_tuner import BayesianOptimization

def build_model(hp):
    model = keras.Sequential()
    model.add(layers.Dense(
        hp.Int('units_1', min_value=32, max_value=256, step=32),
        activation='relu',
        input_dim=len(input_features)
    ))
    model.add(layers.Dropout(hp.Float('dropout_1', 0.0, 0.5, step=0.1)))

    model.add(layers.Dense(
        hp.Int('units_2', min_value=16, max_value=128, step=16),
        activation='relu'
    ))
    model.add(layers.Dropout(hp.Float('dropout_2', 0.0, 0.5, step=0.1)))

    model.add(layers.Dense(6))

    model.compile(
        optimizer=keras.optimizers.Adam(
            hp.Choice('learning_rate', [1e-2, 1e-3, 1e-4])
        ),
        loss='mse',
        metrics=['mae']
    )
    return model

tuner = BayesianOptimization(
    build_model,
    objective='val_loss',
    max_trials=50,
    directory='tuning',
    project_name='reverse_ml'
)

tuner.search(X_train_scaled, y_train_scaled,
             validation_data=(X_val_scaled, y_val_scaled),
             epochs=100,
             batch_size=32)
```

---

## PHASE 6: MODEL EVALUATION

### 6.1 Metrics

**Regression Metrics** (per component):
- R² (coefficient of determination)
- RMSE (root mean squared error)
- MAE (mean absolute error)
- MAPE (mean absolute percentage error)

**Composition-Level Metrics**:
- Total composition error: `|Σ(predicted) - 100|`
- Component ranking accuracy: Do we identify the dominant component correctly?

### 6.2 Visualization

**Predicted vs Actual Plots**:
```python
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

for idx, component in enumerate(target_features):
    ax = axes[idx // 3, idx % 3]

    ax.scatter(y_val[component], y_pred[:, idx], alpha=0.5)
    ax.plot([0, 100], [0, 100], 'r--', lw=2)  # Perfect prediction line
    ax.set_xlabel('Actual (%)')
    ax.set_ylabel('Predicted (%)')
    ax.set_title(component)

    r2 = r2_score(y_val[component], y_pred[:, idx])
    ax.text(0.05, 0.95, f'R² = {r2:.3f}', transform=ax.transAxes)

plt.tight_layout()
plt.savefig('output/predicted_vs_actual.png')
```

**Residual Plots**:
```python
residuals = y_val - y_pred

for component in target_features:
    plt.figure()
    plt.hist(residuals[component], bins=50)
    plt.xlabel('Residual (%)')
    plt.ylabel('Frequency')
    plt.title(f'Residual Distribution: {component}')
    plt.savefig(f'output/residuals_{component}.png')
```

### 6.3 Test Set Evaluation

**Final evaluation on held-out test set**:
```python
# Use best model
y_test_pred = best_model.predict(X_test_scaled)

# Calculate metrics
test_metrics = {}
for idx, component in enumerate(target_features):
    test_metrics[component] = {
        'R2': r2_score(y_test[component], y_test_pred[:, idx]),
        'RMSE': np.sqrt(mean_squared_error(y_test[component], y_test_pred[:, idx])),
        'MAE': mean_absolute_error(y_test[component], y_test_pred[:, idx])
    }

# Print report
print("\nTEST SET PERFORMANCE")
print("="*80)
for comp, metrics in test_metrics.items():
    print(f"{comp:30s} | R²={metrics['R2']:.3f} | RMSE={metrics['RMSE']:.2f} | MAE={metrics['MAE']:.2f}")
```

---

## PHASE 7: DEPLOYMENT AND APPLICATION

### 7.1 Save Best Models

```python
# Save scikit-learn models
import joblib
joblib.dump(best_rf_model, 'models/rf_reverse_model.pkl')
joblib.dump(best_xgb_model, 'models/xgb_reverse_model.pkl')
joblib.dump(scaler_X, 'models/scaler_X.pkl')
joblib.dump(scaler_y, 'models/scaler_y.pkl')

# Save Keras models
best_mlp_model.save('models/mlp_reverse_model.h5')
```

### 7.2 Prediction Interface

```python
class BiooilPredictor:
    """Predict bio-oil composition from syngas output"""

    def __init__(self, model_path, scaler_X_path, scaler_y_path):
        self.model = keras.models.load_model(model_path)
        self.scaler_X = joblib.load(scaler_X_path)
        self.scaler_y = joblib.load(scaler_y_path)

    def predict(self, temperature_C, pressure_bar, sc_ratio,
                H2, CO, CO2, CH4, H2O):
        """
        Predict bio-oil composition

        Args:
            temperature_C: Reformer temperature (°C)
            pressure_bar: Reformer pressure (bar)
            sc_ratio: Steam-to-carbon ratio
            H2, CO, CO2, CH4, H2O: Syngas composition (mol%)

        Returns:
            dict: Bio-oil composition (wt%)
        """
        # Prepare input
        X = np.array([[temperature_C, pressure_bar, sc_ratio,
                       H2, CO, CO2, CH4, H2O]])
        X_scaled = self.scaler_X.transform(X)

        # Predict
        y_scaled = self.model.predict(X_scaled)
        y = self.scaler_y.inverse_transform(y_scaled)

        # Ensure sum to 100% and non-negative
        y = np.maximum(y, 0)
        y = y / y.sum() * 100

        return {
            'Aromatics': y[0, 0],
            'Acids': y[0, 1],
            'Alcohols': y[0, 2],
            'Furans': y[0, 3],
            'Phenols': y[0, 4],
            'Aldehydes_Ketones': y[0, 5]
        }

# Usage
predictor = BiooilPredictor('models/mlp_reverse_model.h5',
                            'models/scaler_X.pkl',
                            'models/scaler_y.pkl')

result = predictor.predict(
    temperature_C=750,
    pressure_bar=5,
    sc_ratio=2.0,
    H2=32.97,
    CO=7.84,
    CO2=15.06,
    CH4=0.37,
    H2O=38.40
)

print("Predicted Bio-oil Composition:")
for component, value in result.items():
    print(f"  {component:20s}: {value:6.2f}%")
```

### 7.3 Inverse Design Tool

**Optimize bio-oil composition for target H₂ yield**:

```python
from scipy.optimize import minimize

def objective(biooil_composition, target_H2, process_conditions):
    """
    Find bio-oil composition that produces target H2

    Args:
        biooil_composition: [aromatics, acids, alcohols, furans, phenols, ketones]
        target_H2: Desired H2 mol% in syngas
        process_conditions: [T, P, S/C]

    Returns:
        Squared error between predicted H2 and target H2
    """
    # Run forward model (Cantera or ML surrogate)
    syngas = forward_model.predict(biooil_composition, process_conditions)

    # Error
    error = (syngas['H2'] - target_H2)**2

    return error

# Constraints: sum to 100%, non-negative
constraints = [
    {'type': 'eq', 'fun': lambda x: np.sum(x) - 100},  # Sum = 100
]
bounds = [(0, 100)] * 6  # Each component 0-100%

# Optimize
result = minimize(
    objective,
    x0=[20, 15, 20, 10, 15, 20],  # Initial guess
    args=(target_H2=35.0, process_conditions=[800, 5, 4.0]),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

print("Optimal Bio-oil Composition for 35% H2:")
print(f"  Aromatics: {result.x[0]:.2f}%")
print(f"  Acids: {result.x[1]:.2f}%")
print(f"  Alcohols: {result.x[2]:.2f}%")
print(f"  Furans: {result.x[3]:.2f}%")
print(f"  Phenols: {result.x[4]:.2f}%")
print(f"  Ketones: {result.x[5]:.2f}%")
```

---

## PHASE 8: THESIS DOCUMENTATION

### 8.1 Results to Report

**Model Comparison Table**:
```
Model                  | Aromatics R² | Acids R² | Alcohols R² | ... | Avg R² | Avg MAE
-----------------------|--------------|----------|-------------|-----|--------|--------
Linear Regression      | 0.42         | 0.38     | 0.45        | ... | 0.41   | 8.5%
Random Forest          | 0.78         | 0.72     | 0.81        | ... | 0.76   | 3.2%
XGBoost                | 0.82         | 0.79     | 0.85        | ... | 0.81   | 2.8%
MLP                    | 0.84         | 0.81     | 0.87        | ... | 0.83   | 2.5%
MLP + Softmax          | 0.83         | 0.80     | 0.86        | ... | 0.82   | 2.6%
Ensemble               | 0.86         | 0.83     | 0.89        | ... | 0.85   | 2.3%
```

**Feature Importance**:
- Which syngas species are most informative for predicting each bio-oil component?
- Importance of temperature vs pressure vs S/C ratio?

**Case Studies**:
- Example 1: High-aromatic bio-oil identification
- Example 2: Ambiguous case (multiple bio-oils produce similar syngas)
- Example 3: Inverse design for target H₂ production

### 8.2 Figures for Thesis

1. **Predicted vs Actual** (6 subplots, one per component)
2. **Residual distributions** (histograms)
3. **Feature importance** (bar chart)
4. **Model comparison** (grouped bar chart)
5. **Learning curves** (training/validation loss over epochs)
6. **Uncertainty quantification** (for Bayesian model)
7. **Inverse design example** (optimization trajectory)

### 8.3 Discussion Points

**Strengths**:
- High accuracy (R² > 0.85 for most components)
- Fast prediction (~1 ms vs 5 ms for Cantera)
- Enables inverse design and optimization
- Thermodynamically consistent (via constraints)

**Limitations**:
- Non-uniqueness: multiple bio-oils can produce similar syngas
- Extrapolation risk: only valid for bio-oils in training range
- Assumes equilibrium (real reactors: 75-85% conversion)

**Future Work**:
- Experimental validation with real reformer data
- Extension to kinetic models (non-equilibrium)
- Integration with process economics
- Real-time monitoring application

---

## FOLDER STRUCTURE

```
ml_reverse_prediction/
├── data/
│   ├── raw/                    # Original CSV from database export
│   ├── processed/              # Cleaned, split datasets
│   └── exploratory/            # EDA outputs
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_baseline_models.ipynb
│   ├── 03_deep_learning.ipynb
│   ├── 04_hyperparameter_tuning.ipynb
│   └── 05_evaluation.ipynb
├── src/
│   ├── data_loader.py          # Load and preprocess data
│   ├── models/
│   │   ├── baseline_models.py  # Linear, RF, XGBoost
│   │   ├── deep_models.py      # MLP, CVAE, PINN
│   │   └── ensemble.py         # Ensemble methods
│   ├── evaluation.py           # Metrics, visualization
│   ├── predictor.py            # Deployment interface
│   └── inverse_design.py       # Optimization tools
├── models/                     # Saved trained models
│   ├── rf_reverse_model.pkl
│   ├── xgb_reverse_model.pkl
│   ├── mlp_reverse_model.h5
│   └── scalers/
├── output/
│   ├── figures/                # Plots for thesis
│   ├── metrics/                # Performance tables
│   └── predictions/            # Test set results
├── configs/
│   └── model_config.yaml       # Hyperparameters
├── tests/
│   └── test_models.py          # Unit tests
├── README.md
├── requirements.txt
└── IMPLEMENTATION_PLAN.md      # This file
```

---

## TIMELINE ESTIMATE

**Week 1**: Data preparation and EDA (Phase 1)
**Week 2**: Baseline models (Phase 2)
**Week 3**: Deep learning models (Phase 3)
**Week 4**: Advanced techniques (Phase 4)
**Week 5**: Hyperparameter tuning (Phase 5)
**Week 6**: Evaluation and deployment (Phases 6-7)
**Week 7**: Thesis documentation (Phase 8)

**Total**: 7 weeks for complete implementation

---

## SUCCESS CRITERIA

**Minimum Acceptable**:
- Average R² > 0.70 across all bio-oil components
- MAE < 5% for each component

**Target**:
- Average R² > 0.80
- MAE < 3% for each component
- Constraint satisfaction: predicted bio-oil sums to 100% ± 2%

**Stretch Goal**:
- Average R² > 0.85
- MAE < 2%
- Uncertainty quantification (confidence intervals)
- Successful inverse design demonstration

---

## NEXT STEPS

1. **Immediate**: Load reformer dataset from database/CSV
2. **Data prep**: Clean, split, normalize
3. **Quick prototype**: Train Random Forest baseline
4. **Iterate**: Move to deep learning if baseline shows promise

**Ready to start?** Begin with Phase 1: Data Preparation

---

**END OF IMPLEMENTATION PLAN**
