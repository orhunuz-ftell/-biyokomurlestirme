"""
==============================================================================
REVERSE ML PROJECT - PHASE 2: DATA PREPARATION
Script 1: Extract Bio-oil Composition Data
==============================================================================
Purpose: Extract 30 complete bio-oil compositions from BIOOIL database
Author: Orhun Uzdiyem
Date: 2025-11-16
==============================================================================

This script:
1. Connects to BIOOIL SQL Server database
2. Queries Biooil table for records with complete 6-component data
3. Extracts up to 30 records with complete composition
4. Saves to CSV: biooil_compositions_30.csv

Requirements:
- pyodbc
- pandas
==============================================================================
"""

import pyodbc
import pandas as pd
import os
from datetime import datetime

# Database connection parameters
SERVER = 'DESKTOP-DRO84HP\\SQLEXPRESS'
DATABASE = 'BIOOIL'
DRIVER = '{SQL Server}'

# Output file path
OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'data',
    'biooil_reference_data'
)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'biooil_compositions_30.csv')

# Target number of bio-oil compositions
TARGET_COUNT = 30


def connect_to_database():
    """Connect to BIOOIL SQL Server database using Windows Authentication."""
    try:
        connection_string = (
            f'DRIVER={DRIVER};'
            f'SERVER={SERVER};'
            f'DATABASE={DATABASE};'
            f'Trusted_Connection=yes'
        )
        conn = pyodbc.connect(connection_string)
        print(f"[OK] Successfully connected to {DATABASE} database")
        return conn
    except Exception as e:
        print(f"[ERROR] Error connecting to database: {e}")
        raise


def extract_biooil_data(conn, limit=TARGET_COUNT):
    """
    Extract bio-oil compositions with complete 6-component data.

    6 main components:
    - aromatics
    - acids
    - alcohols
    - furans
    - phenols
    - aldehyde&ketone
    """

    query = """
    SELECT TOP (?)
        b.BiooilId,
        b.Experiment_Id,
        b.aromatics,
        b.acids,
        b.alcohols,
        b.furans,
        b.phenols,
        b.[aldehyde&ketone] AS aldehyde_ketone,

        -- Additional context (optional columns)
        e.ProcessTemperature AS PyrolysisTemp_C,
        bm.BiomassName,
        bm.HHV AS BiomassHHV,
        r.ReferenceCiting AS Reference

    FROM Biooil b
    LEFT JOIN Experiment e ON b.Experiment_Id = e.ExperimentId
    LEFT JOIN Biomass bm ON e.Biomass_Id = bm.BiomassId
    LEFT JOIN Reference r ON bm.Reference_Id = r.ReferenceId

    WHERE
        -- Only records with complete composition data
        b.aromatics IS NOT NULL
        AND b.acids IS NOT NULL
        AND b.alcohols IS NOT NULL
        AND b.furans IS NOT NULL
        AND b.phenols IS NOT NULL
        AND b.[aldehyde&ketone] IS NOT NULL

        -- Optional: Add quality filters
        -- Composition should sum to approximately 100%
        AND (b.aromatics + b.acids + b.alcohols + b.furans + b.phenols + b.[aldehyde&ketone])
            BETWEEN 60 AND 120  -- Allow some margin for error

    ORDER BY b.BiooilId
    """

    try:
        df = pd.read_sql(query, conn, params=(limit,))
        print(f"[OK] Extracted {len(df)} bio-oil compositions")
        return df
    except Exception as e:
        print(f"[ERROR] Error extracting data: {e}")
        raise


def validate_data(df):
    """Validate extracted bio-oil data."""

    print("\n" + "="*70)
    print("DATA VALIDATION")
    print("="*70)

    # Check record count
    print(f"\nRecords extracted: {len(df)}")
    if len(df) < TARGET_COUNT:
        print(f"[WARNING] Warning: Only {len(df)} records found (target: {TARGET_COUNT})")

    # Check for missing values in main components
    main_components = ['aromatics', 'acids', 'alcohols', 'furans', 'phenols', 'aldehyde_ketone']
    missing_counts = df[main_components].isnull().sum()

    print("\nMissing values in main components:")
    for comp in main_components:
        print(f"  {comp}: {missing_counts[comp]}")

    if missing_counts.sum() > 0:
        print("[ERROR] ERROR: Found missing values in main components!")
        return False
    else:
        print("[OK] No missing values in main components")

    # Calculate composition sum for each record
    df['composition_sum'] = df[main_components].sum(axis=1)

    print(f"\nComposition sum statistics:")
    print(f"  Mean: {df['composition_sum'].mean():.2f}%")
    print(f"  Min:  {df['composition_sum'].min():.2f}%")
    print(f"  Max:  {df['composition_sum'].max():.2f}%")
    print(f"  Std:  {df['composition_sum'].std():.2f}%")

    # Check for unrealistic values
    records_out_of_range = ((df['composition_sum'] < 60) | (df['composition_sum'] > 120)).sum()
    if records_out_of_range > 0:
        print(f"[WARNING] Warning: {records_out_of_range} records have composition sum outside 60-120% range")
    else:
        print("[OK] All composition sums are within acceptable range")

    # Display component statistics
    print("\nComponent statistics (%):")
    print(df[main_components].describe().round(2))

    return True


def save_to_csv(df, filepath):
    """Save dataframe to CSV file."""

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
    print("EXTRACT BIO-OIL COMPOSITION DATA")
    print("="*70)
    print(f"Target: Extract {TARGET_COUNT} complete bio-oil compositions")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    try:
        # Step 1: Connect to database
        print("\nStep 1: Connecting to database...")
        conn = connect_to_database()

        # Step 2: Extract data
        print(f"\nStep 2: Extracting bio-oil data...")
        df = extract_biooil_data(conn, limit=TARGET_COUNT)

        # Step 3: Validate data
        print("\nStep 3: Validating data...")
        if not validate_data(df):
            raise ValueError("Data validation failed!")

        # Step 4: Save to CSV
        print("\nStep 4: Saving to CSV...")
        if not save_to_csv(df, OUTPUT_FILE):
            raise IOError("Failed to save CSV file!")

        # Close database connection
        conn.close()
        print("\n[OK] Database connection closed")

        # Final summary
        print("\n" + "="*70)
        print("EXTRACTION COMPLETE")
        print("="*70)
        print(f"[OK] Successfully extracted {len(df)} bio-oil compositions")
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
