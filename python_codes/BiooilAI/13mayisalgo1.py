import glob, os, pandas as pd
from catboost import CatBoostRegressor, Pool
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import RepeatedKFold, GridSearchCV
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

DATA_DIR = r"C:\@biyokomurlestirme\python_codes\BiooilAI\ProcessedData"
targets = ["aromatics", "acids", "phenols", "furans", "aldehydeketone"]

for t in targets:
    X_train = pd.read_csv(f"{DATA_DIR}\\processed_data_{t}_X_train.csv")
    y_train = pd.read_csv(f"{DATA_DIR}\\processed_data_{t}_y_train.csv")
    X_test  = pd.read_csv(f"{DATA_DIR}\\processed_data_{t}_X_test.csv")
    y_test  = pd.read_csv(f"{DATA_DIR}\\processed_data_{t}_y_test.csv")

    # isteğe bağlı: NaN göstergesi ekle
    X_train = X_train.assign(**{c+"_nan": X_train[c].isna() for c in X_train.columns})
    X_test  = X_test.assign(**{c+"_nan": X_test[c].isna()  for c in X_test.columns})

    model = CatBoostRegressor(
        loss_function="RMSE",
        verbose=False,
        random_state=42,
        iterations=1000,
        depth=6,
        learning_rate=0.05,
        early_stopping_rounds=30,
    )

    # k-katlı CV hiperparametre araması (opsiyonel)
    cv = RepeatedKFold(n_splits=5, n_repeats=10, random_state=42)
    param_grid = {"depth": [4, 5, 6], "learning_rate": [0.02, 0.05, 0.1]}
    gcv = GridSearchCV(model, param_grid, cv=cv, scoring="neg_mean_absolute_error")
    gcv.fit(X_train, y_train.values.ravel())

    best_model = gcv.best_estimator_
    preds = best_model.predict(X_test)
    print(t, "R2:", r2_score(y_test, preds), "MAE:", mean_absolute_error(y_test, preds))
    joblib.dump(best_model, f"model_{t}.pkl")
