# Eksik Bilimsel Doğrulama ve Veri Kontrolü

Bu dosya, proje genelinde yapılan aramada bulunan eksik veya riskli noktaları özetler. Bunlar giderilmeden gönderim yapılırsa reviewer'ın en kuvvetli eleştirileri bu başlıklardan gelir.

## 1. Data leakage ve BiooilID genelleme riski

Mevcut güçlü sonuç `row-wise split` üzerinden geliyor:

- Train: 944 sample
- Validation: 203 sample
- Test: 203 sample
- Standard MLP test ortalaması: R2 = 0.863, RMSE = 5.87%, MAE = 4.03%

Risk: Aynı BiooilID'ye ait farklı sıcaklık/basınç/S-C koşulları hem train hem test tarafına düşmüş olabilir. Bu durumda modelin başarısı yeni biyoyağ kompozisyonlarına genellemeden çok, görülen biyoyağların farklı proses koşullarındaki interpolasyonunu gösterir.

Proje genelinde bulunan BiooilID holdout denetimi:

- Train BiooilID sayısı: 24
- Test BiooilID sayısı: 6
- Train sample: 1080
- Test sample: 270
- Ortalama R2: -0.506
- Ortalama RMSE: 6.14%
- Ortalama MAE: 4.62%

Bileşen bazlı BiooilID holdout:

| Bileşen | R2 | RMSE (%) | MAE (%) |
|---|---:|---:|---:|
| Aromatics | 0.951 | 7.43 | 5.84 |
| Acids | 0.803 | 6.42 | 5.23 |
| Alcohols | -6.577 | 4.01 | 2.58 |
| Furans | 0.464 | 2.79 | 2.07 |
| Phenols | 0.698 | 11.51 | 8.88 |
| Aldehydes/ketones | 0.624 | 4.71 | 3.14 |

Makaledeki doğru ifade: row-wise MLP sonucu ana model performansı olarak verilebilir; BiooilID holdout ise modelin yeni biyoyağlara transferinde sınırlılık olduğunu gösteren ek denetim olarak sunulmalı.

Makaledeki yanlış ifade: "perfect generalization" veya "new bio-oils are predicted accurately" denmemeli.

## 2. Metrik tutarsızlıkları

Farklı dosyalarda bazı metrikler farklı görünüyor. Nihai metin tek metrik kaynağından yazılmalı.

Bulunan ana kaynaklar:

- `reverse_ml_biooil_to_product\ml_reverse_prediction\FINAL_REPORT.md`
- `reverse_ml_biooil_to_product\ml_reverse_prediction\output\metrics\ensemble_comparison.json`
- `Biooil_Data_ML_Submission_Packages\04_Data_Repository_Package\metrics\deep_learning_metrics.json`
- `Biooil_Data_ML_Submission_Packages\04_Data_Repository_Package\metrics\baseline_metrics.json`

Özellikle kontrol edilecek tutarsızlık:

- `deep_learning_metrics.json` constrained MLP test bileşenlerinden ortalama R2 yaklaşık 0.745 çıkıyor.
- `ensemble_comparison.json` içinde `mlp_constrained.avg_r2 = 0.173` görünüyor.

Bu fark açıklanmadan constrained MLP sonucunu makaleye koymak riskli. Eğer farkın nedeni farklı metrik hesaplama yöntemi, ölçek dönüşümü veya composition closure sonrası yeniden hesaplama ise Methods içinde açık yazılmalı.

## 3. Cantera ve deneysel doğrulama sınırı

Makale şu şekilde konumlandırılmalı:

- Cantera tabanlı thermodynamic-equilibrium simulation-domain soft sensor.
- Deneysel reaktör verisiyle doğrulanmış doğrudan deployment modeli değil.
- Kinetik, katalizör deaktivasyonu, coke formation, tar, heat/mass transfer ve non-equilibrium etkileri kapsam dışında.

Gerekli ek cümle:

> The model is therefore intended as a simulation-domain soft sensor and screening tool; experimental reactor validation is required before deployment.

## 4. Veri sayıları netleştirilmeli

Proje genelinde bulunan sayı zinciri:

- SQL `dbo.ReformerSimulation`: 3,150
- SQL `dbo.ReformerOutput`: 3,150
- SQL `dbo.ReformerPerformance`: 3,150
- Ham reformer-only simulation: 3,150 case
- Model-ready clean sample: 1,350
- Unique bio-oil composition: 30
- Process grid: 5 temperature x 3 pressure x 3 S/C = 45 condition per composition
- 30 x 45 = 1,350 clean model-ready combinations

Makaledeki önerilen ifade:

> The full simulation campaign produced 3,150 reforming cases. After filtering for complete six-class bio-oil compositions and normalizing the target composition vectors, 1,350 samples corresponding to 30 bio-oil compositions and 45 operating conditions per composition were retained for inverse model training.

## 5. Surrogate molekül ve sınıf indirgeme riski

Bio-oil kompozisyonu altı sınıfa indirgenmiş:

- Aromatics
- Acids
- Alcohols
- Furans
- Phenols
- Aldehydes/ketones

Seçilen surrogate moleküller:

| Sınıf | Surrogate | Risk |
|---|---|---|
| Aromatics | Toluene | Aromatik oxygenate çeşitliliğini tam temsil etmez |
| Acids | Acetic acid | Asit sınıfı için makul ama yüksek asit çeşitliliğini basitleştirir |
| Alcohols | Ethanol | Ağır alkolleri temsil gücü sınırlı |
| Furans | Furan | Methyl-furan vb. türleri indirger |
| Phenols | Phenol | Guaiacol/syringol gibi methoxy phenolics ayrı değil |
| Aldehydes/ketones | Acetone | Aldehit ve ketonları tek temsilciye indirger |

Bu sınırlama Discussion veya Limitations bölümünde açık yazılmalı.

## 6. "First in the literature" iddiası

Mevcut taslakta "first machine learning-based inverse model in the literature" iddiası var. Bu iddia ancak sistematik literatür tablosuyla savunulursa kullanılmalı.

Daha güvenli ifade:

> To the best of our knowledge, no prior study has explicitly formulated bio-oil steam reforming soft sensing as an inverse prediction problem from outlet syngas to six-class bio-oil composition.

Bu iddianın yanında küçük bir literatür karşılaştırma tablosu önerilir:

| Çalışma grubu | Tipik hedef | Bu çalışmadan farkı |
|---|---|---|
| Bio-oil pyrolysis ML | Bio-oil yield/HHV/product distribution prediction | Reformer outlet syngasından bio-oil composition tahmini yok |
| Bio-oil steam reforming simulation | H2/syngas production prediction | Inverse ML soft-sensor yok |
| Process monitoring/soft sensor | Genellikle conventional chemical processes | Bio-oil steam reforming composition inversion yok |

## 7. Makaleye eklenmesi gereken sınırlılıklar

- Veri seti sentetik/simülasyon ağırlıklı.
- Gerçek bio-oil kompozisyonları sınıf bazlı ve literatürden derlenmiş.
- Altı sınıflı temsil ayrıntılı GC-MS bileşik dağılımını vermez.
- Row-wise split sonucu yeni biyoyağ genellemesi olarak yorumlanmamalı.
- BiooilID holdout bazı bileşenlerde genellemenin zor olduğunu gösteriyor.
- Cantera equilibrium yaklaşımı kinetik ve katalizör etkilerini doğrudan çözmüyor.
- MLP çıktılarında composition closure garantisi yoksa normalize etme stratejisi açıklanmalı.
- Feature importance Random Forest'a aitse MLP için doğrudan model açıklaması olarak sunulmamalı.

## 8. Projede bulunan kullanılabilir destek dosyaları

- Temiz veri: `C:\@biyokomurlestirme\Biooil_Data_ML_Submission_Packages\04_Data_Repository_Package\data\reformer_data_clean.csv`
- 30 kompozisyon: `C:\@biyokomurlestirme\Biooil_Data_ML_Submission_Packages\04_Data_Repository_Package\data\biooil_compositions_30.csv`
- Metrikler: `C:\@biyokomurlestirme\Biooil_Data_ML_Submission_Packages\04_Data_Repository_Package\metrics`
- Kaynak manifestosu: `C:\@biyokomurlestirme\Biooil_Data_ML_Submission_Packages\04_Data_Repository_Package\SOURCE_MANIFEST.md`
- TİK5 BiooilID notları: `C:\@biyokomurlestirme\tik5\TIK5_REVIZYON_YUMUSATMA_B29_B3.md`
- ML final raporu: `C:\@biyokomurlestirme\reverse_ml_biooil_to_product\ml_reverse_prediction\FINAL_REPORT.md`

