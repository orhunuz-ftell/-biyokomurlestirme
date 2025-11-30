"""
==============================================================================
ASPEN AUTOMATION - CONFIGURATION FILE
==============================================================================
Purpose: Central configuration for all automation scripts
Author: Orhun Uzdiyem
Date: 2025-11-16

IMPORTANT: Update paths and database settings for Aspen computer!
==============================================================================
"""

import os

# ==============================================================================
# FILE PATHS (Update these for Aspen computer)
# ==============================================================================

# Base directory (update if different)
BASE_DIR = r"C:\BioOilProject"

# Aspen model file
ASPEN_MODEL_PATH = os.path.join(BASE_DIR, "aspen_model", "biooil_reforming_base.bkp")

# Input data file (1,170 simulation scenarios)
INPUT_DATA_PATH = os.path.join(BASE_DIR, "data", "aspen_input_matrix.csv")

# Log directory (auto-created if doesn't exist)
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Progress tracking file (stores last completed simulation)
PROGRESS_FILE = os.path.join(BASE_DIR, "logs", "progress.json")

# ==============================================================================
# DATABASE CONNECTION (*** UPDATE SERVER NAME ***)
# ==============================================================================

# TODO_DB: Change SERVER name to match Aspen computer's SQL Server instance
# Current: DESKTOP-DRO84HP\SQLEXPRESS
# Update to your Aspen computer's server name
DB_SERVER = r'DESKTOP-DRO84HP\SQLEXPRESS'  # TODO_DB: CHANGE THIS!

DB_DATABASE = 'BIOOIL'
DB_DRIVER = '{SQL Server}'

# Authentication method
DB_USE_WINDOWS_AUTH = True  # Set to False if using SQL Server authentication

# If using SQL Server authentication (not Windows auth), set these:
DB_USERNAME = ''  # Leave empty if using Windows auth
DB_PASSWORD = ''  # Leave empty if using Windows auth

# Connection string (automatically built from above)
if DB_USE_WINDOWS_AUTH:
    DB_CONNECTION_STRING = (
        f"DRIVER={DB_DRIVER};"
        f"SERVER={DB_SERVER};"  # TODO_DB: This uses DB_SERVER above
        f"DATABASE={DB_DATABASE};"
        f"Trusted_Connection=yes"
    )
else:
    DB_CONNECTION_STRING = (
        f"DRIVER={DB_DRIVER};"
        f"SERVER={DB_SERVER};"  # TODO_DB: This uses DB_SERVER above
        f"DATABASE={DB_DATABASE};"
        f"UID={DB_USERNAME};"
        f"PWD={DB_PASSWORD}"
    )

# ==============================================================================
# ASPEN PLUS SETTINGS
# ==============================================================================

# Aspen Plus version (V8.8)
# Try these dispatch strings in order until one works:
ASPEN_DISPATCH_OPTIONS = [
    'Apwn.Document.29.0',  # V8.8 (most likely)
    'Apwn.Document.28.0',  # Alternative
    'Apwn.Document',       # Generic (fallback)
]

# Maximum iterations for convergence
ASPEN_MAX_ITERATIONS = 100

# Convergence timeout (seconds)
ASPEN_TIMEOUT = 300  # 5 minutes per simulation

# ==============================================================================
# BATCH MODE SETTINGS
# ==============================================================================

# Number of simulations to run per batch
BATCH_SIZE = 100

# Pause between batches for review?
PAUSE_BETWEEN_BATCHES = True

# Auto-continue after pause (seconds, 0 = wait for user input)
AUTO_CONTINUE_DELAY = 0  # 0 = manual, 30 = auto after 30 seconds

# ==============================================================================
# PROCESS PARAMETERS (Reference - not changed during automation)
# ==============================================================================

# Reformer temperature range (°C)
REFORMER_TEMP_MIN = 650
REFORMER_TEMP_MAX = 850

# Reformer pressure range (bar)
REFORMER_PRES_MIN = 5
REFORMER_PRES_MAX = 30

# Steam-to-carbon ratio range
SC_RATIO_MIN = 2.0
SC_RATIO_MAX = 6.0

# ==============================================================================
# VALIDATION THRESHOLDS
# ==============================================================================

# Mass balance error threshold (%)
MAX_MASS_BALANCE_ERROR = 0.1

# Energy balance error threshold (%)
MAX_ENERGY_BALANCE_ERROR = 1.0

# Minimum H2 purity expected (%)
MIN_H2_PURITY = 98.0

# Maximum CO contamination (ppm)
MAX_CO_PPM = 10000

# ==============================================================================
# ASPEN TREE PATHS (For V8.8)
# ==============================================================================

# These paths work for most Aspen versions, but may need adjustment
# Use Aspen's Variable Explorer to verify if needed

# Input paths (setting values)
PATHS_INPUT = {
    'reformer_temp': r"\Data\Blocks\REFORMER\Input\TEMP",
    'reformer_pres': r"\Data\Blocks\REFORMER\Input\PRES",
    'steam_flow': r"\Data\Streams\STEAM\Input\TOTFLOW\MIXED",
    'biooil_flow': r"\Data\Streams\BIOOIL\Input\TOTFLOW\MIXED",
    'hts_temp': r"\Data\Blocks\HTS\Input\TEMP",
    'lts_temp': r"\Data\Blocks\LTS\Input\TEMP",
    'psa_pres': r"\Data\Blocks\PSA\Input\PRES",
}

# Bio-oil composition paths (RYIELD block)
PATHS_BIOOIL_COMP = {
    'aromatics': r"\Data\Blocks\BIOOILFEED\Input\YIELD\MIXED\TOLUENE",
    'acids': r"\Data\Blocks\BIOOILFEED\Input\YIELD\MIXED\ACETI-01",
    'alcohols': r"\Data\Blocks\BIOOILFEED\Input\YIELD\MIXED\ETHANOL",
    'furans': r"\Data\Blocks\BIOOILFEED\Input\YIELD\MIXED\FURAN",
    'phenols': r"\Data\Blocks\BIOOILFEED\Input\YIELD\MIXED\PHENOL",
    'aldehyde_ketone': r"\Data\Blocks\BIOOILFEED\Input\YIELD\MIXED\ACET-01",
}

# Output paths (extracting results)
PATHS_OUTPUT = {
    'convergence_status': r"\Data\Results Summary\Run-Status\Output\RUNID",
    'h2_mass_flow': r"\Data\Streams\H2PROD\Output\MASSFLMX\MIXED",
    'h2_mole_flow': r"\Data\Streams\H2PROD\Output\MOLEFLMX\MIXED",
    'h2_temp': r"\Data\Streams\H2PROD\Output\TEMP_OUT\MIXED",
    'h2_pres': r"\Data\Streams\H2PROD\Output\PRES_OUT\MIXED",
    'reformer_duty': r"\Data\Blocks\REFORMER\Output\QCALC",
    'preheat_duty': r"\Data\Blocks\PREHEAT\Output\QCALC",
}

# Component mole fractions in H2 product
PATHS_H2_COMPOSITION = {
    'H2': r"\Data\Streams\H2PROD\Output\MOLEFRAC\MIXED\H2",
    'CO': r"\Data\Streams\H2PROD\Output\MOLEFRAC\MIXED\CO",
    'CO2': r"\Data\Streams\H2PROD\Output\MOLEFRAC\MIXED\CO2",
    'CH4': r"\Data\Streams\H2PROD\Output\MOLEFRAC\MIXED\CH4",
}

# Syngas composition at different locations
SYNGAS_STREAMS = {
    'Reformer_Out': 'SYNGAS1',
    'HTS_Out': 'SYNGAS2',
    'LTS_Out': 'SYNGAS3',
    'PSA_In': 'SYNGAS4',
}

SYNGAS_COMPONENTS = ['H2', 'CO', 'CO2', 'CH4', 'H2O', 'N2']

# ==============================================================================
# LOGGING SETTINGS
# ==============================================================================

# Log file names
LOG_FILE_MAIN = os.path.join(LOG_DIR, "automation_log.txt")
LOG_FILE_ERROR = os.path.join(LOG_DIR, "error_log.txt")
LOG_FILE_RESULTS = os.path.join(LOG_DIR, "results_summary.csv")

# Log level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL = 'INFO'

# ==============================================================================
# DISPLAY SETTINGS
# ==============================================================================

# Show detailed progress for each simulation?
VERBOSE_MODE = True

# Update frequency (show progress every N simulations)
PROGRESS_UPDATE_FREQ = 1

# Show warnings?
SHOW_WARNINGS = True

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def validate_config():
    """Validate configuration before starting automation."""
    issues = []

    # Check if Aspen model file exists
    if not os.path.exists(ASPEN_MODEL_PATH):
        issues.append(f"Aspen model file not found: {ASPEN_MODEL_PATH}")

    # Check if input data file exists
    if not os.path.exists(INPUT_DATA_PATH):
        issues.append(f"Input data file not found: {INPUT_DATA_PATH}")

    # Create log directory if doesn't exist
    if not os.path.exists(LOG_DIR):
        try:
            os.makedirs(LOG_DIR)
            print(f"Created log directory: {LOG_DIR}")
        except Exception as e:
            issues.append(f"Cannot create log directory: {e}")

    # Check database connection string
    if 'TODO_DB' in DB_SERVER or 'DESKTOP-DRO84HP' in DB_SERVER:
        print("\n[WARNING] Database server name may need updating!")
        print(f"Current: {DB_SERVER}")
        print("Search for 'TODO_DB' in config.py to update\n")

    return issues


def get_db_connection_string():
    """Get database connection string (for external use)."""
    return DB_CONNECTION_STRING


def print_config_summary():
    """Print configuration summary."""
    print("="*70)
    print("CONFIGURATION SUMMARY")
    print("="*70)
    print(f"Aspen Model:     {ASPEN_MODEL_PATH}")
    print(f"Input Data:      {INPUT_DATA_PATH}")
    print(f"Log Directory:   {LOG_DIR}")
    print(f"Database Server: {DB_SERVER}")  # TODO_DB
    print(f"Database Name:   {DB_DATABASE}")
    print(f"Batch Size:      {BATCH_SIZE} simulations")
    print(f"Pause Between:   {'Yes' if PAUSE_BETWEEN_BATCHES else 'No'}")
    print("="*70)


# ==============================================================================
# LOAD TEST
# ==============================================================================

if __name__ == "__main__":
    print("Testing configuration...")
    print_config_summary()

    issues = validate_config()

    if issues:
        print("\n[ERROR] Configuration issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n[OK] Configuration validated successfully!")

    print("\nTo update database server:")
    print("  1. Open config.py")
    print("  2. Press Ctrl+F and search for: TODO_DB")
    print("  3. Update DB_SERVER variable")
