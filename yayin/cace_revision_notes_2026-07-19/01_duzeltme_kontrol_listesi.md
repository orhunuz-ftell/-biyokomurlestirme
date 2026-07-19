# Düzeltme Kontrol Listesi

## A. Gönderimi engelleyen kritik işler

- [ ] Başlık sayfası ekle: makale başlığı, tüm yazarlar, kurumlar, corresponding author e-posta/adres/telefon bilgisi.
- [ ] Abstract ekle: en fazla 250 kelime, referanssız, amaç-yöntem-sonuç-sonuç cümlesi içeren tek parça metin.
- [ ] 1-7 adet İngilizce keyword ekle.
- [ ] Ayrı `highlights` dosyası hazırla: 3-5 madde, her madde en fazla 85 karakter.
- [ ] `References` bölümü oluştur; metindeki tüm atıflar listeye, listedeki tüm kaynaklar metne bağlanmalı.
- [ ] Atıf biçimini tekleştir: C&CE author-year kullanıyor; `[Zhang et al., 2017]` yerine `(Zhang et al., 2017)`.
- [ ] Şekilleri gerçekten ekle veya ayrı dosya olarak yüklemeye hazırla. Mevcut DOCX içinde 11 şekil başlığına karşılık yalnızca 1 gömülü görsel tespit edildi.
- [ ] `B.2.2`, `End-of-Term Study Results`, `previous thesis study period` gibi tez/TİK izlerini kaldır.
- [ ] `Data availability`, `Declaration of competing interests`, `Funding`, `CRediT author statement` ve gerekirse `Declaration of generative AI...` bölümlerini ekle.

## B. Bilimsel savunmayı güçlendiren işler

- [ ] Row-wise split ile BiooilID/group-based split arasındaki farkı açıkça yaz.
- [ ] Aynı BiooilID'nin farklı proses koşulları train ve test setlerine düşebileceği için data leakage/interpolation riski tartışılmalı.
- [ ] BiooilID holdout sonucunu ek bir genelleme denetimi olarak ver; bunu doğrudan nihai MLP validasyonu gibi sunma, eğer MLP ile yeniden çalıştırılmadıysa.
- [ ] Cantera equilibrium varsayımının sınırlarını açıkla: model deneysel reaktör davranışını değil, Cantera veri uzayını temsil ediyor.
- [ ] 30 bio-oil kompozisyonu, 3,150 Cantera senaryosu ve 1,350 temiz model-ready sample arasındaki ilişkiyi netleştir.
- [ ] Surrogate molekül seçimlerini ayrı bir tabloyla gerekçelendir: toluene, acetic acid, ethanol, furan, phenol, acetone.
- [ ] MLP, constrained MLP, RF, XGBoost ve ensemble metrikleri için tek bir nihai kaynak dosya seç; farklı dosyalardaki küçük/büyük farkları çöz.
- [ ] "First in the literature" iddiasını yumuşat: "To the best of our knowledge..." kullan ve karşılaştırmalı literatür tablosu ekle.

## C. Dil ve yapı düzeltmeleri

- [ ] Giriş bölümündeki genel bio-oil kullanım alanları kısmını kısalt. C&CE odağı process systems, soft sensor, simulation, inverse ML ve monitoring olmalı.
- [ ] Uzun paragrafları böl; her paragraf tek bir teknik mesaj taşısın.
- [ ] "very interesting", "actually", "excellent", "perfect generalization" gibi sübjektif ifadeleri çıkar.
- [ ] "No overfitting" ifadesini row-wise split ile sınırlandır: "No row-wise validation/test gap was observed."
- [ ] "Deep learning is far superior" yerine ölçülü ifade kullan: "The MLP outperformed the tested baseline models under the row-wise split."
- [ ] "Experimentally shown" ifadesini kullanma; bu çalışma deneysel doğrulama değil, simülasyon ve ML tabanlı hesaplamalı çalışmadır.
- [ ] Tüm birimleri SI biçiminde ve tutarlı ver: degC yerine °C, wt.%, mol%, bar açıklamaları.

## D. Şekil ve tablo düzeltmeleri

- [ ] Ana makale için 5-7 güçlü şekil seç; kalan şekilleri supplementary yap.
- [ ] Her şekli `Figure_1.png`, `Figure_2.png` gibi mantıklı adla hazırla.
- [ ] Her şekil metinde ilk geçtiği sıraya göre numaralandırılmalı.
- [ ] Şekil altyazılarını ayrı dosyada da hazırla.
- [ ] Tablolar editable text olarak kalmalı; tablo ekran görüntüsü olarak verilmemeli.
- [ ] Sonuçlar metinde, tabloda ve şekilde aynı sayılarla geçmeli.

## E. Gönderim öncesi son kontrol

- [ ] Track changes kapalı olmalı.
- [ ] Word spell/grammar check yapılmalı.
- [ ] Referans alan kodları kaldırılmalı veya Mendeley/Zotero çıktısı finalize edilmeli.
- [ ] Web kaynakları için erişim tarihi eklenmeli.
- [ ] Veri deposu DOI/URL eklenecekse Data Availability ve Reference listesine işlenmeli.
- [ ] Tüm şekillerin çözünürlüğü ve okunabilirliği kontrol edilmeli.

