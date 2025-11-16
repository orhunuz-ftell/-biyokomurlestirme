# Bio-oil Steam Reforming for Hydrogen Production
## Process Description Document

**Date**: 2025-11-16
**Process**: Catalytic Steam Reforming
**Feed**: Pyrolysis Bio-oil
**Main Product**: Hydrogen (H₂)

---

## 1. PROCESS OVERVIEW

Steam reforming is a thermochemical process that converts bio-oil into hydrogen-rich synthesis gas (syngas) through reactions with high-temperature steam in the presence of a catalyst. The process breaks down complex organic molecules in bio-oil into simpler gases, primarily hydrogen and carbon monoxide, which is then further converted to additional hydrogen through the water-gas shift reaction.

**Overall Reaction**:
```
Bio-oil (CₙHₘOₖ) + H₂O → H₂ + CO₂ + CO + CH₄ (+ minor species)
```

---

## 2. RAW MATERIALS (INPUTS)

### 2.1 Primary Feed: Bio-oil

**Source**: Fast or slow pyrolysis of lignocellulosic biomass

**Physical Properties**:
- Dark brown viscous liquid
- Density: 1.1-1.3 g/cm³
- Water content: 15-30 wt%
- pH: 2.5-3.5 (acidic)
- Higher Heating Value (HHV): 16-19 MJ/kg

**Chemical Composition** (typical range):
| Component Group | Content (wt%) |
|----------------|---------------|
| Aromatics | 10-40% |
| Acids (acetic, formic) | 5-30% |
| Alcohols | 2-15% |
| Phenols | 5-35% |
| Furans | 3-12% |
| Aldehydes & Ketones | 5-15% |
| Esters | 1-8% |
| Water | 15-30% |
| Others (sugars, N-compounds) | Variable |

**Key Characteristics**:
- Complex mixture of 200-400 different compounds
- High oxygen content (35-50% by mass)
- Corrosive (high acidity)
- Unstable (aging/polymerization over time)

### 2.2 Process Steam

**Purpose**:
- Reactant in reforming reactions
- Heat carrier
- Prevents carbon (coke) formation on catalyst

**Specification**:
- Superheated steam
- Temperature: 400-600°C
- Pressure: 5-30 bar
- Steam-to-carbon (S/C) ratio: 2-6 (mol steam per mol carbon in feed)

### 2.3 Catalyst

**Type**: Nickel-based supported catalyst

**Typical Formulation**:
- Ni/Al₂O₃ (15-25 wt% Ni on alumina support)
- Alternative: Ni/CeO₂, Ni-Mg/Al₂O₃

**Function**:
- Lowers activation energy of reforming reactions
- Promotes C-C bond breaking
- Catalyzes water-gas shift reaction

**Operating Life**:
- 2-5 years (depending on bio-oil quality and operating conditions)
- Deactivation mechanisms: coking, sintering, poisoning (sulfur)

---

## 3. MAIN PROCESS EQUIPMENT

### 3.1 Feed Preparation & Mixing

**Equipment**: Static Mixer

**Function**: Thoroughly mix bio-oil with superheated steam

**Operating Conditions**:
- Temperature: 200-400°C
- Pressure: 5-30 bar
- S/C ratio control: Critical for preventing coking

**Design Considerations**:
- Corrosion-resistant materials (stainless steel 316L or higher)
- Efficient atomization/vaporization of bio-oil

---

### 3.2 Pre-heater

**Equipment**: Heat Exchanger (Shell & Tube or Fired Heater)

**Function**: Raise temperature of bio-oil/steam mixture to reforming temperature

**Operating Conditions**:
- Inlet: 200-400°C
- Outlet: 600-700°C
- Heating duty: Typically 15-25% of total energy input

**Design Considerations**:
- Prevent cold spots (coking risk)
- Minimize pressure drop
- Heat recovery from hot product gases (energy integration)

---

### 3.3 Main Reformer (Primary Reactor)

**Equipment**: Fixed-bed Catalytic Reactor

**Function**: Convert bio-oil organics into syngas (H₂ + CO) via steam reforming

**Type**:
- Vertical tubular reactor
- Packed with Ni/Al₂O₃ catalyst pellets
- External heating (endothermic reactions)

**Operating Conditions**:
- Temperature: 650-850°C (optimal: ~800°C)
- Pressure: 5-30 bar
- Space velocity (GHSV): 1000-5000 h⁻¹
- Catalyst bed height: 2-5 meters

**Main Reactions** (Endothermic):

1. **Steam Reforming of Hydrocarbons**:
   ```
   CₙHₘOₖ + (n-k)H₂O → nCO + (n-k+m/2)H₂
   ΔH° ≈ +200 to +250 kJ/mol
   ```

2. **Methane Reforming** (if CH₄ forms):
   ```
   CH₄ + H₂O ⇌ CO + 3H₂
   ΔH° = +206 kJ/mol
   ```

3. **Partial Water-Gas Shift** (occurs simultaneously):
   ```
   CO + H₂O ⇌ CO₂ + H₂
   ΔH° = -41 kJ/mol
   ```

**Key Performance Indicators**:
- Carbon conversion: 85-95%
- H₂ yield: 60-80 mol H₂ per mol bio-oil carbon
- Coke formation: <2% (controlled by S/C ratio)

---

### 3.4 High-Temperature Shift (HTS) Reactor

**Equipment**: Fixed-bed Catalytic Reactor (Adiabatic)

**Function**: Convert CO to additional H₂ via water-gas shift reaction

**Catalyst**:
- Iron-chromium oxide (Fe₃O₄-Cr₂O₃)
- More sulfur-tolerant than nickel

**Operating Conditions**:
- Inlet temperature: 320-370°C
- Outlet temperature: 400-450°C (exothermic reaction raises temperature)
- Pressure: Same as reformer
- CO conversion: 60-70%

**Reaction** (Exothermic):
```
CO + H₂O ⇌ CO₂ + H₂
ΔH° = -41 kJ/mol
```

**Purpose**:
- Increase H₂ yield
- Reduce CO content from ~10-12% to ~3-4%

---

### 3.5 Interstage Cooler

**Equipment**: Heat Exchanger

**Function**: Cool gas between HTS and LTS reactors

**Operating Conditions**:
- Inlet: 400-450°C
- Outlet: 190-210°C

**Why Needed**:
- Thermodynamic equilibrium of WGS favors products at lower temperature
- LTS catalyst operates at lower temperature

---

### 3.6 Low-Temperature Shift (LTS) Reactor

**Equipment**: Fixed-bed Catalytic Reactor (Adiabatic)

**Function**: Further convert remaining CO to H₂

**Catalyst**:
- Copper-zinc oxide on alumina (CuO-ZnO/Al₂O₃)
- More active at low temperature than Fe-based catalyst

**Operating Conditions**:
- Inlet temperature: 190-210°C
- Outlet temperature: 220-250°C
- CO conversion: >95% of remaining CO
- Final CO content: <0.5-1%

**Reaction** (Same as HTS):
```
CO + H₂O ⇌ CO₂ + H₂
```

**Result**:
- Maximum H₂ production
- Minimal CO slip

---

### 3.7 Cooling & Condensation

**Equipment**: Heat Exchanger + Flash Separator

**Function**:
- Cool syngas to ambient temperature
- Condense and remove water

**Operating Conditions**:
- Cooling to: 30-40°C
- Pressure: Maintained at process pressure

**Separated Streams**:
- **Gas**: H₂, CO₂, CO, CH₄, N₂ (if air used)
- **Liquid**: Condensed water (needs treatment, contains dissolved CO₂, trace organics)

---

### 3.8 CO₂ Removal Unit

**Equipment**: Absorption Column (Amine Scrubbing)

**Function**: Remove CO₂ from syngas to increase H₂ purity

**Typical System**:
- **Absorber**: CO₂ dissolves in amine solution (MEA, DEA, MDEA)
- **Stripper**: Regenerates amine by heating, releases pure CO₂

**Operating Conditions**:
- Absorber: 30-40°C, process pressure
- Stripper: 100-120°C, 1-2 bar
- CO₂ removal: >95%

**Product Streams**:
- **Gas**: H₂ + small amounts of CO, CH₄, N₂
- **CO₂**: Captured (can be vented or sequestered)

---

### 3.9 Pressure Swing Adsorption (PSA)

**Equipment**: Multi-bed Adsorption System (typically 4-12 beds)

**Function**: Purify hydrogen to >99.9% purity

**Adsorbent Materials** (layered beds):
- Activated carbon (removes hydrocarbons)
- Zeolites (removes CO, CO₂, N₂)
- Molecular sieves (removes remaining impurities)

**Operating Principle**:
- **Adsorption** (high pressure): Impurities adsorbed, H₂ passes through
- **Desorption** (low pressure): Regenerate bed, impurities released as "tail gas"
- Multiple beds operate in cycle (continuous H₂ production)

**Operating Conditions**:
- Adsorption pressure: 15-30 bar
- Desorption pressure: 1-2 bar
- Cycle time: 5-15 minutes per bed
- H₂ recovery: 85-92%

**Output Purity**:
- H₂: >99.9% (suitable for fuel cells, chemical synthesis)
- Impurities: <1000 ppm total

**Tail Gas** (15-10% of feed):
- Contains: H₂, CH₄, CO, CO₂
- Typical use: Fuel for pre-heater/reformer (energy recovery)

---

## 4. PRODUCTS

### 4.1 Primary Product: Hydrogen (H₂)

**Purity**: >99.9% (from PSA)

**Yield**:
- 0.08-0.12 kg H₂ per kg bio-oil (depending on bio-oil composition)
- 60-80 mol H₂ per mol carbon in bio-oil

**Physical Properties**:
- Colorless gas
- Molecular weight: 2.016 g/mol
- Energy density: 120 MJ/kg (HHV)
- Pressure: 15-25 bar (from PSA)

**Applications**:
- **Energy**: Fuel cells, gas turbines, direct combustion
- **Chemical Industry**: Ammonia synthesis, methanol production, hydrogenation processes
- **Petroleum Refining**: Hydrocracking, hydrotreating
- **Metallurgy**: Direct reduction of iron ore
- **Green H₂**: When bio-oil is from sustainable biomass (carbon-neutral)

**Storage/Transport**:
- Compressed gas (200-700 bar cylinders)
- Liquid hydrogen (-253°C cryogenic)
- Pipeline distribution

---

### 4.2 By-Product: Carbon Dioxide (CO₂)

**Source**: CO₂ removal unit

**Purity**: >95% (from amine stripper)

**Quantity**:
- 1.5-2.5 kg CO₂ per kg bio-oil
- Depends on bio-oil oxygen content and process efficiency

**Fate**:
- **Vent** to atmosphere (if biomass is sustainably sourced, this is carbon-neutral)
- **Carbon Capture & Storage (CCS)**: Compress and inject underground (negative emissions)
- **Utilization**: Feed for greenhouses, carbonation, chemical synthesis

---

### 4.3 Waste Stream: Tail Gas from PSA

**Composition**:
- H₂: 40-60%
- CH₄: 5-15%
- CO: 2-5%
- CO₂: 20-30%
- N₂: 0-10%

**Heating Value**: 10-15 MJ/Nm³

**Utilization**:
- **Primary use**: Fuel for pre-heater/reformer burners
- Recovers 15-25% of process energy
- Reduces natural gas/external fuel requirements

---

### 4.4 Waste Stream: Wastewater

**Source**: Condensate from syngas cooling

**Characteristics**:
- Contains: Dissolved CO₂, traces of acetic acid, other organics
- pH: 4-6 (acidic)
- COD: 500-2000 mg/L

**Treatment Required**:
- Neutralization
- Biological treatment (if organics present)
- Can be partially recycled as process steam makeup

---

## 5. MASS & ENERGY BALANCE (Typical)

### Input (per 100 kg bio-oil):

| Input | Quantity |
|-------|----------|
| Bio-oil | 100 kg |
| Steam (process) | 150-250 kg |
| Catalyst (makeup) | 0.5 kg/year |
| **Total** | **250-350 kg** |

### Output:

| Product | Quantity | Energy Content |
|---------|----------|----------------|
| **Hydrogen (H₂)** | **8-12 kg** | **960-1440 MJ** |
| CO₂ (captured) | 150-200 kg | - |
| Wastewater | 50-100 kg | - |
| Heat (recoverable) | - | 200-400 MJ |
| **Total** | **~208-312 kg** | - |

### Energy Balance:

| Energy Flow | Amount (MJ) |
|-------------|-------------|
| **Input**: Bio-oil (HHV) | 1700-1900 |
| **Input**: External heating | 400-600 |
| **Output**: H₂ product (HHV) | 960-1440 |
| **Output**: Tail gas (burned for process heat) | 200-300 |
| **Losses**: Stack, cooling | 300-500 |

**Overall Energy Efficiency**: 55-65% (LHV basis)
**Carbon Efficiency**: 60-75% (carbon to H₂)

---

## 6. KEY PROCESS PARAMETERS

| Parameter | Range | Optimal |
|-----------|-------|---------|
| Reformer Temperature | 650-850°C | 800-820°C |
| Pressure | 5-30 bar | 15-20 bar |
| Steam/Carbon Ratio (S/C) | 2-6 | 3-4 |
| Space Velocity (GHSV) | 1000-5000 h⁻¹ | 2000-3000 h⁻¹ |
| HTS Inlet Temperature | 320-370°C | 350°C |
| LTS Inlet Temperature | 190-210°C | 200°C |
| PSA Feed Pressure | 15-30 bar | 20-25 bar |

---

## 7. PROCESS ADVANTAGES

✅ **High Hydrogen Yield**: 8-12 wt% of bio-oil converted to H₂
✅ **Proven Technology**: Based on mature natural gas reforming
✅ **Flexible Operation**: Can handle variable bio-oil composition
✅ **Carbon Negative Potential**: With bio-oil from sustainable biomass + CCS
✅ **Co-product Utilization**: Tail gas provides process energy
✅ **Scalable**: From small (100 kg/h) to large (10,000 kg/h) plants

---

## 8. PROCESS CHALLENGES

⚠️ **High Temperature**: Requires significant energy input (endothermic reforming)
⚠️ **Catalyst Deactivation**: Coking, sintering, sulfur poisoning
⚠️ **Corrosion**: Bio-oil acidity requires corrosion-resistant materials
⚠️ **Complex Feed**: Variable bio-oil composition affects process stability
⚠️ **Capital Cost**: Multiple reactors and purification units required

---

## 9. ENVIRONMENTAL ASPECTS

### Carbon Footprint:
- **Bio-oil from sustainable biomass**: Carbon-neutral to carbon-negative
- **CO₂ emissions**: Can be captured (95%+ removal efficiency)
- **Net CO₂**: -0.5 to +0.2 kg CO₂-eq per kg H₂ (depending on CCS)

### Water Consumption:
- High (2-3 kg H₂O per kg H₂ produced)
- Wastewater requires treatment

### Comparison to Other H₂ Production:
| Method | CO₂ Emissions (kg/kg H₂) |
|--------|--------------------------|
| Steam Methane Reforming (natural gas) | +9 to +11 |
| Coal Gasification | +15 to +18 |
| **Bio-oil Reforming** | **-0.5 to +2** |
| Water Electrolysis (renewable) | ~0 |

---

## 10. ECONOMIC CONSIDERATIONS

### Capital Cost (Rough Estimates):
- Small scale (100 kg H₂/day): $2-3 million
- Medium scale (1000 kg H₂/day): $15-25 million
- Includes: Reactors, heat exchangers, PSA, controls

### Operating Cost:
- Bio-oil feedstock: $0.2-0.4 per kg
- Steam (natural gas for heating): $0.05-0.10 per kg H₂
- Catalyst replacement: $0.02-0.05 per kg H₂
- Maintenance: 2-4% of CAPEX per year
- **Total**: $1.5-3.0 per kg H₂

### Hydrogen Selling Price:
- Industrial grade: $2-4 per kg
- Fuel cell grade: $4-8 per kg
- Green H₂ with incentives: $3-6 per kg

---

## REFERENCES

1. Bridgwater, A. V., & Peacocke, G. (2000). Fast Pyrolysis Processes for Biomass. *Renewable and Sustainable Energy Reviews*, 4, 1-73.

2. Ni, M., & Leung, D. Y. C. (2006). An Overview of Hydrogen Production from Biomass. *Fuel Processing Technology*, 87, 461-472.

3. Singh, P. P., & Jaswal, A. (2024). Green hydrogen production from biomass – A thermodynamic assessment. *International Journal of Hydrogen Energy*, 50, 627-639.

4. Bekiroğulları, M., & Kaya, M. (2020). Investigation of Hydrogen Production from Bio-Oil Using Aspen Plus. *Gazi University Journal of Science*, 33(1), 14-20.

5. Pafili, A., & Charisiou, N. D. (2021). Recent Progress in the Steam Reforming of Bio-Oil for Hydrogen Production. *Catalysts*, 11(12), 1526-1549.

---

**Document Version**: 1.0
**Last Updated**: 2025-11-16
**Author**: Orhun Uzdiyem PhD Project
