# Machine-learning soft sensor for bio-oil steam reforming: Cantera-generated data and inverse prediction of bio-oil composition from syngas

## Abstract

Bio-oil steam reforming is a promising route for converting biomass pyrolysis liquids into hydrogen-rich syngas, but process monitoring and model predictive control require information on the incoming bio-oil composition. Because detailed liquid characterization is slower than online syngas analysis, this study develops a machine-learning soft sensor that estimates class-level bio-oil composition from reformer outlet gas and operating conditions. Literature-derived bio-oil compositions were first collected in a SQL database and mapped into six representative chemical groups: aromatics, acids, alcohols, furans, phenols, and aldehydes/ketones. These compositions were converted into surrogate mixtures and used as feed inputs for a Cantera steam reforming model. A reformer-only thermodynamic workflow generated 3,150 simulation cases over temperature, pressure, and steam-to-carbon ratio conditions. After target-completeness filtering and normalization, 1,350 samples from 30 unique bio-oil compositions were used for inverse machine learning. Linear regression, random forest, XGBoost, multilayer perceptron, constrained multilayer perceptron, and ensemble models were compared. The standard multilayer perceptron achieved the best row-wise test performance, with average R2 = 0.863 and MAE = 4.03%. Component-level R2 values ranged from 0.762 for phenols to 0.942 for aromatics. A BiooilID holdout audit further showed that transfer to unseen bio-oil identities is component-dependent. The proposed workflow provides a computational soft-sensor foundation for bio-oil reforming monitoring and future MPC integration.

## Keywords

Bio-oil; steam reforming; Cantera; machine learning; soft sensor; model predictive control; syngas

## 1. Introduction

Bio-oil obtained from biomass pyrolysis is a renewable intermediate for fuels, hydrogen, chemicals, carbon materials, and upgrading processes (Sharifzadeh and Sadeqzadeh, 2019; Zhang et al., 2022). Its practical use is challenging because its composition varies substantially with biomass type, pretreatment, pyrolysis temperature, residence time, and collection strategy. The relative amounts of aromatics, acids, alcohols, furans, phenols, and carbonyl compounds affect reforming behavior, hydrogen production potential, methane formation, coke tendency, corrosion risk, and syngas quality (Pafili et al., 2021; Singh and Jaswal, 2024).

For a future bio-oil reforming process, the most useful control variable is not only the current reformer condition, but also the changing composition of the incoming bio-oil. Direct and detailed bio-oil characterization generally requires offline analytical steps such as GC-MS, FTIR, elemental analysis, or wet chemical procedures. In contrast, syngas composition can be monitored more rapidly from the reformer outlet. This difference motivates a soft-sensor approach: infer the incoming bio-oil composition from measurable reformer outlet gas and known operating conditions.

The intended use of the model in this work is therefore process monitoring and future model predictive control (MPC). In an MPC structure, a soft sensor can estimate bio-oil composition from measured syngas, and the estimated composition can then be passed to a forward surrogate or process model to adjust reformer temperature, pressure, and steam-to-carbon ratio. Such a workflow can support feedstock quality tracking, abnormal-feed detection, and operating-condition optimization without requiring continuous detailed liquid analysis.

The main obstacle is that the inverse mapping is difficult. The forward relation from bio-oil composition and reformer conditions to equilibrium syngas is governed by thermodynamics. The reverse relation is less direct because several different bio-oil mixtures can generate similar outlet gas compositions under related process conditions. A machine-learning model for this problem should therefore be treated as a domain-aware soft sensor rather than a replacement for analytical characterization.

The objective of this study is to develop and evaluate such a soft sensor. The work follows four steps. First, literature-derived bio-oil compositions are curated into a structured SQL database and mapped into six functional groups. Second, these compositions are converted into surrogate chemical mixtures for Cantera steam reforming simulations. Third, a synthetic thermodynamic dataset is generated over a structured operating-condition grid. Fourth, inverse machine-learning models are trained to estimate bio-oil composition from syngas composition and process conditions. The primary novelty is the integrated Cantera-to-ML inverse workflow for bio-oil steam reforming soft sensing.

## 2. Bio-oil composition data used for simulation inputs

The experimental bio-oil composition data were collected to define realistic feed compositions for the Cantera simulation workflow. The SQL Server database contains literature-derived biomass, pyrolysis, bio-oil, and reforming records. The `Biooil` table contains 70 class-level bio-oil composition records linked to experiment, biomass, and reference metadata. These records are linked to 14 distinct references and 43 biomass names, with pyrolysis process temperatures ranging from 300 to 850 degC.

The purpose of this database in the present manuscript is not to claim a complete bio-oil composition repository. Its role is to provide literature-grounded input compositions for thermodynamic data generation. Because the Cantera surrogate model requires complete values for the six selected functional groups, records were filtered for aromatics, acids, alcohols, furans, phenols, and aldehydes/ketones. This yielded 30 unique model-ready bio-oil compositions.

The six-class representation was selected because it balances literature availability, chemical interpretability, and simulation feasibility. The groups correspond to major bio-oil families that influence reforming chemistry and syngas composition. Class-level data were normalized before simulation so that the target composition vector represented a consistent six-component bio-oil feed profile.

The SQL audit remains useful for defining the modeling boundary. No `Biooil` record contained all ten broader composition classes available in the database, and only 30 of 70 records contained the six groups required for the present model. Thus, the resulting ML model should be interpreted as valid within the represented six-class composition domain.

## 3. Cantera steam reforming data generation

### 3.1 Reformer-only simulation scope

Steam reforming simulations were performed with Cantera using a reformer-only thermodynamic equilibrium workflow (Goodwin et al., 2017). The reformer was selected as the modeling focus because the bio-oil composition has its most direct influence at this stage. Downstream units such as water-gas shift reactors, CO2 removal, and PSA purification are important in industrial hydrogen production, but including them would introduce additional unit-specific assumptions and separation parameters. For a soft sensor whose purpose is to infer feed composition from reformer gas, the reformer outlet is the most direct measurement point.

The simulation method is based on equilibrium calculation through Gibbs free energy minimization. At a fixed temperature and pressure, Cantera determines the equilibrium composition subject to elemental conservation and non-negative species constraints. This approach is appropriate for generating a consistent thermodynamic dataset for machine-learning model development, especially when the goal is to create a structured data layer rather than fit one specific reactor experiment.

### 3.2 Surrogate representation of bio-oil classes

Each of the six bio-oil functional groups was represented by a surrogate molecule:

- Aromatics: toluene, C7H8.
- Acids: acetic acid, CH3COOH.
- Alcohols: ethanol, C2H5OH.
- Furans: furan, C4H4O.
- Phenols: phenol, C6H6O.
- Aldehydes/ketones: acetone, C3H6O.

This surrogate strategy follows the common practice of representing complex bio-oil mixtures using model compounds for thermodynamic or catalytic reforming studies (Vagia and Lemonidou, 2007). The surrogate composition was not intended to reproduce every individual compound in bio-oil. It was designed to preserve class-level differences that can influence the reformer equilibrium output and therefore provide learnable signals for a soft sensor.

### 3.3 Operating-condition grid

For each bio-oil composition, simulations were performed over a structured grid:

- Reformer temperature: 650, 700, 750, 800, and 850 degC.
- Pressure: 5, 15, and 30 bar.
- Steam-to-carbon ratio: 2.0, 4.0, and 6.0.

The grid produced 45 operating-condition combinations per bio-oil. Across the broader 70 bio-oil records, this corresponded to 3,150 Cantera reforming cases. After removing cases without complete six-class target values, 1,350 samples from 30 unique bio-oil compositions remained for inverse model training and testing.

### 3.4 Simulation outputs

The primary simulation outputs used for inverse prediction were the reformer outlet mole percentages of H2, CO, CO2, CH4, and H2O. Additional thermodynamic and performance fields were generated in the broader workflow, including enthalpy, entropy, density, molecular weight, H2/CO ratio, dry-basis hydrogen content, and carbon/hydrogen distribution indicators. The inverse model in this manuscript uses the gas composition and operating conditions because these are the variables most relevant for online monitoring.

The final inverse-model input vector contains eight variables:

- Reformer temperature.
- Reformer pressure.
- Steam-to-carbon ratio.
- H2 mole percent.
- CO mole percent.
- CO2 mole percent.
- CH4 mole percent.
- H2O mole percent.

The output vector contains six variables:

- Aromatics wt%.
- Acids wt%.
- Alcohols wt%.
- Furans wt%.
- Phenols wt%.
- Aldehydes/ketones wt%.

## 4. Software implementation and model development

### 4.1 Code structure

The computational workflow was implemented as a multi-stage Python project. The Cantera data-generation layer includes modules for input processing, equilibrium calculation, property calculation, validation, and database writing. The reverse machine-learning layer includes modules for data loading, baseline models, deep-learning models, ensemble models, test evaluation, and visualization.

The main implementation files used in the workflow include:

- `generate_data_cantera.py` for Cantera data generation.
- `biooil_mechanism.yaml` for the custom bio-oil surrogate mechanism.
- `cantera_equilibrium.py` for equilibrium calculation.
- `cantera_input_processor.py` for preparing bio-oil and process-condition inputs.
- `database_writer.py` for saving simulation outputs.
- `validation.py` for checking thermodynamic consistency.
- `data_loader.py` for reverse-ML data preparation.
- `baseline_models.py` for linear regression, random forest, and XGBoost models.
- `deep_learning_models.py` for standard and constrained MLP models.
- `ensemble_models.py` for simple averaging, weighted averaging, and stacking.
- `test_evaluation.py` for final test metrics.
- `visualization.py` for model-performance and feature-importance plots.

In total, the current deposited workflow contains more than 1000 lines of project-specific Python code across the Cantera generation, machine-learning, validation, and visualization modules, in addition to the custom Cantera YAML mechanism and configuration files. The code was organized so that data generation, model training, model evaluation, and figure generation can be executed as separate steps.

### 4.2 Data cleaning and splitting

The simulation workflow generated 3,150 rows. For inverse model training, rows with missing values in any of the six target composition groups were removed. This left 1,350 complete samples. The target composition values were normalized to a consistent six-class basis so that the model learned relative class distribution rather than inconsistent partial sums.

The primary reported model comparison uses a row-wise train, validation, and test split:

- Training set: 944 samples.
- Validation set: 203 samples.
- Test set: 203 samples.
- Total: 1,350 samples.

This split evaluates whether the model can interpolate across reformer operating conditions and composition patterns represented in the generated dataset. Because each bio-oil composition is simulated across multiple process conditions, an additional BiooilID holdout audit was also performed to evaluate transfer to unseen bio-oil identities.

### 4.3 Baseline machine-learning models

Three baseline models were developed before neural-network training:

1. Linear regression.
2. Random forest regression.
3. XGBoost regression.

Linear regression provided a lower-bound reference for the inverse mapping. Random forest and XGBoost were used to test whether nonlinear tree-based models could capture relationships between syngas composition and bio-oil classes. The baseline models also provided feature-importance information. The average random forest feature-importance analysis indicated that syngas composition dominates the inverse signal: CH4, CO2, H2O, H2, and CO together contributed most of the predictive information, whereas reformer temperature, pressure, and steam-to-carbon ratio had smaller direct importance in the inverse task.

### 4.4 Deep-learning models

The main model was a standard multilayer perceptron (MLP). The architecture used eight input neurons, three hidden layers, and six output neurons:

- Input layer: 8 features.
- Hidden layer 1: 128 neurons.
- Hidden layer 2: 64 neurons.
- Hidden layer 3: 32 neurons.
- Output layer: 6 bio-oil composition classes.

Batch normalization was applied after hidden layers to stabilize training. Dropout regularization was used to reduce overfitting. The training procedure used the Adam optimizer, mini-batch learning, early stopping, and learning-rate reduction during plateau behavior. A constrained MLP with a softmax-style output was also tested to force composition closure to 100%, but this constraint reduced predictive accuracy relative to the standard MLP.

### 4.5 Ensemble models

Three ensemble strategies were evaluated:

- Simple average ensemble combining random forest, XGBoost, and MLP predictions.
- Weighted ensemble with higher weight assigned to the MLP.
- Stacking ensemble using model predictions as meta-features.

The ensembles were included to test whether combining tree-based and neural models could improve robustness. In this dataset, the standard MLP was already the strongest individual learner, and adding weaker correlated learners reduced average performance.

### 4.6 BiooilID holdout audit

The row-wise split is useful for evaluating interpolation across process conditions, but it does not fully represent the case where a process encounters a completely unseen bio-oil composition. Therefore, an additional BiooilID-based holdout audit was performed. In this audit, 24 BiooilIDs were assigned to training and 6 BiooilIDs were held out for testing, corresponding to 1080 training samples and 270 test samples. This audit was used to identify generalization limits and define the safe operating interpretation of the soft sensor.

## 5. Results

### 5.1 Row-wise model comparison

The row-wise test results show that the inverse mapping contains a strong nonlinear signal. Linear regression achieved average R2 = 0.332 and MAE = 9.92%, confirming that a linear mapping is insufficient. Random forest improved the average R2 to 0.571 with MAE = 6.25%. XGBoost achieved average R2 = 0.603 and MAE = 6.10%.

The standard MLP achieved the best performance:

- Average R2 = 0.863.
- Average RMSE = 5.87%.
- Average MAE = 4.03%.

The constrained MLP produced physically closed outputs but had lower average performance, with test R2 = 0.745 and MAE = 11.54%. The weighted ensemble reached R2 = 0.797 and MAE = 4.75%, while the simple average ensemble reached R2 = 0.746. Stacking did not improve the results and achieved R2 = 0.562.

These results indicate that the standard MLP is the most suitable soft-sensor model for the represented dataset. The nonlinear neural architecture captures interactions between syngas composition and bio-oil class distribution more effectively than linear or tree-based models.

### 5.2 Component-level prediction performance

The standard MLP gave the following row-wise component-level test results:

- Aromatics: R2 = 0.942, RMSE = 8.70%, MAE = 6.35%.
- Acids: R2 = 0.877, RMSE = 6.46%, MAE = 4.80%.
- Alcohols: R2 = 0.853, RMSE = 4.82%, MAE = 3.41%.
- Furans: R2 = 0.897, RMSE = 1.50%, MAE = 1.05%.
- Phenols: R2 = 0.762, RMSE = 8.42%, MAE = 5.28%.
- Aldehydes/ketones: R2 = 0.849, RMSE = 5.30%, MAE = 3.29%.

Aromatics, furans, and acids were especially predictable. Phenols were the most difficult among the six groups but still retained useful predictive performance under the row-wise split. This pattern is chemically plausible because some classes leave stronger signatures in CH4, CO2, and H2O distributions than others.

### 5.3 Feature interpretation

The feature-importance analysis from the random forest baseline showed that the gas-phase outputs carry most of the inverse information. CH4 mole percent and CO2 mole percent were the most influential variables, followed by H2O, H2, and CO. This supports the chemical interpretation that carbon-hydrogen-oxygen balance in the bio-oil feed is reflected in the reformer gas composition.

Operating conditions were less dominant in the inverse task than syngas composition. This does not mean that temperature, pressure, and steam-to-carbon ratio are unimportant for reforming. Rather, once syngas composition is included as an input, the measured gas composition already carries much of the information produced by the operating state.

### 5.4 BiooilID holdout behavior

The BiooilID holdout audit showed that generalization to entirely unseen bio-oil identities is more difficult than row-wise interpolation. Aromatics and acids remained relatively strong under the holdout setting, with R2 values of 0.951 and 0.803, respectively. Phenols and aldehydes/ketones showed moderate performance, while furans were weaker and alcohols produced a negative R2 value. The average MAE remained 4.62%, but the average R2 was strongly affected by the alcohol result.

This outcome is important for practical deployment. The row-wise MLP result supports the soft sensor for bio-oils similar to those represented in the training domain and across changing process conditions. For completely new bio-oil chemistries, the model should be used with uncertainty checks, domain monitoring, or periodic recalibration with new characterization data.

## 6. Relevance to MPC and process monitoring

The developed inverse model is intended as the sensing block of a future MPC framework for bio-oil steam reforming. In such a framework, the sequence is:

1. Measure reformer syngas composition.
2. Use the inverse MLP soft sensor to estimate bio-oil class composition.
3. Pass the estimated composition to a forward surrogate or reformer model.
4. Optimize reformer temperature, pressure, and steam-to-carbon ratio for a target such as H2/CO ratio, hydrogen-rich syngas quality, or operating cost.
5. Apply the selected control move and repeat the cycle with new syngas measurements.

This structure is useful because direct bio-oil composition measurement is not convenient for rapid control. The soft sensor provides a computational estimate that can be updated whenever gas measurements are available. The present study develops and validates the inverse prediction block required for this control architecture.

The model should be deployed as a decision-support soft sensor rather than an absolute analytical instrument. The safest operating domain is the composition range represented by the curated bio-oil dataset. If a new biomass source or pyrolysis condition produces a bio-oil outside this domain, the MPC system should flag uncertainty and request additional characterization or model updating.

## 7. Limitations and future work

The Cantera model is thermodynamic and reformer-only. It does not include catalyst deactivation, kinetic rate limitations, reactor hydrodynamics, heat-transfer limitations, or downstream separation units. The bio-oil composition is represented by six surrogate classes rather than detailed molecular composition. These choices are appropriate for generating a consistent synthetic dataset and developing a soft-sensor proof of concept, but they limit direct extrapolation to every industrial reactor.

The strongest model result is based on a row-wise split of simulation-expanded data. This is useful for evaluating process-condition interpolation but can overestimate performance for fully unseen bio-oil identities. The BiooilID holdout audit was therefore included to define the model boundary. Future work should train the final neural model directly under group-based splits, add uncertainty quantification, and validate the workflow with new experimental reformer data.

Future extensions should also connect the inverse soft sensor to a forward surrogate and MPC optimizer. The forward model can predict syngas quality from estimated bio-oil composition and candidate operating conditions. The controller can then optimize temperature, pressure, and steam-to-carbon ratio to meet H2/CO or hydrogen-production targets.

## 8. Conclusions

This study developed a machine-learning soft sensor for estimating bio-oil composition from steam reforming syngas and operating conditions. Literature-derived bio-oil compositions were curated into six functional groups and used as realistic feed inputs for a Cantera reforming workflow. The simulation layer generated 3,150 thermodynamic cases, and 1,350 complete samples from 30 unique bio-oil compositions were used for inverse model training. Among linear, tree-based, neural, and ensemble models, the standard MLP achieved the best row-wise test performance with average R2 = 0.863 and MAE = 4.03%. Component-level results showed strong prediction of aromatics, acids, alcohols, furans, phenols, and aldehydes/ketones within the represented data domain. A BiooilID holdout audit clarified that generalization to unseen bio-oils is component-dependent. The workflow provides a practical computational basis for syngas-based bio-oil monitoring and future MPC integration in bio-oil steam reforming systems.

## Data availability

The cleaned data tables, data dictionary, simulation scripts, model-training scripts, and model-performance files will be deposited in a public repository before submission. Until a DOI is assigned, the local source files are available in the project repository under `reverse_ml_biooil_to_product/` and `Biooil_Data_ML_Submission_Packages/04_Data_Repository_Package/`.

## Declaration of generative AI and AI-assisted technologies

During preparation of the submission package, AI-assisted tools were used to organize source notes, draft editorial text, and prepare journal-specific submission materials. The authors reviewed, verified, and edited the content and take full responsibility for the final manuscript.

## References

AspenTech, 2022. Aspen Plus V12 Documentation. AspenTech Technical Reference, pp. 1-1500.

Bordoloi, N., Narzari, R., Sut, D., Saikia, R., Chutia, R.S., Kataki, R., 2016. Characterization of bio-oil and its sub-fractions from pyrolysis of Scenedesmus dimorphus. Renew. Energy 98, 245-253. https://doi.org/10.1016/j.renene.2016.03.081.

Chen, D., Cen, K., Jing, X., Gao, J., Li, C., Ma, Z., 2017. An approach for upgrading biomass and pyrolysis product quality using a combination of aqueous phase bio-oil washing and torrefaction pretreatment. Bioresour. Technol. 233, 150-158. https://doi.org/10.1016/j.biortech.2017.02.120.

Goodwin, D.G., Moffat, H.K., Schoegl, I., Speth, R.L., Weber, B.W., 2017. Cantera: An object-oriented software toolkit for chemical kinetics, thermodynamics, and transport processes.

Leng, E., He, B., Chen, J., Liao, G., Ma, Y., Zhang, F., Liu, S., E, J., 2021. Prediction of three-phase product distribution and bio-oil heating value of biomass fast pyrolysis based on machine learning. Energy 236, 121401. https://doi.org/10.1016/j.energy.2021.121401.

Modak, S., Katiyar, P., Yadav, S., Jain, S., Gole, B., Talukdar, D., 2023. Generation and characterization of bio-oil obtained from the slow pyrolysis of cooked food waste at various temperatures. Waste Manag. 158, 23-36. https://doi.org/10.1016/j.wasman.2023.01.002.

Mullen, C.A., Boateng, A.A., Hicks, K.B., Goldberg, N.M., Moreau, R.A., 2010. Analysis and comparison of bio-oil produced by fast pyrolysis from three barley biomass/byproduct streams. Energy Fuels 24, 699-706. https://doi.org/10.1021/ef900912s.

Pafili, A., Charisiou, N.D., Douvartzides, S.L., Siakavelas, G.I., Wang, W., Liu, G., Papadakis, V.G., Goula, M.A., 2021. Recent progress in the steam reforming of bio-oil for hydrogen production: a review of operating parameters, catalytic systems and technological innovations. Catalysts 11, 1527. https://doi.org/10.3390/catal11121526.

Sampaio, T.Q.S., Lima, S.B., Pires, C.A.M., 2025. Influence of extractives on the composition of bio-oil from biomass pyrolysis - a review. J. Anal. Appl. Pyrolysis 186, 106919. https://doi.org/10.1016/j.jaap.2024.106919.

Sharifzadeh, M., Sadeqzadeh, M., 2019. The multi-scale challenges of biomass fast pyrolysis and bio-oil upgrading: review of the state of art and future research directions. Prog. Energy Combust. Sci. 71, 1-80.

Singh, P.P., Jaswal, A., 2024. Green hydrogen production from biomass - a thermodynamic assessment of the potential of conventional and advanced bio-oil steam reforming processes. Int. J. Hydrogen Energy 50, 627-639.

Smith, J.M., Missen, R.W., 1982. Chemical Reaction Equilibrium Analysis: Theory and Algorithms. Wiley, New York.

Vagia, E.C., Lemonidou, A.A., 2007. Thermodynamic analysis of hydrogen production by steam reforming of bio-oil components. Int. J. Hydrogen Energy 32, 212-223.

Zhang, S., Chen, T., Xiong, Y., Dong, Q., 2022. A comprehensive review of bio-oil, bio-binder and bio-asphalt materials: their source, composition, preparation and performance. J. Traffic Transp. Eng. Engl. Ed. 9, 151-166.
