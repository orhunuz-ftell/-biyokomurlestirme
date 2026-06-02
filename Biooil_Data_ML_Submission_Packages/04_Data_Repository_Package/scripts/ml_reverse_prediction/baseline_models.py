"""
Baseline ML Models for Reverse Prediction
Random Forest, XGBoost, and Linear Regression
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import json

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler

try:
    from xgboost import XGBRegressor
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("WARNING: XGBoost not installed. Install with: pip install xgboost")


class BaselineModels:
    """Train and evaluate baseline ML models"""

    def __init__(self):
        self.input_features = [
            'Reformer_Temperature_C',
            'Reformer_Pressure_bar',
            'Steam_to_Carbon_Ratio',
            'H2_molpercent',
            'CO_molpercent',
            'CO2_molpercent',
            'CH4_molpercent',
            'H2O_molpercent'
        ]

        self.target_features = [
            'Biooil_Aromatics_pct',
            'Biooil_Acids_pct',
            'Biooil_Alcohols_pct',
            'Biooil_Furans_pct',
            'Biooil_Phenols_pct',
            'Biooil_Aldehydes_Ketones_pct'
        ]

        self.models = {}
        self.metrics = {}
        self.scalers = {}

    def load_data(self, csv_path):
        """Load processed data"""
        print(f"Loading data from: {csv_path}")
        df = pd.read_csv(csv_path)
        print(f"  Loaded {len(df)} samples")
        return df

    def split_data(self, df, test_size=0.15, val_size=0.15, random_state=42):
        """
        Split data into train, validation, and test sets

        Args:
            df: DataFrame
            test_size: Fraction for test set
            val_size: Fraction for validation set
            random_state: Random seed

        Returns:
            X_train, X_val, X_test, y_train, y_val, y_test
        """
        print("\n" + "="*80)
        print("DATA SPLITTING")
        print("="*80)

        X = df[self.input_features]
        y = df[self.target_features]

        # First split: separate test set
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        # Second split: separate train and validation
        val_size_adjusted = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_size_adjusted, random_state=random_state
        )

        print(f"Total samples: {len(df)}")
        print(f"Train set:     {len(X_train)} ({len(X_train)/len(df)*100:.1f}%)")
        print(f"Validation:    {len(X_val)} ({len(X_val)/len(df)*100:.1f}%)")
        print(f"Test set:      {len(X_test)} ({len(X_test)/len(df)*100:.1f}%)")
        print("="*80)

        return X_train, X_val, X_test, y_train, y_val, y_test

    def calculate_metrics(self, y_true, y_pred, component_name):
        """Calculate regression metrics"""
        return {
            'R2': r2_score(y_true, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
            'MAE': mean_absolute_error(y_true, y_pred),
            'MAPE': np.mean(np.abs((y_true - y_pred) / (y_true + 1e-10))) * 100
        }

    def train_linear_regression(self, X_train, y_train, X_val, y_val):
        """Train Linear Regression models (one per component)"""
        print("\n" + "="*80)
        print("TRAINING: LINEAR REGRESSION")
        print("="*80)

        models = {}
        metrics = {}

        for component in self.target_features:
            # Train
            model = LinearRegression()
            model.fit(X_train, y_train[component])

            # Predict on validation set
            y_pred = model.predict(X_val)

            # Calculate metrics
            metrics[component] = self.calculate_metrics(
                y_val[component], y_pred, component
            )

            models[component] = model

            # Print results
            print(f"{component:35s} | R²={metrics[component]['R2']:.3f} | "
                  f"RMSE={metrics[component]['RMSE']:.2f} | "
                  f"MAE={metrics[component]['MAE']:.2f}")

        # Calculate average metrics
        avg_metrics = {
            'R2': np.mean([m['R2'] for m in metrics.values()]),
            'RMSE': np.mean([m['RMSE'] for m in metrics.values()]),
            'MAE': np.mean([m['MAE'] for m in metrics.values()])
        }

        print(f"\n{'AVERAGE':35s} | R²={avg_metrics['R2']:.3f} | "
              f"RMSE={avg_metrics['RMSE']:.2f} | MAE={avg_metrics['MAE']:.2f}")

        return models, metrics

    def train_random_forest(self, X_train, y_train, X_val, y_val):
        """Train Random Forest models (one per component)"""
        print("\n" + "="*80)
        print("TRAINING: RANDOM FOREST")
        print("="*80)

        models = {}
        metrics = {}

        for component in self.target_features:
            # Train
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=20,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1,
                verbose=0
            )

            print(f"Training {component}...", end=' ')
            model.fit(X_train, y_train[component])

            # Predict on validation set
            y_pred = model.predict(X_val)

            # Calculate metrics
            metrics[component] = self.calculate_metrics(
                y_val[component], y_pred, component
            )

            models[component] = model

            # Print results
            print(f"R²={metrics[component]['R2']:.3f} | "
                  f"RMSE={metrics[component]['RMSE']:.2f} | "
                  f"MAE={metrics[component]['MAE']:.2f}")

        # Calculate average metrics
        avg_metrics = {
            'R2': np.mean([m['R2'] for m in metrics.values()]),
            'RMSE': np.mean([m['RMSE'] for m in metrics.values()]),
            'MAE': np.mean([m['MAE'] for m in metrics.values()])
        }

        print(f"\n{'AVERAGE':35s} | R²={avg_metrics['R2']:.3f} | "
              f"RMSE={avg_metrics['RMSE']:.2f} | MAE={avg_metrics['MAE']:.2f}")

        return models, metrics

    def train_xgboost(self, X_train, y_train, X_val, y_val):
        """Train XGBoost models (one per component)"""
        if not XGBOOST_AVAILABLE:
            print("\nXGBoost not available, skipping...")
            return None, None

        print("\n" + "="*80)
        print("TRAINING: XGBOOST")
        print("="*80)

        models = {}
        metrics = {}

        for component in self.target_features:
            # Train
            model = XGBRegressor(
                n_estimators=200,
                max_depth=10,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                n_jobs=-1,
                verbosity=0
            )

            print(f"Training {component}...", end=' ')
            model.fit(
                X_train, y_train[component],
                eval_set=[(X_val, y_val[component])],
                verbose=False
            )

            # Predict on validation set
            y_pred = model.predict(X_val)

            # Calculate metrics
            metrics[component] = self.calculate_metrics(
                y_val[component], y_pred, component
            )

            models[component] = model

            # Print results
            print(f"R²={metrics[component]['R2']:.3f} | "
                  f"RMSE={metrics[component]['RMSE']:.2f} | "
                  f"MAE={metrics[component]['MAE']:.2f}")

        # Calculate average metrics
        avg_metrics = {
            'R2': np.mean([m['R2'] for m in metrics.values()]),
            'RMSE': np.mean([m['RMSE'] for m in metrics.values()]),
            'MAE': np.mean([m['MAE'] for m in metrics.values()])
        }

        print(f"\n{'AVERAGE':35s} | R²={avg_metrics['R2']:.3f} | "
              f"RMSE={avg_metrics['RMSE']:.2f} | MAE={avg_metrics['MAE']:.2f}")

        return models, metrics

    def get_feature_importance(self, models, model_type='rf'):
        """
        Get feature importance from tree-based models

        Args:
            models: Dict of trained models
            model_type: 'rf' or 'xgb'

        Returns:
            DataFrame with feature importance
        """
        importance_dict = {}

        for component, model in models.items():
            if hasattr(model, 'feature_importances_'):
                importance_dict[component] = model.feature_importances_

        df_importance = pd.DataFrame(
            importance_dict,
            index=self.input_features
        )

        # Calculate average importance
        df_importance['Average'] = df_importance.mean(axis=1)
        df_importance = df_importance.sort_values('Average', ascending=False)

        return df_importance

    def save_models(self, models, model_name, output_dir):
        """Save trained models"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        for component, model in models.items():
            component_clean = component.replace('Biooil_', '').replace('_pct', '')
            filename = output_path / f"{model_name}_{component_clean}.pkl"
            joblib.dump(model, filename)

        print(f"\nSaved {len(models)} models to: {output_dir}")

    def save_metrics(self, all_metrics, output_path):
        """Save metrics to JSON"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to JSON-serializable format
        metrics_serializable = {}
        for model_name, components in all_metrics.items():
            metrics_serializable[model_name] = {}
            for component, metrics in components.items():
                metrics_serializable[model_name][component] = {
                    k: float(v) for k, v in metrics.items()
                }

        with open(output_path, 'w') as f:
            json.dump(metrics_serializable, f, indent=2)

        print(f"\nSaved metrics to: {output_path}")


def main():
    """Main training pipeline"""

    # Initialize
    trainer = BaselineModels()

    # Load data
    data_path = Path(__file__).parent.parent / 'data' / 'processed' / 'reformer_data_clean.csv'
    df = trainer.load_data(data_path)

    # Split data
    X_train, X_val, X_test, y_train, y_val, y_test = trainer.split_data(df)

    # Store all metrics
    all_metrics = {}

    # Train Linear Regression
    models_lr, metrics_lr = trainer.train_linear_regression(X_train, y_train, X_val, y_val)
    all_metrics['linear_regression'] = metrics_lr

    # Train Random Forest
    models_rf, metrics_rf = trainer.train_random_forest(X_train, y_train, X_val, y_val)
    all_metrics['random_forest'] = metrics_rf

    # Train XGBoost (if available)
    if XGBOOST_AVAILABLE:
        models_xgb, metrics_xgb = trainer.train_xgboost(X_train, y_train, X_val, y_val)
        all_metrics['xgboost'] = metrics_xgb

    # Feature importance
    print("\n" + "="*80)
    print("FEATURE IMPORTANCE (Random Forest)")
    print("="*80)
    importance_rf = trainer.get_feature_importance(models_rf, 'rf')
    print(importance_rf.round(4))

    # Save models
    models_dir = Path(__file__).parent.parent / 'models'
    trainer.save_models(models_rf, 'rf', models_dir / 'random_forest')

    if XGBOOST_AVAILABLE:
        trainer.save_models(models_xgb, 'xgb', models_dir / 'xgboost')

    # Save metrics
    metrics_path = Path(__file__).parent.parent / 'output' / 'metrics' / 'baseline_metrics.json'
    trainer.save_metrics(all_metrics, metrics_path)

    # Save feature importance
    importance_path = Path(__file__).parent.parent / 'output' / 'metrics' / 'feature_importance_rf.csv'
    importance_path.parent.mkdir(parents=True, exist_ok=True)
    importance_rf.to_csv(importance_path)

    # Save train/val/test splits for later use
    splits_dir = Path(__file__).parent.parent / 'data' / 'processed'
    X_train.to_csv(splits_dir / 'X_train.csv', index=False)
    X_val.to_csv(splits_dir / 'X_val.csv', index=False)
    X_test.to_csv(splits_dir / 'X_test.csv', index=False)
    y_train.to_csv(splits_dir / 'y_train.csv', index=False)
    y_val.to_csv(splits_dir / 'y_val.csv', index=False)
    y_test.to_csv(splits_dir / 'y_test.csv', index=False)

    print("\n" + "="*80)
    print("TRAINING COMPLETE!")
    print("="*80)
    print(f"\nBest model: Random Forest")
    print(f"  Average R²:   {np.mean([m['R2'] for m in metrics_rf.values()]):.3f}")
    print(f"  Average RMSE: {np.mean([m['RMSE'] for m in metrics_rf.values()]):.2f}%")
    print(f"  Average MAE:  {np.mean([m['MAE'] for m in metrics_rf.values()]):.2f}%")


if __name__ == '__main__':
    main()
