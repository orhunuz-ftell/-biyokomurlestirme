# Reverse Machine Learning: Product-to-Bio-oil Property Prediction

## Project Overview

This project implements a **reverse machine learning approach** where we predict bio-oil properties based on desired product characteristics from a downstream chemical process.

---

## Methodology Flow

```
Bio-oil Properties → [Aspen Simulation] → Product Properties
        ↑                                         ↓
        └─────────[Machine Learning Model]────────┘
```

### Traditional Approach (Original Project)
- **ML Input**: Biomass properties + Process conditions
- **ML Output**: Bio-oil yield + Bio-oil composition

### New Reverse Approach (This Project)
- **Process Input**: Bio-oil with known composition
- **Process Output**: Product with specific properties (simulated in Aspen)
- **ML Input**: Product properties from Aspen simulation
- **ML Output**: Required bio-oil properties

---

## Project Objectives

1. **Select a chemical process** that uses bio-oil as feedstock
2. **Simulate the process in Aspen Plus/HYSYS** with various bio-oil compositions
3. **Generate training data** by running multiple simulations with different bio-oil inputs
4. **Train ML models** to predict required bio-oil properties from desired product specifications
5. **Enable reverse engineering** of bio-oil composition for target product quality

---

## Data Structure

### Machine Learning Inputs (Features)
Properties of the **product** obtained from Aspen simulation:
- Product composition (chemical species concentrations)
- Product physical properties (density, viscosity, boiling point, etc.)
- Product quality metrics (purity, yield, conversion rate, etc.)
- Process operating conditions (temperature, pressure, flow rates)
- Energy consumption
- Economic indicators (if applicable)

*Note: Specific features will be defined after process selection*

### Machine Learning Outputs (Targets)
Properties of the **bio-oil** (process feedstock):
- **LiquidOutput** - Total bio-oil available (%)
- **aromatics** - Aromatic compounds content (%)
- **acids** - Organic acids content (%)
- **alcohols** - Alcohol compounds content (%)
- **furans** - Furan compounds content (%)
- **phenols** - Phenolic compounds content (%)
- **aldehyde_ketone** - Aldehydes and ketones content (%)
- **esters** - Ester compounds content (%)
- **aliphatichydrocarbon** - Aliphatic hydrocarbons content (%)
- Other relevant bio-oil properties

---

## Implementation Steps

### Phase 1: Process Selection and Simulation Setup
1. **Select downstream chemical process**
   - Bio-oil upgrading (hydrodeoxygenation, catalytic cracking, etc.)
   - Bio-fuel production (biodiesel, bio-gasoline, etc.)
   - Biochemical production (platform chemicals, solvents, etc.)

2. **Setup Aspen simulation model**
   - Define process flowsheet
   - Select thermodynamic models
   - Configure unit operations
   - Set operating conditions

3. **Validate simulation model**
   - Compare with literature data
   - Verify mass and energy balances
   - Check physical property predictions

### Phase 2: Data Generation
1. **Define bio-oil composition ranges**
   - Use historical data from original project as reference
   - Define realistic variation ranges for each component

2. **Design simulation experiments**
   - Create Design of Experiments (DOE) matrix
   - Include process variable variations
   - Ensure adequate coverage of input space

3. **Run Aspen simulations**
   - Automate simulation runs (Python + Aspen COM interface)
   - Extract product properties
   - Record corresponding bio-oil inputs
   - Store data in structured format (CSV/Excel)

4. **Data quality control**
   - Check for simulation convergence issues
   - Identify and handle outliers
   - Verify thermodynamic consistency

### Phase 3: Machine Learning Development
1. **Data preprocessing**
   - Clean and format simulation data
   - Handle missing values
   - Feature engineering
   - Train-test split

2. **Model selection and training**
   - Test multiple algorithms (Random Forest, XGBoost, ANN, etc.)
   - Hyperparameter optimization
   - Cross-validation

3. **Model evaluation**
   - R², MAE, RMSE metrics
   - Feature importance analysis
   - Prediction accuracy assessment

4. **Model deployment**
   - Save trained models
   - Create prediction interface
   - Documentation

### Phase 4: Integration and Application
1. **Create prediction tool**
   - Input: Desired product specifications
   - Output: Required bio-oil composition

2. **Validate predictions**
   - Back-test with Aspen simulations
   - Compare predicted vs. actual bio-oil requirements

3. **Optimization module** (optional)
   - Multi-objective optimization
   - Economic analysis integration
   - Process constraint handling

---

## Directory Structure

```
reverse_ml_biooil_to_product/
├── PROJECT_SPECIFICATION.md          (this file)
├── README.md                         (project summary)
├── aspen_simulations/
│   ├── process_flowsheet/           (Aspen files)
│   ├── simulation_data/             (raw simulation outputs)
│   └── automation_scripts/          (Python scripts for Aspen automation)
├── data/
│   ├── raw/                         (raw simulation data)
│   ├── processed/                   (cleaned and formatted data)
│   └── biooil_reference_data/       (from original project)
├── ml_models/
│   ├── data_preparation.py
│   ├── train_models.py
│   ├── model_evaluation.py
│   └── trained_models/              (saved model files)
├── notebooks/
│   ├── exploratory_analysis.ipynb
│   ├── model_comparison.ipynb
│   └── results_visualization.ipynb
├── tools/
│   └── prediction_tool.py           (interface for predictions)
├── docs/
│   ├── process_description.md
│   ├── simulation_methodology.md
│   └── model_documentation.md
└── results/
    ├── figures/
    ├── tables/
    └── reports/
```

---

## Expected Outputs

1. **Aspen Process Model**: Validated simulation of selected chemical process
2. **Simulation Dataset**: Comprehensive data linking bio-oil properties to product characteristics
3. **ML Models**: Trained models for predicting bio-oil composition from product specs
4. **Prediction Tool**: User-friendly interface for reverse bio-oil design
5. **Technical Reports**: Documentation of methodology and results
6. **Publications**: Scientific papers describing the approach

---

## Key Advantages of This Approach

1. **Product-Driven Design**: Start with desired product specifications
2. **Optimization Opportunity**: Find optimal bio-oil composition for target products
3. **Process Integration**: Better integration between pyrolysis and downstream processing
4. **Economic Benefits**: Produce bio-oil tailored for specific applications
5. **Resource Efficiency**: Reduce trial-and-error in process development

---

## Next Steps

1. ✅ Create project folder structure
2. ⬜ Select specific chemical process for Aspen simulation
3. ⬜ Build and validate Aspen process model
4. ⬜ Design simulation experiment matrix
5. ⬜ Develop Aspen automation scripts
6. ⬜ Generate training dataset
7. ⬜ Develop ML pipeline
8. ⬜ Train and validate models
9. ⬜ Create prediction tool
10. ⬜ Document results

---

## Dependencies

### Software Requirements
- Aspen Plus / Aspen HYSYS (for process simulation)
- Python 3.8+
- Required Python packages:
  - pandas, numpy (data handling)
  - scikit-learn (machine learning)
  - xgboost, lightgbm, catboost (advanced ML)
  - tensorflow/keras (neural networks)
  - matplotlib, seaborn (visualization)
  - pywin32 (Aspen COM automation)

### Data Requirements
- Historical bio-oil composition data (from original project database)
- Literature data for process validation
- Thermodynamic property data

---

## Contact and Collaboration

**Project Lead**: Orhun Uzdiyem
**Institution**: [Your Institution]
**Related Project**: Biomass Pyrolysis Bio-oil Prediction ML Project

---

*Document Version: 1.0*
*Date Created: 2025-11-16*
*Last Updated: 2025-11-16*
