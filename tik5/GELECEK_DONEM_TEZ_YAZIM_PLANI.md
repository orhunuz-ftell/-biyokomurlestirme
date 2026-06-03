# Gelecek Dönemde Yapılacak Çalışmalar ve Doktora Tezi Yazım Planı

Tez çalışmasının araştırma, model geliştirme ve hesaplamalı uygulama aşamaları tamamlanmıştır. Bundan sonraki dönemde yürütülecek temel çalışma, önceki tüm tez izleme raporlarında sunulan çalışmaların bütüncül biçimde gözden geçirilmesi, elde edilen veri setlerinin, modellerin, sonuç tablolarının ve figürlerin doktora tezi formatında birleştirilmesi ve tezin nihai yazımının tamamlanması olacaktır.

Tez yazımında ilk aşama, TİK-1 raporunda sunulan literatür taraması, problem tanımı ve veri tabanı oluşturma çalışmalarının giriş ve literatür bölümlerine aktarılmasıdır. Bu bölümde biyokütle pirolizi, biyoyağ oluşumu, biyoyağ kompozisyonunun değişkenliği, biyoyağın katma değerli ürünlere dönüştürülme potansiyeli ve makine öğrenmesi yöntemlerinin bu alandaki kullanım gerekçesi sistematik biçimde ele alınacaktır. Böylece tez çalışmasının bilimsel problemi ve araştırma motivasyonu açık biçimde ortaya konacaktır.

İkinci aşamada, TİK-2 ve TİK-3 dönemlerinde geliştirilen veri işleme, veri temizleme, eksik veri yönetimi, özellik seçimi ve makine öğrenmesi modelleme çalışmaları yöntem bölümünün temelini oluşturacaktır. Bu kapsamda SQL Server tabanlı veri yapısı, biyokütle ve biyoyağ özelliklerinin düzenlenmesi, FTIR/kompozisyon verilerinin işlenmesi, Random Forest ve diğer temel makine öğrenmesi yaklaşımlarının denenmesi ve model performanslarının karşılaştırılması tezde ayrıntılı olarak açıklanacaktır.

Üçüncü aşamada, TİK-4 döneminde geliştirilen Cantera tabanlı biyoyağ buhar reforming veri seti ve ters makine öğrenmesi modeli tezin ana modelleme bölümüne dönüştürülecektir. Bu bölümde 30 biyoyağ kompozisyonu ve farklı reformer koşullarından üretilen simülasyon verileri, ters tahmin probleminin tanımı, model giriş-çıkış değişkenleri, MLP mimarisi, geleneksel modellerle karşılaştırma, ensemble denemeleri ve standart MLP modelinin test performansı birlikte sunulacaktır. Bu bölüm, tezin özgün katkılarından biri olan singaz kompozisyonundan biyoyağ kompozisyonuna geri giden ters tahmin yaklaşımını açıklayacaktır.

Dördüncü aşamada, TİK-5 döneminde tamamlanan soft-sensor, BiooilID bazlı validasyon, ileri surrogate model, statik optimizasyon ve MPC senaryosu tezin uygulama ve süreç optimizasyonu bölümünü oluşturacaktır. Bu bölümde ters ML modelinin proses izleme amacıyla soft-sensor olarak kullanılması, yeni biyoyağ kompozisyonlarına genelleme davranışının BiooilID bazlı test ile değerlendirilmesi, ileri surrogate modelin geliştirilmesi ve bu modelin optimizasyon/MPC döngüsünde kullanılması açıklanacaktır. Statik optimizasyon ve bozucu etki altındaki MPC senaryosu, geliştirilen yaklaşımın proses karar desteği sağlayabildiğini gösteren nihai uygulama örnekleri olarak sunulacaktır.

Son aşamada, bütün TİK raporlarında elde edilen bulgular tek bir tartışma ve sonuç çerçevesinde birleştirilecektir. Bu bölümde çalışmanın güçlü yönleri, model performansları, BiooilID bazlı validasyonla ortaya çıkan sınırlılıklar, H2/CO hedefinin bazı koşullarda tam yakalanamaması ve geliştirilen MPC yapısının hesaplamalı bir senaryo düzeyinde kalması açık biçimde tartışılacaktır. Bu sınırlılıklar, çalışmanın değerini azaltan unsurlar olarak değil, sonraki deneysel doğrulama ve veri genişletme çalışmalarına yön veren teknik bulgular olarak değerlendirilecektir.

## Tez Bölümlerine Aktarım Planı

| Tez bölümü | Kullanılacak temel kaynak | İçerik odağı |
|---|---|---|
| Giriş | TİK-1, TİK-2 | Problem tanımı, tez amacı, biyoyağ kompozisyon değişkenliği, yapay zeka ihtiyacı |
| Literatür Özeti | TİK-1, TİK-2, TİK-3 | Biyokütle pirolizi, biyoyağ karakterizasyonu, ML tabanlı biyokütle/biyoyağ çalışmaları |
| Materyal ve Yöntem | TİK-2, TİK-3, TİK-4 | Veri tabanı, veri ön işleme, Cantera simülasyonları, model giriş-çıkış yapıları |
| Makine Öğrenmesi Modelleri | TİK-3, TİK-4 | Random Forest, XGBoost, MLP, ensemble denemeleri, ters ML modeli |
| Soft-Sensor ve Validasyon | TİK-5 | Ters ML arayüzü, BiooilID bazlı validasyon, model genelleme sınırları |
| Optimizasyon ve MPC | TİK-5 | İleri surrogate model, statik optimizasyon, MPC senaryosu, bozucu etki analizi |
| Bulgular ve Tartışma | TİK-3, TİK-4, TİK-5 | Model performansları, optimizasyon sonuçları, sınırlılıklar ve teknik yorumlar |
| Sonuç ve Öneriler | Tüm TİK raporları | Tezin ana katkıları, tamamlanan çalışma, gelecek araştırma önerileri |

## TİK-5 Raporunda Kullanılabilecek B.3 Metni

Çalışmanın araştırma ve model geliştirme aşamaları bu dönem itibarıyla tamamlanmıştır. Önceki tez izleme dönemlerinde biyoyağ kompozisyonunun tahminine yönelik veri tabanı oluşturulmuş, veri ön işleme ve makine öğrenmesi modelleri geliştirilmiş, Cantera tabanlı reforming simülasyonları kullanılarak ters makine öğrenmesi modeli kurulmuş ve son dönemde bu model soft-sensor, optimizasyon ve model öngörülü kontrol yapısı içerisinde değerlendirilmiştir. Bu nedenle bir sonraki dönemde yeni bir model geliştirme veya yeni bir hesaplamalı senaryo oluşturma hedeflenmemektedir.

Bir sonraki dönemde yapılacak temel çalışma, bugüne kadar tamamlanan tüm tez izleme raporlarının, üretilen veri setlerinin, yazılım çıktılarının, model performans sonuçlarının, optimizasyon/MPC senaryolarının, tablo ve figürlerin doktora tezi bütünlüğü içinde yeniden düzenlenmesidir. Bu kapsamda TİK-1 döneminde oluşturulan literatür ve problem tanımı, TİK-2 ve TİK-3 dönemlerinde geliştirilen veri işleme ve ilk makine öğrenmesi modelleri, TİK-4 döneminde geliştirilen Cantera tabanlı ters makine öğrenmesi modeli ve TİK-5 döneminde tamamlanan soft-sensor, ileri surrogate model, optimizasyon ve MPC çalışmaları tek bir tez akışı altında birleştirilecektir.

Tez yazımında öncelikle giriş ve literatür bölümleri güncellenecek, ardından veri seti oluşturma, veri ön işleme, simülasyon altyapısı ve makine öğrenmesi yöntemleri ayrıntılı olarak yöntem bölümüne aktarılacaktır. Bulgular bölümünde önce biyoyağ kompozisyon tahmin modelleri, ardından ters makine öğrenmesi modeli, BiooilID bazlı validasyon, ileri surrogate model performansı, statik optimizasyon sonuçları ve MPC senaryosu sıralı olarak sunulacaktır. Sonuç bölümünde ise çalışmanın ana katkıları, modelin güçlü yönleri, sınırlılıkları ve gelecekte deneysel doğrulama/veri genişletme çalışmalarıyla nasıl ilerletilebileceği tartışılacaktır.

Bu doğrultuda gelecek dönemin hedefi, tamamlanan bilimsel ve teknik çalışmaları doktora tezinin nihai metnine dönüştürmek, tablo ve figürleri tez formatına uygun hale getirmek, kaynakça ve biçimsel düzenlemeleri tamamlamak ve tezi savunmaya hazır hale getirmektir.
