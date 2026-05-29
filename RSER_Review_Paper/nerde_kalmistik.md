# RSER Review Paper - Nerede Kaldık?

**Son Guncelleme:** 29 Mayis 2026
**Proje Durumu:** %85 tamamlandi - Makale yazimi ve Table 1 genisletmesi bekliyor

---

## CALISMANIN AMACI

**Baslik:** "Machine Learning Applications in Biomass Pyrolysis: A Critical Review on Data Scarcity, Imputation Strategies, and Predictive Performance"

**Hedef Dergi:** Renewable and Sustainable Energy Reviews (RSER) - IF ~15-16, Q1

**Ana Arguman:** Biyokutle pirolizinde ML uygulamalarinda algoritma seciminden cok **veri kalitesi** model basarisini belirliyor.

**Neden Onemli:** Bu calisma ayni zamanda 3. calismanin (Reverse ML - bio-oil'den H2 uretimi ters tahmini) on calismasi. Buradaki 70 orneklik veritabani, Cantera simulasyonlarina girdi olarak kullanildi (26 bio-oil bilesimi turetildi, 1170 simulasyon uretildi).

---

## BUYUK RESIM - 3 YAYIN PLANI

```
[1. RSER Review Paper] --> Veritabani + ML metodolojisi
        |
        v
[3. Reverse ML Paper] --> Bio-oil --> Cantera --> H2 urun --> ML ters tahmin
        |
        v
[2. Composition Data Paper] --> Veri erisilebilirligi (en son)
```

**Oncelik sirasi: 1 --> 3 --> 2**

---

## TAMAMLANAN ISLER

### 1. Veritabani Olusturma (TAMAM)
- **70 ornek** deneysel veri, **14 farkli calismadan**
- Biyokutle cesitliligi: Bambu, pirinc kabugu, cam fistigi, yosun, misir kocani, mahogany, EFB vb.
- **13 girdi degiskeni:** C, H, O, N, S, Volatiles, FixedCarbon, Ash, HHV, Cellulose, Hemicellulose, Lignin, ProcessTemperature, CatalystBiomassRatio vb.
- **11 cikti degiskeni:** LiquidOutput, aromatics, acids, phenols, furans, alcohols, aldehyde_ketone, esters, aliphatichydrocarbon, oxides, sugars
- Veri SQL Server veritabaninda (BIOOIL, DESKTOP-DRO84HP\SQLEXPRESS)

### 2. Eksik Veri Analizi (TAMAM)
| Degisken | Eksik % | Oncelik |
|----------|---------|---------|
| FeedRate | 89.58% | KRITIK |
| ResidenceTime | 89.58% | KRITIK |
| Sugar | 56.25% | Yuksek |
| Alcohols | 52.08% | Yuksek |
| Oxides | 52.08% | Yuksek |
| Esters | 47.92% | Yuksek |
| Aliphatichydrocarbon | 47.92% | Yuksek |
| GasFlowrate | 47.92% | Yuksek |
| LiquidOutput | 37.50% | Orta |
| Sulfur | 31.25% | Orta |
| Aromatics | 29.17% | Orta |

### 3. Imputation Stratejileri Gelistirildi (TAMAM)
**Uc katmanli yaklasim:**
1. **Hesaplama tabanli** (Domain Knowledge): O/C, H/C oranlari; Duration sentezi; Holocellulose = Cellulose + Hemicellulose
2. **KNN Imputation:** Volatiles, FixedCarbon, Lignin, HHV icin
3. **Ortalama Imputation:** Sadece dusuk varyansli degiskenler (N)

### 4. ML Model Karsilastirmasi (TAMAM)
**Test edilen algoritmalar:** Random Forest, XGBoost, LightGBM, CatBoost, Linear Regression

| Cikti | R2 | Durum |
|-------|-----|-------|
| LiquidOutput | 0.93 | BASARILI |
| Acids | 0.88 | BASARILI |
| Aromatics | 0.83 | BASARILI |
| Aldehyde_ketone | 0.81 | BASARILI |
| Phenols | 0.56 | ORTA |
| Furans | 0.46 | ORTA |
| Aliphatichydrocarbon | -2.25 | BASARISIZ |
| Esters | <0 | BASARISIZ |
| Oxides | <0 | BASARISIZ |
| Sugars | <0 | BASARISIZ |

**Ana bulgu:** Random Forest en iyi (R2=0.90-0.98), veri kalitesi > algoritma secimi

### 5. Literatur Taramasi (TAMAM)
- PRISMA metodolojisi uygulandiw
- 623 makale tarandi --> 70 makale dahil edildi
- 2015-2024 donemi
- Bibliometrik analiz yapildi (Cin lider, +633% buyume 2019-2024)
- Sonuclar: `01_Literature_Database/LITERATURE_SEARCH_RESULTS.md`

### 6. Figurler (TAMAM - 5/5)
Tumu `03_Figures/` klasorunde, 300dpi + 600dpi versiyonlari + Python scriptleri mevcut:

| Figur | Dosya | Icerik |
|-------|-------|--------|
| Figure 1 | Figure1_PRISMA_Diagram.png | PRISMA akis diyagrami |
| Figure 2 | Figure2_Bibliometric_Analysis.png | 3 panel: yillara gore yayin, ulke dagilimi, algoritma kullanimi |
| Figure 4 | Figure4_MissingData_Heatmap.png | 30 degisken icin eksik veri isitma haritasi |
| Figure 5 | Figure5_Preprocessing_Workflow.png | 3 katmanli imputation stratejisi akis semasi |
| Figure 6 | Figure6_Model_Performance.png | 6 panel: R2 siralama, basarili/basarisiz vakalar, RMSE |

### 7. Tablolar (2/3 TAMAM)
`04_Tables/` klasorunde:

| Tablo | Dosya | Durum |
|-------|-------|-------|
| Table 1 | Table1_Algorithm_Benchmark_DRAFT.md | **EKSIK** - 7 giris var, 30-50'ye cikarilmali |
| Table 2 | Table2_MissingData_Analysis.xlsx | TAMAM |
| Table 3 | Table3_Imputation_Comparison.xlsx | TAMAM |

### 8. Makale Taslagi (MEVCUT AMA GOZDEN GECIRILMELI)
`05_Manuscript_Drafts/` klasorunde 8 bolum markdown olarak yazildi:

| Dosya | Bolum | Kelime (tahmini) |
|-------|-------|------------------|
| Section1_Introduction.md | Giris | ~2000 |
| Section2_Methodology.md | Yontem | ~2000 |
| Section3_ML_Overview.md | ML Genel Bakis | ~2500 |
| Section4_Data_Challenges.md | Veri Sorunlari (ANA KATKI) | ~3000 |
| Section5_Imputation_Strategies.md | Imputation Stratejileri | ~3000 |
| Section6_Case_Study.md | Vaka Calismasi | ~2200 |
| Section7_Recommendations.md | Oneriler | ~2000 |
| Section8_Conclusions.md | Sonuclar | ~1000 |

Ayrica `RSER_Manuscript_COMPLETE.docx` (82KB) derlenmmis taslak mevcut.

---

## YAPILMASI GEREKENLER

### Oncelik 1: Table 1 Genisletme
- **Mevcut:** 7 algoritma karsilastirmasi
- **Hedef:** 30-50 giris
- **Kaynak:** `C:\@biyokomurlestirme\biyyag_ftir\` klasorundeki PDF'ler
- **Cikarilacak bilgiler:** N (ornek sayisi), R2, RMSE, algoritma, biyokutle tipi, hedef cikti
- **Oncelikli referanslar:** [5, 12, 13, 14, 15, 18]

### Oncelik 2: Makale Metni Gozden Gecirme
- 8 bolum markdown olarak yazildi ama gozden gecirilmeli
- RSER_Manuscript_COMPLETE.docx ile karsilastirilmali
- Tutarlilik kontrolu yapilmali
- Ingilizce dil kalitesi kontrol edilmeli

### Oncelik 3: Referanslar
- `06_References/` klasoru BOS
- BibTeX dosyasi olusturulmali (100-150 referans hedefi)
- Tum atiflar kontrol edilmeli

### Oncelik 4: RSER Formatlama ve Gonderim Hazirligi
- Graphical abstract (zorunlu)
- Highlights (3-5 madde, max 85 karakter)
- Abstract (max 300 kelime)
- Keywords: biomass pyrolysis, machine learning, bio-oil prediction, missing data imputation, data preprocessing, critical review
- Author contributions statement
- Declaration of competing interest
- RSER sablonuna uygun formatlama

---

## DOSYA YAPISI

```
RSER_Review_Paper/
|
|-- 00_MASTER_PLAN.md                    <-- Ana plan dokumani (detayli 8 bolum yapisi)
|-- README.md                             <-- Proje ozeti
|-- PROGRESS_REPORT.md                    <-- Ilerleme raporu (7 Aralik 2025)
|-- nerde_kalmistik.md                    <-- BU DOSYA
|-- FINAL_SUBMISSION_CHECKLIST.md         <-- Gonderim kontrol listesi
|-- compile_manuscript.py                 <-- Makale birlestirme scripti
|-- RSER_Manuscript_COMPLETE.docx         <-- Derlenmis taslak (82KB)
|-- TODO.txt                              <-- Detayli gorev listesi
|
|-- 01_Literature_Database/
|   |-- LITERATURE_SEARCH_RESULTS.md      <-- Literatur tarama sonuclari (14,000+ kelime)
|   +-- LITERATURE_EXTRACTION_TEMPLATE.md
|
|-- 02_Data_Analysis/
|   +-- TIK_REPORTS_DATA_EXTRACTION.md    <-- TIK-1/2/3'ten cikarilan istatistikler
|
|-- 03_Figures/                           <-- TAMAM (5 figur + high-res + scriptler)
|   |-- Figure1_PRISMA_Diagram.png
|   |-- Figure2_Bibliometric_Analysis.png
|   |-- Figure4_MissingData_Heatmap.png
|   |-- Figure5_Preprocessing_Workflow.png
|   |-- Figure6_Model_Performance.png
|   +-- create_figure*.py                 <-- Tekrar uretilebilirlik icin scriptler
|
|-- 04_Tables/                            <-- 2/3 TAMAM
|   |-- Table1_Algorithm_Benchmark_DRAFT.md  <-- EKSIK (7/50 giris)
|   |-- Table2_MissingData_Analysis.xlsx     <-- TAMAM
|   +-- Table3_Imputation_Comparison.xlsx    <-- TAMAM
|
|-- 05_Manuscript_Drafts/                 <-- 8 bolum yazildi (gozden gecirilmeli)
|   |-- Section1_Introduction.md
|   |-- Section2_Methodology.md
|   |-- Section3_ML_Overview.md
|   |-- Section4_Data_Challenges.md       <-- ANA KATKI BOLUMU
|   |-- Section5_Imputation_Strategies.md
|   |-- Section6_Case_Study.md
|   |-- Section7_Recommendations.md
|   +-- Section8_Conclusions.md
|
+-- 06_References/                        <-- BOS (BibTeX olusturulmali)
```

---

## ILISKILI DOSYA VE KLASORLER

| Konum | Aciklama |
|-------|----------|
| `C:\@biyokomurlestirme\biyyag_ftir\` | 41 PDF makale (Table 1 genisletme kaynagi) |
| `C:\@biyokomurlestirme\OrhunUzdiyem_tik1.pdf` | TIK-1 raporu (ilk 48 ornek) |
| `C:\@biyokomurlestirme\OrhunUzdiyem_tik2.pdf` | TIK-2 raporu (eksik veri + model sonuclari) |
| `C:\@biyokomurlestirme\OrhunUzdiyem_tik3.pdf` | TIK-3 raporu (genisletilmis 70 ornek + imputation) |
| `C:\@biyokomurlestirme\OrhunUzdiyem_tik4.pdf` | TIK-4 raporu (Cantera + Reverse ML) |
| `C:\@biyokomurlestirme\reverse_ml_biooil_to_product\` | 3. calisma (Reverse ML) |
| `C:\@biyokomurlestirme\COMPOSITION_DATA_REVIEW_Paper\` | 2. calisma (henuz planlama asamasinda) |
| `C:\@biyokomurlestirme\biooilml\` | 6 PDF referans literatur |

---

## VERITABANI BILGILERI

- **Server:** DESKTOP-DRO84HP\SQLEXPRESS
- **Database:** BIOOIL
- **Authentication:** Windows Authentication
- **Ana tablolar:** Biooil (26 bilesim), AspenSimulation (1173 kayit), HydrogenProduct, SyngasComposition, ReformingConditions, EnergyBalance
- **Yedek:** `C:\@biyokomurlestirme\BIOOIL.bak` (20MB)

---

## BASLARKEN YAPILACAKLAR (YENI BILGISARDA)

1. Bu dosyayi oku (nerde_kalmistik.md)
2. `00_MASTER_PLAN.md` oku - detayli 8 bolum yapisi
3. `05_Manuscript_Drafts/` klasorundeki taslak bolumleri gozden gecir
4. `04_Tables/Table1_Algorithm_Benchmark_DRAFT.md` oku - genisletmeye basla
5. `biyyag_ftir/` klasorundeki PDF'lerden veri cikar (Table 1 icin)

**Ilk is:** Table 1'i 7'den 30-50 girişe cikar, sonra makale metnini gozden gecir.

---

## YAZARLAR

- **Birinci Yazar:** Orhun Uzdiyem (Ege Universitesi, Gunes Enerjisi Enstitusu)
- **Sorumlu Yazar:** Prof. Dr. Hayati Olgun
