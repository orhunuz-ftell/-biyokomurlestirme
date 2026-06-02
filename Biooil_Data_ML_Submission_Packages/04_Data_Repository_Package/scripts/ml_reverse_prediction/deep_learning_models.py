"""
Deep Learning Models for Reverse Prediction
Multi-Layer Perceptron with and without constraints
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import warnings
warnings.filterwarnings('ignore')

# Check TensorFlow availability
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, callbacks
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
    TF_AVAILABLE = True
    print(f"TensorFlow {tf.__version__} available")
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow not available. Install with: pip install tensorflow")


class DeepLearningModels:
    """Train and evaluate deep learning models"""

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

        self.scaler_X = None
        self.scaler_y = None
        self.models = {}

    def load_data(self, data_dir):
        """Load train, validation, and test data"""
        X_train = pd.read_csv(data_dir / 'X_train.csv')
        X_val = pd.read_csv(data_dir / 'X_val.csv')
        X_test = pd.read_csv(data_dir / 'X_test.csv')
        y_train = pd.read_csv(data_dir / 'y_train.csv')
        y_val = pd.read_csv(data_dir / 'y_val.csv')
        y_test = pd.read_csv(data_dir / 'y_test.csv')

        return X_train, X_val, X_test, y_train, y_val, y_test

    def normalize_data(self, X_train, X_val, X_test, y_train, y_val, y_test):
        """Normalize inputs and outputs"""
        print("\nNormalizing data...")

        # Normalize inputs (StandardScaler: mean=0, std=1)
        self.scaler_X = StandardScaler()
        X_train_scaled = self.scaler_X.fit_transform(X_train)
        X_val_scaled = self.scaler_X.transform(X_val)
        X_test_scaled = self.scaler_X.transform(X_test)

        # Normalize outputs (StandardScaler)
        self.scaler_y = StandardScaler()
        y_train_scaled = self.scaler_y.fit_transform(y_train)
        y_val_scaled = self.scaler_y.transform(y_val)
        y_test_scaled = self.scaler_y.transform(y_test)

        print(f"  Input scaling:  mean={self.scaler_X.mean_[:3]}, std={self.scaler_X.scale_[:3]}")
        print(f"  Output scaling: mean={self.scaler_y.mean_[:3]}, std={self.scaler_y.scale_[:3]}")

        return X_train_scaled, X_val_scaled, X_test_scaled, y_train_scaled, y_val_scaled, y_test_scaled

    def build_mlp_model(self, input_dim, output_dim, architecture='standard'):
        """
        Build Multi-Layer Perceptron model

        Args:
            input_dim: Number of input features
            output_dim: Number of output targets
            architecture: 'standard' or 'constrained'
        """
        model = keras.Sequential(name=f'MLP_{architecture}')

        # Input layer + First hidden layer
        model.add(layers.Dense(128, activation='relu', input_dim=input_dim,
                              kernel_initializer='he_normal'))
        model.add(layers.BatchNormalization())
        model.add(layers.Dropout(0.3))

        # Second hidden layer
        model.add(layers.Dense(64, activation='relu',
                              kernel_initializer='he_normal'))
        model.add(layers.BatchNormalization())
        model.add(layers.Dropout(0.2))

        # Third hidden layer
        model.add(layers.Dense(32, activation='relu',
                              kernel_initializer='he_normal'))
        model.add(layers.Dropout(0.1))

        # Output layer
        if architecture == 'constrained':
            # Softmax ensures outputs sum to 1.0 (proportions)
            model.add(layers.Dense(output_dim, activation='softmax',
                                  name='output_constrained'))
        else:
            # Standard linear output
            model.add(layers.Dense(output_dim, activation='linear',
                                  name='output_standard'))

        return model

    def train_mlp_standard(self, X_train, X_val, y_train, y_val, epochs=200, batch_size=32):
        """Train MLP with standard output layer"""
        print("\n" + "="*80)
        print("TRAINING: MLP (STANDARD OUTPUT)")
        print("="*80)

        model = self.build_mlp_model(
            input_dim=len(self.input_features),
            output_dim=len(self.target_features),
            architecture='standard'
        )

        # Compile
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )

        # Print model summary
        print("\nModel Architecture:")
        model.summary()

        # Callbacks
        early_stop = callbacks.EarlyStopping(
            monitor='val_loss',
            patience=30,
            restore_best_weights=True,
            verbose=1
        )

        reduce_lr = callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=15,
            min_lr=1e-6,
            verbose=1
        )

        # Train
        print("\nTraining...")
        history = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stop, reduce_lr],
            verbose=1
        )

        self.models['mlp_standard'] = model

        return model, history

    def train_mlp_constrained(self, X_train, X_val, y_train, y_val, epochs=200, batch_size=32):
        """Train MLP with softmax output (sum to 1.0 constraint)"""
        print("\n" + "="*80)
        print("TRAINING: MLP (CONSTRAINED OUTPUT - SOFTMAX)")
        print("="*80)

        # Convert outputs to proportions (0-1, sum=1)
        print("\nConverting outputs to proportions...")
        y_train_prop = y_train / y_train.sum(axis=1, keepdims=True)
        y_val_prop = y_val / y_val.sum(axis=1, keepdims=True)

        print(f"  Original y range: {y_train.min().min():.2f} - {y_train.max().max():.2f}")
        print(f"  Proportion y range: {y_train_prop.min().min():.4f} - {y_train_prop.max().max():.4f}")
        print(f"  Proportion sum check: {y_train_prop.sum(axis=1).mean():.6f} (should be 1.0)")

        model = self.build_mlp_model(
            input_dim=len(self.input_features),
            output_dim=len(self.target_features),
            architecture='constrained'
        )

        # Compile - use KL divergence for probability distributions
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='kullback_leibler_divergence',  # Good for distributions
            metrics=['mae']
        )

        # Print model summary
        print("\nModel Architecture:")
        model.summary()

        # Callbacks
        early_stop = callbacks.EarlyStopping(
            monitor='val_loss',
            patience=30,
            restore_best_weights=True,
            verbose=1
        )

        reduce_lr = callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=15,
            min_lr=1e-6,
            verbose=1
        )

        # Train
        print("\nTraining...")
        history = model.fit(
            X_train, y_train_prop,
            validation_data=(X_val, y_val_prop),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stop, reduce_lr],
            verbose=1
        )

        self.models['mlp_constrained'] = model

        return model, history

    def evaluate_model(self, model, X, y, model_name, is_constrained=False):
        """Evaluate model and return metrics"""

        # Predict
        if is_constrained:
            # Model outputs proportions (0-1, sum=1)
            y_prop = y / y.sum(axis=1, keepdims=True)
            y_pred_prop = model.predict(X, verbose=0)

            # Convert back to percentages
            y_pred = y_pred_prop * 100  # Predictions
            y_true = y  # Original scale
        else:
            # Standard model
            y_pred_scaled = model.predict(X, verbose=0)
            y_pred = self.scaler_y.inverse_transform(y_pred_scaled)
            y_true = y

        # Calculate metrics per component
        metrics = {}
        for idx, component in enumerate(self.target_features):
            metrics[component] = {
                'R2': r2_score(y_true[:, idx], y_pred[:, idx]),
                'RMSE': np.sqrt(mean_squared_error(y_true[:, idx], y_pred[:, idx])),
                'MAE': mean_absolute_error(y_true[:, idx], y_pred[:, idx])
            }

        # Print results
        print(f"\n{'='*80}")
        print(f"{model_name.upper()} - EVALUATION RESULTS")
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

        # Composition sum analysis
        y_pred_sum = y_pred.sum(axis=1)
        print(f"\nComposition Sum Analysis:")
        print(f"  Predicted sum: {y_pred_sum.mean():.2f}% ± {y_pred_sum.std():.2f}%")
        print(f"  Range: {y_pred_sum.min():.2f}% - {y_pred_sum.max():.2f}%")

        return metrics, y_pred

    def save_model(self, model, model_name, output_dir):
        """Save Keras model"""
        output_path = output_dir / f'{model_name}.h5'
        output_path.parent.mkdir(parents=True, exist_ok=True)

        model.save(output_path)
        print(f"\nSaved model to: {output_path}")

    def save_metrics(self, all_metrics, output_path):
        """Save metrics to JSON"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to serializable format
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

    if not TF_AVAILABLE:
        print("\nERROR: TensorFlow not available. Please install:")
        print("  pip install tensorflow")
        return

    print("="*80)
    print("DEEP LEARNING MODELS - PHASE 3")
    print("="*80)

    # Initialize
    trainer = DeepLearningModels()

    # Load data
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'data' / 'processed'

    print("\nLoading data...")
    X_train, X_val, X_test, y_train, y_val, y_test = trainer.load_data(data_dir)
    print(f"  Train: {len(X_train)} samples")
    print(f"  Validation: {len(X_val)} samples")
    print(f"  Test: {len(X_test)} samples")

    # Normalize data
    X_train_scaled, X_val_scaled, X_test_scaled, \
    y_train_scaled, y_val_scaled, y_test_scaled = trainer.normalize_data(
        X_train, X_val, X_test, y_train, y_val, y_test
    )

    # Store all metrics
    all_metrics = {}

    # Train Model 1: MLP with standard output
    model_std, history_std = trainer.train_mlp_standard(
        X_train_scaled, X_val_scaled, y_train_scaled, y_val_scaled,
        epochs=200, batch_size=32
    )

    # Evaluate on validation set
    metrics_std_val, _ = trainer.evaluate_model(
        model_std, X_val_scaled, y_val.values, 'MLP Standard (Validation)',
        is_constrained=False
    )
    all_metrics['mlp_standard_val'] = metrics_std_val

    # Evaluate on test set
    metrics_std_test, _ = trainer.evaluate_model(
        model_std, X_test_scaled, y_test.values, 'MLP Standard (Test)',
        is_constrained=False
    )
    all_metrics['mlp_standard_test'] = metrics_std_test

    # Save model
    trainer.save_model(model_std, 'mlp_standard', base_dir / 'models' / 'deep_learning')

    # Train Model 2: MLP with constrained output
    model_const, history_const = trainer.train_mlp_constrained(
        X_train_scaled, X_val_scaled, y_train.values, y_val.values,
        epochs=200, batch_size=32
    )

    # Evaluate on validation set
    metrics_const_val, _ = trainer.evaluate_model(
        model_const, X_val_scaled, y_val.values, 'MLP Constrained (Validation)',
        is_constrained=True
    )
    all_metrics['mlp_constrained_val'] = metrics_const_val

    # Evaluate on test set
    metrics_const_test, _ = trainer.evaluate_model(
        model_const, X_test_scaled, y_test.values, 'MLP Constrained (Test)',
        is_constrained=True
    )
    all_metrics['mlp_constrained_test'] = metrics_const_test

    # Save model
    trainer.save_model(model_const, 'mlp_constrained', base_dir / 'models' / 'deep_learning')

    # Save metrics
    metrics_path = base_dir / 'output' / 'metrics' / 'deep_learning_metrics.json'
    trainer.save_metrics(all_metrics, metrics_path)

    # Save scalers
    import joblib
    scaler_dir = base_dir / 'models' / 'deep_learning'
    scaler_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(trainer.scaler_X, scaler_dir / 'scaler_X.pkl')
    joblib.dump(trainer.scaler_y, scaler_dir / 'scaler_y.pkl')
    print(f"\nSaved scalers to: {scaler_dir}")

    # Summary
    print("\n" + "="*80)
    print("DEEP LEARNING TRAINING COMPLETE!")
    print("="*80)

    print("\nTest Set Performance Summary:")
    print(f"\nMLP Standard:")
    avg_r2_std = np.mean([m['R2'] for m in metrics_std_test.values()])
    avg_mae_std = np.mean([m['MAE'] for m in metrics_std_test.values()])
    print(f"  Average R²:  {avg_r2_std:.3f}")
    print(f"  Average MAE: {avg_mae_std:.2f}%")

    print(f"\nMLP Constrained:")
    avg_r2_const = np.mean([m['R2'] for m in metrics_const_test.values()])
    avg_mae_const = np.mean([m['MAE'] for m in metrics_const_test.values()])
    print(f"  Average R²:  {avg_r2_const:.3f}")
    print(f"  Average MAE: {avg_mae_const:.2f}%")

    # Compare with baseline (load from file)
    baseline_path = base_dir / 'output' / 'metrics' / 'test_results_random_forest.json'
    if baseline_path.exists():
        with open(baseline_path, 'r') as f:
            baseline_metrics = json.load(f)

        avg_r2_rf = np.mean([m['R2'] for m in baseline_metrics.values()])
        avg_mae_rf = np.mean([m['MAE'] for m in baseline_metrics.values()])

        print(f"\nBaseline (Random Forest):")
        print(f"  Average R²:  {avg_r2_rf:.3f}")
        print(f"  Average MAE: {avg_mae_rf:.2f}%")

        print(f"\nImprovement vs Baseline:")
        print(f"  MLP Standard:    R² {avg_r2_std - avg_r2_rf:+.3f}, MAE {avg_mae_std - avg_mae_rf:+.2f}%")
        print(f"  MLP Constrained: R² {avg_r2_const - avg_r2_rf:+.3f}, MAE {avg_mae_const - avg_mae_rf:+.2f}%")


if __name__ == '__main__':
    main()
