# TIK-5 Bozucu Etki Sondajı — Sonuçlar ve Yorum

> Koşum: `tik5/run_disturbance_probe.py` · Ham veri: `tik5/TIK5_DISTURBANCE_PROBE_RESULTS.json`
> **Model yeniden eğitilmedi.** Kayıtlı forward surrogate (`forward_surrogate.joblib`) ve reverse
> soft-sensor (`mlp_standard.h5`) yüklendi; yalnızca senaryo parametreleri değiştirildi.

## TL;DR — Karar

Senin spec'inin çekirdek hedefi ("bozucu etki sonrası H2/CO >3.2 veya <2.1'e sapsın") **bu modelde
ulaşılamaz.** Sebep, benim spec'imde *birincil* sandığım köşe kilitlenmesi değil; **birincil engel
forward surrogate'in kompozisyona neredeyse duyarsız olması.** Köşe kilidi gerçek ama ikincil ve hedefi
2.5 yapmak onu çözüyor — ne var ki bu, bozucu etkiyi görünür kılmıyor çünkü bozucu etkinin kendisi
H2/CO'yu kıpırdatmıyor.

## PART A — Duyarlılık Sondajı

Koşullar `[750, 15, 4]` iç noktasında **sabit**, sadece kompozisyon değişiyor:

| Ölçüm | Sonuç | Yorum |
|---|---|---|
| 30 gerçek kompozisyon, H2/CO aralığı | 5.78 – 6.87 (std **0.196**) | Dağılım çok dar; 1.10'luk "delta_max" tek bir uç kompozisyonun artefaktı |
| **Gerçekçi bozucu yön** (asit+, aromatik−, fenol−), 0→4× büyüklük | 5.907 → 5.943, **Δ≈0.05** | 4 KATINA çıkarılmış bozucu etki bile H2/CO'yu 0.05 oynatıyor |
| Tek-değişkenli süpürme, en duyarlı (aromatik, %0→89) | Δ**0.139** | Tüm aralık baştan başa gezilse bile 0.14 |
| Diğer 5 bileşen tek-değişkenli | Δ 0.03 – 0.085 | İhmal edilebilir |

**Sonuç:** Gerçekçi bir kompozisyon bozucusunun H2/CO'da yaratabileceği değişim **~0.05**. Spec'in
istediği sapma **≥0.7**. Yani 14 kat fark var — senaryo ayarıyla kapanmaz. (Benim spec'imdeki eşik
mantığına göre: `ΔH2CO_max < 0.3` → **Plan B zorunlu**.)

> Not: Surrogate koşullara ŞİDDETLE duyarlı — aynı kompozisyon `[750,15,4]`'te H2/CO≈5.9, `[850,5,2]`'de
> ≈2.65. Yani modelde sinyal var, ama **kompozisyonda değil, T/P/S/C'de.**

## PART B — Senaryo Karşılaştırması (kapalı çevrim, bozucu adım = 5)

| Senaryo | Hedef | Başlangıç | Bozulma anı dip | Toparlanma açığı | Kontrol değişti mi? | Seçilen T |
|---|---|---|---|---|---|---|
| **V0** mevcut | 2.0 | balanced | **+0.024** | 0.67 | ✗ Hayır | 850 (köşe) |
| **V1** | 2.5 | balanced | +0.031 | 0.35 | ✗ Hayır | **800** |
| **V2** | 2.5 | aromatik-zengin | +0.032 | 0.30 | ✗ Hayır | **775** |
| **V3** | 2.5 | asit-zengin, **20-puan** asit bozucu | **−0.008** | 0.38 | ✗ Hayır | 825 |

Okunuşu:

1. **Bozulma her senaryoda görünmez.** En agresif deneme (V3: asit +20 puan) bile H2/CO'yu
   −0.008 oynatıyor. Part A'yı kapalı çevrimde doğruluyor.
2. **Hedef kaldıracı işletme noktasını gerçekten açtı:** T 850 → 800 → 775; toparlanma açığı 0.67 → 0.30.
   Yani benim "hedefi 2.5 yap, köşe kilidini aç" hipotezim **işletme noktası için doğru.** Ama…
3. **…kontrol değişkenleri bozucuya YANIT olarak hiç oynamıyor** (her senaryoda `changed=false`).
   Çünkü optimizer bozulmadan önce ve sonra neredeyse aynı H2/CO görüyor → aynı koşulu seçiyor →
   gösterilecek "toparlama hareketi" oluşmuyor.

## İki Spec'in Bu Veriyle Sınanması

- **Senin spec'in** ("bozucu etkiyi büyüt, uygun case'i tara"): büyüklük artırmak işe yaramıyor (V3 kanıtı).
  Çekirdek hedef bu modelde fiziksel olarak karşılanamaz.
- **Benim spec'im** ("önce ölç, hedefi 2.5 yap"): teşhis adımı doğru kararı verdirdi ve hedef-2.5 kaldıracı
  işletme noktasını açtı — ama **birincil engeli yanlış sıraladım.** Asıl engel köşe kilidi değil,
  kompozisyon duyarsızlığı. Bu, ancak ölçünce ortaya çıktı; sondajın değeri tam da bu.

## Öneri — Bundan Sonra (hâlâ "yeniden eğitim yok")

Kompozisyon→H2/CO hikâyesi bu surrogate ile anlatılamaz. Prensibi bozmadan üç gerçekçi yol:

1. **Bozucu etkiyi modelin duyarlı olduğu yere taşı (en güçlü, önerilen).** Bozucu etkiyi *kompozisyon*
   yerine bir *işletme bozulması* olarak tanımla (örn. ısıtıcı arızasıyla T düşüşü ya da S/C sapması).
   Surrogate koşullara şiddetle duyarlı olduğu için H2/CO belirgin sapar, optimizasyon T/P/S/C'yi
   gerçekten oynatarak toparlar → temiz "bozulma→toparlanma" eğrisi. Anlatım: "ham madde değil, **proses
   bozucusu**". Tamamen senaryo-içi, eğitim yok.
2. **Dürüst yeniden çerçeveleme.** Hikâyeyi "soft-sensor kompozisyon kaymasını yakalar, optimizasyon
   işletme noktasını hedefe sadık tutar" mesajına indir; grafikte H2/CO sapması değil, **kontrol
   değişkenlerinin/optimum noktanın** kayması vurgulanır. Zayıf yanı: Part B'de optimum da bozucuya
   yanıt vermiyor, bu yüzden bu çerçeve de cılız kalır.
3. **(Bu aşama dışı, kayıt için)** Spec'in özgün niyeti — kompozisyon kaynaklı H2/CO kontrolü — yalnızca
   surrogate'in kompozisyona duyarlı hale gelmesiyle mümkün; bu da yeniden eğitim/fizik-bilgili model
   gerektirir. Mevcut prensiple yapılamaz; gelecek dönem işi olarak not edilebilir.

**Net tavsiye:** Sunum için **Yol 1**'e geç (proses bozucusu). Tek satırla: *bozucu etkiyi biyoyağ
kompozisyonundan işletme koşuluna kaydır* — model bu sinyali taşıyor, diğerini taşımıyor.
