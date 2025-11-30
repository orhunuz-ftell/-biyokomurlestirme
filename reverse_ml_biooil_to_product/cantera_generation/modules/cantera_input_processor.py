"""
Input Processor for Cantera Data Generation System

This module handles:
- Loading simulation matrix from database
- Converting bio-oil composition to chemical species
- Calculating steam requirements
- Preparing Cantera-ready input dictionaries
"""

import pandas as pd
import pyodbc
from typing import Dict, Tuple
import sys
import os

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import cantera_config as config


class InputProcessor:
    """Process and prepare inputs for Cantera simulations"""

    def __init__(self):
        """Initialize input processor"""
        self.conn = None
        self.simulation_matrix = None

    def connect_database(self) -> bool:
        """
        Connect to SQL Server database

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.conn = pyodbc.connect(config.DB_CONNECTION_STRING)
            if config.VERBOSE:
                print("[OK] Database connection established")
            return True
        except Exception as e:
            print(f"[ERROR] Database connection failed: {e}")
            return False

    def load_simulation_matrix(self) -> pd.DataFrame:
        """
        Load simulation matrix from CSV file

        Returns:
            pd.DataFrame: Simulation matrix with 1,170 rows

        Columns:
            - BiooilId
            - aromatics, acids, alcohols, furans, phenols, aldehyde_ketone (mass %)
            - Temperature_C, Pressure_bar, SC_ratio
        """
        try:
            # Load from CSV file
            self.simulation_matrix = pd.read_csv(config.INPUT_MATRIX_FILE)

            # Rename columns to match expected names
            column_mapping = {
                'aldehyde&ketone': 'aldehyde_ketone',
                'ReformerTemperature_C': 'Temperature_C',
                'ReformerPressure_bar': 'Pressure_bar',
                'SteamToCarbonRatio': 'SC_ratio'
            }

            self.simulation_matrix = self.simulation_matrix.rename(columns=column_mapping)

            if config.VERBOSE:
                print(f"[OK] Loaded {len(self.simulation_matrix)} simulation scenarios")
                print(f"    Bio-oil compositions: {self.simulation_matrix['BiooilId'].nunique()}")
                print(f"    Process conditions: {len(self.simulation_matrix) // self.simulation_matrix['BiooilId'].nunique()}")

            return self.simulation_matrix

        except Exception as e:
            print(f"[ERROR] Failed to load simulation matrix: {e}")
            raise

    def prepare_bio_oil_composition(self, row: pd.Series) -> Dict[str, float]:
        """
        Convert bio-oil mass percentages to mole fractions for Cantera

        Args:
            row: DataFrame row with bio-oil composition (mass %)

        Returns:
            dict: Mole fractions of chemical species for Cantera

        Example:
            {'C7H8': 0.15, 'CH3COOH': 0.25, 'C2H5OH': 0.20, ...}
        """
        # Extract mass percentages
        mass_fractions = {
            'C7H8': row['aromatics'] / 100.0,       # Toluene
            'CH3COOH': row['acids'] / 100.0,        # Acetic acid
            'C2H5OH': row['alcohols'] / 100.0,      # Ethanol
            'C4H4O': row['furans'] / 100.0,         # Furan
            'C6H6O': row['phenols'] / 100.0,        # Phenol
            'C3H6O': row['aldehyde_ketone'] / 100.0 # Acetone
        }

        # Convert mass fractions to moles
        moles = {}
        for species, mass_frac in mass_fractions.items():
            if mass_frac > 0:
                mw = config.MOLECULAR_WEIGHTS[species]
                moles[species] = mass_frac / mw

        # Normalize to mole fractions
        total_moles = sum(moles.values())
        mole_fractions = {species: mole / total_moles
                         for species, mole in moles.items()}

        return mole_fractions

    def calculate_carbon_content(self, mole_fractions: Dict[str, float]) -> float:
        """
        Calculate total carbon moles in bio-oil

        Args:
            mole_fractions: Mole fractions of bio-oil species

        Returns:
            float: Moles of carbon per mole of bio-oil
        """
        carbon_moles = 0.0
        for species, mole_frac in mole_fractions.items():
            if species in config.CARBON_ATOMS:
                carbon_moles += mole_frac * config.CARBON_ATOMS[species]

        return carbon_moles

    def calculate_steam_requirement(self, mole_fractions: Dict[str, float],
                                   sc_ratio: float) -> float:
        """
        Calculate steam mole fraction based on S/C ratio

        Args:
            mole_fractions: Bio-oil mole fractions
            sc_ratio: Steam-to-carbon ratio

        Returns:
            float: Steam mole fraction to add to mixture
        """
        # Calculate carbon content
        carbon_moles = self.calculate_carbon_content(mole_fractions)

        # Steam moles required (per mole of bio-oil)
        steam_moles = carbon_moles * sc_ratio

        # Total moles (bio-oil + steam)
        total_moles = 1.0 + steam_moles

        # Steam mole fraction
        steam_mole_fraction = steam_moles / total_moles

        return steam_mole_fraction

    def create_cantera_input(self, row: pd.Series) -> Dict:
        """
        Create complete input dictionary for Cantera simulation

        Args:
            row: DataFrame row with bio-oil composition and process conditions

        Returns:
            dict: Complete Cantera input with composition, T, P

        Example:
            {
                'BiooilId': 1,
                'Temperature_C': 800,
                'Pressure_bar': 15,
                'SC_ratio': 4.0,
                'composition': {'C7H8': 0.10, 'CH3COOH': 0.15, ..., 'H2O': 0.40},
                'temperature_K': 1073.15,
                'pressure_Pa': 1500000
            }
        """
        # Get bio-oil mole fractions
        biooil_mole_fractions = self.prepare_bio_oil_composition(row)

        # Calculate steam requirement
        steam_mole_frac = self.calculate_steam_requirement(
            biooil_mole_fractions,
            row['SC_ratio']
        )

        # Create final composition including steam
        composition = {}

        # Bio-oil species (scaled by 1 - steam_mole_frac)
        for species, mole_frac in biooil_mole_fractions.items():
            composition[species] = mole_frac * (1.0 - steam_mole_frac)

        # Add steam
        composition['H2O'] = steam_mole_frac

        # Convert temperature and pressure to SI units
        temperature_K = row['Temperature_C'] + 273.15
        pressure_Pa = row['Pressure_bar'] * 1e5

        # Create input dictionary
        cantera_input = {
            'BiooilId': int(row['BiooilId']),
            'Temperature_C': float(row['Temperature_C']),
            'Pressure_bar': float(row['Pressure_bar']),
            'SC_ratio': float(row['SC_ratio']),
            'composition': composition,
            'temperature_K': temperature_K,
            'pressure_Pa': pressure_Pa
        }

        return cantera_input

    def process_all_scenarios(self) -> list:
        """
        Process all simulation scenarios

        Returns:
            list: List of Cantera input dictionaries (1,170 items)
        """
        if self.simulation_matrix is None:
            self.load_simulation_matrix()

        cantera_inputs = []

        for idx, row in self.simulation_matrix.iterrows():
            cantera_input = self.create_cantera_input(row)
            cantera_inputs.append(cantera_input)

            # Progress update
            if config.VERBOSE and (idx + 1) % config.PROGRESS_UPDATE_FREQ == 0:
                print(f"    Processed {idx + 1}/{len(self.simulation_matrix)} scenarios")

        if config.VERBOSE:
            print(f"[OK] All {len(cantera_inputs)} scenarios processed")

        return cantera_inputs

    def get_scenario_by_index(self, index: int) -> Dict:
        """
        Get single scenario by index (for testing)

        Args:
            index: Row index in simulation matrix

        Returns:
            dict: Cantera input dictionary
        """
        if self.simulation_matrix is None:
            self.load_simulation_matrix()

        row = self.simulation_matrix.iloc[index]
        return self.create_cantera_input(row)

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            if config.VERBOSE:
                print("[OK] Database connection closed")


# ==============================================================================
# TESTING AND VALIDATION
# ==============================================================================

def test_input_processor():
    """Test the input processor with first scenario"""
    print("\n" + "="*80)
    print("TESTING INPUT PROCESSOR")
    print("="*80)

    processor = InputProcessor()

    # Test 1: Database connection
    print("\nTest 1: Database Connection")
    if processor.connect_database():
        print("[PASS] Database connected")
    else:
        print("[FAIL] Database connection failed")
        return

    # Test 2: Load simulation matrix
    print("\nTest 2: Load Simulation Matrix")
    df = processor.load_simulation_matrix()
    print(f"[PASS] Loaded {len(df)} scenarios")
    print(f"    Columns: {list(df.columns)}")
    print(f"    First bio-oil ID: {df['BiooilId'].iloc[0]}")

    # Test 3: Process first scenario
    print("\nTest 3: Process First Scenario")
    first_scenario = processor.get_scenario_by_index(0)
    print("[PASS] First scenario processed:")
    print(f"    Bio-oil ID: {first_scenario['BiooilId']}")
    print(f"    Temperature: {first_scenario['Temperature_C']} °C ({first_scenario['temperature_K']} K)")
    print(f"    Pressure: {first_scenario['Pressure_bar']} bar ({first_scenario['pressure_Pa']} Pa)")
    print(f"    S/C ratio: {first_scenario['SC_ratio']}")
    print(f"    Composition (mole fractions):")
    for species, mole_frac in sorted(first_scenario['composition'].items()):
        print(f"        {species:12s}: {mole_frac:.4f}")

    # Test 4: Mass balance check
    print("\nTest 4: Mass Balance Check")
    total_mole_frac = sum(first_scenario['composition'].values())
    print(f"    Total mole fraction: {total_mole_frac:.6f}")
    if abs(total_mole_frac - 1.0) < 1e-6:
        print("[PASS] Mass balance OK")
    else:
        print(f"[WARNING] Mass balance error: {abs(total_mole_frac - 1.0):.2e}")

    processor.close()

    print("\n" + "="*80)
    print("INPUT PROCESSOR TEST COMPLETE")
    print("="*80)


if __name__ == "__main__":
    test_input_processor()
