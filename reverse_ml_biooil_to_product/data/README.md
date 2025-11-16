# Data Directory

This directory contains all datasets for the reverse ML project.

## Subdirectories

### `raw/`
Raw simulation output data directly from Aspen
- CSV/Excel files from simulation runs
- Unprocessed, as extracted from Aspen
- Include metadata (simulation ID, date, convergence status)

### `processed/`
Cleaned and formatted data ready for ML training
- Missing value handling
- Feature engineering applied
- Normalized/standardized if needed
- Train-test splits
- Final datasets with clear naming convention

### `biooil_reference_data/`
Historical bio-oil composition data from original project
- Reference ranges for bio-oil components
- Typical values from literature
- Constraints for realistic bio-oil composition
- Used for defining simulation input ranges

## Data Format Guidelines

### File Naming Convention
```
raw/simulation_run_YYYYMMDD_HHMMSS.csv
processed/training_data_YYYYMMDD.csv
processed/test_data_YYYYMMDD.csv
```

### Required Columns

**Input Features (Product Properties)**
- Product composition columns
- Physical properties (density, viscosity, etc.)
- Process conditions (T, P, flow rates)
- Performance metrics (yield, conversion, etc.)

**Output Targets (Bio-oil Properties)**
- LiquidOutput
- aromatics
- acids
- alcohols
- furans
- phenols
- aldehyde_ketone
- (other relevant components)

## Data Quality Checks

- [ ] Check for missing values
- [ ] Verify data ranges are physically realistic
- [ ] Confirm mass balances close
- [ ] Identify and document outliers
- [ ] Ensure simulation convergence status recorded
