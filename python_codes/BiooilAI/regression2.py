import os
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def load_data():
    # Veri yükleme
    X_train = pd.read_csv('processed_data_X_train.csv')
    y_train = pd.read_csv('processed_data_y_train.csv')
    X_test = pd.read_csv('processed_data_X_test.csv')
    y_test = pd.read_csv('processed_data_y_test.csv')
    
    # Seçilen özellikleri yükle
    selected_features = pd.read_csv('selected_features_per_target.csv', index_col=0)
    
    return X_train, y_train, X_test, y_test, selected_features

def create_pipeline(model_type='rf'):
    """Model pipeline'ı oluştur"""
    if model_type == 'rf':
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=5,
            min_samples_split=5,
            min_samples_leaf=3,
            max_features='sqrt',
            random_state=42
        )
    else:  # xgb
        model = XGBRegressor(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1.0,
            random_state=42
        )
    
    return Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('model', model)
    ])

def train_and_evaluate_models(X_train, y_train, X_test, y_test, selected_features):
    """Her hedef için ayrı model eğit ve değerlendir"""
    results = {}
    
    for target in y_train.columns:
        print(f"\n{target} için model eğitimi:")
        print("-" * 50)
        
        # Bu hedef için seçilen özellikleri al
        features_str = selected_features.loc[target].iloc[0]
        # String'i liste olarak parse et
        features = [f.strip().strip("'") for f in features_str.strip('[]').split(',')]
        print(f"Kullanılan özellikler: {features}")
        
        # Veriyi hazırla
        X_train_selected = X_train[features]
        X_test_selected = X_test[features]
        y_train_target = y_train[target]
        y_test_target = y_test[target]
        
        # Random Forest modeli
        rf_pipeline = create_pipeline('rf')
        rf_pipeline.fit(X_train_selected, y_train_target)
        
        # XGBoost modeli
        xgb_pipeline = create_pipeline('xgb')
        xgb_pipeline.fit(X_train_selected, y_train_target)
        
        # Tahminler
        y_pred_rf = rf_pipeline.predict(X_test_selected)
        y_pred_xgb = xgb_pipeline.predict(X_test_selected)
        
        # Metrikler
        mse_rf = mean_squared_error(y_test_target, y_pred_rf)
        r2_rf = r2_score(y_test_target, y_pred_rf)
        
        mse_xgb = mean_squared_error(y_test_target, y_pred_xgb)
        r2_xgb = r2_score(y_test_target, y_pred_xgb)
        
        print(f"Random Forest - MSE: {mse_rf:.4f}, R²: {r2_rf:.4f}")
        print(f"XGBoost - MSE: {mse_xgb:.4f}, R²: {r2_xgb:.4f}")
        
        # En iyi modeli seç ve kaydet
        if r2_rf > r2_xgb:
            best_model = rf_pipeline
            best_type = 'rf'
            best_r2 = r2_rf
        else:
            best_model = xgb_pipeline
            best_type = 'xgb'
            best_r2 = r2_xgb
        
        # Modeli kaydet
        model_path = f'models/{target}_{best_type}_model.joblib'
        os.makedirs('models', exist_ok=True)
        joblib.dump(best_model, model_path)
        
        results[target] = {
            'features': features,
            'best_model_type': best_type,
            'best_r2': best_r2,
            'model_path': model_path
        }
    
    return results

def main():
    # Veriyi yükle
    X_train, y_train, X_test, y_test, selected_features = load_data()
    
    # Modelleri eğit ve değerlendir
    results = train_and_evaluate_models(X_train, y_train, X_test, y_test, selected_features)
    
    # Sonuçları özetle
    print("\nModel Performans Özeti:")
    print("-" * 50)
    for target, result in results.items():
        print(f"\n{target}:")
        print(f"En iyi model: {result['best_model_type']}")
        print(f"R² skoru: {result['best_r2']:.4f}")
        print(f"Model kaydedildi: {result['model_path']}")

if __name__ == "__main__":
    main() 