"""
Final Test Set Evaluation
Evaluate best models on held-out test data
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import json
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


class TestEvaluator:
    """Evaluate models on test set"""

    def __init__(self):
        self.target_features = [
            'Biooil_Aromatics_pct',
            'Biooil_Acids_pct',
            'Biooil_Alcohols_pct',
            'Biooil_Furans_pct',
            'Biooil_Phenols_pct',
            'Biooil_Aldehydes_Ketones_pct'
        ]

    def load_test_data(self, data_dir):
        """Load test set"""
        X_test = pd.read_csv(data_dir / 'X_test.csv')
        y_test = pd.read_csv(data_dir / 'y_test.csv')
        return X_test, y_test

    def load_models(self, models_dir, model_type='rf'):
        """Load trained models"""
        models = {}
        model_dir = models_dir / ('random_forest' if model_type == 'rf' else 'xgboost')

        for component in self.target_features:
            component_clean = component.replace('Biooil_', '').replace('_pct', '')
            model_path = model_dir / f"{model_type}_{component_clean}.pkl"
            if model_path.exists():
                models[component] = joblib.load(model_path)

        return models

    def predict_all(self, models, X):
        """Predict all components"""
        predictions = {}
        for component, model in models.items():
            predictions[component] = model.predict(X)
        return pd.DataFrame(predictions)

    def calculate_metrics(self, y_true, y_pred):
        """Calculate all metrics"""
        metrics = {}

        for component in self.target_features:
            metrics[component] = {
                'R2': r2_score(y_true[component], y_pred[component]),
                'RMSE': np.sqrt(mean_squared_error(y_true[component], y_pred[component])),
                'MAE': mean_absolute_error(y_true[component], y_pred[component]),
                'MAPE': np.mean(np.abs((y_true[component] - y_pred[component]) / (y_true[component] + 1e-10))) * 100,
                'Max_Error': np.max(np.abs(y_true[component] - y_pred[component]))
            }

        return metrics

    def print_results_table(self, metrics, model_name):
        """Print formatted results table"""
        print(f"\n{'='*90}")
        print(f"TEST SET RESULTS - {model_name}")
        print(f"{'='*90}")
        print(f"{'Component':<30s} | {'R²':>6s} | {'RMSE':>7s} | {'MAE':>7s} | {'MAPE':>7s} | {'Max Err':>7s}")
        print(f"{'-'*90}")

        for component in self.target_features:
            comp_short = component.replace('Biooil_', '').replace('_pct', '')
            m = metrics[component]
            print(f"{comp_short:<30s} | {m['R2']:>6.3f} | {m['RMSE']:>7.2f} | "
                  f"{m['MAE']:>7.2f} | {m['MAPE']:>7.1f} | {m['Max_Error']:>7.2f}")

        # Average metrics
        avg_r2 = np.mean([m['R2'] for m in metrics.values()])
        avg_rmse = np.mean([m['RMSE'] for m in metrics.values()])
        avg_mae = np.mean([m['MAE'] for m in metrics.values()])
        avg_mape = np.mean([m['MAPE'] for m in metrics.values()])

        print(f"{'-'*90}")
        print(f"{'AVERAGE':<30s} | {avg_r2:>6.3f} | {avg_rmse:>7.2f} | "
              f"{avg_mae:>7.2f} | {avg_mape:>7.1f} |")
        print(f"{'='*90}")

    def analyze_predictions(self, y_true, y_pred):
        """Analyze prediction quality"""
        print(f"\n{'='*90}")
        print("PREDICTION ANALYSIS")
        print(f"{'='*90}")

        # Composition sum analysis
        y_pred_sum = y_pred.sum(axis=1)
        y_true_sum = y_true.sum(axis=1)

        print(f"\nBio-oil Composition Sum (should be ~100%):")
        print(f"  True:      Mean = {y_true_sum.mean():.2f}%, Std = {y_true_sum.std():.2f}%")
        print(f"  Predicted: Mean = {y_pred_sum.mean():.2f}%, Std = {y_pred_sum.std():.2f}%")
        print(f"  Error:     Mean = {(y_pred_sum - y_true_sum).mean():.2f}%, "
              f"Std = {(y_pred_sum - y_true_sum).std():.2f}%")

        # Component-wise analysis
        print(f"\nPer-Component Analysis:")
        print(f"{'Component':<30s} | {'Mean True':>10s} | {'Mean Pred':>10s} | {'Bias':>8s}")
        print(f"{'-'*70}")

        for component in self.target_features:
            comp_short = component.replace('Biooil_', '').replace('_pct', '')
            mean_true = y_true[component].mean()
            mean_pred = y_pred[component].mean()
            bias = mean_pred - mean_true

            print(f"{comp_short:<30s} | {mean_true:>10.2f} | {mean_pred:>10.2f} | {bias:>+8.2f}")

        # Prediction range analysis
        print(f"\nPrediction Ranges:")
        print(f"{'Component':<30s} | {'True Min-Max':>15s} | {'Pred Min-Max':>15s}")
        print(f"{'-'*70}")

        for component in self.target_features:
            comp_short = component.replace('Biooil_', '').replace('_pct', '')
            true_range = f"{y_true[component].min():.1f}-{y_true[component].max():.1f}"
            pred_range = f"{y_pred[component].min():.1f}-{y_pred[component].max():.1f}"

            print(f"{comp_short:<30s} | {true_range:>15s} | {pred_range:>15s}")

    def save_test_results(self, metrics, output_dir, model_name):
        """Save test results to JSON"""
        output_path = output_dir / f'test_results_{model_name.lower()}.json'
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to serializable format
        metrics_serializable = {}
        for component, m in metrics.items():
            metrics_serializable[component] = {k: float(v) for k, v in m.items()}

        with open(output_path, 'w') as f:
            json.dump(metrics_serializable, f, indent=2)

        print(f"\nSaved test results to: {output_path}")


def main():
    """Run test set evaluation"""

    print("="*90)
    print("FINAL TEST SET EVALUATION")
    print("="*90)

    base_dir = Path(__file__).parent.parent
    evaluator = TestEvaluator()

    # Load test data
    print("\nLoading test data...")
    X_test, y_test = evaluator.load_test_data(base_dir / 'data' / 'processed')
    print(f"  Test samples: {len(X_test)}")

    # Evaluate Random Forest
    print("\n" + "-"*90)
    print("Evaluating Random Forest...")
    print("-"*90)

    models_rf = evaluator.load_models(base_dir / 'models', 'rf')
    y_pred_rf = evaluator.predict_all(models_rf, X_test)
    metrics_rf = evaluator.calculate_metrics(y_test, y_pred_rf)

    evaluator.print_results_table(metrics_rf, "Random Forest")
    evaluator.analyze_predictions(y_test, y_pred_rf)
    evaluator.save_test_results(metrics_rf, base_dir / 'output' / 'metrics', 'random_forest')

    # Evaluate XGBoost (if available)
    try:
        print("\n" + "-"*90)
        print("Evaluating XGBoost...")
        print("-"*90)

        models_xgb = evaluator.load_models(base_dir / 'models', 'xgb')
        if models_xgb:
            y_pred_xgb = evaluator.predict_all(models_xgb, X_test)
            metrics_xgb = evaluator.calculate_metrics(y_test, y_pred_xgb)

            evaluator.print_results_table(metrics_xgb, "XGBoost")
            evaluator.save_test_results(metrics_xgb, base_dir / 'output' / 'metrics', 'xgboost')
    except Exception as e:
        print(f"\nXGBoost evaluation skipped: {e}")

    # Compare with validation results
    print("\n" + "="*90)
    print("VALIDATION vs TEST COMPARISON")
    print("="*90)

    # Load validation metrics
    val_metrics_path = base_dir / 'output' / 'metrics' / 'baseline_metrics.json'
    if val_metrics_path.exists():
        with open(val_metrics_path, 'r') as f:
            val_metrics = json.load(f)

        print("\nRandom Forest - Average R²:")
        val_r2_avg = np.mean([v['R2'] for v in val_metrics['random_forest'].values()])
        test_r2_avg = np.mean([v['R2'] for v in metrics_rf.values()])

        print(f"  Validation: {val_r2_avg:.3f}")
        print(f"  Test:       {test_r2_avg:.3f}")
        print(f"  Difference: {test_r2_avg - val_r2_avg:+.3f}")

        if abs(test_r2_avg - val_r2_avg) < 0.05:
            print("  → Good generalization (difference < 0.05)")
        else:
            print("  → Warning: Possible overfitting or underfitting")

    print("\n" + "="*90)
    print("TEST EVALUATION COMPLETE!")
    print("="*90)


if __name__ == '__main__':
    main()
