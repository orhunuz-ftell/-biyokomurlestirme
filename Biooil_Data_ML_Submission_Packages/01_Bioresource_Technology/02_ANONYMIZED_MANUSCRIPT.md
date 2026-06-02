# Data availability constraints and deep learning-based inverse prediction of bio-oil composition from steam reforming syngas

## Abstract

Background: Bio-oil composition is central to biomass pyrolysis valorization, yet detailed characterization is slow, costly, and inconsistently reported. This limits both process control and machine-learning reuse. Methods: A SQL-curated literature dataset was audited to quantify reporting gaps in bio-oil composition data. The usable class-level data were then mapped to six representative bio-oil groups and used in a Cantera-based steam reforming workflow. A total of 3,150 thermodynamic reforming cases were generated across 70 bio-oil records and process conditions; after target-completeness filtering, 1,350 samples from 30 unique bio-oil compositions were used for inverse modeling. Results: The SQL audit showed that no record contained all ten composition classes, while only 30 of 70 records contained the six target groups required for modeling. A multilayer perceptron using reformer conditions and syngas composition predicted six bio-oil classes with average row-wise test R2 = 0.863 and MAE = 4.03%, outperforming linear regression, random forest, XGBoost, and ensemble models. A BiooilID holdout audit showed stronger generalization for aromatics and acids than for alcohols, revealing limits when extrapolating to unseen bio-oils. Conclusions: Syngas-based inverse prediction can operate as a soft sensor within the represented composition domain, but reusable bio-oil composition models require better data stewardship, source-level metadata, and group-aware validation.

## Keywords

Bio-oil; biomass pyrolysis; steam reforming; syngas; machine learning; soft sensor; data stewardship

## 1. Introduction

Bio-oil from biomass pyrolysis is a complex intermediate for renewable fuels, hydrogen, chemicals, and carbon-containing materials (Sharifzadeh and Sadeqzadeh, 2019; Zhang et al., 2022). Its use is constrained by large compositional variability across feedstocks and pyrolysis conditions. In practice, the downstream processing strategy depends strongly on the relative abundance of aromatics, acids, alcohols, furans, phenols, and carbonyl compounds. These groups influence reforming behavior, hydrogen generation potential, upgrading severity, corrosion risk, and process stability (Pafili et al., 2021; Singh and Jaswal, 2024).

Detailed bio-oil characterization is slower and more expensive than online gas analysis. Gas composition from a reformer can be monitored much more rapidly than the complete chemical characterization of a liquid bio-oil sample. This creates an attractive inverse problem: if a steam reformer converts a bio-oil into syngas, can the measured syngas composition and operating conditions be used to infer the original bio-oil composition?

This question is scientifically useful but difficult. The forward process from bio-oil composition and operating conditions to equilibrium syngas is governed by thermodynamics. The inverse problem is not unique: different bio-oils may produce similar syngas compositions under comparable reformer conditions. Therefore, any machine-learning model must be interpreted as a domain-limited soft sensor rather than a universal analytical replacement.

The data problem is equally important. A local SQL audit of bio-oil literature records showed that the main limitation is not simply the absence of reported composition values. The stronger limitation is the lack of reusable, standardized, machine-readable, and comparable composition data. This study combines a data-availability audit with a thermodynamically validated inverse modeling workflow. The objectives are to quantify the data limitations, generate a consistent reforming dataset, compare inverse prediction models, and define the practical boundaries of syngas-based bio-oil soft sensing.

## 2. Evidence base and data curation

The starting evidence base was a SQL Server database containing literature-derived biomass, pyrolysis, bio-oil, and reforming tables. The `Biooil` table contained 70 class-level bio-oil composition records linked to experiment, biomass, and reference metadata. These records were connected to 14 distinct references and 43 biomass names, with pyrolysis process temperatures ranging from 300 to 850 degC.

The audit showed severe incompleteness. None of the 70 `Biooil` records contained all ten main composition classes. Only 30 records contained the six target groups used in the reverse model: aromatics, acids, alcohols, furans, phenols, and aldehydes/ketones. Individual marker fields were sparse: guaiacol, syringol, and catechol were each present in only 5 of 70 records, and N-containing compounds were present in 7 of 70 records. When missing values were treated as zero for a simple coverage check, class-sum totals ranged from 11.07 to 103.49, with an average of 87.82. This spread indicates partial reporting, inconsistent normalization, and source-dependent extraction rules.

The database therefore supports a reporting-quality and data-stewardship argument, not a claim of a complete compound-level repository. The usable modeling layer was restricted to the six class groups with enough coverage for simulation and learning. This filtering step reduced the model-ready bio-oil set to 30 unique compositions.

## 3. Thermodynamic simulation workflow

Steam reforming simulations were performed with Cantera using a reformer-only equilibrium model (Goodwin et al., 2017). The reformer was selected as the core unit because bio-oil composition has its strongest direct effect at this stage, whereas downstream water-gas shift, separation, and purification units introduce additional assumptions that can obscure the inverse relationship.

Six representative surrogate species were used to encode the functional composition of bio-oil: toluene for aromatics, acetic acid for acids, ethanol for alcohols, furan for furans, phenol for phenols, and acetone for aldehydes/ketones. These surrogate groups were used to translate class-level composition data into a thermodynamic input mixture, consistent with the use of representative bio-oil model compounds in reforming analysis (Vagia and Lemonidou, 2007).

The process-condition grid used five reformer temperatures (650, 700, 750, 800, and 850 degC), three pressures (5, 15, and 30 bar), and three steam-to-carbon ratios (2.0, 4.0, and 6.0). This produced 45 process-condition combinations. Across the broader SQL-linked bio-oil records, 3,150 reforming cases were generated. After removing rows with incomplete target values, 1,350 samples remained for inverse machine learning.

The primary model inputs were reformer temperature, pressure, steam-to-carbon ratio, and syngas mole percentages of H2, CO, CO2, CH4, and H2O. The target outputs were the six bio-oil class percentages. The resulting task was a multi-output regression problem from eight input variables to six composition variables.

## 4. Machine-learning models

A sequence of linear, tree-based, ensemble, and neural models was compared. Linear regression provided a lower-bound baseline. Random forest and XGBoost represented nonlinear tree-based approaches. Two neural architectures were tested: a standard multilayer perceptron and a constrained-output multilayer perceptron. Ensemble variants included simple averaging, weighted averaging, and stacking.

The best model was the standard multilayer perceptron with hidden layers of 128, 64, and 32 neurons. Batch normalization and dropout regularization were used to stabilize learning under limited composition diversity. The model was trained on the cleaned 1,350-sample dataset using train, validation, and test splits.

## 5. Results and discussion

The row-wise test comparison showed that the inverse mapping contains a strong nonlinear signal. Linear regression achieved average R2 = 0.332 and MAE = 9.92%. Random forest improved performance to R2 = 0.571 and MAE = 6.25%, while XGBoost achieved R2 = 0.603 and MAE = 6.10%. The standard multilayer perceptron achieved the strongest row-wise performance with average R2 = 0.863 and MAE = 4.03%.

Component-level performance was highest for aromatics (R2 = 0.942), furans (R2 = 0.897), acids (R2 = 0.877), alcohols (R2 = 0.853), aldehydes/ketones (R2 = 0.849), and phenols (R2 = 0.762). These results indicate that the syngas composition retains information about the original class-level bio-oil composition within the represented dataset.

The ensemble models did not improve performance. The weighted ensemble reached R2 = 0.797, below the standard multilayer perceptron. This suggests that adding weaker and correlated learners can dilute a strong neural model in this specific inverse thermodynamic setting.

The interpretation changes under a stricter generalization audit. A BiooilID-based holdout split separated entire bio-oil identities between training and testing. In this audit, 24 BiooilIDs were used for training and 6 were held out for testing. Aromatics and acids remained predictable, with R2 values of 0.951 and 0.803, respectively. Phenols and aldehydes/ketones showed moderate behavior, while furans were weaker and alcohols produced a negative R2 value. The mean absolute error remained moderate at 4.62%, but the average R2 was dominated by the alcohol failure.

This finding is central to the manuscript. The row-wise model is a strong interpolation soft sensor for known or compositionally similar bio-oils. It should not be claimed as a universally validated model for unseen bio-oil chemistry. The group-holdout behavior supports the data-availability argument: broader, standardized, and source-diverse bio-oil composition data are needed before such models can generalize reliably.

## 6. Implications for bioresource technology

The combined data audit and inverse model suggest a practical route for bio-oil process monitoring. In a reforming process, syngas composition is faster to monitor than full liquid bio-oil characterization. A trained inverse model can therefore support feedstock quality tracking, abnormal-composition detection, and decision support for operating-condition adjustment. However, the model must be deployed with uncertainty awareness and within the data domain represented by the curated compositions.

For future datasets, the minimum reporting package should include feedstock metadata, pyrolysis conditions, quantified bio-oil class composition, explicit normalization basis, analytical method, raw or processed chromatographic data where possible, and a data availability statement. These reporting elements would directly improve the reliability of ML-based soft sensors and process optimization models.

## 7. Limitations

The SQL-derived composition data are class-level and literature-derived. They are not raw GC-MS data and do not constitute a complete compound-level database. Several records are partially reported, and some source entries originate from secondary review material that should be separated in final primary-source analyses. The Cantera reforming model is thermodynamic and reformer-only; it does not model catalyst deactivation, kinetic limitations, reactor hydrodynamics, or downstream separation units. The strongest ML performance is row-wise and reflects interpolation across process conditions. Generalization to entirely unseen bio-oil identities is more limited and should be improved with group-aware retraining, uncertainty quantification, and additional experimental validation.

## 8. Conclusions

This study shows that bio-oil composition reporting limitations and inverse soft-sensor development are linked problems. A SQL audit of literature-derived records found that reusable bio-oil composition data remain incomplete and inconsistently normalized. Only 30 of 70 class-level records were complete enough for six-target inverse modeling. Cantera-based steam reforming simulations generated a thermodynamically consistent dataset, and a multilayer perceptron predicted six bio-oil classes from syngas and operating conditions with row-wise average R2 = 0.863 and MAE = 4.03%. However, BiooilID-based holdout analysis showed that unseen-composition generalization is uneven across compound classes. The most defensible application is therefore a domain-limited soft sensor for compositionally represented bio-oils. Wider use will require better composition data stewardship, raw-data sharing, consistent normalization, and validation on new experimental reforming cases.

## Data availability

The cleaned data tables, data dictionary, simulation scripts, model-training scripts, and model-performance files will be deposited in a public repository before submission. Until a DOI is assigned, the local source files are available in the project repository under `reverse_ml_biooil_to_product/` and `COMPOSITION_DATA_REVIEW_Paper/`.

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
