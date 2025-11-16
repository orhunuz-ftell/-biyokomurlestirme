# Aspen Simulations

This directory contains all Aspen-related files and simulation outputs.

## Directory Structure

### `process_flowsheet/`
Contains Aspen Plus/HYSYS files (.apw, .apwz, .hsc, etc.)
- Process flowsheet diagrams
- Unit operation configurations
- Property method selections
- Stream specifications

### `simulation_data/`
Raw output data from Aspen simulations
- Product composition data
- Product physical properties
- Process conditions
- Energy balances
- Material balances

### `automation_scripts/`
Python scripts for automating Aspen simulations
- COM interface scripts
- Batch simulation runners
- Data extraction utilities
- Error handling routines

## Workflow

1. Develop process model in Aspen manually
2. Validate model against literature/experimental data
3. Create automation scripts for batch runs
4. Generate simulation matrix (DOE)
5. Run automated simulations
6. Extract and store results

## Notes

- Always save backup copies of working Aspen files
- Document any assumptions made in process model
- Keep log of simulation runs and convergence issues
- Verify mass and energy balances for each simulation
