"""
Configuration for Cantera Data Generation System
"""

import os

# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================

DB_SERVER = r'DESKTOP-DRO84HP\SQLEXPRESS'
DB_DATABASE = 'BIOOIL'
DB_DRIVER = '{SQL Server}'
DB_USE_WINDOWS_AUTH = True

DB_CONNECTION_STRING = (
    f"DRIVER={DB_DRIVER};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_DATABASE};"
    f"Trusted_Connection=yes"
)

# ==============================================================================
# FILE PATHS
# ==============================================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'biooil_reference_data')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')

INPUT_MATRIX_FILE = os.path.join(DATA_DIR, 'aspen_input_matrix.csv')

# ==============================================================================
# CANTERA SETTINGS
# ==============================================================================

# Chemical mechanism (Custom bio-oil mechanism based on GRI-Mech 3.0)
MECHANISM = os.path.join(os.path.dirname(__file__), 'biooil_mechanism.yaml')

# Alternative mechanisms if needed
BACKUP_MECHANISMS = ['gri30.yaml', 'gri30.xml', 'gri30.cti']

# ==============================================================================
# BIO-OIL COMPONENT MAPPING
# ==============================================================================

# Map bio-oil components to chemical species
BIOOIL_SPECIES_MAP = {
    'aromatics': 'C7H8',        # Toluene
    'acids': 'CH3COOH',         # Acetic acid (will use C2H4O2)
    'alcohols': 'C2H5OH',       # Ethanol
    'furans': 'C4H4O',          # Furan
    'phenols': 'C6H6O',         # Phenol
    'aldehyde_ketone': 'C3H6O'  # Acetone
}

# Molecular weights (g/mol)
MOLECULAR_WEIGHTS = {
    'C7H8': 92.14,      # Toluene
    'CH3COOH': 60.05,   # Acetic acid
    'C2H5OH': 46.07,    # Ethanol
    'C4H4O': 68.07,     # Furan
    'C6H6O': 94.11,     # Phenol
    'C3H6O': 58.08,     # Acetone
    'H2O': 18.015,      # Water
    'H2': 2.016,        # Hydrogen
    'CO': 28.01,        # Carbon monoxide
    'CO2': 44.01,       # Carbon dioxide
    'CH4': 16.04,       # Methane
    'N2': 28.01         # Nitrogen
}

# Carbon atoms per molecule
CARBON_ATOMS = {
    'C7H8': 7,          # Toluene
    'CH3COOH': 2,       # Acetic acid
    'C2H5OH': 2,        # Ethanol
    'C4H4O': 4,         # Furan
    'C6H6O': 6,         # Phenol
    'C3H6O': 3          # Acetone
}

# ==============================================================================
# PROCESS PARAMETERS
# ==============================================================================

# Fixed downstream temperatures
HTS_TEMPERATURE_C = 370.0   # High-temperature shift
LTS_TEMPERATURE_C = 210.0   # Low-temperature shift
FLASH_TEMPERATURE_C = 40.0  # Flash separation
PSA_PRESSURE_BAR = 25.0     # PSA operating pressure

# Separation efficiencies
CO2_REMOVAL_EFFICIENCY = 0.95   # 95% CO2 removal
PSA_H2_RECOVERY = 0.88          # 88% H2 recovery
PSA_H2_PURITY = 0.999           # 99.9% H2 purity

# Component losses in CO2 removal
CO2_REMOVAL_LOSSES = {
    'H2': 0.01,     # 1% H2 loss
    'CO': 0.01,     # 1% CO loss
    'CH4': 0.005    # 0.5% CH4 loss
}

# ==============================================================================
# VALIDATION THRESHOLDS
# ==============================================================================

# Mass balance error (%)
MAX_MASS_BALANCE_ERROR = 0.1

# Energy balance error (%)
MAX_ENERGY_BALANCE_ERROR = 1.0

# Physical constraints
H2_YIELD_MIN = 5.0      # kg per 100 kg bio-oil
H2_YIELD_MAX = 15.0
CARBON_CONV_MIN = 75.0  # %
CARBON_CONV_MAX = 100.0
ENERGY_EFF_MIN = 50.0   # %
ENERGY_EFF_MAX = 80.0

# ==============================================================================
# THERMODYNAMIC DATA
# ==============================================================================

# Higher heating values (MJ/kg)
HHV = {
    'H2': 141.8,
    'CO': 10.1,
    'CH4': 55.5,
    'biooil': 18.5  # Typical bio-oil HHV
}

# ==============================================================================
# LOGGING
# ==============================================================================

LOG_FILE = os.path.join(OUTPUT_DIR, 'cantera_generation.log')
VERBOSE = True
PROGRESS_UPDATE_FREQ = 10  # Update every N simulations
