import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
import pyodbc
import warnings
import os
warnings.filterwarnings('ignore')

# ---------- DB bağlantısı ----------
SERVER = "DESKTOP-DRO84HP\\SQLEXPRESS"
DB     = "BIOOIL"
CONN   = pyodbc.connect(f"DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DB};Trusted_Connection=yes")

# ---------- Veri çekme yardımcıları ----------

def _sql(q: str) -> pd.DataFrame:
    return pd.read_sql(q, CONN)

def get_biomass():
    return _sql("""
        SELECT BiomassId,Reference_Id, Carbon, Hydrogen, Nitrogen, Sulfur, Oxygen,
               Ash, Volatiles, FixedCarbon, HHV, [O/C] AS OC, [H/C] AS HC,
               Cellulose, Hemicellulose, Lignin, Holocellulose
        FROM Biomass""")

def get_experiment():
    return _sql("""
        SELECT ExperimentId, Biomass_Id, ProcessTemperature, Duration, GasFlowrate,
               FeedRate, ResidenceTime, CatalystBiomassRatio, Catalyst_Id,
               LiquidOutput
        FROM Experiment""")

def get_biooil():
    return _sql("""
        SELECT BiooilId, Experiment_Id,
               aromatics, aliphatichydrocarbon, acids, alcohols,
               furans, phenols, [aldehyde&ketone] AS aldehyde_ketone
        FROM Biooil""")

def get_catalyst():
    return _sql("""
        SELECT CatalystId, CatalystSymbol, CatalystName, CatalystType_Id,
               Si_over_Al, PoreD, Acidity, SBET, Vtot, MetalRatio
        FROM Catalyst""")

# ---------- Yardımcı fonksiyonlar ----------

def _calculate_oc_hc_ratios(df):
    """Eksik O/C ve H/C değerlerini hesaplar."""
    for col in ['Carbon', 'Oxygen', 'Hydrogen']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    oc_mask = df['OC'].isna()
    df.loc[oc_mask, 'OC'] = df.loc[oc_mask].apply(
        lambda row: round(row['Oxygen'] / row['Carbon'], 6) if pd.notnull(row['Oxygen']) and pd.notnull(row['Carbon']) and row['Carbon'] != 0 else np.nan,
        axis=1
    )
    filled_oc_count = oc_mask.sum() - df['OC'].isna().sum()
    if oc_mask.sum() > 0:
        print(f"Toplam {oc_mask.sum()} eksik O/C değerinden {filled_oc_count} tanesi dolduruldu.")

    hc_mask = df['HC'].isna()
    df.loc[hc_mask, 'HC'] = df.loc[hc_mask].apply(
        lambda row: round(row['Hydrogen'] / row['Carbon'], 6) if pd.notnull(row['Hydrogen']) and pd.notnull(row['Carbon']) and row['Carbon'] != 0 else np.nan,
        axis=1
    )
    filled_hc_count = hc_mask.sum() - df['HC'].isna().sum()
    if hc_mask.sum() > 0:
        print(f"Toplam {hc_mask.sum()} eksik H/C değerinden {filled_hc_count} tanesi dolduruldu.")
    return df

def _impute_missing_values_knn(df):
    """Ash, Volatiles, FixedCarbon, Cellulose, Hemicellulose, Lignin, HHV değerlerini KNN kullanarak impute eder."""
    cols_to_impute = ['Ash', 'Volatiles', 'FixedCarbon', 'Cellulose', 'Hemicellulose', 'Lignin', 'HHV']
    predictor_features = ['OC', 'HC', 'Carbon', 'Hydrogen', 'Oxygen', 'Nitrogen', 'Sulfur']

    actual_cols_to_impute = [col for col in cols_to_impute if col in df.columns]
    actual_predictor_features = [col for col in predictor_features if col in df.columns]
    
    knn_imputation_cols = sorted(list(set(actual_cols_to_impute + actual_predictor_features)))

    if not actual_cols_to_impute:
        print("İstatistiksel yöntemle impute edilecek hedef sütun bulunamadı.")
    elif not actual_predictor_features:
        print("KNN imputasyonu için kullanılacak öznitelik bulunamadı.")
    elif not knn_imputation_cols or len(knn_imputation_cols) < 2:
        print("KNN imputasyonu için yeterli sayıda mevcut sütun bulunamadı.")
    else:
        print(f"\nKNN Imputasyonu başlıyor...")
        print(f"Impute edilecek sütunlar: {actual_cols_to_impute}")
        print(f"Imputasyon için kullanılacak öznitelikler: {knn_imputation_cols}")

        nan_counts_before_knn = df[actual_cols_to_impute].isnull().sum()
        
        for col in knn_imputation_cols:
            if not pd.api.types.is_numeric_dtype(df[col]):
                 df[col] = pd.to_numeric(df[col], errors='coerce')

        imputer = KNNImputer(n_neighbors=5)
        df_knn_subset = df[knn_imputation_cols].copy()

        try:
            imputed_values = imputer.fit_transform(df_knn_subset)
            imputed_values = np.round(imputed_values, 6)
            df_imputed_subset = pd.DataFrame(imputed_values, columns=knn_imputation_cols, index=df_knn_subset.index)
            
            for col in knn_imputation_cols:
                df[col] = df_imputed_subset[col]

            print("KNN imputasyonu tamamlandı.")
            for col in actual_cols_to_impute:
                nans_before = nan_counts_before_knn.get(col, 0)
                nans_after = df[col].isnull().sum()
                filled_knn = nans_before - nans_after
                if nans_before > 0:
                    print(f"'{col}' sütununda {nans_before} eksik değerden {filled_knn} tanesi KNN ile dolduruldu.")
        except Exception as e:
            print(f"KNN Imputasyon sırasında bir hata oluştu: {str(e)}")
    return df

def _calculate_holocellulose(df):
    """Eksik Holocellulose değerlerini Cellulose ve Hemicellulose toplamından hesaplar."""
    if 'Holocellulose' in df.columns and 'Cellulose' in df.columns and 'Hemicellulose' in df.columns:
        holocellulose_missing_before = df['Holocellulose'].isnull().sum()
        if holocellulose_missing_before == 0:
            print("Holocellulose sütununda eksik değer bulunmamaktadır.")
            return df

        mask_missing_holo = df['Holocellulose'].isnull()
        mask_can_calculate = df['Cellulose'].notnull() & df['Hemicellulose'].notnull()
        
        df.loc[mask_missing_holo & mask_can_calculate, 'Holocellulose'] = (
            df.loc[mask_missing_holo & mask_can_calculate, 'Cellulose'] +
            df.loc[mask_missing_holo & mask_can_calculate, 'Hemicellulose']
        )
        
        holocellulose_filled = holocellulose_missing_before - df['Holocellulose'].isnull().sum()
        
        if holocellulose_filled > 0:
            print(f"Toplam {holocellulose_missing_before} eksik Holocellulose değerinden {holocellulose_filled} tanesi Cellulose + Hemicellulose toplamından dolduruldu.")
    return df

def _save_split(X_tr, X_te, y_tr, y_te, prefix):
    """Split edilmiş verileri CSV olarak kaydeder"""
    X_tr.to_csv(f"{prefix}_X_train.csv", index=False)
    X_te.to_csv(f"{prefix}_X_test.csv",  index=False)
    y_tr.to_csv(f"{prefix}_y_train.csv", index=False)
    y_te.to_csv(f"{prefix}_y_test.csv", index=False)

def prepare_datasets(save_dir: str = r"C:\@biyokomurlestirme\python_codes\BiooilAI"):
    # 1) Birleştir
    df = (get_experiment()
            .merge(get_biomass(),  left_on="Biomass_Id",  right_on="BiomassId")
            .merge(get_catalyst(), left_on="Catalyst_Id", right_on="CatalystId", how="left")
            .merge(get_biooil(),   left_on="ExperimentId", right_on="Experiment_Id"))

    # 2) Temizlik
    drop_cols = ["BiomassId", "ExperimentId", "BiooilId", "Experiment_Id",
                 "Biomass_Id", "CatalystId", "CatalystSymbol", "CatalystName"]
    df.drop(columns=drop_cols, inplace=True, errors="ignore")

    # 3) Katalizör tipi kategorik olsun
    df["CatalystType_Id"] = df["CatalystType_Id"].astype(str)

    # 4) Kayıp değer yönetimi
    df = _calculate_oc_hc_ratios(df)
    df = _impute_missing_values_knn(df)
    df = _calculate_holocellulose(df)

    # 5) Giriş / çıkış listeleri
    input_cols = [
        "Reference_Id", "Carbon", "Hydrogen", "Nitrogen", "Sulfur", "Oxygen",
        "Ash", "Volatiles", "FixedCarbon", "HHV", "OC", "HC",
        "ProcessTemperature", "Duration", "GasFlowrate", "CatalystBiomassRatio",
        "Si_over_Al", "PoreD", "Acidity", "SBET", "Vtot", "MetalRatio",
        "CatalystType_Id"
    ]
    output_cols = [
        "aromatics", "acids", "phenols", "furans", "aldehyde_ketone"
    ]

    # 6) Split: önce katalizörlü veriyi ayrı tut, katalizörsüzü 80-20 böl
    X = df[input_cols]
    y = df[output_cols]

    X_cat = X[df["Catalyst_Id"].notna()]
    y_cat = y.loc[X_cat.index]
    X_non = X[df["Catalyst_Id"].isna()]
    y_non = y.loc[X_non.index]

    X_train_nc, X_test, y_train_nc, y_test = train_test_split(
        X_non, y_non, test_size=0.2, random_state=42)

    X_train = pd.concat([X_cat, X_train_nc], ignore_index=True)
    y_train = pd.concat([y_cat, y_train_nc], ignore_index=True)

    # 7) Kaydet
    base = os.path.join(save_dir, "ProcessedData", "processed_data")
    os.makedirs(os.path.dirname(base), exist_ok=True)
    for tgt in output_cols:
        prefix = f"{base}_{tgt}"
        _save_split(X_train, X_test, y_train[[tgt]], y_test[[tgt]], prefix)

    print("✔ Veri setleri kaydedildi (categorical: CatalystType_Id).")

if __name__ == "__main__":
    prepare_datasets() 