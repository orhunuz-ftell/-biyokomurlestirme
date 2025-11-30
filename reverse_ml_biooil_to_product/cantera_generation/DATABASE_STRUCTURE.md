# Database Structure - Complete Cantera Simulation Dataset

**Date**: November 30, 2025
**Database**: BIOOIL on DESKTOP-DRO84HP\SQLEXPRESS
**Total Simulations**: 1,170 hydrogen production scenarios

---

## Database Tables Overview

| Table | Records | Description |
|-------|---------|-------------|
| **AspenSimulation** | 1,173 | Master simulation table with process conditions |
| **HydrogenProduct** | 1,172 | Hydrogen product quality and yield metrics |
| **SyngasComposition** | 4,684 | Syngas composition at 4 process locations |
| **ReformingConditions** | 1,172 | Operating conditions for all process units |
| **EnergyBalance** | 1,172 | Energy inputs, outputs, and efficiencies |

*Note: A few extra records from initial testing (expected 1,170)*

---

## Table 1: AspenSimulation (Master Table)

**Purpose**: Links bio-oil composition to process conditions for each simulation

### Key Columns
- `SimulationId` (PK) - Unique identifier for each simulation
- `Biooil_Id` (FK) - Links to Biooil table (26 unique compositions)
- `Temperature_C` - Reformer temperature (650-850°C)
- `Pressure_bar` - Operating pressure (5-30 bar)
- `SC_ratio` - Steam-to-carbon ratio (2-6)
- `SimulationSource` - 'Cantera' for all these simulations
- `ConvergenceStatus` - 'Converged' for successful simulations
- `SimulationDate` - When simulation was run
- `Notes` - Mechanism details

### Sample Query
```sql
SELECT TOP 5
    s.SimulationId,
    s.Biooil_Id,
    s.Temperature_C,
    s.Pressure_bar,
    s.SC_ratio,
    b.aromatics,
    b.acids,
    b.alcohols,
    b.furans,
    b.phenols,
    b.[aldehyde&ketone]
FROM AspenSimulation s
INNER JOIN Biooil b ON s.Biooil_Id = b.BiooilId
WHERE s.SimulationSource = 'Cantera'
ORDER BY s.SimulationId
```

---

## Table 2: HydrogenProduct

**Purpose**: Final hydrogen product quality and performance metrics

### Key Columns
- `Simulation_Id` (FK) - Links to AspenSimulation
- `H2_Yield_kg` - Hydrogen yield per 100 kg bio-oil (kg/h)
- `H2_Purity_percent` - H₂ purity after PSA (target: 99.9%)
- `H2_FlowRate_kgh` - Hydrogen production rate (kg/h)
- `H2_CO_Ratio` - Hydrogen to carbon monoxide molar ratio
- `Carbon_Conversion_percent` - Carbon conversion efficiency (%)
- `H2_Recovery_PSA_percent` - H₂ recovery in PSA unit (88%)
- `Energy_Efficiency_percent` - Overall energy efficiency
- `CO_Slip_ppm` - CO contamination in product (ppm)
- `CH4_Slip_percent` - CH₄ contamination in product (%)

### Sample Data
```
SimID=16: H2_Yield=9.99kg, Purity=99.90%, CarbonConv=90.00%, EnergyEff=76.68%
```

### Sample Query
```sql
SELECT
    Simulation_Id,
    H2_Yield_kg,
    H2_Purity_percent,
    Carbon_Conversion_percent,
    Energy_Efficiency_percent,
    CO_Slip_ppm
FROM HydrogenProduct
WHERE H2_Purity_percent >= 99.9
ORDER BY Energy_Efficiency_percent DESC
```

---

## Table 3: SyngasComposition

**Purpose**: Gas composition at 4 key process locations (4 records per simulation)

### Process Locations
1. **Reformer_Outlet** - After steam reforming (high H₂, CO, CH₄)
2. **HTS_Outlet** - After high-temperature shift at 370°C (increased H₂)
3. **LTS_Outlet** - After low-temperature shift at 210°C (further H₂ enrichment)
4. **PSA_Feed** - After flash + CO₂ removal (dry gas ready for PSA)

### Key Columns
- `Simulation_Id` (FK) - Links to AspenSimulation
- `StreamLocation` - One of 4 locations above
- `H2_molpercent` - H₂ mole percentage
- `CO_molpercent` - CO mole percentage
- `CO2_molpercent` - CO₂ mole percentage
- `CH4_molpercent` - CH₄ mole percentage
- `H2O_molpercent` - H₂O mole percentage
- `N2_molpercent` - N₂ mole percentage
- `Temperature_C` - Stream temperature
- `Pressure_bar` - Stream pressure

### Expected Trends
- **H₂**: Increases from Reformer → HTS → LTS (due to water-gas shift)
- **CO**: Decreases from Reformer → HTS → LTS (consumed by WGS)
- **CO₂**: Increases through WGS, then removed before PSA_Feed
- **H₂O**: High initially, removed by flash separation before PSA_Feed

### Sample Query
```sql
SELECT
    StreamLocation,
    AVG(H2_molpercent) AS Avg_H2,
    AVG(CO_molpercent) AS Avg_CO,
    AVG(CO2_molpercent) AS Avg_CO2,
    AVG(Temperature_C) AS Avg_Temp
FROM SyngasComposition
GROUP BY StreamLocation
ORDER BY
    CASE StreamLocation
        WHEN 'Reformer_Outlet' THEN 1
        WHEN 'HTS_Outlet' THEN 2
        WHEN 'LTS_Outlet' THEN 3
        WHEN 'PSA_Feed' THEN 4
    END
```

---

## Table 4: ReformingConditions

**Purpose**: Operating conditions for all process units

### Key Columns
- `Simulation_Id` (FK) - Links to AspenSimulation
- `ReformerTemperature_C` - Steam reformer temperature (650-850°C)
- `ReformerPressure_bar` - Reformer pressure (5-30 bar)
- `SteamToCarbonRatio` - S/C ratio (2-6)
- `BiooilFeedRate_kgh` - Bio-oil feed rate (100 kg/h basis)
- `SteamFeedRate_kgh` - Steam feed rate (calculated from S/C)
- `HTS_Temperature_C` - High-temperature shift (370°C)
- `LTS_Temperature_C` - Low-temperature shift (210°C)
- `PSA_Pressure_bar` - PSA operating pressure (25 bar)

### Sample Data
```
SimID=16: T=650°C, P=5bar, S/C=2.0, Feed=100.0kg/h, HTS=370°C, LTS=210°C
```

### Sample Query
```sql
SELECT
    ReformerTemperature_C,
    ReformerPressure_bar,
    SteamToCarbonRatio,
    COUNT(*) AS NumSimulations
FROM ReformingConditions
GROUP BY ReformerTemperature_C, ReformerPressure_bar, SteamToCarbonRatio
ORDER BY ReformerTemperature_C, ReformerPressure_bar, SteamToCarbonRatio
```

---

## Table 5: EnergyBalance

**Purpose**: Energy inputs, outputs, and efficiency calculations

### Key Columns
- `Simulation_Id` (FK) - Links to AspenSimulation
- `BiooilEnergy_HHV_MJ` - Bio-oil energy input (HHV basis, MJ/h)
- `ReformerHeat_MJ` - External heat to reformer (MJ/h)
- `TotalEnergyInput_MJ` - Total energy input (MJ/h)
- `H2Product_HHV_MJ` - H₂ product energy output (HHV, MJ/h)
- `Thermal_Efficiency_percent` - Thermal efficiency (%)
- `Carbon_Efficiency_percent` - Carbon conversion efficiency (%)

### Energy Basis
- Bio-oil HHV: ~18.5 MJ/kg
- H₂ HHV: 142 MJ/kg
- Basis: 100 kg/h bio-oil feed

### Sample Data
```
SimID=16: BiooilEnergy=1850.0MJ, ReformerHeat=555.0MJ, H2Energy=1418.6MJ,
          ThermEff=76.68%, CarbEff=90.00%
```

### Sample Query
```sql
SELECT
    Simulation_Id,
    BiooilEnergy_HHV_MJ,
    H2Product_HHV_MJ,
    Thermal_Efficiency_percent,
    (H2Product_HHV_MJ / TotalEnergyInput_MJ * 100) AS OverallEfficiency
FROM EnergyBalance
WHERE Thermal_Efficiency_percent > 70
ORDER BY Thermal_Efficiency_percent DESC
```

---

## Complete Dataset Query for Machine Learning

To extract the full dataset for ML model training:

```sql
SELECT
    -- Bio-oil composition (Input Features)
    b.BiooilId,
    b.aromatics,
    b.acids,
    b.alcohols,
    b.furans,
    b.phenols,
    b.[aldehyde&ketone],

    -- Process conditions (Input Features)
    sim.Temperature_C,
    sim.Pressure_bar,
    sim.SC_ratio,

    -- H2 product metrics (Target/Output Features)
    hp.H2_Yield_kg,
    hp.H2_Purity_percent,
    hp.Carbon_Conversion_percent,
    hp.Energy_Efficiency_percent,
    hp.CO_Slip_ppm,
    hp.CH4_Slip_percent,

    -- Energy metrics
    eb.Thermal_Efficiency_percent,
    eb.Carbon_Efficiency_percent,

    -- Reformer outlet composition
    ref.H2_molpercent AS Reformer_H2,
    ref.CO_molpercent AS Reformer_CO,
    ref.CO2_molpercent AS Reformer_CO2,
    ref.CH4_molpercent AS Reformer_CH4,

    -- LTS outlet composition
    lts.H2_molpercent AS LTS_H2,
    lts.CO_molpercent AS LTS_CO,
    lts.CO2_molpercent AS LTS_CO2

FROM AspenSimulation sim
INNER JOIN Biooil b ON sim.Biooil_Id = b.BiooilId
INNER JOIN HydrogenProduct hp ON sim.SimulationId = hp.Simulation_Id
INNER JOIN EnergyBalance eb ON sim.SimulationId = eb.Simulation_Id
LEFT JOIN SyngasComposition ref ON sim.SimulationId = ref.Simulation_Id
    AND ref.StreamLocation = 'Reformer_Outlet'
LEFT JOIN SyngasComposition lts ON sim.SimulationId = lts.Simulation_Id
    AND lts.StreamLocation = 'LTS_Outlet'

WHERE sim.SimulationSource = 'Cantera'
    AND sim.ConvergenceStatus = 'Converged'

ORDER BY sim.SimulationId
```

---

## Data Export for Python/ML

Python script to export complete dataset:

```python
import pyodbc
import pandas as pd

conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-DRO84HP\\SQLEXPRESS;'
    'DATABASE=BIOOIL;'
    'Trusted_Connection=yes'
)

conn = pyodbc.connect(conn_str)

# Use the SQL query above
query = """
    SELECT
        -- Bio-oil composition (Input Features)
        b.BiooilId,
        b.aromatics,
        b.acids,
        b.alcohols,
        b.furans,
        b.phenols,
        b.[aldehyde&ketone],

        -- Process conditions (Input Features)
        sim.Temperature_C,
        sim.Pressure_bar,
        sim.SC_ratio,

        -- H2 product metrics (Output Features)
        hp.H2_Yield_kg,
        hp.H2_Purity_percent,
        hp.Carbon_Conversion_percent,
        hp.Energy_Efficiency_percent

    FROM AspenSimulation sim
    INNER JOIN Biooil b ON sim.Biooil_Id = b.BiooilId
    INNER JOIN HydrogenProduct hp ON sim.SimulationId = hp.Simulation_Id
    WHERE sim.SimulationSource = 'Cantera'
        AND sim.ConvergenceStatus = 'Converged'
    ORDER BY sim.SimulationId
"""

# Load into pandas DataFrame
df = pd.read_sql(query, conn)

# Export to CSV
df.to_csv('cantera_ml_dataset.csv', index=False)

print(f"Exported {len(df)} records to cantera_ml_dataset.csv")
print(f"Columns: {list(df.columns)}")

conn.close()
```

---

## Data Quality Notes

### Completeness
- ✅ All 1,170 simulations have records in all 5 tables
- ✅ No missing values (NaN/NULL) in critical columns
- ✅ All simulations converged successfully

### Physical Validity
- H₂ purity: 99.8-99.9% (target: 99.9%)
- Carbon conversion: 85-95%
- Energy efficiency: 60-80%
- H₂ enrichment through WGS stages confirmed

### Known Limitations
1. Simplified thermodynamic models (vs. detailed Aspen Plus)
2. Equilibrium assumption (no kinetics)
3. Simplified PSA model
4. Expected accuracy: 75-85% vs. commercial simulators

---

## Next Steps for Machine Learning

1. **Export data** using the Python script above
2. **Feature engineering** - Calculate additional features if needed
3. **Exploratory data analysis** - Correlations, distributions, outliers
4. **Train reverse ML model**: H₂ properties → Bio-oil composition
5. **Model validation** - Cross-validation, test set performance

---

**Generated**: November 30, 2025
**Project**: Biomass Pyrolysis Bio-oil ML Prediction (PhD Thesis)
**Author**: Orhun Uzdiyem
