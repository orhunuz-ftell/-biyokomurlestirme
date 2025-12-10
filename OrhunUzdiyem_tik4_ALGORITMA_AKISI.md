# ALGORİTMA AKIŞ DİYAGRAMI

## 1. GENEL SİSTEM AKIŞI

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│   BİYO-YAĞ KOMPOZİSYONU TAHMİN SİSTEMİ                            │
│   (Ters Makine Öğrenmesi Yaklaşımı)                               │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

                              AŞAMA 1
                         VERİ OLUŞTURMA
                               │
                               ▼
         ┌─────────────────────────────────────────┐
         │                                         │
         │   30 farklı biyo-yağ kompozisyonu       │
         │                 +                       │
         │   45 farklı proses koşulu               │
         │   (5 sıcaklık × 3 basınç × 3 S/C)       │
         │                                         │
         └─────────────────────────────────────────┘
                               │
                               ▼
         ┌─────────────────────────────────────────┐
         │                                         │
         │        CANTERA SİMÜLASYONU              │
         │   (Termodinamik denge hesabı)           │
         │                                         │
         └─────────────────────────────────────────┘
                               │
                               ▼
         ┌─────────────────────────────────────────┐
         │                                         │
         │      1,350 adet veri noktası            │
         │   (biyo-yağ + sıngaz eşleşmeleri)       │
         │                                         │
         └─────────────────────────────────────────┘


                              AŞAMA 2
                         MODEL EĞİTİMİ
                               │
                               ▼
         ┌─────────────────────────────────────────┐
         │                                         │
         │   Veriyi 3 parçaya böl:                 │
         │   • Eğitim:    944 örnek (%70)          │
         │   • Doğrulama: 203 örnek (%15)          │
         │   • Test:      203 örnek (%15)          │
         │                                         │
         └─────────────────────────────────────────┘
                               │
                               ▼
         ┌─────────────────────────────────────────┐
         │                                         │
         │   Yapay sinir ağını eğit                │
         │   (Giriş: sıngaz → Çıkış: biyo-yağ)     │
         │                                         │
         └─────────────────────────────────────────┘
                               │
                               ▼
         ┌─────────────────────────────────────────┐
         │                                         │
         │   Test setinde doğrula                  │
         │   (R² = 0.863, yani %86 doğruluk)       │
         │                                         │
         └─────────────────────────────────────────┘


                              AŞAMA 3
                           KULLANIM
                               │
                               ▼
         ┌─────────────────────────────────────────┐
         │                                         │
         │   Reaktörden sıngaz ölçümü al           │
         │   (H₂, CO, CO₂, CH₄, H₂O)               │
         │                                         │
         └─────────────────────────────────────────┘
                               │
                               ▼
         ┌─────────────────────────────────────────┐
         │                                         │
         │   Eğitilmiş modele ver                  │
         │                                         │
         └─────────────────────────────────────────┘
                               │
                               ▼
         ┌─────────────────────────────────────────┐
         │                                         │
         │   Biyo-yağ kompozisyonu tahmini al      │
         │   (6 bileşen: aromatik, asit, vb.)      │
         │                                         │
         └─────────────────────────────────────────┘
```

---

## 2. CANTERA SİMÜLASYON AKIŞI

```
┌─────────────────────────────────────────────────────────────────┐
│                     CANTERA SİMÜLASYONU                         │
│              (Termodinamik Denge Hesabı)                        │
└─────────────────────────────────────────────────────────────────┘

                           GİRİŞLER
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
     ┌────────────┐    ┌────────────┐    ┌────────────┐
     │  Biyo-yağ  │    │   Proses   │    │   Buhar    │
     │kompozisyonu│    │  koşulları │    │  miktarı   │
     │ (6 bileşen)│    │  (T, P)    │    │  (S/C)     │
     └────────────┘    └────────────┘    └────────────┘
            │                 │                 │
            └─────────────────┼─────────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │                         │
                 │   Gibbs Serbest Enerji  │
                 │     Minimizasyonu       │
                 │                         │
                 │  (Sistemin dengeye      │
                 │   ulaştığı noktayı      │
                 │   hesaplar)             │
                 │                         │
                 └─────────────────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │                         │
                 │   SINGAZ KOMPOZİSYONU   │
                 │                         │
                 │   • H₂  (hidrojen)      │
                 │   • CO  (karbon monoksit)│
                 │   • CO₂ (karbondioksit) │
                 │   • CH₄ (metan)         │
                 │   • H₂O (su buharı)     │
                 │                         │
                 └─────────────────────────┘
```

---

## 3. YAPAY SİNİR AĞI YAPISI

```
┌─────────────────────────────────────────────────────────────────┐
│                    YAPAY SİNİR AĞI (MLP)                        │
│                                                                 │
│   "Sıngaz kompozisyonundan biyo-yağ kompozisyonunu tahmin et"   │
└─────────────────────────────────────────────────────────────────┘


      GİRİŞ                  İŞLEM                    ÇIKIŞ
   (8 değişken)           (Sinir Ağı)             (6 bileşen)
        │                      │                       │
        ▼                      ▼                       ▼

  ┌───────────┐         ┌───────────┐          ┌───────────────┐
  │ Sıcaklık  │         │           │          │  Aromatikler  │
  ├───────────┤         │           │          ├───────────────┤
  │ Basınç    │         │   128     │          │    Asitler    │
  ├───────────┤         │  nöron    │          ├───────────────┤
  │ S/C oranı │         │     │     │          │   Alkoller    │
  ├───────────┤  ────▶  │    64     │  ────▶   ├───────────────┤
  │ H₂ %      │         │  nöron    │          │   Furanlar    │
  ├───────────┤         │     │     │          ├───────────────┤
  │ CO %      │         │    32     │          │   Fenoller    │
  ├───────────┤         │  nöron    │          ├───────────────┤
  │ CO₂ %     │         │           │          │  Aldehitler   │
  ├───────────┤         │           │          │  & Ketonlar   │
  │ CH₄ %     │         └───────────┘          └───────────────┘
  ├───────────┤
  │ H₂O %     │
  └───────────┘


   Ölçülebilir          Eğitim ile             Tahmin edilen
    değerler            öğrenilir              değerler
```

---

## 4. MODEL EĞİTİM SÜRECİ

```
┌─────────────────────────────────────────────────────────────────┐
│                      MODEL EĞİTİM SÜRECİ                        │
└─────────────────────────────────────────────────────────────────┘


                         ┌─────────┐
                         │ BAŞLA   │
                         └────┬────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Veriyi yükle   │
                    │  (1,350 örnek)  │
                    └────────┬────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Eğitim verisini│
                    │  modele göster  │
                    └────────┬────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Model tahmin   │
                    │  yapar          │
                    └────────┬────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Tahmini gerçek │
                    │  değerle        │
                    │  karşılaştır    │
                    └────────┬────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Hatayı hesapla │
                    │  ve modeli      │
                    │  düzelt         │
                    └────────┬────────┘
                              │
                              ▼
                       ┌─────────────┐
                       │ Yeterince   │───HAYIR───┐
                       │ iyi mi?     │           │
                       └──────┬──────┘           │
                              │                  │
                             EVET                │
                              │                  │
                              ▼                  │
                    ┌─────────────────┐          │
                    │  Test setinde   │          │
                    │  doğrula        │◀─────────┘
                    └────────┬────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Modeli kaydet  │
                    └────────┬────────┘
                              │
                              ▼
                         ┌─────────┐
                         │  BİTİR  │
                         └─────────┘
```

---

## 5. TERS TAHMİN KULLANIM SENARYOSU

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRATİK KULLANIM SENARYOSU                    │
│                                                                 │
│   "Reaktörden çıkan gazı ölçerek, girişte hangi biyo-yağın      │
│    kullanıldığını tahmin et"                                    │
└─────────────────────────────────────────────────────────────────┘


    REFORMER REAKTÖRÜ
    ─────────────────

         Biyo-yağ                              Sıngaz
        (BİLİNMİYOR)                         (ÖLÇÜLEBİLİR)
             │                                    │
             ▼                                    ▼
    ┌─────────────────┐                  ┌─────────────────┐
    │                 │                  │                 │
    │   ?????????     │ ═══════════════▶ │  Gaz Analizi    │
    │                 │    Reforming     │  ile ölç        │
    │  Hangi biyo-yağ │    Reaksiyonu    │                 │
    │  kullanıldı?    │                  │  H₂  = 33%      │
    │                 │                  │  CO  = 8%       │
    └─────────────────┘                  │  CO₂ = 15%      │
                                         │  CH₄ = 0.4%     │
                                         │  H₂O = 38%      │
                                         │                 │
                                         └────────┬────────┘
                                                  │
                                                  ▼
                                      ┌───────────────────────┐
                                      │                       │
                                      │   EĞİTİLMİŞ MODEL     │
                                      │   (Yapay Sinir Ağı)   │
                                      │                       │
                                      └───────────┬───────────┘
                                                  │
                                                  ▼
                                      ┌───────────────────────┐
                                      │                       │
                                      │   TAHMİN EDİLEN       │
                                      │   BİYO-YAĞ:           │
                                      │                       │
                                      │   Aromatikler: 42%    │
                                      │   Asitler:     26%    │
                                      │   Alkoller:     6%    │
                                      │   Furanlar:     5%    │
                                      │   Fenoller:    12%    │
                                      │   Ald-Ketonlar: 9%    │
                                      │                       │
                                      └───────────────────────┘
```

---

## ÖZET

**Bu çalışmada ne yaptık?**

1. **Veri ürettik**: Cantera yazılımı ile 1,350 adet termodinamik simülasyon yaptık

2. **Model eğittik**: Yapay sinir ağı ile sıngaz-biyo-yağ ilişkisini öğrettik

3. **Ters tahmin**: Artık sıngaz ölçümünden biyo-yağ kompozisyonunu tahmin edebiliyoruz

**Neden önemli?**

- Sıngaz analizi kolay ve hızlı (gaz kromatografisi ile dakikalar içinde)
- Biyo-yağ analizi zor ve pahalı (ıslak kimya, saatler/günler sürer)
- Bu model ile sıngaza bakarak biyo-yağı tahmin edebiliyoruz
