# TIK-5 Ağırlık Taraması — Amaç Ağırlıkları Optimumu Nasıl Kaydırıyor?

> Koşum: `tik5/run_weight_sweep.py` · Ham veri: `tik5/TIK5_WEIGHT_SWEEP_RESULTS.json`
> **Model yeniden eğitilmedi.** Kayıtlı surrogate yüklendi, `run_multiobjective.py`'deki **aynı** amaç
> fonksiyonu kullanıldı. Biyoyağ: balanced (ID 60), hedef H2/CO = 2.5, statik optimizasyon.

Amaç: `J = w_ratio·(H2/CO sapma)² + w_h2·(H2 açığı) + w_ch4·(CH4) + w_co2·(CO2) + w_energy·(enerji) + w_coke·(koklaşma)`
Her terim tek tek temel değerinin **{0×, 0.5×, 1×, 2×, 4×}** katına ayarlandı, diğerleri sabit tutuldu.

---

## 1) Tek-tek ağırlık taraması (optimum T'nin kayışı)

### `w_coke` — koklaşma cezası (en belirgin etki)
| w_coke | T | S/C | H2/CO | CH4 | Yorum |
|---|---|---|---|---|---|
| 0 | **850** | 2 | 2.65 | 0.28 | Koklaşma yok sayılır → en sıcak köşe |
| 0.75 | 800 | 2 | 2.82 | 0.79 | |
| **1.5 (temel)** | **775** | 2 | 2.95 | 1.31 | |
| 3.0 | 750 | 2 | 3.12 | 2.09 | |
| 6.0 | **700** | 2 | 3.62 | 4.54 | Koklaşmayı bastırmak için en soğuk nokta |

**Monoton ve net:** Koklaşmayı ne kadar cezalandırırsan T o kadar düşüyor (850→700). Bedeli: CH4 kayması 0.28→4.54'e fırlıyor (soğukta reforming tamamlanmıyor). Gerçek ödünleşim.

### `w_energy` — enerji cezası
| w_energy | T | H2/CO | Yorum |
|---|---|---|---|
| 0 | 800 | 2.82 | Enerji bedava → daha sıcak |
| **1.5 (temel)** | 775 | 2.95 | |
| 6.0 | **700** | 3.62 | Enerjiden kaç → soğut |

### `w_h2` — H2 verimi ödülü
| w_h2 | T | S/C | H2 mol% | Yorum |
|---|---|---|---|---|
| 0 | 800 | 3 | 39.5 | H2 önemsiz → S/C yükselt, oran kötüleşir |
| **3 (temel)** | 775 | 2 | 44.6 | |
| 6–12 | **800** | 2 | 45.3 | H2 için T yükselt |

### `w_ch4` — metan kayması cezası (dönüşüm)
| w_ch4 | T | CH4 mol% | Yorum |
|---|---|---|---|
| 0 | 725 | 3.37 | Metan kaçışına izin var |
| **2 (temel)** | 775 | 1.31 | |
| 4 | 800 | 0.79 | |
| 8 | **850** | 0.16 | Tam dönüşüm için en sıcak nokta |

### `w_co2` ve `w_ratio` (daha yumuşak)
- **w_co2:** 0→1.5× iken T 775→800'e küçük kayış; CO2 ham değeri yüksek olduğu için J'yi büyütür ama optimumu az oynatır.
- **w_ratio:** 0× iken oran yok sayılır → T=750, S/C=4, H2/CO=**5.65** (!); ağırlık arttıkça optimum H2/CO=2.5'e doğru çekilir (4×'te H2/CO=2.82).

---

## 2) Adlandırılmış rejimler (sunum için özet tablo)

| Rejim | T | S/C | H2/CO | H2 | CH4 | CO2 | Optimumu çeken |
|---|---|---|---|---|---|---|---|
| **Sadece oran** (tek-amaçlı) | 850 | 2 | 2.65 | 45.6 | 0.28 | 9.47 | en sıcak köşe |
| **Dengeli** (varsayılan) | 775 | 2 | 2.95 | 44.6 | 1.31 | 11.09 | denge |
| **Verim-baskın** | 850 | 2 | 2.65 | 45.6 | 0.28 | 9.47 | H2↑+CH4↓ ⇒ sıcak |
| **Enerji-baskın** | 700 | 2 | 3.62 | 40.1 | 4.54 | 13.64 | soğut |
| **Koklaşma-baskın** | 700 | 2 | 3.62 | 40.1 | 4.54 | 13.64 | soğut + S/C koru |
| **Çevre-baskın (CO2)** | 850 | 3 | 3.15 | 39.5 | 0.16 | 9.69 | sıcak + buhar↑ |

---

## 3) Çıkarımlar (slayt mesajları)

1. **Tek-amaçlı (sadece oran) optimum = en sıcak köşe (T=850) = aynı zamanda koklaşmanın EN yüksek olduğu nokta.**
   Yani tek kriterli optimizasyon, farkında olmadan katalizör için en kötü noktayı seçiyor. Çok-amaçlı bunu düzeltiyor. (En güçlü punchline.)

2. **Sıcaklık baskın kaldıraç:** Optimum çoğunlukla T'yi oynatarak dengeleniyor (700–850). S/C ancak CH4 veya CO2 çok ağırlıklandığında 2→3'e çıkıyor. Basınç hep 5 bar (en düşük) kalıyor — yüksek P hem maliyet hem termodinamik olarak H2 aleyhine.

3. **Zıt kutuplar net:** Verim/CH4-baskın → **sıcak (850)**; enerji/koklaşma-baskın → **soğuk (700)**. İkisi tek T'de buluşamaz → optimizer ağırlıklı orta noktayı (≈775) seçiyor. Çok-amaçlı optimizasyonun varlık sebebi tam olarak bu.

4. **Ağırlık = mühendislik tercihi:** Tablo, "hangi amaca öncelik verirsek proses nereye yerleşir" sorusunun doğrudan haritası. Tezde ağırlıkları gerekçelendirmek (ör. katalizör ömrü kritikse w_coke yüksek) savunulabilir bir tasarım kararı olur.

## Öneri
- Sunumda **2 numaralı tabloyu** ve **w_coke taramasını** (monoton T kayışı) kullan — en okunaklı ikisi.
- Nihai ağırlık setini katalizör/enerji önceliğine göre seç; bu tablo gerekçeni hazır veriyor.
- İstersen bu taramayı aromatik-zengin ve asit-zengin biyoyağlar için de koşup üç biyoyağı yan yana koyabilirim.
