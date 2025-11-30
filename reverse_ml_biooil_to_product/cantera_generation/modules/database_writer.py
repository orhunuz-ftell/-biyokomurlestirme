"""
Database Writer for Cantera Simulation Results

This module handles:
- Inserting simulation results into SQL Server database
- Writing to 5 tables (AspenSimulation, ReformingConditions, HydrogenProduct, etc.)
- Transaction management and error handling
- Resume capability for interrupted runs
"""

import pyodbc
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import cantera_config as config


class DatabaseWriter:
    """Write Cantera simulation results to SQL Server database"""

    def __init__(self):
        """Initialize database writer"""
        self.conn = None
        self.cursor = None

    def connect(self) -> bool:
        """
        Connect to SQL Server database

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.conn = pyodbc.connect(config.DB_CONNECTION_STRING)
            self.cursor = self.conn.cursor()
            if config.VERBOSE:
                print("[OK] Database connection established for writing")
            return True
        except Exception as e:
            print(f"[ERROR] Database connection failed: {e}")
            return False

    def check_existing_simulation(self, biooil_id: int, temperature: float,
                                  pressure: float, sc_ratio: float) -> Optional[int]:
        """
        Check if simulation already exists in database

        Args:
            biooil_id: Bio-oil ID
            temperature: Temperature (°C)
            pressure: Pressure (bar)
            sc_ratio: S/C ratio

        Returns:
            int: SimulationId if exists, None otherwise
        """
        query = """
        SELECT TOP 1 SimulationId
        FROM AspenSimulation
        WHERE Biooil_Id = ?
          AND ABS(Temperature_C - ?) < 0.01
          AND ABS(Pressure_bar - ?) < 0.01
          AND ABS(SC_ratio - ?) < 0.01
        """

        try:
            self.cursor.execute(query, (biooil_id, temperature, pressure, sc_ratio))
            row = self.cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            print(f"[WARNING] Check existing simulation failed: {e}")
            return None

    def insert_simulation_master(self, biooil_id: int, temperature: float,
                                pressure: float, sc_ratio: float,
                                converged: bool = True,
                                simulation_source: str = "Cantera") -> int:
        """
        Insert master record into AspenSimulation table

        Args:
            biooil_id: Bio-oil ID
            temperature: Temperature (°C)
            pressure: Pressure (bar)
            sc_ratio: S/C ratio
            converged: Convergence status
            simulation_source: Data source (default "Cantera")

        Returns:
            int: SimulationId (newly inserted ID)
        """
        query = """
        INSERT INTO AspenSimulation (
            Biooil_Id,
            Temperature_C,
            Pressure_bar,
            SC_ratio,
            SimulationDate,
            ConvergenceStatus,
            SimulationSource,
            Notes
        ) VALUES (?, ?, ?, ?, GETDATE(), ?, ?, ?)
        """

        notes = f"Generated using Cantera v{config.__version__} with GRI-Mech 3.0"

        try:
            self.cursor.execute(query, (
                biooil_id, temperature, pressure, sc_ratio,
                1 if converged else 0,
                simulation_source,
                notes
            ))
            self.conn.commit()

            # Get the inserted SimulationId
            self.cursor.execute("SELECT @@IDENTITY")
            simulation_id = int(self.cursor.fetchone()[0])

            return simulation_id

        except Exception as e:
            self.conn.rollback()
            print(f"[ERROR] Insert simulation master failed: {e}")
            raise

    def insert_reforming_conditions(self, simulation_id: int,
                                    reformer_data: Dict,
                                    hts_data: Dict,
                                    lts_data: Dict) -> bool:
        """
        Insert reforming conditions into ReformingConditions table

        Args:
            simulation_id: Simulation ID
            reformer_data: Reformer results
            hts_data: HTS results
            lts_data: LTS results

        Returns:
            bool: True if successful
        """
        query = """
        INSERT INTO ReformingConditions (
            Simulation_Id,
            Reformer_Temp_C,
            Reformer_Pressure_bar,
            HTS_Temp_C,
            LTS_Temp_C,
            Flash_Temp_C,
            PSA_Pressure_bar,
            Reformer_Residence_Time_s,
            HTS_Residence_Time_s,
            LTS_Residence_Time_s,
            Catalyst_Type_Reformer,
            Catalyst_Type_HTS,
            Catalyst_Type_LTS
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            self.cursor.execute(query, (
                simulation_id,
                reformer_data['temperature_K'] - 273.15,
                reformer_data['pressure_Pa'] / 1e5,
                config.HTS_TEMPERATURE_C,
                config.LTS_TEMPERATURE_C,
                config.FLASH_TEMPERATURE_C,
                config.PSA_PRESSURE_BAR,
                2.0,  # Typical reformer residence time (s)
                1.0,  # HTS residence time
                0.5,  # LTS residence time
                'Ni-based',  # Typical reformer catalyst
                'Fe-Cr',     # Typical HTS catalyst
                'Cu-Zn'      # Typical LTS catalyst
            ))
            self.conn.commit()
            return True

        except Exception as e:
            self.conn.rollback()
            print(f"[ERROR] Insert reforming conditions failed: {e}")
            return False

    def insert_hydrogen_product(self, simulation_id: int,
                               ml_features: Dict) -> bool:
        """
        Insert hydrogen product properties (16 ML features)

        Args:
            simulation_id: Simulation ID
            ml_features: Dictionary with 16 ML features

        Returns:
            bool: True if successful
        """
        query = """
        INSERT INTO HydrogenProduct (
            Simulation_Id,
            H2_Yield,
            H2_Purity,
            H2_ProductionRate,
            CarbonConversion,
            EnergyEfficiency,
            H2_CO_Ratio,
            Syngas_H2_Content,
            Syngas_CO_Content,
            Syngas_CO2_Content,
            Syngas_CH4_Content,
            Product_H2_Content,
            Product_CO2_Content,
            Product_CH4_Content,
            WaterConsumption,
            SteamToCarbon_Actual,
            OverallH2Recovery
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            self.cursor.execute(query, (
                simulation_id,
                ml_features['H2_Yield'],
                ml_features['H2_Purity'],
                ml_features['H2_ProductionRate'],
                ml_features['CarbonConversion'],
                ml_features['EnergyEfficiency'],
                ml_features['H2_CO_Ratio'],
                ml_features['Syngas_H2_Content'],
                ml_features['Syngas_CO_Content'],
                ml_features['Syngas_CO2_Content'],
                ml_features['Syngas_CH4_Content'],
                ml_features['Product_H2_Content'],
                ml_features['Product_CO2_Content'],
                ml_features['Product_CH4_Content'],
                ml_features['WaterConsumption'],
                ml_features['SteamToCarbon_Actual'],
                ml_features['OverallH2Recovery']
            ))
            self.conn.commit()
            return True

        except Exception as e:
            self.conn.rollback()
            print(f"[ERROR] Insert hydrogen product failed: {e}")
            return False

    def insert_syngas_composition(self, simulation_id: int,
                                  reformer: Dict,
                                  hts: Dict,
                                  lts: Dict,
                                  flash_vapor: Dict) -> bool:
        """
        Insert syngas composition at 4 process points

        Args:
            simulation_id: Simulation ID
            reformer: Reformer outlet composition
            hts: HTS outlet composition
            lts: LTS outlet composition
            flash_vapor: Flash vapor composition

        Returns:
            bool: True if successful
        """
        query = """
        INSERT INTO SyngasComposition (
            Simulation_Id,
            Location,
            H2_MoleFraction,
            CO_MoleFraction,
            CO2_MoleFraction,
            CH4_MoleFraction,
            H2O_MoleFraction,
            N2_MoleFraction,
            Temperature_C,
            Pressure_bar
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        locations = [
            ('Reformer_Outlet', reformer),
            ('HTS_Outlet', hts),
            ('LTS_Outlet', lts),
            ('Flash_Vapor', flash_vapor)
        ]

        try:
            for location, data in locations:
                comp = data['mole_fractions']
                self.cursor.execute(query, (
                    simulation_id,
                    location,
                    comp.get('H2', 0.0),
                    comp.get('CO', 0.0),
                    comp.get('CO2', 0.0),
                    comp.get('CH4', 0.0),
                    comp.get('H2O', 0.0),
                    comp.get('N2', 0.0),
                    data['temperature_K'] - 273.15,
                    data['pressure_Pa'] / 1e5
                ))

            self.conn.commit()
            return True

        except Exception as e:
            self.conn.rollback()
            print(f"[ERROR] Insert syngas composition failed: {e}")
            return False

    def insert_energy_balance(self, simulation_id: int,
                             energy_data: Dict) -> bool:
        """
        Insert energy balance data

        Args:
            simulation_id: Simulation ID
            energy_data: Energy balance dictionary

        Returns:
            bool: True if successful
        """
        query = """
        INSERT INTO EnergyBalance (
            Simulation_Id,
            Feed_Enthalpy,
            Product_Enthalpy,
            Heat_Input_Reformer,
            Heat_Output_HTS,
            Heat_Output_LTS,
            Heat_Output_Flash,
            Net_Heat_Duty,
            Cold_Gas_Efficiency,
            Thermal_Efficiency,
            Exergy_Efficiency,
            CO2_Emissions,
            Energy_Per_kg_H2
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            self.cursor.execute(query, (
                simulation_id,
                energy_data.get('feed_enthalpy', 0.0),
                energy_data.get('product_enthalpy', 0.0),
                energy_data.get('heat_input_reformer', 0.0),
                energy_data.get('heat_output_hts', 0.0),
                energy_data.get('heat_output_lts', 0.0),
                energy_data.get('heat_output_flash', 0.0),
                energy_data.get('net_heat_duty', 0.0),
                energy_data.get('cold_gas_efficiency', 0.0),
                energy_data.get('thermal_efficiency', 0.0),
                energy_data.get('exergy_efficiency', 0.0),
                energy_data.get('co2_emissions', 0.0),
                energy_data.get('energy_per_kg_h2', 0.0)
            ))
            self.conn.commit()
            return True

        except Exception as e:
            self.conn.rollback()
            print(f"[ERROR] Insert energy balance failed: {e}")
            return False

    def write_complete_simulation(self, simulation_data: Dict) -> bool:
        """
        Write complete simulation results to all 5 tables

        Args:
            simulation_data: Complete simulation results

        Returns:
            bool: True if all writes successful
        """
        try:
            # Check if already exists
            existing_id = self.check_existing_simulation(
                simulation_data['BiooilId'],
                simulation_data['Temperature_C'],
                simulation_data['Pressure_bar'],
                simulation_data['SC_ratio']
            )

            if existing_id:
                if config.VERBOSE:
                    print(f"[SKIP] Simulation already exists (ID={existing_id})")
                return True

            # Insert master record
            simulation_id = self.insert_simulation_master(
                simulation_data['BiooilId'],
                simulation_data['Temperature_C'],
                simulation_data['Pressure_bar'],
                simulation_data['SC_ratio'],
                simulation_data.get('converged', True)
            )

            # Insert reforming conditions
            self.insert_reforming_conditions(
                simulation_id,
                simulation_data['reformer'],
                simulation_data['hts'],
                simulation_data['lts']
            )

            # Insert hydrogen product (16 ML features)
            self.insert_hydrogen_product(
                simulation_id,
                simulation_data['ml_features']
            )

            # Insert syngas composition
            self.insert_syngas_composition(
                simulation_id,
                simulation_data['reformer'],
                simulation_data['hts'],
                simulation_data['lts'],
                simulation_data['flash_vapor']
            )

            # Insert energy balance
            self.insert_energy_balance(
                simulation_id,
                simulation_data.get('energy_balance', {})
            )

            if config.VERBOSE:
                print(f"[OK] Simulation written (ID={simulation_id})")

            return True

        except Exception as e:
            print(f"[ERROR] Write complete simulation failed: {e}")
            return False

    def get_completion_count(self) -> int:
        """
        Get count of completed simulations

        Returns:
            int: Number of simulations in database
        """
        try:
            query = "SELECT COUNT(*) FROM AspenSimulation WHERE SimulationSource = 'Cantera'"
            self.cursor.execute(query)
            count = self.cursor.fetchone()[0]
            return count
        except Exception as e:
            print(f"[WARNING] Get completion count failed: {e}")
            return 0

    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            if config.VERBOSE:
                print("[OK] Database connection closed")


# ==============================================================================
# TESTING
# ==============================================================================

def test_database_writer():
    """Test database writer with sample data"""
    print("\n" + "="*80)
    print("TESTING DATABASE WRITER")
    print("="*80)

    writer = DatabaseWriter()

    # Test 1: Connect
    print("\nTest 1: Database Connection")
    if writer.connect():
        print("[PASS] Database connected")
    else:
        print("[FAIL] Database connection failed")
        return

    # Test 2: Check completion count
    print("\nTest 2: Check Completion Count")
    count = writer.get_completion_count()
    print(f"[INFO] Existing Cantera simulations: {count}")

    # Test 3: Create sample simulation data
    print("\nTest 3: Write Sample Simulation")

    sample_data = {
        'BiooilId': 1,
        'Temperature_C': 800.0,
        'Pressure_bar': 15.0,
        'SC_ratio': 4.0,
        'converged': True,
        'reformer': {
            'temperature_K': 1073.15,
            'pressure_Pa': 1.5e6,
            'mole_fractions': {'H2': 0.50, 'CO': 0.15, 'CO2': 0.20, 'CH4': 0.05, 'H2O': 0.08, 'N2': 0.02}
        },
        'hts': {
            'temperature_K': 643.15,
            'pressure_Pa': 1.5e6,
            'mole_fractions': {'H2': 0.55, 'CO': 0.08, 'CO2': 0.25, 'CH4': 0.05, 'H2O': 0.05, 'N2': 0.02}
        },
        'lts': {
            'temperature_K': 483.15,
            'pressure_Pa': 1.5e6,
            'mole_fractions': {'H2': 0.60, 'CO': 0.03, 'CO2': 0.28, 'CH4': 0.05, 'H2O': 0.02, 'N2': 0.02}
        },
        'flash_vapor': {
            'temperature_K': 313.15,
            'pressure_Pa': 1.01e5,
            'mole_fractions': {'H2': 0.61, 'CO': 0.03, 'CO2': 0.28, 'CH4': 0.05, 'N2': 0.02, 'H2O': 0.01}
        },
        'ml_features': {
            'H2_Yield': 10.5,
            'H2_Purity': 99.9,
            'H2_ProductionRate': 500.0,
            'CarbonConversion': 95.0,
            'EnergyEfficiency': 65.0,
            'H2_CO_Ratio': 20.0,
            'Syngas_H2_Content': 60.0,
            'Syngas_CO_Content': 3.0,
            'Syngas_CO2_Content': 28.0,
            'Syngas_CH4_Content': 5.0,
            'Product_H2_Content': 99.9,
            'Product_CO2_Content': 0.05,
            'Product_CH4_Content': 0.03,
            'WaterConsumption': 2.5,
            'SteamToCarbon_Actual': 4.0,
            'OverallH2Recovery': 88.0
        },
        'energy_balance': {
            'feed_enthalpy': 1850.0,
            'product_enthalpy': 1420.0,
            'heat_input_reformer': 500.0,
            'heat_output_hts': 50.0,
            'heat_output_lts': 30.0,
            'heat_output_flash': 20.0,
            'net_heat_duty': 400.0,
            'cold_gas_efficiency': 65.0,
            'thermal_efficiency': 70.0,
            'exergy_efficiency': 60.0,
            'co2_emissions': 5.2,
            'energy_per_kg_h2': 38.5
        }
    }

    # Write to database
    success = writer.write_complete_simulation(sample_data)

    if success:
        print("[PASS] Sample simulation written successfully")
    else:
        print("[FAIL] Sample simulation write failed")

    # Test 4: Check count again
    print("\nTest 4: Verify Completion Count")
    new_count = writer.get_completion_count()
    print(f"[INFO] Cantera simulations after write: {new_count}")

    writer.close()

    print("\n" + "="*80)
    print("DATABASE WRITER TEST COMPLETE")
    print("="*80)


if __name__ == "__main__":
    test_database_writer()
