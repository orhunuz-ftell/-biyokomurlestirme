# TİK-5 Çalışma Taslağı: Ters ML Destekli Optimizasyon ve MPC

## Çalışmanın Amacı

Bu dönemde, önceki aşamada geliştirilen ters makine öğrenmesi modeli soft-sensor olarak kullanılarak hedef H2/CO oranını sağlayan enerji etkin reformer çalışma koşullarını belirleyen optimizasyon ve MPC yapısı geliştirilmiştir. Sistem, reformer çıkışındaki singaz kompozisyonundan biyoyağ bileşimini tahmin etmekte ve bu tahmini kullanarak sıcaklık, basınç ve buhar/karbon oranı için uygun kontrol hamlesini hesaplamaktadır.

## Geliştirilen Yazılım Altyapısı

Çalışma kapsamında `optimization_control_mpc/` klasörü altında uygulama kodları oluşturulmuştur. `inverse_predictor.py` dosyasında mevcut standart MLP modeli için tahmin arayüzü geliştirilmiş, `surrogate_model.py` dosyasında ileri proses modeli kurulmuş, `optimization.py` dosyasında statik optimizasyon problemi tanımlanmış ve `mpc_controller.py` dosyasında basit kapalı çevrim MPC senaryosu hazırlanmıştır. Tüm çalışma `run_case_studies.py` ile tek komutla çalıştırılabilir hale getirilmiştir.

## Ters ML Modelinin Soft-Sensor Olarak Kullanımı

Mevcut MLP modeli, reformer sıcaklığı, basınç, buhar/karbon oranı ve H2, CO, CO2, CH4, H2O mol yüzdelerini girdi olarak alarak biyoyağ bileşimini tahmin etmektedir. Çıktı olarak aromatikler, asitler, alkoller, furanlar, fenoller ve aldehit-ketonlar yüzde bileşimleri elde edilmektedir. Bu yapı MPC sisteminde gerçek zamanlı biyoyağ kompozisyon tahmini yapan soft-sensor görevi görmektedir.

## BiooilID Bazlı Validasyon

Önceki model başarısı satır bazlı train/test ayrımıyla elde edildiği için bu dönemde ek olarak BiooilID bazlı holdout validasyon yapılmıştır. Bu testte 6 biyoyağ tamamen test setinde bırakılmış, 24 biyoyağ ile model eğitilmiştir. Aromatikler için R2=0.951, asitler için R2=0.803, fenoller için R2=0.698 ve aldehit-ketonlar için R2=0.624 elde edilmiştir. Alkoller bileşeninde düşük varyans ve zor genelleme nedeniyle R2 negatif çıkmıştır. Ortalama MAE %4.62 olarak bulunmuştur. Bu sonuç, modelin bazı bileşenlerde yeni biyoyağlara iyi genellenebildiğini, ancak özellikle düşük varyanslı veya zayıf singaz imzası taşıyan bileşenlerde daha fazla veri ve ek validasyon gerektiğini göstermektedir.

## İleri Surrogate Model

MPC ve optimizasyon için hızlı çalışan bir ileri model geliştirilmiştir. Bu model biyoyağ bileşimi ile T, P ve S/C koşullarını girdi olarak almakta; H2, CO, CO2, CH4, H2O ve H2/CO oranını tahmin etmektedir. ExtraTrees tabanlı surrogate model test setinde ortalama R2=0.996, RMSE=0.268 ve MAE=0.125 performansına ulaşmıştır. Bu nedenle Cantera simülasyonunu her optimizasyon adımında tekrar çalıştırmak yerine hızlı surrogate model kullanılmıştır.

## Optimizasyon Problemi

Karar değişkenleri reformer sıcaklığı, basınç ve buhar/karbon oranı olarak seçilmiştir. Sınırlar sırasıyla 650-850 C, 5-30 bar ve 2-6 aralığıdır. Amaç fonksiyonu, hedef H2/CO oranına yaklaşma cezası ile enerji/operasyon maliyeti vekil fonksiyonunu birlikte minimize edecek şekilde kurulmuştur. Enerji maliyeti sıcaklık, basınç ve S/C oranının normalize edilmiş ağırlıklı toplamı olarak tanımlanmıştır.

## Statik Optimizasyon Sonuçları

Üç farklı biyoyağ kompozisyonu için statik optimizasyon yapılmıştır: aromatik-zengin, asit-zengin ve dengeli kompozisyon. Başlangıç koşulu 750 C, 15 bar ve S/C=4 alınmıştır. Başlangıçta H2/CO oranı 5.78-6.07 aralığında iken optimizasyon sonrası 2.52-2.82 aralığına indirilmiştir. Hedef H2/CO=2.0 için tam hedefe ulaşılamamış, fakat mevcut proses sınırları içinde en yakın çözüm 850 C, 5 bar ve S/C=2 olarak bulunmuştur. Hedef H2/CO=2.5 durumunda bazı kompozisyonlarda daha düşük sıcaklıkta enerji maliyeti azaltılmış çözümler elde edilmiştir.

## MPC Senaryosu

Basit MPC senaryosunda sistem 10 zaman adımı boyunca çalıştırılmıştır. Başlangıçta dengeli biyoyağ kompozisyonu kullanılmış, 5. adımda biyoyağ kompozisyonuna bozucu etki uygulanmıştır. Her adımda önce surrogate model ile ölçülen singaz üretilmiş, sonra ters MLP soft-sensor ile biyoyağ kompozisyonu tahmin edilmiş ve son olarak optimizer yeni T, P ve S/C hamlesini hesaplamıştır. MPC döngüsü, H2/CO oranını başlangıçtaki 5.91 seviyesinden yaklaşık 2.65 seviyesine indirmiş ve bozucu etki sonrasında sistemi yaklaşık 2.67 seviyesinde tutmuştur.

## Çıktılar

Üretilen ana çıktılar `results/` klasörüne kaydedilmiştir. Statik optimizasyon sonuçları `results/tables/static_optimization_cases.csv`, MPC zaman serisi `results/tables/mpc_case_study.csv`, metrikler `results/metrics/` ve grafikler `results/figures/` altında yer almaktadır. Özellikle `static_optimization_h2co.png` ve `mpc_case_study_timeseries.png` rapora doğrudan eklenebilecek niteliktedir.

## Değerlendirme

Bu çalışma, ters ML modelinin yalnızca tahmin modeli olarak kalmadığını, proses optimizasyonu içinde kullanılabilecek bir soft-sensor bileşenine dönüştüğünü göstermiştir. İleri surrogate modelin yüksek doğruluğu, optimizasyon ve MPC hesaplamalarının hızlı yapılmasına olanak sağlamıştır. Bununla birlikte H2/CO=2.0 hedefinin bazı biyoyağlar için mevcut T, P ve S/C sınırlarında tam sağlanamaması, hedef oran seçiminin ve proses sınırlarının birlikte değerlendirilmesi gerektiğini göstermektedir. BiooilID bazlı validasyon sonucu ise yeni biyoyağ genellemesi için ek veri ve daha güçlü validasyon stratejilerinin önemli olduğunu ortaya koymuştur.

## Sonraki Adımlar

Bir sonraki aşamada optimizasyon ağırlıkları hassasiyet analizine tabi tutulmalı, H2/CO hedef oranı uygulama senaryosuna göre netleştirilmeli ve MPC senaryosu daha uzun zaman ufku ile test edilmelidir. Ayrıca BiooilID bazlı MLP yeniden eğitimi ve belirsizlik tahmini eklenerek soft-sensor güvenilirliği artırılabilir.
