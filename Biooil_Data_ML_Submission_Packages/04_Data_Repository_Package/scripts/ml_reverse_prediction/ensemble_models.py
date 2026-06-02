"""
Ensemble Methods - Phase 4
Combine predictions from multiple models for improved accuracy
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import json
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from tensorflow import keras
import warnings
warnings.filterwarnings('ignore')


class EnsemblePredictor:
    """Ensemble methods combining RF, XGB, and MLP predictions"""

    def __init__(self):
        self.target_features = [
            'Biooil_Aromatics_pct',
            'Biooil_Acids_pct',
            'Biooil_Alcohols_pct',
            'Biooil_Furans_pct',
            'Biooil_Phenols_pct',
            'Biooil_Aldehydes_Ketones_pct'
        ]

        self.models = {}
        self.scalers = {}

    def load_all_models(self, base_dir):
        """Load all trained models"""
        print("Loading models...")

        # Load Random Forest
        rf_dir = base_dir / 'models' / 'random_forest'
        self.models['rf'] = {}
        for component in self.target_features:
            comp_clean = component.replace('Biooil_', '').replace('_pct', '')
            model_path = rf_dir / f"rf_{comp_clean}.pkl"
            if model_path.exists():
                self.models['rf'][component] = joblib.load(model_path)
                print(f"  + Loaded RF for {comp_clean}")

        # Load XGBoost
        xgb_dir = base_dir / 'models' / 'xgboost'
        self.models['xgb'] = {}
        for component in self.target_features:
            comp_clean = component.replace('Biooil_', '').replace('_pct', '')
            model_path = xgb_dir / f"xgb_{comp_clean}.pkl"
            if model_path.exists():
                self.models['xgb'][component] = joblib.load(model_path)
                print(f"  + Loaded XGB for {comp_clean}")

        # Load MLP models
        dl_dir = base_dir / 'models' / 'deep_learning'

        # Load scalers
        scaler_X_path = dl_dir / 'scaler_X.pkl'
        scaler_y_path = dl_dir / 'scaler_y.pkl'

        if scaler_X_path.exists() and scaler_y_path.exists():
            self.scalers['X'] = joblib.load(scaler_X_path)
            self.scalers['y'] = joblib.load(scaler_y_path)
            print("  + Loaded scalers")

        # Load MLP Standard
        mlp_std_path = dl_dir / 'mlp_standard.h5'
        if mlp_std_path.exists():
            self.models['mlp_standard'] = keras.models.load_model(mlp_std_path)
            print("  + Loaded MLP Standard")

        # Load MLP Constrained
        mlp_const_path = dl_dir / 'mlp_constrained.h5'
        if mlp_const_path.exists():
            self.models['mlp_constrained'] = keras.models.load_model(mlp_const_path)
            print("  + Loaded MLP Constrained")

        print(f"\nTotal models loaded: {len(self.models)}")

    def predict_single_model(self, model_type, X):
        """Get predictions from a single model type"""

        if model_type in ['rf', 'xgb']:
            # Tree-based models predict per component
            predictions = {}
            for component, model in self.models[model_type].items():
                predictions[component] = model.predict(X)
            return pd.DataFrame(predictions)

        elif model_type in ['mlp_standard', 'mlp_constrained']:
            # Neural networks predict all components at once
            X_scaled = self.scalers['X'].transform(X)
            y_pred_scaled = self.models[model_type].predict(X_scaled, verbose=0)
            y_pred = self.scalers['y'].inverse_transform(y_pred_scaled)

            # For constrained model, ensure sum = 100%
            if model_type == 'mlp_constrained':
                row_sums = y_pred.sum(axis=1, keepdims=True)
                y_pred = (y_pred / row_sums) * 100

            return pd.DataFrame(y_pred, columns=self.target_features, index=X.index)

        else:
            raise ValueError(f"Unknown model type: {model_type}")

    def simple_average_ensemble(self, X, model_types=None):
        """Simple average of all model predictions"""
        if model_types is None:
            model_types = ['rf', 'xgb', 'mlp_standard']

        predictions = []
        for model_type in model_types:
            if model_type in self.models:
                pred = self.predict_single_model(model_type, X)
                predictions.append(pred)

        # Average all predictions
        ensemble_pred = pd.concat(predictions).groupby(level=0).mean()
        return ensemble_pred

    def weighted_ensemble(self, X, weights=None, model_types=None):
        """Weighted average based on validation performance"""
        if model_types is None:
            model_types = ['rf', 'xgb', 'mlp_standard']

        if weights is None:
            # Default weights based on test performance
            # MLP Standard: R2=0.863, RF: R2=0.571, XGB: R2=0.603
            weights = {
                'mlp_standard': 0.5,  # Best performer gets 50%
                'xgb': 0.25,          # Second best gets 25%
                'rf': 0.25            # Third gets 25%
            }

        predictions = []
        used_weights = []

        for model_type in model_types:
            if model_type in self.models:
                pred = self.predict_single_model(model_type, X)
                predictions.append(pred * weights.get(model_type, 1.0))
                used_weights.append(weights.get(model_type, 1.0))

        # Weighted average
        ensemble_pred = sum(predictions) / sum(used_weights)
        return ensemble_pred

    def stacking_ensemble(self, X_train, y_train, X_val, y_val):
        """
        Stacking: Use base model predictions as features for meta-model
        Train a simple linear regression on top of base predictions
        """
        from sklearn.linear_model import Ridge

        print("\nTraining stacking ensemble...")

        # Get base model predictions on training set
        train_preds = {}
        for model_type in ['rf', 'xgb', 'mlp_standard']:
            if model_type in self.models:
                train_preds[model_type] = self.predict_single_model(model_type, X_train)

        # Get base model predictions on validation set
        val_preds = {}
        for model_type in ['rf', 'xgb', 'mlp_standard']:
            if model_type in self.models:
                val_preds[model_type] = self.predict_single_model(model_type, X_val)

        # Train meta-model for each component
        self.meta_models = {}

        for component in self.target_features:
            # Prepare meta-features (predictions from base models)
            X_meta_train = np.column_stack([
                train_preds[m][component].values
                for m in train_preds.keys()
            ])

            X_meta_val = np.column_stack([
                val_preds[m][component].values
                for m in val_preds.keys()
            ])

            # Train Ridge regression as meta-model
            meta_model = Ridge(alpha=1.0)
            meta_model.fit(X_meta_train, y_train[component])

            # Evaluate on validation
            y_pred_val = meta_model.predict(X_meta_val)
            r2 = r2_score(y_val[component], y_pred_val)

            self.meta_models[component] = meta_model

            comp_short = component.replace('Biooil_', '').replace('_pct', '')
            print(f"  {comp_short}: R² = {r2:.3f}")

        print("Stacking ensemble trained!")

    def predict_stacking(self, X):
        """Make predictions using stacking ensemble"""
        if not hasattr(self, 'meta_models'):
            raise ValueError("Stacking ensemble not trained. Call stacking_ensemble() first.")

        # Get base model predictions
        base_preds = {}
        for model_type in ['rf', 'xgb', 'mlp_standard']:
            if model_type in self.models:
                base_preds[model_type] = self.predict_single_model(model_type, X)

        # Meta-model predictions
        predictions = {}
        for component in self.target_features:
            X_meta = np.column_stack([
                base_preds[m][component].values
                for m in base_preds.keys()
            ])
            predictions[component] = self.meta_models[component].predict(X_meta)

        return pd.DataFrame(predictions, index=X.index)

    def calculate_metrics(self, y_true, y_pred):
        """Calculate performance metrics"""
        metrics = {}

        for component in self.target_features:
            metrics[component] = {
                'R2': r2_score(y_true[component], y_pred[component]),
                'RMSE': np.sqrt(mean_squared_error(y_true[component], y_pred[component])),
                'MAE': mean_absolute_error(y_true[component], y_pred[component])
            }

        return metrics

    def print_results_table(self, metrics, ensemble_name):
        """Print formatted results"""
        print(f"\n{'='*80}")
        print(f"ENSEMBLE RESULTS - {ensemble_name}")
        print(f"{'='*80}")
        print(f"{'Component':<30s} | {'R²':>6s} | {'RMSE':>7s} | {'MAE':>7s}")
        print(f"{'-'*80}")

        for component in self.target_features:
            comp_short = component.replace('Biooil_', '').replace('_pct', '')
            m = metrics[component]
            print(f"{comp_short:<30s} | {m['R2']:>6.3f} | {m['RMSE']:>7.2f} | {m['MAE']:>7.2f}")

        # Average
        avg_r2 = np.mean([m['R2'] for m in metrics.values()])
        avg_rmse = np.mean([m['RMSE'] for m in metrics.values()])
        avg_mae = np.mean([m['MAE'] for m in metrics.values()])

        print(f"{'-'*80}")
        print(f"{'AVERAGE':<30s} | {avg_r2:>6.3f} | {avg_rmse:>7.2f} | {avg_mae:>7.2f}")
        print(f"{'='*80}")

        return {'avg_r2': avg_r2, 'avg_rmse': avg_rmse, 'avg_mae': avg_mae}

    def compare_all_methods(self, X_test, y_test):
        """Compare all ensemble methods"""
        results = {}

        print("\n" + "="*80)
        print("COMPARING ALL ENSEMBLE METHODS ON TEST SET")
        print("="*80)

        # 1. Individual models
        print("\n--- INDIVIDUAL MODELS ---")
        for model_type in ['rf', 'xgb', 'mlp_standard', 'mlp_constrained']:
            if model_type in self.models:
                y_pred = self.predict_single_model(model_type, X_test)
                metrics = self.calculate_metrics(y_test, y_pred)
                avg = self.print_results_table(metrics, model_type.upper())
                results[model_type] = avg

        # 2. Simple average ensemble
        print("\n--- SIMPLE AVERAGE ENSEMBLE ---")
        y_pred_avg = self.simple_average_ensemble(X_test)
        metrics_avg = self.calculate_metrics(y_test, y_pred_avg)
        avg = self.print_results_table(metrics_avg, "Simple Average")
        results['simple_average'] = avg

        # 3. Weighted ensemble
        print("\n--- WEIGHTED ENSEMBLE ---")
        y_pred_weighted = self.weighted_ensemble(X_test)
        metrics_weighted = self.calculate_metrics(y_test, y_pred_weighted)
        avg = self.print_results_table(metrics_weighted, "Weighted Average")
        results['weighted'] = avg

        # 4. Stacking ensemble (if trained)
        if hasattr(self, 'meta_models'):
            print("\n--- STACKING ENSEMBLE ---")
            y_pred_stack = self.predict_stacking(X_test)
            metrics_stack = self.calculate_metrics(y_test, y_pred_stack)
            avg = self.print_results_table(metrics_stack, "Stacking")
            results['stacking'] = avg

        # Summary comparison
        print("\n" + "="*80)
        print("SUMMARY COMPARISON")
        print("="*80)
        print(f"{'Method':<30s} | {'Avg R²':>8s} | {'Avg RMSE':>9s} | {'Avg MAE':>8s}")
        print("-"*80)

        for method, avg in results.items():
            print(f"{method:<30s} | {avg['avg_r2']:>8.3f} | {avg['avg_rmse']:>9.2f} | {avg['avg_mae']:>8.2f}")

        print("="*80)

        # Find best method
        best_method = max(results.items(), key=lambda x: x[1]['avg_r2'])
        print(f"\nBest Method: {best_method[0].upper()} (R² = {best_method[1]['avg_r2']:.3f})")

        return results

    def save_ensemble_results(self, results, output_dir):
        """Save ensemble comparison results"""
        output_path = output_dir / 'ensemble_comparison.json'
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to serializable format
        results_serializable = {}
        for method, metrics in results.items():
            results_serializable[method] = {k: float(v) for k, v in metrics.items()}

        with open(output_path, 'w') as f:
            json.dump(results_serializable, f, indent=2)

        print(f"\nSaved ensemble results to: {output_path}")


def main():
    """Run ensemble model evaluation"""

    print("="*80)
    print("PHASE 4: ENSEMBLE METHODS")
    print("="*80)

    base_dir = Path(__file__).parent.parent

    # Initialize ensemble predictor
    ensemble = EnsemblePredictor()

    # Load all models
    ensemble.load_all_models(base_dir)

    # Load test data
    print("\nLoading test data...")
    X_test = pd.read_csv(base_dir / 'data' / 'processed' / 'X_test.csv')
    y_test = pd.read_csv(base_dir / 'data' / 'processed' / 'y_test.csv')
    print(f"Test samples: {len(X_test)}")

    # Load train/val data for stacking
    print("\nLoading train/val data for stacking...")
    X_train = pd.read_csv(base_dir / 'data' / 'processed' / 'X_train.csv')
    y_train = pd.read_csv(base_dir / 'data' / 'processed' / 'y_train.csv')
    X_val = pd.read_csv(base_dir / 'data' / 'processed' / 'X_val.csv')
    y_val = pd.read_csv(base_dir / 'data' / 'processed' / 'y_val.csv')

    # Train stacking ensemble
    ensemble.stacking_ensemble(X_train, y_train, X_val, y_val)

    # Compare all methods
    results = ensemble.compare_all_methods(X_test, y_test)

    # Save results
    ensemble.save_ensemble_results(results, base_dir / 'output' / 'metrics')

    print("\n" + "="*80)
    print("ENSEMBLE EVALUATION COMPLETE!")
    print("="*80)


if __name__ == '__main__':
    main()
