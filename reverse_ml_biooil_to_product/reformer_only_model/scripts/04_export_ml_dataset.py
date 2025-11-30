"""
Export ML Dataset
=================

Export complete reformer dataset to CSV format for machine learning.

Joins:
- Biooil (input: bio-oil composition)
- ReformerSimulation (input: process conditions)
- ReformerOutput (output: syngas composition)
- ReformerPerformance (output: performance metrics)

Author: Orhun Uzdiyem
Date: November 30, 2025
"""

import sys
import os
import pyodbc
import pandas as pd
from datetime import datetime

# Add config to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
import reformer_config as config

print("=" * 80)
print("EXPORTING ML DATASET")
print("=" * 80)
print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Create output directory
output_dir = config.create_output_dir()
print(f"Output directory: {output_dir}")
print()

# Connect to database
conn = pyodbc.connect(config.DB_CONNECTION_STRING)

# ============================================================================
# QUERY: COMPLETE DATASET
# ============================================================================

print("Querying complete dataset...")
query = """
    SELECT
        -- Simulation identifier
        s.SimulationID,
        s.BiooilID,

        -- INPUT FEATURES: Bio-oil composition (6 features)
        b.aromatics AS Biooil_Aromatics_pct,
        b.acids AS Biooil_Acids_pct,
        b.alcohols AS Biooil_Alcohols_pct,
        b.furans AS Biooil_Furans_pct,
        b.phenols AS Biooil_Phenols_pct,
        b.[aldehyde&ketone] AS Biooil_Aldehydes_Ketones_pct,

        -- INPUT FEATURES: Process conditions (3 features)
        s.Temperature_C AS Reformer_Temperature_C,
        s.Pressure_bar AS Reformer_Pressure_bar,
        s.SC_Ratio AS Steam_to_Carbon_Ratio,

        -- OUTPUT FEATURES: Reformer composition (mol%)
        o.H2_molpercent AS H2_molpercent,
        o.CO_molpercent AS CO_molpercent,
        o.CO2_molpercent AS CO2_molpercent,
        o.CH4_molpercent AS CH4_molpercent,
        o.H2O_molpercent AS H2O_molpercent,
        o.C2H4_molpercent AS C2H4_molpercent,
        o.C2H6_molpercent AS C2H6_molpercent,

        -- OUTPUT FEATURES: Thermodynamic properties
        o.Temperature_K AS Reformer_Outlet_Temperature_K,
        o.Enthalpy_J_mol AS Reformer_Enthalpy_J_mol,
        o.Entropy_J_molK AS Reformer_Entropy_J_molK,
        o.Density_kg_m3 AS Reformer_Density_kg_m3,
        o.MeanMolecularWeight_g_mol AS Reformer_MeanMW_g_mol,

        -- OUTPUT FEATURES: Performance metrics
        p.H2_CO_Ratio,
        p.H2_CO2_Ratio,
        p.CO_CO2_Ratio,
        p.H2_DryBasis_molpercent,
        p.CO_DryBasis_molpercent,
        p.CO2_DryBasis_molpercent,
        p.CH4_DryBasis_molpercent,
        p.Carbon_in_CO_percent,
        p.Carbon_in_CO2_percent,
        p.Carbon_in_CH4_percent,
        p.Hydrogen_in_H2_percent,
        p.Hydrogen_in_CH4_percent,
        p.Hydrogen_in_H2O_percent,
        p.Equilibrium_Constant_WGS,
        p.H2_Selectivity,
        p.CO_Selectivity,
        p.DataQualityFlag

    FROM ReformerSimulation s
    INNER JOIN Biooil b ON s.BiooilID = b.BiooilId
    INNER JOIN ReformerOutput o ON s.SimulationID = o.SimulationID
    INNER JOIN ReformerPerformance p ON s.SimulationID = p.SimulationID

    WHERE s.ConvergenceStatus = 'Converged'

    ORDER BY s.SimulationID
"""

df = pd.read_sql(query, conn)
print(f"  [OK] Loaded {len(df)} records with {len(df.columns)} columns")
print()

# ============================================================================
# DATA QUALITY CHECKS
# ============================================================================

print("Data quality checks...")

# Check for missing values
missing = df.isnull().sum()
if missing.sum() > 0:
    print("  [WARNING] Missing values detected:")
    print(missing[missing > 0])
else:
    print("  [OK] No missing values")

# Check for invalid values
if (df['H2_molpercent'] < 0).any():
    print("  [WARNING] Negative H2 values detected")
elif (df['H2_molpercent'] > 100).any():
    print("  [WARNING] H2 > 100% detected")
else:
    print("  [OK] H2 values in valid range")

print()

# ============================================================================
# EXPORT TO CSV
# ============================================================================

print("Exporting to CSV...")

# Full dataset
csv_path = os.path.join(output_dir, 'reformer_ml_dataset.csv')
df.to_csv(csv_path, index=False, sep=config.CSV_SEPARATOR,
          decimal=config.CSV_DECIMAL, encoding=config.CSV_ENCODING)
print(f"  [OK] Full dataset: {csv_path}")
print(f"       Records: {len(df)}, Columns: {len(df.columns)}")

# Input features only
input_cols = [
    'SimulationID', 'BiooilID',
    'Biooil_Aromatics_pct', 'Biooil_Acids_pct', 'Biooil_Alcohols_pct',
    'Biooil_Furans_pct', 'Biooil_Phenols_pct', 'Biooil_Aldehydes_Ketones_pct',
    'Reformer_Temperature_C', 'Reformer_Pressure_bar', 'Steam_to_Carbon_Ratio'
]
df_inputs = df[input_cols]
inputs_path = os.path.join(output_dir, 'reformer_inputs.csv')
df_inputs.to_csv(inputs_path, index=False, sep=config.CSV_SEPARATOR,
                 decimal=config.CSV_DECIMAL, encoding=config.CSV_ENCODING)
print(f"  [OK] Input features: {inputs_path}")

# Output features only (for ML targets)
output_cols = [
    'SimulationID',
    'H2_molpercent', 'CO_molpercent', 'CO2_molpercent', 'CH4_molpercent', 'H2O_molpercent',
    'H2_CO_Ratio', 'H2_DryBasis_molpercent',
    'Carbon_in_CO_percent', 'Carbon_in_CO2_percent',
    'Hydrogen_in_H2_percent', 'H2_Selectivity'
]
df_outputs = df[output_cols]
outputs_path = os.path.join(output_dir, 'reformer_outputs.csv')
df_outputs.to_csv(outputs_path, index=False, sep=config.CSV_SEPARATOR,
                  decimal=config.CSV_DECIMAL, encoding=config.CSV_ENCODING)
print(f"  [OK] Output features: {outputs_path}")

print()

# ============================================================================
# DATA DICTIONARY
# ============================================================================

print("Creating data dictionary...")

dict_path = os.path.join(output_dir, 'data_dictionary.txt')
with open(dict_path, 'w') as f:
    f.write("=" * 80 + "\n")
    f.write("REFORMER-ONLY MODEL - DATA DICTIONARY\n")
    f.write("=" * 80 + "\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Total records: {len(df)}\n")
    f.write(f"Total features: {len(df.columns)}\n")
    f.write("\n")

    f.write("INPUT FEATURES (9 total)\n")
    f.write("-" * 80 + "\n")
    f.write("Bio-oil Composition (wt%):\n")
    f.write("  Biooil_Aromatics_pct       - Aromatic compounds (toluene surrogate)\n")
    f.write("  Biooil_Acids_pct           - Organic acids (acetic acid surrogate)\n")
    f.write("  Biooil_Alcohols_pct        - Alcohols (ethanol surrogate)\n")
    f.write("  Biooil_Furans_pct          - Furan compounds\n")
    f.write("  Biooil_Phenols_pct         - Phenolic compounds\n")
    f.write("  Biooil_Aldehydes_Ketones_pct - Aldehydes and ketones (acetone surrogate)\n")
    f.write("\n")
    f.write("Process Conditions:\n")
    f.write("  Reformer_Temperature_C     - Steam reforming temperature (650-850°C)\n")
    f.write("  Reformer_Pressure_bar      - Operating pressure (5-30 bar)\n")
    f.write("  Steam_to_Carbon_Ratio      - Molar ratio of steam to carbon (2-6)\n")
    f.write("\n")

    f.write("OUTPUT FEATURES (Primary)\n")
    f.write("-" * 80 + "\n")
    f.write("Syngas Composition (mol%):\n")
    f.write("  H2_molpercent              - Hydrogen (target product)\n")
    f.write("  CO_molpercent              - Carbon monoxide\n")
    f.write("  CO2_molpercent             - Carbon dioxide\n")
    f.write("  CH4_molpercent             - Methane\n")
    f.write("  H2O_molpercent             - Water (unreacted steam)\n")
    f.write("  C2H4_molpercent            - Ethylene\n")
    f.write("  C2H6_molpercent            - Ethane\n")
    f.write("\n")

    f.write("Performance Metrics:\n")
    f.write("  H2_CO_Ratio                - H2/CO molar ratio (important for syngas applications)\n")
    f.write("  H2_CO2_Ratio               - H2/CO2 molar ratio\n")
    f.write("  CO_CO2_Ratio               - CO/CO2 ratio (WGS equilibrium indicator)\n")
    f.write("  H2_DryBasis_molpercent     - H2 content excluding water\n")
    f.write("  H2_Selectivity             - Fraction of H atoms converted to H2\n")
    f.write("  Carbon_in_CO_percent       - Carbon distribution to CO\n")
    f.write("  Carbon_in_CO2_percent      - Carbon distribution to CO2\n")
    f.write("  Hydrogen_in_H2_percent     - Hydrogen distribution to H2\n")
    f.write("\n")

    f.write("Thermodynamic Properties:\n")
    f.write("  Reformer_Enthalpy_J_mol    - Molar enthalpy (J/mol)\n")
    f.write("  Reformer_Entropy_J_molK    - Molar entropy (J/mol·K)\n")
    f.write("  Reformer_Density_kg_m3     - Gas density (kg/m³)\n")
    f.write("  Equilibrium_Constant_WGS   - WGS reaction equilibrium constant\n")
    f.write("\n")

    f.write("DATA QUALITY\n")
    f.write("-" * 80 + "\n")
    f.write("  DataQualityFlag            - 'Valid', 'Warning', or 'Invalid'\n")
    f.write("\n")

    f.write("DATASET STATISTICS\n")
    f.write("-" * 80 + "\n")
    f.write(f"  Bio-oil compositions: {df['BiooilID'].nunique()}\n")
    f.write(f"  Temperature levels: {df['Reformer_Temperature_C'].nunique()}\n")
    f.write(f"  Pressure levels: {df['Reformer_Pressure_bar'].nunique()}\n")
    f.write(f"  S/C ratio levels: {df['Steam_to_Carbon_Ratio'].nunique()}\n")
    f.write(f"  Total simulations: {len(df)}\n")
    f.write("\n")

    f.write("=" * 80 + "\n")

print(f"  [OK] Data dictionary: {dict_path}")
print()

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

print("Summary statistics:")
print()

print("INPUT FEATURES:")
print(df[['Biooil_Aromatics_pct', 'Biooil_Acids_pct', 'Biooil_Alcohols_pct',
          'Reformer_Temperature_C', 'Reformer_Pressure_bar', 'Steam_to_Carbon_Ratio']].describe())
print()

print("OUTPUT FEATURES:")
print(df[['H2_molpercent', 'CO_molpercent', 'CO2_molpercent', 'CH4_molpercent',
          'H2_CO_Ratio', 'H2_DryBasis_molpercent']].describe())
print()

conn.close()

print("=" * 80)
print("EXPORT COMPLETE")
print("=" * 80)
print()
print("Files created:")
print(f"  1. {csv_path}")
print(f"  2. {inputs_path}")
print(f"  3. {outputs_path}")
print(f"  4. {dict_path}")
print()
print("[SUCCESS] Dataset ready for machine learning!")
print("=" * 80)
