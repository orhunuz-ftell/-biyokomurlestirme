# Implementation Quick Reference
## Reverse ML Project - Phases 1-3 Summary

**Full Plan**: See `IMPLEMENTATION_PLAN_DB_AND_ASPEN.md`

---

## 📋 PHASE SUMMARY

### Phase 1: Database Extension (Days 1-2)
**Goal**: Add 5 new tables to BIOOIL database

**Tables to Create**:
1. `AspenSimulation` - Master simulation table
2. `ReformingConditions` - Process parameters (T, P, S/C)
3. `HydrogenProduct` - H₂ outputs (ML inputs)
4. `SyngasComposition` - Gas analysis at 4 points
5. `EnergyBalance` - Energy metrics

**Key View**: `vw_ML_ReversePrediction` - Joins everything for ML

---

### Phase 2: Reference Data Preparation (Days 3-5)
**Goal**: Prepare input data for 1,350 Aspen simulations

**Steps**:
1. Extract 30 complete bio-oil compositions from database
2. Generate DOE matrix: 5 temps × 3 pressures × 3 S/C = 45 conditions
3. Create full matrix: 30 bio-oils × 45 conditions = **1,350 simulations**

**Output Files**:
- `biooil_compositions_30.csv`
- `doe_matrix.csv`
- `aspen_input_matrix.csv` (1,350 rows)

---

### Phase 3: Aspen Automation (Days 6-15)
**Goal**: Run 1,350 Aspen simulations, store results in database

**Workflow**:
```
For each simulation (1-1350):
  1. Set bio-oil composition in RYIELD
  2. Set T, P, S/C conditions
  3. Run Aspen simulation
  4. Validate convergence & balances
  5. Extract H₂ product properties
  6. Store in database
```

**Time Estimate**: 4-5 hours for all simulations

---

## 🎯 KEY TARGETS

| Metric | Target |
|--------|--------|
| Total Simulations | 1,350 |
| Successful Runs | >1,200 (>89%) |
| Convergence Rate | >95% |
| Mass Balance Error | <0.1% |
| Energy Balance Error | <1.0% |

---

## 📁 FILE STRUCTURE

```
C:\@biyokomurlestirme\
├── specs/                               ← YOU ARE HERE
│   ├── IMPLEMENTATION_PLAN_DB_AND_ASPEN.md
│   └── QUICK_REFERENCE.md
│
├── reverse_ml_biooil_to_product/
│   ├── database/
│   │   ├── 01_create_tables.sql
│   │   ├── 02_create_indexes.sql
│   │   ├── 03_create_views.sql
│   │   └── 04_test_schema.sql
│   │
│   ├── scripts/
│   │   ├── phase2_data_prep/
│   │   │   ├── extract_biooil_data.py
│   │   │   ├── generate_doe_matrix.py
│   │   │   └── create_simulation_matrix.py
│   │   │
│   │   └── phase3_aspen_automation/
│   │       ├── aspen_connection.py
│   │       ├── aspen_input_setter.py
│   │       ├── aspen_result_extractor.py
│   │       ├── database_inserter.py
│   │       └── run_batch_simulations.py
│   │
│   ├── data/
│   │   └── biooil_reference_data/
│   │       ├── biooil_compositions_30.csv
│   │       ├── doe_matrix.csv
│   │       └── aspen_input_matrix.csv
│   │
│   ├── aspen_simulations/
│   │   └── process_flowsheet/
│   │       └── biooil_reforming_base.bkp
│   │
│   └── logs/
│       ├── simulation_log.csv
│       └── checkpoint.json
```

---

## 🚀 EXECUTION SEQUENCE

### Day 1-2: Database Setup
```bash
# Navigate to database folder
cd C:\@biyokomurlestirme\reverse_ml_biooil_to_product\database

# Run SQL scripts in order
sqlcmd -S DESKTOP-DRO84HP\SQLEXPRESS -d BIOOIL -i 01_create_tables.sql
sqlcmd -S DESKTOP-DRO84HP\SQLEXPRESS -d BIOOIL -i 02_create_indexes.sql
sqlcmd -S DESKTOP-DRO84HP\SQLEXPRESS -d BIOOIL -i 03_create_views.sql
sqlcmd -S DESKTOP-DRO84HP\SQLEXPRESS -d BIOOIL -i 04_test_schema.sql
```

### Day 3-5: Data Preparation
```bash
cd C:\@biyokomurlestirme\reverse_ml_biooil_to_product\scripts\phase2_data_prep

# Extract bio-oil data
python extract_biooil_data.py

# Generate DOE matrix
python generate_doe_matrix.py

# Create full simulation matrix
python create_simulation_matrix.py
```

### Day 6-10: Aspen Setup & Testing
1. Build Aspen model manually
2. Validate with 3-5 test cases
3. Write automation scripts
4. Test with 10 simulations

### Day 11-15: Production Runs
```bash
cd C:\@biyokomurlestirme\reverse_ml_biooil_to_product\scripts\phase3_aspen_automation

# Run in batches
python run_batch_simulations.py \
  --input ../../data/biooil_reference_data/aspen_input_matrix.csv \
  --model ../../aspen_simulations/process_flowsheet/biooil_reforming_base.bkp \
  --batch-size 100
```

---

## 📊 DATABASE SCHEMA (Simplified)

```
Existing:
  Biooil (70 records)
    ↓ (used as input for Aspen)

New:
  AspenSimulation (1,350 records)
    ├─→ ReformingConditions (T, P, S/C)
    ├─→ HydrogenProduct (H₂ yield, purity, etc.)
    ├─→ SyngasComposition (4 stream locations)
    └─→ EnergyBalance (energy metrics)

ML View:
  vw_ML_ReversePrediction
    ML Inputs:  HydrogenProduct columns
    ML Outputs: Biooil composition columns
```

---

## 🔑 KEY PYTHON FUNCTIONS

### Connect to Database
```python
import pyodbc
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DESKTOP-DRO84HP\\SQLEXPRESS;'
    'DATABASE=BIOOIL;'
    'Trusted_Connection=yes'
)
```

### Connect to Aspen
```python
import win32com.client as win32
aspen = win32.Dispatch('Apwn.Document')
aspen.InitFromArchive2('path/to/model.bkp')
```

### Set Bio-oil Composition
```python
ryield_path = r"\Data\Blocks\BIOOILFEED\Input\YIELD\MIXED"
aspen.Tree.FindNode(f"{ryield_path}\\TOLUENE").Value = aromatics / 100.0
# ... repeat for other components
```

### Run Simulation
```python
aspen.Engine.Run2()
status = aspen.Tree.FindNode(r"\Data\Results Summary\Run-Status\Output\RUNID").Value
```

### Extract H₂ Yield
```python
h2_flow = aspen.Tree.FindNode(
    r"\Data\Streams\H2PROD\Output\MASSFLMX\MIXED"
).Value
```

---

## ⚠️ COMMON ISSUES & SOLUTIONS

### Issue: Simulation doesn't converge
**Solution**:
- Increase max iterations
- Check initial guesses
- Verify S/C ratio is reasonable (2-6)
- Check bio-oil composition sums to ~100%

### Issue: Database connection fails
**Solution**:
- Check SQL Server is running
- Verify Windows Authentication
- Test connection with `sqlcmd`

### Issue: Aspen COM crashes
**Solution**:
- Close Aspen GUI if open
- Restart script
- Use checkpoint to resume

### Issue: Mass balance error >0.1%
**Solution**:
- Check for leaks in flowsheet
- Verify all streams connected
- Review separator specifications

---

## 📞 QUICK CONTACTS

**Database**: SQL Server Management Studio (SSMS)
**Aspen**: Aspen Plus V12 (or V2006)
**Python**: Python 3.8+, pyodbc, pywin32

**Key Libraries**:
```bash
pip install pyodbc pandas numpy pywin32 openpyxl
```

---

## ✅ PRE-FLIGHT CHECKLIST

Before starting:
- [ ] SQL Server running and accessible
- [ ] Aspen Plus installed and licensed
- [ ] Python environment set up with required packages
- [ ] Database backup created
- [ ] Sufficient disk space (~5 GB for logs/results)
- [ ] Read full implementation plan
- [ ] Understand process flow

---

## 📈 PROGRESS TRACKING

Track in `simulation_log.csv`:
- Total simulations: 1,350
- Completed: _____
- Success rate: _____%
- Average time per simulation: ____ seconds
- Estimated completion: ____

---

**For detailed information, see**: `IMPLEMENTATION_PLAN_DB_AND_ASPEN.md`

**Status**: Ready to begin Phase 1
**Date**: 2025-11-16
