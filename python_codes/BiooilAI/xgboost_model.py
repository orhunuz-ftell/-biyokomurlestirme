import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

class BiooilXGBoostPredictor:
    def __init__(self):
        """Model ve sonuçları tutacak değişkenleri başlat"""
        self.xgb_models = {}  # Her çıktı için ayrı model
        self.feature_importance = {}  # Her çıktı için özellik önem dereceleri
        self.performance_metrics = {}  # Her çıktı için performans metrikleri

    def train_models(self, X_train, X_test, y_train, y_test):
        """Her çıktı değişkeni için ayrı XGBoost modeli eğit"""
        output_names = y_train.columns

        for output in output_names:
            print(f"\n{output} için model eğitiliyor...")

            # Eksik değerleri olan satırları çıkar
            mask = ~y_train[output].isna()
            X_train_clean = X_train[mask]
            y_train_clean = y_train[output][mask]

            # Eğitim verisi sayısını kontrol et
            n_samples = len(y_train_clean)
            print(f"Geçerli örnek sayısı: {n_samples}")

            if n_samples < 2:
                print(f"UYARI: {output} için yeterli veri yok. Atlanıyor...")
                continue

            try:
                # XGBoost modelini oluştur ve eğit
                xgb_model = xgb.XGBRegressor(
                    objective='reg:squarederror',  # Regresyon görevi için
                    n_estimators=100,  # Ağaç sayısı
                    learning_rate=0.1, # Öğrenme oranı
                    max_depth=5,       # Maksimum derinlik
                    subsample=0.8,     # Her ağaç için kullanılacak örnek oranı
                    colsample_bytree=0.8, # Her ağaç için kullanılacak özellik oranı
                    random_state=42
                )

                # Modeli eğit
                xgb_model.fit(X_train_clean, y_train_clean)

                # Test seti üzerinde tahmin yap
                mask_test = ~y_test[output].isna()
                X_test_clean = X_test[mask_test]
                y_test_clean = y_test[output][mask_test]

                if len(y_test_clean) > 0:
                    y_pred = xgb_model.predict(X_test_clean)

                    # Performans metriklerini hesapla
                    metrics = {
                        'R2': r2_score(y_test_clean, y_pred),
                        'MAE': mean_absolute_error(y_test_clean, y_pred),
                        'MSE': mean_squared_error(y_test_clean, y_pred),
                        'RMSE': np.sqrt(mean_squared_error(y_test_clean, y_pred))
                    }
                else:
                    print(f"UYARI: {output} için test verisi yok!")
                    metrics = {
                        'R2': None,
                        'MAE': None,
                        'MSE': None,
                        'RMSE': None
                    }

                # Sonuçları kaydet
                self.xgb_models[output] = xgb_model
                self.performance_metrics[output] = metrics
                self.feature_importance[output] = pd.DataFrame({
                    'feature': X_train.columns,
                    'importance': xgb_model.feature_importances_
                }).sort_values('importance', ascending=False)

                # Sonuçları yazdır
                print(f"\n{output} için performans metrikleri:")
                for metric, value in metrics.items():
                    if value is not None:
                        print(f"{metric}: {value:.4f}")
                    else:
                        print(f"{metric}: NA")

            except Exception as e:
                print(f"HATA ({output}): {str(e)}")
                continue

    def plot_feature_importance(self, output, top_n=10):
        """Özellik önem derecelerini görselleştir"""
        if output not in self.feature_importance:
            print(f"UYARI: {output} için model bulunamadı!")
            return

        plt.figure(figsize=(10, 6))
        importance_df = self.feature_importance[output].head(top_n)

        sns.barplot(x='importance', y='feature', data=importance_df)
        plt.title(f'En Önemli {top_n} Özellik - {output} (XGBoost)')
        plt.xlabel('Önem Derecesi')
        plt.ylabel('Özellik')
        plt.tight_layout()
        plt.show()

    def plot_predictions(self, X_test, y_test, output):
        """Tahmin vs gerçek değer grafiğini çiz"""
        if output not in self.xgb_models:
            print(f"UYARI: {output} için model bulunamadı!")
            return

        mask = ~y_test[output].isna()
        X_test_clean = X_test[mask]
        y_test_clean = y_test[output][mask]

        if len(y_test_clean) == 0:
            print(f"UYARI: {output} için test verisi yok!")
            return

        y_pred = self.xgb_models[output].predict(X_test_clean)

        plt.figure(figsize=(8, 8))
        plt.scatter(y_test_clean, y_pred, alpha=0.5)
        plt.plot([y_test_clean.min(), y_test_clean.max()],
                 [y_test_clean.min(), y_test_clean.max()],
                 'r--', lw=2)

        plt.xlabel('Gerçek Değerler')
        plt.ylabel('Tahmin Edilen Değerler')
        plt.title(f'{output} - Tahmin vs Gerçek Değerler (XGBoost)')
        plt.tight_layout()
        plt.show()

    def save_models(self, path='xgb_models'):
        """Eğitilmiş modelleri kaydet"""
        for output, model in self.xgb_models.items():
            joblib.dump(model, f'{path}_{output}.joblib')
        print("XGBoost Modelleri kaydedildi!")

# Kullanım örneği
if __name__ == "__main__":
    # Verileri yükle
    X_train = pd.read_csv('processed_data_X_train.csv')
    X_test = pd.read_csv('processed_data_X_test.csv')
    y_train = pd.read_csv('processed_data_y_train.csv')
    y_test = pd.read_csv('processed_data_y_test.csv')

    # Modeli oluştur ve eğit
    predictor = BiooilXGBoostPredictor()
    predictor.train_models(X_train, X_test, y_train, y_test)

    # Her bir çıktı için önemli özellikleri ve tahminleri görselleştir
    for output in y_train.columns:
        if output in predictor.xgb_models: # Check if model exists
            print(f"\n{output} için özellik önem dereceleri (XGBoost):")
            predictor.plot_feature_importance(output)
            predictor.plot_predictions(X_test, y_test, output)

    # Modelleri kaydet
    predictor.save_models() 