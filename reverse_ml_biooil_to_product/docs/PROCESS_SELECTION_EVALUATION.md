# Bio-oil Utilization Process Selection & Evaluation

**Based on TIK 3 Report Literature Review**
**Date**: 2025-11-16

---

## Available Process Options

Based on section B.2.4 of your TIK 3 report, the following processes utilize bio-oil as feedstock:

### 1. Direct Combustion for Energy/Heating
### 2. Hydrodeoxygenation (HDO) for Transportation Fuels
### 3. Steam Reforming for Hydrogen Production
### 4. Phenolic Resin Synthesis
### 5. Bio-Asphalt/Bitumen Production
### 6. Other Emerging Applications (Fuel Cells, Bio-polyols)

---

## Evaluation Criteria

Each process is graded on a scale of 1-10 (10 = best) across multiple criteria:

1. **Aspen Modeling Complexity** (Lower is better for data generation)
2. **Data Availability** (Thermodynamic, kinetic data)
3. **Simulation Speed** (Important for generating 200-500+ runs)
4. **Number of Process Variables** (More variables = richer dataset)
5. **Industrial Relevance** (Market potential, existing applications)
6. **Literature Support** (Validation data availability)
7. **ML Dataset Suitability** (Clear input-output relationships)
8. **Technical Feasibility** (Can be done in Aspen 2006)

---

## Detailed Process Evaluation

### ⭐ Option 1: Direct Combustion for Energy/Heating

**Description**: Bio-oil is directly burned in boilers for heat/electricity generation

**Technical Details**:
- **Operating Conditions**: Atmospheric pressure, 800-1200°C
- **Process Complexity**: Single RGibbs or RStoic reactor + heat exchanger
- **Industrial Status**: Commercial scale (30 MW plants in Europe, US Forest Service)

**Evaluation Scores**:

| Criterion | Score | Justification |
|-----------|-------|---------------|
| Aspen Modeling Complexity | 9/10 | Simplest - single reactor, no recycle loops |
| Data Availability | 10/10 | Complete combustion thermodynamics well-known |
| Simulation Speed | 10/10 | Seconds per run |
| Number of Variables | 4/10 | Limited: temperature, air ratio, bio-oil composition |
| Industrial Relevance | 7/10 | Proven at industrial scale but commodity product |
| Literature Support | 8/10 | Well documented (Bosch Industrial 2023, US Forest Service 2021) |
| ML Dataset Suitability | 6/10 | Simple relationships, limited complexity |
| Technical Feasibility | 10/10 | Fully achievable in Aspen 2006 |
| **TOTAL** | **64/80** | **80%** |

**Advantages**:
- ✅ Easiest to model (minutes to set up)
- ✅ Fast simulations
- ✅ Proven industrial application

**Disadvantages**:
- ❌ Too simple - limited ML learning opportunity
- ❌ Few manipulable variables
- ❌ Low-value product (heat/electricity)
- ❌ Doesn't fully utilize your database of bio-oil composition

---

### ⭐⭐⭐ Option 2: Hydrodeoxygenation (HDO) for Transportation Fuels

**Description**: Catalytic upgrading of bio-oil to drop-in transportation fuels (gasoline, diesel, jet fuel)

**Technical Details**:
- **Operating Conditions**: 300-400°C, 10-20 MPa H₂, NiMo/Al₂O₃ catalyst
- **Process Stages**: Multi-stage reactors, H₂ recycle, product separation
- **Industrial Status**: Pilot/demonstration scale
- **Target Products**: Low-oxygen hydrocarbon fuels (O/C < 2%)

**Evaluation Scores**:

| Criterion | Score | Justification |
|-----------|-------|---------------|
| Aspen Modeling Complexity | 4/10 | Very complex - multiple reactors, H₂ recycle, flash separators |
| Data Availability | 5/10 | Requires literature kinetics (Lee et al. 2016) |
| Simulation Speed | 5/10 | Moderate - recycle loops slow convergence |
| Number of Variables | 8/10 | Many: T, P, H₂/oil ratio, catalyst, residence time |
| Industrial Relevance | 9/10 | High-value products, strong market interest |
| Literature Support | 7/10 | Good (Yang & Xu 2023, Zhang et al. 2021) |
| ML Dataset Suitability | 7/10 | Complex relationships between bio-oil composition and fuel quality |
| Technical Feasibility | 6/10 | Challenging in Aspen 2006 - requires kinetic models |
| **TOTAL** | **51/80** | **64%** |

**Advantages**:
- ✅ High-value products
- ✅ Many process variables
- ✅ Strong industrial interest
- ✅ Direct link between bio-oil composition and fuel properties

**Disadvantages**:
- ❌ Very complex modeling (weeks of setup)
- ❌ Requires detailed kinetic data
- ❌ Slow simulations (recycle convergence issues)
- ❌ High H₂ consumption adds complexity

---

### ⭐⭐⭐⭐⭐ Option 3: Steam Reforming for Hydrogen Production

**Description**: Catalytic steam reforming of bio-oil to produce hydrogen-rich syngas

**Technical Details**:
- **Operating Conditions**: 650-850°C, 5-30 bar, S/C ratio 2-6
- **Catalyst**: Ni/Al₂O₃
- **Process Stages**:
  1. Pre-heating + steam mixing
  2. Main reformer (endothermic)
  3. High-temperature water-gas shift (350°C)
  4. Low-temperature water-gas shift (200°C)
  5. Condensation
  6. CO₂ removal (amine scrubbing)
  7. PSA for H₂ purification

**Evaluation Scores**:

| Criterion | Score | Justification |
|-----------|-------|---------------|
| Aspen Modeling Complexity | 8/10 | Moderate - clear unit ops, no complex recycles |
| Data Availability | 10/10 | Excellent - gas phase equilibrium well-established |
| Simulation Speed | 10/10 | Very fast - <5 seconds per run (Bekiroğulları & Kaya 2020) |
| Number of Variables | 9/10 | Excellent: T (650-850°C), P (5-30 bar), S/C (2-6), bio-oil composition (14+ components) |
| Industrial Relevance | 9/10 | Hydrogen is strategic (green H₂ production) |
| Literature Support | 10/10 | Extensive (Singh et al. 2024, Bekiroğulları & Kaya 2020, Pafili & Charisiou 2021) |
| ML Dataset Suitability | 9/10 | Clear relationships: bio-oil composition → H₂ yield, H₂/CO ratio, conversion |
| Technical Feasibility | 9/10 | Fully achievable in Aspen 2006 (RYIELD, RGIBBS, WGS reactors) |
| **TOTAL** | **74/80** | **93%** |

**Advantages**:
- ✅ **FAST simulations** - can generate 500+ datasets quickly
- ✅ **Many manipulable variables** (T, P, S/C, composition)
- ✅ **Excellent thermodynamic data** available
- ✅ **Validated by multiple literature sources**
- ✅ **Clear product outputs**: H₂ yield, H₂/CO ratio, CH₄ slip, CO₂ production
- ✅ **Industrial relevance**: green hydrogen production
- ✅ **Suitable for Aspen 2006** (all required blocks available)
- ✅ **Endothermic reaction** allows stable, fast convergence

**Disadvantages**:
- ⚠️ PSA unit not available as icon in Aspen 2006 (but can use component splitter with 90% H₂ recovery)
- ⚠️ Requires defining 5-component surrogate model for bio-oil

**Your TIK 3 Report Conclusion**: ✅ **SELECTED PROCESS**

---

### ⭐⭐ Option 4: Phenolic Resin Synthesis

**Description**: Using bio-oil phenolic fraction to partially replace phenol in novolak/resole resins

**Technical Details**:
- **Operating Conditions**: 60-100°C, atmospheric pressure
- **Replacement Level**: 15-25% phenol substitution with bio-oil phenolics
- **Applications**: Adhesives, composite materials
- **Industrial Status**: Laboratory/pilot scale

**Evaluation Scores**:

| Criterion | Score | Justification |
|-----------|-------|---------------|
| Aspen Modeling Complexity | 3/10 | Very complex - requires pseudo-components, UNIQUAC parameters |
| Data Availability | 4/10 | Limited - special interaction parameters needed |
| Simulation Speed | 4/10 | Slow - complex phase equilibrium |
| Number of Variables | 6/10 | Moderate: phenol/bio-oil ratio, temperature, catalyst type |
| Industrial Relevance | 6/10 | Niche market, limited scale |
| Literature Support | 6/10 | Some data (Choi et al. 2015, Xu & Brodu 2022) |
| ML Dataset Suitability | 5/10 | Complex polymer chemistry, hard to correlate |
| Technical Feasibility | 4/10 | Requires custom components not in Aspen database |
| **TOTAL** | **38/80** | **48%** |

**Disadvantages**:
- ❌ Requires custom pseudo-components
- ❌ Special UNIQUAC parameters needed
- ❌ Slow simulation convergence
- ❌ Limited industrial application
- ❌ Polymer property prediction is complex

---

### ⭐ Option 5: Bio-Asphalt/Bitumen Production

**Description**: Using bio-oil as binder/modifier in asphalt production

**Technical Details**:
- **Replacement Level**: 10-20% petroleum bitumen replacement
- **Operating Conditions**: 150-180°C, atmospheric
- **Industrial Status**: Research/pilot scale

**Evaluation Scores**:

| Criterion | Score | Justification |
|-----------|-------|---------------|
| Aspen Modeling Complexity | 2/10 | Extremely complex - high MW compounds, viscous phase |
| Data Availability | 2/10 | Very limited - requires PC-SAFT EOS, not in Aspen DB |
| Simulation Speed | 2/10 | Very slow - complex rheology |
| Number of Variables | 5/10 | Moderate: bio-oil%, temperature, aging conditions |
| Industrial Relevance | 7/10 | Large market (road construction) but niche application |
| Literature Support | 5/10 | Limited (Zhang et al. 2022, Varun Kumar & Mayakrishnan 2024) |
| ML Dataset Suitability | 3/10 | Difficult to correlate viscous properties |
| Technical Feasibility | 2/10 | **NOT feasible in Aspen 2006** - requires special EOS |
| **TOTAL** | **28/80** | **35%** |

**Disadvantages**:
- ❌ **Cannot be modeled in Aspen 2006** - requires PC-SAFT
- ❌ Physical property data not available in Aspen database
- ❌ High molecular weight compounds
- ❌ Complex rheological properties

---

## Summary Ranking Table

| Rank | Process | Total Score | % | Recommendation |
|------|---------|-------------|---|----------------|
| 🥇 **1** | **Steam Reforming (H₂ Production)** | **74/80** | **93%** | ✅ **HIGHLY RECOMMENDED** |
| 🥈 2 | Direct Combustion | 64/80 | 80% | ⚠️ Too simple for ML |
| 🥉 3 | Hydrodeoxygenation (HDO) | 51/80 | 64% | ⚠️ Too complex for rapid data generation |
| 4 | Phenolic Resin | 38/80 | 48% | ❌ Not recommended |
| 5 | Bio-Asphalt | 28/80 | 35% | ❌ Not feasible in Aspen 2006 |

---

## Final Recommendation: Steam Reforming for Hydrogen Production

### Why This Process is Optimal for Your Reverse ML Project:

#### 1. **Perfect Balance of Complexity**
- Not too simple (like combustion)
- Not too complex (like HDO)
- Rich enough for meaningful ML learning

#### 2. **Excellent Data Generation Capability**
✅ **Fast simulations** (<5s per run)
✅ **Can generate 500-1000 scenarios** in hours
✅ **4 major variables**: Temperature (650-850°C), Pressure (5-30 bar), S/C ratio (2-6), bio-oil composition (14 components)

#### 3. **Clear ML Input-Output Mapping**

**ML INPUTS (Product Properties from Aspen)**:
- H₂ flow rate (kg/h)
- H₂ purity (%)
- H₂/CO molar ratio
- CO₂ production (kg/h)
- CH₄ slip (%)
- Syngas composition (H₂, CO, CO₂, CH₄, H₂O)
- Energy consumption (MJ/kg H₂)
- Carbon conversion efficiency (%)

**ML OUTPUTS (Bio-oil Composition Required)**:
- aromatics (%)
- acids (%)
- alcohols (%)
- furans (%)
- phenols (%)
- aldehyde_ketone (%)
- esters (%)
- aliphatichydrocarbon (%)
- Water content (%)

#### 4. **Validated Approach**
- ✅ Confirmed in your TIK 3 report (pages 10-12)
- ✅ Multiple literature validations
- ✅ Aspen flowsheet already designed (Figure 1)

#### 5. **Industrial Relevance**
- Green hydrogen is strategic for energy transition
- Direct application to your thesis goal: optimizing bio-oil for specific products

---

## Implementation Roadmap

### Phase 1: Aspen Model Setup (Week 1-2)
1. Build reforming flowsheet in Aspen 2006
2. Define bio-oil surrogate components
3. Configure RYIELD → RGIBBS → WGS → SEP sequence
4. Validate against Bekiroğulları & Kaya (2020) data

### Phase 2: DOE & Data Generation (Week 3-4)
1. Create DOE matrix (500+ scenarios)
2. Vary: T, P, S/C, bio-oil composition (from your existing DB)
3. Run automated simulations
4. Extract outputs: H₂ yield, composition, energy metrics

### Phase 3: ML Training (Week 5-6)
1. Prepare dataset: Product properties (X) → Bio-oil composition (Y)
2. Train multiple algorithms
3. Validate reverse predictions

---

## Process Flowsheet (From Your TIK 3 Report)

```
Bio-oil + Steam → [Mixer] → [Heater] → [Main Reformer 850°C, Ni/Al₂O₃]
    → [Cooler] → [HTS Reactor 350°C] → [Cooler] → [LTS Reactor 200°C]
    → [Flash Separator] → [CO₂ Removal] → [PSA] → H₂ Product (99.9% purity)
```

**Key Reactions**:
- Main reforming: CₙHₘOₖ + nH₂O → nCO + (n+m/2)H₂  (Endothermic, ΔH° ≈ +200 kJ/mol)
- Water-gas shift: CO + H₂O ⇌ CO₂ + H₂  (Exothermic, ΔH° = -41 kJ/mol)

---

## Decision

✅ **SELECTED PROCESS: Steam Reforming for Hydrogen Production**

**Rationale**: Best combination of modeling feasibility, simulation speed, variable richness, industrial relevance, and suitability for generating ML training datasets.

**Next Steps**: Proceed to Aspen model development using the flowsheet in Figure 1 of TIK 3 report.

---

**Document Prepared By**: Claude Code AI Assistant
**Based On**: TIK 3 Report (OrhunUzdiyem_tik3.pdf, pages 8-12)
**Date**: 2025-11-16
