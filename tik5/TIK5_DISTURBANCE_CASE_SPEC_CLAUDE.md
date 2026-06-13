# TIK-5 Bozucu Etki Case-Study — Alternatif Spec (Claude)

> Bu, mevcut `TIK5_DISTURBANCE_CASE_SPEC.md`'ye **alternatif/tamamlayıcı** bir method spec'idir.
> Aynı prensibe bağlı kalır: **modeller yeniden eğitilmez, script yapısı korunur, yalnızca senaryo
> parametreleri değiştirilir.** Fark: önce kök sebebi ölçer, sonra tarar. Bu dosya yalnızca *nasıl
> yapılacağını* anlatır — script çalıştırılmaz, akış/model dosyaları değiştirilmez.

## 1. Kök Sebep Teşhisi (mevcut sonuçtan)

`results/tables/mpc_case_study.csv` üzerinden gözlenen gerçek davranış:

- Optimum 1. adımdan itibaren grid köşesine kilitleniyor: `T=850, P=5, S/C=2`. 9. adıma kadar hiç değişmiyor.
- Bozucu etki büyük (asit 24.9→31.3, aromatik 1.08→0, fenol 38.9→35.2) ama ölçülen H2/CO yalnızca
  **2.6465 → 2.6708 (Δ≈0.024)** değişiyor.
- Hedef 2.0; sistem ~2.65'e doyuyor, 2.0'a hiç ulaşamıyor.

Çıkarılan iki yapısal sorun:

- **(A) Köşe kilitlenmesi:** Hedef 2.0 ulaşılamaz olduğu için optimizer `_candidate_grid()` köşesinde
  sıkışıyor. Köşede kontrol payı (headroom) yok → bozulsa bile "toparlama" için oynatacak değişken yok.
  *Bu, senaryo değişikliğiyle çözülebilir.*
- **(B) Kompozisyon duyarsızlığı:** Forward surrogate, biyoyağ kompozisyonunu H2/CO çıktısına çok zayıf
  yansıtıyor. Büyük kayma → Δ0.02. *Bu, senaryo değişikliğiyle çözülemeyebilir; önce ölçülmelidir.*

> Ana mesaj: Bozucu etkinin görünmemesinin sebebi bozucu etkinin küçüklüğü **değil**, hedef 2.0'ın
> optimizeri köşede doyurması (A) + surrogate'in kompozisyona duyarsızlığı (B).

## 2. Adım 0 — Duyarlılık Sondajı (git/kal kararı)

Tarama yapmadan önce tek bir teşhis koşusu (yeni eğitim yok, mevcut surrogate kullanılır):

- Koşulları bir **iç nokta**da sabitle (örn. `T=750, P=15, S/C=4` — köşe değil).
- Veri setindeki tüm biyoyağ kompozisyonlarını (veya her TARGET özelliğinin min–max aralığını) bu sabit
  koşullarda surrogate'e ver, çıktı H2/CO dağılımını topla.
- **Tek metrik:** kompozisyondan elde edilebilen `max(H2/CO) − min(H2/CO) = ΔH2CO_max`.

Karar kuralı:

- `ΔH2CO_max ≳ 0.7` → kompozisyon kaynaklı bozulma fiziksel olarak mümkün. Bölüm 3'e geç (tam senaryo).
- `0.3 ≲ ΔH2CO_max < 0.7` → sınırda; bozulmayı hedef seçimiyle (2.5) görünür kıl, ama eşiği gevşet
  (Bölüm 5, kabul kriteri B').
- `ΔH2CO_max < 0.3` → kompozisyonla istenen sapma imkânsız. Bölüm 6'daki yeniden çerçeveleme şart.

Bu sondaj, kör tarama tuzağına düşmeden önce yapılır ve tek sayı üretir.

## 3. Hedef Davranış (mekanizma netleştirilmiş)

Köşe kilitlenmesi çözülünce istenen döngü şu mekanizmayla oluşur:

1. **Hedefi 2.5 yap** (mevcut spec'te izinli knob). Optimum iç bölgeye kayar; ön-bozulma koşulları
   2.5'i tutturan bir iç nokta olur — kontrol payı doğar.
2. Bozucu etki adımında kompozisyon kayar; **aynı koşullar altında** H2/CO 2.5'ten sapar → "bozulma".
3. Soft-sensor yeni kompozisyonu tahmin eder.
4. Re-optimizasyon T/P/S/C'yi oynatır (artık köşede değil, payı var) → "toparlanma".

Yani bozulma, "önceki optimum koşullar altında ölçülen H2/CO" olarak kaydedilir; bu yüzden ön-koşulların
**köşe olmaması** (interior) kritiktir.

## 4. Denenecek Parametreler (yalnızca senaryo)

Öncelik sırasına göre, her biri tek başına bir kaldıraç:

1. **Hedef H2/CO: 2.0 → 2.5** (en yüksek değerli; köşe kilidini açar). İlk denenecek.
2. **Başlangıç koşulu:** `[850,5,2]` köşesi yerine `[750,15,4]` gibi bir iç nokta — payı korur.
3. **Bozucu etki yönü/büyüklüğü:** Bölüm 2 sondajında H2/CO'ya en duyarlı çıkan eksen boyunca uygula
   (körlemesine "asit +8" değil, ölçülen en etkili bileşen).
4. **Move ağırlığı:** Kilit açıldıktan sonra hâlâ oynamıyorsa `move: 0.25 → 0.1` geçici düşür.
   (Not: köşe kilidi `move` yüzünden değil, doygunluk yüzünden; bu yüzden move son sıra.)

## 5. Kabul Kriteri (sondaja göre uyarlanan)

- Ön-bozulma H2/CO hedefe yakın: **2.35–2.65** (hedef 2.5 senaryosu için).
- Bozulma sonrası sapma:
  - **B (tercih):** |ΔH2/CO| ≥ 0.7 (örn. >3.2 veya <1.8).
  - **B' (sınır durumda):** Sondaj 0.3–0.7 verdiyse, "belirgin sapma" eşiği `ΔH2CO_max`'ın ~%70'i
    olarak raporlanır ve bu sınır dürüstçe metinde belirtilir.
- Toparlanma sonrası H2/CO tekrar 2.35–2.65'e döner.
- **T, P veya S/C'den en az birinde görünür değişim** (köşe kilidi açıldığının kanıtı).
- Grafikte "bozulma → toparlanma" tek bakışta okunur.

## 6. Eğer Kompozisyon Yetersizse — Dürüst Yeniden Çerçeveleme

`ΔH2CO_max < 0.3` ise (modelin gerçeği), anlatımı abartmak yerine doğru olanı söyle:

> "Bozucu etki, biyoyağ kompozisyonunu değiştirerek **optimum işletme noktasını** kaydırmıştır;
> soft-sensor değişimi tahmin etmiş, optimizasyon yeni T/P/S/C seçmiştir. Açık-çevrim H2/CO sapması
> küçük olsa da, kontrol bloğu işletme noktasını hedefe sadık tutmuştur."

Bu durumda grafik ana mesajı **kontrol değişkenlerinin hareketi** olur (alt panel), H2/CO sapması değil.
Bu, modeli zorlamadan teknik olarak savunulabilir bir hikâyedir.

## 7. Çalıştırma Stratejisi (method)

1. Adım 0 sondajını koş, `ΔH2CO_max` al → git/kal.
2. Küçük matris: `{hedef ∈ [2.5]} × {başlangıç ∈ [iç nokta]} × {bozucu yönü ∈ [sondajın en duyarlı ekseni]}`.
   İlk turda move'a dokunma.
3. Her denemede yalnızca: ön-bozulma H2/CO, bozulma anı H2/CO, toparlanma H2/CO, seçilen T/P/S/C,
   amaç fonksiyonu + enerji cezası — beş metrik.
4. Kabul kriterini karşılayan ilk senaryo için nihai tablo + grafik üret; gerisini üretme.

## 8. Değiştirilmeyecek Noktalar (mevcut spec'le aynı)

- Ters ML soft-sensor yeniden eğitilmez.
- İleri vekil model yeniden eğitilmez.
- Raporun resmi dosyaları değiştirilmez.
- Bu aşamada script çalıştırılmaz; yalnızca plan + sondaj tasarımı hazırlanır.

## 9. İki Spec Arasındaki Tek Cümlelik Fark

Mevcut spec: "bozucu etkiyi büyüt, uygun case'i tarayarak bul."
Bu spec: "önce neden görünmediğini ölç (köşe kilidi + duyarlılık), hedefi 2.5 yaparak kilidi aç,
sonra dar tara; kompozisyon yetersizse hikâyeyi koşul hareketine kaydır."
