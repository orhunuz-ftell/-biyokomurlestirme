"""
train_biooil_models.py
----------------------
• Verisetlerini okur
• Eksik değerlere medyan imputasyonu + ölçekleme uygular
• RandomForestRegressor (her bir hedef için) ile modeli kurar
• Test kümesindeki R² skorlarını raporlar
"""

from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# --- DOSYA YOLLARI -----------------------------------------------------------
BASE_DIR = Path(r"C:\@biyokomurlestirme\python_codes\mayis")
X_train = pd.read_csv(BASE_DIR / "ProcessedData_X_train.csv")
X_test  = pd.read_csv(BASE_DIR / "ProcessedData_X_test.csv")
y_train = pd.read_csv(BASE_DIR / "ProcessedData_y_train.csv")
y_test  = pd.read_csv(BASE_DIR / "ProcessedData_y_test.csv")

# --- ÖN-İŞLEME ---------------------------------------------------------------
numeric_features   = X_train.columns.tolist()
numeric_transform  = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler",  StandardScaler())
])
preproc = ColumnTransformer([("num", numeric_transform, numeric_features)])

# --- HEDEF LİSTESİ -----------------------------------------------------------
targets = ["aromatics",
           "aliphatichydrocarbon",  # ad sütunlarda farklı ise düzeltin
           "acids",
           "alcohols",
           "furans",
           "phenols",
           "aldehyde_ketone"]       # CSV’deki tam sütun adını kullanın

r2_scores = {}

for tgt in targets:
    if tgt not in y_train.columns:
        print(f"[SKIP] {tgt:<25} -> sütun bulunamadı")
        continue

    # hedef NaN satırlarını at
    train_idx = y_train[tgt].dropna().index
    test_idx  = y_test[tgt].dropna().index
    if len(test_idx) < 2:                # <2 satırda R² tanımsız
        print(f"[SKIP] {tgt:<25} -> test verisi yetersiz")
        continue

    Xtr, ytr = X_train.loc[train_idx], y_train.loc[train_idx, tgt]
    Xte, yte = X_test.loc[test_idx],  y_test.loc[test_idx,  tgt]

    model = Pipeline([
        ("prep", preproc),
        ("rf",   RandomForestRegressor(n_estimators=500,
                                       random_state=42,
                                       n_jobs=-1))
    ])
    model.fit(Xtr, ytr)
    ypred = model.predict(Xte)
    r2    = r2_score(yte, ypred)
    r2_scores[tgt] = r2
    print(f"{tgt:<25} R² = {r2:5.3f}")

# --- ÖZET --------------------------------------------------------------------
print("\n=== R² Özet ===")
for k, v in r2_scores.items():
    print(f"{k:<25} : {v:5.3f}")
