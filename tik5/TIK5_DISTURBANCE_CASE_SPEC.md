# TIK-5 Bozucu Etki Case-Study Spec

## Amaç

Mevcut MÖK-benzeri kapalı çevrim senaryoda bozucu etki sonrası H2/CO oranı belirgin şekilde bozulmamaktadır. Bu nedenle sunumda anlatılmak istenen kontrol etkisi zayıf kalmaktadır. Bu çalışmanın amacı, bozucu etki sonrası H2/CO oranının hedef değerden uzaklaştığı, ardından optimizasyonun yeni T, P ve S/C değerleri belirleyerek H2/CO oranını tekrar hedef bölgeye yaklaştırdığı daha açıklayıcı bir case-study üretmektir.

## İstenen Sonuç Davranışı

Yeni case-study şu davranışı göstermelidir:

1. Başlangıç koşulunda H2/CO oranı hedef bölgeye yakın veya kontrol öncesi yüksek bir değerdedir.
2. Belirli bir zaman adımında biyoyağ kompozisyonuna bozucu etki uygulanır.
3. Bozucu etki sonrası H2/CO oranı hedef değerden belirgin şekilde uzaklaşır.
4. Soft-sensor yeni ölçümden biyoyağ kompozisyonunu tekrar tahmin eder.
5. Optimizasyon yeni T, P ve S/C değerleri seçer.
6. H2/CO oranı optimizasyon sonrası tekrar hedef değere yaklaşır.

## Kabul Kriteri

Sunuma uygun case-study için aşağıdaki koşullar aranacaktır:

- Bozucu etki öncesi H2/CO hedefe yakın olmalıdır: yaklaşık 2.4-2.8 aralığı.
- Bozucu etki sonrası H2/CO belirgin sapmalıdır: örn. 3.2 üzeri veya 2.1 altı.
- Optimizasyon sonrası H2/CO tekrar hedef bölgeye yaklaşmalıdır: yaklaşık 2.4-2.8 aralığı.
- Kontrol değişkenlerinde görünür değişim olmalıdır: en az birinde T, P veya S/C değişmelidir.
- Sonuç, "bozulma ve toparlanma" şeklinde grafik üzerinde açıkça okunabilmelidir.

## Denenecek Parametreler

Öncelikle mevcut script yapısı korunacaktır. Sadece senaryo parametreleri değiştirilecektir:

- Başlangıç biyoyağ tipi: dengeli kompozisyon yerine aromatikçe zengin veya asitçe zengin örnekler denenebilir.
- Başlangıç işletme koşulları: `[750, 15, 4]` dışında hedefe yakın ama hassas bir başlangıç noktası denenebilir.
- Bozucu etki büyüklüğü: asit, aromatik, fenol, furan ve alkol yüzdelerinde daha büyük kompozisyon kaydırmaları denenebilir.
- Bozucu etki yönü: yalnızca asit artışı değil, aromatik/fenol artışı veya alkol/furan azalması gibi alternatifler denenebilir.
- Hedef H2/CO: öncelik `2.5`; gerekirse `2.0` için ayrı senaryo değerlendirilebilir.
- Move penalty: MÖK-benzeri senaryoda kontrol hareketini fazla bastırıyorsa `move` ağırlığı geçici olarak azaltılabilir.

## Çalıştırma Stratejisi

Scriptler doğrudan büyük tarama şeklinde çalıştırılmayacaktır. Önce küçük bir parametre matrisi oluşturulacaktır. Her denemede yalnızca şu bilgiler kontrol edilecektir:

- Bozucu etki öncesi H2/CO
- Bozucu etki anındaki H2/CO
- Optimizasyon sonrası H2/CO
- Seçilen T, P ve S/C değerleri
- Amaç fonksiyonu ve enerji cezası

Uygun case bulunduğunda yalnızca o senaryo için nihai tablo ve grafik üretilecektir.

## Sunumda Kullanılacak Anlatım Hedefi

Yeni case-study şu mesajı desteklemelidir:

"Bozucu etki sonrası biyoyağ kompozisyonundaki değişim H2/CO oranını hedef değerden uzaklaştırmıştır. Soft-sensor bu değişimi yeni ölçümlerden tekrar tahmin etmiş, optimizasyon bloğu yeni T, P ve S/C değerlerini seçmiş ve H2/CO oranı tekrar hedef bölgeye yaklaştırılmıştır."

## Değiştirilmeyecek Noktalar

- Ters ML soft-sensor modeli yeniden eğitilmeyecektir.
- İleri vekil model yeniden eğitilmeyecektir.
- Raporun mevcut resmi dosyaları değiştirilmeyecektir.
- Bu aşamada script çalıştırılmayacak, yalnızca case-study arama planı hazırlanacaktır.
