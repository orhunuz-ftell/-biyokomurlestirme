# A Cantera-assisted inverse deep-learning soft sensor for bio-oil steam reforming

## Abstract

Detailed characterization of pyrolysis bio-oil is commonly performed offline, whereas reformer outlet gas composition can be measured more readily for process monitoring. This study develops a Cantera-assisted inverse soft sensor that estimates six bio-oil composition classes from steam-reforming syngas and operating conditions. Literature-derived bio-oil compositions were curated in a relational database and represented by surrogate compounds for aromatics, acids, alcohols, furans, phenols, and aldehydes/ketones. A thermodynamic equilibrium workflow generated 3,150 reforming cases over temperature, pressure, and steam-to-carbon ratio grids. After completeness filtering, 1,350 samples from 30 bio-oil compositions were used for inverse modeling. Linear regression, random forest, XGBoost, standard and composition-constrained multilayer perceptrons, and three ensemble strategies were compared using a 70/15/15 row-wise split. The standard multilayer perceptron achieved the best test performance, with mean R² = 0.863, root mean squared error = 5.87 wt.%, and mean absolute error = 4.03 wt.%. Component-level R² ranged from 0.762 for phenols to 0.942 for aromatics. Methane and carbon dioxide were the most influential inputs in the random-forest interpretation. Enforcing exact composition closure reduced predictive accuracy, and none of the ensemble strategies outperformed the standard neural network. The results establish a simulation-domain proof of concept for syngas-based monitoring of bio-oil reforming and define the validation required before experimental or control-system deployment.

## Keywords

Bio-oil; steam reforming; soft sensor; inverse modeling; Cantera; deep learning; process monitoring

## 1. Introduction

Fast and slow pyrolysis convert biomass into gas, char, and a liquid fraction generally referred to as bio-oil. The liquid product is a potential intermediate for renewable fuels, chemicals, materials, and hydrogen production, but its composition varies strongly with biomass origin, pretreatment, reactor configuration, temperature, heating rate, residence time, and condensation strategy (Bridgwater, 2012; Sharifzadeh and Sadeqzadeh, 2019; Zhang et al., 2022). This variability affects acidity, stability, heating value, coke tendency, catalyst performance, and the composition of products obtained during upgrading or reforming.

Steam reforming is a promising route for converting the oxygenated fraction of bio-oil into hydrogen-rich synthesis gas. The process is nevertheless sensitive to feed composition and operating conditions, while the molecular complexity of bio-oil complicates mechanistic reactor modeling (Vagia and Lemonidou, 2007; Pafili et al., 2021; Singh and Jaswal, 2024). Detailed liquid characterization typically relies on offline methods such as gas chromatography-mass spectrometry, Fourier-transform infrared spectroscopy, elemental analysis, and wet-chemical procedures (Oasmaa and Peacocke, 2010). Reformer outlet gas composition, in contrast, is more compatible with frequent or online measurement. This difference creates an opportunity for a soft sensor that infers feed composition from measured syngas and known operating conditions.

Machine learning has been increasingly applied to biomass conversion for forward prediction of yields, product distributions, and fuel properties (Leng et al., 2021). The present problem is different: it seeks the inverse relation from reformer outputs to feed composition. Such inverse mappings may be ill posed because distinct feed mixtures can approach similar equilibrium gas states. A useful model must therefore capture nonlinear interactions while being interpreted within the composition and operating domain represented during training.

This study develops a simulation-assisted inverse soft sensor for bio-oil steam reforming. Its contributions are: (i) the curation of literature-derived bio-oil compositions into six chemically interpretable classes; (ii) thermodynamically consistent data generation with Cantera over a structured process grid; (iii) a comparison of linear, tree-based, deep-learning, constrained-output, and ensemble inverse models; and (iv) interpretation of the resulting soft sensor from a process-monitoring perspective. The intended contribution to process systems engineering is the integration of a thermodynamic simulator and a data-driven inverse estimator that can later serve as a sensing block in model predictive control (MPC).

> **[INSERT FIGURE 1 HERE]**
>
> **Figure 1.** Overall workflow from literature-derived bio-oil compositions to Cantera simulation, inverse model training, and syngas-based soft sensing.

## 2. Materials and methods

### 2.1. Literature-derived bio-oil composition data

Experimental bio-oil composition data were collected from published pyrolysis studies and stored in a SQL Server relational database. The database links biomass identity, pyrolysis conditions, bio-oil composition, and bibliographic metadata. It contains 70 class-level bio-oil records spanning 43 biomass names and pyrolysis temperatures from 300 to 850 °C. Representative source studies include analyses of algal, agricultural-residue, food-waste, and lignocellulosic bio-oils (Mullen et al., 2010; Bordoloi et al., 2016; Chen et al., 2017; Modak et al., 2023).

The database includes a broader set of chemical classes, but many literature records are incomplete. The inverse workflow therefore retained records containing all six target groups: aromatics, acids, alcohols, furans, phenols, and aldehydes/ketones. Thirty unique bio-oil compositions met this requirement. Their six retained fractions were normalized to a common 100 wt.% basis before simulation. This normalization defines the model target as a class-level surrogate composition rather than the complete molecular composition of raw bio-oil.

### 2.2. Surrogate representation

Each chemical class was represented by one model compound: toluene for aromatics, acetic acid for acids, ethanol for alcohols, furan for furans, phenol for phenols, and acetone for aldehydes/ketones. Model compounds are commonly used to reduce the complexity of thermodynamic and catalytic studies of bio-oil reforming (Vagia and Lemonidou, 2007). The surrogate set was selected to preserve differences in carbon, hydrogen, and oxygen balance among the six classes while remaining compatible with the thermodynamic mechanism used in Cantera.

Table 1 summarizes the class representation.

**Table 1. Bio-oil classes and surrogate compounds used in the simulation.**

| Target class | Surrogate compound | Formula |
|---|---|---|
| Aromatics | Toluene | C7H8 |
| Acids | Acetic acid | C2H4O2 |
| Alcohols | Ethanol | C2H6O |
| Furans | Furan | C4H4O |
| Phenols | Phenol | C6H6O |
| Aldehydes/ketones | Acetone | C3H6O |

### 2.3. Cantera equilibrium model

Steam-reforming data were generated with Cantera 3.2.0, an open-source framework for thermodynamics, chemical kinetics, and transport calculations (Goodwin et al., 2025). The model represents the reformer at thermodynamic equilibrium. At specified temperature and pressure, the equilibrium state minimizes total Gibbs free energy subject to elemental conservation and non-negative species amounts (Smith and Missen, 1982):

\[
\min_{n_i} G = \sum_i n_i\mu_i, \qquad
\mu_i = \mu_i^{\circ} + RT\ln a_i,
\tag{1}
\]

where \(n_i\) is the amount of species \(i\), \(\mu_i\) is its chemical potential, \(R\) is the universal gas constant, \(T\) is temperature, and \(a_i\) is activity. Elemental carbon, hydrogen, and oxygen balances were checked for each converged case.

The reformer-only boundary was selected because the inlet bio-oil composition has its most direct effect on this unit. Downstream water-gas shift, carbon-dioxide removal, and pressure-swing adsorption are relevant to hydrogen purification but were excluded from the inverse-model boundary. Accordingly, the model estimates feed composition from reformer outlet gas rather than from final purified hydrogen.

> **[INSERT FIGURE 2 HERE]**
>
> **Figure 2.** Cantera data-generation workflow, including surrogate-feed construction, operating-condition assignment, equilibrium calculation, validation, and database storage.

### 2.4. Operating grid and generated dataset

For each literature-derived bio-oil composition, simulations were conducted over five temperatures (650, 700, 750, 800, and 850 °C), three pressures (5, 15, and 30 bar), and three steam-to-carbon ratios (2.0, 4.0, and 6.0). The full factorial grid contains 45 operating points per composition. Across the original 70 records, 3,150 cases were generated. Removal of records without complete six-class targets left 30 compositions and 1,350 complete cases for machine learning.

The final inverse-model input vector comprised eight variables: reformer temperature, pressure, steam-to-carbon ratio, and outlet mole percentages of H2, CO, CO2, CH4, and H2O. The output vector comprised the normalized weight percentages of the six bio-oil classes. Table 2 defines the modeling dataset.

**Table 2. Inverse-model dataset and row-wise split used in this study.**

| Item | Value |
|---|---:|
| Original Cantera cases | 3,150 |
| Complete model-ready cases | 1,350 |
| Unique model-ready bio-oil compositions | 30 |
| Input variables | 8 |
| Output variables | 6 |
| Training samples | 944 |
| Validation samples | 203 |
| Test samples | 203 |

The primary comparison used a random row-wise split of approximately 70% training, 15% validation, and 15% testing. Because each bio-oil composition contributes multiple operating-condition rows, this protocol measures interpolation within the simulation-expanded data domain. It does not by itself establish transfer to a completely unseen bio-oil identity.

### 2.5. Machine-learning models

Linear regression was used as a lower-bound baseline. Random forest and XGBoost represented nonlinear tree-based learners. The principal deep-learning model was a multilayer perceptron (MLP) with eight inputs, hidden layers of 128, 64, and 32 neurons, and six linear outputs. Batch normalization followed the hidden layers, while dropout rates of 0.30, 0.20, and 0.10 were used from the first to the third hidden layer. Training used the Adam optimizer, a batch size of 32, a maximum of 200 epochs, early stopping with a patience of 30 epochs, and learning-rate reduction with a patience of 15 epochs.

A second MLP used a softmax-style output to impose exact closure of the six predicted fractions to 100%. This constrained model was evaluated to quantify the trade-off between compositional consistency and prediction error. Three ensembles were also tested: an equal average of random forest, XGBoost, and standard MLP; a weighted average assigning weights of 0.25, 0.25, and 0.50, respectively; and a stacking model with ridge regression as the meta-learner.

The model-development environment used Python 3.11, TensorFlow/Keras 2.12.0, scikit-learn 1.2.2, and XGBoost 1.7.5. Data splitting and the tree-based models used a fixed random state of 42.

> **[INSERT FIGURE 3 HERE]**
>
> **Figure 3.** Standard MLP architecture with eight inputs, three hidden layers, and six bio-oil composition outputs.

### 2.6. Performance measures

Model performance was assessed separately for each output using the coefficient of determination (R²), root mean squared error (RMSE), and mean absolute error (MAE):

\[
R^2_j = 1 - \frac{\sum_{i=1}^{N}(y_{ij}-\hat{y}_{ij})^2}
{\sum_{i=1}^{N}(y_{ij}-\bar{y}_{j})^2},
\tag{2}
\]

\[
\mathrm{RMSE}_j = \sqrt{\frac{1}{N}\sum_{i=1}^{N}(y_{ij}-\hat{y}_{ij})^2},
\tag{3}
\]

\[
\mathrm{MAE}_j = \frac{1}{N}\sum_{i=1}^{N}|y_{ij}-\hat{y}_{ij}|.
\tag{4}
\]

The reported overall values are arithmetic means across the six output classes. RMSE and MAE are reported in percentage points on the normalized composition basis.

## 3. Results and discussion

### 3.1. Comparison of inverse models

Table 3 reports the test-set results. Linear regression explained only 33.2% of the target variance on average, indicating that the inverse mapping cannot be represented adequately by one linear relation. Random forest and XGBoost improved the mean R² to 0.571 and 0.603, respectively. The standard MLP was the strongest model, with mean R² = 0.863, RMSE = 5.87 wt.%, and MAE = 4.03 wt.%.

**Table 3. Test-set comparison of inverse modeling strategies.**

| Model | Mean R² | Mean RMSE (wt.%) | Mean MAE (wt.%) |
|---|---:|---:|---:|
| Linear regression | 0.332 | 13.38 | 9.92 |
| Random forest | 0.571 | 9.83 | 6.25 |
| XGBoost | 0.603 | 9.50 | 6.10 |
| Standard MLP | **0.863** | **5.87** | **4.03** |
| Constrained MLP | 0.745 | 15.06 | 11.54 |
| Simple-average ensemble | 0.746 | 7.69 | 5.16 |
| Weighted-average ensemble | 0.797 | 6.94 | 4.75 |
| Stacking ensemble | 0.562 | 9.95 | 6.34 |

The standard MLP improved mean R² by 0.292 absolute points relative to random forest, corresponding to a 51.1% relative increase when random forest is used as the baseline. The comparison supports the use of a multilayer nonlinear representation for this inverse equilibrium mapping. It does not imply that neural networks will universally outperform tree models outside the present data and tuning protocol.

> **[INSERT FIGURE 4 HERE]**
>
> **Figure 4.** Test-set comparison of the standard MLP, baseline models, constrained MLP, and ensemble strategies using mean R², RMSE, and MAE.

### 3.2. Component-level MLP performance

The standard MLP produced R² values above 0.84 for five of the six classes (Table 4). Aromatics had the highest R² (0.942), whereas phenols had the lowest (0.762). Furans had the smallest absolute errors because their range and abundance in the normalized target space were lower. Reporting all three metrics is important because R² is scale dependent and may appear low for a target with limited variance even when its absolute error is small.

**Table 4. Component-level standard MLP performance on the test set.**

| Bio-oil class | R² | RMSE (wt.%) | MAE (wt.%) |
|---|---:|---:|---:|
| Aromatics | 0.942 | 8.70 | 6.35 |
| Acids | 0.877 | 6.46 | 4.80 |
| Alcohols | 0.853 | 4.82 | 3.41 |
| Furans | 0.897 | 1.50 | 1.05 |
| Phenols | 0.762 | 8.42 | 5.28 |
| Aldehydes/ketones | 0.849 | 5.30 | 3.29 |
| Arithmetic mean | **0.863** | **5.87** | **4.03** |

The similar mean R² values on validation and test partitions (both 0.863) indicate stable performance across these two row-wise subsets. This observation should not be interpreted as proof of generalization to bio-oil compositions outside the dataset, because operating-condition rows derived from the same underlying compositions can occur in different partitions.

### 3.3. Composition closure

The standard MLP uses independent linear outputs and therefore does not enforce exact summation to 100%. Its predicted total was 99.85 ± 7.4 wt.% in the reported evaluation. The constrained MLP enforced 100.00 ± 0.00 wt.% closure but reduced mean test R² from 0.863 to 0.745 and increased MAE from 4.03 to 11.54 wt.%. For the present dataset, a hard output constraint introduced a larger predictive penalty than the closure benefit justified.

A practical deployment can handle this trade-off in three ways: retain the unconstrained model and report the total as a diagnostic; apply post-prediction normalization only after checking its effect on class errors; or train a compositional model with an objective designed specifically for simplex-valued outputs. The first option preserves the reported test performance and is therefore the reference implementation in this study.

### 3.4. Ensemble behavior

None of the ensemble strategies outperformed the standard MLP. The weighted average was the strongest ensemble with mean R² = 0.797, followed by simple averaging at 0.746. Stacking reached only 0.562. Combining models is beneficial when component learners have comparable skill and sufficiently diverse errors. Here, the two tree models were substantially weaker than the MLP, so averaging diluted the strongest predictions. The ensemble results are retained because they establish that additional model complexity did not automatically improve this inverse problem.

### 3.5. Feature interpretation

Random-forest feature importance was used as a model-specific interpretation of the inputs. Methane mole fraction had the largest importance (27.1%), followed by CO2 (26.0%), H2O (20.5%), H2 (11.9%), CO (9.9%), temperature (3.1%), pressure (1.0%), and steam-to-carbon ratio (0.6%). These values indicate that outlet gas composition carries most of the inverse signal once the operating state is supplied to the model.

The ranking is consistent with elemental-balance reasoning. Changes in the carbon, hydrogen, and oxygen content of the surrogate feed alter the equilibrium distribution among CH4, CO, CO2, H2, and H2O. Feature importance does not demonstrate causality, however, and correlated gas variables can share or redistribute importance. The result should therefore be treated as a consistency check rather than a mechanistic proof.

> **[INSERT FIGURE 5 HERE]**
>
> **Figure 5.** Random-forest feature importance for syngas measurements and reformer operating conditions.

## 4. Process-monitoring interpretation

The inverse MLP is intended as a soft-sensing layer between reformer measurements and a future supervisory or predictive controller. At each update, measured temperature, pressure, steam-to-carbon ratio, and outlet gas composition form the model input. The predicted six-class feed representation can then be passed to a forward reformer surrogate or used to flag deviations from a reference feed. A controller could subsequently optimize operating conditions for hydrogen yield, H2/CO ratio, or another process objective.

This architecture separates estimation from control. The present study evaluates only the inverse estimator; it does not claim closed-loop MPC performance. Before control integration, the soft sensor requires experimental calibration, an applicability-domain check, uncertainty estimation, and a strategy for handling measurements that fall outside the training range. The model output should be interpreted as a rapid class-level estimate supporting process decisions, not as a replacement for comprehensive analytical characterization.

> **[INSERT FIGURE 6 HERE]**
>
> **Figure 6.** Proposed use of the inverse soft sensor in a future monitoring and MPC workflow.

## 5. Limitations and future work

The dataset is generated from thermodynamic equilibrium simulations. It does not represent finite-rate kinetics, catalyst deactivation, carbon deposition, reactor hydrodynamics, heat- and mass-transfer limitations, sensor noise, or downstream separation dynamics. The surrogate approach also compresses a chemically complex liquid into six representative compounds. Consequently, the numerical accuracy reported here applies to the simulated surrogate domain.

The row-wise split is another important limitation. Multiple rows originate from the same bio-oil composition under different operating conditions, so the test set primarily evaluates interpolation over represented feed identities and process states. A composition-grouped external validation is required before claiming performance for unseen bio-oils. The current mean R² of 0.863 must therefore be cited together with the row-wise split protocol.

Future work should include experimental reformer measurements, grouped validation by bio-oil identity and biomass source, uncertainty quantification, robustness tests with realistic sensor error, and comparison with compositional-learning approaches. The validated inverse estimator can then be coupled to a forward surrogate and assessed in closed-loop MPC simulations.

## 6. Conclusions

A Cantera-assisted inverse soft sensor was developed to estimate six bio-oil composition classes from steam-reforming syngas and operating conditions. Literature-derived compositions were represented by six surrogate compounds, producing 3,150 equilibrium cases and 1,350 complete model-ready samples. Under the row-wise split, the standard 128-64-32 MLP outperformed linear regression, random forest, XGBoost, a composition-constrained MLP, and three ensemble strategies. Its test performance was mean R² = 0.863, RMSE = 5.87 wt.%, and MAE = 4.03 wt.%. Aromatics produced the highest component R² (0.942), and phenols the lowest (0.762). Exact output closure and ensemble averaging both reduced accuracy relative to the standard MLP. The study demonstrates a process-monitoring proof of concept within a simulation-defined domain; experimental and composition-grouped validation remain necessary before deployment.

## Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## Funding

**[AUTHOR CONFIRMATION REQUIRED: retain only the applicable statement.]**

This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

## CRediT authorship contribution statement

Orhun Uzdiyem: Conceptualization, Data curation, Methodology, Software, Formal analysis, Investigation, Validation, Visualization, Writing - original draft.

**[CO-AUTHOR CONTRIBUTIONS TO BE COMPLETED AFTER THE FINAL AUTHOR LIST IS CONFIRMED.]**

## Data availability

The cleaned data tables, data dictionary, simulation scripts, model-training scripts, and model-performance files will be deposited in a public repository before submission. The repository DOI and permanent URL will be inserted in the accepted data statement.

## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work, the authors used OpenAI Codex to organize source material and assist with language and manuscript structure. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article.

## References

Bordoloi, N., Narzari, R., Sut, D., Saikia, R., Chutia, R.S., Kataki, R., 2016. Characterization of bio-oil and its sub-fractions from pyrolysis of *Scenedesmus dimorphus*. Renewable Energy 98, 245-253. https://doi.org/10.1016/j.renene.2016.03.081.

Bridgwater, A.V., 2012. Review of fast pyrolysis of biomass and product upgrading. Biomass and Bioenergy 38, 68-94.

Chen, D., Cen, K., Jing, X., Gao, J., Li, C., Ma, Z., 2017. An approach for upgrading biomass and pyrolysis product quality using a combination of aqueous phase bio-oil washing and torrefaction pretreatment. Bioresource Technology 233, 150-158. https://doi.org/10.1016/j.biortech.2017.02.120.

Goodwin, D.G., Moffat, H.K., Schoegl, I., Speth, R.L., Weber, B.W., 2025. Cantera: An object-oriented software toolkit for chemical kinetics, thermodynamics, and transport processes. Version 3.2.0. https://doi.org/10.5281/zenodo.17620923.

Leng, E., He, B., Chen, J., Liao, G., Ma, Y., Zhang, F., Liu, S., E, J., 2021. Prediction of three-phase product distribution and bio-oil heating value of biomass fast pyrolysis based on machine learning. Energy 236, 121401. https://doi.org/10.1016/j.energy.2021.121401.

Modak, S., Katiyar, P., Yadav, S., Jain, S., Gole, B., Talukdar, D., 2023. Generation and characterization of bio-oil obtained from the slow pyrolysis of cooked food waste at various temperatures. Waste Management 158, 23-36. https://doi.org/10.1016/j.wasman.2023.01.002.

Mullen, C.A., Boateng, A.A., Hicks, K.B., Goldberg, N.M., Moreau, R.A., 2010. Analysis and comparison of bio-oil produced by fast pyrolysis from three barley biomass/byproduct streams. Energy & Fuels 24, 699-706. https://doi.org/10.1021/ef900912s.

Oasmaa, A., Peacocke, C., 2010. A guide to physical property characterisation of biomass-derived fast pyrolysis liquids. VTT Publications.

Pafili, A., Charisiou, N.D., Douvartzides, S.L., Siakavelas, G.I., Wang, W., Liu, G., Papadakis, V.G., Goula, M.A., 2021. Recent progress in the steam reforming of bio-oil for hydrogen production: A review of operating parameters, catalytic systems and technological innovations. Catalysts 11, 1526. https://doi.org/10.3390/catal11121526.

Sharifzadeh, M., Sadeqzadeh, M., 2019. The multi-scale challenges of biomass fast pyrolysis and bio-oil upgrading: Review of the state of art and future research directions. Progress in Energy and Combustion Science 71, 1-80.

Singh, P.P., Jaswal, A., Singh, R., Mondal, T., Pant, K.K., 2024. Green hydrogen production from biomass: A thermodynamic assessment of the potential of conventional and advanced bio-oil steam reforming processes. International Journal of Hydrogen Energy 50, 627-639. https://doi.org/10.1016/j.ijhydene.2023.10.099.

Smith, W.R., Missen, R.W., 1982. Chemical Reaction Equilibrium Analysis: Theory and Algorithms. Research Studies Press.

Vagia, E.C., Lemonidou, A.A., 2007. Thermodynamic analysis of hydrogen production by steam reforming of bio-oil components. International Journal of Hydrogen Energy 32, 212-223.

Zhang, S., Chen, T., Xiong, Y., Dong, Q., 2022. A comprehensive review of bio-oil, bio-binder and bio-asphalt materials: Their source, composition, preparation and performance. Journal of Traffic and Transportation Engineering (English Edition) 9, 151-166.
