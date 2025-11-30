"""
Data Loader for Reverse ML Prediction
Loads reformer simulation data from database or CSV
"""

import pandas as pd
import numpy as np
import pyodbc
from pathlib import Path

class ReformerDataLoader:
    """Load and preprocess reformer simulation data"""

    def __init__(self, connection_string=None):
        """
        Initialize data loader

        Args:
            connection_string: SQL Server connection string (if loading from DB)
        """
        self.connection_string = connection_string or (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-DRO84HP\\SQLEXPRESS;'
            'DATABASE=BIOOIL;'
            'Trusted_Connection=yes'
        )

        # Define feature columns
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

    def load_from_csv(self, csv_path):
        """
        Load data from CSV file

        Args:
            csv_path: Path to reformer_ml_dataset.csv

        Returns:
            DataFrame with all features
        """
        print(f"Loading data from CSV: {csv_path}")
        df = pd.read_csv(csv_path)

        # Rename columns to match our naming convention
        column_mapping = {
            'Temperature_C': 'Reformer_Temperature_C',
            'Pressure_bar': 'Reformer_Pressure_bar',
            'SC_Ratio': 'Steam_to_Carbon_Ratio',
            'aromatics': 'Biooil_Aromatics_pct',
            'acids': 'Biooil_Acids_pct',
            'alcohols': 'Biooil_Alcohols_pct',
            'furans': 'Biooil_Furans_pct',
            'phenols': 'Biooil_Phenols_pct',
            'aldehyde&ketone': 'Biooil_Aldehydes_Ketones_pct'
        }

        df = df.rename(columns=column_mapping)

        print(f"Loaded {len(df)} records")
        print(f"Columns: {list(df.columns)}")

        return df

    def load_from_database(self):
        """
        Load data directly from SQL Server database

        Returns:
            DataFrame with all features
        """
        print("Connecting to database...")
        conn = pyodbc.connect(self.connection_string)

        query = """
        SELECT
            -- Identifiers
            s.SimulationID,
            s.BiooilID,

            -- Process conditions (inputs)
            s.Temperature_C AS Reformer_Temperature_C,
            s.Pressure_bar AS Reformer_Pressure_bar,
            s.SC_Ratio AS Steam_to_Carbon_Ratio,

            -- Syngas composition (inputs)
            o.H2_molpercent,
            o.CO_molpercent,
            o.CO2_molpercent,
            o.CH4_molpercent,
            o.H2O_molpercent,
            o.C2H4_molpercent,
            o.C2H6_molpercent,

            -- Bio-oil composition (targets)
            b.aromatics AS Biooil_Aromatics_pct,
            b.acids AS Biooil_Acids_pct,
            b.alcohols AS Biooil_Alcohols_pct,
            b.furans AS Biooil_Furans_pct,
            b.phenols AS Biooil_Phenols_pct,
            b.[aldehyde&ketone] AS Biooil_Aldehydes_Ketones_pct,

            -- Additional performance metrics
            p.H2_CO_Ratio,
            p.H2_DryBasis_molpercent

        FROM ReformerSimulation s
        INNER JOIN ReformerOutput o ON s.SimulationID = o.SimulationID
        INNER JOIN Biooil b ON s.BiooilID = b.BiooilId
        LEFT JOIN ReformerPerformance p ON s.SimulationID = p.SimulationID

        WHERE s.ConvergenceStatus = 'Converged'
        ORDER BY s.SimulationID
        """

        print("Executing query...")
        df = pd.read_sql(query, conn)
        conn.close()

        print(f"Loaded {len(df)} records from database")
        return df

    def clean_data(self, df):
        """
        Clean and validate data

        Args:
            df: Raw DataFrame

        Returns:
            Cleaned DataFrame with statistics
        """
        print("\n" + "="*80)
        print("DATA CLEANING")
        print("="*80)

        initial_rows = len(df)
        print(f"Initial rows: {initial_rows}")

        # Check for required columns
        all_features = self.input_features + self.target_features
        missing_cols = [col for col in all_features if col not in df.columns]
        if missing_cols:
            print(f"WARNING: Missing columns: {missing_cols}")

        # Handle missing values
        print("\nMissing values per column:")
        missing_counts = df[all_features].isnull().sum()
        for col, count in missing_counts.items():
            if count > 0:
                pct = count / len(df) * 100
                print(f"  {col:35s}: {count:4d} ({pct:5.1f}%)")

        # Drop rows with missing values in critical columns
        df_clean = df.dropna(subset=all_features)

        dropped_rows = initial_rows - len(df_clean)
        if dropped_rows > 0:
            print(f"\nDropped {dropped_rows} rows with missing values ({dropped_rows/initial_rows*100:.1f}%)")

        # Validate bio-oil composition sums
        biooil_sum = df_clean[self.target_features].sum(axis=1)
        print(f"\nBio-oil composition sum:")
        print(f"  Min:  {biooil_sum.min():.2f}%")
        print(f"  Max:  {biooil_sum.max():.2f}%")
        print(f"  Mean: {biooil_sum.mean():.2f}%")
        print(f"  Std:  {biooil_sum.std():.2f}%")

        # Normalize if needed (some bio-oils may not sum to exactly 100%)
        if abs(biooil_sum.mean() - 100) > 1.0:
            print("\nNormalizing bio-oil composition to sum to 100%...")
            df_clean[self.target_features] = df_clean[self.target_features].div(
                biooil_sum, axis=0
            ) * 100

            # Verify
            new_sum = df_clean[self.target_features].sum(axis=1)
            print(f"  After normalization - Mean sum: {new_sum.mean():.2f}%")

        # Check for outliers in process conditions
        print("\nProcess conditions ranges:")
        for col in ['Reformer_Temperature_C', 'Reformer_Pressure_bar', 'Steam_to_Carbon_Ratio']:
            print(f"  {col:30s}: {df_clean[col].min():.1f} - {df_clean[col].max():.1f}")

        # Check for outliers in syngas composition
        print("\nSyngas composition ranges (mol%):")
        for col in ['H2_molpercent', 'CO_molpercent', 'CO2_molpercent', 'CH4_molpercent']:
            print(f"  {col:20s}: {df_clean[col].min():.2f} - {df_clean[col].max():.2f}")

        print(f"\nFinal rows: {len(df_clean)}")
        print("="*80)

        return df_clean

    def get_summary_statistics(self, df):
        """
        Generate summary statistics

        Args:
            df: Cleaned DataFrame

        Returns:
            Dictionary with statistics
        """
        stats = {
            'total_samples': len(df),
            'unique_biooils': df['BiooilID'].nunique() if 'BiooilID' in df.columns else None,
            'temperature_levels': df['Reformer_Temperature_C'].nunique(),
            'pressure_levels': df['Reformer_Pressure_bar'].nunique(),
            'sc_ratio_levels': df['Steam_to_Carbon_Ratio'].nunique(),
        }

        # Input feature statistics
        stats['input_stats'] = df[self.input_features].describe().to_dict()

        # Target feature statistics
        stats['target_stats'] = df[self.target_features].describe().to_dict()

        return stats

    def save_processed_data(self, df, output_path):
        """
        Save processed data to CSV

        Args:
            df: Processed DataFrame
            output_path: Path to save CSV
        """
        df.to_csv(output_path, index=False)
        print(f"\nSaved processed data to: {output_path}")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {len(df.columns)}")


def main():
    """Test data loading"""

    # Initialize loader
    loader = ReformerDataLoader()

    # Try loading from CSV first
    csv_path = Path(__file__).parent.parent.parent / 'reformer_only_model' / 'output' / 'reformer_ml_dataset.csv'

    if csv_path.exists():
        print(f"Loading from CSV: {csv_path}")
        df = loader.load_from_csv(csv_path)
    else:
        print("CSV not found, loading from database...")
        df = loader.load_from_database()

    # Clean data
    df_clean = loader.clean_data(df)

    # Get statistics
    stats = loader.get_summary_statistics(df_clean)
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    print(f"Total samples: {stats['total_samples']}")
    print(f"Unique bio-oils: {stats['unique_biooils']}")
    print(f"Temperature levels: {stats['temperature_levels']}")
    print(f"Pressure levels: {stats['pressure_levels']}")
    print(f"S/C ratio levels: {stats['sc_ratio_levels']}")

    # Save processed data
    output_path = Path(__file__).parent.parent / 'data' / 'processed' / 'reformer_data_clean.csv'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    loader.save_processed_data(df_clean, output_path)

    print("\nData loading complete!")


if __name__ == '__main__':
    main()
