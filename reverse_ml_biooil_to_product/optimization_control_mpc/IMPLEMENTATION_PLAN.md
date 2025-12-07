# Biyo-Yağ Karışım Optimizasyonu ve Model Öngörülü Kontrol - Uygulama Planı

**Proje**: Derin Öğrenme Modeli ile Biyo-Yağ Buhar Reforming Optimizasyonu
**Tarih**: Aralık 2024
**Durum**: ⚠️ Danışman Onayı Bekliyor (H2/CO Hedef Oranı)
**Versiyon**: 1.0 - İlk Taslak

---

## 📋 İÇİNDEKİLER

1. [Proje Özeti](#1-proje-özeti)
2. [Bilimsel Motivasyon](#2-bilimsel-motivasyon)
3. [Problem Tanımı](#3-problem-tanımı)
4. [Optimizasyon Formülasyonu](#4-optimizasyon-formülasyonu)
5. [Uygulama Aşamaları](#5-uygulama-aşamaları)
6. [Teknik Detaylar](#6-teknik-detaylar)
7. [Beklenen Çıktılar](#7-beklenen-çıktılar)
8. [Danışmana Sorulacak Sorular](#8-danışmana-sorulacak-sorular)
9. [Zaman Planı](#9-zaman-planı)

---

## 1. PROJE ÖZETİ

### Amaç
Geliştirilen derin öğrenme modelini (MLP Standard, R² = 0.863) kullanarak, hedeflenen sıngaz kalitesini üretecek **optimal biyo-yağ karışım oranları** ve **işletme koşullarını** belirlemek.

### Giriş
- Mevcut durum: **Sıngaz → Biyo-yağ** tahmini (TERS model, R² = 0.863)
- Yeni hedef: **Hedef Sıngaz → Optimal Biyo-yağ Karışımı** (TERS OPTİMİZASYON)

### Çıkış
- 30 farklı biyo-yağın optimal karışım oranları (%0-100, toplam %100)
- Optimal proses koşulları (T, P, S/C)
- Beklenen sıngaz kompozisyonu ve performans metrikleri

---

## 2. BİLİMSEL MOTİVASYON

### Neden Gerekli?

**Endüstriyel İhtiyaç:**
- Farklı biyokütle kaynaklarından gelen biyo-yağların sürekli değişen kompozisyonu
- Hammadde maliyetlerinin optimize edilmesi ihtiyacı (gelecek çalışmada)
- İstenilen sıngaz kalitesini garantilemek

**Bilimsel Katkı:**
- Ters ML modeli + optimizasyon entegrasyonu (literatürde ilk)
- Çok amaçlı optimizasyon ile biyo-yağ harmanlama
- Model öngörülü kontrol (MPC) için temel mimari

**Pratik Değer:**
- Gerçek zamanlı karar desteği sistemi
- "Ne tür biyo-yağ karışımı kullanmalıyım?" sorusuna cevap
- Esnek hammadde yönetimi

---

## 3. PROBLEM TANIMI

### Genel Problem İfadesi

```
Hedef: Belirli bir sıngaz kalitesi (H2%, CO%, CO2%, CH4%, H2/CO oranı)

Karar:
  - 30 farklı biyo-yağın karışım oranları (x1, x2, ..., x30)
  - Reformer sıcaklığı (T)
  - Basınç (P)
  - Buhar-karbon oranı (S/C)

Kısıtlar:
  - Σxi = 100% (karışım oranları toplamı)
  - 0 ≤ xi ≤ 100 (her bir oran)
  - 650°C ≤ T ≤ 850°C
  - 5 bar ≤ P ≤ 30 bar
  - 2.0 ≤ S/C ≤ 6.0

Amaç Fonksiyonları:
  1. Hidrojen verimi maksimizasyonu
  2. H2/CO oranı hedef değere yaklaştırma [DANISMAN ONAY BEKLİYOR]
  3. CO2 emisyonu minimizasyonu
  4. (Gelecek) Hammadde maliyeti minimizasyonu
```

---

## 4. OPTİMİZASYON FORMÜLASYONU

### 4.1 Karar Değişkenleri

**Biyo-yağ Karışım Oranları (30 değişken):**
```
x = [x1, x2, x3, ..., x30]  (ağırlık yüzdesi)

Örnek:
x1 = 25%  (Biyo-yağ #1 - Aromatik-zengin)
x2 = 30%  (Biyo-yağ #2 - Asit-zengin)
x3 = 45%  (Biyo-yağ #3 - Alkol-zengin)
x4...x30 = 0%
```

**Proses Koşulları (3 değişken):**
```
T  = Reformer sıcaklığı [650-850°C]
P  = Basınç [5-30 bar]
SC = Buhar-karbon oranı [2.0-6.0]
```

**Toplam: 33 karar değişkeni**

### 4.2 Amaç Fonksiyonları (Çok Amaçlı)

#### F1: Hidrojen Verimi Maksimizasyonu
```python
F1 = -H2_mol_percent  # (negatif çünkü minimize ediyoruz)

Hedef: Maksimum H2 üretimi
Beklenen: %40-50 H2 (mol bazında, kuru gaz)
```

#### F2: H2/CO Oranı Hedef Değere Yaklaştırma
```python
F2 = |H2/CO - H2CO_target|²

⚠️ DANISMAN ONAY BEKLIYOR:
  - Fischer-Tropsch için: H2CO_target = 2.5
  - Metanol sentezi için: H2CO_target = 2.0
  - Maksimum H2 için: Bu kısıtı kaldır
```

#### F3: CO2 Emisyonu Minimizasyonu
```python
F3 = CO2_mol_percent

Hedef: Karbon dioksit üretimini minimize et
Tipik değer: %10-15
```

#### F4: (Gelecek Çalışma) Maliyet Minimizasyonu
```python
F4 = Σ(xi * cost_i)  # Toplam hammadde maliyeti

Not: Şimdilik göz ardı edilecek
```

### 4.3 Kısıtlar

**Eşitlik Kısıtı:**
```python
g1: Σxi = 100  (karışım oranları toplamı %100 olmalı)
```

**Eşitsizlik Kısıtları:**
```python
# Karışım oranları
g2: 0 ≤ xi ≤ 100  (i = 1...30)

# Proses koşulları
g3: 650 ≤ T ≤ 850
g4: 5 ≤ P ≤ 30
g5: 2.0 ≤ S/C ≤ 6.0

# Sıngaz kompozisyonu (isteğe bağlı)
g6: H2 ≥ 30%  (minimum hidrojen)
g7: CH4 ≤ 10%  (maksimum metan - karbon kaybı)
```

---

## 5. UYGULAMA AŞAMALARI

### Faz 1: Veri Hazırlığı ve Model Entegrasyonu (1 hafta)

**Adım 1.1: Mevcut ML Modelini Yükle**
- `mlp_standard.h5` modelini yükle (R² = 0.863)
- Scaler dosyalarını yükle (`scaler_X.pkl`, `scaler_y.pkl`)
- Model test et: örnek girdi → tahmin

**Adım 1.2: İleri Yönlü Simülasyon Fonksiyonu**
```python
def forward_simulation(biooil_mix_ratios, T, P, SC):
    """
    Biyo-yağ karışımı + proses koşulları → Sıngaz tahmini

    Input:
      - biooil_mix_ratios: [30] array, ağırlık yüzdeleri
      - T, P, SC: proses koşulları

    Process:
      1. Karışımın ortalama kompozisyonunu hesapla (6 bileşen)
      2. Cantera ile denge simülasyonu
      3. Sıngaz kompozisyonu ve metrikler

    Output:
      - H2, CO, CO2, CH4, H2O mol %
      - H2/CO oranı
      - Termodinamik özellikler
    """
    # Karışım kompozisyonunu hesapla
    avg_composition = weighted_average(biooil_mix_ratios, biooil_database)

    # Cantera simülasyonu
    syngas = cantera_reformer_simulation(avg_composition, T, P, SC)

    return syngas
```

**Adım 1.3: Benchmark Simülasyonları**
- 100 rastgele karışım + koşul kombinasyonu test et
- Süre: ~500 ms (Cantera) vs ~200 ms (ML modeli - gelecek kullanım)

---

### Faz 2: Optimizasyon Algoritması Geliştirme (2 hafta)

**Adım 2.1: Particle Swarm Optimization (PSO) İmplementasyonu**

```python
class BiooilBlendOptimizer:
    """
    PSO ile biyo-yağ karışım optimizasyonu
    """

    def __init__(self, n_particles=50, n_iterations=100):
        self.n_particles = n_particles
        self.n_iterations = n_iterations
        self.n_dimensions = 33  # 30 karışım + 3 proses

    def objective_function(self, x):
        """
        Çok amaçlı objektif fonksiyon

        x = [x1...x30, T, P, SC]
        """
        # Karışım oranları
        biooil_ratios = x[:30]
        T, P, SC = x[30], x[31], x[32]

        # Kısıt kontrolü
        if abs(sum(biooil_ratios) - 100) > 0.1:
            return 1e6  # Penalti (toplam != 100)

        # İleri simülasyon
        syngas = forward_simulation(biooil_ratios, T, P, SC)

        # Amaç fonksiyonları
        F1 = -syngas['H2_mol']  # Maksimize (negatif)
        F2 = (syngas['H2']/syngas['CO'] - H2CO_target)**2
        F3 = syngas['CO2_mol']

        # Ağırlıklı toplam (çok amaçlı → tek amaçlı)
        # w1, w2, w3 danışmanla belirlenecek
        objective = w1*F1 + w2*F2 + w3*F3

        return objective

    def optimize(self):
        """PSO optimizasyon döngüsü"""
        # PSO başlat
        # ...
        # Her iterasyonda particle'ları güncelle
        # ...
        return best_solution
```

**Adım 2.2: Pareto Frontu Analizi (Çok Amaçlı)**
- NSGA-II veya MOEA/D algoritması ile
- H2 verimi vs CO2 emisyonu trade-off'u
- H2 verimi vs H2/CO hedefine yakınlık

**Adım 2.3: Kısıt Yönetimi**
- Penalti fonksiyonları
- Projeksiyon yöntemi (toplam %100'e normalize)

---

### Faz 3: Senaryo Analizleri (2 hafta)

**Senaryo 1: Maksimum Hidrojen Üretimi**
```
Amaç: F1 (H2 maksimum)
Kısıt: H2/CO oran kısıtı yok
Beklenen: T=850°C, P=5 bar, alkol-zengin karışım
```

**Senaryo 2: Fischer-Tropsch için Optimum Karışım**
```
⚠️ DANISMAN ONAY BEKLIYOR
Amaç: F2 (H2/CO = 2.5'e yakın)
Beklenen: Dengeli aromatik-alkol karışımı
```

**Senaryo 3: Metanol Sentezi için Optimum**
```
⚠️ DANISMAN ONAY BEKLIYOR
Amaç: F2 (H2/CO = 2.0'a yakın)
```

**Senaryo 4: Düşük Emisyon (CO2 Minimize)**
```
Amaç: F3 (CO2 minimum)
Beklenen: T=850°C, S/C=6.0, H2 yüksek ama CO2 düşük
```

**Senaryo 5: Çok Amaçlı (Pareto Optimal)**
```
Amaç: F1 + F2 + F3 eşzamanlı
Çıktı: Pareto frontu (trade-off grafikleri)
```

---

### Faz 4: Model Öngörülü Kontrol (MPC) Mimarisi (3 hafta)

**Adım 4.1: MPC Problem Formülasyonu**

```
Zaman Adımı: k
Horizon: N = 10 (10 adım ileriye bak)

Durum Değişkenleri (x_k):
  - Mevcut biyo-yağ karışım oranları
  - Mevcut proses koşulları
  - Ölçülen sıngaz kompozisyonu

Kontrol Değişkenleri (u_k):
  - Biyo-yağ karışım oranlarındaki değişim (Δx)
  - Proses koşullarındaki değişim (ΔT, ΔP, ΔSC)

Hedef Yörünge (r_k):
  - İstenilen H2 mol %
  - İstenilen H2/CO oranı
  - İzin verilen CO2 limiti

Optimizasyon (her zaman adımında):
  min Σ[k to k+N] (||y_k - r_k||² + λ||Δu_k||²)

  Birinci terim: Hedef sapması
  İkinci terim: Kontrol çabası (yumuşak değişim)
```

**Adım 4.2: Geri Besleme Döngüsü**

```
1. Sıngaz kompozisyonunu ölç (GC-MS)
2. Ters ML modeli ile biyo-yağ kompozisyonunu tahmin et
3. Hedef sıngaz ile mevcut arasındaki farkı hesapla
4. MPC ile düzeltme hareketi belirle
5. Biyo-yağ karışım oranlarını güncelle
6. 1. adıma dön
```

**Adım 4.3: Simülasyon Testi**
- Sanal reaktör simülasyonu (Cantera)
- Rastgele girdi bozulmaları ekle
- MPC'nin düzeltme performansını test et

---

### Faz 5: Görselleştirme ve Raporlama (1 hafta)

**Çıktılar:**

1. **Optimal Karışım Reçetesi**
   - Bar chart: 30 biyo-yağın karışım oranları
   - Pie chart: Ana bileşenler dağılımı

2. **Proses Koşulları**
   - Optimal T, P, S/C değerleri
   - Hassasiyet analizi (±10°C, ±5 bar etkileri)

3. **Pareto Frontu**
   - H2 verimi vs CO2 emisyonu
   - Trade-off noktaları

4. **Zaman Serisi (MPC Simülasyonu)**
   - Hedef vs gerçek sıngaz kompozisyonu
   - Kontrol hareketleri (karışım oranı değişimleri)

5. **Karşılaştırma Tabloları**
   - 5 senaryo yan yana
   - Performans metrikleri

---

## 6. TEKNİK DETAYLAR

### 6.1 Yazılım Gereksinimleri

```python
# Python 3.11
tensorflow==2.12.0          # MLP modeli
scikit-learn==1.2.2         # Scaler
cantera==3.0.0              # Termodinamik simülasyon
pyswarm==0.6               # PSO algoritması
numpy==1.23.5
pandas
matplotlib
seaborn
```

### 6.2 Hesaplama Karmaşıklığı

**PSO Parametreleri:**
- Particle sayısı: 50
- İterasyon sayısı: 100
- Toplam fonksiyon değerlendirmesi: 50 × 100 = 5,000

**Süre Tahmini:**
- Cantera simülasyonu: ~5 ms
- Toplam: 5,000 × 5 ms = 25 saniye (tek senaryo)

**Alternatif (Hızlandırma):**
- ML modeli kullan (Cantera yerine): ~0.2 ms
- Toplam: 5,000 × 0.2 ms = 1 saniye
- Ama ML modeli sıngaz → biyo-yağ (ters), biyo-yağ → sıngaz yok!
- **Çözüm**: Cantera kullan, paralelize et (10 çekirdek → 2.5 saniye)

### 6.3 Dosya Yapısı

```
optimization_control_mpc/
│
├── data/
│   ├── biooil_database.csv         # 30 biyo-yağ kompozisyonları
│   └── optimization_results.csv    # Sonuçlar
│
├── src/
│   ├── forward_simulator.py        # Cantera simülasyon
│   ├── pso_optimizer.py            # PSO algoritması
│   ├── mpc_controller.py           # MPC implementasyonu
│   ├── objective_functions.py      # F1, F2, F3 fonksiyonları
│   └── visualization.py            # Grafikler
│
├── scenarios/
│   ├── scenario1_max_h2.py
│   ├── scenario2_fischer_tropsch.py
│   ├── scenario3_methanol.py
│   ├── scenario4_low_emission.py
│   └── scenario5_pareto.py
│
├── results/
│   ├── optimal_blends/
│   ├── pareto_fronts/
│   ├── mpc_simulations/
│   └── figures/
│
├── models/
│   └── mlp_standard.h5             # Ters model (sıngaz→biyo-yağ)
│
├── IMPLEMENTATION_PLAN.md          # Bu dosya
├── IMPLEMENTATION_PLAN.txt         # Aynı içerik (text)
└── README.md
```

---

## 7. BEKLENEN ÇIKTILAR

### 7.1 Teknik Çıktılar

1. **Optimal Biyo-yağ Karışım Reçeteleri** (5 senaryo için)
2. **Pareto Optimal Çözümler** (çok amaçlı)
3. **MPC Simülasyon Sonuçları**
4. **Hassasiyet Analizi** (parametrik çalışmalar)

### 7.2 Bilimsel Katkılar

1. **İlk kez**: Ters ML modeli + optimizasyon entegrasyonu (biyo-yağ reforming)
2. **İlk kez**: Çok kaynaklı biyo-yağ harmanlama optimizasyonu
3. MPC mimarisi (gerçek zamanlı kontrol için temel)

### 7.3 Tez İçin Malzeme

- **1 Bölüm**: Optimizasyon metodolojisi
- **5-10 Grafik**: Pareto, optimal karışımlar, MPC simülasyonu
- **2-3 Tablo**: Senaryo karşılaştırmaları
- **1 Algoritma Şeması**: PSO akış diyagramı
- **1 Mimari Şema**: MPC döngüsü

---

## 8. DANIŞMANA SORULACAK SORULAR

### ⚠️ KRİTİK SORULAR (Planı Tamamlamak İçin)

#### Soru 1: Hedef H2/CO Oranı
```
Fischer-Tropsch sentezi için mi (H2/CO = 2.5)?
Metanol sentezi için mi (H2/CO = 2.0)?
Yoksa maksimum H2 üretimi mi (H2/CO kısıtı yok)?

Bu karar F2 objektif fonksiyonunu belirleyecek.
```

#### Soru 2: Amaç Fonksiyon Ağırlıkları
```
Eğer çok amaçlı optimizasyon yaparsak:
  w1 * (H2 maksimum) + w2 * (H2/CO hedef) + w3 * (CO2 minimum)

Öncelik sıralaması:
  1. Hangi amaç en önemli?
  2. Hangi amaç ikincil?
  3. Trade-off'lar kabul edilebilir mi?

Örnek:
  - %10 daha fazla H2 için %5 daha fazla CO2 kabul edilir mi?
```

#### Soru 3: Hammadde Çeşitliliği Kısıtı
```
Pratikte kullanılabilecek maksimum biyo-yağ çeşidi sayısı?
  - 30 farklı kaynak kullanmak realistik değil
  - Örnek: "En fazla 5 farklı kaynak karıştırılabilir"

Bu kısıt eklenmeli mi?
```

#### Soru 4: Operasyonel Kısıtlar
```
Sıcaklık değişim hızı limiti var mı?
  - Örnek: ΔT ≤ 50°C/saat

Karışım değişim sınırı?
  - Örnek: |Δx_i| ≤ 10%/gün

MPC için önemli!
```

### 📝 YARDIMCI SORULAR (İyileştirmeler İçin)

#### Soru 5: Deneysel Validasyon
```
Gelecekte deneysel çalışma planlanıyor mu?
  - Eğer evet: Hangi karışımları test etmeliyiz?
  - Öncelik: Optimal çözümleri mi yoksa ekstrem koşulları mı?
```

#### Soru 6: Literatür Hedefleri
```
Belirli bir literatür çalışmasıyla karşılaştırma yapılacak mı?
  - Eğer evet: Hedef değerleri bilelim
  - Örnek: "Smith et al. 2020: H2 = %45, CO2 = %12"
```

#### Soru 7: Ekonomik Analiz
```
Gelecek aşamada maliyet optimizasyonu eklenecek mi?
  - Şimdilik hayır dedik ama plan için düşünelim
  - Biyo-yağ fiyat tahminleri lazım mı?
```

---

## 9. ZAMAN PLANI

### Taslak Takvim (Danışman Onayından Sonra Başlayacak)

| Hafta | Faz | Görevler | Tamamlanma |
|-------|-----|----------|------------|
| 1 | Faz 1 | Model entegrasyonu, forward simulation | □ |
| 2-3 | Faz 2 | PSO implementasyonu, test | □ |
| 4-5 | Faz 3 | 5 senaryo analizi | □ |
| 6-8 | Faz 4 | MPC geliştirme ve simülasyon | □ |
| 9 | Faz 5 | Raporlama, görselleştirme | □ |

**Toplam Süre**: 9 hafta (~2 ay)

### Kilometre Taşları

- ✅ **Hafta 0**: Plan tamamlandı, danışman onayı bekleniyor
- ⬜ **Hafta 1**: İlk optimizasyon sonuçları (basit senaryo)
- ⬜ **Hafta 3**: PSO çalışıyor, tüm senaryolar test edildi
- ⬜ **Hafta 6**: MPC ilk simülasyon başarılı
- ⬜ **Hafta 9**: Tüm sonuçlar hazır, tez yazımı başlayabilir

---

## 10. BAŞARI KRİTERLERİ

### Minimum Başarı (Tez için yeterli)
- ✅ En az 3 farklı senaryo için optimal karışım bulundu
- ✅ PSO algoritması yakınsıyor (100 iterasyonda)
- ✅ Pareto frontu elde edildi (2 amaç için)
- ✅ MPC simülasyonu çalışıyor (sanal reaktör)

### Hedeflenen Başarı
- ✅ 5 senaryo tamamlandı
- ✅ Çok amaçlı (3 amaç) Pareto frontu
- ✅ MPC bozulmalara karşı dayanıklı
- ✅ Hassasiyet analizi yapıldı

### Mükemmel Başarı (Bonus)
- ✅ Deneysel validasyon (1-2 karışım test edildi)
- ✅ Literatür ile karşılaştırma
- ✅ Ekonomik analiz eklendi (maliyet optimizasyonu)
- ✅ Gerçek zamanlı dashboard (web arayüzü)

---

## 11. RİSKLER VE ÇÖZÜMLER

### Risk 1: PSO Yakınsamıyor
**Çözüm**:
- Particle sayısını artır (50 → 100)
- Başlangıç popülasyonunu iyileştir (random → heuristic)
- Alternatif algoritma: Genetik Algoritma

### Risk 2: Cantera Simülasyonu Yavaş
**Çözüm**:
- Paralel hesaplama (multiprocessing)
- GPU hızlandırma (mümkünse)
- ML surrogate model (Cantera yerine)

### Risk 3: Pareto Frontu Dejenere
**Çözüm**:
- Amaç fonksiyonlarını yeniden normalize et
- Ağırlık vektörlerini ayarla
- Farklı çok amaçlı algoritma: NSGA-II

### Risk 4: MPC Kararsız
**Çözüm**:
- Horizon uzunluğunu ayarla (N = 10 → 20)
- Kontrol ağırlığını artır (λ)
- Yumuşak kısıtlar ekle

---

## 12. SONRAKİ ADIMLAR

### Şimdi Yapılacaklar:
1. ✅ Bu planı danışmana sun
2. ⬜ H2/CO hedef oranını belirle (danışman)
3. ⬜ Amaç fonksiyon ağırlıklarını kararlaştır
4. ⬜ Ek kısıtlar var mı kontrol et
5. ⬜ Planı revize et (danışman geri bildirimiyle)

### Plan Onaylandıktan Sonra:
1. Faz 1'e başla (model entegrasyonu)
2. GitHub/version control kur
3. Haftalık ilerleme takibi

---

## 13. REFERANSLAR

### Kullanılacak Kütüphaneler
- **Cantera**: Termodinamik simülasyon
- **PySwarm**: PSO implementasyonu
- **DEAP**: Genetik algoritma (yedek)
- **Platypus**: Çok amaçlı optimizasyon
- **Python-MPC**: Model öngörülü kontrol

### İlgili Literatür (Eklenecek)
- Fischer-Tropsch sentezi optimizasyonu
- Metanol sentezi için sıngaz kalitesi
- Biyo-yağ harmanlama
- Model öngörülü kontrol reaktörlerde

---

**Hazırlayan**: Claude + Orhun Uzdiyem
**Tarih**: Aralık 2024
**Versiyon**: 1.0 - İlk Taslak
**Durum**: ⚠️ Danışman Onayı Bekleniyor

---

## NOTLAR

Bu plan bir **ilk taslaktır**. Danışmanla görüşmeden sonra:
- H2/CO hedef oranı eklenecek
- Amaç fonksiyonları netleştirilecek
- Ek kısıtlar tanımlanacak
- Zaman planı revize edilecek

Planın son hali `IMPLEMENTATION_PLAN_FINAL.md` olarak kaydedilecektir.
