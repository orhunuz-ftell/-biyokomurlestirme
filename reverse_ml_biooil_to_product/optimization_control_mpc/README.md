# Biyo-Yağ Buhar Reforming Proses Optimizasyonu ve Model Öngörülü Kontrol

## Proje Durumu

⚠️ **Planlama Aşaması** - Danışman onayı bekleniyor

## Özet

Bu klasör, derin öğrenme modeli (R² = 0.863) kullanılarak biyo-yağ buhar reforming prosesinin optimizasyonu ve model öngörülü kontrol (MPC) sisteminin geliştirilmesi için planları içerir.

### Ana Hedef
**Sürekli çalışan gerçek zamanlı optimizasyon sistemi** geliştirmek:
- Ters ML modelden gelen **herhangi bir biyo-yağ kompozisyonu** için
- Hedeflenen sıngaz kalitesini (H2, CO, CO2, CH4, H2/CO oranı) üretecek
- **Optimal proses koşullarını** (T, P, S/C) otomatik olarak hesaplayıp
- **MPC ile gerçek zamanlı kontrol** yapabilen bir sistem

## Dosyalar

### 📋 Planlama Dosyaları

1. **IMPLEMENTATION_PLAN_rev2.md** - 🎯 **GÜNCEL PLAN** (Markdown formatı)
   - ✅ DÜZELTİLMİŞ: Biyo-yağ kompozisyonu sabit girdi
   - ✅ 3 karar değişkeni (T, P, S/C)
   - 12 bölüm, detaylı teknik plan
   - Danışmana sorulacak kritik sorular
   - 7 haftalık zaman planı

2. **IMPLEMENTATION_PLAN.md** - ⚠️ ESKİ VERSİYON (Kullanılmayacak)
   - ❌ Hatalı: 33 karar değişkeni
   - Sadece referans için saklandı

3. **IMPLEMENTATION_PLAN.txt** - ⚠️ ESKİ VERSİYON (Kullanılmayacak)
   - ❌ Hatalı versiyonun text formatı

4. **README.md** - Bu dosya
   - Hızlı genel bakış ve güncel durum

## Optimizasyon Problemi

### 🔧 Sabit Girdi (Bilinen Değer)
**Biyo-yağ kompozisyonu** - Ters ML model tarafından tahmin edilmiş veya laboratuvar analizi ile bilinen:
- Aromatikler [%]
- Asitler [%]
- Alkoller [%]
- Furanlar [%]
- Fenoller [%]
- Aldehit-ketonlar [%]

### ⚙️ Karar Değişkenleri (3 adet)
**Bu biyo-yağ için optimal proses koşulları:**
- Reformer sıcaklığı (T) [650-850°C]
- Basınç (P) [5-30 bar]
- Buhar-karbon oranı (S/C) [2.0-6.0]

### Amaç Fonksiyonları
1. **F1**: Hidrojen verimi maksimizasyonu
2. **F2**: H2/CO oranı hedef değere yaklaştırma ⚠️ *Danışman onayı gerekli*
3. **F3**: CO2 emisyonu minimizasyonu
4. **F4**: Hammadde maliyeti minimizasyonu (*gelecek çalışma*)

### Optimizasyon Algoritması
- **Particle Swarm Optimization (PSO)**
- 30 particle, 50 iterasyon (3D problem, daha hızlı)
- Çok amaçlı: Ağırlıklı toplam + Pareto analizi
- Hesaplama süresi: ~7.5 saniye/senaryo

## Planlanan Senaryolar

### 🔄 Sürekli Çalışan MPC Sistemi

**Nihai Hedef**: Herhangi bir biyo-yağ kompozisyonu için gerçek zamanlı optimizasyon yapabilen sistem
```
Reaktör → Sıngaz → Ters ML → Biyo-yağ tahmini → PSO → Optimal T,P,S/C → MPC kontrolü
         (sürekli döngü)
```

### Sistem Validasyonu - Test Kapsamı
⚠️ **OPSİYONEL - Danışman onayına bağlı**

**Seçenek A (Basit Validasyon)**:
- 1-2 örnek biyo-yağ kompozisyonu ile test
- Her test için 5 farklı amaç senaryosu
- Toplam: ~5-10 optimizasyon problemi
- Amaç: "Sistem çalışıyor mu?" doğrulaması

**Seçenek B (Kapsamlı Validasyon)**:
- 30 farklı biyo-yağ kompozisyonu ile test (veritabanından)
- Her test için 5 amaç senaryosu
- Toplam: 150 optimizasyon problemi
- Amaç: "Sistem tüm kompozisyonlarda iyi çalışıyor mu?" analizi
- Avantaj: Kompozisyon-koşul ilişkisi haritası, tez için zengin içerik

### Amaç Fonksiyon Senaryoları

| Senaryo | Amaç | Beklenen Sonuç |
|---------|------|----------------|
| 1 | Maksimum H2 verimi | T≈850°C, S/C yüksek |
| 2 | Fischer-Tropsch (H2/CO=2.5) | ⚠️ Danışman onayı bekliyor |
| 3 | Metanol sentezi (H2/CO=2.0) | ⚠️ Danışman onayı bekliyor |
| 4 | Minimum CO2 emisyonu | T yüksek, S/C=6.0 |
| 5 | Pareto optimal çözümler | Çok amaçlı trade-off analizi |

## Zaman Planı

### Seçenek A: Basit Validasyon
**Toplam Süre**: 5 hafta (~1 ay)

| Faz | Süre | Açıklama |
|-----|------|----------|
| Faz 1 | 1 hafta | Model entegrasyonu, forward simulation |
| Faz 2 | 1 hafta | PSO implementasyonu (3D optimizasyon) |
| Faz 3 | 3-4 gün | Sistem validasyonu: 1-2 örnek × 5 amaç |
| Faz 4 | 2 hafta | **MPC sistemi geliştirme** (sürekli döngü) |
| Faz 5 | 1 hafta | Raporlama, görselleştirme |

### Seçenek B: Kapsamlı Validasyon
**Toplam Süre**: 7 hafta (~1.5-2 ay)

| Faz | Süre | Açıklama |
|-----|------|----------|
| Faz 1 | 1 hafta | Model entegrasyonu, forward simulation |
| Faz 2 | 1 hafta | PSO implementasyonu (3D optimizasyon) |
| Faz 3 | 2 hafta | Kapsamlı validasyon: 30 test × 5 amaç |
| Faz 4 | 2 hafta | **MPC sistemi geliştirme** (sürekli döngü) |
| Faz 5 | 1 hafta | Raporlama, görselleştirme |

**Not**: Her iki seçenekte de nihai ürün, **herhangi bir biyo-yağ kompozisyonuna uyum sağlayan sürekli çalışan MPC sistemi**. Fark sadece test/validasyon kapsamında.

## Danışmana Sorulacak Kritik Sorular

### ⚠️ Öncelik 0: Validasyon Test Kapsamı
```
MPC sistemi geliştirilirken kaç farklı biyo-yağ kompozisyonu ile test edilsin?

Seçenek A: Basit validasyon (1-2 örnek, 3-4 gün)
  - Sistem çalışıyor mu? kontrolü
  - Hızlı prototip

Seçenek B: Kapsamlı validasyon (30 farklı kompozisyon, 2 hafta)
  - Farklı kompozisyonlarda performans analizi
  - Tez için daha zengin içerik
  - Kompozisyon-koşul ilişkisi haritası

NOT: Her iki durumda da nihai ürün SÜREKLI ÇALIŞAN MPC sistemi.
```

### ⚠️ Öncelik 1: H2/CO Hedef Oranı
```
Fischer-Tropsch için mi (H2/CO = 2.5)?
Metanol sentezi için mi (H2/CO = 2.0)?
Maksimum H2 mi (H2/CO kısıtı yok)?
Başka bir hedef oran var mı?
```

### ⚠️ Öncelik 2: Amaç Fonksiyon Ağırlıkları
```
w1 * (H2 maksimum) + w2 * (H2/CO hedef) + w3 * (CO2 minimum)

Öncelik sıralaması nedir?
Trade-off'lar kabul edilebilir mi?
Örnek: %5 daha az H2 karşılığında %20 daha az CO2?
```

### ⚠️ Öncelik 3: Proses Kısıtları
```
Sıcaklık artış hızı kısıtı var mı? (°C/dak)
Basınç değişim limiti var mı?
Güvenlik/operasyon limitleri?
```

## Beklenen Çıktılar

### Ana Ürün
- 🎯 **Sürekli Çalışan MPC Sistemi**
  - Input: Biyo-yağ kompozisyonu (6 bileşen %)
  - Çıktı: Optimal T, P, S/C + gerçek zamanlı kontrol
  - Özellik: Herhangi bir kompozisyona uyum sağlar

### Validasyon Sonuçları
- ✅ **Test senaryoları** (1-2 veya 30 örnek, danışman kararına göre)
  - Her test için optimal T, P, S/C değerleri
  - Elde edilen sıngaz kalitesi (H2, CO, CO2, CH4)
  - 5 farklı amaç senaryosu (max H2, F-T, metanol, min CO2, Pareto)

- ✅ **Pareto frontu analizi**: H2 vs CO2 trade-off eğrileri

- ✅ **MPC performans testi**:
  - Set-point değişimlerine yanıt süresi
  - Bozucu etki giderimi
  - Kararlı hal hatası

- ✅ **Hassasiyet analizi**: ΔT, ΔP, ΔS/C değişimlerinin etkisi

### Tez İçin Malzeme
- 1 Bölüm (Optimizasyon metodolojisi)
- 8-12 Grafik:
  - Pareto frontları (H2 vs CO2)
  - Optimal koşul haritaları (T-P-S/C)
  - MPC performans grafikleri
  - Hassasiyet analizi sonuçları
- 3-5 Tablo (30 biyo-yağ için sonuç özeti)
- 1 Algoritma şeması (PSO)
- 1 Mimari şema (MPC)

## Yazılım Gereksinimleri

```bash
# Python 3.11
pip install tensorflow==2.12.0
pip install cantera==3.0.0
pip install pyswarm==0.6
pip install numpy==1.23.5
pip install pandas matplotlib seaborn
```

## Klasör Yapısı (Planlanmış)

```
optimization_control_mpc/
├── data/                       # Biyo-yağ veritabanı
│   ├── biooil_database.csv    # 30 biyo-yağ kompozisyonu
│   └── syngas_database.csv    # İlgili sıngaz verileri
├── src/                        # Kaynak kodlar
│   ├── forward_simulator.py   # Cantera simülasyonu
│   ├── pso_optimizer.py       # PSO algoritması
│   ├── mpc_controller.py      # MPC implementasyonu
│   ├── sensitivity_analysis.py
│   └── visualization.py
├── scenarios/                  # 5 amaç senaryosu
│   ├── scenario1_max_H2.py
│   ├── scenario2_fischer_tropsch.py
│   ├── scenario3_methanol.py
│   ├── scenario4_low_CO2.py
│   └── scenario5_pareto.py
├── results/                    # Çıktılar
│   ├── optimal_conditions/    # T, P, S/C sonuçları
│   ├── pareto_fronts/         # Pareto grafikleri
│   ├── mpc_simulations/       # MPC sonuçları
│   └── figures/               # Tüm grafikler
├── models/                     # MLP modeli
│   └── mlp_standard_r2_0863.h5
└── docs/                       # Dokümantasyon
    ├── IMPLEMENTATION_PLAN_rev2.md
    └── README.md
```

## Sonraki Adımlar

### Şimdi
1. ✅ Plan hazırlandı
2. ⬜ Danışmana sunulacak
3. ⬜ Kritik sorular cevaplandırılacak
4. ⬜ Plan revize edilecek

### Onay Sonrası
1. Faz 1'e başla (model entegrasyonu)
2. Git repository kur
3. Haftalık ilerleme takibi

## ⚠️ Önemli Revizyon Notu

### V1.0 → V2.0 Değişikliği
**Düzeltilen Hata**: İlk planda biyo-yağ karışım oranları karar değişkeni olarak planlanmıştı (33 değişken). Bu yanlış yaklaşımdı.

**Doğru Yaklaşım**:
- Biyo-yağ kompozisyonu **sabit girdi** (ters ML model tarafından tahmin edilmiş)
- Sadece proses koşulları optimize edilecek: T, P, S/C (3 değişken)
- Bu çok daha pratik ve gerçekçi bir yaklaşım

**Sonuç**:
- ✅ Problem boyutu: 33D → 3D (10× daha basit)
- ✅ Hesaplama süresi: 25s → 7.5s (3× daha hızlı)
- ✅ Zaman planı: 9 hafta → 7 hafta
- ✅ Daha gerçekçi uygulama senaryosu

---

## İletişim

**Proje**: Biyo-yağ Buhar Reforming Proses Optimizasyonu
**Öğrenci**: Orhun Uzdiyem
**Tarih**: Aralık 2024
**Versiyon**: 2.0 - Düzeltilmiş Plan

---

*Danışman onayı alındıktan sonra implementasyon başlayacaktır.*
