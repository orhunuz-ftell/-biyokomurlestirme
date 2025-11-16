"""
Model Training Module for Reverse ML Project
Purpose: Train ML models to predict bio-oil properties from product characteristics
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import xgboost as xgb
import joblib
import os


class ReverseMLModelTrainer:
    """
    Train machine learning models for reverse prediction:
    Product Properties → Bio-oil Composition
    """

    def __init__(self):
        self.models = {}
        self.performance_metrics = {}
        self.feature_importance = {}

    def train_random_forest(self, X_train, y_train, X_test, y_test, target_name):
        """
        Train Random Forest model for a specific bio-oil property

        Parameters:
        -----------
        X_train, y_train : DataFrames
            Training data
        X_test, y_test : DataFrames
            Test data
        target_name : str
            Name of bio-oil property being predicted

        Returns:
        --------
        model : RandomForestRegressor
            Trained model
        """
        print(f"\nTraining Random Forest for {target_name}...")

        # Remove NaN values for this target
        mask_train = ~y_train[target_name].isna()
        X_tr = X_train[mask_train]
        y_tr = y_train[target_name][mask_train]

        mask_test = ~y_test[target_name].isna()
        X_te = X_test[mask_test]
        y_te = y_test[target_name][mask_test]

        if len(y_tr) < 10:
            print(f"  WARNING: Insufficient training data ({len(y_tr)} samples)")
            return None

        # Train model
        rf_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=3,
            random_state=42
        )

        rf_model.fit(X_tr, y_tr)

        # Evaluate
        if len(y_te) > 0:
            y_pred = rf_model.predict(X_te)
            metrics = {
                'R2': r2_score(y_te, y_pred),
                'MAE': mean_absolute_error(y_te, y_pred),
                'RMSE': np.sqrt(mean_squared_error(y_te, y_pred))
            }

            print(f"  Training samples: {len(y_tr)}")
            print(f"  Test samples: {len(y_te)}")
            print(f"  R² = {metrics['R2']:.4f}")
            print(f"  MAE = {metrics['MAE']:.4f}")
            print(f"  RMSE = {metrics['RMSE']:.4f}")

            # Feature importance
            importance_df = pd.DataFrame({
                'feature': X_train.columns,
                'importance': rf_model.feature_importances_
            }).sort_values('importance', ascending=False)

            self.feature_importance[target_name] = importance_df
            self.performance_metrics[target_name] = metrics

        return rf_model

    def train_xgboost(self, X_train, y_train, X_test, y_test, target_name):
        """
        Train XGBoost model for a specific bio-oil property
        """
        print(f"\nTraining XGBoost for {target_name}...")

        mask_train = ~y_train[target_name].isna()
        X_tr = X_train[mask_train]
        y_tr = y_train[target_name][mask_train]

        mask_test = ~y_test[target_name].isna()
        X_te = X_test[mask_test]
        y_te = y_test[target_name][mask_test]

        if len(y_tr) < 10:
            print(f"  WARNING: Insufficient training data ({len(y_tr)} samples)")
            return None

        xgb_model = xgb.XGBRegressor(
            objective='reg:squarederror',
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )

        xgb_model.fit(X_tr, y_tr)

        if len(y_te) > 0:
            y_pred = xgb_model.predict(X_te)
            metrics = {
                'R2': r2_score(y_te, y_pred),
                'MAE': mean_absolute_error(y_te, y_pred),
                'RMSE': np.sqrt(mean_squared_error(y_te, y_pred))
            }

            print(f"  Training samples: {len(y_tr)}")
            print(f"  Test samples: {len(y_te)}")
            print(f"  R² = {metrics['R2']:.4f}")
            print(f"  MAE = {metrics['MAE']:.4f}")
            print(f"  RMSE = {metrics['RMSE']:.4f}")

            self.performance_metrics[f"{target_name}_xgb"] = metrics

        return xgb_model

    def train_all_models(self, X_train, y_train, X_test, y_test, algorithm='random_forest'):
        """
        Train models for all bio-oil properties

        Parameters:
        -----------
        X_train, y_train, X_test, y_test : DataFrames
            Training and test data
        algorithm : str
            'random_forest' or 'xgboost'
        """
        print("="*60)
        print("TRAINING MODELS FOR ALL BIO-OIL PROPERTIES")
        print("="*60)

        for target in y_train.columns:
            if algorithm == 'random_forest':
                model = self.train_random_forest(X_train, y_train, X_test, y_test, target)
            elif algorithm == 'xgboost':
                model = self.train_xgboost(X_train, y_train, X_test, y_test, target)
            else:
                raise ValueError(f"Unknown algorithm: {algorithm}")

            if model is not None:
                self.models[target] = model

        print("\n" + "="*60)
        print("MODEL TRAINING COMPLETE")
        print("="*60)
        self.print_summary()

    def print_summary(self):
        """Print summary of all model performances"""
        print("\n=== MODEL PERFORMANCE SUMMARY ===")
        for target, metrics in self.performance_metrics.items():
            print(f"\n{target}:")
            for metric_name, value in metrics.items():
                print(f"  {metric_name}: {value:.4f}")

    def save_models(self, output_dir='./trained_models'):
        """Save all trained models"""
        os.makedirs(output_dir, exist_ok=True)

        for target, model in self.models.items():
            filepath = os.path.join(output_dir, f'{target}_model.joblib')
            joblib.dump(model, filepath)
            print(f"Saved: {filepath}")

        # Save metrics
        metrics_df = pd.DataFrame(self.performance_metrics).T
        metrics_df.to_csv(os.path.join(output_dir, 'model_performance.csv'))

        print(f"\nAll models saved to {output_dir}")

    def load_models(self, input_dir='./trained_models'):
        """Load previously trained models"""
        for filename in os.listdir(input_dir):
            if filename.endswith('_model.joblib'):
                target = filename.replace('_model.joblib', '')
                filepath = os.path.join(input_dir, filename)
                self.models[target] = joblib.load(filepath)
                print(f"Loaded: {target}")

    def predict(self, X_new, target_name):
        """
        Make prediction for new product properties

        Parameters:
        -----------
        X_new : DataFrame or array
            Product properties (same features as training)
        target_name : str
            Bio-oil property to predict

        Returns:
        --------
        prediction : float or array
            Predicted bio-oil property value
        """
        if target_name not in self.models:
            raise ValueError(f"No trained model for {target_name}")

        prediction = self.models[target_name].predict(X_new)
        return prediction

    def predict_all(self, X_new):
        """
        Predict all bio-oil properties from product properties

        Parameters:
        -----------
        X_new : DataFrame
            Product properties

        Returns:
        --------
        predictions : DataFrame
            Predicted bio-oil composition
        """
        predictions = {}
        for target, model in self.models.items():
            predictions[target] = model.predict(X_new)

        return pd.DataFrame(predictions)


if __name__ == "__main__":
    # Example usage
    print("Model training module loaded successfully")
    print("Waiting for processed training data...")

    # TODO: Uncomment when data is ready
    # trainer = ReverseMLModelTrainer()
    #
    # # Load processed data
    # X_train = pd.read_csv('../data/processed/X_train.csv')
    # X_test = pd.read_csv('../data/processed/X_test.csv')
    # y_train = pd.read_csv('../data/processed/y_train.csv')
    # y_test = pd.read_csv('../data/processed/y_test.csv')
    #
    # # Train models
    # trainer.train_all_models(X_train, y_train, X_test, y_test, algorithm='random_forest')
    #
    # # Save models
    # trainer.save_models()
