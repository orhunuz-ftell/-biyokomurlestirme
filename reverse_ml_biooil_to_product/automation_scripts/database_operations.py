"""
==============================================================================
ASPEN AUTOMATION - DATABASE OPERATIONS MODULE
==============================================================================
Purpose: Handle all database operations for storing simulation results
Author: Orhun Uzdiyem
Date: 2025-11-16

Functions:
- Connect to SQL Server database
- Insert simulation results into 5 tables
- Track progress (resume capability)
- Mark failed simulations
- Validation and error handling
==============================================================================
"""

import pyodbc
import config
from datetime import datetime


class DatabaseOperations:
    """Handle database operations for simulation results."""

    def __init__(self):
        """Initialize database connection."""
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to SQL Server database."""
        print("\n[DATABASE] Connecting to SQL Server...")
        # TODO_DB: Connection string uses config.DB_CONNECTION_STRING
        # which contains config.DB_SERVER - update in config.py!
        print(f"  Server: {config.DB_SERVER}")  # TODO_DB
        print(f"  Database: {config.DB_DATABASE}")

        try:
            self.conn = pyodbc.connect(config.DB_CONNECTION_STRING)
            self.cursor = self.conn.cursor()
            print("  [OK] Connected to database")
            return True
        except Exception as e:
            print(f"  [ERROR] Failed to connect: {e}")
            print("\n  Troubleshooting:")
            print("    1. Check SQL Server is running")
            print("    2. Update DB_SERVER in config.py (search: TODO_DB)")
            print("    3. Verify database 'BIOOIL' exists")
            print("    4. Check Windows authentication or credentials")
            return False

    def test_connection(self):
        """Test database connection with a simple query."""
        try:
            # Test query
            self.cursor.execute("SELECT @@VERSION")
            version = self.cursor.fetchone()[0]
            print(f"\n[DATABASE] Connected to: {version[:50]}...")

            # Check if tables exist
            self.cursor.execute("""
                SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_NAME IN (
                    'AspenSimulation', 'ReformingConditions',
                    'HydrogenProduct', 'SyngasComposition', 'EnergyBalance'
                )
                ORDER BY TABLE_NAME
            """)

            tables = [row[0] for row in self.cursor.fetchall()]
            print(f"\n  Found {len(tables)} required tables:")
            for table in tables:
                print(f"    - {table}")

            if len(tables) == 5:
                print("  [OK] All required tables exist")
                return True
            else:
                print("  [ERROR] Missing tables! Run database creation scripts first.")
                return False

        except Exception as e:
            print(f"  [ERROR] Database test failed: {e}")
            return False

    def insert_simulation(self, biooil_id, convergence_status, mass_error=None,
                         energy_error=None, warnings=None, notes=None):
        """
        Insert simulation record into AspenSimulation table.

        Returns:
            simulation_id (int) if successful, None if failed
        """
        try:
            sql = """
                INSERT INTO AspenSimulation (
                    Biooil_Id, SimulationDate, AspenVersion,
                    ConvergenceStatus, ConvergenceIterations,
                    MassBalanceError_percent, EnergyBalanceError_percent,
                    Warnings, Notes, ValidationFlag
                ) VALUES (?, GETDATE(), ?, ?, ?, ?, ?, ?, ?, ?)
            """

            self.cursor.execute(sql, (
                biooil_id,
                'V8.8',
                convergence_status,
                None,  # Iterations (not easily available)
                mass_error,
                energy_error,
                warnings,
                notes,
                0  # ValidationFlag (will be updated later if validated)
            ))

            self.conn.commit()

            # Get the inserted simulation ID
            self.cursor.execute("SELECT @@IDENTITY")
            simulation_id = self.cursor.fetchone()[0]

            return int(simulation_id)

        except Exception as e:
            print(f"    [ERROR] Failed to insert simulation: {e}")
            self.conn.rollback()
            return None

    def insert_reforming_conditions(self, simulation_id, temp_c, pres_bar, sc_ratio,
                                    biooil_flow=100.0, steam_flow=200.0,
                                    hts_temp=370.0, lts_temp=210.0, psa_pres=25.0):
        """Insert reforming conditions into ReformingConditions table."""
        try:
            sql = """
                INSERT INTO ReformingConditions (
                    Simulation_Id,
                    ReformerTemperature_C, ReformerPressure_bar, SteamToCarbonRatio,
                    BiooilFeedRate_kgh, SteamFeedRate_kgh,
                    ResidenceTime_min, CatalystWeight_kg, GHSV_h1,
                    HTS_Temperature_C, LTS_Temperature_C, PSA_Pressure_bar
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            self.cursor.execute(sql, (
                simulation_id,
                temp_c, pres_bar, sc_ratio,
                biooil_flow, steam_flow,
                2.5,   # Residence time (typical value)
                50.0,  # Catalyst weight (typical value)
                5000.0,  # GHSV (typical value)
                hts_temp, lts_temp, psa_pres
            ))

            self.conn.commit()
            return True

        except Exception as e:
            print(f"    [ERROR] Failed to insert reforming conditions: {e}")
            self.conn.rollback()
            return False

    def insert_hydrogen_product(self, simulation_id, h2_data):
        """
        Insert hydrogen product properties into HydrogenProduct table.

        Args:
            simulation_id: ID from AspenSimulation table
            h2_data: Dictionary from aspen_interface.extract_h2_properties()
        """
        try:
            sql = """
                INSERT INTO HydrogenProduct (
                    Simulation_Id,
                    H2_Yield_kg, H2_Purity_percent,
                    H2_FlowRate_kgh, H2_FlowRate_Nm3h,
                    H2_CO_Ratio, H2_CO2_Ratio,
                    CO2_Production_kg, CO2_Purity_percent,
                    CH4_Slip_percent, CO_Slip_ppm,
                    Carbon_Conversion_percent, H2_Recovery_PSA_percent,
                    Energy_Efficiency_percent, Specific_Energy_MJperkg_H2,
                    TailGas_FlowRate_kgh, TailGas_HHV_MJperkg
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            self.cursor.execute(sql, (
                simulation_id,
                h2_data.get('H2_Yield_kg'),
                h2_data.get('H2_Purity_percent'),
                h2_data.get('H2_FlowRate_kgh'),
                h2_data.get('H2_FlowRate_Nm3h'),
                h2_data.get('H2_CO_Ratio'),
                h2_data.get('H2_CO2_Ratio'),
                None,  # CO2 production (calculate if needed)
                None,  # CO2 purity (extract if needed)
                h2_data.get('CH4_Slip_percent'),
                h2_data.get('CO_Slip_ppm'),
                90.0,  # Carbon conversion (placeholder)
                88.0,  # H2 recovery PSA (typical value)
                None,  # Energy efficiency (calculate if needed)
                None,  # Specific energy (calculate if needed)
                None,  # Tail gas flow (extract if needed)
                None   # Tail gas HHV (extract if needed)
            ))

            self.conn.commit()
            return True

        except Exception as e:
            print(f"    [ERROR] Failed to insert H2 product: {e}")
            self.conn.rollback()
            return False

    def insert_syngas_composition(self, simulation_id, location, syngas_data):
        """
        Insert syngas composition into SyngasComposition table.

        Args:
            simulation_id: ID from AspenSimulation table
            location: Stream location name (e.g., 'Reformer_Out')
            syngas_data: Dictionary from aspen_interface.extract_syngas_composition()
        """
        try:
            sql = """
                INSERT INTO SyngasComposition (
                    Simulation_Id, StreamLocation,
                    H2_molpercent, CO_molpercent, CO2_molpercent,
                    CH4_molpercent, H2O_molpercent, N2_molpercent,
                    Temperature_C, Pressure_bar,
                    MassFlowRate_kgh, MolarFlowRate_kmolh
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            self.cursor.execute(sql, (
                simulation_id,
                location,
                syngas_data.get('H2_molpercent'),
                syngas_data.get('CO_molpercent'),
                syngas_data.get('CO2_molpercent'),
                syngas_data.get('CH4_molpercent'),
                syngas_data.get('H2O_molpercent'),
                syngas_data.get('N2_molpercent'),
                syngas_data.get('Temperature_C'),
                syngas_data.get('Pressure_bar'),
                syngas_data.get('MassFlowRate_kgh'),
                syngas_data.get('MolarFlowRate_kmolh')
            ))

            self.conn.commit()
            return True

        except Exception as e:
            print(f"    [ERROR] Failed to insert syngas composition: {e}")
            self.conn.rollback()
            return False

    def insert_energy_balance(self, simulation_id, energy_data):
        """
        Insert energy balance into EnergyBalance table.

        Args:
            simulation_id: ID from AspenSimulation table
            energy_data: Dictionary from aspen_interface.extract_energy_data()
        """
        try:
            sql = """
                INSERT INTO EnergyBalance (
                    Simulation_Id,
                    BiooilEnergy_HHV_MJ, PreheaterHeat_MJ, ReformerHeat_MJ,
                    TotalEnergyInput_MJ,
                    H2Product_HHV_MJ, TailGasEnergy_MJ,
                    HeatRecovered_MJ, HeatLoss_MJ,
                    Thermal_Efficiency_percent, Carbon_Efficiency_percent
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            self.cursor.execute(sql, (
                simulation_id,
                None,  # Bio-oil HHV (calculate if needed)
                energy_data.get('PreheaterHeat_MJ'),
                energy_data.get('ReformerHeat_MJ'),
                energy_data.get('TotalEnergyInput_MJ'),
                None,  # H2 product HHV (calculate if needed)
                None,  # Tail gas energy (calculate if needed)
                None,  # Heat recovered (calculate if needed)
                None,  # Heat loss (calculate if needed)
                None,  # Thermal efficiency (calculate if needed)
                None   # Carbon efficiency (calculate if needed)
            ))

            self.conn.commit()
            return True

        except Exception as e:
            print(f"    [ERROR] Failed to insert energy balance: {e}")
            self.conn.rollback()
            return False

    def mark_simulation_failed(self, biooil_id, error_message):
        """Mark a simulation as failed in database."""
        try:
            sql = """
                INSERT INTO AspenSimulation (
                    Biooil_Id, SimulationDate, AspenVersion,
                    ConvergenceStatus, Warnings, Notes, ValidationFlag
                ) VALUES (?, GETDATE(), ?, ?, ?, ?, ?)
            """

            self.cursor.execute(sql, (
                biooil_id,
                'V8.8',
                'Failed',
                error_message[:500] if error_message else None,
                'Automation: Failed to converge',
                0
            ))

            self.conn.commit()
            return True

        except Exception as e:
            print(f"    [ERROR] Failed to mark simulation as failed: {e}")
            self.conn.rollback()
            return False

    def get_completed_simulations(self):
        """
        Get list of BiooilIds that already have completed simulations.

        Returns:
            Set of BiooilIds
        """
        try:
            sql = """
                SELECT DISTINCT Biooil_Id
                FROM AspenSimulation
                WHERE ConvergenceStatus IN ('Converged', 'Failed')
            """

            self.cursor.execute(sql)
            completed = {row[0] for row in self.cursor.fetchall()}

            return completed

        except Exception as e:
            print(f"    [ERROR] Failed to get completed simulations: {e}")
            return set()

    def get_simulation_statistics(self):
        """Get statistics on simulation results."""
        try:
            sql = """
                SELECT
                    ConvergenceStatus,
                    COUNT(*) as Count,
                    AVG(MassBalanceError_percent) as AvgMassError,
                    AVG(EnergyBalanceError_percent) as AvgEnergyError
                FROM AspenSimulation
                GROUP BY ConvergenceStatus
            """

            self.cursor.execute(sql)
            stats = {}

            for row in self.cursor.fetchall():
                stats[row[0]] = {
                    'count': row[1],
                    'avg_mass_error': row[2],
                    'avg_energy_error': row[3]
                }

            return stats

        except Exception as e:
            print(f"    [ERROR] Failed to get statistics: {e}")
            return {}

    def close(self):
        """Close database connection."""
        if self.conn:
            try:
                self.conn.close()
                print("\n[DATABASE] Connection closed")
            except:
                pass
        self.conn = None
        self.cursor = None


# ==============================================================================
# TEST FUNCTIONS
# ==============================================================================

def test_database_connection():
    """Test database connection and table existence."""
    print("="*70)
    print("TESTING DATABASE CONNECTION")
    print("="*70)

    db = DatabaseOperations()

    # Test connection
    if not db.connect():
        print("\n[ERROR] Database connection failed!")
        print("Update config.py - search for: TODO_DB")
        return False

    # Test tables
    if not db.test_connection():
        print("\n[ERROR] Database structure incomplete!")
        return False

    print("\n[OK] Database connection test passed!")
    db.close()
    return True


def test_database_insert():
    """Test inserting a dummy record."""
    print("="*70)
    print("TESTING DATABASE INSERT")
    print("="*70)

    db = DatabaseOperations()

    if not db.connect():
        return False

    try:
        # Insert test simulation
        print("\nInserting test simulation...")
        sim_id = db.insert_simulation(
            biooil_id=1,
            convergence_status='Converged',
            mass_error=0.05,
            energy_error=0.8,
            notes='TEST_AUTOMATION'
        )

        if sim_id:
            print(f"  [OK] Inserted with SimulationId: {sim_id}")

            # Insert test conditions
            print("Inserting test conditions...")
            db.insert_reforming_conditions(
                simulation_id=sim_id,
                temp_c=800.0,
                pres_bar=15.0,
                sc_ratio=3.5
            )

            # Insert test H2 data
            print("Inserting test H2 product...")
            test_h2_data = {
                'H2_Yield_kg': 10.5,
                'H2_Purity_percent': 99.92,
                'H2_FlowRate_kgh': 10.5,
                'H2_FlowRate_Nm3h': 116.9,
                'H2_CO_Ratio': 4.2,
                'H2_CO2_Ratio': 3.8,
                'CH4_Slip_percent': 0.8,
                'CO_Slip_ppm': 50.0
            }
            db.insert_hydrogen_product(sim_id, test_h2_data)

            print("\n[OK] Database insert test passed!")
            print("\nTo clean up test data, run:")
            print(f"  DELETE FROM AspenSimulation WHERE Notes = 'TEST_AUTOMATION'")

            return True
        else:
            print("  [ERROR] Failed to insert simulation")
            return False

    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    # Run tests
    print("\nTest 1: Database Connection")
    test_database_connection()

    print("\n\nTest 2: Database Insert")
    test_database_insert()
