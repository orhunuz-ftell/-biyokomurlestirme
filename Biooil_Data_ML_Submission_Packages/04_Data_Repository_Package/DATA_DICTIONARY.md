# Data Dictionary

## Bio-oil composition targets

`aromatics`

Class-level aromatic compounds in bio-oil, reported or mapped from the source paper. Used as a target variable in wt% after cleaning/normalization.

`acids`

Class-level organic acids in bio-oil, reported or mapped from the source paper. Used as a target variable in wt% after cleaning/normalization.

`alcohols`

Class-level alcohol compounds in bio-oil, reported or mapped from the source paper. Used as a target variable in wt% after cleaning/normalization.

`furans`

Class-level furan compounds in bio-oil, reported or mapped from the source paper. Used as a target variable in wt% after cleaning/normalization.

`phenols`

Class-level phenolic compounds in bio-oil, reported or mapped from the source paper. Used as a target variable in wt% after cleaning/normalization.

`aldehydes_ketones`

Combined aldehyde and ketone class in bio-oil, reported or mapped from the source paper. Used as a target variable in wt% after cleaning/normalization.

## Reformer process inputs

`Reformer_Temperature_C`

Steam reformer temperature in degC. Grid values: 650, 700, 750, 800, 850.

`Reformer_Pressure_bar`

Steam reformer pressure in bar. Grid values: 5, 15, 30.

`Steam_to_Carbon_Ratio`

Molar steam-to-carbon ratio. Grid values: 2.0, 4.0, 6.0.

## Syngas inputs

`H2_molpercent`

Hydrogen mole percentage in reformer outlet gas.

`CO_molpercent`

Carbon monoxide mole percentage in reformer outlet gas.

`CO2_molpercent`

Carbon dioxide mole percentage in reformer outlet gas.

`CH4_molpercent`

Methane mole percentage in reformer outlet gas.

`H2O_molpercent`

Water vapor mole percentage in reformer outlet stream.

## Identifiers

`BiooilID`

Bio-oil record identifier used for group-aware validation. Row-wise splits evaluate interpolation across process conditions; BiooilID holdout evaluates generalization to unseen bio-oil identities.

`ReferenceID`

Reference identifier from the SQL database. Before public deposition, each reference should be tagged as primary experimental, review/secondary, or other.

## Missing value interpretation

Missing bio-oil class values mean that the class was not available in a usable numeric form after source extraction. Missing does not necessarily mean the compound class was absent in the bio-oil.

