# Reverse ML: Product-to-Bio-oil Property Prediction

## Quick Overview

This project uses **machine learning to predict required bio-oil properties** based on desired product characteristics from a downstream chemical process.

### The Concept

Instead of predicting what products we can make from bio-oil, we predict **what bio-oil composition we need** to achieve specific product specifications.

```
Traditional:  Biomass → Bio-oil → ??? Product
Reverse:      ??? Bio-oil → Desired Product
```

## How It Works

1. **Aspen Simulation**: Model a chemical process that converts bio-oil to products
2. **Data Generation**: Run simulations with various bio-oil inputs → record product outputs
3. **Machine Learning**: Train models to learn the inverse relationship
4. **Application**: Input desired product specs → Get required bio-oil composition

## Current Status

🟡 **Project Phase**: Setup and Planning

- ✅ Project structure created
- ✅ Specification document written
- ⬜ Process selection pending
- ⬜ Aspen model development pending
- ⬜ Data generation pending
- ⬜ ML model training pending

## Quick Start

See [PROJECT_SPECIFICATION.md](./PROJECT_SPECIFICATION.md) for detailed methodology and implementation plan.

## Key Files

- `PROJECT_SPECIFICATION.md` - Complete project specification and methodology
- `README.md` - This file
- `aspen_simulations/` - Aspen process models and simulation data
- `ml_models/` - Machine learning pipeline and trained models
- `data/` - Training datasets

## Requirements

- Aspen Plus/HYSYS
- Python 3.8+
- See PROJECT_SPECIFICATION.md for complete dependency list

## Contributing

This is a research project. For questions or collaboration, contact the project team.

---

**Related Project**: [Biomass Pyrolysis Bio-oil Prediction ML Project](../)
