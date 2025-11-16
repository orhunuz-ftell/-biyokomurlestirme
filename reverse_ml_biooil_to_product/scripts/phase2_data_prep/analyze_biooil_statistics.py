"""
==============================================================================
REVERSE ML PROJECT - PHASE 2: DATA PREPARATION
Script 2: Analyze Bio-oil Composition Statistics
==============================================================================
Purpose: Analyze statistical properties of extracted bio-oil compositions
Author: Orhun Uzdiyem
Date: 2025-11-16
==============================================================================

This script:
1. Reads biooil_compositions_30.csv
2. Performs statistical analysis on 6 main components
3. Generates summary report
4. Identifies outliers and data quality issues

Requirements:
- pandas
- numpy
==============================================================================
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

# Input file path
INPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'data',
    'biooil_reference_data'
)
INPUT_FILE = os.path.join(INPUT_DIR, 'biooil_compositions_30.csv')

# Main components
MAIN_COMPONENTS = ['aromatics', 'acids', 'alcohols', 'furans', 'phenols', 'aldehyde_ketone']


def load_data(filepath):
    """Load bio-oil composition data from CSV."""
    try:
        df = pd.read_csv(filepath)
        print(f"[OK] Loaded data from: {filepath}")
        print(f"  Records: {len(df)}")
        print(f"  Columns: {len(df.columns)}")
        return df
    except FileNotFoundError:
        print(f"[ERROR] Error: File not found: {filepath}")
        print("  Please run extract_biooil_data.py first!")
        raise
    except Exception as e:
        print(f"[ERROR] Error loading data: {e}")
        raise


def calculate_basic_statistics(df):
    """Calculate basic statistics for each component."""

    print("\n" + "="*70)
    print("BASIC STATISTICS")
    print("="*70)

    stats = df[MAIN_COMPONENTS].describe()
    print("\nDescriptive statistics (%):")
    print(stats.round(2))

    # Additional statistics
    print("\n\nAdditional statistics:")
    print(f"{'Component':<20} {'Mean':<10} {'Median':<10} {'Range':<15} {'CV (%)':<10}")
    print("-" * 70)

    for comp in MAIN_COMPONENTS:
        mean_val = df[comp].mean()
        median_val = df[comp].median()
        min_val = df[comp].min()
        max_val = df[comp].max()
        range_val = max_val - min_val
        cv = (df[comp].std() / mean_val) * 100 if mean_val > 0 else 0

        print(f"{comp:<20} {mean_val:<10.2f} {median_val:<10.2f} "
              f"{min_val:.2f}-{max_val:.2f}    {cv:<10.2f}")


def analyze_composition_sum(df):
    """Analyze total composition sum for each record."""

    print("\n" + "="*70)
    print("COMPOSITION SUM ANALYSIS")
    print("="*70)

    # Calculate sum for each record
    df['composition_sum'] = df[MAIN_COMPONENTS].sum(axis=1)

    print(f"\nComposition sum (should be ~100%):")
    print(f"  Mean:   {df['composition_sum'].mean():.2f}%")
    print(f"  Median: {df['composition_sum'].median():.2f}%")
    print(f"  Std:    {df['composition_sum'].std():.2f}%")
    print(f"  Min:    {df['composition_sum'].min():.2f}%")
    print(f"  Max:    {df['composition_sum'].max():.2f}%")

    # Identify records with unusual sums
    unusual_threshold_low = 80
    unusual_threshold_high = 110

    unusual_low = df[df['composition_sum'] < unusual_threshold_low]
    unusual_high = df[df['composition_sum'] > unusual_threshold_high]

    if len(unusual_low) > 0:
        print(f"\n[WARNING] Warning: {len(unusual_low)} records with sum < {unusual_threshold_low}%:")
        for idx, row in unusual_low.iterrows():
            print(f"  BiooilId {row['BiooilId']}: {row['composition_sum']:.2f}%")

    if len(unusual_high) > 0:
        print(f"\n[WARNING] Warning: {len(unusual_high)} records with sum > {unusual_threshold_high}%:")
        for idx, row in unusual_high.iterrows():
            print(f"  BiooilId {row['BiooilId']}: {row['composition_sum']:.2f}%")

    if len(unusual_low) == 0 and len(unusual_high) == 0:
        print(f"\n[OK] All composition sums are within {unusual_threshold_low}-{unusual_threshold_high}% range")


def detect_outliers(df):
    """Detect outliers using IQR method."""

    print("\n" + "="*70)
    print("OUTLIER DETECTION (IQR Method)")
    print("="*70)

    outliers_detected = False

    for comp in MAIN_COMPONENTS:
        Q1 = df[comp].quantile(0.25)
        Q3 = df[comp].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[(df[comp] < lower_bound) | (df[comp] > upper_bound)]

        if len(outliers) > 0:
            outliers_detected = True
            print(f"\n{comp}:")
            print(f"  IQR range: {lower_bound:.2f} - {upper_bound:.2f}%")
            print(f"  Outliers: {len(outliers)} records")
            for idx, row in outliers.iterrows():
                print(f"    BiooilId {row['BiooilId']}: {row[comp]:.2f}%")

    if not outliers_detected:
        print("\n[OK] No outliers detected in any component")


def analyze_correlations(df):
    """Analyze correlations between components."""

    print("\n" + "="*70)
    print("COMPONENT CORRELATIONS")
    print("="*70)

    corr_matrix = df[MAIN_COMPONENTS].corr()

    print("\nCorrelation matrix:")
    print(corr_matrix.round(3))

    # Find strong correlations (|r| > 0.5, excluding diagonal)
    print("\nStrong correlations (|r| > 0.5):")
    strong_corr_found = False

    for i in range(len(MAIN_COMPONENTS)):
        for j in range(i+1, len(MAIN_COMPONENTS)):
            comp1 = MAIN_COMPONENTS[i]
            comp2 = MAIN_COMPONENTS[j]
            corr_val = corr_matrix.loc[comp1, comp2]

            if abs(corr_val) > 0.5:
                strong_corr_found = True
                corr_type = "positive" if corr_val > 0 else "negative"
                print(f"  {comp1} vs {comp2}: {corr_val:.3f} ({corr_type})")

    if not strong_corr_found:
        print("  No strong correlations found")


def check_data_quality(df):
    """Perform data quality checks."""

    print("\n" + "="*70)
    print("DATA QUALITY CHECKS")
    print("="*70)

    issues = []

    # Check 1: Missing values
    missing = df[MAIN_COMPONENTS].isnull().sum()
    if missing.sum() > 0:
        issues.append("Missing values detected")
        print("\n[ERROR] Missing values:")
        for comp in MAIN_COMPONENTS:
            if missing[comp] > 0:
                print(f"  {comp}: {missing[comp]} records")
    else:
        print("\n[OK] No missing values")

    # Check 2: Negative values
    negative_counts = (df[MAIN_COMPONENTS] < 0).sum()
    if negative_counts.sum() > 0:
        issues.append("Negative values detected")
        print("\n[ERROR] Negative values:")
        for comp in MAIN_COMPONENTS:
            if negative_counts[comp] > 0:
                print(f"  {comp}: {negative_counts[comp]} records")
    else:
        print("\n[OK] No negative values")

    # Check 3: Values > 100%
    over_100 = (df[MAIN_COMPONENTS] > 100).sum()
    if over_100.sum() > 0:
        issues.append("Values > 100% detected")
        print("\n[ERROR] Values > 100%:")
        for comp in MAIN_COMPONENTS:
            if over_100[comp] > 0:
                print(f"  {comp}: {over_100[comp]} records")
    else:
        print("\n[OK] No values > 100%")

    # Check 4: Record count
    if len(df) < 30:
        issues.append(f"Only {len(df)} records (target: 30)")
        print(f"\n[WARNING] Warning: Only {len(df)} records available (target: 30)")
    else:
        print(f"\n[OK] Sufficient records: {len(df)}")

    # Summary
    if len(issues) == 0:
        print("\n[OK] All data quality checks passed!")
    else:
        print(f"\n[WARNING] Data quality issues found: {len(issues)}")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")


def generate_summary_report(df):
    """Generate overall summary report."""

    print("\n" + "="*70)
    print("SUMMARY REPORT")
    print("="*70)

    print(f"\nDataset Information:")
    print(f"  Total records: {len(df)}")
    print(f"  Components analyzed: {len(MAIN_COMPONENTS)}")

    print(f"\nComposition Coverage:")
    total_sum = df[MAIN_COMPONENTS].sum(axis=1)
    print(f"  Average total: {total_sum.mean():.2f}%")
    print(f"  This represents the 6 main chemical groups")
    print(f"  Other minor components may make up the remaining percentage")

    print(f"\nDominant Components (by average %):")
    avg_values = df[MAIN_COMPONENTS].mean().sort_values(ascending=False)
    for i, (comp, val) in enumerate(avg_values.items(), 1):
        print(f"  {i}. {comp}: {val:.2f}%")

    print(f"\nVariability (by coefficient of variation):")
    cv_values = ((df[MAIN_COMPONENTS].std() / df[MAIN_COMPONENTS].mean()) * 100).sort_values(ascending=False)
    for i, (comp, cv) in enumerate(cv_values.items(), 1):
        variability = "High" if cv > 100 else "Medium" if cv > 50 else "Low"
        print(f"  {i}. {comp}: {cv:.1f}% CV ({variability} variability)")


def main():
    """Main execution function."""

    print("="*70)
    print("ANALYZE BIO-OIL COMPOSITION STATISTICS")
    print("="*70)
    print(f"Input: {INPUT_FILE}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    try:
        # Load data
        print("\nStep 1: Loading data...")
        df = load_data(INPUT_FILE)

        # Basic statistics
        print("\nStep 2: Calculating basic statistics...")
        calculate_basic_statistics(df)

        # Composition sum analysis
        print("\nStep 3: Analyzing composition sums...")
        analyze_composition_sum(df)

        # Outlier detection
        print("\nStep 4: Detecting outliers...")
        detect_outliers(df)

        # Correlation analysis
        print("\nStep 5: Analyzing correlations...")
        analyze_correlations(df)

        # Data quality checks
        print("\nStep 6: Checking data quality...")
        check_data_quality(df)

        # Summary report
        print("\nStep 7: Generating summary report...")
        generate_summary_report(df)

        # Final message
        print("\n" + "="*70)
        print("ANALYSIS COMPLETE")
        print("="*70)
        print("[OK] Statistical analysis completed successfully")
        print("="*70)

    except Exception as e:
        print(f"\n[ERROR] FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
