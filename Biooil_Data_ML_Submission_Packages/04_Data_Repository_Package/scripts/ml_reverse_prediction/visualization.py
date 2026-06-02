"""
Visualization and Analysis Tools
Generate plots for thesis and evaluation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import joblib
import json

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


class ModelVisualizer:
    """Create visualizations for model evaluation"""

    def __init__(self, models_dir, data_dir, output_dir):
        self.models_dir = Path(models_dir)
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.target_features = [
            'Biooil_Aromatics_pct',
            'Biooil_Acids_pct',
            'Biooil_Alcohols_pct',
            'Biooil_Furans_pct',
            'Biooil_Phenols_pct',
            'Biooil_Aldehydes_Ketones_pct'
        ]

        self.feature_labels = {
            'Biooil_Aromatics_pct': 'Aromatics',
            'Biooil_Acids_pct': 'Acids',
            'Biooil_Alcohols_pct': 'Alcohols',
            'Biooil_Furans_pct': 'Furans',
            'Biooil_Phenols_pct': 'Phenols',
            'Biooil_Aldehydes_Ketones_pct': 'Aldehydes/Ketones'
        }

    def load_data(self):
        """Load train, validation, and test data"""
        X_val = pd.read_csv(self.data_dir / 'X_val.csv')
        y_val = pd.read_csv(self.data_dir / 'y_val.csv')
        X_test = pd.read_csv(self.data_dir / 'X_test.csv')
        y_test = pd.read_csv(self.data_dir / 'y_test.csv')
        return X_val, y_val, X_test, y_test

    def load_models(self, model_type='rf'):
        """Load trained models"""
        models = {}
        model_dir = self.models_dir / ('random_forest' if model_type == 'rf' else 'xgboost')

        for component in self.target_features:
            component_clean = component.replace('Biooil_', '').replace('_pct', '')
            model_path = model_dir / f"{model_type}_{component_clean}.pkl"
            if model_path.exists():
                models[component] = joblib.load(model_path)

        return models

    def predict_all_components(self, models, X):
        """Predict all components and return as DataFrame"""
        predictions = {}
        for component, model in models.items():
            predictions[component] = model.predict(X)

        return pd.DataFrame(predictions)

    def plot_predicted_vs_actual(self, y_true, y_pred, model_name='Random Forest'):
        """Create predicted vs actual scatter plots"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()

        for idx, component in enumerate(self.target_features):
            ax = axes[idx]

            # Scatter plot
            ax.scatter(y_true[component], y_pred[component],
                      alpha=0.5, s=30, edgecolors='k', linewidth=0.5)

            # Perfect prediction line
            min_val = min(y_true[component].min(), y_pred[component].min())
            max_val = max(y_true[component].max(), y_pred[component].max())
            ax.plot([min_val, max_val], [min_val, max_val],
                   'r--', lw=2, label='Perfect prediction')

            # Labels
            ax.set_xlabel('Actual (%)', fontsize=11)
            ax.set_ylabel('Predicted (%)', fontsize=11)
            ax.set_title(self.feature_labels[component], fontsize=12, fontweight='bold')

            # R² score
            from sklearn.metrics import r2_score
            r2 = r2_score(y_true[component], y_pred[component])
            ax.text(0.05, 0.95, f'R² = {r2:.3f}',
                   transform=ax.transAxes,
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                   verticalalignment='top', fontsize=10)

            ax.legend(loc='lower right', fontsize=9)
            ax.grid(True, alpha=0.3)

        plt.suptitle(f'Predicted vs Actual - {model_name}',
                    fontsize=14, fontweight='bold', y=0.995)
        plt.tight_layout()

        output_path = self.output_dir / f'predicted_vs_actual_{model_name.lower().replace(" ", "_")}.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {output_path}")
        plt.close()

    def plot_residuals(self, y_true, y_pred, model_name='Random Forest'):
        """Create residual distribution plots"""
        residuals = y_true - y_pred

        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()

        for idx, component in enumerate(self.target_features):
            ax = axes[idx]

            # Histogram
            ax.hist(residuals[component], bins=30, alpha=0.7,
                   edgecolor='black', color='steelblue')

            # Mean line
            mean_residual = residuals[component].mean()
            ax.axvline(mean_residual, color='red', linestyle='--',
                      linewidth=2, label=f'Mean = {mean_residual:.2f}%')

            # Zero line
            ax.axvline(0, color='green', linestyle='-',
                      linewidth=1, alpha=0.5, label='Zero')

            # Labels
            ax.set_xlabel('Residual (Actual - Predicted) %', fontsize=11)
            ax.set_ylabel('Frequency', fontsize=11)
            ax.set_title(self.feature_labels[component], fontsize=12, fontweight='bold')

            # Stats
            std_residual = residuals[component].std()
            ax.text(0.05, 0.95,
                   f'Mean = {mean_residual:.2f}%\nStd = {std_residual:.2f}%',
                   transform=ax.transAxes,
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                   verticalalignment='top', fontsize=9)

            ax.legend(loc='upper right', fontsize=9)
            ax.grid(True, alpha=0.3)

        plt.suptitle(f'Residual Distributions - {model_name}',
                    fontsize=14, fontweight='bold', y=0.995)
        plt.tight_layout()

        output_path = self.output_dir / f'residuals_{model_name.lower().replace(" ", "_")}.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {output_path}")
        plt.close()

    def plot_feature_importance(self):
        """Plot feature importance from saved CSV"""
        importance_path = self.output_dir.parent / 'metrics' / 'feature_importance_rf.csv'

        if not importance_path.exists():
            print(f"Feature importance file not found: {importance_path}")
            return

        df_importance = pd.read_csv(importance_path, index_col=0)

        # Plot average importance
        fig, ax = plt.subplots(figsize=(10, 6))

        importance_avg = df_importance['Average'].sort_values(ascending=True)

        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(importance_avg)))
        bars = ax.barh(range(len(importance_avg)), importance_avg.values, color=colors)

        # Labels
        ax.set_yticks(range(len(importance_avg)))
        ax.set_yticklabels(importance_avg.index, fontsize=11)
        ax.set_xlabel('Average Feature Importance', fontsize=12, fontweight='bold')
        ax.set_title('Feature Importance - Random Forest\n(Averaged across all bio-oil components)',
                    fontsize=13, fontweight='bold')

        # Add value labels
        for i, (idx, val) in enumerate(importance_avg.items()):
            ax.text(val + 0.005, i, f'{val:.3f}', va='center', fontsize=10)

        ax.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()

        output_path = self.output_dir / 'feature_importance.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {output_path}")
        plt.close()

        # Plot heatmap of importance per component
        fig, ax = plt.subplots(figsize=(12, 6))

        df_heatmap = df_importance.drop('Average', axis=1)
        df_heatmap.columns = [self.feature_labels[col] for col in df_heatmap.columns]

        sns.heatmap(df_heatmap, annot=True, fmt='.3f', cmap='YlOrRd',
                   cbar_kws={'label': 'Importance'}, ax=ax)

        ax.set_xlabel('Bio-oil Component', fontsize=12, fontweight='bold')
        ax.set_ylabel('Input Feature', fontsize=12, fontweight='bold')
        ax.set_title('Feature Importance by Component - Random Forest',
                    fontsize=13, fontweight='bold')

        plt.tight_layout()

        output_path = self.output_dir / 'feature_importance_heatmap.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {output_path}")
        plt.close()

    def plot_model_comparison(self):
        """Compare different models' performance"""
        metrics_path = self.output_dir.parent / 'metrics' / 'baseline_metrics.json'

        if not metrics_path.exists():
            print(f"Metrics file not found: {metrics_path}")
            return

        with open(metrics_path, 'r') as f:
            all_metrics = json.load(f)

        # Extract R² scores
        models = list(all_metrics.keys())
        components = self.target_features

        r2_data = []
        for model_name in models:
            for component in components:
                r2_data.append({
                    'Model': model_name.replace('_', ' ').title(),
                    'Component': self.feature_labels[component],
                    'R2': all_metrics[model_name][component]['R2']
                })

        df_r2 = pd.DataFrame(r2_data)

        # Grouped bar chart
        fig, ax = plt.subplots(figsize=(14, 7))

        components_short = [self.feature_labels[c] for c in components]
        x = np.arange(len(components_short))
        width = 0.25

        for i, model in enumerate(df_r2['Model'].unique()):
            model_data = df_r2[df_r2['Model'] == model]
            r2_values = [model_data[model_data['Component'] == comp]['R2'].values[0]
                        for comp in components_short]

            offset = (i - 1) * width
            bars = ax.bar(x + offset, r2_values, width, label=model, alpha=0.8)

            # Add value labels
            for j, bar in enumerate(bars):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.2f}',
                       ha='center', va='bottom', fontsize=8)

        ax.set_xlabel('Bio-oil Component', fontsize=12, fontweight='bold')
        ax.set_ylabel('R² Score', fontsize=12, fontweight='bold')
        ax.set_title('Model Comparison - R² Scores by Component',
                    fontsize=13, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(components_short, rotation=45, ha='right')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim(0, 1.0)

        plt.tight_layout()

        output_path = self.output_dir / 'model_comparison_r2.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {output_path}")
        plt.close()

        # Average metrics comparison
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        metrics_names = ['R2', 'RMSE', 'MAE']
        for idx, metric in enumerate(metrics_names):
            ax = axes[idx]

            avg_values = []
            for model_name in models:
                values = [all_metrics[model_name][comp][metric] for comp in components]
                avg_values.append(np.mean(values))

            model_labels = [m.replace('_', ' ').title() for m in models]
            colors = ['steelblue', 'orange', 'green'][:len(models)]

            bars = ax.bar(model_labels, avg_values, color=colors, alpha=0.7, edgecolor='black')

            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}' if metric == 'R2' else f'{height:.2f}',
                       ha='center', va='bottom', fontsize=10, fontweight='bold')

            ax.set_ylabel(f'Average {metric}', fontsize=11, fontweight='bold')
            ax.set_title(f'{metric} Comparison', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')

            if metric == 'R2':
                ax.set_ylim(0, 1.0)

        plt.suptitle('Model Performance Comparison - Average Metrics',
                    fontsize=14, fontweight='bold')
        plt.tight_layout()

        output_path = self.output_dir / 'model_comparison_avg_metrics.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {output_path}")
        plt.close()

    def plot_correlation_matrix(self, X, y):
        """Plot correlation between inputs and outputs"""
        # Combine X and y
        df_combined = pd.concat([X, y], axis=1)

        # Calculate correlation
        corr = df_combined.corr()

        # Extract correlation between inputs and outputs
        input_cols = X.columns
        output_cols = y.columns

        corr_subset = corr.loc[input_cols, output_cols]

        # Rename for readability
        corr_subset.columns = [self.feature_labels[col] for col in corr_subset.columns]

        # Plot
        fig, ax = plt.subplots(figsize=(10, 8))

        sns.heatmap(corr_subset, annot=True, fmt='.2f', cmap='coolwarm',
                   center=0, vmin=-1, vmax=1,
                   cbar_kws={'label': 'Correlation'}, ax=ax)

        ax.set_xlabel('Bio-oil Component (Output)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Input Feature', fontsize=12, fontweight='bold')
        ax.set_title('Correlation: Input Features vs Bio-oil Components',
                    fontsize=13, fontweight='bold')

        plt.tight_layout()

        output_path = self.output_dir / 'correlation_matrix.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {output_path}")
        plt.close()


def main():
    """Generate all visualizations"""

    print("="*80)
    print("GENERATING VISUALIZATIONS")
    print("="*80)

    # Initialize visualizer
    base_dir = Path(__file__).parent.parent
    viz = ModelVisualizer(
        models_dir=base_dir / 'models',
        data_dir=base_dir / 'data' / 'processed',
        output_dir=base_dir / 'output' / 'figures'
    )

    # Load data
    print("\nLoading data...")
    X_val, y_val, X_test, y_test = viz.load_data()
    print(f"  Validation: {len(X_val)} samples")
    print(f"  Test: {len(X_test)} samples")

    # Load Random Forest models
    print("\nLoading Random Forest models...")
    models_rf = viz.load_models('rf')
    print(f"  Loaded {len(models_rf)} models")

    # Predictions
    print("\nGenerating predictions...")
    y_pred_val = viz.predict_all_components(models_rf, X_val)
    y_pred_test = viz.predict_all_components(models_rf, X_test)

    # Generate plots
    print("\n" + "-"*80)
    print("Creating visualizations...")
    print("-"*80)

    # 1. Predicted vs Actual
    print("\n1. Predicted vs Actual (Validation set)...")
    viz.plot_predicted_vs_actual(y_val, y_pred_val, 'Random Forest')

    # 2. Residuals
    print("\n2. Residual Distributions...")
    viz.plot_residuals(y_val, y_pred_val, 'Random Forest')

    # 3. Feature Importance
    print("\n3. Feature Importance...")
    viz.plot_feature_importance()

    # 4. Model Comparison
    print("\n4. Model Comparison...")
    viz.plot_model_comparison()

    # 5. Correlation Matrix
    print("\n5. Correlation Matrix...")
    viz.plot_correlation_matrix(X_val, y_val)

    print("\n" + "="*80)
    print("VISUALIZATION COMPLETE!")
    print("="*80)
    print(f"\nAll figures saved to: {viz.output_dir}")
    print("\nGenerated files:")
    for file in sorted(viz.output_dir.glob('*.png')):
        print(f"  - {file.name}")


if __name__ == '__main__':
    main()
