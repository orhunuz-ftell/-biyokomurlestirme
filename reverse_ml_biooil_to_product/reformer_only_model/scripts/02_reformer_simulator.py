"""
Reformer-Only Simulator
=======================

Generate 1,170 thermodynamically valid steam reforming equilibrium simulations.

This script:
1. Loads 26 bio-oil compositions from database
2. Generates 45 process condition combinations (5 temp × 3 pressure × 3 S/C)
3. Runs Cantera Gibbs minimization for reformer ONLY
4. Stores results in ReformerSimulation and ReformerOutput tables

NO downstream processing (HTS, LTS, separations) - pure reformer equilibrium.

Author: Orhun Uzdiyem
Date: November 30, 2025
"""

import sys
import os
import pyodbc
import cantera as ct
import pandas as pd
import numpy as np
from datetime import datetime

# Add config to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
import reformer_config as config

print("=" * 80)
print("REFORMER-ONLY SIMULATION - THERMODYNAMICALLY VALID")
print("=" * 80)
print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# ============================================================================
# STEP 1: DATABASE CONNECTION
# ============================================================================

print("Connecting to database...")
try:
    conn = pyodbc.connect(config.DB_CONNECTION_STRING)
    cursor = conn.cursor()
    print(f"  [OK] Connected to {config.DB_SERVER}/{config.DB_DATABASE}")
except Exception as e:
    print(f"  [ERROR] Database connection failed: {e}")
    sys.exit(1)

# ============================================================================
# STEP 2: LOAD BIO-OIL COMPOSITIONS
# ============================================================================

print("\nLoading bio-oil compositions...")
query = """
    SELECT
        BiooilId,
        aromatics,
        acids,
        alcohols,
        furans,
        phenols,
        [aldehyde&ketone] AS aldehyde_ketone
    FROM Biooil
    ORDER BY BiooilId
"""

try:
    biooils = pd.read_sql(query, conn)
    print(f"  [OK] Loaded {len(biooils)} bio-oil compositions")
    print(f"       BiooilID range: {biooils['BiooilId'].min()} to {biooils['BiooilId'].max()}")
except Exception as e:
    print(f"  [ERROR] Failed to load bio-oil data: {e}")
    conn.close()
    sys.exit(1)

# ============================================================================
# STEP 3: LOAD CANTERA MECHANISM
# ============================================================================

print("\nLoading Cantera mechanism...")
try:
    mechanism_path = config.get_mechanism_path()
    gas = ct.Solution(mechanism_path)
    print(f"  [OK] Loaded: {mechanism_path}")
    print(f"       Species: {gas.n_species}")
    print(f"       Reactions: {gas.n_reactions}")
except Exception as e:
    print(f"  [ERROR] Failed to load mechanism: {e}")
    conn.close()
    sys.exit(1)

# ============================================================================
# STEP 4: HELPER FUNCTIONS
# ============================================================================

def calculate_steam_moles(biooil_composition, sc_ratio):
    """
    Calculate steam moles needed for given S/C ratio.

    Args:
        biooil_composition: Dict with species percentages
        sc_ratio: Steam-to-carbon ratio

    Returns:
        float: Moles of steam per 100 g bio-oil
    """
    # Calculate total carbon atoms in bio-oil (per 100 g)
    total_carbon_atoms = 0

    for group, percentage in biooil_composition.items():
        if percentage > 0 and group in config.BIOOIL_SPECIES_MAP:
            species = config.BIOOIL_SPECIES_MAP[group]
            if species in config.STOICHIOMETRY:
                mw = config.MOLECULAR_WEIGHTS[species]
                moles_species = (percentage / 100) / mw  # mol per 100 g bio-oil
                c_atoms = config.STOICHIOMETRY[species].get('C', 0)
                total_carbon_atoms += moles_species * c_atoms

    # Steam moles = S/C ratio × total carbon atoms
    steam_moles = sc_ratio * total_carbon_atoms
    return steam_moles


def create_cantera_input(biooil_composition, steam_moles):
    """
    Create Cantera input composition from bio-oil + steam.

    Args:
        biooil_composition: Dict with bio-oil species percentages
        steam_moles: Moles of steam to add

    Returns:
        dict: Mole fractions for Cantera (sum = 1.0)
    """
    composition = {}

    # Add bio-oil species
    total_moles = 0
    for group, percentage in biooil_composition.items():
        if percentage > 0 and group in config.BIOOIL_SPECIES_MAP:
            species = config.BIOOIL_SPECIES_MAP[group]
            if species in gas.species_names:
                mw = config.MOLECULAR_WEIGHTS[species]
                moles = (percentage / 100) / mw  # mol per 100 g bio-oil
                composition[species] = moles
                total_moles += moles

    # Add steam
    composition['H2O'] = steam_moles
    total_moles += steam_moles

    # Normalize to mole fractions
    if total_moles > 0:
        for species in composition:
            composition[species] /= total_moles

    return composition


def run_reformer_equilibrium(composition, temperature_K, pressure_Pa):
    """
    Run Gibbs free energy minimization for reformer.

    Args:
        composition: dict of mole fractions
        temperature_K: Reformer temperature (K)
        pressure_Pa: Reformer pressure (Pa)

    Returns:
        dict: Equilibrium composition and properties
    """
    try:
        # Set initial state
        gas.TPX = temperature_K, pressure_Pa, composition

        # Perform Gibbs minimization (constant T, P)
        gas.equilibrate('TP')

        # Extract all species mole fractions
        results = {
            'temperature_K': gas.T,
            'pressure_Pa': gas.P,
            'mole_fractions': {},
            'enthalpy_J_mol': gas.enthalpy_mole,
            'entropy_J_molK': gas.entropy_mole,
            'density_kg_m3': gas.density,
            'mean_molecular_weight': gas.mean_molecular_weight,
        }

        # Get composition
        total_mole_fraction = 0
        for i, species_name in enumerate(gas.species_names):
            mole_frac = gas.X[i]
            if mole_frac > config.MIN_MOLE_FRACTION:
                results['mole_fractions'][species_name] = mole_frac
                total_mole_fraction += mole_frac

        results['total_mole_fraction'] = total_mole_fraction

        return results

    except Exception as e:
        raise RuntimeError(f"Equilibrium calculation failed: {e}")


# ============================================================================
# STEP 5: GENERATE SIMULATION MATRIX
# ============================================================================

print("\nGenerating simulation matrix...")
simulations = []

for _, biooil_row in biooils.iterrows():
    biooil_id = int(biooil_row['BiooilId'])
    biooil_comp = {
        'aromatics': biooil_row['aromatics'],
        'acids': biooil_row['acids'],
        'alcohols': biooil_row['alcohols'],
        'furans': biooil_row['furans'],
        'phenols': biooil_row['phenols'],
        'aldehyde_ketone': biooil_row['aldehyde_ketone']
    }

    for temp_C in config.TEMPERATURES_C:
        for press_bar in config.PRESSURES_BAR:
            for sc_ratio in config.SC_RATIOS:
                simulations.append({
                    'biooil_id': biooil_id,
                    'biooil_comp': biooil_comp,
                    'temperature_C': temp_C,
                    'pressure_bar': press_bar,
                    'sc_ratio': sc_ratio
                })

print(f"  [OK] Created {len(simulations)} simulation scenarios")
print(f"       {len(biooils)} bio-oils × {len(config.TEMPERATURES_C)} temps × "
      f"{len(config.PRESSURES_BAR)} pressures × {len(config.SC_RATIOS)} S/C = {len(simulations)}")

# ============================================================================
# STEP 6: RUN SIMULATIONS
# ============================================================================

print("\nRunning reformer equilibrium calculations...")
print("(This may take 2-5 minutes for 1,170 simulations)")
print()

successful = 0
failed = 0
start_time = datetime.now()

for i, sim in enumerate(simulations):
    try:
        # Extract simulation parameters
        biooil_id = sim['biooil_id']
        biooil_comp = sim['biooil_comp']
        temp_C = sim['temperature_C']
        press_bar = sim['pressure_bar']
        sc_ratio = sim['sc_ratio']

        # Calculate steam requirement
        steam_moles = calculate_steam_moles(biooil_comp, sc_ratio)

        # Create Cantera input
        cantera_input = create_cantera_input(biooil_comp, steam_moles)

        # Run equilibrium calculation
        temp_K = temp_C + 273.15
        press_Pa = press_bar * config.BAR_TO_PA
        result = run_reformer_equilibrium(cantera_input, temp_K, press_Pa)

        # Insert into ReformerSimulation table
        cursor.execute("""
            INSERT INTO ReformerSimulation (
                BiooilID, Temperature_C, Pressure_bar, SC_Ratio,
                SimulationDate, ConvergenceStatus, Notes
            ) VALUES (?, ?, ?, ?, GETDATE(), ?, ?)
        """, (
            biooil_id, temp_C, press_bar, sc_ratio,
            'Converged',
            'Reformer equilibrium only - Gibbs minimization'
        ))

        # Get the SimulationID that was just inserted
        simulation_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

        # Extract species mole percentages
        mole_fracs = result['mole_fractions']
        h2 = mole_fracs.get('H2', 0) * 100
        co = mole_fracs.get('CO', 0) * 100
        co2 = mole_fracs.get('CO2', 0) * 100
        ch4 = mole_fracs.get('CH4', 0) * 100
        h2o = mole_fracs.get('H2O', 0) * 100
        c2h4 = mole_fracs.get('C2H4', 0) * 100
        c2h6 = mole_fracs.get('C2H6', 0) * 100
        c2h2 = mole_fracs.get('C2H2', 0) * 100
        c3h6 = mole_fracs.get('C3H6', 0) * 100
        n2 = mole_fracs.get('N2', 0) * 100
        ar = mole_fracs.get('AR', 0) * 100

        # Insert into ReformerOutput table
        cursor.execute("""
            INSERT INTO ReformerOutput (
                SimulationID,
                H2_molpercent, CO_molpercent, CO2_molpercent, CH4_molpercent, H2O_molpercent,
                C2H4_molpercent, C2H6_molpercent, C2H2_molpercent, C3H6_molpercent,
                N2_molpercent, AR_molpercent,
                Temperature_K, Pressure_Pa, Enthalpy_J_mol, Entropy_J_molK,
                Density_kg_m3, MeanMolecularWeight_g_mol, TotalMoleFraction
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            simulation_id,
            h2, co, co2, ch4, h2o,
            c2h4, c2h6, c2h2, c3h6, n2, ar,
            result['temperature_K'], result['pressure_Pa'],
            result['enthalpy_J_mol'], result['entropy_J_molK'],
            result['density_kg_m3'], result['mean_molecular_weight'],
            result['total_mole_fraction']
        ))

        conn.commit()
        successful += 1

        # Progress reporting
        if (successful % config.REPORT_INTERVAL == 0) or (successful == len(simulations)):
            elapsed = (datetime.now() - start_time).total_seconds()
            rate = successful / elapsed if elapsed > 0 else 0
            remaining = (len(simulations) - successful) / rate if rate > 0 else 0
            print(f"  Progress: {successful}/{len(simulations)} "
                  f"({successful/len(simulations)*100:.1f}%) | "
                  f"Rate: {rate:.1f} sim/s | "
                  f"ETA: {remaining:.0f}s")

    except Exception as e:
        failed += 1
        if failed <= 10:  # Only print first 10 errors
            print(f"  [ERROR] Simulation {i+1} failed: {e}")
        conn.rollback()

# ============================================================================
# STEP 7: SUMMARY
# ============================================================================

end_time = datetime.now()
elapsed = (end_time - start_time).total_seconds()

print()
print("=" * 80)
print("SIMULATION COMPLETE")
print("=" * 80)
print(f"Total scenarios: {len(simulations)}")
print(f"Successful: {successful} ({successful/len(simulations)*100:.1f}%)")
print(f"Failed: {failed} ({failed/len(simulations)*100:.1f}%)")
print(f"Execution time: {elapsed:.1f} seconds")
print(f"Average time per simulation: {elapsed/len(simulations):.3f} seconds")
print()

# Verify database records
print("Verifying database records...")
cursor.execute("SELECT COUNT(*) FROM ReformerSimulation")
sim_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM ReformerOutput")
output_count = cursor.fetchone()[0]

print(f"  ReformerSimulation table: {sim_count} records")
print(f"  ReformerOutput table: {output_count} records")
print()

if sim_count == successful and output_count == successful:
    print("[SUCCESS] All records properly stored in database!")
else:
    print("[WARNING] Record count mismatch - check for errors")

# Sample output
print("\nSample results (first 3 simulations):")
cursor.execute("""
    SELECT TOP 3
        s.SimulationID,
        s.BiooilID,
        s.Temperature_C,
        s.Pressure_bar,
        s.SC_Ratio,
        o.H2_molpercent,
        o.CO_molpercent,
        o.CO2_molpercent,
        o.CH4_molpercent,
        o.H2O_molpercent
    FROM ReformerSimulation s
    INNER JOIN ReformerOutput o ON s.SimulationID = o.SimulationID
    ORDER BY s.SimulationID
""")

print("\nSimID  BiooilID  T(°C)  P(bar)  S/C   H2(%)   CO(%)  CO2(%)  CH4(%)  H2O(%)")
for row in cursor.fetchall():
    print(f"{row[0]:5d}  {row[1]:8d}  {row[2]:5.0f}  {row[3]:6.0f}  {row[4]:4.1f}  "
          f"{row[5]:6.2f}  {row[6]:6.2f}  {row[7]:6.2f}  {row[8]:6.2f}  {row[9]:6.2f}")

# Close database
cursor.close()
conn.close()

print()
print("=" * 80)
print("NEXT STEPS")
print("=" * 80)
print("1. Run 03_calculate_performance.py to compute performance metrics")
print("2. Run 04_export_ml_dataset.py to create CSV for machine learning")
print("3. Run 05_validate_data.py to verify thermodynamic consistency")
print()
print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
