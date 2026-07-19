# Makale Yapısı ve Aktarım Planı

## Önerilen makale odağı

Mevcut taslak, C&CE için "bio-oil steam reforming prosesinde singazdan biyoyağ kompozisyonu tahmin eden ters ML soft-sensor" olarak konumlandırılmalı. Genel bio-oil uygulamaları yardımcı arka plan olarak kalmalı; ana katkı process monitoring, simulation-based data generation, inverse modeling ve model validation olmalı.

Önerilen başlık:

**A Cantera-assisted inverse deep learning soft sensor for estimating bio-oil composition from steam reforming syngas**

Alternatif daha kısa başlık:

**Inverse deep learning estimation of bio-oil composition from steam reforming syngas**

## C&CE uyumlu ana bölüm yapısı

1. Introduction
2. Materials and methods
3. Cantera-based steam reforming data generation
4. Inverse machine learning framework
5. Results and discussion
6. Generalization audit and limitations
7. Conclusions
8. Declaration of generative AI and AI-assisted technologies in the manuscript preparation process
9. CRediT author statement
10. Declaration of competing interest
11. Data availability
12. Acknowledgements
13. References

Not: Abstract numaralandırmaya dahil edilmemeli. C&CE kılavuzu alt bölümlerin `1.1`, `1.1.1` biçiminde numaralandırılmasını istiyor.

## Mevcut taslaktan aktarım haritası

| Mevcut bölüm/parça | Yapılacak işlem | Yeni makaledeki yer |
|---|---|---|
| Başlık | Daha C&CE/process-systems odaklı kısalt | Title page |
| Bio-oil kullanım alanları uzun girişi | 1-2 kısa paragraf olarak özetle | Introduction |
| Steam reforming proses zinciri | Gereksiz Aspen 2006 plan dili çıkarılarak netleştir | Methods / Process description |
| `2.0 Data preperation` | Yazım hatasını düzelt; veri kaynağı ve temizlik adımlarına ayır | Materials and methods |
| `2.1 litreature` | Literature-derived data curation olarak yeniden yaz | Materials and methods |
| `2.2 synthetic data` | Cantera data generation olarak yeniden yaz | Cantera-based data generation |
| `B.2.1 Data generation with Cantera` | Tez numaralandırması kaldır; matematik ve varsayımları düzenle | Cantera-based data generation |
| `B.2.2 Prediction of bio-oil content with AI` | ML framework olarak sistematikleştir | Inverse ML framework |
| Baseline model sonuçları | Tek tabloya indir | Results |
| MLP sonuçları | Ana sonuç tablosu olarak ver | Results |
| Ensemble karşılaştırması | Kısa metodolojik tartışma olarak ver | Results and discussion |
| Feature importance | Kimya mühendisliği yorumu ile bağla | Results and discussion |
| BiooilID holdout | Mevcut taslakta eksik; TİK5 ve proje metriklerinden ekle | Generalization audit and limitations |
| "End-of-Term Study Results" | Tamamen kaldır | Yok |

## Abstract taslak metni

Detailed characterization of pyrolysis bio-oil is usually performed offline, whereas syngas composition can be monitored more readily at the outlet of a steam reformer. This work develops a Cantera-assisted inverse machine-learning workflow to estimate six bio-oil composition classes from reformer outlet syngas and operating conditions. Literature-derived bio-oil compositions were mapped to surrogate compounds representing aromatics, acids, alcohols, furans, phenols, and aldehydes/ketones. Steam reforming simulations were generated over temperature, pressure, and steam-to-carbon ratio grids, producing 3,150 thermodynamic cases and 1,350 complete model-ready samples after filtering and normalization. Linear regression, random forest, XGBoost, standard multilayer perceptron, constrained multilayer perceptron, and ensemble strategies were compared. Under the row-wise split, the standard multilayer perceptron achieved the best test performance, with average R2 = 0.863 and MAE = 4.03%. Feature-importance analysis indicated that methane and carbon dioxide mole fractions carried the strongest inverse signal, consistent with carbon-hydrogen-oxygen balance effects. A stricter BiooilID-based holdout audit showed that transfer to unseen bio-oil compositions remains uneven for some classes, so the model should be interpreted as a simulation-domain soft sensor rather than a replacement for direct analytical characterization. The results demonstrate the potential of inverse learning for monitoring-oriented bio-oil reforming workflows and identify the validation steps required before experimental deployment.

Yaklaşık 220 kelime. Gönderim öncesi kesin metrik kaynağı seçildikten sonra sayılar yeniden kontrol edilmeli.

## Keyword önerileri

- Bio-oil
- Steam reforming
- Soft sensor
- Inverse modeling
- Cantera
- Deep learning
- Process monitoring

## Highlight taslakları

Her madde 85 karakter sınırının altında tutuldu.

- Cantera generated reforming data from literature-derived bio-oil classes.
- An inverse MLP inferred six bio-oil classes from syngas data.
- The best row-wise model reached R2 = 0.863 and MAE = 4.03%.
- BiooilID holdout exposed limits for unseen bio-oil compositions.
- The workflow supports soft sensing for reformer monitoring and MPC.

## Introduction için önerilen son paragraf

This study contributes a simulation-assisted inverse soft-sensing workflow for estimating bio-oil composition from reformer outlet syngas and operating conditions. The specific contributions are: (i) curation of literature-derived bio-oil compositions into six surrogate chemical classes, (ii) Cantera-based generation of a thermodynamically consistent reforming dataset, (iii) comparison of classical, deep-learning, constrained-output, and ensemble inverse models, and (iv) explicit discussion of row-wise interpolation performance versus BiooilID-based generalization limits.

## Conclusions için önerilen iskelet

1. The study generated a Cantera-based steam reforming dataset from literature-derived bio-oil compositions.
2. The standard MLP was the strongest inverse model under the row-wise split.
3. Ensemble methods did not outperform the standard MLP because weaker correlated learners diluted the prediction.
4. Methane and carbon dioxide mole fractions were the most informative inverse features.
5. BiooilID holdout results show that unseen-composition generalization remains the main limitation.
6. The proposed model is best presented as a monitoring-oriented soft sensor within a simulation-supported domain, not as a standalone analytical replacement.

