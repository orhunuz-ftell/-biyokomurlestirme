# =============================================================
# PrepareData_outlier.py  (+ z‑score & IQR outlier filter)
# =============================================================
import os, warnings, pyodbc, pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer

warnings.filterwarnings("ignore")

SERVER = "DESKTOP-DRO84HP\\SQLEXPRESS"
DB     = "BIOOIL"
CONN   = pyodbc.connect(f"DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DB};Trusted_Connection=yes")

# -------------------- DB yardımcıları --------------------
_q = lambda q: pd.read_sql(q, CONN)

def get_biomass():
    return _q("SELECT BiomassId, Reference_Id, Carbon, Hydrogen, Nitrogen, Sulfur, Oxygen, Ash, Volatiles, FixedCarbon, HHV, [O/C] AS OC, [H/C] AS HC, Cellulose, Hemicellulose, Lignin, Holocellulose FROM Biomass")

def get_experiment():
    return _q("SELECT ExperimentId, Biomass_Id, ProcessTemperature, Duration, GasFlowrate, FeedRate, ResidenceTime, CatalystBiomassRatio, Catalyst_Id, LiquidOutput FROM Experiment")

def get_biooil():
    return _q("SELECT BiooilId, Experiment_Id, aromatics, aliphatichydrocarbon, acids, alcohols, furans, phenols, [aldehyde&ketone] AS aldehyde_ketone FROM Biooil")

def get_catalyst():
    return _q("SELECT CatalystId, CatalystType_Id, Si_over_Al, PoreD, Acidity, SBET, Vtot, MetalRatio FROM Catalyst")

# -------------------- Yardımcı fonksiyonlar ------------------

def _calculate_oc_hc_ratios(df: pd.DataFrame):
    df["OC"] = df["Oxygen"] / df["Carbon"].replace(0, np.nan)
    df["HC"] = df["Hydrogen"] / df["Carbon"].replace(0, np.nan)
    return df

def _calculate_holocellulose(df: pd.DataFrame):
    if {"Cellulose", "Hemicellulose"}.issubset(df.columns):
        df["Holocellulose"] = df["Cellulose"] + df["Hemicellulose"]
    return df

def _impute_missing_values_knn(df: pd.DataFrame, n_neighbors: int = 3):
    imputer = KNNImputer(n_neighbors=n_neighbors)
    num_cols = df.select_dtypes(include="number").columns
    df[num_cols] = imputer.fit_transform(df[num_cols])
    return df

# ---- Outlier filtresi (Box‑plot IQR + z‑score 3σ) ----

def _remove_outliers(df: pd.DataFrame, numeric_cols: list, z_thresh: float = 3.0):
    mask = np.ones(len(df), dtype=bool)
    for col in numeric_cols:
        x = df[col]
        # IQR yöntemi
        q1, q3 = np.percentile(x, [25, 75])
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        mask &= (x >= low) & (x <= high)
        # Z‑score yöntemi (ek koruma)
        z = (x - x.mean()) / x.std(ddof=0)
        mask &= np.abs(z) <= z_thresh
    removed = (~mask).sum()
    if removed:
        print(f"📉 Outlier filtre: {removed} satır atıldı → {len(df)-removed} satır kaldı")
    return df[mask].reset_index(drop=True)

# -------------------- Ana hazırlık fonksiyonu ------------

def prepare_datasets(save_dir: str = r"C:\@biyokomurlestirme\python_codes\BiooilAI"):
    df = (get_experiment()
            .merge(get_biomass(),  left_on="Biomass_Id",  right_on="BiomassId")
            .merge(get_catalyst(), left_on="Catalyst_Id", right_on="CatalystId", how="left")
            .merge(get_biooil(),   left_on="ExperimentId", right_on="Experiment_Id"))

    df.drop(columns=["BiomassId", "ExperimentId", "BiooilId", "Experiment_Id", "Biomass_Id", "CatalystId"], inplace=True, errors="ignore")

    # Katalizör tipi kategorik
    df["CatalystType_Id"] = df["CatalystType_Id"].astype(str)

    df = _calculate_oc_hc_ratios(df)
    df = _calculate_holocellulose(df)
    df = _impute_missing_values_knn(df)

    # Outlier temizliği (yalnızca sayısal kolonlar)
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    df = _remove_outliers(df, numeric_cols)

    # Split & save
    input_cols  = [c for c in df.columns if c not in ["aromatics", "acids", "phenols", "furans", "aldehyde_ketone"]]
    output_cols = ["aromatics", "acids", "phenols", "furans", "aldehyde_ketone"]
    X, y = df[input_cols], df[output_cols]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    out_dir = os.path.join(save_dir, "ProcessedData")
    os.makedirs(out_dir, exist_ok=True)
    for tgt in output_cols:
        prefix = os.path.join(out_dir, f"processed_data_{tgt}")
        X_train.to_csv(f"{prefix}_X_train.csv", index=False)
        X_test.to_csv( f"{prefix}_X_test.csv",  index=False)
        y_train[[tgt]].to_csv(f"{prefix}_y_train.csv", index=False)
        y_test[[tgt]].to_csv( f"{prefix}_y_test.csv",  index=False)
    print("✔ Dataset hazırlandı & kaydedildi (outlier filtreli)")

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    prepare_datasets()