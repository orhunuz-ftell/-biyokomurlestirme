# AI-enabled inverse prediction of bio-oil composition from steam reforming syngas under data availability constraints

## Abstract

Fast inference of bio-oil composition can support energy-conversion control, but direct liquid characterization is slower than online syngas monitoring and available bio-oil composition datasets are incomplete. This study develops and evaluates an artificial intelligence soft sensor that predicts class-level bio-oil composition from steam reforming syngas and operating conditions. A SQL-curated literature dataset was first audited to quantify the composition-data constraints. The audit found 70 class-level bio-oil records, but no record contained all ten composition classes and only 30 records contained the six classes required for modeling. A Cantera reformer workflow generated 3,150 thermodynamic cases; after target-completeness filtering, 1,350 samples from 30 unique bio-oils were used to train inverse regression models. A multilayer perceptron with eight inputs and six outputs achieved row-wise test R2 = 0.863 and MAE = 4.03%, outperforming linear regression, random forest, XGBoost, constrained neural output, and ensemble variants. A stricter BiooilID holdout audit showed uneven generalization to unseen bio-oil identities, especially for alcohols, despite stronger behavior for aromatics and acids. The results show that AI can provide a useful syngas-to-composition soft sensor inside the represented composition domain, but reliable deployment requires group-aware validation, uncertainty estimation, and better stewardship of reusable bio-oil composition data.

## Keywords

Artificial intelligence; soft sensor; inverse modeling; bio-oil; syngas; steam reforming; data scarcity

## 1. Introduction

Artificial intelligence is increasingly used to accelerate energy-conversion modeling, process monitoring, and control [4]. Bio-oil steam reforming is a relevant but difficult case because the measurable gas output depends on a complex liquid feedstock whose composition is expensive and time-consuming to characterize [3]. If a model can infer bio-oil composition from reformer syngas, it could act as a soft sensor for quality monitoring and adaptive control.

The inverse task is fundamentally difficult. The forward mapping from bio-oil composition and process conditions to syngas is governed by thermodynamic equilibrium and reaction chemistry. The inverse mapping is ill-posed because multiple liquid compositions can produce similar syngas signatures. An AI model can therefore be useful only if its validation design reflects the difference between interpolation across known bio-oils and extrapolation to unseen bio-oil identities.

This study develops such an inverse soft-sensor workflow. It first audits a SQL-curated bio-oil composition database to identify data completeness constraints. It then uses Cantera to generate a thermodynamically consistent reforming dataset and compares several inverse regression models. Finally, it contrasts row-wise model performance with a BiooilID holdout audit to define the generalization boundary.

## 2. Data constraints and SQL audit

The source database contained 70 class-level bio-oil composition records connected to experiment, biomass, and reference tables. The linked records covered 14 distinct references, 43 biomass names, and pyrolysis temperatures between 300 and 850 degC. The composition fields were not uniformly populated. No record contained all ten targetable composition classes, while 30 of 70 records contained the six groups selected for inverse modeling: aromatics, acids, alcohols, furans, phenols, and aldehydes/ketones.

This incompleteness shaped the AI problem. The model could not be trained as a raw compound-level predictor or as a complete whole-oil composition estimator. It was restricted to six class-level targets. This framing is important for Energy and AI readers because model performance is inseparable from data provenance and validation design.

## 3. Simulation and learning workflow

Cantera was used to simulate reformer equilibrium for literature-derived bio-oil compositions [1]. Six surrogate species represented the major bio-oil groups: toluene, acetic acid, ethanol, furan, phenol, and acetone, following the model-compound logic used in bio-oil reforming analysis [2]. The process-condition grid included five temperatures, three pressures, and three steam-to-carbon ratios. The broader simulation layer contained 3,150 thermodynamic cases. After filtering for complete target variables, the machine-learning dataset contained 1,350 samples from 30 unique bio-oil compositions.

Inputs were reformer temperature, pressure, steam-to-carbon ratio, H2, CO, CO2, CH4, and H2O. Outputs were six bio-oil class percentages. The final multilayer perceptron used 128, 64, and 32 hidden neurons with regularization. Baselines included linear regression, random forest, XGBoost, constrained-output neural regression, and ensembles.

## 4. Results

The standard multilayer perceptron gave the strongest row-wise test performance, with average R2 = 0.863 and MAE = 4.03%. It outperformed linear regression (R2 = 0.332), random forest (R2 = 0.571), XGBoost (R2 = 0.603), and the best weighted ensemble (R2 = 0.797). Component-wise R2 values were 0.942 for aromatics, 0.877 for acids, 0.853 for alcohols, 0.897 for furans, 0.762 for phenols, and 0.849 for aldehydes/ketones.

However, row-wise performance overstates deployment readiness because the same bio-oil identity can appear under different process conditions across train and test partitions. A stricter BiooilID holdout audit held out entire bio-oil identities. Under this setting, aromatics and acids remained strong, but alcohols failed to generalize. This shows that the AI system learns both transferable syngas-composition signatures and dataset-specific composition patterns.

## 5. Discussion

The main AI contribution is not simply a high R2 value. The contribution is a workflow that links data curation, physics-based simulation, inverse learning, and group-aware validation. The results show that nonlinear AI can extract useful composition signals from syngas, but they also demonstrate the danger of claiming universal accuracy from row-wise splits in augmented simulation datasets.

For deployment, the soft sensor should be limited to composition domains represented in training data. Practical extensions should include uncertainty estimation, group-wise neural retraining, active learning for selecting new experiments, and explicit out-of-domain detection. These additions are more valuable than marginal architecture tuning because the limiting factor is data diversity.

## 6. Conclusions

An AI-enabled soft sensor was developed to infer six class-level bio-oil composition variables from steam reforming syngas and process conditions. A SQL audit showed that bio-oil composition reporting is incomplete and constrains model design. A Cantera workflow generated thermodynamic reforming data, and an MLP achieved row-wise R2 = 0.863 with MAE = 4.03%. Group-aware validation revealed weaker generalization for unseen bio-oil identities, especially alcohol-rich or low-variance cases. The study supports AI-based inverse monitoring for represented bio-oil domains while showing that robust generalization depends on better data stewardship, composition diversity, and validation protocols.

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
