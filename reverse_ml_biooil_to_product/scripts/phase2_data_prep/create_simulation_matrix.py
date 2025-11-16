"""
==============================================================================
REVERSE ML PROJECT - PHASE 2: DATA PREPARATION
Script 4: Create Full Simulation Matrix
==============================================================================
Purpose: Combine bio-oil compositions with DOE conditions to create full
         simulation matrix for Aspen automation
Author: Orhun Uzdiyem
Date: 2025-11-16
==============================================================================

This script:
1. Reads biooil_compositions_30.csv (30 bio-oils)
2. Reads doe_matrix.csv (45 process conditions)
3. Creates full cross-product matrix (30 × 45 = 1,350 simulations)
4. Assigns unique SimulationId to each combination
5. Saves to CSV: aspen_input_matrix.csv

This matrix will be used for:
- Aspen automation (Phase 3) - when Aspen is available
- Tracking simulation progress
- Storing results in database

Requirements:
- pandas
==============================================================================
"""

import pandas as pd
import os
from datetime import datetime

# Input file paths
INPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'data',
    'biooil_reference_data'
)
BIOOIL_FILE = os.path.join(INPUT_DIR, 'biooil_compositions_30.csv')
DOE_FILE = os.path.join(INPUT_DIR, 'doe_matrix.csv')

# Output file path
OUTPUT_FILE = os.path.join(INPUT_DIR, 'aspen_input_matrix.csv')


def load_input_files():
    """Load bio-oil compositions and DOE matrix."""

    print("\n" + "="*70)
    print("LOADING INPUT FILES")
    print("="*70)

    try:
        # Load bio-oil data
        print(f"\nLoading bio-oil compositions...")
        biooil_df = pd.read_csv(BIOOIL_FILE)
        print(f"  [OK] Loaded {len(biooil_df)} bio-oil compositions")
        print(f"    Columns: {len(biooil_df.columns)}")

        # Load DOE matrix
        print(f"\nLoading DOE matrix...")
        doe_df = pd.read_csv(DOE_FILE)
        print(f"  [OK] Loaded {len(doe_df)} process conditions")
        print(f"    Columns: {len(doe_df.columns)}")

        return biooil_df, doe_df

    except FileNotFoundError as e:
        print(f"\n[ERROR] ERROR: File not found: {e}")
        print("  Please run previous scripts first:")
        print("    1. extract_biooil_data.py")
        print("    2. generate_doe_matrix.py")
        raise
    except Exception as e:
        print(f"\n[ERROR] ERROR: {e}")
        raise


def create_simulation_matrix(biooil_df, doe_df):
    """Create full simulation matrix by cross-product."""

    print("\n" + "="*70)
    print("CREATING SIMULATION MATRIX")
    print("="*70)

    # Create cross product using merge with dummy key
    biooil_df['_merge_key'] = 1
    doe_df['_merge_key'] = 1

    # Merge to create all combinations
    sim_matrix = pd.merge(biooil_df, doe_df, on='_merge_key', suffixes=('', '_doe'))

    # Remove merge key
    sim_matrix = sim_matrix.drop('_merge_key', axis=1)

    # Add unique SimulationId
    sim_matrix.insert(0, 'SimulationId', range(1, len(sim_matrix) + 1))

    print(f"\nMatrix created:")
    print(f"  Bio-oil compositions: {len(biooil_df)}")
    print(f"  Process conditions: {len(doe_df)}")
    print(f"  Total simulations: {len(sim_matrix)}")
    print(f"    = {len(biooil_df)} bio-oils × {len(doe_df)} conditions")

    return sim_matrix


def organize_columns(df):
    """Organize columns in logical order."""

    print("\n" + "="*70)
    print("ORGANIZING COLUMNS")
    print("="*70)

    # Define column order
    id_cols = ['SimulationId', 'BiooilId', 'Experiment_Id', 'ConditionId']

    # Bio-oil composition columns
    composition_cols = ['aromatics', 'acids', 'alcohols', 'furans', 'phenols', 'aldehyde_ketone']

    # Process condition columns
    process_cols = [
        'ReformerTemperature_C',
        'ReformerPressure_bar',
        'SteamToCarbonRatio',
        'HTS_Temperature_C',
        'LTS_Temperature_C',
        'PSA_Pressure_bar',
        'BiooilFeedRate_kgh',
        'SteamFeedRate_kgh'
    ]

    # Reference information columns
    ref_cols = ['PyrolysisTemp_C', 'BiomassName', 'BiomassHHV', 'Reference']

    # Build ordered column list
    ordered_cols = id_cols.copy()

    # Add composition columns if they exist
    for col in composition_cols:
        if col in df.columns:
            ordered_cols.append(col)

    # Add process columns if they exist
    for col in process_cols:
        if col in df.columns:
            ordered_cols.append(col)

    # Add reference columns if they exist
    for col in ref_cols:
        if col in df.columns:
            ordered_cols.append(col)

    # Add any remaining columns not in the lists
    remaining_cols = [col for col in df.columns if col not in ordered_cols]
    ordered_cols.extend(remaining_cols)

    # Reorder dataframe
    df = df[ordered_cols]

    print(f"\nColumn organization:")
    print(f"  ID columns: {len(id_cols)}")
    print(f"  Composition columns: {len([c for c in composition_cols if c in df.columns])}")
    print(f"  Process columns: {len([c for c in process_cols if c in df.columns])}")
    print(f"  Reference columns: {len([c for c in ref_cols if c in df.columns])}")
    print(f"  Other columns: {len(remaining_cols)}")
    print(f"  Total: {len(df.columns)}")

    return df


def validate_simulation_matrix(df):
    """Validate created simulation matrix."""

    print("\n" + "="*70)
    print("VALIDATION")
    print("="*70)

    issues = []

    # Check 1: Expected number of simulations
    expected_count = 1350  # 30 bio-oils × 45 conditions
    if len(df) != expected_count:
        issues.append(f"Expected {expected_count} simulations, got {len(df)}")
        print(f"\n[WARNING] Warning: Expected {expected_count} simulations, got {len(df)}")
    else:
        print(f"\n[OK] Correct number of simulations: {len(df)}")

    # Check 2: Unique SimulationIds
    unique_ids = df['SimulationId'].nunique()
    if unique_ids != len(df):
        issues.append(f"Duplicate SimulationIds found")
        print(f"\n[ERROR] ERROR: {len(df) - unique_ids} duplicate SimulationIds!")
    else:
        print(f"[OK] All SimulationIds are unique")

    # Check 3: Missing values
    missing = df.isnull().sum()
    critical_cols = ['SimulationId', 'BiooilId', 'ReformerTemperature_C',
                     'ReformerPressure_bar', 'SteamToCarbonRatio',
                     'aromatics', 'acids', 'alcohols', 'furans', 'phenols', 'aldehyde_ketone']

    missing_critical = False
    for col in critical_cols:
        if col in df.columns and missing[col] > 0:
            missing_critical = True
            issues.append(f"Missing values in critical column: {col}")
            print(f"\n[ERROR] ERROR: {missing[col]} missing values in {col}")

    if not missing_critical:
        print("[OK] No missing values in critical columns")

    # Check 4: Each bio-oil appears 45 times
    biooil_counts = df['BiooilId'].value_counts()
    if not all(biooil_counts == 45):
        issues.append("Not all bio-oils appear exactly 45 times")
        print(f"\n[WARNING] Warning: Bio-oils do not all appear 45 times")
        print(f"  Min: {biooil_counts.min()}, Max: {biooil_counts.max()}")
    else:
        print("[OK] Each bio-oil appears exactly 45 times")

    # Summary
    if len(issues) == 0:
        print("\n[OK] All validation checks passed!")
        return True
    else:
        print(f"\n[WARNING] Validation issues found: {len(issues)}")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        return False


def display_sample_simulations(df, n=10):
    """Display sample simulations from matrix."""

    print("\n" + "="*70)
    print(f"SAMPLE SIMULATIONS (first {n})")
    print("="*70)

    # Select key columns for display
    display_cols = [
        'SimulationId',
        'BiooilId',
        'ReformerTemperature_C',
        'ReformerPressure_bar',
        'SteamToCarbonRatio',
        'aromatics',
        'acids',
        'phenols'
    ]

    sample_df = df.head(n)[display_cols]
    print("\n" + sample_df.to_string(index=False))

    print(f"\n(Showing {len(display_cols)} of {len(df.columns)} columns)")


def save_to_csv(df, filepath):
    """Save simulation matrix to CSV file."""

    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Save to CSV
        df.to_csv(filepath, index=False, float_format='%.4f')
        print(f"\n[OK] Data saved to: {filepath}")
        print(f"  File size: {os.path.getsize(filepath):,} bytes")
        print(f"  Rows: {len(df):,}")
        print(f"  Columns: {len(df.columns)}")

        return True
    except Exception as e:
        print(f"\n[ERROR] Error saving file: {e}")
        return False


def main():
    """Main execution function."""

    print("="*70)
    print("CREATE FULL SIMULATION MATRIX")
    print("="*70)
    print(f"Output: {OUTPUT_FILE}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    try:
        # Step 1: Load input files
        print("\nStep 1: Loading input files...")
        biooil_df, doe_df = load_input_files()

        # Step 2: Create simulation matrix
        print("\nStep 2: Creating simulation matrix...")
        sim_matrix = create_simulation_matrix(biooil_df, doe_df)

        # Step 3: Organize columns
        print("\nStep 3: Organizing columns...")
        sim_matrix = organize_columns(sim_matrix)

        # Step 4: Validate matrix
        print("\nStep 4: Validating simulation matrix...")
        validate_simulation_matrix(sim_matrix)

        # Step 5: Display samples
        print("\nStep 5: Displaying sample simulations...")
        display_sample_simulations(sim_matrix, n=10)

        # Step 6: Save to CSV
        print("\nStep 6: Saving to CSV...")
        if not save_to_csv(sim_matrix, OUTPUT_FILE):
            raise IOError("Failed to save CSV file!")

        # Final summary
        print("\n" + "="*70)
        print("SIMULATION MATRIX CREATION COMPLETE")
        print("="*70)
        print(f"[OK] Created {len(sim_matrix):,} simulation scenarios")
        print(f"  = {biooil_df['BiooilId'].nunique()} bio-oils × {len(doe_df)} process conditions")
        print(f"[OK] Data saved to: {OUTPUT_FILE}")
        print("\nThis matrix is ready for:")
        print("  - Aspen simulation automation (when Aspen is available)")
        print("  - Database import and tracking")
        print("  - ML model training (after simulations complete)")
        print("="*70)

    except Exception as e:
        print(f"\n[ERROR] FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
