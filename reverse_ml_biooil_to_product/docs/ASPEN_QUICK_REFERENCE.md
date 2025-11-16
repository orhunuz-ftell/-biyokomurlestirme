# Aspen Automation Quick Reference Card
## Essential Information at a Glance

---

## Process Flowsheet Summary

```
BIOOIL + STEAM → [MIXER] → [PREHEAT] → [REFORMER 800°C] →
  → [HTS 370°C] → [LTS 210°C] → [FLASH 40°C] →
  → [CO2 Removal] → [PSA] → H2 PRODUCT (>99% purity)
```

---

## Block Configuration Quick List

| Block | Type | Temp (°C) | Pressure (bar) | Key Setting |
|-------|------|-----------|----------------|-------------|
| BIOOILFEED | RYIELD | 25 | 1 | Yield distribution |
| MIXER | MIXER | - | Min(inlets) | - |
| PREHEAT | HEATER | Match reformer | 15-20 | Heat to reformer temp |
| REFORMER | RGIBBS | 650-850 | 5-30 | Equilibrium |
| HTS | RGIBBS | 370 | Same | WGS reaction |
| LTS | RGIBBS | 210 | Same | WGS reaction |
| FLASH | FLASH2 | 40 | Same | Water removal |
| CO2REM | SEP | - | Same | 95% CO2 removal |
| PSA | SEP | - | 25 | 88% H2 recovery |

---

## Components List

**Bio-oil Surrogates**:
```
- TOLUENE     (aromatics)
- ACETI-01    (acids)
- ETHANOL     (alcohols)
- FURAN       (furans)
- PHENOL      (phenols)
- ACET-01     (aldehyde&ketone)
```

**Process Gases**:
```
- H2O, H2, CO, CO2, CH4, N2
```

**Property Method**: PENG-ROB

---

## Typical Operating Conditions

```
Bio-oil Feed:     100 kg/h at 25°C, 1 bar
Steam Feed:       200 kg/h at 200°C, 20 bar
S/C Ratio:        2.0 - 6.0 (typical: 3.5)
Reformer Temp:    650-850°C (optimal: 800°C)
Reformer Press:   5-30 bar (typical: 15 bar)
```

---

## Expected Results (Typical Run)

```
H2 Yield:         8-12 kg per 100 kg bio-oil
H2 Purity:        >99.5%
CO in H2:         <1000 ppm (0.1%)
Carbon Conv:      85-95%
Energy Eff:       60-70%

Syngas Composition (after Reformer):
  H2:    50-60 mol%
  CO:    10-15 mol%
  CO2:   15-20 mol%
  CH4:   1-3 mol%
  H2O:   10-20 mol%
```

---

## Python Automation - Essential Code

### Connect to Aspen

```python
import win32com.client as win32

aspen = win32.Dispatch('Apwn.Document')
aspen.InitFromArchive2(r"C:\path\to\biooil_reforming_base.bkp")
```

### Set Bio-oil Composition (RYIELD)

```python
base_path = r"\Data\Blocks\BIOOILFEED\Input\YIELD\MIXED"

aspen.Tree.FindNode(f"{base_path}\\TOLUENE").Value = 0.3287
aspen.Tree.FindNode(f"{base_path}\\ACETI-01").Value = 0.1964
aspen.Tree.FindNode(f"{base_path}\\ETHANOL").Value = 0.0630
aspen.Tree.FindNode(f"{base_path}\\FURAN").Value = 0.0274
aspen.Tree.FindNode(f"{base_path}\\PHENOL").Value = 0.0963
aspen.Tree.FindNode(f"{base_path}\\ACET-01").Value = 0.0653
```

### Set Process Conditions

```python
# Reformer temperature (°C)
aspen.Tree.FindNode(r"\Data\Blocks\REFORMER\Input\TEMP").Value = 800.0

# Reformer pressure (bar)
aspen.Tree.FindNode(r"\Data\Blocks\REFORMER\Input\PRES").Value = 15.0

# Steam flow (kg/h)
aspen.Tree.FindNode(r"\Data\Streams\STEAM\Input\TOTFLOW\MIXED").Value = 200.0
```

### Run Simulation

```python
aspen.Engine.Run2()

# Check status
status = aspen.Tree.FindNode(
    r"\Data\Results Summary\Run-Status\Output\RUNID"
).Value

if "Converged" in str(status):
    print("Success!")
```

### Extract H2 Product Properties

```python
# Mass flow (kg/h)
h2_flow = aspen.Tree.FindNode(
    r"\Data\Streams\H2PROD\Output\MASSFLMX\MIXED"
).Value

# Purity (mole fraction)
h2_purity = aspen.Tree.FindNode(
    r"\Data\Streams\H2PROD\Output\MOLEFRAC\MIXED\H2"
).Value

# CO contamination (ppm)
co_frac = aspen.Tree.FindNode(
    r"\Data\Streams\H2PROD\Output\MOLEFRAC\MIXED\CO"
).Value
co_ppm = co_frac * 1e6

# Temperature (°C)
temp = aspen.Tree.FindNode(
    r"\Data\Streams\H2PROD\Output\TEMP_OUT\MIXED"
).Value

# Pressure (bar)
pres = aspen.Tree.FindNode(
    r"\Data\Streams\H2PROD\Output\PRES_OUT\MIXED"
).Value
```

### Extract Syngas Composition (at each location)

```python
streams = ['SYNGAS1', 'SYNGAS2', 'SYNGAS3', 'SYNGAS4']
components = ['H2', 'CO', 'CO2', 'CH4', 'H2O', 'N2']

for stream in streams:
    for comp in components:
        molfrac = aspen.Tree.FindNode(
            rf"\Data\Streams\{stream}\Output\MOLEFRAC\MIXED\{comp}"
        ).Value
        print(f"{stream} - {comp}: {molfrac*100:.2f}%")
```

### Extract Energy Data

```python
# Reformer duty (MJ/h)
reformer_duty = aspen.Tree.FindNode(
    r"\Data\Blocks\REFORMER\Output\QCALC"
).Value

# Preheater duty (MJ/h)
preheat_duty = aspen.Tree.FindNode(
    r"\Data\Blocks\PREHEAT\Output\QCALC"
).Value
```

### Close Aspen

```python
aspen.Close()
```

---

## Common Tree Paths

### Input Paths (Setting Values)

```
Stream Flow:
\Data\Streams\{STREAM_NAME}\Input\TOTFLOW\MIXED

Stream Temperature:
\Data\Streams\{STREAM_NAME}\Input\TEMP\MIXED

Stream Pressure:
\Data\Streams\{STREAM_NAME}\Input\PRES\MIXED

Block Temperature:
\Data\Blocks\{BLOCK_NAME}\Input\TEMP

Block Pressure:
\Data\Blocks\{BLOCK_NAME}\Input\PRES

Component Mole Fraction:
\Data\Streams\{STREAM_NAME}\Input\MOLEFRAC\MIXED\{COMPONENT}

RYIELD Distribution:
\Data\Blocks\BIOOILFEED\Input\YIELD\MIXED\{COMPONENT}
```

### Output Paths (Extracting Results)

```
Stream Mass Flow:
\Data\Streams\{STREAM_NAME}\Output\MASSFLMX\MIXED

Stream Mole Flow:
\Data\Streams\{STREAM_NAME}\Output\MOLEFLMX\MIXED

Component Mass Flow:
\Data\Streams\{STREAM_NAME}\Output\MASSFLMX\MIXED\{COMPONENT}

Component Mole Fraction:
\Data\Streams\{STREAM_NAME}\Output\MOLEFRAC\MIXED\{COMPONENT}

Stream Temperature:
\Data\Streams\{STREAM_NAME}\Output\TEMP_OUT\MIXED

Stream Pressure:
\Data\Streams\{STREAM_NAME}\Output\PRES_OUT\MIXED

Block Heat Duty:
\Data\Blocks\{BLOCK_NAME}\Output\QCALC

Convergence Status:
\Data\Results Summary\Run-Status\Output\RUNID
```

---

## Database Storage Mapping

Map Aspen outputs to database columns:

### AspenSimulation Table

```python
cursor.execute("""
    INSERT INTO AspenSimulation (
        Biooil_Id, SimulationDate, AspenVersion,
        ConvergenceStatus, MassBalanceError_percent,
        EnergyBalanceError_percent, ValidationFlag
    ) VALUES (?, GETDATE(), ?, ?, ?, ?, ?)
""", (biooil_id, 'V12', status, mass_err, energy_err, 0))

simulation_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
```

### ReformingConditions Table

```python
cursor.execute("""
    INSERT INTO ReformingConditions (
        Simulation_Id,
        ReformerTemperature_C, ReformerPressure_bar,
        SteamToCarbonRatio,
        BiooilFeedRate_kgh, SteamFeedRate_kgh,
        HTS_Temperature_C, LTS_Temperature_C, PSA_Pressure_bar
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (simulation_id, T_reformer, P_reformer, SC_ratio,
      biooil_flow, steam_flow, 370, 210, 25))
```

### HydrogenProduct Table

```python
cursor.execute("""
    INSERT INTO HydrogenProduct (
        Simulation_Id,
        H2_Yield_kg, H2_Purity_percent,
        H2_FlowRate_kgh, H2_FlowRate_Nm3h,
        H2_CO_Ratio, H2_CO2_Ratio,
        CO_Slip_ppm, CH4_Slip_percent,
        Carbon_Conversion_percent,
        H2_Recovery_PSA_percent,
        Energy_Efficiency_percent
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (simulation_id, h2_yield, h2_purity, h2_mass_flow,
      h2_vol_flow, h2_co_ratio, h2_co2_ratio,
      co_ppm, ch4_pct, carbon_conv, h2_recovery, efficiency))
```

### SyngasComposition Table

```python
locations = [
    ('Reformer_Out', 'SYNGAS1'),
    ('HTS_Out', 'SYNGAS2'),
    ('LTS_Out', 'SYNGAS3'),
    ('PSA_In', 'SYNGAS4')
]

for loc_name, stream_name in locations:
    cursor.execute("""
        INSERT INTO SyngasComposition (
            Simulation_Id, StreamLocation,
            H2_molpercent, CO_molpercent, CO2_molpercent,
            CH4_molpercent, H2O_molpercent, N2_molpercent,
            Temperature_C, Pressure_bar, MassFlowRate_kgh
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (simulation_id, loc_name, h2_pct, co_pct, co2_pct,
          ch4_pct, h2o_pct, n2_pct, temp, pres, mass_flow))
```

---

## Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Won't converge | Lower reformer temp to 750°C, increase S/C to 4.0 |
| Solid carbon | Increase S/C ratio >3.5 |
| Low H2 purity | Adjust PSA split fractions, check CO2 removal |
| Negative flows | Check initial guesses, reinitialize |
| Python can't connect | Run as admin, check Aspen version in Dispatch() |
| Path not found | Use Variable Explorer in Aspen to verify path |
| Mass imbalance | Check separator split fractions sum correctly |

---

## Validation Checklist

- [ ] Simulation converges (green checkmark)
- [ ] Mass balance error <0.1%
- [ ] Energy balance error <1.0%
- [ ] H2 purity >99%
- [ ] No negative flows
- [ ] S/C ratio between 2-6
- [ ] Temperature range: Reformer 650-850°C
- [ ] Pressure reasonable (5-30 bar)
- [ ] Results physically sensible

---

## Automation Loop Template

```python
import pandas as pd
import win32com.client as win32
import pyodbc

# Load inputs
df = pd.read_csv('aspen_input_matrix.csv')

# Connect
aspen = win32.Dispatch('Apwn.Document')
aspen.InitFromArchive2('model.bkp')
conn = pyodbc.connect('...')

# Loop
for idx, row in df.iterrows():
    try:
        # 1. Set inputs
        # ... set bio-oil composition
        # ... set T, P, S/C

        # 2. Run
        aspen.Engine.Run2()

        # 3. Check convergence
        status = aspen.Tree.FindNode(
            r"\Data\Results Summary\Run-Status\Output\RUNID"
        ).Value

        if "Converged" not in str(status):
            print(f"Sim {idx} failed")
            continue

        # 4. Extract results
        # ... get H2 properties

        # 5. Store in database
        cursor = conn.cursor()
        # ... INSERT statements
        conn.commit()

        print(f"Sim {idx} complete")

    except Exception as e:
        print(f"Error in sim {idx}: {e}")
        continue

# Cleanup
aspen.Close()
conn.close()
```

---

## File Locations

```
Simulation File:
C:\@biyokomurlestirme\reverse_ml_biooil_to_product\
  aspen_simulations\process_flowsheet\biooil_reforming_base.bkp

Input Data:
C:\@biyokomurlestirme\reverse_ml_biooil_to_product\
  data\biooil_reference_data\aspen_input_matrix.csv

Automation Scripts:
C:\@biyokomurlestirme\reverse_ml_biooil_to_product\
  scripts\phase3_aspen_automation\
```

---

## Performance Targets

```
Total Simulations: 1,170 (26 bio-oils × 45 conditions)
Target Success Rate: >89% (>1,040 converged)
Time per Simulation: 10-20 seconds
Total Time: 3-6 hours
```

---

## Emergency Contacts

- **Aspen Support**: Check your license agreement
- **Full Guide**: See `ASPEN_SIMULATION_GUIDE.md`
- **Process Details**: See `steam_reforming_process_description.md`
- **Database Schema**: See `database/01_create_tables.sql`

---

**Keep this document handy while building and automating!**

**Version**: 1.0 | **Date**: 2025-11-16
