# Implementation Plan: Database Extension & Aspen Data Generation
## Reverse ML Project - Phases 1-3

**Project**: Bio-oil Steam Reforming Reverse ML
**Document Version**: 1.0
**Date**: 2025-11-16
**Author**: Orhun Uzdiyem

---

## TABLE OF CONTENTS

1. [Overview](#overview)
2. [Phase 1: Database Extension](#phase-1-database-extension)
3. [Phase 2: Reference Data Preparation](#phase-2-reference-data-preparation)
4. [Phase 3: Aspen Automation & Data Collection](#phase-3-aspen-automation--data-collection)
5. [Validation & Quality Control](#validation--quality-control)
6. [Risk Assessment](#risk-assessment)
7. [Timeline & Milestones](#timeline--milestones)
8. [Deliverables Checklist](#deliverables-checklist)

---

## OVERVIEW

### Objectives

**Primary Goal**: Extend the existing BIOOIL database to support the reverse ML project, where Aspen simulation outputs (H₂ product properties) are used as ML inputs to predict required bio-oil composition.

**Success Criteria**:
- ✅ Database schema extended with 5 new tables
- ✅ 30 complete bio-oil reference compositions extracted
- ✅ 1,000-1,500 Aspen simulations completed successfully
- ✅ All data validated (mass/energy balances, convergence)
- ✅ Data ready for ML training (Phase 4)

### Scope

**In Scope** (Phases 1-3):
- Database schema design and implementation
- Data extraction and preparation
- Aspen model development and automation
- Simulation execution and data collection
- Data validation and quality control

**Out of Scope** (Phase 4 - Future):
- Machine learning model development
- Model training and evaluation
- Prediction tool development

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    EXISTING DATABASE                         │
│  Biooil Table (70 records) → ML OUTPUT (to predict)         │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                 PHASE 2: REFERENCE DATA                      │
│  Extract 30 complete bio-oil compositions                    │
│  Generate DOE matrix (T, P, S/C variations)                  │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              PHASE 3: ASPEN AUTOMATION                       │
│  For each bio-oil × process condition:                       │
│    - Run Aspen simulation                                    │
│    - Extract H₂ product properties → ML INPUT                │
│    - Validate convergence & balances                         │
│    - Store in database                                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                  PHASE 1: NEW TABLES                         │
│  AspenSimulation, ReformingConditions, HydrogenProduct,     │
│  SyngasComposition, EnergyBalance                            │
│  → Store 1000-1500 simulation results                       │
└─────────────────────────────────────────────────────────────┘
```

---

## PHASE 1: DATABASE EXTENSION

### 1.1 Objectives

- Extend BIOOIL database with 5 new tables to store Aspen simulation data
- Establish proper relationships and constraints
- Create indexes for efficient ML data queries
- Create views for simplified data access

### 1.2 Database Design

#### 1.2.1 New Table: `AspenSimulation`

**Purpose**: Master table for each Aspen simulation run

```sql
CREATE TABLE AspenSimulation (
    SimulationId INT PRIMARY KEY IDENTITY(1,1),
    Biooil_Id INT NOT NULL,  -- FK to Biooil.BiooilId
    SimulationDate DATETIME NOT NULL DEFAULT GETDATE(),
    AspenVersion NVARCHAR(50) NULL,
    ConvergenceStatus NVARCHAR(20) NOT NULL,  -- 'Converged', 'Failed', 'Warning'
    ConvergenceIterations INT NULL,
    MassBalanceError_percent DECIMAL(10,6) NULL,
    EnergyBalanceError_percent DECIMAL(10,6) NULL,
    Warnings NVARCHAR(MAX) NULL,
    Notes NVARCHAR(MAX) NULL,
    ValidationFlag BIT DEFAULT 0,  -- 1=validated, 0=needs review
    CreatedBy NVARCHAR(50) DEFAULT SYSTEM_USER,

    CONSTRAINT FK_AspenSimulation_Biooil
        FOREIGN KEY (Biooil_Id) REFERENCES Biooil(BiooilId)
        ON DELETE CASCADE
);
```

**Indexes**:
```sql
CREATE INDEX IX_AspenSimulation_Biooil ON AspenSimulation(Biooil_Id);
CREATE INDEX IX_AspenSimulation_Status ON AspenSimulation(ConvergenceStatus);
CREATE INDEX IX_AspenSimulation_Date ON AspenSimulation(SimulationDate);
```

#### 1.2.2 New Table: `ReformingConditions`

**Purpose**: Store process operating conditions for each simulation

```sql
CREATE TABLE ReformingConditions (
    ConditionId INT PRIMARY KEY IDENTITY(1,1),
    Simulation_Id INT NOT NULL,  -- FK to AspenSimulation

    -- Reformer Operating Conditions
    ReformerTemperature_C DECIMAL(10,2) NOT NULL,  -- 650-850°C
    ReformerPressure_bar DECIMAL(10,2) NOT NULL,   -- 5-30 bar
    SteamToCarbonRatio DECIMAL(10,4) NOT NULL,     -- 2-6

    -- Feed Conditions
    BiooilFeedRate_kgh DECIMAL(10,2) NULL,         -- kg/h
    SteamFeedRate_kgh DECIMAL(10,2) NULL,          -- kg/h

    -- Reactor Specifications
    ResidenceTime_min DECIMAL(10,2) NULL,          -- minutes in reformer
    CatalystWeight_kg DECIMAL(10,2) NULL,          -- Ni/Al2O3 catalyst
    GHSV_h1 DECIMAL(10,2) NULL,                    -- Gas hourly space velocity

    -- Other Reactors
    HTS_Temperature_C DECIMAL(10,2) NULL,          -- High-temp shift: ~370°C
    LTS_Temperature_C DECIMAL(10,2) NULL,          -- Low-temp shift: ~210°C
    PSA_Pressure_bar DECIMAL(10,2) NULL,           -- Pressure swing adsorption

    CONSTRAINT FK_ReformingConditions_Simulation
        FOREIGN KEY (Simulation_Id) REFERENCES AspenSimulation(SimulationId)
        ON DELETE CASCADE
);
```

**Indexes**:
```sql
CREATE INDEX IX_ReformingConditions_Simulation ON ReformingConditions(Simulation_Id);
CREATE INDEX IX_ReformingConditions_Temp ON ReformingConditions(ReformerTemperature_C);
```

#### 1.2.3 New Table: `HydrogenProduct`

**Purpose**: Store hydrogen product properties (ML INPUTS)

```sql
CREATE TABLE HydrogenProduct (
    ProductId INT PRIMARY KEY IDENTITY(1,1),
    Simulation_Id INT NOT NULL,  -- FK to AspenSimulation

    -- Primary H2 Product Properties (ML INPUTS)
    H2_Yield_kg DECIMAL(10,4) NOT NULL,              -- kg H2 per 100 kg bio-oil
    H2_Purity_percent DECIMAL(10,4) NOT NULL,        -- >99.9% from PSA
    H2_FlowRate_kgh DECIMAL(10,4) NULL,              -- kg/h
    H2_FlowRate_Nm3h DECIMAL(10,4) NULL,             -- Nm³/h

    -- Product Gas Ratios (ML INPUTS)
    H2_CO_Ratio DECIMAL(10,4) NULL,                  -- Molar ratio
    H2_CO2_Ratio DECIMAL(10,4) NULL,                 -- Molar ratio

    -- By-product Quantities
    CO2_Production_kg DECIMAL(10,4) NULL,            -- kg CO2
    CO2_Purity_percent DECIMAL(10,4) NULL,           -- From CO2 removal unit

    -- Performance Indicators (ML INPUTS)
    CH4_Slip_percent DECIMAL(10,4) NULL,             -- Unreacted methane
    CO_Slip_ppm DECIMAL(10,4) NULL,                  -- CO in final H2 (<1%)
    Carbon_Conversion_percent DECIMAL(10,2) NULL,    -- % of carbon converted
    H2_Recovery_PSA_percent DECIMAL(10,2) NULL,      -- H2 recovery in PSA (85-92%)

    -- Energy Metrics (ML INPUTS)
    Energy_Efficiency_percent DECIMAL(10,2) NULL,    -- Overall energy efficiency
    Specific_Energy_MJperkg_H2 DECIMAL(10,2) NULL,   -- MJ per kg H2 produced

    -- Tail Gas (for energy balance)
    TailGas_FlowRate_kgh DECIMAL(10,4) NULL,         -- From PSA
    TailGas_HHV_MJperkg DECIMAL(10,2) NULL,          -- Heating value

    CONSTRAINT FK_HydrogenProduct_Simulation
        FOREIGN KEY (Simulation_Id) REFERENCES AspenSimulation(SimulationId)
        ON DELETE CASCADE
);
```

**Indexes**:
```sql
CREATE INDEX IX_HydrogenProduct_Simulation ON HydrogenProduct(Simulation_Id);
CREATE INDEX IX_HydrogenProduct_Yield ON HydrogenProduct(H2_Yield_kg);
```

#### 1.2.4 New Table: `SyngasComposition`

**Purpose**: Detailed gas composition at various process points

```sql
CREATE TABLE SyngasComposition (
    SyngasId INT PRIMARY KEY IDENTITY(1,1),
    Simulation_Id INT NOT NULL,  -- FK to AspenSimulation
    StreamLocation NVARCHAR(50) NOT NULL,  -- 'Reformer_Out', 'HTS_Out', 'LTS_Out', 'PSA_In'

    -- Gas Composition (mol%)
    H2_molpercent DECIMAL(10,4) NULL,
    CO_molpercent DECIMAL(10,4) NULL,
    CO2_molpercent DECIMAL(10,4) NULL,
    CH4_molpercent DECIMAL(10,4) NULL,
    H2O_molpercent DECIMAL(10,4) NULL,
    N2_molpercent DECIMAL(10,4) NULL,

    -- Stream Properties
    Temperature_C DECIMAL(10,2) NULL,
    Pressure_bar DECIMAL(10,2) NULL,
    MassFlowRate_kgh DECIMAL(10,4) NULL,
    MolarFlowRate_kmolh DECIMAL(10,4) NULL,

    CONSTRAINT FK_SyngasComposition_Simulation
        FOREIGN KEY (Simulation_Id) REFERENCES AspenSimulation(SimulationId)
        ON DELETE CASCADE
);
```

**Indexes**:
```sql
CREATE INDEX IX_SyngasComposition_Simulation ON SyngasComposition(Simulation_Id);
CREATE INDEX IX_SyngasComposition_Location ON SyngasComposition(StreamLocation);
```

#### 1.2.5 New Table: `EnergyBalance`

**Purpose**: Energy inputs/outputs for process optimization

```sql
CREATE TABLE EnergyBalance (
    EnergyId INT PRIMARY KEY IDENTITY(1,1),
    Simulation_Id INT NOT NULL,  -- FK to AspenSimulation

    -- Energy Inputs (MJ)
    BiooilEnergy_HHV_MJ DECIMAL(10,2) NULL,          -- Bio-oil HHV
    PreheaterHeat_MJ DECIMAL(10,2) NULL,             -- External heat to preheater
    ReformerHeat_MJ DECIMAL(10,2) NULL,              -- External heat to reformer
    TotalEnergyInput_MJ DECIMAL(10,2) NULL,          -- Sum of inputs

    -- Energy Outputs (MJ)
    H2Product_HHV_MJ DECIMAL(10,2) NULL,             -- H2 energy content
    TailGasEnergy_MJ DECIMAL(10,2) NULL,             -- Tail gas (can be recovered)
    HeatRecovered_MJ DECIMAL(10,2) NULL,             -- Heat exchanger recovery
    HeatLoss_MJ DECIMAL(10,2) NULL,                  -- Stack loss, cooling

    -- Efficiency Calculations
    Thermal_Efficiency_percent DECIMAL(10,2) NULL,   -- H2 output / total input
    Carbon_Efficiency_percent DECIMAL(10,2) NULL,    -- Carbon to H2 / carbon in

    CONSTRAINT FK_EnergyBalance_Simulation
        FOREIGN KEY (Simulation_Id) REFERENCES AspenSimulation(SimulationId)
        ON DELETE CASCADE
);
```

**Indexes**:
```sql
CREATE INDEX IX_EnergyBalance_Simulation ON EnergyBalance(Simulation_Id);
```

---

### 1.3 Database Views

#### 1.3.1 View: `vw_ML_ReversePrediction`

**Purpose**: Simplified view joining all tables for ML training

```sql
CREATE VIEW vw_ML_ReversePrediction AS
SELECT
    -- Identifiers
    a.SimulationId,
    a.Biooil_Id,
    a.SimulationDate,
    a.ConvergenceStatus,

    -- ML INPUTS: Process Conditions
    rc.ReformerTemperature_C,
    rc.ReformerPressure_bar,
    rc.SteamToCarbonRatio,
    rc.BiooilFeedRate_kgh,

    -- ML INPUTS: Product Properties (from Aspen simulation)
    hp.H2_Yield_kg,
    hp.H2_Purity_percent,
    hp.H2_CO_Ratio,
    hp.H2_CO2_Ratio,
    hp.CO2_Production_kg,
    hp.CH4_Slip_percent,
    hp.CO_Slip_ppm,
    hp.Carbon_Conversion_percent,
    hp.Energy_Efficiency_percent,
    hp.H2_FlowRate_Nm3h,
    hp.Specific_Energy_MJperkg_H2,

    -- ML OUTPUTS: Bio-oil Composition (to predict)
    b.aromatics,
    b.acids,
    b.alcohols,
    b.furans,
    b.phenols,
    b.[aldehyde&ketone] as aldehyde_ketone,
    b.esters,
    b.aliphatichydrocarbon,

    -- Quality Indicators
    a.MassBalanceError_percent,
    a.EnergyBalanceError_percent,
    a.ValidationFlag

FROM AspenSimulation a
INNER JOIN HydrogenProduct hp ON a.SimulationId = hp.Simulation_Id
INNER JOIN ReformingConditions rc ON a.SimulationId = rc.Simulation_Id
INNER JOIN Biooil b ON a.Biooil_Id = b.BiooilId

WHERE a.ConvergenceStatus = 'Converged'
  AND a.ValidationFlag = 1
  AND b.aromatics IS NOT NULL
  AND b.acids IS NOT NULL
  AND b.alcohols IS NOT NULL
  AND b.furans IS NOT NULL
  AND b.phenols IS NOT NULL
  AND b.[aldehyde&ketone] IS NOT NULL;
```

#### 1.3.2 View: `vw_SimulationSummary`

**Purpose**: High-level summary for monitoring

```sql
CREATE VIEW vw_SimulationSummary AS
SELECT
    a.SimulationId,
    a.SimulationDate,
    a.ConvergenceStatus,
    a.ValidationFlag,
    b.BiooilId,
    rc.ReformerTemperature_C,
    rc.ReformerPressure_bar,
    rc.SteamToCarbonRatio,
    hp.H2_Yield_kg,
    hp.Carbon_Conversion_percent,
    hp.Energy_Efficiency_percent,
    CASE
        WHEN a.MassBalanceError_percent <= 0.1 AND a.EnergyBalanceError_percent <= 1.0
        THEN 'Pass'
        ELSE 'Review'
    END AS QualityStatus
FROM AspenSimulation a
LEFT JOIN ReformingConditions rc ON a.SimulationId = rc.Simulation_Id
LEFT JOIN HydrogenProduct hp ON a.SimulationId = hp.Simulation_Id
LEFT JOIN Biooil b ON a.Biooil_Id = b.BiooilId;
```

---

### 1.4 Implementation Scripts

**Deliverables**:
1. `01_create_tables.sql` - Create all 5 new tables
2. `02_create_indexes.sql` - Create all indexes
3. `03_create_views.sql` - Create ML and summary views
4. `04_create_constraints.sql` - Add foreign key constraints (if not in table creation)
5. `05_test_schema.sql` - Insert test records to verify structure

**Script Location**: `C:\@biyokomurlestirme\reverse_ml_biooil_to_product\database\`

---

### 1.5 Testing & Validation

#### Test Cases:

**TC1.1**: Table Creation
- Verify all 5 tables created successfully
- Check column data types
- Verify primary keys

**TC1.2**: Relationships
- Insert test record in AspenSimulation
- Insert child records in all related tables
- Verify foreign key constraints work

**TC1.3**: Cascade Delete
- Delete a simulation record
- Verify all child records deleted (cascade)

**TC1.4**: Indexes
- Query sys.indexes to verify all indexes created
- Test query performance with indexes

**TC1.5**: Views
- Query vw_ML_ReversePrediction
- Verify all columns present and properly joined
- Check filtering logic

---

### 1.6 Rollback Plan

If issues occur:

```sql
-- Rollback script (use with caution!)
DROP VIEW IF EXISTS vw_SimulationSummary;
DROP VIEW IF EXISTS vw_ML_ReversePrediction;

DROP TABLE IF EXISTS EnergyBalance;
DROP TABLE IF EXISTS SyngasComposition;
DROP TABLE IF EXISTS HydrogenProduct;
DROP TABLE IF EXISTS ReformingConditions;
DROP TABLE IF EXISTS AspenSimulation;
```

---

## PHASE 2: REFERENCE DATA PREPARATION

### 2.1 Objectives

- Extract 30 complete bio-oil compositions from existing database
- Analyze composition ranges and statistics
- Generate Design of Experiments (DOE) matrix for Aspen simulations
- Create reference CSV files for Aspen automation

### 2.2 Data Extraction Strategy

#### 2.2.1 Selection Criteria

**Query to identify complete records**:

```sql
SELECT
    b.BiooilId,
    b.Experiment_Id,
    b.aromatics,
    b.acids,
    b.alcohols,
    b.furans,
    b.phenols,
    b.[aldehyde&ketone] as aldehyde_ketone,
    b.esters,
    b.aliphatichydrocarbon,
    -- Calculate total composition
    (ISNULL(b.aromatics,0) +
     ISNULL(b.acids,0) +
     ISNULL(b.alcohols,0) +
     ISNULL(b.furans,0) +
     ISNULL(b.phenols,0) +
     ISNULL(b.[aldehyde&ketone],0)) as total_composition
FROM Biooil b
WHERE b.aromatics IS NOT NULL
  AND b.acids IS NOT NULL
  AND b.alcohols IS NOT NULL
  AND b.furans IS NOT NULL
  AND b.phenols IS NOT NULL
  AND b.[aldehyde&ketone] IS NOT NULL
ORDER BY b.BiooilId;
```

**Expected Result**: 30 complete records (as identified in analysis)

#### 2.2.2 Statistical Analysis

Calculate for each component:
- Minimum value
- Maximum value
- Mean
- Median
- Standard deviation
- 25th and 75th percentiles

**Python Script**: `analyze_biooil_statistics.py`

```python
import pyodbc
import pandas as pd
import numpy as np

def analyze_biooil_composition():
    conn = pyodbc.connect('...')

    query = """SELECT ... (from above)"""
    df = pd.read_sql(query, conn)

    components = ['aromatics', 'acids', 'alcohols',
                  'furans', 'phenols', 'aldehyde_ketone']

    stats = {}
    for comp in components:
        stats[comp] = {
            'min': df[comp].min(),
            'max': df[comp].max(),
            'mean': df[comp].mean(),
            'median': df[comp].median(),
            'std': df[comp].std(),
            'q25': df[comp].quantile(0.25),
            'q75': df[comp].quantile(0.75)
        }

    # Save statistics
    stats_df = pd.DataFrame(stats).T
    stats_df.to_csv('biooil_composition_statistics.csv')

    return df, stats_df
```

---

### 2.3 Design of Experiments (DOE)

#### 2.3.1 Process Variables

**Independent Variables** (to vary in Aspen):

| Variable | Symbol | Min | Baseline | Max | Levels | Unit |
|----------|--------|-----|----------|-----|--------|------|
| Reformer Temperature | T | 650 | 800 | 850 | 5 | °C |
| System Pressure | P | 10 | 20 | 30 | 3 | bar |
| Steam/Carbon Ratio | S/C | 2.0 | 3.5 | 5.0 | 3 | mol/mol |

**Levels for each variable**:
- **Temperature**: 650, 725, 800, 825, 850 (5 levels)
- **Pressure**: 10, 20, 30 (3 levels)
- **S/C Ratio**: 2, 3.5, 5 (3 levels)

**Total combinations**: 5 × 3 × 3 = **45 combinations per bio-oil**

#### 2.3.2 DOE Matrix Generation

**Python Script**: `generate_doe_matrix.py`

```python
import pandas as pd
import itertools

def generate_doe_matrix():
    # Define parameter levels
    temperatures = [650, 725, 800, 825, 850]
    pressures = [10, 20, 30]
    sc_ratios = [2.0, 3.5, 5.0]

    # Generate all combinations
    combinations = list(itertools.product(temperatures, pressures, sc_ratios))

    doe_matrix = pd.DataFrame(combinations,
                              columns=['Temperature_C', 'Pressure_bar', 'SC_Ratio'])

    doe_matrix['RunID'] = range(1, len(doe_matrix) + 1)

    # Save DOE matrix
    doe_matrix.to_csv('doe_matrix.csv', index=False)

    return doe_matrix

# Expected: 45 rows
```

#### 2.3.3 Full Simulation Matrix

**Combine bio-oil compositions with DOE matrix**:

```python
def create_full_simulation_matrix(biooil_df, doe_matrix):
    """
    Cross-product of bio-oil compositions and process conditions

    Returns: DataFrame with ~1,350 rows (30 bio-oils × 45 conditions)
    """

    # Add a key for cross join
    biooil_df['key'] = 1
    doe_matrix['key'] = 1

    # Cross join
    full_matrix = biooil_df.merge(doe_matrix, on='key').drop('key', axis=1)

    # Add unique simulation ID
    full_matrix['SimulationID'] = range(1, len(full_matrix) + 1)

    # Reorder columns
    cols_order = ['SimulationID', 'BiooilId', 'Temperature_C', 'Pressure_bar',
                  'SC_Ratio', 'aromatics', 'acids', 'alcohols', 'furans',
                  'phenols', 'aldehyde_ketone']

    full_matrix = full_matrix[cols_order + [c for c in full_matrix.columns
                                             if c not in cols_order]]

    # Save to CSV for Aspen automation
    full_matrix.to_csv('aspen_input_matrix.csv', index=False)

    print(f"Total simulations to run: {len(full_matrix)}")

    return full_matrix
```

**Expected Output**: `aspen_input_matrix.csv` with ~1,350 rows

---

### 2.4 Reference Data Files

**Output Files** (in `reverse_ml_biooil_to_product/data/biooil_reference_data/`):

1. **`biooil_compositions_30.csv`**
   - 30 complete bio-oil compositions
   - Columns: BiooilId, aromatics, acids, alcohols, furans, phenols, aldehyde_ketone

2. **`biooil_composition_statistics.csv`**
   - Statistical summary of each component
   - Columns: component, min, max, mean, median, std, q25, q75

3. **`doe_matrix.csv`**
   - 45 process condition combinations
   - Columns: RunID, Temperature_C, Pressure_bar, SC_Ratio

4. **`aspen_input_matrix.csv`**
   - Full simulation matrix (~1,350 rows)
   - Columns: SimulationID, BiooilId, Temperature_C, Pressure_bar, SC_Ratio,
              aromatics, acids, alcohols, furans, phenols, aldehyde_ketone

5. **`biooil_surrogate_components.csv`**
   - Mapping of bio-oil components to Aspen surrogate compounds
   - For RYIELD block configuration

---

### 2.5 Bio-oil Surrogate Component Mapping

For Aspen simulation, map bio-oil chemical groups to representative compounds:

| Bio-oil Group | Surrogate Compound | Formula | MW (g/mol) |
|---------------|-------------------|---------|------------|
| Aromatics | Toluene | C₇H₈ | 92.14 |
| Acids | Acetic Acid | C₂H₄O₂ | 60.05 |
| Alcohols | Ethanol | C₂H₆O | 46.07 |
| Furans | Furfural | C₅H₄O₂ | 96.08 |
| Phenols | Phenol | C₆H₆O | 94.11 |
| Aldehyde & Ketones | Acetone | C₃H₆O | 58.08 |
| Water | H₂O | H₂O | 18.02 |

**Assumption**: Water content = 20 wt% of bio-oil (typical)

---

### 2.6 Implementation Scripts

**Python Scripts**:
1. `extract_biooil_data.py` - Extract 30 complete compositions from database
2. `analyze_biooil_statistics.py` - Calculate statistics
3. `generate_doe_matrix.py` - Create DOE matrix
4. `create_simulation_matrix.py` - Generate full input matrix
5. `prepare_aspen_surrogate.py` - Create surrogate component mapping

**Script Location**: `C:\@biyokomurlestirme\reverse_ml_biooil_to_product\scripts\`

---

### 2.7 Validation

**Validation Checks**:
- ✅ Exactly 30 bio-oil records extracted
- ✅ All 6 main components present in each record
- ✅ Component values within reasonable ranges (0-100%)
- ✅ DOE matrix has 45 unique combinations
- ✅ Full simulation matrix has ~1,350 rows (30 × 45)
- ✅ No duplicate SimulationIDs
- ✅ Surrogate components sum to 100% (including water)

---

## PHASE 3: ASPEN AUTOMATION & DATA COLLECTION

### 3.1 Objectives

- Build and validate Aspen Plus reforming model
- Automate simulation execution using Python (COM interface)
- Run 1,000-1,500 simulations with various bio-oil compositions and process conditions
- Extract results and store in database
- Validate mass/energy balances and convergence

### 3.2 Aspen Model Development

#### 3.2.1 Aspen Flowsheet Structure

**Process Flow** (based on TIK 3 report Figure 1):

```
[RYIELD] → [MIXER] → [HEATER] → [RGIBBS/REFORMER] → [COOLER1]
    → [RPLUG/HTS] → [COOLER2] → [RPLUG/LTS] → [FLASH2]
    → [SEP/CO2-REMOVAL] → [SEP/PSA] → H2-PRODUCT
```

**Aspen Blocks**:

| Block Name | Type | Purpose | Operating Conditions |
|------------|------|---------|---------------------|
| BIOOILFEED | RYIELD | Bio-oil decomposition | Ambient |
| STEAMMIX | MIXER | Mix bio-oil + steam | 200-400°C |
| PREHEAT | HEATER | Heat to reforming T | Outlet: 650-850°C |
| REFORMER | RGIBBS | Main reforming | 650-850°C, 5-30 bar |
| COOLHTS | HEATER | Cool to HTS inlet | Outlet: 370°C |
| HTS | RPLUG | High-temp WGS | 350-400°C |
| COOLLTS | HEATER | Cool to LTS inlet | Outlet: 210°C |
| LTS | RPLUG | Low-temp WGS | 200-220°C |
| COOLCOND | HEATER | Cool to condenser | Outlet: 35°C |
| FLASH | FLASH2 | Remove water | 35°C |
| CO2REM | SEP | CO₂ removal (95%) | 35°C |
| PSA | SEP | H₂ purification | H₂ recovery: 90%, purity: 99.9% |

#### 3.2.2 Component List

**Define in Aspen Components**:
- H2, CO, CO2, CH4, H2O, N2 (conventional)
- Toluene (aromatics surrogate)
- Acetic-acid (acids surrogate)
- Ethanol (alcohols surrogate)
- Furfural (furans surrogate)
- Phenol (phenols surrogate)
- Acetone (aldehyde&ketones surrogate)

**Property Method**: PRSV (Peng-Robinson-Stryjek-Vera)

#### 3.2.3 RYIELD Block Configuration

**Decompose bio-oil into surrogate components**:

```
Input Stream: BIOOIL (100 kg/h, assume 25°C, 1 bar)

Yield Distribution (from simulation matrix):
- Toluene:      X1 % (from aromatics column)
- Acetic Acid:  X2 % (from acids column)
- Ethanol:      X3 % (from alcohols column)
- Furfural:     X4 % (from furans column)
- Phenol:       X5 % (from phenols column)
- Acetone:      X6 % (from aldehyde_ketone column)
- H2O:          20 % (assumed)

Total: 100%
```

**This will be updated for each simulation via Python automation**

---

### 3.3 Aspen Automation Strategy

#### 3.3.1 Python-Aspen COM Interface

**Technology**: `pywin32` (win32com.client)

**Connection Setup**:
```python
import win32com.client as win32
import os

def connect_aspen(model_path):
    """
    Connect to Aspen Plus via COM interface

    Args:
        model_path: Full path to .bkp or .apw file

    Returns:
        aspen: Aspen application object
    """
    aspen = win32.Dispatch('Apwn.Document')
    aspen.InitFromArchive2(model_path)

    return aspen
```

#### 3.3.2 Automation Workflow

**Main Script**: `run_aspen_simulations.py`

```python
def run_simulation_batch(input_matrix_csv, aspen_model_path):
    """
    Run batch of Aspen simulations

    Process:
    1. Read simulation matrix CSV
    2. For each row:
        a. Set bio-oil composition in RYIELD
        b. Set process conditions (T, P, S/C)
        c. Run simulation
        d. Check convergence
        e. Extract results
        f. Store in database
        g. Log status
    """

    # Load simulation matrix
    sim_matrix = pd.read_csv(input_matrix_csv)

    # Connect to Aspen
    aspen = connect_aspen(aspen_model_path)

    # Connect to database
    conn = pyodbc.connect('...')

    results = []

    for idx, row in sim_matrix.iterrows():
        print(f"Running simulation {idx+1}/{len(sim_matrix)}")

        try:
            # Set inputs
            set_biooil_composition(aspen, row)
            set_process_conditions(aspen, row)

            # Run simulation
            run_status = aspen.Engine.Run2()

            # Check convergence
            if check_convergence(aspen):
                # Extract results
                result = extract_results(aspen, row)

                # Store in database
                store_results(conn, result)

                results.append({'SimID': row['SimulationID'],
                               'Status': 'Success'})
            else:
                results.append({'SimID': row['SimulationID'],
                               'Status': 'Failed'})

        except Exception as e:
            print(f"Error in simulation {row['SimulationID']}: {str(e)}")
            results.append({'SimID': row['SimulationID'],
                           'Status': 'Error',
                           'Message': str(e)})

    # Save log
    log_df = pd.DataFrame(results)
    log_df.to_csv('simulation_log.csv', index=False)

    return results
```

#### 3.3.3 Setting Bio-oil Composition

```python
def set_biooil_composition(aspen, row):
    """
    Set RYIELD block yields based on bio-oil composition
    """
    # Path to RYIELD block yields
    ryield_path = r"\Data\Blocks\BIOOILFEED\Input\YIELD\MIXED"

    # Set each component yield (mass fraction)
    aspen.Tree.FindNode(f"{ryield_path}\\TOLUENE").Value = row['aromatics'] / 100.0
    aspen.Tree.FindNode(f"{ryield_path}\\ACETIC-ACID").Value = row['acids'] / 100.0
    aspen.Tree.FindNode(f"{ryield_path}\\ETHANOL").Value = row['alcohols'] / 100.0
    aspen.Tree.FindNode(f"{ryield_path}\\FURFURAL").Value = row['furans'] / 100.0
    aspen.Tree.FindNode(f"{ryield_path}\\PHENOL").Value = row['phenols'] / 100.0
    aspen.Tree.FindNode(f"{ryield_path}\\ACETONE").Value = row['aldehyde_ketone'] / 100.0
    aspen.Tree.FindNode(f"{ryield_path}\\H2O").Value = 0.20  # 20% water
```

#### 3.3.4 Setting Process Conditions

```python
def set_process_conditions(aspen, row):
    """
    Set reformer temperature, pressure, and S/C ratio
    """
    # Reformer temperature
    reformer_temp_path = r"\Data\Blocks\REFORMER\Input\TEMP"
    aspen.Tree.FindNode(reformer_temp_path).Value = row['Temperature_C']

    # System pressure
    pressure_path = r"\Data\Blocks\REFORMER\Input\PRES"
    aspen.Tree.FindNode(pressure_path).Value = row['Pressure_bar']

    # S/C ratio (adjust steam flow rate)
    # Calculate required steam flow based on carbon content
    biooil_flow = 100  # kg/h (baseline)
    carbon_molar = calculate_carbon_molar_flow(row)  # kmol C/h
    steam_molar = row['SC_Ratio'] * carbon_molar    # kmol H2O/h
    steam_mass = steam_molar * 18.02                 # kg/h

    steam_flow_path = r"\Data\Streams\STEAM\Input\TOTFLOW\MIXED"
    aspen.Tree.FindNode(steam_flow_path).Value = steam_mass
```

#### 3.3.5 Running Simulation

```python
def run_aspen_simulation(aspen):
    """
    Execute Aspen simulation and check status
    """
    # Run simulation
    aspen.Engine.Run2()

    # Check run status
    # 0 = converged, 1 = converged with warnings, 2+ = errors
    status = aspen.Tree.FindNode(r"\Data\Results Summary\Run-Status\Output\RUNID").Value

    return status
```

#### 3.3.6 Checking Convergence

```python
def check_convergence(aspen):
    """
    Verify simulation converged successfully
    """
    # Get convergence status
    status = aspen.Tree.FindNode(r"\Data\Results Summary\Run-Status\Output\RUNID").Value

    # Check individual block convergence
    blocks = ['REFORMER', 'HTS', 'LTS', 'FLASH', 'CO2REM', 'PSA']

    for block in blocks:
        block_status = aspen.Tree.FindNode(
            f"\\Data\\Blocks\\{block}\\Output\\BLKSTAT"
        ).Value

        if block_status != 'OK':
            print(f"Block {block} did not converge properly")
            return False

    return status in [0, 1]  # 0=OK, 1=OK with warnings
```

#### 3.3.7 Extracting Results

```python
def extract_results(aspen, input_row):
    """
    Extract all relevant results from Aspen simulation

    Returns:
        dict with all results to store in database
    """
    results = {
        'SimulationID': input_row['SimulationID'],
        'BiooilId': input_row['BiooilId'],
    }

    # Get H2 product stream properties
    h2_stream_path = r"\Data\Streams\H2PROD\Output"

    results['H2_FlowRate_kgh'] = aspen.Tree.FindNode(
        f"{h2_stream_path}\\MASSFLMX\\MIXED"
    ).Value

    results['H2_Purity_percent'] = aspen.Tree.FindNode(
        f"{h2_stream_path}\\MOLEFRAC\\MIXED\\H2"
    ).Value * 100.0

    # Get syngas composition at various points
    for location in ['REFORMER-OUT', 'HTS-OUT', 'LTS-OUT']:
        stream_path = f"\\Data\\Streams\\{location}\\Output"

        syngas_comp = {
            'Location': location,
            'H2_mol%': aspen.Tree.FindNode(f"{stream_path}\\MOLEFRAC\\MIXED\\H2").Value * 100,
            'CO_mol%': aspen.Tree.FindNode(f"{stream_path}\\MOLEFRAC\\MIXED\\CO").Value * 100,
            'CO2_mol%': aspen.Tree.FindNode(f"{stream_path}\\MOLEFRAC\\MIXED\\CO2").Value * 100,
            'CH4_mol%': aspen.Tree.FindNode(f"{stream_path}\\MOLEFRAC\\MIXED\\CH4").Value * 100,
            'Temperature_C': aspen.Tree.FindNode(f"{stream_path}\\TEMP_OUT\\MIXED").Value,
            'Pressure_bar': aspen.Tree.FindNode(f"{stream_path}\\PRES_OUT\\MIXED").Value
        }

        results[f'syngas_{location}'] = syngas_comp

    # Calculate derived metrics
    results['Carbon_Conversion_%'] = calculate_carbon_conversion(aspen)
    results['Energy_Efficiency_%'] = calculate_energy_efficiency(aspen)

    # Get mass and energy balances
    results['MassBalanceError_%'] = get_mass_balance_error(aspen)
    results['EnergyBalanceError_%'] = get_energy_balance_error(aspen)

    return results
```

---

### 3.4 Database Storage

#### 3.4.1 Storing Results

```python
def store_results(conn, results):
    """
    Store simulation results in database tables
    """
    cursor = conn.cursor()

    # 1. Insert into AspenSimulation
    cursor.execute("""
        INSERT INTO AspenSimulation
        (Biooil_Id, AspenVersion, ConvergenceStatus, MassBalanceError_percent,
         EnergyBalanceError_percent)
        VALUES (?, ?, ?, ?, ?)
    """, results['BiooilId'], 'Aspen Plus V12', 'Converged',
         results['MassBalanceError_%'], results['EnergyBalanceError_%'])

    simulation_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

    # 2. Insert into ReformingConditions
    cursor.execute("""
        INSERT INTO ReformingConditions
        (Simulation_Id, ReformerTemperature_C, ReformerPressure_bar,
         SteamToCarbonRatio, BiooilFeedRate_kgh)
        VALUES (?, ?, ?, ?, ?)
    """, simulation_id, results['Temperature_C'], results['Pressure_bar'],
         results['SC_Ratio'], 100.0)

    # 3. Insert into HydrogenProduct
    cursor.execute("""
        INSERT INTO HydrogenProduct
        (Simulation_Id, H2_Yield_kg, H2_Purity_percent, H2_FlowRate_kgh, ...)
        VALUES (?, ?, ?, ?, ...)
    """, simulation_id, results['H2_Yield_kg'], results['H2_Purity_percent'], ...)

    # 4. Insert into SyngasComposition (multiple rows)
    for location, comp in results['syngas_compositions'].items():
        cursor.execute("""
            INSERT INTO SyngasComposition
            (Simulation_Id, StreamLocation, H2_molpercent, CO_molpercent, ...)
            VALUES (?, ?, ?, ?, ...)
        """, simulation_id, location, comp['H2_mol%'], comp['CO_mol%'], ...)

    # 5. Insert into EnergyBalance
    cursor.execute("""
        INSERT INTO EnergyBalance
        (Simulation_Id, TotalEnergyInput_MJ, H2Product_HHV_MJ, ...)
        VALUES (?, ?, ?, ...)
    """, simulation_id, ...)

    conn.commit()
```

---

### 3.5 Error Handling & Recovery

#### 3.5.1 Error Types

**1. Convergence Failures**:
- Reformer doesn't converge
- Shift reactors have issues
- Flash separator problems

**Action**: Log failure, skip to next simulation

**2. Aspen Crashes**:
- COM interface disconnects
- Aspen hangs

**Action**: Restart Aspen, resume from checkpoint

**3. Database Errors**:
- Connection lost
- Constraint violations

**Action**: Reconnect, retry insert

#### 3.5.2 Checkpoint System

```python
def create_checkpoint(sim_id, status):
    """
    Save checkpoint after each simulation
    """
    checkpoint = {
        'last_completed_sim': sim_id,
        'timestamp': datetime.now(),
        'status': status
    }

    with open('checkpoint.json', 'w') as f:
        json.dump(checkpoint, f)

def resume_from_checkpoint():
    """
    Resume simulation batch from last checkpoint
    """
    if os.path.exists('checkpoint.json'):
        with open('checkpoint.json', 'r') as f:
            checkpoint = json.load(f)

        print(f"Resuming from simulation {checkpoint['last_completed_sim']}")
        return checkpoint['last_completed_sim']

    return 0  # Start from beginning
```

---

### 3.6 Validation & Quality Control

#### 3.6.1 Convergence Checks

For each simulation, verify:
- ✅ All blocks converged (status = 'OK')
- ✅ Iterations < 100 (reasonable convergence speed)
- ✅ No error messages in Aspen history

#### 3.6.2 Mass Balance Validation

```python
def validate_mass_balance(aspen):
    """
    Check overall mass balance error

    Should be < 0.1% for valid simulation
    """
    # Get input mass flow
    biooil_in = aspen.Tree.FindNode(
        r"\Data\Streams\BIOOIL\Output\MASSFLMX\MIXED"
    ).Value

    steam_in = aspen.Tree.FindNode(
        r"\Data\Streams\STEAM\Output\MASSFLMX\MIXED"
    ).Value

    total_in = biooil_in + steam_in

    # Get output mass flows
    h2_out = aspen.Tree.FindNode(
        r"\Data\Streams\H2PROD\Output\MASSFLMX\MIXED"
    ).Value

    co2_out = aspen.Tree.FindNode(
        r"\Data\Streams\CO2OUT\Output\MASSFLMX\MIXED"
    ).Value

    water_out = aspen.Tree.FindNode(
        r"\Data\Streams\WATER\Output\MASSFLMX\MIXED"
    ).Value

    tailgas_out = aspen.Tree.FindNode(
        r"\Data\Streams\TAILGAS\Output\MASSFLMX\MIXED"
    ).Value

    total_out = h2_out + co2_out + water_out + tailgas_out

    # Calculate error
    error_percent = abs(total_in - total_out) / total_in * 100

    if error_percent > 0.1:
        print(f"WARNING: Mass balance error = {error_percent:.4f}%")
        return False

    return True
```

#### 3.6.3 Energy Balance Validation

```python
def validate_energy_balance(aspen):
    """
    Check energy balance

    Should be < 1% for valid simulation
    """
    # Get energy inputs
    biooil_energy = get_stream_enthalpy(aspen, 'BIOOIL')
    steam_energy = get_stream_enthalpy(aspen, 'STEAM')
    reformer_duty = get_block_duty(aspen, 'REFORMER')
    preheater_duty = get_block_duty(aspen, 'PREHEAT')

    total_energy_in = biooil_energy + steam_energy + reformer_duty + preheater_duty

    # Get energy outputs
    h2_energy = get_stream_enthalpy(aspen, 'H2PROD')
    co2_energy = get_stream_enthalpy(aspen, 'CO2OUT')
    water_energy = get_stream_enthalpy(aspen, 'WATER')
    tailgas_energy = get_stream_enthalpy(aspen, 'TAILGAS')

    # Subtract heat removed by coolers
    cooler_duties = sum([get_block_duty(aspen, b) for b in ['COOLHTS', 'COOLLTS', 'COOLCOND']])

    total_energy_out = h2_energy + co2_energy + water_energy + tailgas_energy - cooler_duties

    # Calculate error
    error_percent = abs(total_energy_in - total_energy_out) / total_energy_in * 100

    if error_percent > 1.0:
        print(f"WARNING: Energy balance error = {error_percent:.4f}%")
        return False

    return True
```

#### 3.6.4 Physical Reasonableness Checks

```python
def validate_physical_reasonableness(results):
    """
    Check if results are physically reasonable
    """
    checks = {
        'H2_Yield': (0.05, 0.15),      # 5-15 kg H2 per 100 kg bio-oil
        'H2_Purity': (99.0, 100.0),    # >99% purity
        'Carbon_Conv': (70.0, 99.0),    # 70-99% conversion
        'CH4_Slip': (0.0, 10.0),        # <10% methane slip
        'CO_Slip': (0.0, 1.0),          # <1% CO in product
    }

    all_ok = True

    for param, (min_val, max_val) in checks.items():
        value = results.get(param)

        if value is None or value < min_val or value > max_val:
            print(f"WARNING: {param} = {value} is outside expected range [{min_val}, {max_val}]")
            all_ok = False

    return all_ok
```

---

### 3.7 Execution Plan

#### 3.7.1 Batch Strategy

**Option 1: Single Long Run** (Not Recommended)
- Run all 1,350 simulations continuously
- Risk: If crash occurs, lose progress

**Option 2: Batch Processing** (Recommended)
- Split into batches of 100 simulations
- Save checkpoint after each batch
- Can pause/resume

```python
def run_in_batches(input_matrix, batch_size=100):
    """
    Run simulations in batches with checkpoints
    """
    n_sims = len(input_matrix)
    n_batches = (n_sims + batch_size - 1) // batch_size

    for batch_num in range(n_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, n_sims)

        batch_data = input_matrix.iloc[start_idx:end_idx]

        print(f"\n=== BATCH {batch_num+1}/{n_batches} ===")
        print(f"Simulations {start_idx+1} to {end_idx}")

        run_simulation_batch(batch_data)

        create_checkpoint(end_idx, 'completed')

        print(f"Batch {batch_num+1} completed. Progress: {end_idx}/{n_sims}")
```

#### 3.7.2 Parallel Execution (Advanced)

If multiple Aspen licenses available:

```python
from multiprocessing import Pool

def run_parallel_simulations(input_matrix, n_processes=2):
    """
    Run simulations in parallel (requires multiple Aspen licenses)
    """
    # Split data
    chunks = np.array_split(input_matrix, n_processes)

    # Run in parallel
    with Pool(n_processes) as pool:
        results = pool.map(run_simulation_batch, chunks)

    return results
```

#### 3.7.3 Estimated Execution Time

**Assumptions**:
- Average simulation time: 5-10 seconds per run
- Total simulations: 1,350
- Convergence rate: 95% (5% failures, will retry)

**Time Estimate**:
- Sequential: 1,350 × 10 sec = 13,500 sec = **3.75 hours**
- With retries: ~4-5 hours
- Batch mode (100 at a time): ~30 minutes per batch, 14 batches = **7 hours** (including breaks)

**Recommendation**: Run overnight or over weekend

---

### 3.8 Deliverables

**Scripts** (in `reverse_ml_biooil_to_product/scripts/aspen_automation/`):

1. `aspen_connection.py` - COM interface utilities
2. `aspen_input_setter.py` - Set bio-oil composition and conditions
3. `aspen_result_extractor.py` - Extract results from Aspen
4. `aspen_validator.py` - Validation functions (mass/energy balance)
5. `database_inserter.py` - Store results in SQL database
6. `run_batch_simulations.py` - Main execution script
7. `checkpoint_manager.py` - Checkpoint and recovery functions

**Aspen Files** (in `reverse_ml_biooil_to_product/aspen_simulations/`):

1. `biooil_reforming_base.bkp` - Baseline Aspen model
2. `biooil_reforming_automated.bkp` - Model configured for automation
3. `README_aspen_setup.md` - Instructions for setting up Aspen model

**Logs** (in `reverse_ml_biooil_to_product/logs/`):

1. `simulation_log.csv` - Status of each simulation
2. `error_log.txt` - Detailed error messages
3. `checkpoint.json` - Resume point

---

## VALIDATION & QUALITY CONTROL

### Overall Quality Metrics

**Target Quality Standards**:
- ✅ Convergence rate: >95%
- ✅ Mass balance error: <0.1%
- ✅ Energy balance error: <1.0%
- ✅ Valid simulations: >1,200 out of 1,350 (89%)

### Final Data Quality Report

Generate report with:
- Total simulations attempted
- Converged simulations
- Failed simulations (with reasons)
- Average mass/energy balance errors
- Distribution of H₂ yields
- Range of process conditions covered

**Script**: `generate_quality_report.py`

---

## RISK ASSESSMENT

### Identified Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Database connection fails** | High | Medium | Implement retry logic, save to CSV backup |
| **Aspen crashes frequently** | High | Medium | Batch processing, checkpoints, error handling |
| **Low convergence rate (<80%)** | High | Low | Adjust initial guesses, relax tolerances, review flowsheet |
| **Insufficient data quality** | High | Low | Stringent validation, exclude bad simulations |
| **Automation script bugs** | Medium | Medium | Extensive testing with 10-20 test simulations first |
| **Hardware failure** | Medium | Low | Regular backups, cloud storage |
| **Time overrun** | Low | Medium | Start early, run overnight/weekend |

---

## TIMELINE & MILESTONES

### Gantt Chart (Text Format)

```
Week 1:
  Days 1-2: Phase 1 - Database Extension
    [■■] Create SQL scripts
    [■■] Execute in database
    [■■] Test with dummy data

  Days 3-5: Phase 2 - Reference Data Preparation
    [■■] Extract 30 bio-oil records
    [■■] Generate DOE matrix
    [■■] Create full simulation matrix
    [■■] Prepare surrogate mapping

Week 2:
  Days 1-3: Phase 3 Setup
    [■■■] Build Aspen model
    [■■■] Validate model manually
    [■■■] Write automation scripts

  Days 4-5: Testing & Debugging
    [■■] Test with 10 simulations
    [■■] Fix bugs
    [■■] Validate results

Week 3:
  Days 1-5: Production Runs
    [■■■■■] Run batches of simulations
    [■■■■■] Monitor and troubleshoot
    [■■■■■] Validate data quality
    [■■■■■] Generate quality report

Total Duration: 15 working days (3 weeks)
```

### Milestones

**M1**: Database schema complete and tested (Day 2)
**M2**: Reference data prepared and validated (Day 5)
**M3**: Aspen model validated manually (Day 8)
**M4**: Automation scripts complete (Day 10)
**M5**: First 100 simulations successful (Day 11)
**M6**: All simulations complete (Day 15)
**M7**: Data validated and quality report generated (Day 15)

---

## DELIVERABLES CHECKLIST

### Phase 1: Database Extension

- [ ] `01_create_tables.sql`
- [ ] `02_create_indexes.sql`
- [ ] `03_create_views.sql`
- [ ] `04_test_schema.sql`
- [ ] Database schema documentation
- [ ] Test results report

### Phase 2: Reference Data Preparation

- [ ] `extract_biooil_data.py`
- [ ] `analyze_biooil_statistics.py`
- [ ] `generate_doe_matrix.py`
- [ ] `create_simulation_matrix.py`
- [ ] `biooil_compositions_30.csv`
- [ ] `biooil_composition_statistics.csv`
- [ ] `doe_matrix.csv`
- [ ] `aspen_input_matrix.csv`
- [ ] `biooil_surrogate_components.csv`

### Phase 3: Aspen Automation

- [ ] `biooil_reforming_base.bkp` (Aspen model)
- [ ] `aspen_connection.py`
- [ ] `aspen_input_setter.py`
- [ ] `aspen_result_extractor.py`
- [ ] `aspen_validator.py`
- [ ] `database_inserter.py`
- [ ] `run_batch_simulations.py`
- [ ] `checkpoint_manager.py`
- [ ] `simulation_log.csv`
- [ ] `data_quality_report.pdf`

### Documentation

- [ ] Implementation plan (this document)
- [ ] Database schema diagram
- [ ] Aspen model documentation
- [ ] Automation user guide
- [ ] Troubleshooting guide
- [ ] Results validation report

---

## APPENDIX A: COMMAND REFERENCE

### Database Commands

```bash
# Run SQL scripts
sqlcmd -S DESKTOP-DRO84HP\SQLEXPRESS -d BIOOIL -i 01_create_tables.sql

# Backup database
sqlcmd -S DESKTOP-DRO84HP\SQLEXPRESS -Q "BACKUP DATABASE BIOOIL TO DISK='C:\Backup\BIOOIL_backup.bak'"
```

### Python Commands

```bash
# Install dependencies
pip install pyodbc pandas numpy pywin32

# Run data extraction
python extract_biooil_data.py

# Run Aspen automation
python run_batch_simulations.py --input aspen_input_matrix.csv --model biooil_reforming_base.bkp --batch-size 100
```

---

## APPENDIX B: CONTACT & SUPPORT

**Project Lead**: Orhun Uzdiyem
**Advisor**: Prof. Dr. Hayati OLGUN
**Institution**: Ege University - Solar Energy Institute

**Technical Support**:
- Aspen Plus: AspenTech documentation, support forums
- Python: Stack Overflow, GitHub issues
- SQL Server: Microsoft documentation

---

**Document Control**:
- Version: 1.0
- Created: 2025-11-16
- Last Modified: 2025-11-16
- Status: Draft - Awaiting Approval
- Next Review: After Phase 1 completion

---

**END OF IMPLEMENTATION PLAN**
