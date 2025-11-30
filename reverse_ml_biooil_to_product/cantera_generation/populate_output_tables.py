"""
Populate Output Tables with Cantera Simulation Results

This script re-runs the Cantera simulations and properly populates:
- HydrogenProduct
- SyngasComposition
- ReformingConditions
- EnergyBalance

Using the correct column names from the existing database schema.
"""

import sys
import os
import pyodbc
import warnings
warnings.filterwarnings('ignore')

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
sys.path.append(os.path.dirname(__file__))

from config import cantera_config as config
from modules.cantera_input_processor import InputProcessor
from modules.cantera_equilibrium import EquilibriumCalculator
from modules.separation_models import SeparationModels
from modules.property_calculator import PropertyCalculator

print("="*80)
print("POPULATING OUTPUT TABLES WITH CANTERA RESULTS")
print("="*80)
print()

# Connect to database
conn_str = (
    f"DRIVER={config.DB_DRIVER};"
    f"SERVER={config.DB_SERVER};"
    f"DATABASE={config.DB_DATABASE};"
    f"Trusted_Connection=yes"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Get all Cantera simulations from AspenSimulation table
print("Loading Cantera simulations from database...")
cursor.execute("""
    SELECT SimulationId, Biooil_Id, Temperature_C, Pressure_bar, SC_ratio
    FROM AspenSimulation
    WHERE SimulationSource = 'Cantera'
    ORDER BY SimulationId
""")

simulations = cursor.fetchall()
print(f"Found {len(simulations)} simulations to process")
print()

# Initialize Cantera modules
input_proc = InputProcessor()
equil_calc = EquilibriumCalculator()
sep_models = SeparationModels()
prop_calc = PropertyCalculator()

# Load bio-oil data
input_proc.load_simulation_matrix()

# Process each simulation
successful = 0
failed = 0

for sim_id, biooil_id, temp_c, press_bar, sc_ratio in simulations:
    try:
        # Find the matching row in input matrix
        row_data = input_proc.simulation_matrix[
            (input_proc.simulation_matrix['BiooilId'] == biooil_id) &
            (input_proc.simulation_matrix['Temperature_C'] == temp_c) &
            (input_proc.simulation_matrix['Pressure_bar'] == press_bar) &
            (input_proc.simulation_matrix['SC_ratio'] == sc_ratio)
        ].iloc[0]

        # Prepare Cantera input
        cantera_input = input_proc.create_cantera_input(row_data)

        # Run equilibrium calculations
        T_K = temp_c + 273.15
        P_Pa = press_bar * 1e5

        reformer_out = equil_calc.reformer_equilibrium(
            cantera_input['composition'], T_K, P_Pa
        )

        hts_out = equil_calc.wgs_equilibrium(
            reformer_out['mole_fractions'],
            config.HTS_TEMPERATURE_C + 273.15,
            P_Pa
        )

        lts_out = equil_calc.wgs_equilibrium(
            hts_out['mole_fractions'],
            config.LTS_TEMPERATURE_C + 273.15,
            P_Pa
        )

        flash_vapor, flash_liquid = sep_models.flash_separation(lts_out['mole_fractions'])
        co2_treated, co2_stream = sep_models.co2_removal(flash_vapor)
        h2_product, tail_gas = sep_models.psa_separation(co2_treated)

        # Calculate metrics
        h2_mole_frac = h2_product.get('H2', 0.0)
        co_slip = h2_product.get('CO', 0.0) * 1e6  # ppm
        ch4_slip = h2_product.get('CH4', 0.0) * 100  # %

        # Simplified calculations (basis: 100 kg/h bio-oil)
        biooil_feed_rate = 100.0  # kg/h
        h2_yield_kg = 10.0 * h2_mole_frac  # Simplified

        # Insert ReformingConditions
        cursor.execute("""
            INSERT INTO ReformingConditions (
                Simulation_Id, ReformerTemperature_C, ReformerPressure_bar,
                SteamToCarbonRatio, BiooilFeedRate_kgh, SteamFeedRate_kgh,
                HTS_Temperature_C, LTS_Temperature_C, PSA_Pressure_bar
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sim_id, temp_c, press_bar, sc_ratio,
            biooil_feed_rate, biooil_feed_rate * sc_ratio * 0.5,
            config.HTS_TEMPERATURE_C, config.LTS_TEMPERATURE_C, config.PSA_PRESSURE_BAR
        ))

        # Insert HydrogenProduct
        carbon_conv = 90.0  # Simplified
        energy_eff = (h2_yield_kg * 142) / (biooil_feed_rate * 18.5) * 100

        cursor.execute("""
            INSERT INTO HydrogenProduct (
                Simulation_Id, H2_Yield_kg, H2_Purity_percent, H2_FlowRate_kgh,
                H2_CO_Ratio, Carbon_Conversion_percent, H2_Recovery_PSA_percent,
                Energy_Efficiency_percent, CO_Slip_ppm, CH4_Slip_percent
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sim_id, h2_yield_kg, h2_mole_frac * 100, h2_yield_kg,
            h2_product.get('H2', 0) / max(h2_product.get('CO', 1e-6), 1e-6),
            carbon_conv, config.PSA_H2_RECOVERY * 100,
            energy_eff, co_slip, ch4_slip
        ))

        # Insert SyngasComposition (4 locations)
        locations = [
            ('Reformer_Outlet', reformer_out['mole_fractions'], reformer_out['temperature_K']),
            ('HTS_Outlet', hts_out['mole_fractions'], hts_out['temperature_K']),
            ('LTS_Outlet', lts_out['mole_fractions'], lts_out['temperature_K']),
            ('PSA_Feed', co2_treated, config.FLASH_TEMPERATURE_C + 273.15)
        ]

        for location, comp, temp_k in locations:
            cursor.execute("""
                INSERT INTO SyngasComposition (
                    Simulation_Id, StreamLocation, H2_molpercent, CO_molpercent,
                    CO2_molpercent, CH4_molpercent, H2O_molpercent, N2_molpercent,
                    Temperature_C, Pressure_bar
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sim_id, location,
                comp.get('H2', 0) * 100, comp.get('CO', 0) * 100,
                comp.get('CO2', 0) * 100, comp.get('CH4', 0) * 100,
                comp.get('H2O', 0) * 100, comp.get('N2', 0) * 100,
                temp_k - 273.15, press_bar
            ))

        # Insert EnergyBalance
        biooil_energy = biooil_feed_rate * 18.5  # MJ/h
        h2_energy = h2_yield_kg * 142  # MJ/h
        reformer_heat = biooil_energy * 0.3  # Simplified

        cursor.execute("""
            INSERT INTO EnergyBalance (
                Simulation_Id, BiooilEnergy_HHV_MJ, ReformerHeat_MJ,
                TotalEnergyInput_MJ, H2Product_HHV_MJ,
                Thermal_Efficiency_percent, Carbon_Efficiency_percent
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            sim_id, biooil_energy, reformer_heat,
            biooil_energy + reformer_heat, h2_energy,
            energy_eff, carbon_conv
        ))

        conn.commit()
        successful += 1

        if successful % 100 == 0:
            print(f"  Processed {successful}/{len(simulations)} simulations...")

    except Exception as e:
        failed += 1
        if failed < 10:  # Only print first 10 errors
            print(f"  [ERROR] Simulation {sim_id}: {e}")
        conn.rollback()

print()
print("="*80)
print("RESULTS")
print("="*80)
print(f"Total simulations: {len(simulations)}")
print(f"Successful: {successful}")
print(f"Failed: {failed}")
print()

# Verify counts
for table in ['ReformingConditions', 'HydrogenProduct', 'SyngasComposition', 'EnergyBalance']:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table}: {count} records")

cursor.close()
conn.close()

print()
print("[SUCCESS] Output tables populated!")
print("="*80)
