# Literature Data Assessment - Phase 1
## Bio-oil Composition Data Availability Survey

**Tarih:** 5 Ocak 2026
**Durum:** Devam ediyor

---

## Veri Detay Seviyeleri (Data Detail Levels)

| Seviye | Aciklama | Ornek |
|--------|----------|-------|
| 1 | Sadece bio-yag verimi | "Bio-oil yield: 45%" |
| 2 | Bilesik sinifi toplamlari | "Aromatics: 25%, Acids: 15%" |
| 3 | Bireysel bilesenler | "Acetic acid: 5.2%, Phenol: 3.1%" |
| 4 | Tam GC-MS veri paylasimi | Kromatogram + raw data repository |

---

## Degerlendirme Tablosu

| # | Makale | Yil | Dergi | Biyokutle | Veri Seviyesi | Bireysel Bilesen Sayisi | Olcum Tipi | Data Availability | Notlar |
|---|--------|-----|-------|-----------|---------------|------------------------|------------|-------------------|--------|
| 1 | Hu et al. | 2023 | JAAP | Bambu | 2 | 0 | Semi-kantitatif (a.u./mg) | "No data used" | Referans ornek |
| 2 | - | - | Appl. Sci. | - | - | - | - | - | ÇIKARILDI: Biochar çalışması, bio-oil değil |
| 3 | Zhang et al. | 2017 | Energy Conv. Mgmt. | Lignoselülozik | 3 | ~30 | Kantitatif (wt%) | Belirtilmemiş | İyi Level 3 örneği |
| 4 | Hwang et al. | 2013 | Bioresource Tech. | Çam talaşı | 3 | 44 | Kantitatif (wt%) | Belirtilmemiş | Mükemmel Level 3 |
| 5 | Kim et al. | 2012 | Renewable Energy | Pinus | 3 | 29 | Kantitatif (wt%) | Belirtilmemiş | İyi Level 3 |
| 6 | Su et al. | 2022 | Sci. Tot. Environ. | Gıda atığı | - | - | - | - | ÇIKARILDI: Review makale |
| 7 | Mullen et al. | 2009 | Energy & Fuels | Arpa biyokütlesi | 3 | 21 | Kantitatif (wt%) | Belirtilmemiş | Tablo 7: acetic acid 8.56% |
| 8 | Hussain et al. | 2016 | Waste Biomass Valor | Spirogyra (alg) | 3 | ~24 | Rel. konsantrasyon (%) | Belirtilmemiş | Tablo 6 detaylı |
| 9 | Leng et al. | 2021 | Bioresource Tech. | ML çalışması | - | - | - | - | ÇIKARILDI: Orijinal veri yok |
| 10 | Lachos-Perez et al. | 2023 | Analytica | - | - | - | - | - | ÇIKARILDI: Review makale |
| 11 | Bordoloi et al. | 2016 | Renewable Energy | Mikroalg (S. dimorphus) | 3 | ~20 | Area % | Belirtilmemiş | Supplementary Table 1 |
| 12 | Sukiran et al. | 2009 | Am. J. Appl. Sci. | Palmiye EFB | 3 | 11 | Area % | Belirtilmemiş | Tablo 3 detaylı |
| 13 | Chukwuneke et al. | 2019 | Heliyon | Maun ağacı | 3 | 24 | Area % | Belirtilmemiş | Tablo 5 GC-MS |
| 14 | Khor et al. | 2009 | Am. J. Appl. Sci. | Palmiye EFB | 3 | ~30 | Relative % | Belirtilmemiş | Yavaş piroliz |

---

## Ozet Istatistikler

**Degerlendirme Durumu:** 14 PDF tarandı, 10 tanesi uygun (orijinal araştırma)

| Metrik | Deger | Yorum |
|--------|-------|-------|
| Uygun makale sayısı | 10/14 | 4 tanesi review/ML/biochar - çıkarıldı |
| Seviye 1 (sadece verim) | 0/10 (0%) | - |
| Seviye 2 (sinif toplamlari) | 1/10 (10%) | Hu et al. 2023 |
| Seviye 3 (bireysel bilesenler) | 9/10 (90%) | Zhang, Hwang, Kim, Mullen, Hussain, Bordoloi, Sukiran, Chukwuneke, Khor |
| Seviye 4 (tam veri paylasimi) | 0/10 (0%) | Hiçbir makale raw GC-MS paylaşmıyor |
| Data Availability Statement var | 1/10 | Sadece Hu et al. (ama "No data used") |
| Kantitatif olcum (wt%) | 4/10 | 6 makale semi-kantitatif (area %, rel. %) |

### Kritik Bulgular
1. **Level 3 verisi yaygın (%90) ama Level 4 yok (%0)!** Makalelerin çoğu bireysel bileşen konsantrasyonlarını paylaşıyor, ancak hiçbiri ham GC-MS verilerini veya kromatogramları paylaşmıyor.

2. **Semi-kantitatif ölçüm sorunu:** 10 makaleden 6'sı sadece area % veya relative % veriyor. Bu değerler farklı çalışmalar arasında karşılaştırılamaz.

3. **Data Availability Statement eksikliği:** 10 makaleden sadece 1'inde var (o da "No data used" diyor).

4. **Biyokütle çeşitliliği iyi:** Odun, alg, palmiye EFB, tarımsal atık - farklı türler temsil ediliyor.

---

## Detayli Notlar (Her PDF icin)

### PDF 1: Hu et al. (2023) - 1-huEtAl.pdf
**Durum:** TAMAMLANDI (onceden analiz edilmis)
- **Dergi:** Journal of Analytical and Applied Pyrolysis
- **Biyokutle:** Bambu
- **Veri Seviyesi:** 2 (bilesik sinifi toplamlari)
- **Paylasilan:** Ultimate analysis, proximate analysis, compound-class totals (aromatics %, oxygenates %)
- **Paylasilmayan:** Bireysel bilesen konsantrasyonlari, GC-MS kromatogramlari
- **Data Availability:** "No data was used for the research described in the article"
- **Olcum Tipi:** Semi-kantitatif (a.u./mg peak area ratios)

### PDF 2: applsci-09-03980
**Durum:** ÇIKARILDI
- **Sebep:** Biochar çalışması, bio-oil kompozisyon verisi içermiyor
- **Not:** Listeye bio-oil odaklı başka makale eklenmeli

### PDF 3: Zhang et al. (2017) - Energy Conv. & Mgmt
**Durum:** TAMAMLANDI
- **Dergi:** Energy Conversion and Management
- **Biyokutle:** Lignoselülozik biyokütle
- **Veri Seviyesi:** 3 (bireysel bilesenler)
- **Paylasilan:** ~30 bireysel bilesen konsantrasyonu (wt%)
- **Data Availability:** Belirtilmemiş
- **Olcum Tipi:** Kantitatif (wt%)

### PDF 4: Hwang et al. (2013) - Bioresource Technology
**Durum:** TAMAMLANDI
- **Dergi:** Bioresource Technology
- **Biyokutle:** Çam talaşı (pine sawdust)
- **Veri Seviyesi:** 3 (bireysel bilesenler)
- **Paylasilan:** 44 bireysel bilesen konsantrasyonu (wt%)
- **Data Availability:** Belirtilmemiş
- **Olcum Tipi:** Kantitatif (wt%)
- **Not:** En yüksek bileşen sayısı - mükemmel Level 3 örneği

### PDF 5: Kim et al. (2012) - Renewable Energy
**Durum:** TAMAMLANDI
- **Dergi:** Renewable Energy
- **Biyokutle:** Pinus rigida (çam)
- **Veri Seviyesi:** 3 (bireysel bilesenler)
- **Paylasilan:** 29 bireysel bilesen konsantrasyonu (wt%)
- **Data Availability:** Belirtilmemiş
- **Olcum Tipi:** Kantitatif (wt%)

### PDF 6: Su et al. (2022) - Sci. Total Environ.
**Durum:** ÇIKARILDI
- **Sebep:** Review makale - gıda atığı pirolizi literatürünü derliyor
- **Not:** Orijinal deneysel veri yok, başka çalışmalardan derleme

### PDF 7: Mullen et al. (2009) - Energy & Fuels
**Durum:** TAMAMLANDI
- **Dergi:** Energy & Fuels
- **Biyokutle:** Arpa biyokütlesi (switchgrass, corn cobs, corn stover)
- **Veri Seviyesi:** 3 (bireysel bilesenler)
- **Paylasilan:** 21 bireysel bilesen - Tablo 7
  - Acetic acid: 8.56 wt%
  - Acetol: 6.31 wt%
  - Levoglucosan: 2.06 wt%
  - Phenol: 0.40 wt%
  - Guaiacol: 0.04 wt%
- **Data Availability:** Belirtilmemiş
- **Olcum Tipi:** Kantitatif (wt%)

### PDF 8: Hussain et al. (2016) - Waste Biomass Valor
**Durum:** TAMAMLANDI
- **Dergi:** Waste and Biomass Valorization
- **Biyokutle:** Spirogyra (tatlı su algi)
- **Veri Seviyesi:** 3 (bireysel bilesenler)
- **Paylasilan:** ~24 bireysel bilesen - Tablo 6
- **Data Availability:** Belirtilmemiş
- **Olcum Tipi:** Semi-kantitatif (relative concentration %)
- **Not:** Alg bazlı bio-oil - farklı biyokütle türü

### PDF 9: Leng et al. (2021) - biooilML
**Durum:** ÇIKARILDI
- **Sebep:** Makine öğrenmesi çalışması
- **Not:** Orijinal bio-oil kompozisyon verisi üretmiyor, literatürden derleme kullanıyor

### PDF 10: Lachos-Perez et al. (2023) - Analytica
**Durum:** ÇIKARILDI
- **Sebep:** Review makale - bio-oil upgrading teknikleri hakkında
- **Not:** Orijinal kompozisyon verisi içermiyor

### PDF 11: Bordoloi et al. (2016) - Renewable Energy
**Durum:** TAMAMLANDI
- **Dergi:** Renewable Energy
- **Biyokutle:** Scenedesmus dimorphus (mikroalg)
- **Veri Seviyesi:** 3 (bireysel bilesenler)
- **Paylasilan:** ~20+ bireysel bilesen - Supplementary Table 1
  - n-alkanes (C9-C22), aromatic compounds, phenolic compounds
  - 1H NMR hydrogen distributions (Table 3)
- **Data Availability:** Belirtilmemiş
- **Olcum Tipi:** Semi-kantitatif (area %)
- **Not:** Mikroalg bazlı bio-oil, fraksiyonasyon çalışması

### PDF 12: Sukiran et al. (2009) - Am. J. Applied Sciences
**Durum:** TAMAMLANDI
- **Dergi:** American Journal of Applied Sciences
- **Biyokutle:** Oil Palm Empty Fruit Bunches (EFB)
- **Veri Seviyesi:** 3 (bireysel bilesenler)
- **Paylasilan:** 11 bireysel bilesen - Tablo 3
  - Phenol: 18.10%
  - 2-methylphenol: 1.71%
  - 4-methylphenol: 2.69%
  - Phenol, 2-methoxy: 4.46%
- **Data Availability:** Belirtilmemiş
- **Olcum Tipi:** Semi-kantitatif (area %)
- **Not:** Malezya palmiye atığı çalışması

### PDF 13: Chukwuneke et al. (2019) - Heliyon
**Durum:** TAMAMLANDI
- **Dergi:** Heliyon
- **Biyokutle:** Swietenia macrophylla (maun ağacı)
- **Veri Seviyesi:** 3 (bireysel bilesenler)
- **Paylasilan:** 24 bireysel bilesen - Tablo 5
  - 2-methyldecane: 11.58%
  - 2,7-dimethyloctane: 10.55%
  - 2-methylnonane: 8.23%
  - 5-(1-methylethylidene): 8.05%
- **Data Availability:** Belirtilmemiş (Open Access makale)
- **Olcum Tipi:** Semi-kantitatif (area %)
- **Not:** Nijerya'dan egzotik odun türü

### PDF 14: Khor et al. (2009) - Am. J. Applied Sciences
**Durum:** TAMAMLANDI
- **Dergi:** American Journal of Applied Sciences
- **Biyokutle:** Oil Palm Empty Fruit Bunches (EFB)
- **Veri Seviyesi:** 3 (bireysel bilesenler)
- **Paylasilan:** ~30 bireysel bilesen - Tablo 3
  - Dodecanoic acid: 30.92%
  - Phenol: 11.68%
  - Tetradecanoic acid: 4.87%
  - Various phenol derivatives
- **Data Availability:** Belirtilmemiş
- **Olcum Tipi:** Semi-kantitatif (relative %)
- **Not:** Yavaş piroliz çalışması, diesel ile karışım özellikleri
