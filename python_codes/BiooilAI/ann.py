import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import tensorflow as tf
from tensorflow.keras.models import Sequential, save_model, load_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import joblib
import os

class BiooilPredictorANN:
    def __init__(self):
        """Model ve sonuçları tutacak değişkenleri başlat"""
        self.ann_models = {}  # Her çıktı için ayrı model
        self.performance_metrics = {}  # Her çıktı için performans metrikleri
        self.input_shapes = {}  # Her model için giriş boyutu
        
    def create_model(self, input_shape):
        """Yapay sinir ağı modelini oluştur"""
        model = Sequential([
            Dense(64, activation='relu', input_shape=(input_shape,)),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dropout(0.1),
            Dense(16, activation='relu'),
            Dense(1, activation='linear')
        ])
        
        model.compile(
            optimizer='adam',
            loss='mean_squared_error',
            metrics=['mae']
        )
        
        return model
    
    def train_models(self, X_train, X_test, y_train, y_test):
        """Her çıktı değişkeni için ayrı ANN modeli eğit ve detaylı sonuçları yazdır"""
        output_names = y_train.columns
        overall_results = {}
        
        print("\n=== MODEL EĞİTİM SONUÇLARI ===")
        print(f"Toplam Giriş Değişkeni Sayısı: {X_train.shape[1]}")
        print(f"Toplam Çıkış Değişkeni Sayısı: {len(output_names)}")
        print(f"Eğitim Seti Boyutu: {X_train.shape[0]}")
        print(f"Test Seti Boyutu: {X_test.shape[0]}")
        print("\n" + "="*50)
        
        # Early stopping callback
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=50,
            restore_best_weights=True,
            verbose=0
        )
        
        for output in output_names:
            print(f"\n{output.upper()} DEĞİŞKENİ İÇİN MODEL SONUÇLARI:")
            print("-"*50)
            
            # Eksik değerleri olan satırları çıkar
            mask = ~y_train[output].isna()
            X_train_clean = X_train[mask].values
            y_train_clean = y_train[output][mask].values
            
            # Eğitim verisi sayısını kontrol et
            n_samples = len(y_train_clean)
            print(f"Geçerli Eğitim Örneği Sayısı: {n_samples}")
            
            if n_samples < 2:
                print(f"UYARI: {output} için yeterli veri yok. Atlanıyor...")
                continue
            
            try:
                # ANN modelini oluştur
                model = self.create_model(X_train.shape[1])
                self.input_shapes[output] = X_train.shape[1]
                
                # Modeli eğit
                history = model.fit(
                    X_train_clean,
                    y_train_clean,
                    epochs=1000,
                    batch_size=8,
                    validation_split=0.2,
                    callbacks=[early_stopping],
                    verbose=0
                )
                
                # Test seti üzerinde tahmin yap
                mask_test = ~y_test[output].isna()
                X_test_clean = X_test[mask_test].values
                y_test_clean = y_test[output][mask_test].values
                
                # Model sonuçlarını hesapla ve kaydet
                if len(y_test_clean) > 0:
                    y_pred = model.predict(X_test_clean, verbose=0).flatten()
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
                self.ann_models[output] = model
                self.performance_metrics[output] = metrics
                
                # Eğitim geçmişini analiz et
                final_loss = history.history['loss'][-1]
                final_val_loss = history.history['val_loss'][-1]
                epochs_trained = len(history.history['loss'])
                
                # Sonuçları yazdır
                print("\nEğitim Bilgileri:")
                print(f"Toplam Epoch Sayısı: {epochs_trained}")
                print(f"Son Eğitim Loss: {final_loss:.4f}")
                print(f"Son Validation Loss: {final_val_loss:.4f}")
                
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
                
                # Genel sonuçları kaydet
                overall_results[output] = {
                    'metrics': metrics,
                    'pred_stats': pred_stats,
                    'training_info': {
                        'epochs': epochs_trained,
                        'final_loss': final_loss,
                        'final_val_loss': final_val_loss
                    }
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
                print(f"Eğitim Epoch Sayısı: {results['training_info']['epochs']}")
    
    def save_models(self, path='ann_models'):
        """Eğitilmiş modelleri kaydet"""
        if not os.path.exists(path):
            os.makedirs(path)
            
        # Model mimarilerini ve ağırlıkları kaydet
        for output, model in self.ann_models.items():
            model_path = f'{path}/{output}'
            save_model(model, model_path)
            
        # Input shapes bilgisini kaydet
        joblib.dump(self.input_shapes, f'{path}/input_shapes.joblib')
        print("\nTüm modeller başarıyla kaydedildi!")
    
    def load_models(self, path='ann_models'):
        """Kaydedilmiş modelleri yükle"""
        # Input shapes bilgisini yükle
        self.input_shapes = joblib.load(f'{path}/input_shapes.joblib')
        
        # Modelleri yükle
        for output in self.input_shapes.keys():
            model_path = f'{path}/{output}'
            self.ann_models[output] = load_model(model_path)
        
        print("\nTüm modeller başarıyla yüklendi!")

# Kullanım örneği
if __name__ == "__main__":
    # Verileri yükle
    X_train = pd.read_csv('processed_data_X_train.csv')
    X_test = pd.read_csv('processed_data_X_test.csv')
    y_train = pd.read_csv('processed_data_y_train.csv')
    y_test = pd.read_csv('processed_data_y_test.csv')
    
    # Modeli oluştur ve eğit
    predictor = BiooilPredictorANN()
    predictor.train_models(X_train, X_test, y_train, y_test)
    
    # Modelleri kaydet
    predictor.save_models()