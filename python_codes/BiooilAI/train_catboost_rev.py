
# =============================================================
# train_catboost_rev.py  (NaN ve sabit-target sorunu çözüldü)
# =============================================================
import os, numpy as np, pandas as pd, joblib
from catboost import CatBoostRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import GridSearchCV, RepeatedKFold

DATA_DIR = r"C:\@biyokomurlestirme\python_codes\BiooilAI\ProcessedData"
TARGETS   = ["aromatics", "acids", "phenols", "furans", "aldehyde_ketone"]

for tgt in TARGETS:
    X_tr = pd.read_csv(os.path.join(DATA_DIR, f"processed_data_{tgt}_X_train.csv"))
    y_tr = pd.read_csv(os.path.join(DATA_DIR, f"processed_data_{tgt}_y_train.csv"))
    X_te = pd.read_csv(os.path.join(DATA_DIR, f"processed_data_{tgt}_X_test.csv"))
    y_te = pd.read_csv(os.path.join(DATA_DIR, f"processed_data_{tgt}_y_test.csv"))

    # 1) Target NaN satırları at
    mtr = ~y_tr[tgt].isna();  mte = ~y_te[tgt].isna()
    X_train, y_train = X_tr.loc[mtr].reset_index(drop=True), y_tr.loc[mtr].reset_index(drop=True)
    X_test,  y_test  = X_te.loc[mte].reset_index(drop=True), y_te.loc[mte].reset_index(drop=True)

    # 2) Yeterli çeşit yoksa modeli atla
    if y_train[tgt].nunique() < 2:
        print(f"⚠ {tgt}: eğitim setinde tekil hedef yok – model geçildi.")
        continue

    # 3) Kategorik sütunları belirle (string dtype’li)
    for col in ["CatalystType_Id"]:
        if col in X_train.columns:
            X_train[col] = X_train[col].astype(str)
            X_test[col]  = X_test[col].astype(str)
    cat_cols = [c for c in X_train.columns if X_train[c].dtype == "object"]

    # 4) NaN bayrak kolonları (opsiyonel; sorun olmaz)
    X_train = X_train.assign(**{f"{c}_nan": X_train[c].isna().astype(int) for c in X_train.columns})
    X_test  = X_test.assign(**{f"{c}_nan": X_test[c].isna().astype(int)  for c in X_test.columns})

    # 5) CV parametrelerini küçült → sabit hedef katlanmaz
    base_model = CatBoostRegressor(loss_function="RMSE", random_state=42, verbose=False, early_stopping_rounds=25)

    param_grid = {
        "iterations": [400, 800],
        "depth": [4, 6],
        "learning_rate": [0.03, 0.08]
    }

    splits = min(3, len(X_train) - 1)  # en az 2 numune / fold
    cv = RepeatedKFold(n_splits=splits, n_repeats=4, random_state=42)

    gcv = GridSearchCV(base_model, param_grid, cv=cv, scoring="neg_mean_absolute_error", n_jobs=-1, error_score="raise")

    try:
        gcv.fit(X_train, y_train.values.ravel(), cat_features=cat_cols)
    except ValueError as e:
        print(f"⚠ {tgt}: CV sırasında hata – {e}. Varsayılan parametrelerle eğitiliyor…")
        gcv = base_model.fit(X_train, y_train.values.ravel(), cat_features=cat_cols)
        best_model = gcv
    else:
        best_model = gcv.best_estimator_

    preds = best_model.predict(X_test)
    print(f"{tgt:16s}  R²={r2_score(y_test, preds):6.3f}   MAE={mean_absolute_error(y_test, preds):8.4f}")

    joblib.dump(best_model, os.path.join(DATA_DIR, f"catboost_{tgt}.pkl"))

print("✔ Eğitim tamamlandı – modeller kaydedildi.")
