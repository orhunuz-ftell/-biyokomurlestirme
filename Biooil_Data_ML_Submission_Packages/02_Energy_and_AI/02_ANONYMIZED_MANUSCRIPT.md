# AI-enabled soft sensor for bio-oil steam reforming using Cantera-generated data and inverse syngas-to-composition prediction

## Abstract

Fast estimation of bio-oil composition can support energy-conversion monitoring and model predictive control, but detailed liquid characterization is slower than online syngas measurement. This study develops an AI-enabled soft sensor that predicts six class-level bio-oil composition groups from steam reforming syngas and operating conditions. Literature-derived bio-oil compositions were curated in a SQL database, mapped into aromatics, acids, alcohols, furans, phenols, and aldehydes/ketones, and converted into surrogate feed definitions. A Cantera reformer workflow generated 3,150 thermodynamic simulation cases across temperature, pressure, and steam-to-carbon ratio conditions. After target-completeness filtering and normalization, 1,350 samples from 30 unique bio-oils were used to train inverse regression models. A multilayer perceptron with eight inputs and six outputs achieved row-wise test R2 = 0.863 and MAE = 4.03%, outperforming linear regression, random forest, XGBoost, constrained neural output, and ensemble variants. The workflow provides a soft-sensor block for future MPC of bio-oil reforming. A BiooilID holdout audit showed that generalization to unseen bio-oil identities is component-dependent, indicating the need for uncertainty-aware deployment and further validation.

## Keywords

Artificial intelligence; soft sensor; bio-oil; Cantera; steam reforming; syngas; model predictive control

## 1. Introduction

AI-based soft sensors are increasingly useful in energy conversion systems where important state variables are difficult to measure directly. Bio-oil steam reforming is a strong example: syngas composition can be monitored rapidly, whereas detailed liquid bio-oil characterization requires slower offline analysis. For future MPC, estimating the incoming bio-oil composition from outlet syngas can provide the missing state information needed to optimize reformer temperature, pressure, and steam-to-carbon ratio.

This work develops an inverse AI model for that purpose. Literature-derived bio-oil compositions are used to define realistic feed mixtures, Cantera generates thermodynamically consistent reformer data, and machine learning maps syngas plus operating conditions back to bio-oil composition.

## 2. Data generation and model workflow

The source bio-oil compositions were curated in a SQL database and mapped into six functional groups: aromatics, acids, alcohols, furans, phenols, and aldehydes/ketones. These groups were represented with surrogate compounds and passed to a Cantera reformer model [1,2]. The simulation grid used five temperatures, three pressures, and three steam-to-carbon ratios. The workflow generated 3,150 thermodynamic cases, of which 1,350 samples from 30 unique bio-oil compositions were complete for inverse model training.

The model inputs were reformer temperature, pressure, steam-to-carbon ratio, and H2, CO, CO2, CH4, and H2O mole percentages. The outputs were the six bio-oil composition classes. Linear regression, random forest, XGBoost, standard MLP, constrained MLP, and ensemble models were compared.

## 3. Results

The standard MLP gave the best row-wise test performance with average R2 = 0.863 and MAE = 4.03%. Baseline models were weaker: linear regression reached R2 = 0.332, random forest reached R2 = 0.571, and XGBoost reached R2 = 0.603. The weighted ensemble reached R2 = 0.797, below the MLP.

Component-level MLP performance was strong for aromatics, acids, alcohols, furans, phenols, and aldehydes/ketones. Aromatics reached R2 = 0.942, while phenols were the weakest but still useful at R2 = 0.762. A BiooilID holdout audit showed that transfer to unseen bio-oil identities is less uniform, especially for alcohols.

## 4. Discussion

The main contribution is an AI soft-sensor workflow rather than a standalone data audit. The literature-derived bio-oil database provides feed diversity for Cantera simulation. The Cantera model creates a consistent thermodynamic training space. The MLP then learns the inverse relation needed for monitoring and future MPC.

For deployment, the model should operate within the represented bio-oil composition domain and should be paired with uncertainty checks. Future work should connect the inverse MLP to a forward surrogate and MPC optimizer, then validate the closed-loop workflow on new experimental reformer data.

## 5. Conclusions

An AI-enabled soft sensor was developed to estimate bio-oil composition from steam reforming syngas. Literature-derived bio-oil compositions were converted into Cantera feed definitions, 3,150 thermodynamic cases were generated, and 1,350 model-ready samples were used for inverse learning. The best MLP achieved row-wise R2 = 0.863 and MAE = 4.03%. The workflow supports future MPC integration for bio-oil reforming, while group-aware validation highlights the need for uncertainty-aware use on unseen bio-oil types.

## Data availability

The cleaned data tables, data dictionary, simulation scripts, model-training scripts, and model-performance files will be deposited in a public repository before submission. The DOI or repository URL will be inserted in the final manuscript.

## Declaration of generative AI and AI-assisted technologies

During preparation of the submission package, AI-assisted tools were used to organize source notes, draft editorial text, and prepare journal-specific submission materials. The authors reviewed, verified, and edited the content and take full responsibility for the final manuscript.

## References

1. D.G. Goodwin, H.K. Moffat, I. Schoegl, R.L. Speth, B.W. Weber, Cantera: An object-oriented software toolkit for chemical kinetics, thermodynamics, and transport processes, 2017.

2. E.C. Vagia, A.A. Lemonidou, Thermodynamic analysis of hydrogen production by steam reforming of bio-oil components, Int. J. Hydrogen Energy 32 (2007) 212-223.

3. A. Pafili, N.D. Charisiou, S.L. Douvartzides, G.I. Siakavelas, W. Wang, G. Liu, V.G. Papadakis, M.A. Goula, Recent progress in the steam reforming of bio-oil for hydrogen production: a review of operating parameters, catalytic systems and technological innovations, Catalysts 11 (2021) 1527. https://doi.org/10.3390/catal11121526.

4. E. Leng, B. He, J. Chen, G. Liao, Y. Ma, F. Zhang, S. Liu, J. E, Prediction of three-phase product distribution and bio-oil heating value of biomass fast pyrolysis based on machine learning, Energy 236 (2021) 121401. https://doi.org/10.1016/j.energy.2021.121401.
