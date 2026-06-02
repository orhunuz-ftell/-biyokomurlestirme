# TİK-5 Raporu İçin Word'e Aktarılacak Tablolar

## Tablo B.1. Bu dönem gerçekleştirilen ana çalışma adımları

| Aşama | Çalışma adımı | Amaç | Çıktı |
|---|---|---|---|
| 1 | Ters ML modelinin soft-sensor olarak düzenlenmesi | Singaz ve proses koşullarından biyoyağ kompozisyonu tahmini üretmek | Kullanılabilir tahmin arayüzü |
| 2 | BiooilID bazlı validasyon | Modelin yeni biyoyağ kompozisyonlarına genelleme davranışını incelemek | Grup bazlı validasyon metrikleri |
| 3 | İleri surrogate model geliştirilmesi | Biyoyağ kompozisyonu ve proses koşullarından singaz çıktısını hızlı tahmin etmek | Çok çıkışlı ileri tahmin modeli |
| 4 | Statik optimizasyon | Hedef H2/CO oranına yakın ve daha düşük maliyetli çalışma koşulları belirlemek | Case-study optimizasyon sonuçları |
| 5 | MPC senaryosu | Kompozisyon değişimi altında kontrol hareketlerini test etmek | Kapalı çevrim simülasyon senaryosu |

## Tablo B.2. Geliştirilen yazılım dosyaları ve işlevleri

| Dosya / modül | İşlev |
|---|---|
| `src/common.py` | Ortak kolon adları, veri yolu tanımları ve yardımcı fonksiyonlar |
| `src/inverse_predictor.py` | Ters ML modelini soft-sensor olarak çalıştıran tahmin arayüzü |
| `src/biooil_holdout_validation.py` | BiooilID bazlı eğitim/test ayrımı ve validasyon metrikleri |
| `src/surrogate_model.py` | İleri surrogate model eğitimi ve performans değerlendirmesi |
| `src/optimization.py` | Amaç fonksiyonu ve statik optimizasyon hesaplamaları |
| `src/mpc_controller.py` | Basit MPC döngüsü ve bozucu etki senaryosu |
| `run_case_studies.py` | Statik optimizasyon ve MPC case-study çalıştırma dosyası |

## Tablo B.3. Önceki dönemde geliştirilen ters ML modelinin girişleri, çıkışları ve performans özeti

| Özellik | Açıklama |
|---|---|
| Model tipi | Standart çok katmanlı yapay sinir ağı (MLP) |
| Giriş değişkenleri | Reformer sıcaklığı, basınç, S/C, H2, CO, CO2, CH4, H2O |
| Çıkış değişkenleri | Aromatikler, asitler, alkoller, furanlar, fenoller, aldehit-ketonlar |
| Veri kaynağı | Cantera tabanlı biyoyağ buhar reforming simülasyonları |
| Veri büyüklüğü | 30 biyoyağ kompozisyonu ve 1350 temiz simülasyon örneği |
| Ortalama test R2 | 0.863 |
| Ortalama test MAE | %4.03 |
| Bu dönemki kullanım | Soft-sensor bileşeni olarak biyoyağ kompozisyon tahmini |

## Tablo B.4. Ters ML soft-sensor modelinin giriş ve çıkış değişkenleri

| Değişken grubu | Değişkenler | Açıklama |
|---|---|---|
| Proses koşulları | Reformer sıcaklığı, basınç, buhar/karbon oranı | İşletme sırasında bilinen kontrol/işletme değişkenleri |
| Singaz kompozisyonu | H2, CO, CO2, CH4, H2O mol yüzdeleri | Reformer çıkışından ölçülen veya simülasyonla elde edilen değişkenler |
| Soft-sensor çıktısı | Aromatikler, asitler, alkoller, furanlar, fenoller, aldehit-ketonlar | Tahmin edilen biyoyağ kompozisyonu |

## Tablo B.5. Soft-sensor modülünün yazılım yapısı

| Dosya / bileşen | Görev |
|---|---|
| `inverse_predictor.py` | Kaydedilmiş MLP modelini ve ölçeklendiricileri yükler |
| `ReverseMLSoftSensor` sınıfı | Singaz ve proses koşullarından biyoyağ kompozisyonu tahmini üretir |
| `mlp_standard.h5` | Önceki dönemde eğitilen standart MLP modeli |
| `scaler_X.pkl` | Giriş değişkenleri için kullanılan ölçeklendirici |
| `scaler_y.pkl` | Çıkış değişkenleri için kullanılan ölçeklendirici |

## Tablo B.6. BiooilID bazlı validasyonda kullanılan eğitim ve test veri yapısı

| Veri kümesi | BiooilID sayısı | Örnek sayısı | Açıklama |
|---|---:|---:|---|
| Eğitim kümesi | 24 | 1080 | Modelin eğitildiği biyoyağ kompozisyonları |
| Test kümesi | 6 | 270 | Eğitimde hiç görülmeyen biyoyağ kompozisyonları |
| Toplam | 30 | 1350 | Cantera tabanlı temiz veri seti |

## Tablo B.7. BiooilID bazlı validasyon bileşen bazlı performans sonuçları

| Bileşen | R2 | RMSE (%) | MAE (%) |
|---|---:|---:|---:|
| Aromatikler | 0.951 | 7.43 | 5.84 |
| Asitler | 0.803 | 6.42 | 5.23 |
| Alkoller | -6.577 | 4.01 | 2.58 |
| Furanlar | 0.464 | 2.79 | 2.07 |
| Fenoller | 0.698 | 11.51 | 8.88 |
| Aldehit-ketonlar | 0.624 | 4.71 | 3.14 |
| Ortalama | -0.506 | 6.14 | 4.62 |

## Tablo B.8. İleri surrogate modelin giriş ve çıkış değişkenleri

| Değişken grubu | Değişkenler | Açıklama |
|---|---|---|
| Biyoyağ kompozisyonu | Aromatikler, asitler, alkoller, furanlar, fenoller, aldehit-ketonlar | Soft-sensor çıktısı veya bilinen BiooilID kompozisyonu |
| Kontrol değişkenleri | Reformer sıcaklığı, reformer basıncı, buhar/karbon oranı | Optimizasyon ve MPC tarafından değiştirilen proses koşulları |
| Model çıktıları | H2, CO, CO2, CH4, H2O, H2/CO | Aday çalışma koşulunun sentez gazı performansı |

## Tablo B.9. İleri surrogate model performans sonuçları

| Çıkış değişkeni | R2 | RMSE | MAE |
|---|---:|---:|---:|
| H2 mol% | 0.997 | 0.414 | 0.211 |
| CO mol% | 0.997 | 0.220 | 0.087 |
| CO2 mol% | 0.987 | 0.233 | 0.102 |
| CH4 mol% | 0.998 | 0.188 | 0.071 |
| H2O mol% | 0.999 | 0.393 | 0.217 |
| H2/CO oranı | 0.997 | 0.157 | 0.062 |
| Ortalama | 0.996 | 0.268 | 0.125 |

## Tablo B.10. Optimizasyon karar değişkenleri ve sınırları

| Karar değişkeni | Alt sınır | Üst sınır | Birim |
|---|---:|---:|---|
| Reformer sıcaklığı | 650 | 850 | °C |
| Reformer basıncı | 5 | 30 | bar |
| Buhar/karbon oranı | 2 | 6 | - |

## Tablo B.11. Amaç fonksiyonu bileşenleri

| Amaç fonksiyonu bileşeni | Rolü |
|---|---|
| H2/CO hedef sapması | Sentez gazı oranını hedef değere yaklaştırır |
| Enerji/işletme maliyeti | Daha düşük sıcaklık, basınç ve buhar kullanımını teşvik eder |
| H2 alt sınır cezası | Hidrojen üretiminin yetersiz kalmasını engeller |
| CO2 üst sınır cezası | CO2 oluşumunun artmasını sınırlar |
| Kontrol hareketi cezası | MPC senaryosunda ani kontrol değişimlerini azaltır |

## Tablo B.12. Statik optimizasyon case-study sonuçları

| Senaryo | BiooilID | Hedef H2/CO | Başlangıç H2/CO | Optimum T (°C) | Optimum P (bar) | Optimum S/C | Optimum H2/CO | Enerji maliyeti |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Aromatik zengin | 66 | 2.0 | 5.778 | 850 | 5 | 2 | 2.518 | 0.650 |
| Aromatik zengin | 66 | 2.5 | 5.778 | 775 | 5 | 2 | 2.770 | 0.406 |
| Asit zengin | 70 | 2.0 | 6.070 | 850 | 5 | 2 | 2.786 | 0.650 |
| Asit zengin | 70 | 2.5 | 6.070 | 850 | 5 | 2 | 2.786 | 0.650 |
| Dengeli | 60 | 2.0 | 5.907 | 850 | 5 | 2 | 2.647 | 0.650 |
| Dengeli | 60 | 2.5 | 5.907 | 800 | 5 | 2 | 2.819 | 0.488 |

## Tablo B.13. MPC algoritmasının temel adımları

| Adım | İşlem | Kullanılan model/modül |
|---|---|---|
| 1 | Mevcut proses koşulu ve sentez gazı bileşimi alınır | Ölçüm/senaryo verisi |
| 2 | Biyoyağ kompozisyonu tahmin edilir | Ters ML soft-sensor |
| 3 | Aday T, P ve S/C değerleri denenir | Optimizasyon modülü |
| 4 | Her aday için sentez gazı bileşimi tahmin edilir | İleri surrogate model |
| 5 | Amaç fonksiyonuna göre en uygun kontrol hareketi seçilir | Optimizasyon modülü |
| 6 | Seçilen ilk kontrol hareketi uygulanır | MPC döngüsü |

## Tablo B.14. MPC senaryosunda kullanılan başlangıç koşulları

| Parametre | Değer |
|---|---:|
| Başlangıç biyoyağ tipi | Dengeli kompozisyon |
| Başlangıç BiooilID | 60 |
| Başlangıç sıcaklığı | 750 °C |
| Başlangıç basıncı | 15 bar |
| Başlangıç S/C oranı | 4 |
| H2/CO hedefi | 2.0 |
| Simülasyon süresi | 10 zaman adımı |
| Bozucu etki zamanı | 5. zaman adımı |

## Tablo B.15. MPC senaryosu özet sonuçları

| Zaman adımı | Durum | Uygulanan T (°C) | Uygulanan P (bar) | Uygulanan S/C | Ölçülen H2/CO | Sonraki tahmin H2/CO |
|---:|---|---:|---:|---:|---:|---:|
| 0 | Başlangıç | 750 | 15 | 4 | 5.907 | 2.639 |
| 1 | Kontrol sonrası | 850 | 5 | 2 | 2.647 | 2.639 |
| 5 | Bozucu etki sonrası | 850 | 5 | 2 | 2.671 | 2.670 |
| 9 | Son durum | 850 | 5 | 2 | 2.671 | 2.670 |

## Tablo B.16. Son zaman adımında gerçek ve soft-sensor tahmini biyoyağ kompozisyonu

| Bileşen grubu | Gerçek kompozisyon (%) | Tahmin edilen kompozisyon (%) |
|---|---:|---:|
| Aromatikler | 0.000 | 1.455 |
| Asitler | 31.324 | 27.421 |
| Alkoller | 8.758 | 4.779 |
| Furanlar | 11.334 | 11.372 |
| Fenoller | 35.188 | 35.640 |
| Aldehit-ketonlar | 13.395 | 19.333 |

## Tablo B.17. Dönem içi ana çıktılar ve bulgular

| Çalışma adımı | Ana çıktı | Temel bulgu |
|---|---|---|
| Soft-sensor arayüzü | Ters ML modeli kontrol sistemine bağlandı | Biyoyağ kompozisyonu hızlı tahmin edilebilir hale geldi |
| BiooilID validasyonu | Grup bazlı genelleme testi yapıldı | Bazı bileşenlerde yeni biyoyağa geçişte belirsizlik arttı |
| İleri surrogate model | Sentez gazı tahmin modeli geliştirildi | Ortalama R2 = 0.996 elde edildi |
| Statik optimizasyon | Üç biyoyağ tipi için case-study çalıştırıldı | H2/CO oranı yaklaşık 2.5-2.8 aralığına indirildi |
| MPC senaryosu | Bozucu etki altında kapalı çevrim simülasyon yapıldı | H2/CO oranı bozucu etki sonrasında dar aralıkta tutuldu |
