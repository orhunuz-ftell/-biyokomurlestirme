# TİK-5 Sunum Metni

## Slayt 1 - Başlık

- Biyokütleden Elde Edilen Biyoyağ Kompozisyonunun Makine Öğrenmesi ile Tahmini
- Model Öngörülü Kontrol Tabanlı Süreç Optimizasyonu
- Doktora Tez İzleme Sunumu - 5
- Orhun UZDİYEM
- Ege Üniversitesi Güneş Enerjisi Enstitüsü

## Slayt 2 - Sunum İçeriği

- Tezin amacı
- Önceki dönemlerde yapılan çalışmalar
- TİK-5 döneminde yapılan çalışmalar
- Ters ML modelinin soft-sensor olarak kullanılması
- İleri vekil model, optimizasyon ve MÖK senaryosu
- Dönem içi sonuçlar
- Sonraki dönem çalışma planı

## Slayt 3 - Tezin Amacı

- Biyokütleden elde edilen biyoyağın kompozisyonunu makine öğrenmesi ile tahmin etmek
- Biyoyağın işlenmesi sonucu oluşan ürün özelliklerinden giriş biyoyağı hakkında bilgi üretmek
- Tahmin edilen biyoyağ kompozisyonunu proses optimizasyonunda kullanmak
- Hedef sentez gazı özelliklerine yaklaşan çalışma koşullarını belirlemek
- Bu yaklaşımı kapalı çevrim karar verme senaryosu içinde değerlendirmek

## Slayt 4 - Çalışmanın Genel Çerçevesi

- Biyoyağ kompozisyonu biyokütle türüne ve piroliz koşullarına bağlı olarak değişmektedir
- Bu değişkenlik proses tasarımını ve kontrolünü zorlaştırmaktadır
- Biyoyağ karakterizasyonu deneysel olarak zaman alıcı ve maliyetlidir
- Singaz kompozisyonu proses sırasında daha hızlı izlenebilir
- Bu çalışmada singazdan biyoyağ kompozisyonuna giden ters tahmin yaklaşımı kullanılmıştır

## Slayt 5 - Önceki Dönemlerde Yapılan Çalışmalar

- Literatürden biyokütle, piroliz koşulları ve biyoyağ kompozisyon verileri toplandı
- SQL Server tabanlı veri yapısı oluşturuldu
- Eksik veri doldurma ve veri ön işleme yöntemleri denendi
- Random Forest, XGBoost, ANN ve farklı regresyon modelleri karşılaştırıldı
- Biyoyağ kompozisyon tahmini için ilk makine öğrenmesi altyapısı kuruldu

## Slayt 6 - TİK-4 Dönemi: Ters ML Modeli

- Biyoyağ buhar reforming prosesi Cantera ile simüle edildi
- 30 biyoyağ kompozisyonu ve farklı proses koşullarından veri seti oluşturuldu
- Girdi değişkenleri: T, P, S/C, H2, CO, CO2, CH4, H2O
- Çıktı değişkenleri: aromatikler, asitler, alkoller, furanlar, fenoller, aldehit-ketonlar
- Standart MLP modeli en başarılı model olarak belirlendi
- Ortalama test R2 = 0.863 ve MAE = %4.03 elde edildi

## Slayt 7 - TİK-5 Döneminin Başlangıç Noktası

- Önceki dönemde geliştirilen ters MLP modeli bu dönemin temelini oluşturdu
- Model yalnızca tahmin aracı olarak değil, soft-sensor bileşeni olarak ele alındı
- Amaç, singaz kompozisyonundan biyoyağ bileşimini hesaplamalı olarak tahmin etmekti
- Bu tahminin optimizasyon ve MÖK-benzeri karar verme yapısına aktarılması hedeflendi
- T, P ve S/C karar değişkenleri olarak seçildi

## Slayt 8 - TİK-5 Döneminde Yapılan Ana Çalışmalar

- Ters ML modeli için tahmin arayüzü oluşturuldu
- İleri vekil model geliştirildi
- H2/CO hedefli optimizasyon problemi tanımlandı
- Statik optimizasyon case-study çalışmaları yürütüldü
- MÖK-benzeri kapalı çevrim senaryo oluşturuldu
- Bozucu etki altında sistem davranışı incelendi

## Slayt 9 - Ters ML Modelinin Soft-Sensor Olarak Kullanılması

- Soft-sensor, doğrudan ölçülmesi zor bir değişkenin ölçülebilir değişkenlerden tahmin edilmesidir
- Bu çalışmada tahmin edilen değişken biyoyağ kompozisyonudur
- Model girdileri proses koşulları ve singaz kompozisyonudur
- Model çıktısı altı bileşenli biyoyağ kompozisyonudur
- Tahmin edilen kompozisyon optimizasyon bloğuna aktarılmaktadır

## Slayt 10 - Soft-Sensor Giriş ve Çıkışları

- Proses koşulları: reformer sıcaklığı, basınç, buhar/karbon oranı
- Singaz bileşenleri: H2, CO, CO2, CH4, H2O
- Tahmin edilen biyoyağ bileşenleri: aromatikler, asitler, alkoller
- Tahmin edilen biyoyağ bileşenleri: furanlar, fenoller, aldehit-ketonlar
- Model çıktıları fiziksel anlamlılık için sınırlandırılıp normalize edilmektedir

## Slayt 11 - İleri Vekil Modelin Geliştirilmesi

- Optimizasyon için aday proses koşullarının hızlı değerlendirilmesi gereklidir
- Her aday koşulda Cantera simülasyonu çalıştırmak pratik değildir
- Bu nedenle ileri vekil model geliştirilmiştir
- Girdi: biyoyağ kompozisyonu, T, P, S/C
- Çıktı: H2, CO, CO2, CH4, H2O ve H2/CO oranı

## Slayt 12 - İleri Vekil Model Performansı

- Model Cantera tabanlı temiz veri seti üzerinde eğitildi
- Çok çıkışlı regresyon yaklaşımı kullanıldı
- Ortalama R2 = 0.996
- Ortalama RMSE = 0.268
- Ortalama MAE = 0.125
- Bu sonuç Cantera simülasyon veri uzayının yüksek doğrulukla temsil edildiğini göstermektedir

## Slayt 13 - Optimizasyon Problemi

- Amaç, hedef H2/CO oranına yaklaşan çalışma koşullarını belirlemektir
- Karar değişkenleri: T, P ve S/C
- Sıcaklık aralığı: 650-850 °C
- Basınç aralığı: 5-30 bar
- S/C aralığı: 2-6
- Amaç fonksiyonunda H2/CO sapması ve normalize işletme cezası birlikte kullanılmıştır

## Slayt 14 - Amaç Fonksiyonu Yorumu

- H2/CO hedef sapması temel performans ölçütüdür
- Sıcaklık, basınç ve S/C için normalize işletme cezası tanımlanmıştır
- Bu ceza gerçek ekonomik maliyet hesabı değildir
- Isı yükü, buhar üretim yükü ve kompresyon maliyeti ayrıca hesaplanmamıştır
- Bu nedenle sonuçlar basitleştirilmiş hesaplamalı optimizasyon olarak yorumlanmalıdır

## Slayt 15 - Statik Optimizasyon Senaryoları

- Üç farklı biyoyağ tipi incelendi
- Aromatik bakımından zengin biyoyağ
- Asit bakımından zengin biyoyağ
- Dengeli kompozisyona sahip biyoyağ
- Başlangıç koşulu: 750 °C, 15 bar, S/C = 4
- Hedef H2/CO değerleri: 2.0 ve 2.5

## Slayt 16 - Statik Optimizasyon Sonuçları

- Başlangıç H2/CO oranları yaklaşık 5.78-6.07 aralığındadır
- Optimizasyon sonrası H2/CO oranları yaklaşık 2.52-2.82 aralığına düşmüştür
- H2/CO = 2.0 hedefi seçilen sınırlar içinde tam yakalanamamıştır
- H2/CO = 2.5 hedefinde daha yakın sonuçlar elde edilmiştir
- Optimum noktalar çoğunlukla değişken sınırlarında bulunmuştur

## Slayt 17 - Sınır Koşullarının Yorumu

- Optimizasyon çoğu durumda T = 850 °C değerini seçmiştir
- Basınç çoğu durumda 5 bar alt sınırına gitmiştir
- S/C çoğu durumda 2 alt sınırına gitmiştir
- Bu sonuç serbest ve dengelenmiş bir optimumdan çok sınır-kısıtlı en iyi noktayı göstermektedir
- Tez yazımında karar değişkeni sınırları ayrıca tartışılacaktır

## Slayt 18 - MÖK-Benzeri Kapalı Çevrim Senaryo

- Statik optimizasyon sonrası zaman adımlı kapalı çevrim senaryo oluşturuldu
- Her adımda singaz kompozisyonu ölçüm/simülasyon bilgisi olarak alındı
- Soft-sensor ile biyoyağ kompozisyonu tahmin edildi
- İleri vekil model ile aday T, P ve S/C değerleri değerlendirildi
- Bir sonraki adım için uygun kontrol hareketi seçildi

## Slayt 19 - MÖK Senaryosunda Başlangıç Koşulları

- Başlangıç biyoyağ tipi: dengeli kompozisyon
- Başlangıç BiooilID: 60
- Başlangıç sıcaklığı: 750 °C
- Başlangıç basıncı: 15 bar
- Başlangıç S/C oranı: 4
- Simülasyon süresi: 10 zaman adımı
- Bozucu etki: 5. zaman adımı

## Slayt 20 - Bozucu Etki Senaryosu

- Beşinci zaman adımında biyoyağ kompozisyonu değiştirilmiştir
- Asit içeriği artırılmıştır
- Aromatik ve fenolik bileşenler azaltılmıştır
- Amaç, kompozisyon değişimine karşı sistem davranışını gözlemlemektir
- Bozucu etki sonrası H2/CO oranı yaklaşık 2.67 seviyesinde kalmıştır

## Slayt 21 - Kapalı Çevrim Senaryo Sonuçları

- Başlangıç H2/CO oranı 5.907 olarak hesaplanmıştır
- İlk kontrol hareketinden sonra H2/CO oranı yaklaşık 2.65 seviyesine düşmüştür
- Bozucu etki sonrası H2/CO oranı yaklaşık 2.67 seviyesine yerleşmiştir
- Sistem H2/CO oranını başlangıçtaki yüksek değerden hedef bölgeye yakın aralığa çekmiştir
- Bu sonuç tam dinamik MÖK doğrulaması değil, hesaplamalı kapalı çevrim denemedir

## Slayt 22 - Dönem İçi Ana Sonuçlar

- Ters ML modeli soft-sensor olarak kullanılabilir hale getirildi
- İleri vekil model ile Cantera veri uzayı hızlı temsil edildi
- H2/CO hedefli statik optimizasyon çalıştırıldı
- MÖK-benzeri kapalı çevrim senaryo kuruldu
- Bozucu etki altında sistem davranışı incelendi
- Çalışma tahmin, optimizasyon ve karar verme bileşenlerini aynı iş akışında birleştirdi

## Slayt 23 - Dikkatli Yorumlanması Gereken Noktalar

- Çalışma deneysel olarak doğrulanmış nihai proses kontrol sistemi değildir
- MÖK senaryosu tam dinamik MÖK formülasyonu değildir
- Enerji/maliyet terimi gerçek ekonomik analiz değil, normalize işletme cezasıdır
- İleri vekil model başarısı Cantera simülasyon verisine göredir
- H2/CO oranı tek başına proses üstünlüğünü kanıtlamaz
- Gaz kompozisyonu H2O dahil yaş baz olarak değerlendirilmelidir

## Slayt 24 - Tez Çalışmasına Katkı

- Biyoyağ kompozisyon tahmini için veri tabanı ve ML altyapısı oluşturuldu
- Buhar reforming prosesi için Cantera tabanlı veri seti üretildi
- Singazdan biyoyağ kompozisyonuna giden ters ML yaklaşımı geliştirildi
- Ters model soft-sensor olarak konumlandırıldı
- İleri vekil model ile optimizasyon hesapları hızlandırıldı
- Hesaplamalı kapalı çevrim karar verme senaryosu gösterildi

## Slayt 25 - Bir Sonraki Dönem İçerisinde Yapılacak Çalışmalar

- Araştırma ve model geliştirme aşamaları tamamlanmıştır
- Bir sonraki dönemde doktora tez yazımı tamamlanacaktır
- Tüm TİK raporları tez bütünlüğü içinde birleştirilecektir
- Tablo ve figürler tez formatına uygun hale getirilecektir
- Kaynakça ve biçimsel düzenlemeler tamamlanacaktır
- Tez savunmasına hazır nihai metin hazırlanacaktır

## Slayt 26 - Tez Yazımında Birleştirilecek Bölümler

- TİK-1: literatür, problem tanımı ve ilk veri tabanı
- TİK-2: veri çekme, veri ön işleme ve ilk modelleme altyapısı
- TİK-3: veri genişletme, model karşılaştırmaları ve performans analizi
- TİK-4: Cantera tabanlı ters ML modeli
- TİK-5: soft-sensor, ileri vekil model, optimizasyon ve kapalı çevrim senaryo
- Son aşama: sonuçların tez formatında bütünleştirilmesi

## Slayt 27 - Kapanış

- TİK-5 döneminde ters ML modeli optimizasyon iş akışına bağlanmıştır
- Cantera tabanlı ileri vekil model yüksek doğrulukla çalışmıştır
- H2/CO hedefli çalışma koşulu seçimi gösterilmiştir
- Kapalı çevrim hesaplamalı senaryo ile bozucu etki analizi yapılmıştır
- Sonraki adım doktora tezinin nihai yazımıdır
