# Biyo-Yağ Buhar Reforming Proses Optimizasyonu ve Model Öngörülü Kontrol - Uygulama Planı

**Proje**: Belirli Biyo-Yağ için Optimal Proses Koşulları Bulma
**Tarih**: Aralık 2024
**Durum**: ⚠️ Danışman Onayı Bekliyor (H2/CO Hedef Oranı)
**Versiyon**: 2.0 - Revize (Karar Değişkenleri Düzeltildi)

---

## 📋 İÇİNDEKİLER

1. [Proje Özeti](#1-proje-özeti)
2. [Problem Tanımı - Düzeltilmiş](#2-problem-tanımı-düzeltilmiş)
3. [Optimizasyon Formülasyonu](#3-optimizasyon-formülasyonu)
4. [Uygulama Aşamaları](#4-uygulama-aşamaları)
5. [Model Öngörülü Kontrol (MPC)](#5-model-öngörülü-kontrol-mpc)
6. [Danışmana Sorulacak Sorular](#6-danışmana-sorulacak-sorular)
7. [Zaman Planı](#7-zaman-planı)

---

## 1. PROJE ÖZETİ

### Amaç
Belirli bir biyo-yağ kompozisyonu için (tahmin edilmiş veya bilinen), hedeflenen sıngaz kalitesini üretecek **optimal proses koşullarını** (sıcaklık, basınç, buhar-karbon oranı) belirlemek.

### Sistem Akışı

```
[Reaktör] → [Sıngaz Ölçümü] → [Ters ML Model] → [Biyo-yağ Tahmini]
                                                          ↓
                                                    [SABİT GİRDİ]
                                                          ↓
[Hedef Sıngaz] ← [OPTİMİZASYON] ← [Cantera Simülasyon] ← [T, P, S/C]
    Kalitesi         (PSO)              (İleri)          [KARAR DEĞİŞKENLERİ]
```

### Giriş (Sabit)
- **Biyo-yağ kompozisyonu**: 6 bileşen (aromatikler, asitler, alkoller, furanlar, fenoller, aldehitler-ketonlar) [wt%]
  - Kaynak 1: Ters ML modelinden tahmin edilmiş (R² = 0.863)
  - Kaynak 2: Laboratuvar analizi ile bilinen
  - Kaynak 3: Veritabanından seçilmiş (30 biyo-yağdan biri)

### Karar Değişkenleri (Optimize Edilecek - 3 adet)
- **T**: Reformer sıcaklığı [650-850°C]
- **P**: Basınç [5-30 bar]
- **S/C**: Buhar-karbon oranı [2.0-6.0]

### Çıkış
- Optimal proses koşulları (T*, P*, S/C*)
- Beklenen sıngaz kompozisyonu (H2, CO, CO2, CH4, H2O)
- Performans metrikleri (H2 verimi, H2/CO oranı, CO2 emisyonu)

---

## 2. PROBLEM TANIMI - DÜZELTİLMİŞ

### 2.1 Doğru Problem İfadesi

```
VERİLEN (Sabit Girdi):
  - Biyo-yağ kompozisyonu: [Aromatikler%, Asitler%, Alkoller%,
                             Furanlar%, Fenoller%, Aldehitler-Ketonlar%]

BULMAK İSTENEN (Karar Değişkenleri):
  - Optimal T  [650-850°C]
  - Optimal P  [5-30 bar]
  - Optimal S/C [2.0-6.0]

AMAÇ:
  - Hedef sıngaz kalitesi:
    • Maksimum H2 verimi
    • Belirli H2/CO oranı [DANISMAN ONAY BEKLİYOR]
    • Minimum CO2 emisyonu

KISITLAR:
  - 650 ≤ T ≤ 850
  - 5 ≤ P ≤ 30
  - 2.0 ≤ S/C ≤ 6.0
  - (İsteğe bağlı) H2 ≥ 30%, CH4 ≤ 10%
```

### 2.2 Neden Bu Yaklaşım Doğru?

**Önceki Yanlış Yaklaşım:**
- ❌ 30 biyo-yağın karışımını optimize et (33 karar değişkeni)
- ❌ Gerçekçi değil: 30 farklı biyo-yağ karıştırmak pratikte imkansız

**Doğru Yaklaşım:**
- ✅ Kullanılan biyo-yağ BELLİ (ters modelden tahmin edilmiş veya bilinen)
- ✅ Bu biyo-yağ için en iyi proses koşullarını bul (3 karar değişkeni)
- ✅ Gerçekçi: Operatör T, P, S/C'yi ayarlayabilir

---

## 3. OPTİMİZASYON FORMÜLASYONU

### 3.1 Matematiksel Model

**Karar Vektörü:**
```
x = [T, P, S/C]
```

**İleri Simülasyon Modeli:**
```python
Syngas = Cantera_Simulation(Biooil_Composition, T, P, S/C)

# Cantera Gibbs minimizasyonu
# Girdi: Biyo-yağ (6 bileşen) + Buhar + T + P
# Çıktı: Denge sıngaz kompozisyonu (H2, CO, CO2, CH4, H2O)
```

**Amaç Fonksiyonları:**

#### F1: Hidrojen Verimi Maksimizasyonu
```python
F1 = -H2_mol_percent  # Negatif (minimize ediyoruz)

Hedef: Maksimum H2 üretimi
Beklenen: 40-50% H2 (mol, kuru gaz)
```

#### F2: H2/CO Oranı Hedef Değere Yaklaştırma
```python
F2 = |H2/CO - target|²

⚠️ DANISMAN ONAY BEKLIYOR:
  - Fischer-Tropsch: target = 2.5
  - Metanol sentezi: target = 2.0
  - Maksimum H2: Bu kısıtı kaldır
```

#### F3: CO2 Emisyonu Minimizasyonu
```python
F3 = CO2_mol_percent

Hedef: Karbon dioksit minimize
Tipik: 10-15%
```

**Çok Amaçlı Birleştirme:**
```python
Objective = w1*F1 + w2*F2 + w3*F3

# Ağırlıklar danışmanla belirlenecek
```

### 3.2 Kısıtlar

```python
# Proses sınırları
g1: 650 ≤ T ≤ 850
g2: 5 ≤ P ≤ 30
g3: 2.0 ≤ S/C ≤ 6.0

# Sıngaz kalitesi (isteğe bağlı)
g4: H2 ≥ 30%  # Minimum hidrojen
g5: CH4 ≤ 10%  # Maksimum metan (karbon kaybı)
g6: CO > 0%    # Yanma olmamalı
```

---

## 4. UYGULAMA AŞAMALARI

### Faz 1: Model Entegrasyonu (1 hafta)

**Adım 1.1: Cantera İleri Simülasyon Fonksiyonu**

```python
def forward_simulation(biooil_composition, T, P, SC):
    """
    Biyo-yağ + proses koşulları → Sıngaz (Cantera)

    Input:
      - biooil_composition: dict
        {
          'aromatics': 32.87,  # wt%
          'acids': 10.21,
          'alcohols': 14.45,
          'furans': 8.33,
          'phenols': 16.82,
          'aldehydes_ketones': 17.32
        }
      - T: Sıcaklık [°C]
      - P: Basınç [bar]
      - SC: Buhar-karbon oranı

    Output:
      - syngas: dict
        {
          'H2_mol': 45.2,     # mol%
          'CO_mol': 18.5,
          'CO2_mol': 12.3,
          'CH4_mol': 5.8,
          'H2O_mol': 18.2,
          'H2_CO_ratio': 2.44,
          'enthalpy': -125.3,  # kJ/mol
          'entropy': 245.6     # J/mol-K
        }

    Process:
      1. Biyo-yağ → vekil moleküller (C7H8, CH3COOH, ...)
      2. Buhar miktarı hesapla (S/C oranından)
      3. Cantera'ya ver: kompozisyon, T, P
      4. Gibbs minimizasyonu → denge
      5. Sonuçları döndür
    """

    # Surrogate mapping
    surrogate_species = {
        'aromatics': 'C7H8',           # Toluene
        'acids': 'CH3COOH',            # Acetic acid
        'alcohols': 'C2H5OH',          # Ethanol
        'furans': 'C4H4O',             # Furan
        'phenols': 'C6H6O',            # Phenol
        'aldehydes_ketones': 'C3H6O'  # Acetone
    }

    # Cantera simülasyon
    gas = ct.Solution('gri30.yaml')

    # ... (tam implementasyon Faz 1'de)

    return syngas
```

**Adım 1.2: Optimizasyon Test Senaryosu**

```python
# Test: Bilinen bir biyo-yağ için optimal koşulları bul

biooil_test = {
    'aromatics': 40.0,
    'acids': 25.0,
    'alcohols': 15.0,
    'furans': 5.0,
    'phenols': 10.0,
    'aldehydes_ketones': 5.0
}

# Hedef: Maksimum H2
# Başlangıç tahmini: T=750, P=15, SC=4
# PSO ile bul: T=?, P=?, SC=?
```

---

### Faz 2: Particle Swarm Optimization (2 hafta)

**Adım 2.1: PSO Algoritması**

```python
class ProcessOptimizer:
    """
    Belirli bir biyo-yağ için optimal T, P, S/C bulur
    """

    def __init__(self, biooil_composition, objective_weights):
        self.biooil = biooil_composition
        self.w1, self.w2, self.w3 = objective_weights

        # PSO parametreleri
        self.n_particles = 30  # 3 değişken → daha az particle
        self.n_iterations = 50  # Daha hızlı yakınsama

        # Sınırlar
        self.lb = [650, 5, 2.0]    # [T_min, P_min, SC_min]
        self.ub = [850, 30, 6.0]   # [T_max, P_max, SC_max]

    def objective_function(self, x):
        """
        x = [T, P, S/C]
        """
        T, P, SC = x

        # İleri simülasyon
        syngas = forward_simulation(self.biooil, T, P, SC)

        # Amaç fonksiyonları
        F1 = -syngas['H2_mol']  # Maksimize (negatif)
        F2 = (syngas['H2_CO_ratio'] - H2CO_target)**2
        F3 = syngas['CO2_mol']

        # Kısıt ihlali penaltisi
        penalty = 0
        if syngas['H2_mol'] < 30:  # Minimum H2
            penalty += 1e6
        if syngas['CH4_mol'] > 10:  # Maksimum CH4
            penalty += 1e6

        return self.w1*F1 + self.w2*F2 + self.w3*F3 + penalty

    def optimize(self):
        """PSO çalıştır"""
        from pyswarm import pso

        xopt, fopt = pso(
            self.objective_function,
            self.lb,
            self.ub,
            swarmsize=self.n_particles,
            maxiter=self.n_iterations
        )

        return {
            'T_optimal': xopt[0],
            'P_optimal': xopt[1],
            'SC_optimal': xopt[2],
            'objective_value': fopt
        }
```

**Hesaplama Süresi:**
```
Particle sayısı: 30
İterasyon: 50
Toplam değerlendirme: 30 × 50 = 1,500

Cantera simülasyon: ~5 ms
Toplam süre: 1,500 × 5 ms = 7.5 saniye (tek senaryo!)

Çok hızlı! ✅
```

---

### Faz 3: Çoklu Biyo-Yağ Senaryoları (2 hafta)

**30 farklı biyo-yağ için optimal koşulları bul**

```python
# Veritabanından 30 biyo-yağ yükle
biooils = load_biooil_database()  # 30 kompozisyon

results = []

for i, biooil in enumerate(biooils):
    print(f"Biyo-yağ #{i+1} optimize ediliyor...")

    optimizer = ProcessOptimizer(
        biooil_composition=biooil,
        objective_weights=[0.6, 0.3, 0.1]  # w1, w2, w3
    )

    result = optimizer.optimize()

    results.append({
        'biooil_id': i+1,
        'composition': biooil,
        'T_optimal': result['T_optimal'],
        'P_optimal': result['P_optimal'],
        'SC_optimal': result['SC_optimal'],
        'H2_predicted': result['H2_mol'],
        'H2_CO_ratio': result['H2_CO_ratio'],
        'CO2_predicted': result['CO2_mol']
    })

# Sonuçları kaydet
df = pd.DataFrame(results)
df.to_csv('optimal_conditions_30_biooils.csv')
```

**Beklenen Çıktı:**

| Biyo-yağ ID | Aromatikler | T_opt | P_opt | S/C_opt | H2% | H2/CO |
|-------------|-------------|-------|-------|---------|-----|-------|
| 1 | 80% | 850°C | 5 bar | 6.0 | 48% | 2.8 |
| 2 | 10% | 820°C | 10 bar | 4.5 | 45% | 2.3 |
| ... | ... | ... | ... | ... | ... | ... |

**Analiz:**
- Aromatik-zengin → Yüksek T, Düşük P (metan minimize)
- Alkol-zengin → Orta T, Yüksek S/C (H2 maksimize)
- Asit-zengin → Yüksek T, Yüksek S/C (CO2 yönetimi)

---

### Faz 4: Hassasiyet Analizi (1 hafta)

**Optimal koşulların hassasiyeti:**

```python
# Optimal nokta: T=800°C, P=15 bar, S/C=4.0

# T hassasiyeti
for delta_T in [-50, -25, 0, +25, +50]:
    syngas = forward_simulation(biooil, 800+delta_T, 15, 4.0)
    print(f"ΔT={delta_T}: H2={syngas['H2_mol']:.1f}%")

# P hassasiyeti
for delta_P in [-10, -5, 0, +5, +10]:
    syngas = forward_simulation(biooil, 800, 15+delta_P, 4.0)
    print(f"ΔP={delta_P}: H2={syngas['H2_mol']:.1f}%")

# S/C hassasiyeti
for delta_SC in [-1, -0.5, 0, +0.5, +1]:
    syngas = forward_simulation(biooil, 800, 15, 4.0+delta_SC)
    print(f"ΔSC={delta_SC}: H2={syngas['H2_mol']:.1f}%")
```

**Çıktı: Hassasiyet Matrisi**
```
           ΔH2%    ΔCO2%   ΔH2/CO
ΔT=+10°C   +2.3%   -0.5%   +0.15
ΔP=+5bar   -1.8%   +0.3%   -0.12
ΔS/C=+0.5  +3.5%   +1.2%   +0.28
```

---

### Faz 5: Model Öngörülü Kontrol (MPC) (3 hafta)

**Senaryo: Reaktör gerçek zamanlı çalışıyor**

```
DÖNGÜ:
  1. Sıngaz ölç (her 5 dakika)
  2. Ters ML model ile biyo-yağ tahmin et
  3. Bu biyo-yağ için optimal T, P, S/C bul
  4. Mevcut koşullar ile karşılaştır
  5. Düzeltme hareketi yap (MPC)
  6. Bekle 5 dakika, tekrarla
```

**MPC Formülasyonu:**

```python
class MPCController:
    """
    Model Predictive Control for bio-oil reforming
    """

    def __init__(self, horizon=10):
        self.N = horizon  # 10 adım ileriye bak
        self.dt = 5       # 5 dakika örnekleme

    def compute_control(self, current_state, target_state):
        """
        current_state: [T_current, P_current, SC_current, syngas_measured]
        target_state: [H2_target, CO_target, CO2_target, H2CO_target]

        return: [ΔT, ΔP, ΔSC] (düzeltme hareketleri)
        """

        # 1. Ters model ile biyo-yağ tahmin et
        biooil_estimated = inverse_ml_model(syngas_measured)

        # 2. Hedef için optimal koşulları bul
        optimizer = ProcessOptimizer(biooil_estimated, weights)
        optimal = optimizer.optimize()

        # 3. Mevcut vs optimal farkı
        ΔT = optimal['T'] - current_state['T']
        ΔP = optimal['P'] - current_state['P']
        ΔSC = optimal['SC'] - current_state['SC']

        # 4. Yumuşak değişim (operasyonel kısıtlar)
        ΔT = np.clip(ΔT, -10, +10)    # Maks ±10°C/adım
        ΔP = np.clip(ΔP, -2, +2)      # Maks ±2 bar/adım
        ΔSC = np.clip(ΔSC, -0.5, +0.5)  # Maks ±0.5/adım

        return [ΔT, ΔP, ΔSC]
```

**Simülasyon Testi:**

```python
# Sanal reaktör (Cantera)
reactor_state = {
    'T': 750,
    'P': 15,
    'SC': 4.0,
    'biooil': biooil_random  # Rastgele değişen
}

# Hedef
target = {
    'H2': 45,
    'H2_CO': 2.5
}

# MPC simülasyonu (100 adım = 500 dakika)
for t in range(100):
    # Sıngaz ölç
    syngas = forward_simulation(
        reactor_state['biooil'],
        reactor_state['T'],
        reactor_state['P'],
        reactor_state['SC']
    )

    # MPC düzeltme
    control = mpc.compute_control(reactor_state, target)

    # Koşulları güncelle
    reactor_state['T'] += control[0]
    reactor_state['P'] += control[1]
    reactor_state['SC'] += control[2]

    # Biyo-yağ değişimi simüle et (bozulma)
    if t % 20 == 0:  # Her 20 adımda değiş
        reactor_state['biooil'] = add_noise(biooil_random)

    # Kaydet
    log(t, syngas, reactor_state)
```

**Beklenen Sonuç:**
- Hedef H2 = 45% → Gerçekleşen 45% ± 2% (iyi)
- Hedef H2/CO = 2.5 → Gerçekleşen 2.5 ± 0.2 (iyi)
- Biyo-yağ değişimlerine karşı dayanıklı

---

## 5. VİZÜALİZASYON

### Grafik 1: Optimal Koşullar Haritası (30 Biyo-yağ)

```
3D Scatter Plot:
  X: Aromatikler%
  Y: Alkoller%
  Z: T_optimal
  Renk: H2 verimi
```

### Grafik 2: Pareto Frontu

```
H2 Verimi vs CO2 Emisyonu
  - Her nokta: Farklı ağırlık (w1, w2, w3)
  - Trade-off: +5% H2 → +2% CO2
```

### Grafik 3: Hassasiyet Analizi

```
Heatmap:
  Satır: ΔT, ΔP, ΔS/C
  Sütun: ΔH2, ΔCO, ΔCO2, ΔH2/CO
  Değer: Hassasiyet katsayısı
```

### Grafik 4: MPC Simülasyon Zaman Serisi

```
Zaman (dakika) vs:
  - H2% (hedef=45, gerçekleşen)
  - H2/CO (hedef=2.5, gerçekleşen)
  - T, P, S/C (kontrol hareketleri)
  - Biyo-yağ değişimleri (bozulma)
```

---

## 6. DANIŞMANA SORULACAK SORULAR

### ⚠️ KRİTİK SORULAR

**Soru 1: H2/CO Hedef Oranı**
```
Fischer-Tropsch sentezi için mi (H2/CO = 2.5)?
Metanol sentezi için mi (H2/CO = 2.0)?
Maksimum H2 üretimi mi (H2/CO kısıtı yok)?
```

**Soru 2: Amaç Fonksiyon Öncelikleri**
```
Hangisi en önemli?
  1. Maksimum H2
  2. Hedef H2/CO oranı
  3. Minimum CO2

Ağırlıklar: w1=?, w2=?, w3=?
```

**Soru 3: Operasyonel Kısıtlar**
```
Sıcaklık değişim hızı limiti?
  - Örnek: ΔT ≤ 10°C/dakika

Basınç değişim hızı?
  - Örnek: ΔP ≤ 1 bar/dakika
```

**Soru 4: MPC Parametreleri**
```
Örnekleme süresi?
  - Örnek: Her 5 dakikada sıngaz ölç

Horizon uzunluğu?
  - Örnek: N=10 adım ileri bak
```

---

## 7. ZAMAN PLANI

**Toplam: 7 hafta (Daha kısa! Sadece 3 karar değişkeni)**

| Hafta | Faz | Görev | Çıktı |
|-------|-----|-------|-------|
| 1 | Faz 1 | Cantera entegrasyonu | forward_simulation.py |
| 2-3 | Faz 2 | PSO optimizasyon | pso_optimizer.py |
| 4-5 | Faz 3 | 30 biyo-yağ senaryoları | optimal_conditions_30_biooils.csv |
| 6 | Faz 4 | Hassasiyet analizi | sensitivity_analysis.csv |
| 7 | Faz 5 | MPC simülasyon | mpc_simulation_results.csv |

---

## 8. BEKLENEN ÇIKTILAR

### Teknik
1. **Optimal Koşullar Tablosu** (30 biyo-yağ)
2. **Pareto Frontu** (H2 vs CO2)
3. **Hassasiyet Matrisi**
4. **MPC Simülasyon Sonuçları**

### Tez İçin
- 1 Bölüm (Optimizasyon)
- 4-5 Grafik
- 2-3 Tablo
- MPC algoritma şeması

---

## 9. AVANTAJLAR (Revize Yaklaşım)

### Önceki Plan vs Yeni Plan

| Özellik | Önceki (Yanlış) | Yeni (Doğru) |
|---------|-----------------|--------------|
| Karar değişkeni | 33 (30 karışım + 3 proses) | **3 (sadece proses)** ✅ |
| Hesaplama süresi | 25 saniye | **7.5 saniye** ✅ |
| Gerçekçilik | Düşük (30 karışım?) | **Yüksek** ✅ |
| Uygulanabilirlik | Zor | **Kolay** ✅ |
| Optimizasyon zorluğu | Yüksek (33D) | **Düşük (3D)** ✅ |

---

**Hazırlayan**: Claude + Orhun Uzdiyem
**Tarih**: Aralık 2024
**Versiyon**: 2.0 - Revize (Karar Değişkenleri Düzeltildi)
**Durum**: ⚠️ Danışman Onayı Bekleniyor

---

## ÖZET - ÖNEMLİ DEĞİŞİKLİK

**ESKI (YANLIŞ):**
- Biyo-yağ karışım oranları karar değişkeni (30 değişken)
- Toplam 33 karar değişkeni
- Gerçekçi değil

**YENİ (DOĞRU):**
- Biyo-yağ kompozisyonu SABİT (tahmin edilmiş veya bilinen)
- Sadece proses koşulları karar değişkeni (3 değişken: T, P, S/C)
- Gerçekçi ve uygulanabilir ✅
