"""
==============================================================================
ASPEN AUTOMATION - CONNECTION TESTING SCRIPT
==============================================================================
Purpose: Test all components before running full automation
Author: Orhun Uzdiyem
Date: 2025-11-16

Tests:
1. Python packages installed
2. File paths exist
3. Aspen Plus connection
4. Database connection
5. Single simulation run
6. Database insert/query
==============================================================================
"""

import sys
import os

print("="*70)
print("ASPEN AUTOMATION - SYSTEM TEST")
print("="*70)
print()

# ==============================================================================
# TEST 1: Python Packages
# ==============================================================================

print("TEST 1: Checking Python packages...")
print("-"*70)

required_packages = {
    'pandas': 'pandas',
    'numpy': 'numpy',
    'pyodbc': 'pyodbc',
    'win32com.client': 'pywin32'
}

missing_packages = []

for module_name, package_name in required_packages.items():
    try:
        __import__(module_name)
        print(f"  [OK] {package_name}")
    except ImportError:
        print(f"  [MISSING] {package_name}")
        missing_packages.append(package_name)

if missing_packages:
    print(f"\n[ERROR] Missing packages: {', '.join(missing_packages)}")
    print("\nInstall with:")
    print(f"  pip install {' '.join(missing_packages)}")
    sys.exit(1)
else:
    print("\n[OK] All required packages installed")

print()

# ==============================================================================
# TEST 2: Configuration and File Paths
# ==============================================================================

print("TEST 2: Checking configuration...")
print("-"*70)

try:
    import config
    print(f"  [OK] Configuration loaded")
    print(f"       Base directory: {config.BASE_DIR}")
    print(f"       Batch size: {config.BATCH_SIZE}")
    print(f"       Database server: {config.DB_SERVER}")

    # Check if database server needs updating
    if 'TODO_DB' in config.DB_SERVER or 'DESKTOP-DRO84HP' in config.DB_SERVER:
        print(f"\n  [WARNING] Database server may need updating!")
        print(f"            Current: {config.DB_SERVER}")
        print(f"            Search for 'TODO_DB' in config.py to update")

    # Validate config
    issues = config.validate_config()
    if issues:
        print(f"\n  [WARNING] Configuration issues found:")
        for issue in issues:
            print(f"            - {issue}")
    else:
        print(f"\n  [OK] Configuration validated")

except Exception as e:
    print(f"  [ERROR] Failed to load configuration: {e}")
    sys.exit(1)

print()

# ==============================================================================
# TEST 3: Aspen Plus Connection
# ==============================================================================

print("TEST 3: Testing Aspen Plus connection...")
print("-"*70)

try:
    from aspen_interface import AspenInterface

    aspen = AspenInterface()

    # Test connection
    if aspen.connect():
        print("  [OK] Connected to Aspen Plus")

        # Test model loading
        if os.path.exists(config.ASPEN_MODEL_PATH):
            print(f"  [OK] Model file found: {config.ASPEN_MODEL_PATH}")

            if aspen.load_model():
                print("  [OK] Model loaded successfully")
            else:
                print("  [ERROR] Failed to load model")
                print("          Make sure model file is valid Aspen .bkp file")
        else:
            print(f"  [WARNING] Model file not found: {config.ASPEN_MODEL_PATH}")
            print(f"            You need to build the Aspen model first")
            print(f"            See: docs/ASPEN_SIMULATION_GUIDE.md")

        aspen.close()
    else:
        print("  [ERROR] Failed to connect to Aspen Plus")
        print("          Possible solutions:")
        print("          1. Ensure Aspen Plus V8.8 is installed")
        print("          2. Run Python as administrator")
        print("          3. Check Aspen license is active")
        sys.exit(1)

except Exception as e:
    print(f"  [ERROR] Aspen test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# ==============================================================================
# TEST 4: Database Connection
# ==============================================================================

print("TEST 4: Testing database connection...")
print("-"*70)

try:
    from database_operations import DatabaseOperations

    db = DatabaseOperations()

    # Test connection
    if db.connect():
        print("  [OK] Connected to database")

        # Test table existence
        if db.test_connection():
            print("  [OK] All required tables exist")
        else:
            print("  [ERROR] Database structure incomplete")
            print("          Run database creation scripts first:")
            print("          - database/01_create_tables.sql")
            print("          - database/02_create_indexes.sql")
            print("          - database/03_create_views.sql")
            sys.exit(1)

        db.close()
    else:
        print("  [ERROR] Failed to connect to database")
        print("          Check config.py - search for: TODO_DB")
        print(f"          Current server: {config.DB_SERVER}")
        sys.exit(1)

except Exception as e:
    print(f"  [ERROR] Database test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# ==============================================================================
# TEST 5: Single Simulation Run (Optional - requires model)
# ==============================================================================

print("TEST 5: Testing single simulation (optional)...")
print("-"*70)

if os.path.exists(config.ASPEN_MODEL_PATH):
    print("  Aspen model found. Testing single simulation...")

    try:
        from aspen_interface import AspenInterface

        aspen = AspenInterface()

        if aspen.connect() and aspen.load_model():
            # Test composition
            test_comp = {
                'aromatics': 0.3287,
                'acids': 0.1964,
                'alcohols': 0.0630,
                'furans': 0.0274,
                'phenols': 0.0963,
                'aldehyde_ketone': 0.0653
            }

            print("  Setting test composition...")
            aspen.set_biooil_composition(test_comp)

            print("  Setting test conditions (800°C, 15 bar, S/C=3.5)...")
            aspen.set_process_conditions(800.0, 15.0, 3.5)

            print("  Running simulation...")
            if aspen.run_simulation():
                print(f"  [OK] Simulation converged in {aspen.get_simulation_time():.1f}s")

                # Extract results
                h2_data = aspen.extract_h2_properties()
                if h2_data:
                    print(f"       H2 Yield: {h2_data['H2_Yield_kg']:.2f} kg")
                    print(f"       H2 Purity: {h2_data['H2_Purity_percent']:.2f}%")
                    print("  [OK] Results extracted successfully")
                else:
                    print("  [WARNING] Could not extract results")
            else:
                print("  [WARNING] Simulation did not converge")
                print("            This is OK for testing - may need model tuning")

            aspen.close()
        else:
            print("  [SKIPPED] Could not load Aspen model")

    except Exception as e:
        print(f"  [WARNING] Simulation test failed: {e}")
        print("            This may be OK - model may need adjustments")
else:
    print("  [SKIPPED] Aspen model not found")
    print(f"            Create model first: {config.ASPEN_MODEL_PATH}")

print()

# ==============================================================================
# TEST 6: Database Insert Test
# ==============================================================================

print("TEST 6: Testing database insert...")
print("-"*70)

try:
    from database_operations import DatabaseOperations

    db = DatabaseOperations()

    if db.connect():
        # Insert test record
        print("  Inserting test simulation...")
        sim_id = db.insert_simulation(
            biooil_id=1,
            convergence_status='Test',
            mass_error=0.05,
            energy_error=0.8,
            notes='TEST_CONNECTION_SCRIPT'
        )

        if sim_id:
            print(f"  [OK] Test record inserted (SimulationId: {sim_id})")

            # Clean up test record
            print("  Cleaning up test record...")
            db.cursor.execute(
                "DELETE FROM AspenSimulation WHERE Notes = 'TEST_CONNECTION_SCRIPT'"
            )
            db.conn.commit()
            print("  [OK] Test record removed")
        else:
            print("  [ERROR] Failed to insert test record")

        db.close()
    else:
        print("  [ERROR] Could not connect to database")

except Exception as e:
    print(f"  [ERROR] Database insert test failed: {e}")
    import traceback
    traceback.print_exc()

print()

# ==============================================================================
# FINAL SUMMARY
# ==============================================================================

print("="*70)
print("TEST SUMMARY")
print("="*70)
print()
print("System is ready for automation if all tests above passed.")
print()
print("Next steps:")
print("  1. If model not found: Build Aspen model using guide")
print("     (docs/ASPEN_SIMULATION_GUIDE.md)")
print()
print("  2. If database server needs updating:")
print("     - Open config.py")
print("     - Search for: TODO_DB")
print("     - Update DB_SERVER variable")
print()
print("  3. Test with 5 simulations before full run:")
print("     - Modify config.py: BATCH_SIZE = 5")
print("     - Run: python run_automation.py")
print("     - Review results")
print()
print("  4. Run full automation:")
print("     - Modify config.py: BATCH_SIZE = 100")
print("     - Run: python run_automation.py")
print("     - Can run overnight (3-6 hours total)")
print()
print("="*70)
print()
print("To run automation now:")
print("  python run_automation.py")
print()
print("="*70)
