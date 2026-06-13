# TIK-5 Case Study — 4 Adımlı Anlatı (gerçek sayılarla)

> Koşum: `tik5/run_case_study_4step.py` · Ham veri: `tik5/TIK5_CASE_STUDY_4STEP_RESULTS.json`
> **Model yeniden eğitilmedi.** Kayıtlı surrogate. Bozucu etki **kompozisyonda** (seçilen senaryo).
> Biyoyağ: balanced (ID 60), hedef H2/CO = 2.5.

---

## ADIM 1 — Optimizasyon amaç fonksiyonu seçildi

Çok-amaçlı (ağırlıklı toplam), sabit ağırlık seti:

```
J = 4.0·(H2/CO sapma)² + 3.0·(H2 açığı) + 2.0·(CH4) + 1.0·(CO2)
  + 1.5·(enerji) + 1.5·(koklaşma riski)
```
Karar değişkenleri: **T** (650–850 °C), **P** (5–30 bar), **S/C** (2–6). Hedef H2/CO = 2.5.

---

## ADIM 2 — Bu parametrelerle çalıştırıldı, optimum koşullar belirlendi

Bozucu etki **öncesi** balanced biyoyağ için optimum:

| | Değer |
|---|---|
| **Optimum koşullar** | **T = 775 °C, P = 5 bar, S/C = 2.0** |
| H2/CO oranı | **2.949** (hedef 2.5'ten sapma = 0.449) |
| H2 mol% | 44.58 |
| CO2 mol% | 11.09 |
| CH4 mol% | 1.311 |
| Amaç değeri J | 3.031 |

Amaç terim katkıları: `oran 0.13 | H2 0.33 | CH4 0.52 | CO2 0.69 | enerji 0.61 | koklaşma 0.75`

---

## ADIM 3 — Biyoyağ bozucusu uygulandı, optimum noktadan uzaklaşıldı

Bozucu: **asit +8, aromatik −6, fenol −2** (puan), sonra normalize.

Kompozisyon değişimi:
| Bileşen | Önce | Sonra |
|---|---|---|
| Aromatik | 1.08 | 0.00 |
| Asit | 24.86 | **31.32** |
| Fenol | 38.92 | 35.19 |
| (diğerleri) | … | … |

**Eski optimum koşulda (775/5/2) ölçülen sapma:**
| | Önce (Adım 2) | Bozucu sonrası | Değişim |
|---|---|---|---|
| H2/CO | 2.949 | **2.982** | **+0.033** |
| Hedeften sapma | 0.449 | 0.482 | +0.033 |

> Yani bozucu, optimum noktadan **yalnızca 0.033 birim** uzaklaştırdı (%1.1). Bozucu 3 katına
> (asit +24) çıkarılınca bile H2/CO 2.949 → 3.030, sapma sadece **+0.081**.

---

## ADIM 4 — Tekrar optimize edildi, yeni optimum belirlendi

Yeni (bozulmuş) kompozisyonla yeniden optimizasyon:

| | Bozucu öncesi optimum | Bozucu sonrası yeni optimum |
|---|---|---|
| **Koşullar** | T=775, P=5, S/C=2 | **T=775, P=5, S/C=2** |
| H2/CO | 2.949 | 2.982 |
| Optimum **kaydı mı?** | — | **HAYIR (aynı)** |

24-puanlık büyütülmüş bozucuda dahi yeni optimum yine **775/5/2** — değişmedi.

---

## Sonuç ve dürüst not

| Adım | Sonuç |
|---|---|
| 1 — Amaç | 6 terimli çok-amaçlı J seçildi |
| 2 — Optimum | **T=775, P=5, S/C=2** → H2/CO=2.949 |
| 3 — Bozucu | Optimumdan **+0.033** uzaklaşıldı (24-puanda +0.081) |
| 4 — Yeniden optimum | **Aynı: 775/5/2** — koşullar değişmedi |

**Bu, daha önce kabul ettiğin durumdur:** kompozisyon bozucusu bu surrogate'te H2/CO'yu kayda değer
oynatmadığı için optimum nokta da kaymıyor. Yani 3. ve 4. adım sayısal olarak "neredeyse hareketsiz".

**Eğer 3–4 adımının gerçek bir uzaklaşma ve geri-toparlama göstermesini istersen**, tek gereken bozucuyu
modelin duyarlı olduğu kanala taşımak (proses bozucusu, ör. ısıtıcı arızasıyla T tavanının düşmesi):
o zaman Adım 3'te H2/CO ~0.7 birim sapar, Adım 4'te optimizer P ve S/C'yi oynatarak hedefe geri çeker.
Aynı çok-amaçlı amaç fonksiyonuyla, yine model eğitmeden. İstersen bu versiyonu da üretebilirim.
