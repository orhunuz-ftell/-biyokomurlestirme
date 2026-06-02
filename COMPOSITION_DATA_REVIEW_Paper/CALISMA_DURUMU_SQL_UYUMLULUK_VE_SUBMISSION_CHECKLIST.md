# Bio-oil Composition Data Availability Review - Durum, SQL Uyumu ve Basvuru Checklisti

Tarih: 31 Mayis 2026

## 1. Kisa karar

Bu calisma icin en dogru ana hedef dergi su an **Bioresource Technology** gorunuyor. Gerekce: derginin kapsaminda bioresource teknolojileri, biomass/biological resources'in enerji, yakit, kimyasal ve materyale donusumu, termokimyasal surecler ve pyrolysis acikca yer aliyor.

Yedek hedefler:

- **Fuel**: Biofuels ve fuel science ekseni guclu; ancak review icin Editor-in-Chief ile on gorusme oneriliyor.
- **Energy Conversion and Management**: Review kabul ediyor; fakat SQL verisinin mevcut hali daha cok veri raporlama/standardizasyon problemi anlattigi icin ECM'ye ancak daha genis enerji sistemleri, modelleme ve optimizasyon baglami eklenirse daha iyi oturur.

## 2. Yerel dosyalarda ne yapilmis?

Calisma klasoru: `COMPOSITION_DATA_REVIEW_Paper/`

Bulunan aktif dosyalar:

- `DECISION_AND_PLAN.md`: senaryo secimi ve hedef dergi alternatifleri.
- `PROJECT_STATUS.md`: proje durum notlari.
- `README.md`: proje ozeti.
- `TODO.txt`: 6 fazli yol haritasi; Faz 1 baslamis, Faz 2 SQL/veritabani incelemesi henuz yapilmamis olarak isaretlenmis.
- `01_Literature_Assessment/LITERATURE_DATA_ASSESSMENT.md`: 14 PDF taramasi, 10 uygun makale uzerinden ilk degerlendirme.
- `01_Literature_Assessment/PDF_SELECTION.md`: `biyyag_ftir` klasorunden secilen PDF listesi.

Ayrica kok dizinde su dosya var:

- `SystematicLiteratureReview.docx`: yaklasik 3642 kelimelik anlatimli taslak. Baslik: "Systematic Literature Review: The State of Bio-Oil Composition Data Reporting and Stewardship in Biomass Pyrolysis Research".

Onemli eksik:

- `COMPOSITION_DATA_REVIEW_Paper/03_Manuscript_Drafts/` icinde teslim edilebilir bir manuscript taslagi bulunmadi.
- Mevcut Word taslagi okunabilir bir literatur anlatimi veriyor; fakat SQL verisine dogrudan baglanmis, tekrarlanabilir bir systematic review/metodoloji metni degil.

## 3. PDF taramasindan gelen mevcut bulgular

`LITERATURE_DATA_ASSESSMENT.md` dosyasindaki ilk tarama:

- Taranan PDF: 14
- Uygun orijinal arastirma makalesi: 10
- Level 1, sadece yield: 0/10
- Level 2, compound-class toplam: 1/10
- Level 3, individual compounds: 9/10
- Level 4, raw GC-MS/chromatogram veri paylasimi: 0/10
- Data availability statement: 1/10; Hu et al. icin "No data used" gibi zayif/uygunsuz ifade.
- Quantitative wt%: 4/10
- Semi-quantitative area% / relative%: 6/10

Bu bulgu ilk hipotezi degistiriyor. Eski tez "makalelerde individual compounds yok" seklindeyse zayif kaliyor. Daha dogru tez:

> Bio-oil calismalarinda bilesik isimleri veya siniflari siklikla raporlaniyor; asil kriz, ham GC-MS verisinin, makine-okunabilir tablolarin, nicel standardizasyonun, veri uygunluk beyanlarinin ve calismalar arasi karsilastirilabilirligin eksik olmasi.

## 4. SQL veritabanindan dogrulanan kapsam

Baglanilan veritabani: `BIOOIL`

Ana tablo sayilari:

- `Reference`: 19
- `Experiment`: 110
- `Biomass`: 51
- `Biooil`: 70
- `Biooil_Mutlak`: 18

`Biooil` tablosu:

- 70 satirin tamami `Experiment` ile bagli.
- `Biooil -> Experiment -> Biomass -> Reference` join'inde 14 farkli referans var.
- 43 farkli biomass adi gorunuyor.
- Pyrolysis process temperature araligi: 300-850 degC.

Referans dagilimi:

- Hu et al. 2023, Journal of Analytical and Applied Pyrolysis: 18 satir.
- Sampaio et al. 2025, Journal of Analytical and Applied Pyrolysis review: 12 satir.
- Cao et al. 2021: 7 satir.
- Zhang et al. 2017, Energy Conversion and Management: 5 satir.
- Hwang et al. 2013, Bioresource Technology: 5 satir.
- Wang et al. 2018, Bioresource Technology: 5 satir.
- Chen et al. 2016, Bioresource Technology: 4 satir.
- Chen et al. 2017, Bioresource Technology: 4 satir.
- Digerleri: 1-3 satir.

Dikkat edilmesi gereken kritik nokta:

- SQL'deki 12 satir Sampaio et al. 2025 gibi bir review kaynagindan geliyor. Bir "primary experimental evidence" analizi yapilacaksa bu kayitlar ayri isaretlenmeli veya ana analizden ayrilmalidir.

## 5. SQL verisine gore kompozisyon eksiklikleri

`Biooil` tablosunda 70 satir uzerinden eksiklik:

| Degisken | Dolu | Eksik | Eksik % |
|---|---:|---:|---:|
| catechol | 5 | 65 | 92.9 |
| guaiacol | 5 | 65 | 92.9 |
| syringol | 5 | 65 | 92.9 |
| N-containing | 7 | 63 | 90.0 |
| oxides | 23 | 47 | 67.1 |
| esters | 30 | 40 | 57.1 |
| sugar | 36 | 34 | 48.6 |
| alcohols | 42 | 28 | 40.0 |
| aliphatichydrocarbon | 43 | 27 | 38.6 |
| aromatics | 51 | 19 | 27.1 |
| furans | 56 | 14 | 20.0 |
| aldehyde_ketone | 60 | 10 | 14.3 |
| acids | 68 | 2 | 2.9 |
| phenols | 69 | 1 | 1.4 |

Ek SQL kontrolleri:

- 6 cekirdek grup tam olan satir: 30/70.
- 10 ana class alaninin tamami dolu olan satir: 0/70.
- Guaiacol/syringol/catechol/N-containing alanlarindan en az biri dolu olan satir: 12/70.
- `Biooil` satirlarinda kompozisyon toplami, NULL degerler 0 kabul edilince: min 11.07, max 103.49, ortalama 87.82.
- `Biooil_Mutlak` 18 satirda tum 12 alan dolu; fakat toplamlar min 30.94, max 48.64, ortalama 39.87. Bu tablo da tam bio-oil kompozisyonu degil, sinif/subclass toplamlari gibi davranmali.

Bu nedenle SQL'e sadik bir makale su iddiayi kurabilir:

- "70 bio-oil composition record from 14 references" var.
- Veri cogunlukla class-level/subclass-level.
- Ham GC-MS veya sistematik bireysel bilesik matrisi yok.
- Eksiklik ve standardizasyon sorunu cok guclu.
- Kompozisyon toplamlari 100'e normalize olmayan, parcali raporlama niteliginde.

Bu iddialar SQL ile desteklenmez:

- "Complete compound-level bio-oil database olusturduk."
- "Ham GC-MS veya chromatogram verisi toplandi."
- "Tum literature corpus nicel ve karsilastirilabilir."
- "Bio-oil composition verisi yok" gibi fazla genel iddia. Daha dogru iddia: veri var, ama yeniden kullanilabilirlik ve standardizasyon eksik.

## 6. Mevcut Word taslaginin durumu

`SystematicLiteratureReview.docx` iyi bir anlatimli iskelet sagliyor:

- Data reporting/stewardship problemi kurulmus.
- Level 0-5 gibi bir raporlama seviyesi siniflandirmasi var.
- Semi-quantitative reporting, invisible fraction, advanced characterization ve data stewardship basliklari var.

Ancak teslim edilebilir manuscript degil:

- SQL'deki 70 satirlik veri ve 14 referansla dogrudan bag kurmuyor.
- 14 PDF/10 uygun makale taramasinin sayisal sonucunu metne sistematik sekilde gommemis.
- Metindeki bazi ornekler yerel SQL/PDF corpus disindan gorunuyor; bunlar tek tek dogrulanmadan ana kanit gibi kullanilmamali.
- "Level 5 / gold standard" anlatimi guclu, fakat mevcut yerel veri bu seviyede degil. Bu kisim ideal framework/recommendation olarak kalmali.

## 7. Onerilen SQL-sadik makale ekseni

Onerilen baslik:

**From Reported Compounds to Reusable Data: A SQL-Curated Review of Bio-Oil Composition Reporting in Biomass Pyrolysis Research**

Alternatif baslik:

**The State of Bio-Oil Composition Data Reporting in Biomass Pyrolysis: Evidence from a Curated SQL Dataset and Systematic Literature Assessment**

Onerilen ana mesaj:

> Biomass pyrolysis literature often reports bio-oil composition, but the reporting is rarely reusable as harmonized, machine-readable, quantitative data. A curated SQL dataset of 70 class-level bio-oil composition records shows severe missingness, inconsistent normalization, limited individual-marker coverage, and no raw-data layer; therefore the key barrier for ML and cross-study synthesis is data stewardship, not only data scarcity.

Onerilen makale yapisi:

1. Introduction: bio-oil composition neden ML/modelleme icin kritik?
2. Review question and evidence base: PDF tarama + SQL dataset.
3. Reporting-level framework: Level 1-4 veya 0-5, fakat SQL'e uyarlanmis.
4. SQL dataset description: 70 Biooil, 18 Biooil_Mutlak, 14 referans, 43 biomass, 300-850 degC.
5. Missingness and comparability results.
6. Case-level literature assessment: 10 uygun makaleden gelen reporting-level sonuclari.
7. Data stewardship gaps: raw GC-MS, data availability statement, units, normalization, class mapping.
8. Recommendations: minimum reporting checklist.
9. Limitations: corpus henuz sinirli; secondary-source rows ayrilmali; SQL class-level.
10. Conclusion.

Maksimum 6 tablo/figur siniri dikkate alinarak Bioresource Technology icin onerilen gorsel set:

1. PRISMA-benzeri PDF secim akisi.
2. Reporting-level framework semasi.
3. SQL veri modeli ve kapsam tablosu.
4. `Biooil` missingness heatmap.
5. Composition sum distribution.
6. Minimum reporting checklist tablosu.

## 8. Bioresource Technology basvuru gereksinimleri

Resmi kaynak:

- Guide for Authors: https://www.sciencedirect.com/journal/bioresource-technology/publish/guide-for-authors
- Submit linki ScienceDirect sayfasindan Editorial Manager'a gider: https://www.editorialmanager.com/bite/default.aspx

Uygunluk:

- Dergi original research, review articles, case studies ve short communications yayinlar.
- Kapsamda biofuels/bioenergy, thermochemical conversion, pyrolysis, gasification, catalytic upgrading ve systems analysis/modeling var.

Hakemlik:

- Double anonymized peer review.
- Title page ve anonymized manuscript ayri dosya olmalidir.
- Anonymized manuscript author names, affiliations ve acknowledgements icermemelidir.

Dosya formati:

- Tum submission icin editable source files istenir.
- Word icin `.doc/.docx`, LaTeX icin `.tex`.
- PDF source file olarak kabul edilmez.
- Word single-column olmali.

Title page icerigi:

- Article title.
- Author names.
- Affiliations.
- Corresponding author full address ve email.
- Present/permanent address varsa.
- Acknowledgements sadece title page'de.
- Declaration of competing interests, ayri dosya verilmezse title page'de.

Abstract ve keywords:

- Abstract en fazla 250 kelime.
- Structured abstract kullanilmali.
- 1-7 keyword.
- Keyword'lerde "and/of" iceren uzun ifadelerden kacinilmasi oneriliyor.

Highlights:

- Zorunlu.
- Ayri editable file olarak yuklenmeli.
- Dosya adinda `highlights` gecmeli.
- 3-5 bullet.
- Her bullet en fazla 85 karakter.

Graphical abstract:

- Zorunlu.
- Ayri dosya olarak yuklenmeli.
- En az 531 x 1328 px (h x w) veya oransal olarak daha buyuk.
- 5 x 13 cm boyutta okunabilir olmali.
- Tercih edilen formatlar: TIFF, EPS, PDF veya MS Office.
- Dis kaynak/web imaji kullanilmamali; kendi grafiklerin olusturulmasi oneriliyor.
- Elsevier politikasi geregi submitted manuscript artwork veya graphical abstract uretiminde generative AI kullanimi kabul edilmiyor.

Units, tables, figures:

- SI units kullanilmali.
- Tables editable text olmali; image olarak verilmemeli.
- Figures/images/artwork ayri dosyalar olarak verilmeli.
- Figure captions gerekli.
- Halftone/color image icin 300 dpi, line drawing icin 1000 dpi, combination figure icin 500 dpi oneriliyor.

Journal-specific formatting:

- Title'da acronym kullanmaktan kacin.
- Introduction en fazla 3 sayfa.
- Research article en fazla 35 sayfa.
- Review article en fazla 50 sayfa.
- Short communication en fazla 15 sayfa.
- Font size 12.
- Tum bolumler, references dahil double-spaced.
- Maksimum 6 figure/table.
- Conclusion yaklasik 250 kelime.
- Non-English references kullanma.
- References alfabetik siralanmali.
- Heading/subheading'lerde acronym kullanmaktan kacin.
- Self-citation 3 calismayi asmamali; asarsa gerekce verilmeli.
- Tables/Figures ana metne gomulmemeli; her biri ayri sayfada verilmeli.
- Tum data istatistiksel olarak analiz edilmeli ve karsilastirilmali; figure'lerde error bar, table'larda SD beklenir. Review paper icin bu madde, SQL-derived descriptive statistics ve tarama oranlari icin net metrikler verilmesi seklinde yorumlanmali.

Research data ve data statement:

- Bioresource Technology icin research data policy Option B: data repository'ye deposit etmek, dataset'i cite/link etmek tesvik ediliyor.
- Data availability statement tesvik ediliyor.
- Data repository varsa submission sirasinda link verilmeli.
- Bu calisma icin en uygun paket: SQL export CSV/XLSX, data dictionary, inclusion/exclusion table, extraction protocol, analysis notebook/script.

Supplementary material:

- Supplementary material manuscript ile ayni anda yuklenmeli.
- Main text icinde cite edilmeli.
- Her supplementary file icin kisa caption/description verilmeli.
- Supplementary files production tarafindan formatlanmaz; yuklendigi gibi online gorunur.

References:

- Text icindeki tum atiflar reference list'te olmali ve tersi.
- Web references icin URL ve access date verilmeli.
- Dataset references icin author, title, repository, version, year ve persistent identifier verilmeli.
- Dataset referansinin basina `[dataset]` eklenmesi oneriliyor.

Submission checklist:

- Corresponding author atanmis olmali.
- Corresponding author email, full postal address ve phone details girilmeli.
- Keywords, figure captions, tables, supplementary files ve video varsa tum dosyalar yuklenmeli.
- Spelling/grammar kontrolu yapilmali.
- Text-reference ve reference-list eslesmesi kontrol edilmeli.
- Copyright material icin izin alinmali.
- Open access secilirse APC sorumlulugu yazarlarca bilinmeli.

Etik ve beyanlar:

- Submission declaration: calisma daha once yayinlanmamis, baska yerde degerlendirmede degil, tum yazarlar onaylamis olmali.
- Competing interests declaration gerekli.
- Funding statement gerekli; fon yoksa fon olmadigi belirtilmeli.
- CRediT author contribution statement hazirlanmali.
- Generative AI kullanildiysa beyan edilmeli. Bu proje eski Claude modeli ve Codex destegi gordugu icin manuscript hazirlik surecinde AI-assisted drafting/review kullanimi seffaf bicimde beyan edilmelidir.
- Human/animal subject yoksa ilgili etik onay gerekmez; yine de "Not applicable" beyanlari hazir tutulabilir.

## 9. Fuel icin kisa resmi gereksinim ozeti

Resmi kaynak:

- https://www.sciencedirect.com/journal/fuel/publish/guide-for-authors

Notlar:

- Fuel biofuels ve sustainable fuels kapsaminda uygun olabilir.
- Review article hazirlamadan once Editor-in-Chief ile onerilen review konusunda gorusmek tavsiye ediliyor.
- Single anonymized peer review.
- Abstract en fazla 250 kelime.
- 1-7 keyword.
- Highlights zorunlu: 3-5 bullet, her biri en fazla 85 karakter.
- Graphical abstract tesvik ediliyor, zorunlu degil.
- Research data policy Option C: data repository'ye deposit etmek ve makalede cite/link etmek gerekli; mumkun degilse neden paylasilamadigi aciklanmali.
- Data availability statement zorunlu.

Fuel icin strateji:

- "Fuel science / biofuel quality / pyrolysis oil compositional comparability" vurgusu gerekir.
- Review baslamadan once editor'e kisa proposal/cover inquiry yazmak mantikli.

## 10. Energy Conversion and Management icin kisa resmi gereksinim ozeti

Resmi kaynak:

- https://www.sciencedirect.com/journal/energy-conversion-and-management/publish/guide-for-authors

Notlar:

- Original research papers ve Review articles kabul ediyor.
- Single anonymized peer review.
- Cover Letter basligi submission menulerinde ayrica listelenmis.
- Abstract en fazla 250 kelime.
- 1-7 keyword.
- Highlights zorunlu: 3-5 bullet, her biri en fazla 85 karakter.
- Graphical abstract tesvik ediliyor, zorunlu degil.
- Research data policy Option C: data repository'ye deposit etmek ve makalede cite/link etmek gerekli; mumkun degilse neden paylasilamadigi aciklanmali.
- Data availability statement zorunlu.

ECM icin strateji:

- Mevcut SQL veri seti tek basina ECM icin dar kalabilir.
- Makale enerji sistemleri, conversion modeling, optimization, ML-ready datasets ve process decision-making eksenine genisletilirse daha iyi konumlanir.

## 11. Hemen yapilacak isler

1. Corpus'u dondur: Hangi PDF'ler ve hangi SQL referanslari ana analize dahil?
2. `Reference` tablosunda primary experimental paper ile review/secondary source ayrimi ekle.
3. `Biooil` ve `Biooil_Mutlak` icin exportable CSV/XLSX cikart.
4. Data dictionary hazirla: her class/subclass alaninin tanimi, unit, NULL anlami, source extraction rule.
5. Composition sum, missingness ve source-level completeness metriklerini script ile tekrarlanabilir hale getir.
6. `SystematicLiteratureReview.docx` metnini SQL bulgularina gore yeniden yaz; SQL ile desteklenmeyen genis iddialari recommendation/framework kismina tasi.
7. Bioresource Technology icin 50 sayfa / 6 figure-table sinirina gore manuscript'i daralt.
8. Repository paketi hazirla: CSV, data dictionary, extraction protocol, analysis script, README.
9. Data availability statement ve generative AI declaration yaz.
10. Highlights, structured abstract ve graphical abstract'i Bioresource Technology formatina gore hazirla.

