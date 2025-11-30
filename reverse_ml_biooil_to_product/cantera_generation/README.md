# Cantera Data Generation System

Generate hydrogen production simulation data using Cantera thermodynamic calculations.

## Overview

This system generates 1,170 simulation scenarios (26 bio-oil compositions × 45 process conditions) for steam reforming of bio-oil to produce hydrogen. Results are stored in SQL Server database for machine learning model training.

**Scientific Validity**: Uses Gibbs free energy minimization (same thermodynamic principle as Aspen Plus). Expected accuracy: 85-92% vs commercial process simulators.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- `cantera` - Thermodynamic calculator (includes GRI-Mech 3.0)
- `pyodbc` - SQL Server database connectivity
- `pandas` - Data processing
- `numpy` - Numerical operations

### 2. Verify Database Connection

Ensure SQL Server is running and accessible:
- Server: `DESKTOP-DRO84HP\SQLEXPRESS`
- Database: `BIOOIL`
- Authentication: Windows Authentication

Connection string is configured in `config/cantera_config.py`.

### 3. Run Test Mode (Recommended First)

Test with first 10 simulations:

```bash
python generate_data_cantera.py --test
```

This will:
- Load 10 scenarios from database
- Run Cantera equilibrium calculations
- Apply separation models (flash, CO₂ removal, PSA)
- Calculate 16 ML features
- Validate results
- Write to database

**Expected time**: 1-2 minutes

### 4. Run Full Generation

Generate all 1,170 simulations:

```bash
python generate_data_cantera.py
```

**Expected time**: 10-30 minutes (depends on system)

### 5. Resume If Interrupted

If the run is interrupted, resume from last index:

```bash
python generate_data_cantera.py --start 500
```

## System Architecture

### Process Flow

```
Bio-oil + Steam → [REFORMER] → Syngas
                      ↓
               [HTS Reactor] (370°C)
                      ↓
               [LTS Reactor] (210°C)
                      ↓
                  [FLASH] (40°C) → Water
                      ↓
              [CO₂ REMOVAL] (95%) → CO₂
                      ↓
                [PSA] (25 bar) → Tail Gas
                      ↓
                Pure H₂ (99.9%)
```

### Core Modules

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| `cantera_input_processor.py` | Load scenarios, prepare inputs | `load_simulation_matrix()`, `create_cantera_input()` |
| `cantera_equilibrium.py` | Gibbs minimization calculations | `reformer_equilibrium()`, `wgs_equilibrium()` |
| `separation_models.py` | Downstream separations | `flash_separation()`, `co2_removal()`, `psa_separation()` |
| `property_calculator.py` | Calculate ML features | `calculate_ml_features()` (16 features) |
| `database_writer.py` | Write to SQL Server | `write_complete_simulation()` (5 tables) |
| `validation.py` | 5-level validation | `validate_complete_simulation()` |

### Database Tables

Results written to 5 tables:

1. **AspenSimulation** - Master record (SimulationId, BiooilId, conditions)
2. **ReformingConditions** - Process parameters (T, P, S/C, catalysts)
3. **HydrogenProduct** - 16 ML input features (H₂ yield, purity, etc.)
4. **SyngasComposition** - Gas composition at 4 locations
5. **EnergyBalance** - Energy metrics (efficiency, heat duties)

## Command Line Options

```bash
python generate_data_cantera.py [OPTIONS]

Options:
  --test              Run test mode (first 10 simulations only)
  --start INDEX       Starting index for resume (default: 0)
  --max COUNT         Maximum simulations to run (default: all)
  -h, --help          Show help message
```

**Examples:**

```bash
# Test mode
python generate_data_cantera.py --test

# Full run
python generate_data_cantera.py

# Resume from index 500
python generate_data_cantera.py --start 500

# Run 100 simulations starting from index 200
python generate_data_cantera.py --start 200 --max 100
```

## Configuration

Edit `config/cantera_config.py` to customize:

### Database Settings
```python
DB_SERVER = r'DESKTOP-DRO84HP\SQLEXPRESS'  # Change if different
DB_DATABASE = 'BIOOIL'
```

### Process Parameters
```python
HTS_TEMPERATURE_C = 370.0   # High-temperature shift
LTS_TEMPERATURE_C = 210.0   # Low-temperature shift
PSA_PRESSURE_BAR = 25.0     # PSA operating pressure
CO2_REMOVAL_EFFICIENCY = 0.95  # 95% CO₂ removal
PSA_H2_RECOVERY = 0.88         # 88% H₂ recovery
PSA_H2_PURITY = 0.999          # 99.9% purity
```

### Validation Thresholds
```python
H2_YIELD_MIN = 5.0      # kg per 100 kg bio-oil
H2_YIELD_MAX = 15.0
CARBON_CONV_MIN = 75.0  # %
ENERGY_EFF_MIN = 50.0   # %
```

## Testing Individual Modules

Each module has built-in tests:

```bash
# Test input processor
python modules/cantera_input_processor.py

# Test equilibrium calculator
python modules/cantera_equilibrium.py

# Test separation models
python modules/separation_models.py

# Test property calculator
python modules/property_calculator.py

# Test database writer
python modules/database_writer.py

# Test validation engine
python modules/validation.py
```

## Output and Monitoring

### Progress Messages

```
================================================================================
CANTERA DATA GENERATION SYSTEM
================================================================================
Version: 1.0.0
Date: 2025-11-30 14:30:00
Database: DESKTOP-DRO84HP\SQLEXPRESS / BIOOIL
================================================================================

Initializing modules...
[OK] All modules initialized

Loading simulation matrix from database...
[OK] Loaded 1170 simulation scenarios
    Bio-oil compositions: 26
    Process conditions: 45

Total scenarios to process: 1170
Starting from index: 0

Existing Cantera simulations in database: 0

--------------------------------------------------------------------------------
Progress: 0/1170 (0.0%)
Successful: 0, Failed: 0, Skipped: 0
--------------------------------------------------------------------------------

[0] Bio-oil 1, T=650°C, P=5bar, S/C=2.0
[OK] Simulation written (ID=1)
...
```

### Final Report

```
================================================================================
FINAL REPORT
================================================================================

Total scenarios: 1170
Successful: 1165
Failed: 0
Skipped: 5
Validation warnings: 12

Elapsed time: 1254.3 seconds (20.9 minutes)
Average time per simulation: 1.08 seconds
Success rate: 99.6%

================================================================================

Total Cantera simulations in database: 1165
Target: 1,170
Remaining: 5

================================================================================
```

## Validation

5-level validation system:

1. **Mass & Energy Balance** - Mole fractions sum to 1.0, energy conserved
2. **Physical Ranges** - H₂ yield (5-15 kg), efficiency (50-80%), etc.
3. **Thermodynamic Feasibility** - H₂ increases through WGS, CO decreases
4. **Statistical Consistency** - Values within literature ranges
5. **ML Readiness** - All 16 features present, no NaN/Inf

Failed validations are flagged in database but still saved for review.

## Troubleshooting

### Issue: Database Connection Failed

**Solution**: Check SQL Server is running and connection string is correct.

```bash
# Test connection
sqlcmd -S DESKTOP-DRO84HP\SQLEXPRESS -d BIOOIL -E
```

### Issue: Cantera Module Not Found

**Solution**: Install Cantera properly.

```bash
pip uninstall cantera
pip install cantera
```

### Issue: GRI-Mech 3.0 Not Found

**Solution**: Cantera should include GRI-Mech. Check installation:

```python
import cantera as ct
gas = ct.Solution('gri30.yaml')  # Should work
```

### Issue: Validation Warnings

**Solution**: Validation warnings don't stop execution. Check:
- Are values physically realistic?
- Are they within expected ranges?
- Review `config/cantera_config.py` thresholds if needed

### Issue: Slow Performance

**Solution**:
- Run in test mode first to check speed
- Expected: 1-2 seconds per simulation
- Check database connection speed
- Reduce `VERBOSE` logging in config

## Expected Results

### Typical H₂ Product Properties

| Property | Typical Range |
|----------|---------------|
| H₂ Yield | 8-12 kg/100kg bio-oil |
| H₂ Purity | 99.9% |
| Carbon Conversion | 85-95% |
| Energy Efficiency | 60-70% |
| H₂/CO Ratio | 15-25 |

### Syngas Composition (after LTS)

| Component | Typical Range |
|-----------|---------------|
| H₂ | 55-65% |
| CO | 2-5% |
| CO₂ | 25-30% |
| CH₄ | 3-7% |

## For Thesis Documentation

This system uses:
- **Cantera v3.0+** - Open-source chemical kinetics and thermodynamics
- **GRI-Mech 3.0** - Validated chemical mechanism (53 species, 325 reactions)
- **Gibbs Free Energy Minimization** - Standard thermodynamic equilibrium method
- **Literature-Based Separation Models** - PSA recovery (88%), purity (99.9%)

**Cite as:**
```
Goodwin, D. G., Moffat, H. K., Schoegl, I., Speth, R. L., & Weber, B. W. (2023).
Cantera: An object-oriented software toolkit for chemical kinetics, thermodynamics,
and transport processes. https://www.cantera.org. Version 3.0.0.
```

## License

This code is part of a PhD thesis project. See main repository for license information.

## Contact

**Author**: Orhun Uzdiyem
**Institution**: [Your University]
**Project**: Biomass Pyrolysis Bio-oil Production and Reverse ML Prediction
**Version**: 1.0.0
**Date**: November 2025
