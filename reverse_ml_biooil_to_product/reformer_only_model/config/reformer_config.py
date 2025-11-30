"""
Reformer-Only Model Configuration
==================================

Configuration parameters for bio-oil steam reforming equilibrium modeling.
This simplified model focuses ONLY on the reformer reactor, excluding
downstream water-gas shift and separation units.

Author: Orhun Uzdiyem
Date: November 30, 2025
"""

import os

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

DB_DRIVER = '{ODBC Driver 17 for SQL Server}'
DB_SERVER = r'DESKTOP-DRO84HP\SQLEXPRESS'
DB_DATABASE = 'BIOOIL'

# Connection string
DB_CONNECTION_STRING = (
    f"DRIVER={DB_DRIVER};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_DATABASE};"
    "Trusted_Connection=yes"
)

# ============================================================================
# CANTERA MECHANISM
# ============================================================================

# Use the custom bio-oil mechanism from cantera_generation
# Get absolute path to mechanism file
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_current_dir))
MECHANISM_PATH = os.path.join(
    _project_root,
    'cantera_generation',
    'config',
    'biooil_mechanism.yaml'
)

# Backup mechanisms if primary fails
BACKUP_MECHANISMS = [
    'gri30.yaml',  # GRI-Mech 3.0 (standard)
]

# ============================================================================
# BIO-OIL SPECIES MAPPING
# ============================================================================
# Maps bio-oil functional groups to Cantera species names

BIOOIL_SPECIES_MAP = {
    'aromatics': 'C7H8',        # Toluene
    'acids': 'CH3COOH',         # Acetic acid
    'alcohols': 'C2H5OH',       # Ethanol
    'furans': 'C4H4O',          # Furan
    'phenols': 'C6H6O',         # Phenol
    'aldehyde_ketone': 'C3H6O'  # Acetone (represents aldehydes & ketones)
}

# Molecular weights (g/mol) for mass/mole conversions
MOLECULAR_WEIGHTS = {
    'C7H8': 92.14,      # Toluene
    'CH3COOH': 60.05,   # Acetic acid
    'C2H5OH': 46.07,    # Ethanol
    'C4H4O': 68.07,     # Furan
    'C6H6O': 94.11,     # Phenol
    'C3H6O': 58.08,     # Acetone
    'H2O': 18.015,      # Water
}

# Stoichiometric coefficients (atoms per molecule)
STOICHIOMETRY = {
    'C7H8': {'C': 7, 'H': 8},
    'CH3COOH': {'C': 2, 'H': 4, 'O': 2},
    'C2H5OH': {'C': 2, 'H': 6, 'O': 1},
    'C4H4O': {'C': 4, 'H': 4, 'O': 1},
    'C6H6O': {'C': 6, 'H': 6, 'O': 1},
    'C3H6O': {'C': 3, 'H': 6, 'O': 1},
    'H2O': {'H': 2, 'O': 1},
}

# ============================================================================
# REFORMER OPERATING CONDITIONS
# ============================================================================

# Temperature range (°C)
TEMPERATURES_C = [650, 700, 750, 800, 850]  # 5 levels

# Pressure range (bar)
PRESSURES_BAR = [5, 15, 30]  # 3 levels

# Steam-to-carbon ratio range
SC_RATIOS = [2.0, 4.0, 6.0]  # 3 levels

# Total process conditions: 5 × 3 × 3 = 45 combinations

# ============================================================================
# PHYSICAL CONSTANTS
# ============================================================================

R_GAS_CONSTANT = 8.314  # J/(mol·K) - Universal gas constant
ATM_TO_PA = 101325      # Pa/atm - Conversion factor
BAR_TO_PA = 1e5         # Pa/bar - Conversion factor

# ============================================================================
# SIMULATION PARAMETERS
# ============================================================================

# Basis for calculations
BIOOIL_FEED_RATE_KG_H = 100.0  # kg/h bio-oil feed (basis)

# Convergence criteria
EQUILIBRIUM_TOL = 1e-6          # Tolerance for Gibbs minimization
MAX_ITERATIONS = 1000           # Max iterations for equilibrium solver

# ============================================================================
# OUTPUT SPECIES TO TRACK
# ============================================================================

# Major species (always present in significant amounts)
MAJOR_SPECIES = ['H2', 'CO', 'CO2', 'CH4', 'H2O']

# Minor species (may be present in trace amounts)
MINOR_SPECIES = ['C2H4', 'C2H6', 'C2H2', 'C3H6', 'N2', 'AR']

# Threshold for considering a species "present"
MIN_MOLE_FRACTION = 1e-10  # Species below this are ignored

# ============================================================================
# VALIDATION CRITERIA
# ============================================================================

# Mass balance tolerance
MASS_BALANCE_TOL = 0.01  # ±1% tolerance for mole fraction sum

# Expected composition ranges (mol%, for validation)
EXPECTED_RANGES = {
    'H2': (10, 70),     # Hydrogen typically 10-70%
    'CO': (0, 40),      # Carbon monoxide 0-40%
    'CO2': (0, 40),     # Carbon dioxide 0-40%
    'CH4': (0, 30),     # Methane 0-30%
    'H2O': (0, 60),     # Water 0-60% (unreacted steam)
}

# ============================================================================
# LOGGING AND OUTPUT
# ============================================================================

VERBOSE = True  # Print detailed progress messages
LOG_FILE = 'reformer_simulation.log'

# Progress reporting interval
REPORT_INTERVAL = 50  # Print progress every N simulations

# ============================================================================
# THERMODYNAMIC PROPERTY CALCULATIONS
# ============================================================================

# Reference state for enthalpy/entropy
REFERENCE_TEMP_K = 298.15  # K (25°C)
REFERENCE_PRESSURE_PA = 101325  # Pa (1 atm)

# ============================================================================
# PERFORMANCE METRICS CALCULATION
# ============================================================================

# Minimum mole fractions for ratio calculations (avoid division by zero)
MIN_FOR_RATIO = 1e-6

# Quality flags based on carbon/hydrogen recovery
CARBON_RECOVERY_WARNING = 95  # % - Warn if carbon recovery < 95%
HYDROGEN_RECOVERY_WARNING = 95  # % - Warn if hydrogen recovery < 95%

# ============================================================================
# DATA EXPORT SETTINGS
# ============================================================================

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')

# CSV export settings
CSV_SEPARATOR = ','
CSV_DECIMAL = '.'
CSV_ENCODING = 'utf-8'

# ============================================================================
# LITERATURE VALIDATION CASES
# ============================================================================

# Reference cases for validation against published data
VALIDATION_CASES = {
    'ethanol_800C': {
        'biooil_composition': {
            'aromatics': 0, 'acids': 0, 'alcohols': 100,
            'furans': 0, 'phenols': 0, 'aldehyde_ketone': 0
        },
        'temperature_C': 800,
        'pressure_bar': 1,
        'sc_ratio': 3,
        'expected_H2_molpercent': (55, 65),
        'expected_CO2_molpercent': (20, 30),
        'reference': 'Ethanol steam reforming literature'
    },
    'acetic_acid_700C': {
        'biooil_composition': {
            'aromatics': 0, 'acids': 100, 'alcohols': 0,
            'furans': 0, 'phenols': 0, 'aldehyde_ketone': 0
        },
        'temperature_C': 700,
        'pressure_bar': 1,
        'sc_ratio': 2,
        'expected_H2_molpercent': (45, 55),
        'expected_CO_molpercent': (5, 15),
        'reference': 'Acetic acid reforming literature'
    },
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_mechanism_path():
    """
    Get the path to the Cantera mechanism file.
    Returns absolute path, checking if file exists.
    """
    if os.path.exists(MECHANISM_PATH):
        return MECHANISM_PATH
    else:
        raise FileNotFoundError(
            f"Cantera mechanism not found at: {MECHANISM_PATH}\n"
            f"Please ensure cantera_generation is set up correctly."
        )


def validate_temperature(temp_C):
    """Check if temperature is within valid range."""
    return 600 <= temp_C <= 900


def validate_pressure(pressure_bar):
    """Check if pressure is within valid range."""
    return 1 <= pressure_bar <= 50


def validate_sc_ratio(sc_ratio):
    """Check if S/C ratio is within valid range."""
    return 1 <= sc_ratio <= 10


def create_output_dir():
    """Create output directory if it doesn't exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    return OUTPUT_DIR


# ============================================================================
# MODULE TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("REFORMER-ONLY MODEL CONFIGURATION")
    print("=" * 80)
    print()

    print("Database Configuration:")
    print(f"  Server: {DB_SERVER}")
    print(f"  Database: {DB_DATABASE}")
    print()

    print("Cantera Mechanism:")
    try:
        mech_path = get_mechanism_path()
        print(f"  Path: {mech_path}")
        print(f"  Exists: {os.path.exists(mech_path)}")
    except FileNotFoundError as e:
        print(f"  ERROR: {e}")
    print()

    print("Process Conditions:")
    print(f"  Temperatures: {TEMPERATURES_C} °C")
    print(f"  Pressures: {PRESSURES_BAR} bar")
    print(f"  S/C Ratios: {SC_RATIOS}")
    print(f"  Total combinations: {len(TEMPERATURES_C) * len(PRESSURES_BAR) * len(SC_RATIOS)}")
    print()

    print("Bio-oil Species Mapping:")
    for group, species in BIOOIL_SPECIES_MAP.items():
        print(f"  {group:20s} → {species}")
    print()

    print("Output Directory:")
    out_dir = create_output_dir()
    print(f"  {out_dir}")
    print(f"  Exists: {os.path.exists(out_dir)}")
    print()

    print("=" * 80)
    print("CONFIGURATION LOADED SUCCESSFULLY")
    print("=" * 80)
