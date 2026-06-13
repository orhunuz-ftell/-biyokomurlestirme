# Fuel-processing soft sensor for bio-oil steam reforming using Cantera-generated syngas data

## Abstract

Bio-oil steam reforming can produce hydrogen-rich syngas, but fuel-processing decisions depend on liquid bio-oil composition, which is slower to measure than gas-phase products. This study develops a soft sensor that estimates class-level bio-oil composition from reformer syngas and operating conditions. Literature-derived bio-oil compositions were mapped into six target groups and represented using surrogate compounds for Cantera steam reforming simulations. The broader simulation set contained 3,150 thermodynamic cases; 1,350 complete samples were used for machine learning. A multilayer perceptron predicted aromatics, acids, alcohols, furans, phenols, and aldehydes/ketones from eight inputs with row-wise test R2 = 0.863 and MAE = 4.03%, outperforming linear, tree-based, and ensemble alternatives. The workflow supports soft-sensor monitoring and future MPC for represented bio-oil domains. A BiooilID holdout audit showed that transfer to unseen bio-oil identities is component-dependent, especially for alcohols.

## Keywords

Bio-oil; steam reforming; fuel processing; syngas; hydrogen; soft sensor; inverse prediction

## 1. Introduction

Bio-oil produced from biomass pyrolysis is a renewable intermediate for fuel and hydrogen-oriented conversion routes [3]. Steam reforming is one route for converting oxygenated bio-oil fractions or model compounds into hydrogen-rich syngas [2]. However, bio-oil composition varies strongly with biomass type and pyrolysis conditions. This variability affects reformer behavior, hydrogen yield, methane formation, carbon distribution, and syngas quality.

For fuel-processing applications, online syngas monitoring is more practical than frequent detailed liquid characterization. This creates an opportunity for a soft sensor that infers bio-oil composition from reformer output. Such a tool would support feedstock quality tracking, process adjustment, and screening of bio-oil blends. The challenge is that inverse thermodynamic prediction is not unique, and the available literature-derived composition data are incomplete.

This study combines literature-based feed definition, thermodynamic simulation, and machine learning to evaluate a syngas-based bio-oil soft sensor. The manuscript focuses on fuel-processing utility and future MPC support.

## 2. Data and fuel representation

A SQL-curated bio-oil database was audited before model development. The `Biooil` table contained 70 class-level records linked to references, biomass records, and pyrolysis experiments. The records covered 14 linked references and 43 biomass names. No record contained all ten composition classes. Only 30 records contained the six classes required for the fuel-processing soft sensor: aromatics, acids, alcohols, furans, phenols, and aldehydes/ketones.

The six classes were represented by surrogate compounds for thermodynamic simulation: toluene, acetic acid, ethanol, furan, phenol, and acetone. This class-level surrogate representation is suitable for a screening-level reformer soft sensor, but it is not a substitute for detailed kinetic modeling or raw analytical characterization.

## 3. Reformer simulation

Cantera was used to simulate steam reforming equilibrium for the curated bio-oil compositions [1]. The reformer-only scope was selected to avoid introducing uncertain downstream separation assumptions. The process grid included temperatures of 650-850 degC, pressures of 5-30 bar, and steam-to-carbon ratios of 2.0-6.0. These conditions produced a thermodynamic reforming dataset with syngas composition outputs.

The complete simulation workflow generated 3,150 cases. After removing rows with incomplete target composition variables, 1,350 samples remained for machine learning. Inputs were reformer temperature, pressure, steam-to-carbon ratio, H2, CO, CO2, CH4, and H2O. Outputs were six class-level bio-oil composition percentages.

## 4. Inverse prediction models

Linear regression, random forest, XGBoost, multilayer perceptron, constrained-output multilayer perceptron, and ensemble models were compared. The standard multilayer perceptron used three hidden layers with 128, 64, and 32 neurons. Regularization was applied through dropout and batch normalization.

The best row-wise test performance was obtained by the standard multilayer perceptron. The model achieved average R2 = 0.863 and MAE = 4.03%. Component-wise R2 values were highest for aromatics, furans, acids, alcohols, and aldehydes/ketones, while phenols remained the weakest but still useful in the row-wise split.

Tree-based models were weaker: random forest reached R2 = 0.571 and XGBoost reached R2 = 0.603. The weighted ensemble reached R2 = 0.797, which was below the MLP, showing that ensemble averaging diluted the best model in this dataset.

## 5. Generalization and fuel-processing interpretation

The row-wise test result supports use as an interpolation soft sensor inside the represented fuel-composition space. However, a BiooilID holdout audit showed that fully unseen bio-oil identities are more difficult. Aromatics and acids transferred well, while alcohol prediction was not reliable under the holdout setting. This difference is important for fuel-processing deployment because a plant may encounter feedstocks outside the training composition domain.

The practical conclusion is that the model can support monitoring and decision support when the feedstock resembles curated training compositions. For new feedstock families, the soft sensor should be used with uncertainty flags and updated with additional characterization data.

## 6. Conclusions

A fuel-processing soft sensor was developed for bio-oil steam reforming. Literature-derived bio-oil compositions were converted into six surrogate feed classes, Cantera generated a thermodynamic reformer dataset, and a multilayer perceptron predicted six bio-oil classes from syngas and process conditions with row-wise R2 = 0.863 and MAE = 4.03%. Group-holdout analysis showed that generalization to unseen bio-oils is component-dependent. The approach is promising for fuel-processing monitoring and future MPC, but deployment requires uncertainty estimation and experimental validation.

## Data availability

The cleaned data tables, data dictionary, simulation scripts, model-training scripts, and model-performance files will be deposited in a public repository before submission. The DOI or repository URL will be inserted in the final manuscript.

## Declaration of generative AI and AI-assisted technologies

During preparation of the submission package, AI-assisted tools were used to organize source notes, draft editorial text, and prepare journal-specific submission materials. The authors reviewed, verified, and edited the content and take full responsibility for the final manuscript.

## References

1. D.G. Goodwin, H.K. Moffat, I. Schoegl, R.L. Speth, B.W. Weber, Cantera: An object-oriented software toolkit for chemical kinetics, thermodynamics, and transport processes, 2017.

2. E.C. Vagia, A.A. Lemonidou, Thermodynamic analysis of hydrogen production by steam reforming of bio-oil components, Int. J. Hydrogen Energy 32 (2007) 212-223.

3. A. Pafili, N.D. Charisiou, S.L. Douvartzides, G.I. Siakavelas, W. Wang, G. Liu, V.G. Papadakis, M.A. Goula, Recent progress in the steam reforming of bio-oil for hydrogen production: a review of operating parameters, catalytic systems and technological innovations, Catalysts 11 (2021) 1527. https://doi.org/10.3390/catal11121526.

4. E. Leng, B. He, J. Chen, G. Liao, Y. Ma, F. Zhang, S. Liu, J. E, Prediction of three-phase product distribution and bio-oil heating value of biomass fast pyrolysis based on machine learning, Energy 236 (2021) 121401. https://doi.org/10.1016/j.energy.2021.121401.

5. T.Q.S. Sampaio, S.B. Lima, C.A.M. Pires, Influence of extractives on the composition of bio-oil from biomass pyrolysis - a review, J. Anal. Appl. Pyrolysis 186 (2025) 106919. https://doi.org/10.1016/j.jaap.2024.106919.

6. J.M. Smith, R.W. Missen, Chemical Reaction Equilibrium Analysis: Theory and Algorithms, Wiley, New York, 1982.
