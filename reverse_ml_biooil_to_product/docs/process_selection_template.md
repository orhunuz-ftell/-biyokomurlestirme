# Process Selection Template

## Process Information

**Process Name**: [e.g., Bio-oil Hydrodeoxygenation, Catalytic Cracking, etc.]

**Date**: YYYY-MM-DD

**Selected By**: [Your Name]

---

## Process Description

### Overview
[Brief description of the chemical process]

### Main Reactions
```
[List key chemical reactions]
```

### Process Flow
```
Bio-oil → [Unit Op 1] → [Unit Op 2] → ... → Final Product(s)
```

---

## Input Requirements

### Bio-oil Specifications
- **Flow rate range**: [min - max] kg/h
- **Temperature**: [value] °C
- **Pressure**: [value] bar
- **Key components affecting process**:
  - [ ] Aromatics
  - [ ] Acids
  - [ ] Alcohols
  - [ ] Phenols
  - [ ] Water content
  - [ ] Others: _____________

### Other Feedstocks
[List any co-reactants, catalysts, solvents, etc.]

---

## Process Outputs

### Main Products
1. **Product 1**: [Name, typical composition/properties]
2. **Product 2**: [Name, typical composition/properties]

### By-products
- [List by-products if any]

### Key Product Properties to Track
- [ ] Chemical composition (species concentrations)
- [ ] Density
- [ ] Viscosity
- [ ] Boiling point/distillation curve
- [ ] Heating value
- [ ] Cetane/Octane number (for fuels)
- [ ] Oxygen content
- [ ] Aromatics content
- [ ] Sulfur content
- [ ] Other: _____________

---

## Unit Operations Required

### List of Unit Operations
1. **[Unit Op 1]**: [Type, purpose]
   - Model in Aspen: [Model name]
   - Key parameters: [list]

2. **[Unit Op 2]**: [Type, purpose]
   - Model in Aspen: [Model name]
   - Key parameters: [list]

[Continue for all unit operations]

---

## Thermodynamic Model Selection

**Recommended Property Method**: [e.g., NRTL, UNIFAC, Peng-Robinson, etc.]

**Justification**: [Why this method is appropriate]

**Components to Define**:
- [ ] Bio-oil pseudo-components
- [ ] Reaction products
- [ ] Gases (H2, CO2, etc.)
- [ ] Solvents
- [ ] Others: _____________

---

## Operating Conditions

### Process Variables to Vary
| Variable | Min | Max | Unit | Notes |
|----------|-----|-----|------|-------|
| Reactor Temperature | | | °C | |
| Pressure | | | bar | |
| H2/Bio-oil ratio | | | mol/mol | |
| LHSV | | | h⁻¹ | |
| Catalyst type | | | - | |

### Fixed Conditions
[List any conditions that will remain constant]

---

## Literature References

### Key Papers
1. [Author et al., Year] - [Brief description]
2. [Author et al., Year] - [Brief description]

### Experimental Data for Validation
- [Source of validation data]
- [Available data points]

---

## Implementation Considerations

### Advantages of This Process
- [List benefits]

### Challenges/Limitations
- [List potential difficulties]

### Data Availability
- [ ] Literature data available for validation
- [ ] Kinetic data available
- [ ] Thermodynamic data available
- [ ] Industrial data available

---

## Expected ML Input-Output Mapping

### ML Inputs (Product Properties)
1. [Property 1]
2. [Property 2]
3. [Property 3]
...

### ML Outputs (Bio-oil Properties)
1. aromatics
2. acids
3. alcohols
4. phenols
5. furans
6. aldehyde_ketone
7. [others as relevant]

---

## Simulation Plan

### Phase 1: Model Development
- [ ] Build basic flowsheet
- [ ] Define components
- [ ] Select property methods
- [ ] Configure unit operations
- [ ] Set initial conditions

### Phase 2: Validation
- [ ] Compare with literature data
- [ ] Verify mass balances
- [ ] Verify energy balances
- [ ] Check convergence stability

### Phase 3: DOE (Design of Experiments)
- [ ] Define bio-oil composition ranges
- [ ] Define process variable ranges
- [ ] Create simulation matrix
- [ ] Estimate number of required simulations

### Phase 4: Automation
- [ ] Develop Python automation scripts
- [ ] Test batch simulation runs
- [ ] Implement error handling
- [ ] Create data extraction routine

---

## Approval

**Approved by**: _________________

**Date**: _________________

**Comments**:
[Any additional notes or modifications]

---

## Notes
[Add any additional information, assumptions, or considerations]
