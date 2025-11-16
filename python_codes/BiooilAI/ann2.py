# Veri manipülasyonu ve analizi için gerekli kütüphaneler
import pandas as pd  # Veri çerçeveleri (DataFrame) oluşturmak ve yönetmek için
import numpy as np   # Numerik hesaplamalar ve diziler için

# Makine öğrenmesi için gerekli kütüphaneler
from sklearn.preprocessing import StandardScaler  # Veri normalizasyonu için
from sklearn.model_selection import train_test_split  # Veri setini eğitim/test olarak bölmek için

# Veritabanı bağlantısı için gerekli kütüphane
import pyodbc  # SQL Server veritabanına bağlanmak için

# Uyarı mesajlarını yönetmek için
import warnings
warnings.filterwarnings('ignore')  # Gereksiz uyarı mesajlarını gizle

# SQL Server bağlantı ayarları
# Yerel veritabanı sunucusu ve BIOOIL veritabanı kullanılıyor
server = 'DESKTOP-DRO84HP\SQLEXPRESS'
database = 'BIOOIL'

# SQL Server bağlantısını Windows kimlik doğrulaması ile gerçekleştir
try:
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes')
    print("Veritabanı bağlantısı başarılı!")
except Exception as e:
    print(f"Bağlantı hatası: {str(e)}")

def get_biomass_data():
    """
    Biomass tablosundan biyokütle özelliklerini çeker
    
    Returns:
    --------
    DataFrame : Biyokütlenin elementel, kısa ve ısıl analiz sonuçlarını içeren veri seti
        - Carbon, Hydrogen, Nitrogen vb.: Elementel analiz sonuçları (%)
        - Ash, Volatiles, FixedCarbon: Kısa analiz sonuçları (%)
        - HHV: Yüksek ısıl değer (MJ/kg)
    """
    query = """
    SELECT BiomassId, Carbon, Hydrogen, Nitrogen, Sulfur, Oxygen, 
           Ash, Voltalies as Volatiles, FixedCarbon, HHV
    FROM Biomass
    """
    return pd.read_sql(query, conn)

def get_experiment_data():
    """
    Experiment tablosundan piroliz deney verilerini çeker
    
    Returns:
    --------
    DataFrame : Piroliz deney koşulları ve çıktılarını içeren veri seti
        - ProcessTemperature: Piroliz sıcaklığı (°C)
        - FeedRate: Besleme hızı (g/dk)
        - GasFlowrate: Gaz akış hızı (ml/dk)
        - Duration: İşlem süresi (dk)
        - ResidenceTime: Kalış süresi (dk)
        - CatalystBiomassRatio: Katalizör/Biyokütle oranı
        - LiquidOutput: Sıvı ürün verimi (%)
    """
    query = """
    SELECT ExperimentId, Biomass_Id, 
           ProcessTemperature, FeedRate, GasFlowrate,
           Duration, ResidenceTime, CatalystBiomassRatio,
           LiquidOutput
    FROM Experiment
    """
    return pd.read_sql(query, conn)

def get_biooil_data():
    """
    Biooil tablosundan FTIR analiz sonuçlarını çeker
    
    Returns:
    --------
    DataFrame : Biyoyağın FTIR analiz sonuçlarını içeren veri seti
        - aromatics: Aromatik bileşikler (%)
        - aliphatichydrocarbon: Alifatik hidrokarbonlar (%)
        - acids: Asitler (%)
        vb. fonksiyonel grupların yüzdeleri
    """
    query = """
    SELECT BiooilId, Experiment_Id,
           aromatics, aliphatichydrocarbon, acids, alcohols,
           esters, furans, phenols, [aldehyde&ketone] as aldehyde_ketone,
           oxides, sugar
    FROM Biooil
    """
    return pd.read_sql(query, conn)

def merge_all_data():
    """
    Tüm tabloları birleştirerek tek bir veri seti oluşturur    
    İşlem Adımları:
    1. Biomass, Experiment ve Biooil tablolarından verileri çeker
    2. Experiment-Biomass tablolarını Biomass_Id üzerinden birleştirir
    3. Oluşan tabloyu Biooil tablosuyla ExperimentId üzerinden birleştirir    
    Returns:
    --------
    DataFrame : Tüm özellikleri içeren birleştirilmiş veri seti
    """
    try:
        biomass_df = get_biomass_data()
        experiment_df = get_experiment_data()
        biooil_df = get_biooil_data()
        print("Veriler başarıyla çekildi!")
        
        # İlk birleştirme: Experiment-Biomass
        merged_df = pd.merge(
            experiment_df,
            biomass_df,
            left_on='Biomass_Id',
            right_on='BiomassId',
            how='inner'
        )
        
        # İkinci birleştirme: (Experiment-Biomass)-Biooil
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

def process_residence_time(df, total_biomass=100):
    """
    FeedRate ve ResidenceTime verilerini Duration'a dönüştürür
    
    Dönüşüm formülü:
    Duration = (Toplam Biyokütle / FeedRate) + ResidenceTime
    
    Parameters:
    -----------
    df : DataFrame
        İşlenecek veri seti
    total_biomass : float
        Varsayılan biyokütle miktarı (100g)
        
    Returns:
    --------
    DataFrame : FeedRate ve ResidenceTime sütunları kaldırılmış,
               Duration değerleri hesaplanmış veri seti
    """
    mask = df['Duration'].isna()
    
    df.loc[mask, 'Duration'] = df.loc[mask].apply(
        lambda row: ((total_biomass / row['FeedRate']) + row['ResidenceTime'])
        if pd.notnull(row['ResidenceTime']) and pd.notnull(row['FeedRate'])
        else row['Duration'],
        axis=1
    )
    
    filled_count = mask.sum() - df['Duration'].isna().sum()
    print(f"Toplam {mask.sum()} eksik Duration değerinden {filled_count} tanesi dolduruldu.")
    
    df = df.drop(['FeedRate', 'ResidenceTime'], axis=1)
    
    return df

def clean_numeric_data(df):
    """
    Sayısal sütunlardaki string değerleri temizler ve sayısal formata çevirir
    
    İşlem Adımları:
    1. Boşlukları temizler
    2. Türkçe ondalık ayracı olan virgülü noktaya çevirir
    3. Sayısal olmayan karakterleri kaldırır
    4. String değerleri float tipine dönüştürür
    
    Parameters:
    -----------
    df : DataFrame
        Temizlenecek veri seti
        
    Returns:
    --------
    DataFrame : Sayısal değerleri temizlenmiş veri seti
    """
    numeric_columns = [
        'Carbon', 'Hydrogen', 'Nitrogen', 'Sulfur', 'Oxygen',
        'Ash', 'Volatiles', 'FixedCarbon', 'HHV',
        'ProcessTemperature', 'GasFlowrate', 'Duration',
        'CatalystBiomassRatio', 'LiquidOutput', 'aromatics', 
        'aliphatichydrocarbon', 'acids', 'alcohols', 'esters', 
        'furans', 'phenols', 'aldehyde_ketone', 'oxides', 'sugar'
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
    """    Özellikleri standartlaştırır ve eksik değerleri doldurur    
    İşlem Adımları:
    1. Sayısal verileri temizler
    2. Residence time hesaplamalarını yapar
    3. Giriş değişkenlerini StandardScaler ile normalize eder
    4. Eksik değerleri ortalama ile doldurur    
    Parameters: df : DataFrame (İşlenecek veri seti)
    --------
    Returns:    tuple : (normalized_df, input_columns, output_columns, scaler)
        - normalized_df: Normalize edilmiş veri seti
        - input_columns: Giriş değişkenlerinin listesi
        - output_columns: Çıkış değişkenlerinin listesi
        - scaler: Kullanılan StandardScaler nesnesi"""
    df = clean_numeric_data(df)
    df = process_residence_time(df)
    
    scaler = StandardScaler()
    
    # Giriş değişkenleri (biyokütle özellikleri ve proses koşulları)
    input_columns = ['Carbon', 'Hydrogen', 'Nitrogen', 'Sulfur', 'Oxygen', 'Ash', 'Volatiles', 'FixedCarbon', 
                     'HHV', 'ProcessTemperature', 'GasFlowrate', 'Duration', 'CatalystBiomassRatio']
    
    # Çıkış değişkenleri (sıvı ürün verimi ve FTIR değerleri)
    output_columns = ['LiquidOutput', 'aromatics', 'aliphatichydrocarbon','acids', 'alcohols', 'esters', 
                      'furans', 'phenols','aldehyde_ketone', 'oxides', 'sugar']
    
    # Eksik değerleri kontrol et ve raporla
    print("\nEksik değer sayıları:")
    print(df[input_columns + output_columns].isnull().sum())
    
    # Giriş değişkenlerini normalize et
    df_input = df[input_columns].fillna(df[input_columns].mean())
    df[input_columns] = scaler.fit_transform(df_input)
    
    # Çıkış değişkenlerindeki eksik değerleri doldur
    df[output_columns] = df[output_columns].fillna(df[output_columns].mean())
    
    return df, input_columns, output_columns, scaler

def prepare_data():
    """Tüm veri hazırlama sürecini yönetir    
    İşlem Adımları:
    1. Verileri birleştirir
    2. Gereksiz sütunları temizler
    3. Verileri normalize eder
    4. Eğitim ve test setlerine ayırır
    5. İşlenmiş verileri kaydeder    
    Returns:
    tuple : (X_train, X_test, y_train, y_test, scaler)
        Makine öğrenmesi modeli için hazırlanmış veri setleri"""
    # Verileri birleştir
    merged_data = merge_all_data()
    if merged_data is None:
        return None, None, None, None
    
    # Gereksiz kolonları temizle
    cleaned_data = merged_data.drop(['BiomassId', 'ExperimentId', 'BiooilId', 'Experiment_Id', 'Biomass_Id'], 
        axis=1, errors='ignore')
    
    # Verileri normalize et
    normalized_data, input_cols, output_cols, scaler = normalize_features(cleaned_data)
    
    # Eğitim ve test setlerine ayır
    X = normalized_data[input_cols]
    y = normalized_data[output_cols]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Sonuçları kaydet
    save_processed_data(X_train, X_test, y_train, y_test)
    
    # Veri seti boyutlarını göster
    print("\nVeri seti boyutları:")
    print(f"Eğitim seti (X): {X_train.shape}")
    print(f"Test seti (X): {X_test.shape}")
    print(f"Eğitim seti (y): {y_train.shape}")
    print(f"Test seti (y): {y_test.shape}")
    
    return X_train, X_test, y_train, y_test, scaler

def save_processed_data(X_train, X_test, y_train, y_test, file_prefix='processed_data'):
    """
    İşlenmiş verileri CSV dosyaları olarak kaydeder
    
    Parameters:
    -----------
    X_train, X_test : DataFrame
        Eğitim ve test setlerinin giriş değişkenleri
    y_train, y_test : DataFrame
        Eğitim ve test setlerinin çıkış değişkenleri
    file_prefix : str
        Kaydedilecek dosyaların ön eki
    """
    X_train.to_csv(f'{file_prefix}_X_train.csv', index=False)
    X_test.to_csv(f'{file_prefix}_X_test.csv', index=False)
    y_train.to_csv(f'{file_prefix}_y_train.csv', index=False)
    y_test.to_csv(f'{file_prefix}_y_test.csv', index=False)
    print("İşlenmiş veriler başarıyla kaydedildi!")

    # Ana çalıştırma kodu
if __name__ == "__main__":
    X_train, X_test, y_train, y_test, scaler = prepare_data()