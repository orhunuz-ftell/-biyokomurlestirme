
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
import pyodbc
import warnings
warnings.filterwarnings('ignore')

# SQL Server bağlantı bilgileri
server = 'DESKTOP-DRO84HP\\SQLEXPRESS'
database = 'BIOOIL'

# SQL Server'a bağlanma
try:
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes')
    print("Veritabanı bağlantısı başarılı!")
except Exception as e:
    print(f"Bağlantı hatası: {str(e)}")

# Veri çekme fonksiyonları
def get_biomass_data():
    """Biomass tablosundan verileri çeker"""
    query = """
    SELECT BiomassId,Reference_Id, Carbon, Hydrogen, Nitrogen, Sulfur, Oxygen, 
           Ash, Volatiles, FixedCarbon, HHV, [O/C], [H/C], Cellulose, Hemicellulose, Lignin, Holocellulose
    FROM Biomass
    """
    return pd.read_sql(query, conn)

def get_experiment_data():
    """Experiment tablosundan verileri çeker"""
    query = """
    SELECT ExperimentId, Biomass_Id, 
           ProcessTemperature, Duration,GasFlowrate
            FeedRate,  ResidenceTime,
              CatalystBiomassRatio,Catalyst_Id,
              LiquidOutput
    FROM Experiment
    """
    
    return pd.read_sql(query, conn)

def get_biooil_data():
    """Biooil tablosundan FTIR değerlerini çeker"""
    query = """
    SELECT BiooilId, Experiment_Id,
           aromatics, aliphatichydrocarbon, acids, alcohols,
            furans, phenols, [aldehyde&ketone] as aldehyde_ketone,
           esters ,oxides, sugar,guaiacol,syringol,catechol,[N-containing] as N_containing
        
    FROM Biooil where BiooilId <19
    """
    #   ester,oxides
    return pd.read_sql(query, conn)

def get_catalyst_data():
    """Catalyst tablosundan verileri çeker"""
    query = """
    SELECT CatalystId, CatalystSymbol, CatalystName, CatalystType_Id,
           Si_over_Al, PoreD, Acidity, SBET, Vtot, MetalRatio
    FROM Catalyst
    """
    return pd.read_sql(query, conn)

# Verileri çekme ve birleştirme
def merge_all_data():
    """Tüm tabloları birleştirir"""
    try:
        biomass_df = get_biomass_data()
        experiment_df = get_experiment_data()
        biooil_df = get_biooil_data()
        catalyst_df = get_catalyst_data()
        print("Veriler başarıyla çekildi!")
        
        # Önce experiment ve biomass tablolarını birleştir
        merged_df = pd.merge(
            experiment_df,
            biomass_df,
            left_on='Biomass_Id',
            right_on='BiomassId',
            how='inner'
        )
        
        # Sonra catalyst tablosunu experiment verisiyle birleştir
        merged_df = pd.merge(
            merged_df,
            catalyst_df,
            left_on='Catalyst_Id',
            right_on='CatalystId',
            how='left'
        )
        
        # Sonra biooil tablosunu ekle
        final_df = pd.merge(
            merged_df,
            biooil_df,
            left_on='ExperimentId',
            right_on='Experiment_Id',
            how='inner'
        )
        
        return final_df
    except Exception as e:
        print(f"Veri birleştirme hatası: {str(e)}")
        return None

def _calculate_oc_hc_ratios(df):
    """Eksik O/C ve H/C değerlerini hesaplar."""
    # Ensure Carbon, Oxygen, Hydrogen are numeric and handle potential division by zero
    for col in ['Carbon', 'Oxygen', 'Hydrogen']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fill O/C
    # Assuming df has 'O/C' (not '[O/C]') based on user feedback
    oc_mask = df['O/C'].isna()
    df.loc[oc_mask, 'O/C'] = df.loc[oc_mask].apply(
        lambda row: round(row['Oxygen'] / row['Carbon'], 6) if pd.notnull(row['Oxygen']) and pd.notnull(row['Carbon']) and row['Carbon'] != 0 else np.nan,
        axis=1
    )
    filled_oc_count = oc_mask.sum() - df['O/C'].isna().sum()
    if oc_mask.sum() > 0: # Only print if there were initial NaNs to process
        print(f"Toplam {oc_mask.sum()} eksik O/C değerinden {filled_oc_count} tanesi dolduruldu.")

    # Fill H/C
    # Assuming df has 'H/C' (not '[H/C]') based on user feedback
    hc_mask = df['H/C'].isna()
    df.loc[hc_mask, 'H/C'] = df.loc[hc_mask].apply(
        lambda row: round(row['Hydrogen'] / row['Carbon'], 6) if pd.notnull(row['Hydrogen']) and pd.notnull(row['Carbon']) and row['Carbon'] != 0 else np.nan,
        axis=1
    )
    filled_hc_count = hc_mask.sum() - df['H/C'].isna().sum()
    if hc_mask.sum() > 0: # Only print if there were initial NaNs to process
        print(f"Toplam {hc_mask.sum()} eksik H/C değerinden {filled_hc_count} tanesi dolduruldu.")
    return df

def _impute_missing_values_knn(df):
    """Ash, Volatiles, FixedCarbon, Cellulose, Hemicellulose, Lignin, HHV değerlerini KNN kullanarak impute eder."""
    cols_to_impute = ['Ash', 'Volatiles', 'FixedCarbon', 'Cellulose', 'Hemicellulose', 'Lignin', 'HHV']
    
    # # Ensure Cellulose, Hemicellulose, Lignin are numeric for imputation
    # additional_numeric_cols = ['Cellulose', 'Hemicellulose', 'Lignin']
    # for col in additional_numeric_cols:
    #     if col in df.columns:
    #         if not pd.api.types.is_numeric_dtype(df[col]):
    #             try:
    #                 df[col] = df[col].astype(str).str.strip()
    #                 df[col] = df[col].str.replace(',', '.')
    #                 df[col] = df[col].str.replace(r'[^\\d\\.-]', '', regex=True) 
    #                 df[col] = pd.to_numeric(df[col], errors='coerce')
    #                 print(f"{col} sütunu (KNN imputasyonu için) sayısala çevrildi.")
    #             except Exception as e:
    #                 print(f"{col} sütununda (KNN imputasyonu için) sayısala çevirme hatası: {str(e)}")
    #     else:
    #         print(f"Uyarı: '{col}' sütunu DataFrame'de bulunamadı ve KNN imputasyonundan önce numerik çevrimde atlanacak.")

    predictor_features = ['O/C', 'H/C', 'Carbon', 'Hydrogen', 'Oxygen', 'Nitrogen', 'Sulfur']

    actual_cols_to_impute = [col for col in cols_to_impute if col in df.columns]
    actual_predictor_features = [col for col in predictor_features if col in df.columns]
    
    knn_imputation_cols = sorted(list(set(actual_cols_to_impute + actual_predictor_features)))

    if not actual_cols_to_impute:
        print("İstatistiksel yöntemle impute edilecek hedef sütun (Ash, Volatiles vb.) bulunamadı.")
    elif not actual_predictor_features:
        print("KNN imputasyonu için kullanılacak öznitelik ([O/C], [H/C] vb.) bulunamadı.")
    elif not knn_imputation_cols or len(knn_imputation_cols) < 2:
        print("KNN imputasyonu için yeterli sayıda (en az 2) mevcut sütun bulunamadı.")
    else:
        print(f"\nKNN Imputasyonu başlıyor...")
        print(f"Impute edilecek sütunlar: {actual_cols_to_impute}")
        print(f"Imputasyon için kullanılacak öznitelikler (ve impute edilecekler): {knn_imputation_cols}")

        nan_counts_before_knn = df[actual_cols_to_impute].isnull().sum()
        
        for col in knn_imputation_cols:
            if not pd.api.types.is_numeric_dtype(df[col]):
                 df[col] = pd.to_numeric(df[col], errors='coerce')
                 if df[col].isnull().all():
                     print(f"Uyarı: KNN için hazırlanan '{col}' sütunu tamamen NaN değerlerden oluşuyor.")

        imputer = KNNImputer(n_neighbors=5)
        
        original_index = df.index
        df_knn_subset = df[knn_imputation_cols].copy()

        try:
            imputed_values = imputer.fit_transform(df_knn_subset)
            # Round imputed values to 6 decimal places
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
                if nans_after > 0:
                    print(f"UYARI: '{col}' sütununda KNN imputasyonu sonrası hala {nans_after} eksik değer var.")
        except Exception as e:
            print(f"KNN Imputasyon sırasında bir hata oluştu: {str(e)}")
            print("DataFrame'in ilgili alt kümesi:")
            print(df[knn_imputation_cols].info())
            print(df[knn_imputation_cols].head())
    return df

def _calculate_holocellulose(df):
    """Eksik Holocellulose değerlerini Cellulose ve Hemicellulose toplamından hesaplar."""
    if 'Holocellulose' in df.columns and 'Cellulose' in df.columns and 'Hemicellulose' in df.columns:
        holocellulose_missing_before = df['Holocellulose'].isnull().sum()
        if holocellulose_missing_before == 0:
            print("Holocellulose sütununda eksik değer bulunmamaktadır.")
            return df

        # Calculate Holocellulose for rows where it's missing and Cellulose/Hemicellulose are available
        mask_missing_holo = df['Holocellulose'].isnull()
        mask_can_calculate = df['Cellulose'].notnull() & df['Hemicellulose'].notnull()
        
        df.loc[mask_missing_holo & mask_can_calculate, 'Holocellulose'] = (
            df.loc[mask_missing_holo & mask_can_calculate, 'Cellulose'] +
            df.loc[mask_missing_holo & mask_can_calculate, 'Hemicellulose']
        )
        
        holocellulose_filled = holocellulose_missing_before - df['Holocellulose'].isnull().sum()
        
        if holocellulose_filled > 0:
            print(f"Toplam {holocellulose_missing_before} eksik Holocellulose değerinden {holocellulose_filled} tanesi Cellulose + Hemicellulose toplamından dolduruldu.")
        else:
            print(f"Holocellulose sütunundaki {holocellulose_missing_before} eksik değer için Cellulose ve/veya Hemicellulose değerleri de eksik olduğundan hesaplama yapılamadı.")
            
        remaining_nans = df['Holocellulose'].isnull().sum()
        if remaining_nans > 0:
            print(f"UYARI: Holocellulose sütununda hala {remaining_nans} eksik değer bulunmaktadır.")
    else:
        print("Uyarı: Holocellulose, Cellulose veya Hemicellulose sütunlarından biri DataFrame'de bulunamadı. Holocellulose hesaplaması atlandı.")
    return df

def _calculate_duration_and_cleanup(df, total_biomass):
    """Duration değerini hesaplar ve gereksiz sütunları kaldırır."""
    # Duration null olan satırları tespit et
    mask = df['Duration'].isna()
    
    # Duration null olan satırlar için hesaplama yap
    df.loc[mask, 'Duration'] = df.loc[mask].apply(
        lambda row: ((total_biomass / row['FeedRate']) + row['ResidenceTime'])
        if pd.notnull(row['ResidenceTime']) and pd.notnull(row['FeedRate'])
        else row['Duration'],
        axis=1
    )
    
    # Hesaplama sonrası kontrol ve raporlama
    filled_count = mask.sum() - df['Duration'].isna().sum()
    print(f"Toplam {mask.sum()} eksik Duration değerinden {filled_count} tanesi dolduruldu.")
    
    # Artık FeedRate ve ResidenceTime'a ihtiyaç yok
    df = df.drop(['FeedRate', 'ResidenceTime'], axis=1, errors='ignore') # Added errors='ignore'
    return df

def process_data(df, total_biomass=100):
    """
    Veri işleme adımlarını yönetir: [O/C], [H/C] hesaplama, KNN imputasyonu ve Duration hesaplama.
    
    Parameters:
    -----------
    df : DataFrame
        İşlenecek veri seti
    total_biomass : float
        Toplam biyokütle miktarı (gram), varsayılan 100g
    """
    df = _calculate_oc_hc_ratios(df)
    df = _impute_missing_values_knn(df)
    df = _calculate_holocellulose(df)
    #df = _calculate_duration_and_cleanup(df, total_biomass)
    
    return df

def clean_numeric_data(df):
    """Sayısal sütunlardaki string değerleri temizler ve float'a çevirir"""
    numeric_columns = [
        'Carbon', 'Hydrogen', 'Nitrogen', 'Sulfur', 'Oxygen',
        'Ash', 'Volatiles', 'FixedCarbon', 'HHV',
        'ProcessTemperature', 'GasFlowrate', 'Duration',
        'CatalystBiomassRatio', 'LiquidOutput', 'aromatics', 
        'aliphatichydrocarbon', 'acids', 'alcohols', 'esters', 
        'furans', 'phenols', 'aldehyde_ketone', 'oxides', 'sugar',
        'Si_over_Al', 'PoreD', 'Acidity', 'SBET', 'Vtot', 'MetalRatio'
    ]
    
    for col in numeric_columns:
        if col in df.columns:
            try:
                df[col] = df[col].astype(str).str.strip()
                df[col] = df[col].str.replace(',', '.')
                df[col] = df[col].str.replace('[^\d\.-]', '', regex=True)
                df[col] = pd.to_numeric(df[col], errors='coerce')
                print(f"{col} sütunu başarıyla sayısala çevrildi.")
            except Exception as e:
                print(f"{col} sütununda hata: {str(e)}")
    
    return df

def normalize_features(df):
    """Özellikleri standartlaştırır"""
    df = clean_numeric_data(df)
    df = process_data(df)
    
    scaler = StandardScaler()
    
    # Giriş değişkenleri (features)
    input_columns = [
        'Carbon', 'Hydrogen', 'Nitrogen', 'Sulfur', 'Oxygen',
        'Ash', 'Volatiles', 'FixedCarbon', 'HHV',
        'O/C', 'H/C',
        'ProcessTemperature', 'Duration','ResidenceTime',
        'CatalystBiomassRatio',
        'Si_over_Al', 'PoreD', 'Acidity'
    ]
    
    # Çıkış değişkenleri (targets)
    output_columns = [
        'aromatics',
        'acids', 'alcohols', 'furans', 'phenols',
        'aldehyde_ketone'
    ]
    
    # Eksik değerleri kontrol et
    print("\nEksik değer sayıları:")
    print(df[input_columns + output_columns].isnull().sum())
    
    # Giriş değişkenlerindeki kalan eksik değerleri ortalama ile doldur
    df_input_subset = df[input_columns].copy()
    
    # ResidenceTime'ı Duration'un min-max değerleri arasına ölçekle
    if 'ResidenceTime' in input_columns and 'Duration' in input_columns:
        duration_min = df_input_subset['Duration'].min()
        duration_max = df_input_subset['Duration'].max()
        
        # ResidenceTime'ı Duration'un min-max aralığına ölçekle
        if df_input_subset['ResidenceTime'].isnull().any():
            mean_val = round(df_input_subset['ResidenceTime'].mean(), 6)
            df_input_subset['ResidenceTime'].fillna(mean_val, inplace=True)
            print(f"ResidenceTime sütunundaki eksik değerler ortalama ({mean_val:.6f}) ile dolduruldu.")
        
        residence_min = df_input_subset['ResidenceTime'].min()
        residence_max = df_input_subset['ResidenceTime'].max()
        
        df_input_subset['ResidenceTime'] = round(((df_input_subset['ResidenceTime'] - residence_min) * 
                                          (duration_max - duration_min) / 
                                          (residence_max - residence_min) + 
                                          duration_min), 6)
        
        print(f"ResidenceTime sütunu Duration'un min-max aralığına ölçeklendi (Duration min: {duration_min:.6f}, max: {duration_max:.6f})")

    df[input_columns] = df_input_subset

    # Duration ve ResidenceTime'ı birleştir
    if 'Duration' in input_columns and 'ResidenceTime' in input_columns:
        print("Duration null olan satırlar için ResidenceTime değeri atanıyor...")
        # Duration null olan satırlar için ResidenceTime değerini ata
        df.loc[df['Duration'].isnull(), 'Duration'] = df.loc[df['Duration'].isnull(), 'ResidenceTime']
        df.drop('ResidenceTime', axis=1, inplace=True)
        
        # Birleştirme sonrası kalan Duration NaN'leri ortalama ile doldur
        if df['Duration'].isnull().any():
            mean_duration = round(df['Duration'].mean(), 6)
            df['Duration'].fillna(mean_duration, inplace=True)
            print(f"Birleştirme sonrası kalan Duration eksik değerleri ortalama ({mean_duration:.6f}) ile dolduruldu.")
        
        input_columns.remove('ResidenceTime')
        print("Birleştirme sonrası 'ResidenceTime' DataFrame'den kaldırıldı ve input_columns listesi güncellendi.")

    # Çıkış değişkenlerindeki eksik değerleri ortalama ile doldur
    existing_output_columns = [col for col in output_columns if col in df.columns]
    if len(existing_output_columns) != len(output_columns):
         missing_cols = set(output_columns) - set(existing_output_columns)
         print(f"Uyarı: Bazı beklenen output sütunları DataFrame'de bulunamadı ve atlanacak: {missing_cols}. Mevcut olanlar: {existing_output_columns}")
         output_columns = existing_output_columns

    # LiquidOutput için ortalama ile doldurma
    if 'LiquidOutput' in output_columns and df['LiquidOutput'].isnull().any():
        mean_val = round(df['LiquidOutput'].mean(), 6)
        df['LiquidOutput'].fillna(mean_val, inplace=True)

    return df, input_columns, output_columns, scaler

def prepare_data():
    """Tüm veri hazırlama sürecini yönetir"""
    merged_data = merge_all_data()
    if merged_data is None:
        return None, None, None, None, None # Added None for scaler
    
    cleaned_data = merged_data.drop(
        ['BiomassId', 'ExperimentId', 'BiooilId', 'Experiment_Id', 'Biomass_Id', 
         'CatalystId', 'CatalystSymbol', 'CatalystName', 'CatalystType_Id'],  # Catalyst_Id'yi tutuyoruz
        axis=1, 
        errors='ignore'
    )
    
    normalized_data, input_cols, output_cols, scaler = normalize_features(cleaned_data)
    
    if not input_cols: # Check if input_cols is empty
        print("Hata: Normalizasyon sonrası hiçbir giriş sütunu elde edilemedi. İşlem durduruluyor.")
        return None, None, None, None, None

    # Ensure X and y are not empty before splitting
    if normalized_data[input_cols].empty or normalized_data[output_cols].empty:
        print("Hata: Giriş (X) veya çıkış (y) verileri boş. Eğitim/test ayırma işlemi yapılamıyor.")
        return None, None, None, None, None

    
    # Catalyst_Id'yi input_cols'dan çıkar
    if 'Catalyst_Id' in input_cols:
        input_cols.remove('Catalyst_Id')
    
    # Catalyst verilerini eğitim setine al (tamamı)
    X = normalized_data[input_cols]
    y = normalized_data[output_cols]
    

    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )




    
    save_processed_data(X_train, X_test, y_train, y_test)
    
    print("\nVeri seti boyutları:")
    print(f"Eğitim seti (X): {X_train.shape}")
    print(f"Test seti (X): {X_test.shape}")
    print(f"Eğitim seti (y): {y_train.shape}")
    print(f"Test seti (y): {y_test.shape}")
    
    # Catalyst dağılımını göster
    print("\nCatalyst dağılımı:")
    
    return X_train, X_test, y_train, y_test, scaler

def save_processed_data(X_train, X_test, y_train, y_test, file_prefix='C:\@biyokomurlestirme\python_codes\mayis\ProcessedData'):
    """İşlenmiş verileri CSV dosyaları olarak kaydeder"""
    X_train.to_csv(f'{file_prefix}_X_train.csv', index=False)
    X_test.to_csv(f'{file_prefix}_X_test.csv', index=False)
    y_train.to_csv(f'{file_prefix}_y_train.csv', index=False)
    y_test.to_csv(f'{file_prefix}_y_test.csv', index=False)
    print("İşlenmiş veriler başarıyla kaydedildi!")

# Ana çalıştırma kodu
if __name__ == "__main__":
    X_train, X_test, y_train, y_test, scaler = prepare_data()