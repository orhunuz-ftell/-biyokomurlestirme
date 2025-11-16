"""
==============================================================================
REVERSE ML PROJECT - PHASE 2: DATA PREPARATION
Script 3: Generate Design of Experiments (DOE) Matrix
==============================================================================
Purpose: Generate DOE matrix for steam reforming process conditions
Author: Orhun Uzdiyem
Date: 2025-11-16
==============================================================================

This script:
1. Defines process parameter ranges for steam reforming
2. Generates full factorial DOE matrix
3. Creates 45 unique combinations (5 × 3 × 3)
4. Saves to CSV: doe_matrix.csv

Process Parameters:
- Reformer Temperature: 650-850°C (5 levels)
- Reformer Pressure: 5-30 bar (3 levels)
- Steam-to-Carbon Ratio: 2-6 (3 levels)

Requirements:
- pandas
- numpy
==============================================================================
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import itertools

# Output file path
OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'data',
    'biooil_reference_data'
)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'doe_matrix.csv')

# Process parameter ranges
# Based on literature and steam reforming best practices
PARAMETERS = {
    'ReformerTemperature_C': {
        'min': 650,
        'max': 850,
        'levels': 5,
        'description': 'Reformer operating temperature (°C)'
    },
    'ReformerPressure_bar': {
        'min': 5,
        'max': 30,
        'levels': 3,
        'description': 'Reformer operating pressure (bar)'
    },
    'SteamToCarbonRatio': {
        'min': 2.0,
        'max': 6.0,
        'levels': 3,
        'description': 'Molar ratio of steam to carbon in feed'
    }
}


def generate_parameter_levels(param_name, param_config):
    """Generate evenly-spaced levels for a parameter."""

    min_val = param_config['min']
    max_val = param_config['max']
    n_levels = param_config['levels']

    levels = np.linspace(min_val, max_val, n_levels)

    print(f"\n{param_name}:")
    print(f"  Range: {min_val} - {max_val}")
    print(f"  Levels: {n_levels}")
    print(f"  Values: {', '.join([f'{v:.2f}' for v in levels])}")

    return levels


def generate_doe_matrix():
    """Generate full factorial DOE matrix."""

    print("\n" + "="*70)
    print("GENERATING DOE MATRIX")
    print("="*70)

    # Generate levels for each parameter
    temp_levels = generate_parameter_levels('ReformerTemperature_C', PARAMETERS['ReformerTemperature_C'])
    pressure_levels = generate_parameter_levels('ReformerPressure_bar', PARAMETERS['ReformerPressure_bar'])
    sc_ratio_levels = generate_parameter_levels('SteamToCarbonRatio', PARAMETERS['SteamToCarbonRatio'])

    # Generate all combinations (full factorial design)
    combinations = list(itertools.product(temp_levels, pressure_levels, sc_ratio_levels))

    print(f"\nTotal combinations: {len(combinations)}")
    print(f"  = {len(temp_levels)} temps × {len(pressure_levels)} pressures × {len(sc_ratio_levels)} S/C ratios")

    # Create dataframe
    df = pd.DataFrame(combinations, columns=[
        'ReformerTemperature_C',
        'ReformerPressure_bar',
        'SteamToCarbonRatio'
    ])

    # Add condition ID
    df.insert(0, 'ConditionId', range(1, len(df) + 1))

    # Add additional process parameters (typical values)
    # These can be adjusted based on specific simulation requirements
    df['HTS_Temperature_C'] = 370.0  # High-temperature shift
    df['LTS_Temperature_C'] = 210.0  # Low-temperature shift
    df['PSA_Pressure_bar'] = 25.0    # Pressure swing adsorption

    # Add feed rates (per 100 kg bio-oil basis)
    df['BiooilFeedRate_kgh'] = 100.0  # kg/h
    # Steam feed rate calculated from S/C ratio (approximate)
    # Assuming bio-oil has ~5 mol C per kg (rough estimate)
    df['SteamFeedRate_kgh'] = df['SteamToCarbonRatio'] * 100 * 0.018 * 5  # kg/h

    return df


def validate_doe_matrix(df):
    """Validate generated DOE matrix."""

    print("\n" + "="*70)
    print("DOE MATRIX VALIDATION")
    print("="*70)

    print(f"\nMatrix dimensions:")
    print(f"  Rows: {len(df)}")
    print(f"  Columns: {len(df.columns)}")

    print(f"\nColumn names:")
    for col in df.columns:
        print(f"  - {col}")

    # Check for missing values
    missing = df.isnull().sum().sum()
    if missing > 0:
        print(f"\n[ERROR] ERROR: {missing} missing values found!")
        return False
    else:
        print("\n[OK] No missing values")

    # Check for duplicate conditions
    duplicates = df.duplicated(subset=['ReformerTemperature_C', 'ReformerPressure_bar', 'SteamToCarbonRatio']).sum()
    if duplicates > 0:
        print(f"\n[ERROR] ERROR: {duplicates} duplicate conditions found!")
        return False
    else:
        print("[OK] No duplicate conditions")

    # Check parameter ranges
    print("\nParameter ranges:")
    for param in ['ReformerTemperature_C', 'ReformerPressure_bar', 'SteamToCarbonRatio']:
        min_val = df[param].min()
        max_val = df[param].max()
        expected_min = PARAMETERS[param]['min']
        expected_max = PARAMETERS[param]['max']

        print(f"  {param}:")
        print(f"    Expected: {expected_min} - {expected_max}")
        print(f"    Actual:   {min_val} - {max_val}")

        if abs(min_val - expected_min) > 0.01 or abs(max_val - expected_max) > 0.01:
            print(f"    [ERROR] ERROR: Range mismatch!")
            return False

    print("\n[OK] All parameter ranges correct")

    return True


def display_sample_conditions(df, n=10):
    """Display sample conditions from DOE matrix."""

    print("\n" + "="*70)
    print(f"SAMPLE CONDITIONS (first {n})")
    print("="*70)

    sample_df = df.head(n)[['ConditionId', 'ReformerTemperature_C',
                             'ReformerPressure_bar', 'SteamToCarbonRatio']]

    print("\n" + sample_df.to_string(index=False))


def save_to_csv(df, filepath):
    """Save DOE matrix to CSV file."""

    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Save to CSV
        df.to_csv(filepath, index=False, float_format='%.4f')
        print(f"\n[OK] Data saved to: {filepath}")
        print(f"  File size: {os.path.getsize(filepath)} bytes")

        return True
    except Exception as e:
        print(f"\n[ERROR] Error saving file: {e}")
        return False


def main():
    """Main execution function."""

    print("="*70)
    print("GENERATE DOE MATRIX")
    print("="*70)
    print(f"Output: {OUTPUT_FILE}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    print("\nProcess Parameters:")
    for param_name, param_config in PARAMETERS.items():
        print(f"\n{param_name}:")
        print(f"  Range: {param_config['min']} - {param_config['max']}")
        print(f"  Levels: {param_config['levels']}")
        print(f"  Description: {param_config['description']}")

    try:
        # Step 1: Generate DOE matrix
        print("\nStep 1: Generating DOE matrix...")
        df = generate_doe_matrix()

        # Step 2: Validate matrix
        print("\nStep 2: Validating DOE matrix...")
        if not validate_doe_matrix(df):
            raise ValueError("DOE matrix validation failed!")

        # Step 3: Display samples
        print("\nStep 3: Displaying sample conditions...")
        display_sample_conditions(df, n=10)

        # Step 4: Save to CSV
        print("\nStep 4: Saving to CSV...")
        if not save_to_csv(df, OUTPUT_FILE):
            raise IOError("Failed to save CSV file!")

        # Final summary
        print("\n" + "="*70)
        print("DOE MATRIX GENERATION COMPLETE")
        print("="*70)
        print(f"[OK] Generated {len(df)} process conditions")
        print(f"[OK] Full factorial design: {PARAMETERS['ReformerTemperature_C']['levels']} × "
              f"{PARAMETERS['ReformerPressure_bar']['levels']} × "
              f"{PARAMETERS['SteamToCarbonRatio']['levels']}")
        print(f"[OK] Data saved to: {OUTPUT_FILE}")
        print("="*70)

    except Exception as e:
        print(f"\n[ERROR] FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
