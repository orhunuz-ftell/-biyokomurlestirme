import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib

class BiooilPredictor:
    def __init__(self):
        """Model ve sonuçları tutacak değişkenleri başlat"""
        self.rf_models = {}  # Her çıktı için ayrı model
        self.feature_importance = {}  # Her çıktı için özellik önem dereceleri
        self.performance_metrics = {}  # Her çıktı için performans metrikleri
        
    def train_models(self, X_train, X_test, y_train, y_test):
        """Her çıktı değişkeni için ayrı RF modeli eğit ve detaylı sonuçları yazdır"""
        output_names = y_train.columns
        overall_results = {}
        
        print("\n=== MODEL EĞİTİM SONUÇLARI ===")
        print(f"Toplam Giriş Değişkeni Sayısı: {X_train.shape[1]}")
        print(f"Toplam Çıkış Değişkeni Sayısı: {len(output_names)}")
        print(f"Eğitim Seti Boyutu: {X_train.shape[0]}")
        print(f"Test Seti Boyutu: {X_test.shape[0]}")
        print("\n" + "="*50)
        
        for output in output_names:
            print(f"\n{output.upper()} DEĞİŞKENİ İÇİN MODEL SONUÇLARI:")
            print("-"*50)
            
            # Eksik değerleri olan satırları çıkar
            mask = ~y_train[output].isna()
            X_train_clean = X_train[mask]
            y_train_clean = y_train[output][mask]
            
            # Eğitim verisi sayısını kontrol et
            n_samples = len(y_train_clean)
            print(f"Geçerli Eğitim Örneği Sayısı: {n_samples}")
            
            if n_samples < 2:
                print(f"UYARI: {output} için yeterli veri yok. Atlanıyor...")
                continue
            
            try:
                # Random Forest modelini oluştur ve eğit
                rf_model = RandomForestRegressor(
                    n_estimators=100,
                    max_depth=None,
                    min_samples_split=2,
                    min_samples_leaf=1,
                    random_state=42
                )
                
                # Modeli eğit
                rf_model.fit(X_train_clean, y_train_clean)
                
                # Test seti üzerinde tahmin yap
                mask_test = ~y_test[output].isna()
                X_test_clean = X_test[mask_test]
                y_test_clean = y_test[output][mask_test]
                
                # Model sonuçlarını hesapla ve kaydet
                if len(y_test_clean) > 0:
                    y_pred = rf_model.predict(X_test_clean)
                    metrics = {
                        'R2': r2_score(y_test_clean, y_pred),
                        'MAE': mean_absolute_error(y_test_clean, y_pred),
                        'MSE': mean_squared_error(y_test_clean, y_pred),
                        'RMSE': np.sqrt(mean_squared_error(y_test_clean, y_pred))
                    }
                    
                    # Tahmin istatistiklerini hesapla
                    pred_stats = {
                        'Ortalama Tahmin': np.mean(y_pred),
                        'Medyan Tahmin': np.median(y_pred),
                        'Minimum Tahmin': np.min(y_pred),
                        'Maksimum Tahmin': np.max(y_pred),
                        'Tahmin Std': np.std(y_pred)
                    }
                else:
                    print(f"UYARI: {output} için test verisi yok!")
                    metrics = {
                        'R2': None, 'MAE': None, 'MSE': None, 'RMSE': None
                    }
                    pred_stats = {
                        'Ortalama Tahmin': None, 'Medyan Tahmin': None,
                        'Minimum Tahmin': None, 'Maksimum Tahmin': None,
                        'Tahmin Std': None
                    }
                
                # Sonuçları kaydet
                self.rf_models[output] = rf_model
                self.performance_metrics[output] = metrics
                
                # Özellik önem derecelerini hesapla ve kaydet
                importance_df = pd.DataFrame({
                    'feature': X_train.columns,
                    'importance': rf_model.feature_importances_
                }).sort_values('importance', ascending=False)
                self.feature_importance[output] = importance_df
                
                # Sonuçları yazdır
                print("\nModel Performans Metrikleri:")
                for metric, value in metrics.items():
                    if value is not None:
                        print(f"{metric}: {value:.4f}")
                    else:
                        print(f"{metric}: NA")
                
                print("\nTahmin İstatistikleri:")
                for stat, value in pred_stats.items():
                    if value is not None:
                        print(f"{stat}: {value:.4f}")
                    else:
                        print(f"{stat}: NA")
                
                print("\nEn Önemli 5 Özellik:")
                for idx, row in importance_df.head().iterrows():
                    print(f"{row['feature']}: {row['importance']:.4f}")
                
                # Genel sonuçları kaydet
                overall_results[output] = {
                    'metrics': metrics,
                    'pred_stats': pred_stats,
                    'top_features': importance_df.head().to_dict('records')
                }
                
            except Exception as e:
                print(f"HATA ({output}): {str(e)}")
                continue
        
        # Genel performans özeti
        print("\n=== GENEL MODEL PERFORMANS ÖZETİ ===")
        for output, results in overall_results.items():
            if results['metrics']['R2'] is not None:
                print(f"\n{output}:")
                print(f"R2 Score: {results['metrics']['R2']:.4f}")
                print(f"RMSE: {results['metrics']['RMSE']:.4f}")
                print(f"En önemli özellik: {results['top_features'][0]['feature']}")
    
    def save_models(self, path='rf_models'):
        """Eğitilmiş modelleri kaydet"""
        for output, model in self.rf_models.items():
            joblib.dump(model, f'{path}_{output}.joblib')
        print("\nTüm modeller başarıyla kaydedildi!")

# Kullanım örneği
if __name__ == "__main__":
    # Verileri yükle
    X_train = pd.read_csv('processed_data_X_train.csv')
    X_test = pd.read_csv('processed_data_X_test.csv')
    y_train = pd.read_csv('processed_data_y_train.csv')
    y_test = pd.read_csv('processed_data_y_test.csv')
    
    # Modeli oluştur ve eğit
    predictor = BiooilPredictor()
    predictor.train_models(X_train, X_test, y_train, y_test)
    
    # Modelleri kaydet
    predictor.save_models()