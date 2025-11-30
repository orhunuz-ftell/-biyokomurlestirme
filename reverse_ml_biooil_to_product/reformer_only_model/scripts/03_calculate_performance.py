"""
Calculate Reformer Performance Metrics
=======================================

Calculate derived performance metrics from reformer equilibrium compositions:
- H2/CO/CO2 ratios
- Dry basis compositions
- Carbon and hydrogen distributions
- Equilibrium constants

Author: Orhun Uzdiyem
Date: November 30, 2025
"""

import sys
import os
import pyodbc
import pandas as pd
import numpy as np
from datetime import datetime

# Add config to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
import reformer_config as config

print("=" * 80)
print("CALCULATING REFORMER PERFORMANCE METRICS")
print("=" * 80)
print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Connect to database
conn = pyodbc.connect(config.DB_CONNECTION_STRING)
cursor = conn.cursor()

# Load all simulations with their compositions
print("Loading simulation data...")
query = """
    SELECT
        s.SimulationID,
        s.BiooilID,
        s.Temperature_C,
        s.SC_Ratio,
        o.H2_molpercent,
        o.CO_molpercent,
        o.CO2_molpercent,
        o.CH4_molpercent,
        o.H2O_molpercent,
        o.C2H4_molpercent,
        o.C2H6_molpercent,
        b.aromatics,
        b.acids,
        b.alcohols,
        b.furans,
        b.phenols,
        b.[aldehyde&ketone]
    FROM ReformerSimulation s
    INNER JOIN ReformerOutput o ON s.SimulationID = o.SimulationID
    INNER JOIN Biooil b ON s.BiooilID = b.BiooilId
    ORDER BY s.SimulationID
"""

data = pd.read_sql(query, conn)
print(f"  [OK] Loaded {len(data)} simulation results")
print()

successful = 0
failed = 0

print("Calculating performance metrics...")
for idx, row in data.iterrows():
    try:
        sim_id = row['SimulationID']

        # Extract compositions
        h2 = row['H2_molpercent']
        co = row['CO_molpercent']
        co2 = row['CO2_molpercent']
        ch4 = row['CH4_molpercent']
        h2o = row['H2O_molpercent']
        c2h4 = row['C2H4_molpercent']
        c2h6 = row['C2H6_molpercent']

        # Calculate key ratios
        h2_co_ratio = h2 / max(co, config.MIN_FOR_RATIO)
        h2_co2_ratio = h2 / max(co2, config.MIN_FOR_RATIO)
        co_co2_ratio = co / max(co2, config.MIN_FOR_RATIO)

        # Dry basis composition (exclude H2O)
        dry_total = h2 + co + co2 + ch4 + c2h4 + c2h6
        if dry_total > 0:
            h2_dry = (h2 / dry_total) * 100
            co_dry = (co / dry_total) * 100
            co2_dry = (co2 / dry_total) * 100
            ch4_dry = (ch4 / dry_total) * 100
        else:
            h2_dry = co_dry = co2_dry = ch4_dry = 0

        # Carbon distribution
        carbon_in_co = co
        carbon_in_co2 = co2
        carbon_in_ch4 = ch4
        carbon_in_c2 = c2h4 * 2 + c2h6 * 2  # 2 carbons per C2 molecule
        carbon_total = carbon_in_co + carbon_in_co2 + carbon_in_ch4 + carbon_in_c2

        # Hydrogen distribution (relative to total H atoms)
        hydrogen_in_h2 = h2 * 2
        hydrogen_in_ch4 = ch4 * 4
        hydrogen_in_h2o = h2o * 2
        hydrogen_in_c2 = c2h4 * 4 + c2h6 * 6
        hydrogen_total = hydrogen_in_h2 + hydrogen_in_ch4 + hydrogen_in_h2o + hydrogen_in_c2

        if hydrogen_total > 0:
            h2_in_h2_pct = (hydrogen_in_h2 / hydrogen_total) * 100
            h2_in_ch4_pct = (hydrogen_in_ch4 / hydrogen_total) * 100
            h2_in_h2o_pct = (hydrogen_in_h2o / hydrogen_total) * 100
        else:
            h2_in_h2_pct = h2_in_ch4_pct = h2_in_h2o_pct = 0

        # Water-gas shift equilibrium constant
        # K_eq = (CO2 * H2) / (CO * H2O)
        if co > config.MIN_FOR_RATIO and h2o > config.MIN_FOR_RATIO:
            k_wgs = (co2 * h2) / (co * h2o)
        else:
            k_wgs = None

        # Selectivity metrics
        if hydrogen_total > 0:
            h2_selectivity = (hydrogen_in_h2 / hydrogen_total)
        else:
            h2_selectivity = 0

        if carbon_total > 0:
            co_selectivity = carbon_in_co / carbon_total
        else:
            co_selectivity = 0

        # Quality flag
        if carbon_total < config.CARBON_RECOVERY_WARNING:
            quality_flag = 'Warning'
        elif hydrogen_total < config.HYDROGEN_RECOVERY_WARNING:
            quality_flag = 'Warning'
        else:
            quality_flag = 'Valid'

        # Insert into database
        cursor.execute("""
            INSERT INTO ReformerPerformance (
                SimulationID, H2_CO_Ratio, H2_CO2_Ratio, CO_CO2_Ratio,
                H2_DryBasis_molpercent, CO_DryBasis_molpercent,
                CO2_DryBasis_molpercent, CH4_DryBasis_molpercent,
                Carbon_in_CO_percent, Carbon_in_CO2_percent,
                Carbon_in_CH4_percent, Carbon_in_C2_percent, Carbon_Total_percent,
                Hydrogen_in_H2_percent, Hydrogen_in_CH4_percent,
                Hydrogen_in_H2O_percent, Hydrogen_Total_percent,
                Equilibrium_Constant_WGS, H2_Selectivity, CO_Selectivity,
                DataQualityFlag
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sim_id, h2_co_ratio, h2_co2_ratio, co_co2_ratio,
            h2_dry, co_dry, co2_dry, ch4_dry,
            carbon_in_co, carbon_in_co2, carbon_in_ch4, carbon_in_c2, carbon_total,
            h2_in_h2_pct, h2_in_ch4_pct, h2_in_h2o_pct, hydrogen_total,
            k_wgs, h2_selectivity, co_selectivity, quality_flag
        ))

        successful += 1

        if successful % 100 == 0:
            print(f"  Processed {successful}/{len(data)}...")
            conn.commit()

    except Exception as e:
        failed += 1
        if failed <= 5:
            print(f"  [ERROR] SimID {row['SimulationID']}: {e}")
        conn.rollback()

conn.commit()

print()
print("=" * 80)
print("PERFORMANCE CALCULATION COMPLETE")
print("=" * 80)
print(f"Total records: {len(data)}")
print(f"Successful: {successful}")
print(f"Failed: {failed}")
print()

# Verify
cursor.execute("SELECT COUNT(*) FROM ReformerPerformance")
perf_count = cursor.fetchone()[0]
print(f"ReformerPerformance table: {perf_count} records")
print()

# Sample statistics
print("Sample statistics:")
cursor.execute("""
    SELECT
        AVG(H2_CO_Ratio) AS Avg_H2_CO,
        MIN(H2_CO_Ratio) AS Min_H2_CO,
        MAX(H2_CO_Ratio) AS Max_H2_CO,
        AVG(H2_DryBasis_molpercent) AS Avg_H2_Dry,
        AVG(Carbon_Total_percent) AS Avg_Carbon_Recovery
    FROM ReformerPerformance
""")
row = cursor.fetchone()
print(f"  H2/CO ratio: Avg={row[0]:.2f}, Min={row[1]:.2f}, Max={row[2]:.2f}")
print(f"  H2 (dry basis): Avg={row[3]:.2f}%")
print(f"  Carbon recovery: Avg={row[4]:.2f}%")

cursor.close()
conn.close()

print()
print("[SUCCESS] Performance metrics calculated and stored!")
print("=" * 80)
