# Aspen Simulation Construction & Automation Guide
## Bio-oil Steam Reforming for Hydrogen Production

**Project**: Reverse ML - Bio-oil to Product
**Author**: Orhun Uzdiyem
**Date**: 2025-11-16
**Aspen Version**: Aspen Plus V12 (or similar)

---

## Table of Contents

1. [Overview](#overview)
2. [Process Flowsheet Design](#process-flowsheet-design)
3. [Step-by-Step Construction](#step-by-step-construction)
4. [Testing & Validation](#testing--validation)
5. [Automation Setup](#automation-setup)
6. [Troubleshooting](#troubleshooting)

---

## Overview

### Objective
Build an Aspen Plus simulation for bio-oil steam reforming that:
- Takes bio-oil composition (6 components) as input
- Simulates steam reforming process
- Outputs H₂ product properties (yield, purity, efficiency)
- Can be automated via Python COM interface

### Process Summary
```
Bio-oil + Steam → [Reformer] → Syngas → [WGS Reactors] →
    → [CO₂ Removal] → [PSA] → Pure H₂ Product
```

**Key Equipment**:
- Feed Mixer
- Pre-heater
- Steam Reformer (800-850°C)
- High-Temperature Shift (HTS, ~370°C)
- Low-Temperature Shift (LTS, ~210°C)
- Flash Separator
- CO₂ Removal Unit
- Pressure Swing Adsorption (PSA)

---

## Process Flowsheet Design

### Flowsheet Layout

```
BIOOIL (stream) ─┐
                 ├─→ [MIXER] ─→ [PREHEAT] ─→ [REFORMER] ─→ [HTS] ─→ [LTS] ─→ [FLASH] ─→ [CO2REM] ─→ [PSA] ─→ H2PROD
STEAM (stream) ──┘                                                                                             │
                                                                                                               └─→ TAILGAS
```

### Stream Names
| Stream | Description |
|--------|-------------|
| BIOOIL | Bio-oil feed (liquid) |
| STEAM | Steam feed |
| MIXED | Mixed feed after mixer |
| HEATED | Pre-heated feed |
| SYNGAS1 | Syngas from reformer |
| SYNGAS2 | Syngas after HTS |
| SYNGAS3 | Syngas after LTS |
| SYNGAS4 | Gas after flash separation |
| SYNGAS5 | Gas after CO₂ removal |
| H2PROD | Pure H₂ product |
| TAILGAS | PSA tail gas (off-gas) |
| WATER | Condensed water from flash |
| CO2OUT | CO₂ stream |

### Block Names
| Block | Type | Description |
|-------|------|-------------|
| BIOOILFEED | RYIELD | Bio-oil decomposition |
| MIXER | MIXER | Mix bio-oil components with steam |
| PREHEAT | HEATER | Pre-heat feed to reformer temp |
| REFORMER | RGIBBS | Steam reforming (Gibbs reactor) |
| HTS | RGIBBS | High-temp shift reactor |
| LTS | RGIBBS | Low-temp shift reactor |
| FLASH | FLASH2 | Water removal |
| CO2REM | SEP | CO₂ separation |
| PSA | SEP | H₂ purification |

---

## Step-by-Step Construction

### STEP 1: New Simulation Setup

1. **Open Aspen Plus**
   - File → New → Blank Simulation

2. **Setup → Specifications**
   - Type: `General with Metric Units`
   - Property Method: `PENG-ROB` (Peng-Robinson)
   - Save as: `biooil_reforming_base.bkp`

3. **Components → Specifications**
   Add the following components:
   ```
   Main Components:
   - TOLUENE (representative for aromatics)
   - ACETI-01 (acetic acid - representative for acids)
   - ETHANOL (representative for alcohols)
   - FURAN (representative for furans)
   - PHENOL (representative for phenols)
   - ACET-01 (acetone - representative for aldehyde&ketone)

   Process Components:
   - H2O (water/steam)
   - H2 (hydrogen)
   - CO (carbon monoxide)
   - CO2 (carbon dioxide)
   - CH4 (methane)
   - N2 (nitrogen - inert)
   ```

4. **Property Method**
   - Method: `PENG-ROB`
   - Good for high-pressure gas systems
   - Alternative: `RK-SOAVE` also suitable

---

### STEP 2: Define Input Streams

#### Bio-oil Feed Stream (BIOOIL)

**Location**: Streams → BIOOIL

**Specifications**:
```
Temperature: 25°C (ambient)
Pressure: 1 bar
Total Flow: 100 kg/h
Phase: Liquid

Composition (mass fraction):
- TOLUENE: 0.3287 (aromatics)
- ACETI-01: 0.1964 (acids)
- ETHANOL: 0.0630 (alcohols)
- FURAN: 0.0274 (furans)
- PHENOL: 0.0963 (phenols)
- ACET-01: 0.0653 (aldehyde&ketone)
- H2O: 0.2229 (moisture, if any)
```

**Note**: These values will be AUTOMATED later. Use these as initial guesses.

#### Steam Feed Stream (STEAM)

**Location**: Streams → STEAM

**Specifications**:
```
Temperature: 200°C (superheated)
Pressure: 20 bar
Total Flow: 200 kg/h
Phase: Vapor

Composition (mole fraction):
- H2O: 1.0
```

**Note**: Steam flow will be calculated from S/C ratio (automated).

---

### STEP 3: Build Process Blocks

#### Block 1: BIOOILFEED (RYIELD - Decomposer)

**Purpose**: Decompose bio-oil into elemental components for reforming

**Type**: `RYIELD` (Yield Reactor)

**Location**: Blocks → Model Palette → Reactors → RYIELD

**Configuration**:
```
Input: BIOOIL
Output: DECOMP (decomposed stream)

Specifications:
- Temperature: 25°C (isothermal)
- Pressure: 1 bar

Yield Distribution (Mass Basis):
The RYIELD block converts bio-oil components to:
- C (carbon)
- H2 (hydrogen)
- O2 (oxygen)
- N2 (nitrogen)
- H2O (water)

Set yields based on ultimate analysis of each component.
```

**Yield Tab Settings**:
```
For TOLUENE (C7H8):
  → C: 91.3%
  → H2: 8.7%

For ACETI-01 (CH3COOH):
  → C: 40.0%
  → H2: 6.7%
  → O2: 53.3%

For ETHANOL (C2H5OH):
  → C: 52.2%
  → H2: 13.0%
  → O2: 34.8%

[Continue for other components...]
```

**Alternative Approach**: Skip RYIELD and directly use actual components in reformer.

---

#### Block 2: MIXER (Mixer)

**Type**: `MIXER`

**Configuration**:
```
Inputs:
  - DECOMP (from RYIELD) or BIOOIL
  - STEAM

Output: MIXED

Specifications:
- Pressure: Minimum of inlet pressures
- No heat transfer
```

---

#### Block 3: PREHEAT (Heater)

**Type**: `HEATER`

**Configuration**:
```
Input: MIXED
Output: HEATED

Specifications:
- Temperature: 650-850°C (depends on reformer temp)
- Pressure: Reformer pressure (5-30 bar)
- Duty: Calculated
```

**Note**: This temperature will be AUTOMATED to match reformer inlet temp.

---

#### Block 4: REFORMER (Gibbs Reactor)

**Type**: `RGIBBS` (Gibbs Free Energy Minimization Reactor)

**Configuration**:
```
Input: HEATED
Output: SYNGAS1

Operating Conditions:
- Temperature: 650-850°C (VARIABLE - will be automated)
- Pressure: 5-30 bar (VARIABLE - will be automated)

Reactions:
The Gibbs reactor automatically calculates equilibrium for:
1. Steam reforming: CnHm + n·H2O → n·CO + (n+m/2)·H2
2. Water-gas shift: CO + H2O ⇌ CO2 + H2
3. Methanation: CO + 3H2 ⇌ CH4 + H2O
4. Boudouard: 2CO ⇌ C + CO2

Product Components (specify):
- H2
- CO
- CO2
- CH4
- H2O
- N2
- C (solid carbon - check "Allow solid phase")
```

**Specifications Tab**:
- Valid Phases: `Vapor-Liquid-Solid`
- Basis: `Gibbs Free Energy Minimization`

---

#### Block 5: HTS (High-Temperature Shift)

**Type**: `RGIBBS`

**Configuration**:
```
Input: SYNGAS1
Output: SYNGAS2

Operating Conditions:
- Temperature: 370°C (fixed or automated)
- Pressure: Same as inlet (isobaric)

Reaction:
CO + H2O ⇌ CO2 + H2 (exothermic)

Product Components:
- H2, CO, CO2, CH4, H2O, N2
```

---

#### Block 6: LTS (Low-Temperature Shift)

**Type**: `RGIBBS`

**Configuration**:
```
Input: SYNGAS2
Output: SYNGAS3

Operating Conditions:
- Temperature: 210°C
- Pressure: Same as inlet

Purpose: Further CO conversion to maximize H2
```

---

#### Block 7: FLASH (Flash Separator)

**Type**: `FLASH2`

**Configuration**:
```
Input: SYNGAS3
Outputs:
  - SYNGAS4 (vapor)
  - WATER (liquid)

Operating Conditions:
- Temperature: 40°C (cooling)
- Pressure: Same as inlet

Purpose: Remove condensed water before CO2 removal
```

---

#### Block 8: CO2REM (CO₂ Removal)

**Type**: `SEP` (Component Separator)

**Configuration**:
```
Input: SYNGAS4
Outputs:
  - SYNGAS5 (CO2-free gas)
  - CO2OUT (CO2 stream)

Separation Specifications:
- Split fraction for CO2: 0.95 (95% to CO2OUT)
- Split fraction for others: 0.01 (1% loss)

Component Splits:
  CO2 → CO2OUT: 95%
  H2 → SYNGAS5: 99%
  CO → SYNGAS5: 99%
  CH4 → SYNGAS5: 99%
  Other → SYNGAS5: 99%
```

---

#### Block 9: PSA (Pressure Swing Adsorption)

**Type**: `SEP` (Component Separator)

**Configuration**:
```
Input: SYNGAS5
Outputs:
  - H2PROD (pure H2 product)
  - TAILGAS (off-gas)

Operating Conditions:
- Pressure: 25 bar (high pressure)

Separation Specifications:
H2 Recovery: 85-92% (typical PSA)

Component Splits:
  H2 → H2PROD: 88% (adjust for realism)
  H2 → TAILGAS: 12%

  CO2 → TAILGAS: 99%
  CO → TAILGAS: 99%
  CH4 → TAILGAS: 99%
  N2 → TAILGAS: 99%

Purity Target: H2PROD should be >99.9% H2
```

**Pressure Specification**:
- H2PROD: 25 bar (product pressure)
- TAILGAS: 1 bar (vent pressure)

---

### STEP 4: Add Calculators (Optional but Recommended)

#### Calculator 1: S/C Ratio Calculator

**Purpose**: Automatically calculate steam flow based on bio-oil carbon content and desired S/C ratio

**Location**: Flowsheeting Options → Calculator

**Variables**:
```
Input Variables:
- BIOOIL.F (bio-oil flow, kg/h)
- S_C_RATIO (desired S/C ratio, e.g., 3.0)

Output Variables:
- STEAM.F (steam flow, kg/h)

Formula:
STEAM.F = BIOOIL.F × (C_content / 12) × 18 × S_C_RATIO

Where:
  C_content = carbon mass fraction in bio-oil (~50%)
  12 = molecular weight of carbon
  18 = molecular weight of water
```

#### Calculator 2: Energy Efficiency

**Purpose**: Calculate overall energy efficiency

**Variables**:
```
Efficiency = (H2PROD.HHV) / (BIOOIL.HHV + PREHEAT.DUTY + REFORMER.DUTY) × 100%
```

---

## Testing & Validation

### Test Case 1: Baseline Run

Use typical bio-oil composition and standard conditions:

```
Bio-oil Composition (mass %):
- Aromatics: 32.87%
- Acids: 19.64%
- Alcohols: 6.30%
- Furans: 2.74%
- Phenols: 9.63%
- Aldehyde&ketone: 6.53%
- Water: 22.29%

Process Conditions:
- Reformer Temp: 800°C
- Reformer Pressure: 15 bar
- S/C Ratio: 3.5
- Bio-oil Feed: 100 kg/h
```

**Run Simulation**:
1. Press `Next` button (or F5)
2. Wait for convergence

**Expected Results** (approximate):
```
H2 Yield: 8-12 kg per 100 kg bio-oil
H2 Purity: >99.5%
CO in H2 Product: <0.1%
Syngas Composition (Reformer outlet):
  - H2: 50-60 mol%
  - CO: 10-15 mol%
  - CO2: 15-20 mol%
  - CH4: 1-3 mol%
  - H2O: 10-20 mol%
```

### Validation Checks

**1. Mass Balance**
```
Tools → Results Summary → Material Balances
Check: Total mass in = Total mass out (error <0.1%)
```

**2. Energy Balance**
```
Tools → Results Summary → Energy Balances
Check: Total energy in = Total energy out + losses (error <1%)
```

**3. Convergence**
```
Check: "Results available" appears (green checkmark)
Warnings: Review any warnings in message window
```

**4. Physical Reasonableness**
```
- No negative flows
- Temperatures in reasonable ranges
- Pressures decrease along flowsheet (no pressure increases without pumps)
- H2 purity >99% from PSA
```

---

## Automation Setup

### Python COM Automation

Once the simulation converges manually, you can automate it using Python and the COM interface.

#### Prerequisites

```bash
pip install pywin32 pandas numpy
```

#### Basic Automation Script Structure

**File**: `aspen_automation_example.py`

```python
"""
Basic Aspen Automation Example
Demonstrates how to:
1. Connect to Aspen
2. Load simulation file
3. Change input parameters
4. Run simulation
5. Extract results
"""

import win32com.client as win32
import os

# ==============================================================================
# STEP 1: Connect to Aspen Plus
# ==============================================================================

print("Connecting to Aspen Plus...")
aspen = win32.Dispatch('Apwn.Document')

# Load your saved simulation
model_path = r"C:\@biyokomurlestirme\reverse_ml_biooil_to_product\aspen_simulations\process_flowsheet\biooil_reforming_base.bkp"
aspen.InitFromArchive2(model_path)

print("Model loaded successfully!")

# ==============================================================================
# STEP 2: Set Bio-oil Composition
# ==============================================================================

print("\nSetting bio-oil composition...")

# Path to RYIELD block for bio-oil composition
# If using RYIELD decomposer
biooil_path = r"\Data\Blocks\BIOOILFEED\Input\YIELD\MIXED"

# Set mass yields (fractions, must sum to 1.0)
aspen.Tree.FindNode(f"{biooil_path}\\TOLUENE").Value = 0.3287  # Aromatics
aspen.Tree.FindNode(f"{biooil_path}\\ACETI-01").Value = 0.1964  # Acids
aspen.Tree.FindNode(f"{biooil_path}\\ETHANOL").Value = 0.0630   # Alcohols
aspen.Tree.FindNode(f"{biooil_path}\\FURAN").Value = 0.0274     # Furans
aspen.Tree.FindNode(f"{biooil_path}\\PHENOL").Value = 0.0963    # Phenols
aspen.Tree.FindNode(f"{biooil_path}\\ACET-01").Value = 0.0653   # Aldehyde&ketone

# ==============================================================================
# STEP 3: Set Process Conditions
# ==============================================================================

print("Setting process conditions...")

# Reformer temperature (°C)
aspen.Tree.FindNode(r"\Data\Blocks\REFORMER\Input\TEMP").Value = 800.0

# Reformer pressure (bar)
aspen.Tree.FindNode(r"\Data\Blocks\REFORMER\Input\PRES").Value = 15.0

# Steam-to-Carbon ratio (via steam flow)
# Calculate steam flow based on S/C ratio = 3.5
biooil_flow = 100.0  # kg/h
sc_ratio = 3.5
carbon_moles = biooil_flow * 0.5 / 12  # Assume 50% carbon
steam_flow = carbon_moles * 18 * sc_ratio

aspen.Tree.FindNode(r"\Data\Streams\STEAM\Input\TOTFLOW\MIXED").Value = steam_flow

# ==============================================================================
# STEP 4: Run Simulation
# ==============================================================================

print("\nRunning simulation...")
aspen.Engine.Run2()

# Check convergence status
status = aspen.Tree.FindNode(r"\Data\Results Summary\Run-Status\Output\RUNID").Value

if "Converged" in str(status):
    print("Simulation converged successfully!")
else:
    print(f"Simulation failed or did not converge. Status: {status}")
    exit(1)

# ==============================================================================
# STEP 5: Extract Results
# ==============================================================================

print("\nExtracting results...")

# H2 Product Properties
h2_mass_flow = aspen.Tree.FindNode(
    r"\Data\Streams\H2PROD\Output\MASSFLMX\MIXED"
).Value

h2_mole_flow = aspen.Tree.FindNode(
    r"\Data\Streams\H2PROD\Output\MOLEFLMX\MIXED"
).Value

# H2 Purity (mole fraction)
h2_purity = aspen.Tree.FindNode(
    r"\Data\Streams\H2PROD\Output\MOLEFRAC\MIXED\H2"
).Value

# CO contamination (ppm)
co_molfrac = aspen.Tree.FindNode(
    r"\Data\Streams\H2PROD\Output\MOLEFRAC\MIXED\CO"
).Value
co_ppm = co_molfrac * 1e6

# Energy duty
reformer_duty = aspen.Tree.FindNode(
    r"\Data\Blocks\REFORMER\Output\QCALC"
).Value

print(f"\nResults:")
print(f"  H2 Mass Flow: {h2_mass_flow:.2f} kg/h")
print(f"  H2 Yield: {h2_mass_flow / biooil_flow:.2f} kg H2 / 100 kg bio-oil")
print(f"  H2 Purity: {h2_purity * 100:.2f}%")
print(f"  CO in H2: {co_ppm:.1f} ppm")
print(f"  Reformer Duty: {reformer_duty:.2f} MJ/h")

# ==============================================================================
# STEP 6: Close Aspen
# ==============================================================================

print("\nClosing Aspen...")
aspen.Close()
print("Done!")
```

---

### Key Aspen Tree Paths

#### Setting Input Parameters

**Stream Flow Rates**:
```python
# Mass flow (kg/h)
aspen.Tree.FindNode(r"\Data\Streams\BIOOIL\Input\TOTFLOW\MIXED").Value = 100.0

# Molar flow (kmol/h)
aspen.Tree.FindNode(r"\Data\Streams\STEAM\Input\TOTFLOW\MIXED\MOLE").Value = 5.0
```

**Stream Composition** (mole fractions):
```python
# Set mole fraction of H2O in steam
aspen.Tree.FindNode(r"\Data\Streams\STEAM\Input\MOLEFRAC\MIXED\H2O").Value = 1.0
```

**Block Temperatures**:
```python
aspen.Tree.FindNode(r"\Data\Blocks\REFORMER\Input\TEMP").Value = 800.0
aspen.Tree.FindNode(r"\Data\Blocks\HTS\Input\TEMP").Value = 370.0
aspen.Tree.FindNode(r"\Data\Blocks\LTS\Input\TEMP").Value = 210.0
```

**Block Pressures**:
```python
aspen.Tree.FindNode(r"\Data\Blocks\REFORMER\Input\PRES").Value = 15.0
```

#### Extracting Output Results

**Stream Properties**:
```python
# Temperature (°C)
temp = aspen.Tree.FindNode(r"\Data\Streams\H2PROD\Output\TEMP_OUT\MIXED").Value

# Pressure (bar)
pres = aspen.Tree.FindNode(r"\Data\Streams\H2PROD\Output\PRES_OUT\MIXED").Value

# Mass flow (kg/h)
mass = aspen.Tree.FindNode(r"\Data\Streams\H2PROD\Output\MASSFLMX\MIXED").Value

# Mole flow (kmol/h)
mole = aspen.Tree.FindNode(r"\Data\Streams\H2PROD\Output\MOLEFLMX\MIXED").Value
```

**Component Flows**:
```python
# H2 mass flow (kg/h)
h2_mass = aspen.Tree.FindNode(
    r"\Data\Streams\H2PROD\Output\MASSFLMX\MIXED\H2"
).Value

# CO2 mole flow (kmol/h)
co2_mole = aspen.Tree.FindNode(
    r"\Data\Streams\CO2OUT\Output\MOLEFLMX\MIXED\CO2"
).Value
```

**Component Fractions**:
```python
# H2 purity (mole fraction)
h2_purity = aspen.Tree.FindNode(
    r"\Data\Streams\H2PROD\Output\MOLEFRAC\MIXED\H2"
).Value

# CO contamination (mole fraction)
co_frac = aspen.Tree.FindNode(
    r"\Data\Streams\H2PROD\Output\MOLEFRAC\MIXED\CO"
).Value
```

**Energy Duties**:
```python
# Reformer duty (MJ/h)
duty = aspen.Tree.FindNode(r"\Data\Blocks\REFORMER\Output\QCALC").Value
```

---

### Finding Aspen Tree Paths

**Method 1: Use Aspen's Customize Feature**

1. In Aspen Plus, open your simulation
2. Right-click on any input/output field → `Customize`
3. The bottom of the window shows the full tree path
4. Copy this path for use in Python

**Method 2: Use Variable Explorer**

1. Tools → Variable Explorer
2. Browse through the tree structure
3. Find the variable you need
4. Copy the path

**Method 3: Trial and Error with Python**

```python
# Try to find a node
try:
    node = aspen.Tree.FindNode(r"\Data\Streams\H2PROD\Output\TEMP")
    print(f"Found: {node.Value}")
except:
    print("Node not found, try a different path")
```

---

## Full Automation Workflow

### Integration with Database

The complete automation workflow:

```
1. Read simulation matrix from CSV
   ↓
2. For each simulation (1-1170):
   a. Set bio-oil composition
   b. Set process conditions (T, P, S/C)
   c. Run Aspen simulation
   d. Check convergence
   e. Extract H2 product properties
   f. Store in database
   ↓
3. Validate results
   ↓
4. Use for ML training
```

**Example integration with your database**:

```python
import pyodbc
import pandas as pd
import win32com.client as win32

# Load simulation matrix
sim_matrix = pd.read_csv('aspen_input_matrix.csv')

# Connect to database
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DESKTOP-DRO84HP\\SQLEXPRESS;'
    'DATABASE=BIOOIL;'
    'Trusted_Connection=yes'
)

# Connect to Aspen
aspen = win32.Dispatch('Apwn.Document')
aspen.InitFromArchive2('biooil_reforming_base.bkp')

# Loop through simulations
for idx, row in sim_matrix.iterrows():
    print(f"\nSimulation {row['SimulationId']} / {len(sim_matrix)}")

    # Set inputs (bio-oil composition + process conditions)
    # ... (code from automation example)

    # Run simulation
    aspen.Engine.Run2()

    # Extract results
    # ... (code from automation example)

    # Store in database
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO AspenSimulation
        (Biooil_Id, ConvergenceStatus, ...)
        VALUES (?, ?, ...)
    """, (row['BiooilId'], 'Converged', ...))

    cursor.execute("""
        INSERT INTO HydrogenProduct
        (Simulation_Id, H2_Yield_kg, H2_Purity_percent, ...)
        VALUES (?, ?, ?, ...)
    """, (simulation_id, h2_yield, h2_purity, ...))

    conn.commit()

# Close connections
aspen.Close()
conn.close()
```

---

## Troubleshooting

### Common Issues

#### 1. Simulation Does Not Converge

**Symptoms**:
- "Calculations not available" message
- Red X on blocks

**Solutions**:
- Check initial guesses (Blocks → Input → Initialize)
- Reduce reformer temperature (try 750°C first)
- Increase maximum iterations (Run → Settings → Maximum Iterations)
- Check for unrealistic inputs (negative flows, impossible compositions)
- Use sequential modular mode instead of equation-oriented

#### 2. Gibbs Reactor Produces Solid Carbon

**Symptoms**:
- Solid carbon appears in reformer outlet
- Carbon deposits predicted

**Solutions**:
- Increase steam-to-carbon ratio (>3.0)
- Increase reformer temperature
- This is physically realistic but may cause operational issues in automation

#### 3. PSA Doesn't Achieve Target Purity

**Symptoms**:
- H2 purity <99%

**Solutions**:
- Adjust split fractions in SEP block
- Increase PSA operating pressure
- Reduce H2 recovery (trade-off: purity vs. recovery)

#### 4. Python COM Connection Fails

**Error**: `pywintypes.com_error: (-2147221005, 'Invalid class string')`

**Solutions**:
- Ensure Aspen Plus is installed
- Run Python as administrator
- Check Aspen version compatibility
- Try: `win32com.client.Dispatch('Apwn.Document.36.0')` (adjust version)

#### 5. Cannot Find Tree Path

**Error**: `Node not found`

**Solutions**:
- Use Aspen's Variable Explorer to verify path
- Check spelling (case-sensitive)
- Ensure simulation has been initialized
- Try running simulation manually first

---

## Advanced Topics

### Sensitivity Analysis

Run parametric studies automatically:

```python
temperatures = [650, 700, 750, 800, 850]
pressures = [5, 15, 25]

for T in temperatures:
    for P in pressures:
        # Set conditions
        aspen.Tree.FindNode(r"\Data\Blocks\REFORMER\Input\TEMP").Value = T
        aspen.Tree.FindNode(r"\Data\Blocks\REFORMER\Input\PRES").Value = P

        # Run and extract results
        aspen.Engine.Run2()
        # ... extract and save results
```

### Catalyst Deactivation Modeling

Add a `CALCULATOR` block to model catalyst deactivation:

```
Activity = exp(-kd × time)
Effective_Temp = Actual_Temp / Activity
```

### Heat Integration

Add heat exchangers to recover energy:
- Use hot reformer outlet to pre-heat feed
- Use HTS/LTS heat for steam generation

---

## Checklist Before Automation

- [ ] Manual simulation converges successfully
- [ ] Mass balance error <0.1%
- [ ] Energy balance error <1.0%
- [ ] H2 purity >99%
- [ ] All process conditions within realistic ranges
- [ ] Backup simulation file created
- [ ] Python environment with pywin32 installed
- [ ] Database connection tested
- [ ] Automation script tested on 3-5 test cases
- [ ] Error handling implemented in automation script
- [ ] Progress logging/checkpointing implemented

---

## Next Steps

1. **Build Baseline Model**: Follow Step-by-Step Construction guide
2. **Manual Validation**: Run test cases, check balances
3. **Test Automation**: Run Python script on 10 simulations
4. **Production Run**: Execute all 1,170 simulations
5. **Data Analysis**: Validate results in database
6. **ML Training**: Use collected data for reverse ML model

---

## References

- Aspen Plus User Guide (V12)
- Steam Reforming Process: See `steam_reforming_process_description.md`
- Database Schema: See `database/01_create_tables.sql`
- Implementation Plan: See `specs/IMPLEMENTATION_PLAN_DB_AND_ASPEN.md`

---

**Document Version**: 1.0
**Last Updated**: 2025-11-16
**Status**: Ready for Implementation (when Aspen is available)

