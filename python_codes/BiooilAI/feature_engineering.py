import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.ensemble import RandomForestRegressor
import seaborn as sns
import matplotlib.pyplot as plt

def load_data():
    # Veri yükleme
    X_train = pd.read_csv('processed_data_X_train.csv')
    y_train = pd.read_csv('processed_data_y_train.csv')
    X_test = pd.read_csv('processed_data_X_test.csv')
    y_test = pd.read_csv('processed_data_y_test.csv')
    return X_train, y_train, X_test, y_test

def create_new_features(X):
    """Yeni özellikler oluştur"""
    X_new = X.copy()
    
    # 1. Karbon bazlı oranlar
    if all(col in X.columns for col in ['FixedCarbon', 'Volatiles']):
        X_new['CarbonRatio'] = X['FixedCarbon'] / (X['FixedCarbon'] + X['Volatiles'])
    
    # 2. Sıcaklık ve süre etkileşimi
    if all(col in X.columns for col in ['ProcessTemperature', 'Duration']):
        X_new['TempDuration'] = X['ProcessTemperature'] * X['Duration']
    
    # 3. Katalizör etkileşimleri
    if all(col in X.columns for col in ['CatalystBiomassRatio', 'ProcessTemperature']):
        X_new['CatalystTemp'] = X['CatalystBiomassRatio'] * X['ProcessTemperature']
    
    # 4. Kimyasal özellikler
    if all(col in X.columns for col in ['O/C', 'H/C']):
        X_new['O_H_Ratio'] = X['O/C'] / X['H/C']
    
    return X_new

def analyze_features(X, y):
    """Özellik analizi ve görselleştirme"""
    # Korelasyon matrisi
    corr_matrix = X.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Özellikler Arası Korelasyon Matrisi')
    plt.tight_layout()
    plt.savefig('correlation_matrix.png')
    plt.close()
    
    # Random Forest özellik önemleri
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='importance', y='feature', data=feature_importance)
    plt.title('Özellik Önemleri')
    plt.tight_layout()
    plt.savefig('feature_importance.png')
    plt.close()
    
    return feature_importance

def select_features_per_target(X, y, k=10):
    """Her hedef için en önemli k özelliği seç"""
    results = {}
    for target in y.columns:
        selector = SelectKBest(score_func=f_regression, k=min(k, X.shape[1]))
        X_selected = selector.fit_transform(X, y[target])
        selected_features = X.columns[selector.get_support()].tolist()
        results[target] = selected_features
    return results

def main():
    # Veriyi yükle
    X_train, y_train, X_test, y_test = load_data()
    
    # Eksik değerleri doldur
    imputer = SimpleImputer(strategy='median')
    X_train_imputed = pd.DataFrame(
        imputer.fit_transform(X_train),
        columns=X_train.columns
    )
    X_test_imputed = pd.DataFrame(
        imputer.transform(X_test),
        columns=X_test.columns
    )
    
    # Yeni özellikler oluştur
    X_train_new = create_new_features(X_train_imputed)
    X_test_new = create_new_features(X_test_imputed)
    
    # Özellik analizi yap
    feature_importance = analyze_features(X_train_new, y_train)
    print("\nÖzellik Önemleri:")
    print(feature_importance)
    
    # Her hedef için en iyi özellikleri bul
    k = 10  # İsterseniz değiştirin
    per_target_features = select_features_per_target(X_train_new, y_train, k=k)
    print("\nHer hedef için en iyi özellikler:")
    for target, features in per_target_features.items():
        print(f"{target}: {features}")
    
    # Sonuçları CSV'ye kaydet
    pd.DataFrame.from_dict(per_target_features, orient='index').to_csv('selected_features_per_target.csv')
    print("\nHer hedef için seçilen özellikler 'selected_features_per_target.csv' dosyasına kaydedildi.")

if __name__ == "__main__":
    main() 