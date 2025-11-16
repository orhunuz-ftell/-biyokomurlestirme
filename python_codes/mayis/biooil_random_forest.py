# biooil_random_forest.py
# ================================================================
#  ► Konu : Biyokütle pirolizi → biyoyağ kimyasal konsantrasyon tahmini
#  ► Yazar: ChatGPT (2025-05-14)
#  ► Kullanım:
#       PS> cd C:\@biyokomurlestirme\python_codes\mayis
#       PS> python biooil_random_forest.py
# ================================================================

from pathlib import Path
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV, KFold
from sklearn.metrics import r2_score

# ---------- Dosya yolları ----------------------------------------------------
BASE = Path(r"C:\@biyokomurlestirme\python_codes\mayis")
X_train = pd.read_csv(BASE / "ProcessedData_X_train.csv")
X_test  = pd.read_csv(BASE / "ProcessedData_X_test.csv")
y_train = pd.read_csv(BASE / "ProcessedData_y_train.csv")
y_test  = pd.read_csv(BASE / "ProcessedData_y_test.csv")

# ---------- Hedef sütunlar ---------------------------------------------------
TARGETS = [
    "aromatics",
    "aliphatichydrocarbon",   # CSV’deki tam adı farklıysa değiştirin
    "acids",
    "alcohols",
    "furans",
    "phenols",
    "aldehyde_ketone","sugar"
]

# ---------- Ön-işleme --------------------------------------------------------
num_cols = X_train.columns.tolist()
numeric_pipe = Pipeline([
    ("impute", SimpleImputer(strategy="median")),
    ("scale",  StandardScaler())
])
preprocessor = ColumnTransformer([("num", numeric_pipe, num_cols)])

# ---------- Random Forest + Hiperparametre araması ---------------------------
param_space = {
    "rf__n_estimators":   [200, 400, 600, 800, 1000],
    "rf__max_depth":      [None, 10, 20, 40, 60, 80],
    "rf__min_samples_leaf": [1, 2, 4],
    "rf__max_features":   ["sqrt", "log2", None]
}

def build_model():
    """Pipeline: ön-işleme + RandomForest."""
    return Pipeline([
        ("prep", preprocessor),
        ("rf",  RandomForestRegressor(random_state=42, n_jobs=-1))
    ])

# ---------- Eğitim & Değerlendirme ------------------------------------------
print("\n=== R² Sonuçları ===")
print(f"{'Target':25} CV_R2  Test_R2")

cv = KFold(n_splits=3, shuffle=True, random_state=42)
r2_summary = {}

for tgt in TARGETS:
    if tgt not in y_train.columns:
        print(f"{tgt:<25}  ---     ---      (sütun yok)")
        continue

    # hedef NaN satırlarını at
    tr_idx = y_train[tgt].dropna().index
    te_idx = y_test[tgt].dropna().index
    if len(tr_idx) < 10 or len(te_idx) < 2:
        print(f"{tgt:<25}  ---     ---      (veri yetersiz)")
        continue

    Xtr, ytr = X_train.loc[tr_idx], y_train.loc[tr_idx, tgt]
    Xte, yte = X_test.loc[te_idx],  y_test.loc[te_idx,  tgt]

    search = RandomizedSearchCV(
        estimator=build_model(),
        param_distributions=param_space,
        n_iter=25,
        cv=cv,
        scoring="r2",
        n_jobs=-1,
        random_state=42,
        verbose=0
    )
    search.fit(Xtr, ytr)
    best = search.best_estimator_
    cv_r2 = search.best_score_
    test_r2 = r2_score(yte, best.predict(Xte))
    r2_summary[tgt] = test_r2

    print(f"{tgt:<25} {cv_r2:6.3f}  {test_r2:7.3f}")

# ---------- Özet tablosu -----------------------------------------------------
print("\n=== Özet ===")
for k, v in r2_summary.items():
    print(f"{k:<25} : {v:7.3f}")
