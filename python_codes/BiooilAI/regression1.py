import os
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, KFold
from sklearn.preprocessing import StandardScaler

# 1. Çalışma dizini
if '__file__' in globals():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
else:
    BASE_DIR = os.getcwd()

def fp(fname: str) -> str:
    return os.path.join(BASE_DIR, fname)

# 2. Veri Yükleme
X_train = pd.read_csv(fp('processed_data_X_train.csv'))
y_train = pd.read_csv(fp('processed_data_y_train.csv'))
X_test  = pd.read_csv(fp('processed_data_X_test.csv'))
y_test  = pd.read_csv(fp('processed_data_y_test.csv'))

# 3. Random Forest Pipeline with regularization
rf_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),
    ('model', MultiOutputRegressor(RandomForestRegressor(
        n_estimators=100,
        max_depth=5,  # Ağaç derinliğini sınırla
        min_samples_split=5,  # Split için minimum örnek sayısı
        min_samples_leaf=3,   # Yaprak düğümler için minimum örnek sayısı
        max_features='sqrt',  # Her split'te kullanılacak özellik sayısını sınırla
        random_state=42
    )))
])

# Cross-validation için KFold
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Cross-validation scores
cv_scores_rf = cross_val_score(rf_pipeline, X_train, y_train, cv=kf, scoring='r2')
print("\nRandom Forest Cross-validation R² scores:", cv_scores_rf)
print("Mean CV R² score: {:.4f} (+/- {:.4f})".format(cv_scores_rf.mean(), cv_scores_rf.std() * 2))

rf_pipeline.fit(X_train, y_train)
y_pred_rf = rf_pipeline.predict(X_test)

mse_rf = mean_squared_error(y_test, y_pred_rf, multioutput='raw_values')
r2_rf  = r2_score(y_test, y_pred_rf, multioutput='raw_values')

print("Random Forest MSE per target:\n", mse_rf)
print("Random Forest Mean MSE: {:.4f}".format(mse_rf.mean()))
print("\nRandom Forest R² değerleri:")
print("-" * 50)
for col, r2 in zip(y_test.columns, r2_rf):
    print(f"{col:20}: {r2:.4f}")
print("-" * 50)
print(f"Ortalama R²: {r2_rf.mean():.4f}")

# Training R² values for Random Forest
y_train_pred_rf = rf_pipeline.predict(X_train)
r2_train_rf = r2_score(y_train, y_train_pred_rf, multioutput='raw_values')
print("\nRandom Forest Training R² değerleri:")
print("-" * 50)
for col, r2 in zip(y_train.columns, r2_train_rf):
    print(f"{col:20}: {r2:.4f}")
print("-" * 50)
print(f"Training Ortalama R²: {r2_train_rf.mean():.4f}")

# 4. XGBoost Pipeline with regularization
xgb_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),
    ('model', MultiOutputRegressor(XGBRegressor(
        n_estimators=100,
        max_depth=4,          # Ağaç derinliğini sınırla
        learning_rate=0.05,   # Daha düşük learning rate
        subsample=0.8,        # Her iterasyonda verinin %80'ini kullan
        colsample_bytree=0.8, # Her ağaç için özelliklerin %80'ini kullan
        reg_alpha=0.1,        # L1 regularizasyon
        reg_lambda=1.0,       # L2 regularizasyon
        objective='reg:squarederror',
        random_state=42
    )))
])

# Cross-validation scores for XGBoost
cv_scores_xgb = cross_val_score(xgb_pipeline, X_train, y_train, cv=kf, scoring='r2')
print("\nXGBoost Cross-validation R² scores:", cv_scores_xgb)
print("Mean CV R² score: {:.4f} (+/- {:.4f})".format(cv_scores_xgb.mean(), cv_scores_xgb.std() * 2))

xgb_pipeline.fit(X_train, y_train)
y_pred_xgb = xgb_pipeline.predict(X_test)

mse_xgb = mean_squared_error(y_test, y_pred_xgb, multioutput='raw_values')
r2_xgb  = r2_score(y_test, y_pred_xgb, multioutput='raw_values')

print("\nXGBoost MSE per target:\n", mse_xgb)
print("XGBoost Mean MSE: {:.4f}".format(mse_xgb.mean()))
print("\nXGBoost R² değerleri:")
print("-" * 50)
for col, r2 in zip(y_test.columns, r2_xgb):
    print(f"{col:20}: {r2:.4f}")
print("-" * 50)
print(f"Ortalama R²: {r2_xgb.mean():.4f}")

# Training R² values for XGBoost
y_train_pred_xgb = xgb_pipeline.predict(X_train)
r2_train_xgb = r2_score(y_train, y_train_pred_xgb, multioutput='raw_values')
print("\nXGBoost Training R² değerleri:")
print("-" * 50)
for col, r2 in zip(y_train.columns, r2_train_xgb):
    print(f"{col:20}: {r2:.4f}")
print("-" * 50)
print(f"Training Ortalama R²: {r2_train_xgb.mean():.4f}")
