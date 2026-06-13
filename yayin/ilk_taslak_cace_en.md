# A Reverse Deep Learning Approach for Estimating Bio-Oil Composition from Syngas Characteristics in Steam Reforming Processes

## 1. Introduction

Bio-oil obtained from biomass pyrolysis is a renewable intermediate for fuels, hydrogen, chemicals, carbon materials, and upgrading processes (Sharifzadeh and Sadeqzadeh, 2019; Zhang et al., 2022). Its practical use is challenging because its composition varies substantially with biomass type, pretreatment, pyrolysis temperature, residence time, and collection strategy. The relative amounts of aromatics, acids, alcohols, furans, phenols, and carbonyl compounds affect reforming behavior, hydrogen production potential, methane formation, coke tendency, corrosion risk, and syngas quality (Pafili et al., 2021; Singh and Jaswal, 2024).

For a future bio-oil reforming process, the most useful control variable is not only the current reformer condition, but also the changing composition of the incoming bio-oil. Direct and detailed bio-oil characterization generally requires offline analytical steps such as gas chromatography-mass spectrometry (GC-MS), Fourier-transform infrared spectroscopy (FTIR), elemental analysis, or wet chemical procedures. In contrast, syngas composition can be monitored more rapidly from the reformer outlet. This difference motivates a soft-sensor approach: infer the incoming bio-oil composition from measurable reformer outlet syngas and known operating conditions.

The intended use of the model in this work is therefore process monitoring and future model predictive control (MPC). In an MPC structure, a soft sensor can estimate bio-oil composition from measured syngas, and the estimate can then be passed to a forward surrogate or process model to adjust reformer temperature, pressure, and steam-to-carbon ratio. Such a workflow can support feedstock quality tracking, abnormal-feed detection, and operating-condition optimization without requiring continuous detailed liquid analysis.

The main obstacle is that the inverse mapping is difficult. The forward relation from bio-oil composition and reformer conditions to equilibrium syngas is governed by thermodynamics. The reverse relation is less direct because several different bio-oil mixtures can generate similar outlet gas compositions under related process conditions. A machine-learning model for this problem should therefore be treated as a domain-aware soft sensor rather than a replacement for analytical characterization.

The objective of this study is to develop and evaluate such a soft sensor. The work follows four steps. First, literature-derived bio-oil compositions are curated into a structured SQL database and mapped into six functional groups. Second, these compositions are converted into surrogate chemical mixtures for Cantera steam reforming simulations. Third, a synthetic thermodynamic dataset is generated over a structured operating-condition grid. Fourth, inverse machine-learning models are trained to estimate bio-oil composition from syngas composition and process conditions. The primary novelty is the integrated Cantera-to-ML inverse workflow for bio-oil steam reforming soft sensing.

Bio-oil reforming has practical constraints and application boundaries in production, transport, and materials sectors. In transport and district heating contexts, direct use of raw bio-oil is limited by high oxygen content and corrosivity; for this reason it is often upgraded to fuels. In hydrogen production, upgrading via steam reforming is especially attractive because biogenic carbon can be converted into synthesis gas and then to hydrogen. In materials or chemical routes, bio-oil-derived phenolics can be used in resins and composites, but long-term stability and process compatibility remain critical.

This study is, to our knowledge, the first machine-learning based inverse model developed specifically for bio-oil steam reforming in the literature.

## 2. Process Description and Thermodynamic Simulation

The experimental bio-oil composition data were collected to define realistic feed compositions for the Cantera simulation workflow. The SQL Server database contains literature-derived biomass, pyrolysis, bio-oil, and reforming records. The `Biooil` table contains 70 class-level bio-oil composition records linked to experiment, biomass, and reference metadata. These records are linked to 14 references and 43 biomass names, with pyrolysis process temperatures ranging from 300 to 850 °C. Because the Cantera surrogate model requires complete values for six selected classes, records were filtered to include only aromatics, acids, alcohols, furans, phenols, and aldehydes/ketones. This yielded 30 unique model-ready bio-oil compositions.

Steam reforming simulations were performed with Cantera using a reformer-only thermodynamic equilibrium workflow (Goodwin et al., 2017). The reformer was selected as the modeling focus because the bio-oil composition has its most direct influence at this stage. Water-gas shift, CO₂ removal, and pressure swing adsorption are represented in later unit-level descriptions, but not in the inverse soft-sensor core because this study targets the reformer outlet as the directly measured point.

The hydrogen-production flow scheme follows five stages: feed preheating and mixing, Ni/Al₂O₃-catalyzed reforming, high-temperature water-gas shift, cooling and condensation, CO₂ removal, and PSA purification. A typical syngas route is represented by Aspen-style reformer blocks for the original simulation design context.

The simulation method is based on equilibrium calculation through Gibbs free energy minimization. At fixed temperature and pressure, Cantera determines equilibrium composition subject to elemental conservation and non-negative species constraints. The Gibbs free energy minimization is formulated as:

$$
\mu_i = \mu_i^\circ + RT\ln(a_i)
$$

where \( \mu_i^\circ \) is the standard chemical potential, \(R\) is the gas constant, \(T\) is temperature, and \(a_i\) is species activity.

Cantera solves this nonlinear constrained optimization problem iteratively using Newton-Raphson steps:

1. initialize composition estimate for all species.
2. compute Jacobian of Gibbs gradients.
3. solve linearized update equation \(J\Delta n = -\nabla G\).
4. perform step-size control (line search).
5. check convergence tolerance.
6. enforce elemental balance and non-negative mole constraints.

For each six-class bio-oil composition, simulations were executed on a structured grid:

- Reforming temperature: 650, 700, 750, 800, 850 °C
- Pressure: 5, 15, 30 bar
- Steam-to-carbon ratio: 2.0, 4.0, 6.0

This produces \(5\times3\times3 = 45\) conditions per composition and \(30\times45 = 1{,}350\) simulation conditions after the final 30-composition selection.

The six bio-oil classes were represented by six representative surrogate molecules:

- Aromatics: toluene (C₇H₈)
- Acids: acetic acid (CH₃COOH)
- Alcohols: ethanol (C₂H₅OH)
- Furans: furan (C₄H₄O)
- Phenols: phenol (C₆H₆O)
- Aldehydes/ketones: acetone (C₃H₆O)

These choices follow common bio-oil surrogate practices for thermodynamic reforming models (Vagia and Lemonidou, 2007).

### 2.1. Input-Output Specification

**Input specification (8):**

1. reformer temperature (°C)
2. pressure (bar)
3. steam-to-carbon ratio
4. H₂ mole percent
5. CO mole percent
6. CO₂ mole percent
7. CH₄ mole percent
8. H₂O mole percent

**Output specification (6):**

1. aromatics (wt.%)
2. acids (wt.%)
3. alcohols (wt.%)
4. furans (wt.%)
5. phenols (wt.%)
6. aldehydes/ketones (wt.%)

## 3. Machine Learning and Deep Learning Framework

From the simulation outputs, 1,350 usable records were organized into a 70/15/15 split:

- Training set: 944 samples
- Validation set: 203 samples
- Test set: 203 samples

The workflow was implemented with the following model families:

- classical machine-learning approaches:
  - linear regression
  - random forest
  - XGBoost
- deep-learning approaches:
  - standard MLP with 3 hidden layers (128-64-32)
  - constrained MLP with softmax-style normalized output layer
- ensemble approaches:
  - simple averaging
  - weighted averaging
  - stacking

For all deep-learning models, mini-batch training, batch normalization, dropout, early stopping, and adaptive learning-rate adjustment were applied. The standard MLP was compared directly with the constrained version to evaluate the tradeoff between composition-closure constraints and predictive accuracy.

## 4. Results and Discussion

### 4.1 Baseline and nonlinear learners

In the row-wise test setting, the inverse task showed clear nonlinearity. Linear regression was insufficient (average R² = 0.332, MAE = 9.92%). Random forest and XGBoost were stronger yet still clearly below neural-network performance (average R² = 0.571 and 0.603, respectively). The standard MLP produced the best row-wise result with average R² = 0.863 and MAE = 4.03% on the test set. The constrained MLP reached lower performance (test R² = 0.745) and higher error (MAE = 11.54%).

### 4.2 Feature interpretation

Random-forest feature importance indicated that syngas species dominated the inverse signal. The two largest contributors were methane (27.1%) and CO₂ (26.0%), followed by water vapor (20.5%), H₂ (11.9%), and CO (9.9%). Operating conditions (temperature, pressure, steam-to-carbon ratio) collectively had much smaller importance. This supports the thermodynamic interpretation that syngas composition already carries most of the transferable information about bio-oil elemental balance.

### 4.3 Comparison of standard and constrained MLP

The standard MLP and constrained MLP were contrasted through row-wise test performance:

- Standard MLP: average R² = 0.863, MAE = 4.03%, average RMSE = 5.87%.
- Constrained MLP: test R² = 0.745, MAE = 11.54%.

The constrained architecture enforces \(\sum y_i = 100\%\), but its accuracy loss in several classes reduced its practical soft-sensor value for this dataset.

### 4.4 Ensemble behavior

Three ensemble strategies were tested:

- simple average (R² = 0.746, MAE = 5.16%)
- weighted average (R² = 0.797, MAE = 4.75%)
- stacking (R² = 0.562, MAE = 6.34%)

Even though ensemble methods are often expected to improve robustness, all three underperformed the standard MLP in the present inverse mapping.

**The methodological insight from this study is that ensemble methods can cause performance degradation when the strongest base model is combined with weaker but correlated learners; this was demonstrated experimentally in our results.**

### 4.5 Model ranking and practical interpretation

Across all tested methods, ranking by test-set mean R² was:

1. standard MLP (0.863)
2. weighted ensemble (0.797)
3. simple average ensemble (0.746)
4. XGBoost (0.603)
5. random forest (0.571)
6. stacking ensemble (0.562)
7. linear regression (0.332)

MAE-based ranking was consistent, with the standard MLP as best (4.03%).

### 4.6 Figure and table alignment

All figure references are formatted with **Figure** and all table references with **Table**, consistent with CACE style.

## 5. Conclusions

- The study converted 30 literature-based bio-oil compositions into six surrogate classes and generated Cantera simulation data at a structured 5T × 3P × 3S/C condition grid.
- After completeness filtering and normalization, 1,350 complete samples were used for model training and evaluation.
- On the test set, the standard MLP is the strongest model with R² = 0.863 and MAE = 4.03%.
- The constrained MLP and ensemble models did not outperform the standard MLP; in particular, weighted averaging, simple averaging, and stacking reduced predictive performance in this dataset.
- The model can support real-time monitoring and control-oriented workflows, particularly future MPC integration for process optimization.

The thermodynamic inverse mapping remains a practical but bounded soft-sensor solution. The present study used complete dataset consistency checks and can be interpreted as a first-stage deployment model for digital monitoring of bio-oil reforming processes.
