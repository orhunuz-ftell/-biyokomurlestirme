# TIK-5 Report Results Review

Source report: `tik5/OrhunUzdiyem_tik5.docx`  
Review focus: Results, model validity, optimization interpretation, and MPC claims  
Reviewer perspective: Chemical engineering professor  
Date: 2026-06-03

## Overall Verdict

The reported results are generally plausible as a simulation-based machine-learning and optimization proof-of-concept. There is no obvious result that is physically impossible or completely nonsensical. However, several parts of the results section are not acceptable if presented as final thesis-level scientific evidence without revision.

The report should be framed as a computational workflow that connects an inverse soft-sensor, a Cantera-trained forward surrogate, static optimization, and a closed-loop optimization scenario. It should not overclaim industrial process validity, real energy optimization, or fully developed MPC control.

## Not Acceptable Issues

### 1. The MPC Claim Is Too Strong

The reported control trajectory jumps immediately from:

```text
750 degC, 15 bar, S/C = 4
```

to:

```text
850 degC, 5 bar, S/C = 2
```

and then remains at those values. This behavior looks like repeated static optimization with feedback rather than a rigorous model predictive control implementation.

A true MPC result should define and justify:

- prediction horizon
- control horizon
- dynamic process model or state-update model
- actuator/ramp constraints
- move suppression weights
- delay and settling behavior
- measured versus predicted trajectory over time

As written, calling this a real MPC result is not acceptable. It should be renamed as a simple closed-loop optimization scenario, MPC-like computational demonstration, or receding static optimization unless dynamic MPC details are added.

Required fix:

- Either add a real dynamic MPC formulation, or revise the wording throughout the report to avoid implying that a fully validated MPC controller was developed.

Suggested wording:

```text
Bu calismada gelistirilen yapi, deneysel olarak dogrulanmis tam bir MPC sistemi degil,
soft-sensor ve ileri surrogate modelin kapali cevrim karar verme yapisinda nasil
kullanilabilecegini gosteren hesaplamali bir senaryodur.
```

### 2. Energy and Operating Cost Claims Are Not Justified

The optimizer repeatedly selects the maximum allowed temperature, `850 degC`. From a chemical engineering perspective, this is not automatically energy-efficient. High temperature increases heat duty and furnace/reformer energy demand.

The report mentions lower energy or operating cost, but the objective function appears to use only a normalized penalty term. There is no rigorous calculation of:

- heat duty
- steam generation duty
- compression duty
- decompression or downstream pressure cost
- reactor/furnace duty
- economic objective function

Therefore, claiming that the optimized condition is "energy-wise more suitable" or "lower cost" is not acceptable unless the cost term is clearly described as a simplified proxy.

Required fix:

- Replace strong energy/cost language with wording that describes a simplified normalized operating penalty.
- If true energy/cost optimization is desired, calculate heat duty, steam duty, and pressure-related utility costs.

Suggested wording:

```text
Optimizasyonda kullanilan maliyet terimi, gercek bir enerji veya ekonomik analiz
degil, sicaklik, basinc ve buhar/karbon oranina dayali basitlestirilmis normalize
bir isletme cezasi olarak degerlendirilmelidir.
```

### 3. BiooilID Validation Does Not Directly Validate the Deployed Soft-Sensor

The report states that the deployed inverse soft-sensor is the previous standard MLP model. However, the BiooilID-based generalization validation is performed with an ExtraTrees multi-output regressor.

This is a serious methodological ambiguity. ExtraTrees validation may be useful as a supplementary diagnostic, but it does not directly validate the MLP model used in the soft-sensor, optimization, and MPC workflow.

Required fix:

- Repeat BiooilID holdout validation using the actual deployed MLP model; or
- Explicitly state that the ExtraTrees result is only a supplementary generalization check and not validation of the deployed MLP soft-sensor.

Suggested wording:

```text
BiooilID bazli ayrimda verilen ExtraTrees sonucu, ters tahmin probleminin
genelleme zorlugunu gosteren ek bir denetimdir. Nihai soft-sensor olarak
kullanilan MLP modelinin BiooilID bazli performansi ayrica raporlanmalidir.
```

### 4. The Inverse Soft-Sensor Identifiability Problem Is Underdiscussed

The report assumes that bio-oil composition can be inferred from syngas composition and operating conditions:

```text
T, P, S/C, H2, CO, CO2, CH4, H2O -> bio-oil composition groups
```

Chemically, this inverse problem may be non-unique. Different bio-oil compositions can produce similar reformer outlet syngas compositions, especially if the reactor is close to equilibrium. This means the inverse mapping may not be uniquely identifiable.

The report discusses uncertainty for some components, especially alcohols and aldehyde-ketones, which is useful. However, it should explicitly discuss non-uniqueness and identifiability.

Required fix:

- Add a paragraph explaining that the inverse model is empirical/data-driven and valid only within the represented data domain.
- State that similar syngas outputs may correspond to more than one bio-oil composition.
- Add uncertainty analysis or nearest-neighbor/domain-of-applicability checks if possible.

Suggested wording:

```text
Ters tahmin problemi fiziksel olarak tekil bir cozum garanti etmemektedir.
Benzer reformer cikis gazlari farkli biyoyag bilesimlerinden elde edilebilir.
Bu nedenle soft-sensor tahminleri, egitim veri uzayinda temsil edilen kompozisyon
araliklari icin gecerlidir ve ozellikle yeni biyoyag tiplerinde belirsizlikle
birlikte yorumlanmalidir.
```

### 5. Surrogate Model Accuracy Is Overinterpreted

The forward surrogate model reaches approximately `R2 = 0.996`. This is plausible for deterministic, smooth Cantera-generated simulation data. However, this proves mainly that the machine-learning model interpolates the Cantera simulation space well.

It does not prove that the surrogate accurately predicts a real bio-oil reformer.

Required fix:

- State clearly that surrogate accuracy is with respect to Cantera-generated simulation data.
- Avoid implying experimental validation unless experimental data were used.
- Add stronger validation if possible: held-out BiooilIDs, held-out operating regions, boundary cases, and parity/residual plots.

Suggested wording:

```text
Ileri surrogate model, Cantera tabanli simulasyon veri uzayini yuksek dogrulukla
yeniden uretebilmistir. Bu sonuc, modelin simulasyon verisine gore basarili bir
interpolasyon araci oldugunu gostermektedir; deneysel reaktor davranisinin
dogrudan dogrulanmasi olarak yorumlanmamalidir.
```

### 6. H2/CO Alone Is Insufficient as an Optimization Result

The optimization and MPC results focus mainly on H2/CO. H2/CO is important, but it is not enough to establish that the process condition is chemically or industrially preferable.

For bio-oil steam reforming, the results section should also report several of the following:

- H2 yield
- CO yield
- CO2 selectivity
- CH4 slip
- total dry gas composition
- wet gas composition, if water is included
- carbon conversion
- steam conversion
- coke/carbon formation risk, if modeled
- mole-fraction closure
- elemental balance closure

A condition can improve H2/CO while still being undesirable because of low total hydrogen production, high CO2 formation, methane slip, excessive steam, or unrealistic material balances.

Required fix:

- Add a table for each optimized case with full gas composition and at least one yield or conversion metric.
- Interpret H2/CO together with total hydrogen production and carbon-containing products.

### 7. Wet/Dry Gas Basis Is Not Clear

The model outputs include `H2O`, and the inverse model inputs include syngas components including water. The report should explicitly state whether gas compositions are reported on a wet basis or dry basis.

This is important because syngas composition and model interpretation change significantly depending on whether water is included in the normalized composition.

Required fix:

- Add a clear statement defining the basis for all gas compositions.
- If both wet and dry values are used, separate them clearly.

Suggested wording:

```text
Bu raporda gaz bilesimleri [yas/kuru] bazda raporlanmistir. H2O'nun modele dahil
edildigi durumlarda mol yuzdeleri yas baz kompozisyonu temsil etmektedir; H2/CO
orani ise ayni bazda raporlanan H2 ve CO degerlerinden hesaplanmistir.
```

### 8. The Optimized Solution Sits on Variable Bounds

The optimizer repeatedly selects:

```text
T = 850 degC
P = 5 bar
S/C = 2
```

This is not automatically wrong. It is chemically plausible that lower S/C and low pressure reduce H2/CO and that high temperature favors reforming and CO formation. However, it means the optimum is boundary-driven.

The report should explicitly discuss active constraints. Otherwise, the result may look like a balanced optimum even though the objective function is pushing to the limits of the allowed search space.

Required fix:

- State that the optimum is located at the imposed control-variable boundaries.
- Discuss whether the search range should be expanded, the target should be changed, or objective weights should be adjusted.

Suggested wording:

```text
Optimum noktalarin siklikla sicaklik ust sinirinda, basinc ve S/C alt sinirinda
bulunmasi, tanimlanan amac fonksiyonunun mevcut kontrol araliginda sinir
noktalarina yoneldigini gostermektedir. Bu nedenle sonuc, serbest ve dengelenmis
bir optimumdan cok, mevcut sinirlar altindaki en iyi erisilebilir calisma noktasi
olarak yorumlanmalidir.
```

## Plausible Results

The following findings are chemically reasonable and can remain, provided the wording is careful:

- Initial H2/CO values around `5.8-6.1` are plausible for steam-rich reforming at `S/C = 4`.
- Reducing H2/CO to approximately `2.5-2.8` by moving toward lower S/C and low pressure is plausible.
- Failure to reach `H2/CO = 2.0` within the selected bounds is plausible and should be interpreted as an accessibility/constraint limitation.
- Lower BiooilID generalization performance for alcohols is plausible because alcohol content may have weak or non-unique signatures in syngas output.
- A very high surrogate-model R2 is plausible for smooth Cantera simulation data, but it should be interpreted only as simulator-surrogate agreement.

## Recommended Revised Framing

The most defensible claim is:

```text
The developed ML workflow can reproduce the Cantera-generated simulation space
and can guide H2/CO-oriented operating-condition selection within the studied
data range.
```

The report should avoid claiming:

```text
The method determines fully validated real reactor optimum conditions and provides
an experimentally ready MPC controller.
```

## Minimum Required Revisions Before Thesis Use

1. Rename the current MPC result or add real dynamic MPC details.
2. Rephrase all energy/cost claims as simplified proxy-objective claims unless real utility calculations are added.
3. Validate the actual MLP soft-sensor using BiooilID holdout, or clearly separate ExtraTrees as supplementary.
4. Add an identifiability/non-uniqueness limitation for inverse prediction.
5. State that surrogate accuracy is against Cantera simulation data, not experimental reality.
6. Add full optimized gas composition and at least H2 yield or conversion metrics.
7. Define wet/dry gas basis.
8. Discuss boundary optima and active constraints.

## Final Assessment

For a TIK progress report, the results are acceptable if the claims are softened and the limitations are clearly stated. For final thesis defense, the current results section needs revision. The strongest scientific contribution is the computational integration of inverse prediction, surrogate modeling, and H2/CO-targeted operating-condition selection. The weakest parts are the overuse of the term MPC, unsupported energy-cost language, and insufficient discussion of inverse-model identifiability.
