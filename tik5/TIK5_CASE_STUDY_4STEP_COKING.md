# TIK-5 Case Study — 4 Adımlı Anlatı (kompozisyona bağlı koklaşma terimi)

> Koşum: `tik5/run_case_study_coking.py` · Ham veri: `tik5/TIK5_CASE_STUDY_COKING_RESULTS.json`
> **Model yeniden eğitilmedi.** Kayıtlı surrogate. Yenilik: amaç fonksiyonuna **kompozisyona bağlı
> koklaşma terimi** eklendi → biyoyağ değişince **optimum proses koşulları gerçekten değişiyor.**

---

## ADIM 1 — Optimizasyon amaç fonksiyonu seçildi

Çok-amaçlı (ağırlıklı toplam), **koklaşma terimi artık kompozisyona bağlı**:

```
J = 4.0·(H2/CO sapma)² + 3.0·(H2 açığı) + 2.0·(CH4) + 1.0·(CO2)
  + 1.5·(enerji) + 8.0·[ φ(komp) · koklaşma_şekli(T, S/C) ]

φ(komp) = (aromatik% + fenol%) / 100        ← kok öncül fraksiyonu
koklaşma_şekli = clip((T−700)/150) · clip((4−S/C)/2)   ← yüksek T + düşük S/C
```
Yeni olan tek şey: koklaşma cezasının **gücü beslemenin kok-öncül içeriğiyle (φ) çarpılıyor.**

---

## ADIM 2 — Çalıştırıldı, optimum koşullar belirlendi

Başlangıç biyoyağı: **ID 69 — alkolce zengin** (Alkol %78, Aromatik %0, Fenol %0) → **φ = 0.00** (kok öncülü yok).

| | Değer |
|---|---|
| **Optimum koşullar** | **T = 850 °C, P = 5 bar, S/C = 2.0** |
| H2/CO | 3.305 |
| **Koklaşma terimi** | **0.00** (φ=0 olduğu için) |
| Amaç J | 2.006 |

> Kok öncülü olmadığı için optimizer **en sıcak noktada (850 °C)** çalışıyor — verim/dönüşüm için ideal,
> koklaşma kaygısı yok.

---

## ADIM 3 — Biyoyağ bozucusu uygulandı, optimumdan uzaklaşıldı

Bozucu: besleme **kok öncülünce zenginleşiyor** (Aromatik +15, Fenol +35 puan).

| Bileşen | Önce | Sonra |
|---|---|---|
| Aromatik | 0.0 | **10.0** |
| Fenol | 0.0 | **23.3** |
| Alkol | 78.0 | 52.0 |
| **φ (kok öncülü)** | **0.00** | **0.333** |

**Eski optimum koşulda (850/5/2) ne oldu:**
| | Adım 2 (önce) | Bozucu sonrası | Değişim |
|---|---|---|---|
| H2/CO | 3.305 | 2.972 | −0.33 |
| **Koklaşma terimi** | 0.00 | **2.667** | **+2.67** |
| **Amaç J** | 2.006 | **4.532** | **+2.525** |

> Asıl uzaklaşma **koklaşma riskinde**: φ 0 → 0.33 olunca eski sıcak nokta (850 °C) artık **yüksek-kok
> rejimi**. Amaç fonksiyonu 2.0'dan 4.5'e fırladı — yani eski optimum artık kötü bir nokta.

---

## ADIM 4 — Tekrar optimize edildi, yeni optimum belirlendi

Yeni (kok-öncüllü) kompozisyonla yeniden optimizasyon:

| | Bozucu öncesi optimum | **Bozucu sonrası yeni optimum** |
|---|---|---|
| **Sıcaklık T** | 850 °C | **775 °C  (−75 °C)** |
| Basınç P | 5 bar | 5 bar |
| S/C | 2.0 | 2.0 |
| H2/CO | 3.305 | 3.295 |
| Koklaşma terimi | 0.00 | 1.333 (eski noktadaki 2.667'nin yarısı) |
| Amaç J | 2.006 | 3.750 |

> **Optimizer sıcaklığı 850 → 775 °C düşürdü.** Sebep fiziksel: kok öncülü artınca, sıcağı düşürmek
> koklaşma terimini yarıya indiriyor (2.667 → 1.333). S/C 2'de kaldı çünkü bu beslemede H2/CO zaten
> hedefin (2.5) üstünde; S/C'yi artırmak oranı daha da bozar, ratio cezası buna direnir. Yani **T,
> koklaşmadan kaçışın kullanılabilir kaldıracı** ve optimizer onu kullandı.

---

## Özet tablo

| Adım | Sonuç |
|---|---|
| 1 — Amaç | J'ye **kompozisyona bağlı koklaşma** terimi (`8·φ·şekil`) eklendi |
| 2 — Optimum | Alkol beslemesi (φ=0) → **T=850, P=5, S/C=2** |
| 3 — Bozucu | Besleme aromatik/fenolce zenginleşti (φ: 0 → 0.33) → eski optimumda koklaşma 0 → 2.67, **J 2.0 → 4.5** |
| 4 — Yeniden optimum | **T=850 → 775 °C** — koklaşmadan kaçmak için soğudu |

**Sonuç:** Biyoyağ kompozisyonu değişince optimum proses sıcaklığı **gerçekten değişti (75 °C)**.
Bunu sağlayan, dengenin (Cantera/GRI-Mech gaz-fazı) hiç görmediği ama fiziksel olarak gerçek olan
**koklaşma** olgusunu amaç fonksiyonuna kompozisyona bağlı bir terim olarak eklemek oldu. Model
eğitilmedi; sadece amaç fonksiyonuna fizik-bilgili bir terim kondu.

## Not (ayar kaldıraçları)
- T **ve** S/C'nin birlikte kayması istenirse, hedef H2/CO daha düşük (ör. 2.0) seçilen bir beslemeyle
  çalışılır; o zaman S/C artışı hem oranı hem koklaşmayı iyileştirir ve birlikte kayar.
- `w_coke` (şu an 8) ve bozucu büyüklüğü, kayışın şiddetini ayarlar.
