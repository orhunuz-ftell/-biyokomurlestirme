# TIK-5 Çok-Amaçlı (Ağırlıklı-Toplam) Optimizasyon — Sonuçlar

> Koşum: `tik5/run_multiobjective.py` · Ham veri: `tik5/TIK5_MULTIOBJECTIVE_RESULTS.json`
> **Model yeniden eğitilmedi.** Kayıtlı surrogate + soft-sensor yüklendi. Resmi `optimization.py`
> değiştirilmedi; çok-amaçlı amaç ayrı scriptte tanımlandı. **Bozucu etki kompozisyonda korundu.**

## Amaç fonksiyonu

```
J = 4.0·(H2/CO sapma)² + 3.0·(H2 açığı) + 2.0·(CH4 kayması)
  + 1.0·(CO2) + 1.5·(enerji) + 1.5·(koklaşma riski)   [+ 0.25·move, kapalı çevrimde]
```
Her terim ~[0,1] aralığına normalize edildi (H2_REF=50, CH4_REF=5, CO2_REF=16; koklaşma = f(T,S/C)).

## Sonuç 1 — Çok-amaçlı optimum köşeden çıktı (ana kazanım)

Tek-amaçlı (sadece oran) vs çok-amaçlı optimum, 3 temsili biyoyağ:

| Biyoyağ | Tek-amaçlı (T,P,S/C) → H2/CO | Çok-amaçlı (T,P,S/C) → H2/CO | T kayması |
|---|---|---|---|
| balanced | 850, 5, 2 → 2.65 | **775**, 5, 2 → 2.95 | 850 → **775** |
| aromatik-zengin | 850, 5, 2 → 2.52 | **800**, 5, 2 → 2.67 | 850 → **800** |
| asit-zengin | 850, 5, 2 → 2.79 | **775**, 5, 2 → 3.17 | 850 → **775** |

**Neden:** Tek-amaçlı her zaman en sıcak köşeye (T=850) gidiyor — orada **koklaşma riski = 1.0 (maks)**,
**enerji = 0.65**. Çok-amaçlı, koklaşma ve enerji terimleri devreye girince T'yi 775–800'e çekiyor:
koklaşma 1.0 → **0.5–0.67**, enerji 0.65 → **0.41–0.49** düşüyor.

> Anlatım: *"Tek kriterli optimizasyon prosesi katalizör ömrünü ve enerjiyi hiçe sayıp en sıcak noktaya
> sürüyor; çok-amaçlı formülasyon H2/CO doğruluğundan küçük bir taviz (≈0.3 birim) vererek koklaşmayı ve
> enerjiyi belirgin azaltan, işletilebilir bir noktaya yerleşiyor."* — gerçek mühendislik ödünleşimi.

### Amaç terim ayrışımı (sunum için ideal — yığılmış çubuk)
balanced, çok-amaçlı optimum (ağırlıklı katkılar):
`ratio 0.13 | H2 0.33 | CH4 0.52 | CO2 0.69 | enerji 0.61 | koklaşma 0.75`
Tek-amaçlıda bu terimlerin hepsi **0** (çünkü ağırlıkları 0) — yani tek-amaçlı koklaşma/enerji/CO2'yi
hiç görmüyor. Bu kontrast tek slaytta tüm hikâyeyi anlatır.

## Sonuç 2 — Kompozisyon bozucusu yine görünmüyor (dürüst bulgu)

Kapalı çevrim, 5. adımda kompozisyon bozucusu (asit+8, aromatik−6, fenol−2):

| | 4. adım (bozulma öncesi) | 5. adım (bozulma) | Δ |
|---|---|---|---|
| Ölçülen H2/CO | 2.9486 | 2.9816 | **+0.033** |
| Ölçülen H2 mol% | 44.582 | 44.471 | −0.111 |
| Seçilen T/P/S/C | 775/5/2 | 775/5/2 | **değişmedi** |

Çok-amaçlı yapı, **kompozisyon bozucusunu görünür kılmadı** — tıpkı duyarlılık sondajının öngördüğü gibi.
Amaç terimleri de neredeyse sabit (ratio 0.127→0.135, ch4 0.525→0.510). Kontrol hareketi yok.

**Sebep:** Surrogate'in kompozisyona duyarsızlığı yalnızca H2/CO'da değil; H2, CO2, CH4 dahil **tüm
çıktılarında** var. Amacı zenginleştirmek bu fiziksel sınırı aşmaz.

## Özet

| Hedef | Çok-amaçlı sağladı mı? |
|---|---|
| Daha zengin, savunulabilir optimizasyon | ✅ Evet — köşeden çıkış + koklaşma/enerji ödünleşimi |
| Tek vs çok amaçlı kontrast (slayt) | ✅ Evet — terim ayrışımı net |
| **Kompozisyon bozucusunu görünür kılmak** | ❌ Hayır — model sınırı değişmedi |

## Tavsiye

- **Statik optimizasyon hikâyesi için çok-amaçlı formülasyonu kullan** — gerçek bir kazanım, tezde güçlü.
- **Bozulma–toparlanma eğrisi hâlâ proses bozucusu (T/S-C sapması) gerektiriyor.** İstersen aynı
  çok-amaçlı amaçla proses bozucusunu koşayım: H2/CO + H2 verimi + CO2 + koklaşma'nın **birlikte bozulup
  birlikte toparlandığı** çok-panelli bir grafik çıkar — kompozisyon bozucusundan çok daha etkileyici.
- **Ağırlıklar bir kaldıraç:** Oran doğruluğu daha önemliyse `w_ratio`'yu artır (şu an H2/CO'dan
  ≈0.3 taviz veriliyor); koklaşmayı daha sert cezalandırmak istersen `w_coke`'u artır.
