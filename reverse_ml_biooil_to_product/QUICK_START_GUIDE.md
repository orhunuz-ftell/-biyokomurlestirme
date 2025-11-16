# Quick Start Guide - Reverse ML Project

## Step-by-Step Implementation

### Step 1: Process Selection ✋ **START HERE**

1. Review potential processes in literature
2. Fill out `docs/process_selection_template.md`
3. Get approval from advisors/team
4. Document selection rationale

**Key Questions:**
- Which downstream process uses bio-oil as feedstock?
- Is thermodynamic/kinetic data available?
- Can the process be modeled in Aspen?

---

### Step 2: Aspen Model Development

1. **Setup Aspen Project**
   - Create new Aspen Plus/HYSYS file
   - Save in `aspen_simulations/process_flowsheet/`

2. **Define Components**
   - Bio-oil pseudo-components
   - Reaction products
   - Solvents, gases, catalysts

3. **Select Property Method**
   - Based on process chemistry
   - Validate against literature

4. **Build Flowsheet**
   - Add unit operations
   - Connect streams
   - Set specifications

5. **Validate Model**
   - Compare with literature data
   - Check mass/energy balances
   - Verify convergence

---

### Step 3: Prepare Bio-oil Reference Data

1. **Extract from Original Project Database**
   ```python
   # Example: Get bio-oil composition ranges
   import pyodbc
   conn = pyodbc.connect('DRIVER={SQL Server};SERVER=...;DATABASE=BIOOIL;...')
   query = "SELECT aromatics, acids, alcohols, phenols, furans, aldehyde_ketone FROM Biooil"
   biooil_data = pd.read_sql(query, conn)
   ```

2. **Analyze Ranges**
   - Min, max, mean for each component
   - Realistic combinations
   - Correlations between components

3. **Save Reference Data**
   - Save to `data/biooil_reference_data/`
   - Document ranges for simulation inputs

---

### Step 4: Design Simulation Experiments

1. **Create DOE Matrix**
   - Bio-oil composition variations
   - Process variable variations
   - Latin Hypercube or Full Factorial

2. **Example Structure:**
   ```python
   import pandas as pd
   from scipy.stats import qmc

   # Define ranges
   ranges = {
       'aromatics': [10, 40],
       'acids': [5, 30],
       'phenols': [10, 35],
       # ... other components
       'temperature': [300, 450],
       'pressure': [50, 100]
   }

   # Generate DOE samples
   sampler = qmc.LatinHypercube(d=len(ranges))
   samples = sampler.random(n=500)  # 500 simulations

   # Save DOE matrix
   doe_df.to_csv('aspen_simulations/simulation_data/doe_matrix.csv')
   ```

---

### Step 5: Automate Aspen Simulations

1. **Install Required Packages**
   ```bash
   pip install pywin32 pandas numpy
   ```

2. **Create Automation Script**
   - Use template in `aspen_simulations/automation_scripts/`
   - Connect to Aspen via COM
   - Loop through DOE matrix
   - Set input variables
   - Run simulation
   - Extract output variables
   - Save results

3. **Example Script Structure:**
   ```python
   import win32com.client as win32
   import pandas as pd

   # Connect to Aspen
   aspen = win32.Dispatch('Apwn.Document')
   aspen.InitFromArchive2('path/to/model.bkp')

   # Loop through experiments
   for idx, row in doe_df.iterrows():
       # Set bio-oil composition
       aspen.Tree.FindNode(r"\Data\Streams\BIOOIL\Input\FLOW\...").Value = row['aromatics']

       # Run simulation
       aspen.Engine.Run2()

       # Extract results
       results[idx] = aspen.Tree.FindNode(r"\Data\Streams\PRODUCT\Output\...").Value
   ```

---

### Step 6: Generate Training Dataset

1. **Run Batch Simulations**
   - Execute automation script
   - Monitor for convergence issues
   - Handle errors gracefully

2. **Collect Results**
   - Product compositions
   - Product properties
   - Process conditions
   - Performance metrics

3. **Quality Control**
   - Check for failed simulations
   - Verify mass balances
   - Remove outliers

4. **Save Raw Data**
   - Save to `data/raw/simulation_results.csv`
   - Include metadata (date, convergence status, etc.)

---

### Step 7: Prepare ML Dataset

1. **Run Data Preparation Script**
   ```bash
   cd ml_models
   python data_preparation.py
   ```

2. **Review Processed Data**
   - Check `data/processed/` folder
   - Verify train-test split
   - Inspect feature distributions

---

### Step 8: Train ML Models

1. **Run Training Script**
   ```bash
   python train_models.py
   ```

2. **Evaluate Performance**
   - Check R² scores
   - Review feature importance
   - Validate predictions

3. **Save Models**
   - Models saved to `ml_models/trained_models/`
   - Document performance metrics

---

### Step 9: Create Prediction Tool

1. **Develop Interface**
   - Load trained models
   - Input: Desired product specs
   - Output: Required bio-oil composition

2. **Validate Predictions**
   - Test with new Aspen simulations
   - Compare predicted vs actual

---

### Step 10: Documentation and Results

1. **Write Technical Report**
   - Methodology
   - Results
   - Validation

2. **Create Visualizations**
   - Save to `results/figures/`

3. **Prepare Publication**
   - Draft paper
   - Include in thesis

---

## File Checklist

Before starting ML development, ensure you have:

- [ ] Process selection document completed
- [ ] Validated Aspen model
- [ ] Bio-oil reference data from original project
- [ ] DOE matrix created
- [ ] Automation script tested
- [ ] Raw simulation data collected (min. 200-500 runs)
- [ ] Data quality verified

---

## Common Issues and Solutions

### Aspen Automation Issues
- **Problem**: COM connection fails
- **Solution**: Ensure Aspen is properly licensed and installed

### Convergence Problems
- **Problem**: Many simulations fail to converge
- **Solution**: Narrow input ranges, adjust initial estimates

### Insufficient Data
- **Problem**: Not enough valid simulations
- **Solution**: Expand DOE, adjust constraints

---

## Need Help?

Refer to:
- `PROJECT_SPECIFICATION.md` for detailed methodology
- `docs/process_selection_template.md` for process documentation
- Original project database for bio-oil reference data

---

**Last Updated**: 2025-11-16
