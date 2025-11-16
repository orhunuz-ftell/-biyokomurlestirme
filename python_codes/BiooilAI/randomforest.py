import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

class BiooilPredictor:
    def __init__(self):
        self.rf_models = {}
        self.feature_importance = {}
        self.performance_metrics = {}

    def train_models(self, X_train, X_test, y_train, y_test):
        for output in y_train.columns:
            print(f"\n{output} için model eğitiliyor...")
            mask_tr = ~y_train[output].isna()
            X_tr = X_train[mask_tr]
            y_tr = y_train[output][mask_tr]
            print(f"  Eğitim örnek sayısı: {len(y_tr)}")
            if len(y_tr) < 2:
                print("  UYARI: Yeterli veri yok, atlanıyor.")
                continue

            rf = RandomForestRegressor(n_estimators=100, random_state=42,max_depth=10,min_samples_split=5,min_samples_leaf=3,max_features='sqrt')
            rf.fit(X_tr, y_tr)

            mask_te = ~y_test[output].isna()
            X_te = X_test[mask_te]
            y_te = y_test[output][mask_te]
            if len(y_te) > 0:
                y_pred = rf.predict(X_te)
                metrics = {
                    'R2':   r2_score(y_te, y_pred),
                    'MAE':  mean_absolute_error(y_te, y_pred),
                    'MSE':  mean_squared_error(y_te, y_pred),
                    'RMSE': np.sqrt(mean_squared_error(y_te, y_pred))
                }
            else:
                print("  UYARI: Test verisi yok.")
                metrics = dict.fromkeys(['R2','MAE','MSE','RMSE'], None)

            self.rf_models[output] = rf
            self.performance_metrics[output] = metrics
            self.feature_importance[output] = pd.DataFrame({
                'feature': X_train.columns,
                'importance': rf.feature_importances_
            }).sort_values('importance', ascending=False)

            print(f"  {output} performans:")
            for k, v in metrics.items():
                print(f"    {k}: {v:.4f}" if v is not None else f"    {k}: NA")

    def print_r2_scores(self):
        print("\n=== Tüm hedefler için R² değerleri ===")
        for output, m in self.performance_metrics.items():
            r2 = m.get('R2')
            print(f"  {output}: R² = {r2:.4f}" if r2 is not None else f"  {output}: NA")

    def plot_feature_importance(self, output, top_n=10):
        if output not in self.feature_importance:
            print(f"UYARI: {output} için model bulunamadı!")
            return
        df_imp = self.feature_importance[output].head(top_n)
        plt.figure(figsize=(10,6))
        sns.barplot(x='importance', y='feature', data=df_imp)
        plt.title(f'En Önemli {top_n} Özellik - {output}')
        plt.tight_layout()
        plt.show()

    def plot_predictions(self, X_test, y_test, output):
        if output not in self.rf_models:
            print(f"UYARI: {output} için model bulunamadı!")
            return
        mask = ~y_test[output].isna()
        X_te = X_test[mask]
        y_te = y_test[output][mask]
        if len(y_te)==0:
            print(f"UYARI: {output} için test verisi yok!")
            return
        y_pred = self.rf_models[output].predict(X_te)
        plt.figure(figsize=(8,8))
        plt.scatter(y_te, y_pred, alpha=0.5)
        plt.plot([y_te.min(), y_te.max()],
                 [y_te.min(), y_te.max()],
                 'r--')
        plt.xlabel('Gerçek')
        plt.ylabel('Tahmin')
        plt.title(f'{output} – Tahmin vs Gerçek')
        plt.tight_layout()
        plt.show()

    def save_models(self, path='rf_model'):
        for output, model in self.rf_models.items():
            joblib.dump(model, f'{path}_{output}.joblib')
        print("\nModeller kaydedildi!")
