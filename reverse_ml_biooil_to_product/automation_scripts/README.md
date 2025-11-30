# Aspen Automation Scripts

Python automation scripts for running 1,170 bio-oil steam reforming simulations in Aspen Plus V8.8.

---

## Files Overview

### Configuration
- **`config.py`** - Central configuration file
  - Database connection settings (**TODO_DB: Update server name!**)
  - File paths
  - Batch size settings
  - Aspen tree paths
  - Process parameters

### Core Modules
- **`aspen_interface.py`** - Aspen Plus COM automation
  - Connect to Aspen V8.8
  - Set bio-oil composition (6 components)
  - Set process conditions (T, P, S/C)
  - Run simulations
  - Extract H₂ properties, syngas composition, energy data

- **`database_operations.py`** - SQL Server database operations
  - Connect to BIOOIL database
  - Insert simulation results into 5 tables
  - Track progress for resume capability
  - Query statistics

### Main Scripts
- **`run_automation.py`** - Main automation script with batch mode
  - Run all 1,170 simulations
  - Batch mode: run 100, pause, review, continue
  - Resume capability (skip completed)
  - Error handling and logging
  - Progress tracking

- **`test_connection.py`** - System testing script
  - Test Python packages
  - Test Aspen connection
  - Test database connection
  - Test single simulation
  - **Run this first before full automation!**

### Supporting Files
- **`requirements.txt`** - Python package dependencies

---

## Quick Start Guide

### 1. Copy Files to Aspen Computer

Copy these files/folders to Aspen computer:

```
From development computer → To Aspen computer:
  automation_scripts/          → C:\BioOilProject\automation_scripts\
  data/aspen_input_matrix.csv  → C:\BioOilProject\data\
  aspen_simulations/*.bkp      → C:\BioOilProject\aspen_model\
  docs/ASPEN_*.md              → C:\BioOilProject\docs\
```

### 2. Setup on Aspen Computer

**Install Python packages:**
```bash
cd C:\BioOilProject\automation_scripts
pip install -r requirements.txt
```

**Update configuration:**
1. Open `config.py`
2. Press **Ctrl+F** and search: **`TODO_DB`**
3. Update `DB_SERVER` variable to match your SQL Server instance
4. Verify file paths match your setup

### 3. Test Everything

**Run system test:**
```bash
python test_connection.py
```

This will test:
- Python packages installed
- Aspen Plus connection
- Database connection
- Model file exists
- Single simulation run (if model ready)

**Fix any issues before proceeding!**

### 4. Run Small Test Batch

Before running all 1,170 simulations, test with 5:

**Modify config.py:**
```python
BATCH_SIZE = 5  # Test with 5 simulations first
```

**Run:**
```bash
python run_automation.py
```

**Review results** in database - check if data looks correct.

### 5. Run Full Automation

If test batch successful:

**Modify config.py:**
```python
BATCH_SIZE = 100  # Run 100 per batch
PAUSE_BETWEEN_BATCHES = True  # Pause to review
```

**Run:**
```bash
python run_automation.py
```

**Duration:** 3-6 hours (can run overnight)
**Batches:** 12 batches of 100 simulations (26 bio-oils × 45 conditions = 1,170 total)

---

## Configuration Settings

### Database Connection (IMPORTANT!)

**Search for `TODO_DB` and update these:**

```python
# config.py line ~35
DB_SERVER = r'YOUR_SERVER_NAME\SQLEXPRESS'  # TODO_DB: CHANGE THIS!
```

Examples:
```python
# If local instance:
DB_SERVER = r'localhost\SQLEXPRESS'

# If named instance:
DB_SERVER = r'ASPEN-PC\SQLEXPRESS'

# If default instance:
DB_SERVER = r'ASPEN-PC'
```

### Batch Mode Settings

```python
# config.py line ~72
BATCH_SIZE = 100               # Simulations per batch
PAUSE_BETWEEN_BATCHES = True   # Pause for review
AUTO_CONTINUE_DELAY = 0        # 0 = manual, 30 = auto after 30s
```

**Recommended settings:**
- **Testing:** `BATCH_SIZE = 5`, `PAUSE_BETWEEN_BATCHES = True`
- **Production:** `BATCH_SIZE = 100`, `PAUSE_BETWEEN_BATCHES = True`
- **Overnight:** `BATCH_SIZE = 1170`, `PAUSE_BETWEEN_BATCHES = False`

---

## Features

### Batch Mode
- Run N simulations, then pause
- Review results in database
- Press Enter to continue next batch
- Or Ctrl+C to abort

### Resume Capability
- Tracks completed simulations in database
- If interrupted, run again - it will skip completed ones
- Continues from where it stopped

### Error Handling
- If one simulation fails, continues with next
- Logs all errors
- Marks failed simulations in database
- Shows success/failure statistics

### Progress Tracking
- Real-time progress display
- Estimated time remaining
- Success rate statistics
- Batch summaries

---

## Troubleshooting

### Aspen Connection Failed

**Error:** `Cannot connect to Aspen Plus`

**Solutions:**
1. Ensure Aspen Plus V8.8 is installed and licensed
2. Run Python as administrator
3. Check Aspen is not already running
4. Try different dispatch strings in `config.py`:
   ```python
   ASPEN_DISPATCH_OPTIONS = [
       'Apwn.Document.29.0',  # V8.8
       'Apwn.Document',       # Generic
   ]
   ```

### Database Connection Failed

**Error:** `Failed to connect to database`

**Solutions:**
1. Update `DB_SERVER` in config.py (search: `TODO_DB`)
2. Check SQL Server is running
3. Verify database 'BIOOIL' exists
4. Test with SQL Server Management Studio first
5. Check Windows authentication enabled

### Simulation Won't Converge

**Error:** `Simulation did not converge`

**Solutions:**
1. Lower reformer temperature (try 750°C)
2. Increase steam-to-carbon ratio (try 4.0)
3. Check Aspen model is correctly built
4. Review Aspen model manually with test data
5. Check component specifications in model

### Model File Not Found

**Error:** `Model file not found`

**Solutions:**
1. Build Aspen model first (see docs/ASPEN_SIMULATION_GUIDE.md)
2. Verify path in config.py: `ASPEN_MODEL_PATH`
3. Ensure .bkp file is in correct location
4. Check file permissions

---

## Expected Results

### Success Rates
- **Target:** >90% convergence (>1,050 of 1,170 simulations)
- **Typical:** 85-95% convergence
- **Failed simulations:** Marked in database, can review later

### Timing
- **Per simulation:** 10-20 seconds
- **Per batch (100):** 15-30 minutes
- **Total (1,170):** 3-6 hours

### Database Records
After completion, database will have:
- ~1,170 records in `AspenSimulation` table
- ~1,000-1,100 `HydrogenProduct` records (converged only)
- ~4,000+ `SyngasComposition` records (4 locations × converged)

---

## After Automation Completes

### 1. Validate Results
```sql
-- Check convergence statistics
SELECT ConvergenceStatus, COUNT(*) as Count
FROM AspenSimulation
GROUP BY ConvergenceStatus

-- Check H2 yield range
SELECT MIN(H2_Yield_kg), AVG(H2_Yield_kg), MAX(H2_Yield_kg)
FROM HydrogenProduct

-- View ML-ready data
SELECT COUNT(*) FROM vw_ML_ReversePrediction
```

### 2. Export for ML Training
The `vw_ML_ReversePrediction` view contains all data ready for ML:
- 16 input features (H₂ product properties)
- 6 output features (bio-oil composition)

### 3. Review Failed Simulations
```sql
-- Check why simulations failed
SELECT Biooil_Id, Warnings, Notes
FROM AspenSimulation
WHERE ConvergenceStatus = 'Failed'
```

Can manually re-run failed cases with adjusted parameters.

---

## File Locations Reference

```
C:\BioOilProject\
  ├── automation_scripts\       ← Python scripts
  │   ├── config.py             ← UPDATE DB_SERVER HERE (TODO_DB)
  │   ├── aspen_interface.py
  │   ├── database_operations.py
  │   ├── run_automation.py     ← Main script to run
  │   ├── test_connection.py    ← Run this first
  │   ├── requirements.txt
  │   └── README.md
  │
  ├── data\
  │   └── aspen_input_matrix.csv ← 1,170 simulation scenarios
  │
  ├── aspen_model\
  │   └── biooil_reforming_base.bkp ← Build this first
  │
  ├── logs\                     ← Auto-created
  │   ├── automation_log.txt
  │   ├── error_log.txt
  │   └── progress.json
  │
  └── docs\
      ├── ASPEN_SIMULATION_GUIDE.md
      └── ASPEN_QUICK_REFERENCE.md
```

---

## Support

**Documentation:**
- Aspen model building: `../docs/ASPEN_SIMULATION_GUIDE.md`
- Quick reference: `../docs/ASPEN_QUICK_REFERENCE.md`
- Database schema: `../database/01_create_tables.sql`

**Common Issues:**
1. Search "TODO_DB" to update database server
2. Run `test_connection.py` first to diagnose issues
3. Start with small batch (5 simulations) before full run
4. Check logs in `C:\BioOilProject\logs\` folder

---

**Version:** 1.0
**Date:** 2025-11-16
**Status:** Ready for Use on Aspen Computer

