# DOKTORA TEZ İZLEME RAPORU-5

## A. TEZ PROJESİNE İLİŞKİN GENEL BİLGİLER

### A.1 Tezin Adı

### A.2 Tez Danışmanı ve Yürütücüsü

### A.3 Tezin Yürütüldüğü Anabilim Dalı

### A.4 Tezin Yürütülmesinde İş Birliği Yapılacak Kurum ve Kuruluşlar

### A.5 Tezin Başlangıç ve Bitiş Tarihi

## B. TEZİN PLANLANMASI VE YAPILAN ÇALIŞMALAR

Bu dönem içerisinde yapılan çalışma, önceki tez izleme döneminde geliştirilen ters makine öğrenmesi modelinin süreç optimizasyonu ve model öngörülü kontrol yapısı içerisinde kullanılmasına odaklanmıştır. Önceki çalışmada, biyoyağ buhar reforming prosesi için reformer çıkışındaki singaz kompozisyonundan girişte kullanılan biyoyağın kimyasal kompozisyonunu tahmin eden bir derin öğrenme modeli geliştirilmişti. Bu dönemde ise bu model, tek başına bir tahmin aracı olarak değil, prosesin izlenmesi ve uygun çalışma koşullarının belirlenmesi için kullanılan bir soft-sensor bileşeni olarak ele alınmıştır.

Çalışmanın temel amacı, ölçülen veya simülasyonla elde edilen singaz kompozisyonundan biyoyağ bileşimini tahmin etmek ve bu tahmini kullanarak hedeflenen H2/CO oranına mümkün olduğunca yaklaşan, enerji açısından daha uygun reformer çalışma koşullarını belirleyen bir optimizasyon ve model öngörülü kontrol yapısı oluşturmaktır. Bu kapsamda reformer sıcaklığı, basınç ve buhar/karbon oranı karar değişkenleri olarak seçilmiş; biyoyağ kompozisyonu ise ters makine öğrenmesi modeli tarafından tahmin edilen sabit proses girdisi olarak değerlendirilmiştir.

Bu dönemde yapılan çalışma dört ana aşamada yürütülmüştür. İlk aşamada, mevcut ters makine öğrenmesi modeli kullanıma hazır bir tahmin arayüzüne dönüştürülmüştür. İkinci aşamada, modelin genelleme kabiliyetini daha gerçekçi biçimde değerlendirmek için BiooilID bazlı ek validasyon yapılmıştır. Üçüncü aşamada, optimizasyon ve MPC hesaplamalarında Cantera simülasyonlarını tekrar tekrar çalıştırmak yerine hızlı sonuç verebilecek ileri bir surrogate model geliştirilmiştir. Son aşamada ise statik optimizasyon ve basit bir MPC senaryosu oluşturularak sistemin farklı biyoyağ kompozisyonları ve bozucu etkiler altında nasıl davrandığı incelenmiştir.

Bu bölümde sırasıyla önceki çalışmanın bu döneme nasıl temel oluşturduğu, geliştirilen soft-sensor yapısı, BiooilID bazlı validasyon, ileri surrogate model, optimizasyon problemi, statik optimizasyon sonuçları ve MPC senaryosu açıklanacaktır. Çalışma sonunda elde edilen tablolar ve figürler, geliştirilen sistemin hem tahmin hem de kontrol/optimizasyon açısından uygulanabilirliğini göstermek amacıyla rapora eklenmiştir.

**Bu bölümde kullanılacak tablo ve figürler:**

Tablo B.1. Bu dönem geliştirilen yazılım modülleri ve görevleri  
Tablo B.2. Ters ML, ileri surrogate model, optimizasyon ve MPC bileşenlerinin girdi-çıktı yapısı  
Şekil B.1. Ters ML destekli optimizasyon ve MPC genel sistem mimarisi  
Şekil B.2. Bu dönem izlenen çalışma akışı

### B.1 Tezin Amacı

### B.2 Dönem İçerisinde Yapılan Çalışmalar

Bu doktora tez çalışmasının önceki dönemlerinde, biyokütleden piroliz yoluyla elde edilen biyoyağın kompozisyonunu tahmin etmeye yönelik veri tabanı oluşturma, veri ön işleme, makine öğrenmesi modeli geliştirme ve biyoyağın buhar reforming prosesiyle hidrojen üretiminde değerlendirilmesine yönelik modelleme çalışmaları gerçekleştirilmiştir. Önceki tez izleme döneminde, Cantera tabanlı reforming simülasyonlarından elde edilen veri seti kullanılarak reformer çıkışındaki singaz kompozisyonundan giriş biyoyağ kompozisyonunu tahmin eden ters makine öğrenmesi modeli geliştirilmiştir. Bu modelde reformer sıcaklığı, basınç, buhar/karbon oranı ve H2, CO, CO2, CH4, H2O mol yüzdeleri giriş değişkenleri olarak; aromatikler, asitler, alkoller, furanlar, fenoller ve aldehit-ketonlar ise çıkış değişkenleri olarak kullanılmıştır.

Bu dönem içerisinde yapılan çalışmada, söz konusu ters tahmin modeli süreç optimizasyonu ve model öngörülü kontrol yapısında kullanılabilecek şekilde yeniden ele alınmıştır. Bu amaçla ilk olarak mevcut MLP modeli için bir tahmin arayüzü hazırlanmış, modelin giriş ve çıkış değişkenleri standart hale getirilmiş ve model tekil ya da çoklu ölçüm verisiyle çalışabilecek biçimde düzenlenmiştir. Böylece reformer çıkışındaki anlık singaz kompozisyonuna bakılarak biyoyağ kompozisyonu hesaplanabilir hale getirilmiştir.

İkinci aşamada, önceki dönemde elde edilen model başarısının daha ayrıntılı değerlendirilmesi için BiooilID bazlı validasyon yapılmıştır. Önceki sonuçlarda train, validation ve test ayrımı satır bazında yapıldığından aynı biyoyağın farklı proses koşullarındaki örnekleri hem eğitim hem de test kümelerinde bulunabilmekteydi. Bu durum, modelin farklı proses koşullarına karşı başarısını göstermekte, ancak hiç görmediği yeni bir biyoyağ kompozisyonuna genelleme kabiliyetini doğrudan ölçmemektedir. Bu nedenle bu dönem içinde bazı biyoyağlar tamamen test setinde bırakılmış ve model performansı bu daha zor koşul altında ayrıca incelenmiştir.

Üçüncü aşamada, MPC ve optimizasyon hesaplamalarında kullanılmak üzere ileri bir surrogate model geliştirilmiştir. Bu model, biyoyağ kompozisyonu ve proses koşullarından reformer çıkışındaki singaz kompozisyonunu tahmin etmektedir. Böylece optimizasyon algoritması, her aday sıcaklık, basınç ve buhar/karbon oranı için Cantera simülasyonunu yeniden çalıştırmak yerine hızlı çalışan bir makine öğrenmesi modeli üzerinden proses çıktısını hesaplayabilmektedir. Bu yaklaşım, MPC döngüsünün hesaplama süresini azaltmak ve çok sayıda aday proses koşulunun pratik biçimde değerlendirilmesini sağlamak için kullanılmıştır.

Son aşamada, hedef H2/CO oranını yakalamaya ve enerji/operasyon maliyeti vekil fonksiyonunu minimize etmeye yönelik optimizasyon problemi kurulmuştur. Karar değişkenleri reformer sıcaklığı, basınç ve buhar/karbon oranı olarak belirlenmiştir. Geliştirilen yapı önce statik optimizasyon senaryolarında test edilmiş, daha sonra zaman adımlı basit bir MPC senaryosu oluşturulmuştur. MPC senaryosunda her adımda singaz kompozisyonu ölçülmüş, ters ML modeliyle biyoyağ kompozisyonu tahmin edilmiş, ileri surrogate model kullanılarak aday kontrol hamleleri değerlendirilmiş ve bir sonraki adım için uygun T, P ve S/C değerleri hesaplanmıştır.

Bu bölümde verilen çalışmalar, önceki dönemde geliştirilen ters makine öğrenmesi modelinin proses izleme, optimizasyon ve kontrol amaçlı kullanılabileceğini göstermektedir. Böylece tez çalışması yalnızca biyoyağ kompozisyonunu tahmin eden bir model geliştirme aşamasından, bu tahmini proses kararlarına dönüştüren bir kontrol ve optimizasyon çerçevesine ilerletilmiştir.

**Bu alt bölümde kullanılacak tablo ve figürler:**

Tablo B.1. Bu dönem gerçekleştirilen ana çalışma adımları  
Tablo B.2. Geliştirilen yazılım dosyaları ve işlevleri  
Şekil B.1. Ters ML soft-sensor, ileri model, optimizasyon ve MPC bileşenlerinden oluşan genel sistem yapısı

#### B.2.1 Önceki Çalışmanın Kısa Özeti ve Bu Dönemin Başlangıç Noktası

Önceki tez izleme döneminde, biyoyağ buhar reforming prosesi için ters yönde çalışan bir makine öğrenmesi yaklaşımı geliştirilmiştir. Bu yaklaşımda amaç, biyoyağ kompozisyonundan singaz kompozisyonunu tahmin etmek değil; reformer çıkışında elde edilen singaz kompozisyonuna ve bilinen proses koşullarına bakarak girişte kullanılan biyoyağın bileşimini tahmin etmektir. Bu nedenle model, proses çıktılarından hammadde karakteristiğine geri giden ters bir tahmin modeli olarak değerlendirilmiştir.

Bu amaçla öncelikle literatürden ve mevcut veri tabanından elde edilen biyoyağ kompozisyonları kullanılmış, biyoyağ altı ana bileşen grubuyla temsil edilmiştir. Bu bileşen grupları aromatikler, asitler, alkoller, furanlar, fenoller ve aldehit-ketonlar olarak belirlenmiştir. Her bir biyoyağ kompozisyonu, farklı reformer sıcaklığı, basınç ve buhar/karbon oranı koşulları altında Cantera ile simüle edilmiş ve reformer çıkışında oluşan H2, CO, CO2, CH4 ve H2O mol yüzdeleri hesaplanmıştır. Bu şekilde biyoyağ kompozisyonu ile reformer çıkışındaki singaz kompozisyonu arasında makine öğrenmesi modelinin kullanabileceği bir veri seti oluşturulmuştur.

Önceki dönemde bu veri seti üzerinde doğrusal regresyon, Random Forest, XGBoost, standart çok katmanlı yapay sinir ağı ve kısıtlı çıkışlı yapay sinir ağı gibi farklı modeller denenmiştir. Model karşılaştırmaları sonucunda standart çok katmanlı yapay sinir ağı en başarılı yöntem olarak belirlenmiştir. Standart MLP modeli 8 giriş değişkeni ve 6 çıkış değişkeniyle eğitilmiş; test setinde ortalama R2=0.863 ve ortalama MAE=%4.03 performansına ulaşmıştır. Bileşen bazında aromatikler, asitler, alkoller, furanlar, fenoller ve aldehit-ketonlar için elde edilen performans değerleri, ters tahmin yaklaşımının uygulanabilir olduğunu göstermiştir.

Bu dönemin başlangıç noktası, önceki dönemde elde edilen bu ters makine öğrenmesi modelidir. Ancak bu dönemde model yalnızca bir tahmin aracı olarak kullanılmamış, proses kontrol ve optimizasyon yapısının bir bileşeni haline getirilmiştir. Reformer çıkışındaki singaz kompozisyonu pratik olarak daha hızlı ölçülebilen bir proses çıktısı olduğundan, bu veriden biyoyağ kompozisyonunu tahmin etmek prosesin anlık durumunu izlemek açısından önemlidir. Bu nedenle mevcut MLP modeli, bu dönem geliştirilen MPC yapısında biyoyağ kompozisyonunu tahmin eden soft-sensor olarak konumlandırılmıştır.

Bu başlangıç noktasından hareketle bu dönemde iki temel ihtiyaç ortaya çıkmıştır. Birincisi, ters ML modelinin gerçekçi kullanım için bir tahmin arayüzüne dönüştürülmesi ve modelin hiç görmediği biyoyağlara karşı davranışının ayrıca incelenmesidir. İkincisi ise, tahmin edilen biyoyağ kompozisyonunu kullanarak proses koşullarını optimize edebilecek ileri bir proses modelinin oluşturulmasıdır. Bu nedenle çalışma, ters modelin soft-sensor olarak kullanılması, ileri surrogate modelin geliştirilmesi, optimizasyon probleminin kurulması ve MPC senaryosunun oluşturulması aşamalarından oluşmuştur.

Önceki dönemden bu döneme geçişin temel mantığı Şekil B.2'de gösterilecektir. Önceki dönemde geliştirilen ters model, singazdan biyoyağ kompozisyonu tahmini üretmektedir. Bu dönemde ise bu tahmin, ileri model ve optimizasyon bloğuna aktarılmakta; böylece hedef H2/CO oranına yaklaşan uygun reformer çalışma koşulları hesaplanmaktadır.

**Bu alt bölümde kullanılacak tablo ve figürler:**

Tablo B.3. Önceki dönemde geliştirilen ters ML modelinin girişleri, çıkışları ve performans özeti  
Şekil B.2. Önceki dönem ters tahmin modelinden bu dönem MPC/optimizasyon yapısına geçiş akışı

#### B.2.2 Ters Makine Öğrenmesi Modelinin Soft-Sensor Olarak Kullanılması

Bu dönem yapılan çalışmanın ilk aşamasında, önceki dönemde geliştirilen standart MLP tabanlı ters makine öğrenmesi modeli proses optimizasyonu ve model öngörülü kontrol yapısında kullanılabilecek bir soft-sensor bileşeni haline getirilmiştir. Soft-sensor kavramı, doğrudan veya hızlı biçimde ölçülmesi zor olan bir proses değişkeninin, ölçülebilen diğer değişkenler yardımıyla hesaplamalı olarak tahmin edilmesini ifade etmektedir. Bu çalışmada doğrudan ölçülmesi daha zor, pahalı ve zaman alıcı olan biyoyağ kompozisyonu, reformer çıkışında ölçülebilen singaz kompozisyonu ve bilinen işletme koşulları kullanılarak tahmin edilmektedir.

Biyoyağın ayrıntılı kimyasal karakterizasyonu için GC-MS, FTIR ve benzeri analiz yöntemlerine ihtiyaç duyulmaktadır. Bu analizler laboratuvar koşullarında yapılmakta, numune hazırlama ve analiz süreci zaman alabilmektedir. Buna karşılık reformer çıkışındaki H2, CO, CO2, CH4 ve H2O gibi gaz bileşenleri proses hattında daha hızlı izlenebilir niteliktedir. Bu nedenle, singaz kompozisyonundan biyoyağ kompozisyonunu tahmin eden ters model, prosesin anlık hammadde karakteristiğini izlemek için uygun bir soft-sensor yapısı sağlamaktadır.

Geliştirilen soft-sensor yapısında model girişleri reformer sıcaklığı, reformer basıncı, buhar/karbon oranı, H2 mol yüzdesi, CO mol yüzdesi, CO2 mol yüzdesi, CH4 mol yüzdesi ve H2O mol yüzdesidir. Model çıktıları ise biyoyağ kompozisyonunu temsil eden altı bileşen grubudur: aromatikler, asitler, alkoller, furanlar, fenoller ve aldehit-ketonlar. Bu yapı, önceki dönemde eğitilen standart MLP modelinin doğrudan kullanılmasına olanak tanımaktadır.

Bu dönemde mevcut MLP modeli için ayrı bir tahmin arayüzü oluşturulmuştur. Bu arayüz, kaydedilmiş model dosyasını ve ölçeklendirme parametrelerini yüklemekte, verilen singaz ve proses koşullarını modelin beklediği giriş formatına dönüştürmekte ve biyoyağ kompozisyonu tahminini yüzde bileşim olarak üretmektedir. Böylece model, yalnızca eğitim scriptleri içinde çalışan bir yapı olmaktan çıkarılmış ve optimizasyon/MPC algoritmaları tarafından çağrılabilir bir modül haline getirilmiştir.

Modelin çalışması sırasında öncelikle giriş değişkenleri eğitim aşamasında kullanılan ölçeklendirici ile standartlaştırılmaktadır. Daha sonra standart MLP modeli bu ölçeklendirilmiş girdiler üzerinden altı bileşenli biyoyağ kompozisyonunu tahmin etmektedir. Model çıktıları tekrar gerçek yüzde ölçeğine dönüştürülmekte ve negatif tahminler fiziksel anlam taşımadığı için sıfır altına düşmeyecek şekilde sınırlandırılmaktadır. Gerekli durumlarda çıktı bileşenleri toplamı %100 olacak şekilde normalize edilmektedir. Bu işlem, MPC ve optimizasyon aşamalarında fiziksel olarak anlamlı bir biyoyağ kompozisyonunun kullanılmasını sağlamaktadır.

Soft-sensor yapısının genel çalışma mantığı Şekil B.3'te gösterilecektir. Reformerden elde edilen singaz kompozisyonu ve bilinen proses koşulları ters ML modeline girdi olarak verilmekte, model biyoyağ kompozisyonunu tahmin etmekte ve bu tahmin ileri model ile optimizasyon bloğuna aktarılmaktadır. Böylece proses çıkışından hammadde kompozisyonu kestirilmekte ve bu kestirim kullanılarak bir sonraki kontrol hamlesi hesaplanmaktadır.

Bu yapının tez çalışması açısından önemi, biyoyağ kompozisyonunu yalnızca deneysel analizle belirlenen statik bir bilgi olmaktan çıkarıp, proses sırasında izlenebilir bir değişken haline getirmesidir. Reformer çıkışındaki singaz kompozisyonunda meydana gelen değişimler, ters model aracılığıyla biyoyağ kompozisyonundaki olası değişimlere dönüştürülebilmektedir. Bu durum, özellikle farklı kaynaklardan gelen biyoyağların değişken kompozisyonlara sahip olduğu sürekli proseslerde hammadde kalite kontrolü ve proses optimizasyonu açısından avantaj sağlamaktadır.

Bu dönem oluşturulan soft-sensor modülü, sonraki alt bölümlerde anlatılan ileri surrogate model, statik optimizasyon ve MPC senaryosunun temel giriş bileşenlerinden biridir. Model doğrudan proses koşullarını belirlememekte, bunun yerine optimizasyon sistemine biyoyağ kompozisyonu tahmini sağlamaktadır. Optimizasyon sistemi ise bu tahmini kullanarak hedef H2/CO oranına yaklaşan uygun T, P ve S/C değerlerini hesaplamaktadır.

**Tablo B.4. Ters ML soft-sensor modelinin giriş ve çıkış değişkenleri**

| Değişken grubu | Değişkenler | Açıklama |
|---|---|---|
| Proses koşulları | Reformer sıcaklığı, basınç, buhar/karbon oranı | İşletme sırasında bilinen kontrol/işletme değişkenleri |
| Singaz kompozisyonu | H2, CO, CO2, CH4, H2O mol yüzdeleri | Reformer çıkışından ölçülen veya simülasyonla elde edilen değişkenler |
| Soft-sensor çıktısı | Aromatikler, asitler, alkoller, furanlar, fenoller, aldehit-ketonlar | Tahmin edilen biyoyağ kompozisyonu |

**Tablo B.5. Soft-sensor modülünün yazılım yapısı**

| Dosya / bileşen | Görev |
|---|---|
| `inverse_predictor.py` | Kaydedilmiş MLP modelini ve ölçeklendiricileri yükler |
| `ReverseMLSoftSensor` sınıfı | Singaz ve proses koşullarından biyoyağ kompozisyonu tahmini üretir |
| `mlp_standard.h5` | Önceki dönemde eğitilen standart MLP modeli |
| `scaler_X.pkl` | Giriş değişkenleri için kullanılan ölçeklendirici |
| `scaler_y.pkl` | Çıkış değişkenleri için kullanılan ölçeklendirici |

**Bu alt bölümde kullanılacak tablo ve figürler:**

Tablo B.4. Ters ML soft-sensor modelinin giriş ve çıkış değişkenleri  
Tablo B.5. Soft-sensor modülünün yazılım yapısı  
Şekil B.3. Ters ML soft-sensor çalışma akışı  
Şekil B.4. Soft-sensor çıktısının optimizasyon ve MPC bloğuna aktarılması

#### B.2.3 BiooilID Bazlı Model Validasyonu

Önceki tez izleme döneminde ters makine öğrenmesi modelinin performansı train, validation ve test kümeleri üzerinden değerlendirilmiş ve standart MLP modeli test setinde ortalama R2=0.863, ortalama MAE=%4.03 başarısına ulaşmıştır. Bu sonuç, modelin genel olarak yüksek doğrulukla çalıştığını göstermektedir. Ancak önceki değerlendirmede veri ayrımı satır bazında yapılmıştır. Veri setinde her bir biyoyağ kompozisyonu farklı sıcaklık, basınç ve buhar/karbon oranı koşulları altında tekrarlandığı için, satır bazlı ayrım yapıldığında aynı BiooilID'ye ait farklı proses koşulları hem eğitim hem de test kümelerinde yer alabilmektedir.

Bu durum model başarısının yorumlanması açısından önemlidir. Satır bazlı test, modelin daha önce gördüğü biyoyağ kompozisyonlarının farklı proses koşullarındaki davranışını ne kadar iyi öğrendiğini göstermektedir. Başka bir ifadeyle, bu test modelin proses koşullarına bağlı interpolasyon kabiliyetini değerlendirmektedir. Buna karşılık, modelin hiç görmediği yeni bir biyoyağ kompozisyonuna genelleme yapıp yapamadığını anlamak için biyoyağ kimliği bazında ayrım yapılması gerekmektedir. Bu nedenle bu dönemde ek bir BiooilID bazlı validasyon çalışması yapılmıştır.

BiooilID bazlı validasyonda veri seti, biyoyağ kimlikleri birbirinden tamamen ayrılacak şekilde eğitim ve test kümelerine bölünmüştür. Toplam 30 farklı biyoyağ kompozisyonundan 24 tanesi eğitim kümesinde, 6 tanesi ise test kümesinde bırakılmıştır. Böylece test kümesindeki biyoyağlar model eğitimi sırasında hiç görülmemiştir. Eğitim kümesinde 1080 örnek, test kümesinde ise 270 örnek yer almıştır. Bu kurgu, önceki satır bazlı ayrımdan daha zor ve daha gerçekçi bir genelleme testi olarak değerlendirilmiştir.

Bu validasyon çalışmasında hızlı bir genelleme denetimi yapmak amacıyla ExtraTrees tabanlı çok çıktılı regresyon modeli kullanılmıştır. Model girdileri önceki ters tahmin yaklaşımıyla aynı tutulmuştur: reformer sıcaklığı, basınç, buhar/karbon oranı ve H2, CO, CO2, CH4, H2O mol yüzdeleri. Çıkış değişkenleri yine aromatikler, asitler, alkoller, furanlar, fenoller ve aldehit-ketonlar olarak seçilmiştir. Böylece BiooilID bazlı ayrımın, ters tahmin probleminin bileşen bazındaki genelleme başarısı üzerindeki etkisi incelenmiştir.

Elde edilen sonuçlara göre aromatikler ve asitler için model yeni biyoyağlara karşı yüksek doğruluk göstermiştir. Aromatikler için R2=0.951 ve MAE=%5.84, asitler için R2=0.803 ve MAE=%5.23 olarak hesaplanmıştır. Fenoller için R2=0.698, aldehit-ketonlar için R2=0.624 ve furanlar için R2=0.464 değerleri elde edilmiştir. Bu sonuçlar, bazı bileşenlerin singaz kompozisyonu üzerinden yeni biyoyağlarda da tahmin edilebilir olduğunu göstermektedir.

Buna karşılık alkoller için R2 değeri negatif çıkmıştır. Bu durum, alkol bileşeninin test kümesinde düşük varyansa sahip olması, singaz çıktıları üzerinde daha zayıf veya diğer bileşenlerle karışan bir etki bırakması ve modelin bu bileşen için yeni biyoyağlara genelleme yapmakta zorlanmasıyla açıklanabilir. Ortalama R2 değeri bu negatif sonuç nedeniyle düşük görünmektedir; ancak ortalama MAE değeri %4.62 seviyesinde kalmıştır. Bu nedenle BiooilID bazlı validasyon sonucu, modelin bazı bileşenlerde güçlü, bazı bileşenlerde ise daha sınırlı genelleme kabiliyetine sahip olduğunu göstermektedir.

Bu bulgu tez çalışması açısından önemlidir. Önceki dönemde elde edilen yüksek MLP performansı, modelin mevcut veri seti içinde proses koşullarına bağlı ters tahmin görevini başarılı biçimde öğrendiğini göstermektedir. Bu dönemde yapılan BiooilID bazlı validasyon ise daha zor bir senaryoyu temsil etmekte ve modelin tamamen yeni biyoyağ kompozisyonlarında daha dikkatli değerlendirilmesi gerektiğini ortaya koymaktadır. Bu nedenle bu sonuçlar bir başarısızlık olarak değil, modelin uygulama sınırlarını belirleyen ek bir validasyon aşaması olarak değerlendirilmiştir.

MPC ve optimizasyon çalışmasında bu sonuç şu şekilde dikkate alınmıştır: Ters ML modeli, mevcut veri tabanındaki biyoyağ kompozisyon aralığına benzer örneklerde soft-sensor olarak kullanılabilir. Ancak veri tabanında temsil edilmeyen çok farklı biyoyağ kompozisyonları için model tahminlerinin belirsizliği artabilir. Bu nedenle sonraki çalışmalarda BiooilID bazlı MLP yeniden eğitimi, belirsizlik tahmini ve yeni deneysel/simülasyon verileriyle veri setinin genişletilmesi önerilmektedir.

**Tablo B.6. BiooilID bazlı validasyonda kullanılan eğitim ve test veri yapısı**

| Veri kümesi | BiooilID sayısı | Örnek sayısı | Açıklama |
|---|---:|---:|---|
| Eğitim kümesi | 24 | 1080 | Modelin eğitildiği biyoyağ kompozisyonları |
| Test kümesi | 6 | 270 | Eğitimde hiç görülmeyen biyoyağ kompozisyonları |
| Toplam | 30 | 1350 | Cantera tabanlı temiz veri seti |

**Tablo B.7. BiooilID bazlı validasyon bileşen bazlı performans sonuçları**

| Bileşen | R2 | RMSE (%) | MAE (%) |
|---|---:|---:|---:|
| Aromatikler | 0.951 | 7.43 | 5.84 |
| Asitler | 0.803 | 6.42 | 5.23 |
| Alkoller | -6.577 | 4.01 | 2.58 |
| Furanlar | 0.464 | 2.79 | 2.07 |
| Fenoller | 0.698 | 11.51 | 8.88 |
| Aldehit-ketonlar | 0.624 | 4.71 | 3.14 |
| Ortalama | -0.506 | 6.14 | 4.62 |

**Bu alt bölümde kullanılacak tablo ve figürler:**

Tablo B.6. BiooilID bazlı validasyonda kullanılan eğitim ve test veri yapısı  
Tablo B.7. BiooilID bazlı validasyon bileşen bazlı performans sonuçları  
Şekil B.5. Satır bazlı test ile BiooilID bazlı test yaklaşımının karşılaştırılması  
Şekil B.6. BiooilID bazlı validasyonda bileşen bazlı R2 değerleri

#### B.2.4 İleri Surrogate Modelin Geliştirilmesi

Bu dönemde, ters makine öğrenmesi modelini optimizasyon ve MPC yapısında kullanabilmek için ters tahmin yapısını tamamlayan bir ileri surrogate model geliştirilmiştir. Ters model, reformer çalışma koşulları ve sentez gazı bileşiminden biyoyağ kompozisyonunu tahmin etmektedir. Optimizasyon algoritmasının aday sıcaklık, basınç ve buhar/karbon oranı değerlerini hızlı biçimde değerlendirebilmesi için ise belirli bir biyoyağ kompozisyonu ve proses koşulu altında oluşacak sentez gazı bileşimini öngören ileri modele ihtiyaç duyulmuştur.

İleri modelde giriş değişkenleri biyoyağı temsil eden altı bileşen grubu ile reformer sıcaklığı, reformer basıncı ve buhar/karbon oranı olarak tanımlanmıştır. Model çıktıları H2, CO, CO2, CH4 ve H2O mol yüzdeleri ile H2/CO oranıdır. Böylece model, her aday kontrol hareketi için Cantera simülasyonu çalıştırmadan hızlı bir performans tahmini üretebilecek hesaplama bloğu olarak kullanılmıştır.

Model, temizlenmiş Cantera veri seti üzerinde çok çıkışlı regresyon problemi olarak eğitilmiştir. Geliştirilen yazılım yapısında model eğitimi ve değerlendirme işlemleri `surrogate_model.py` modülü altında toplanmıştır. Bu yapı veri setinin okunması, giriş-çıkış kolonlarının ayrılması, model eğitimi, test performansının hesaplanması ve eğitilmiş modelin optimizasyon modülüne aktarılması adımlarını içermektedir.

Model performansı sentez gazı bileşenleri ve H2/CO oranı için ayrı ayrı değerlendirilmiştir. Ortalama R2 değerinin 0.996, ortalama RMSE değerinin 0.268 ve ortalama MAE değerinin 0.125 seviyesinde bulunması, ileri surrogate modelin Cantera tabanlı veri uzayını yüksek doğrulukla temsil edebildiğini göstermektedir. Bu nedenle bu model, bu dönem geliştirilen statik optimizasyon ve MPC senaryolarında hızlı proses tahmincisi olarak kullanılmıştır.

**Tablo B.8. İleri surrogate modelin giriş ve çıkış değişkenleri**

| Değişken grubu | Değişkenler | Açıklama |
|---|---|---|
| Biyoyağ kompozisyonu | Aromatikler, asitler, alkoller, furanlar, fenoller, aldehit-ketonlar | Soft-sensor çıktısı veya bilinen BiooilID kompozisyonu |
| Kontrol değişkenleri | Reformer sıcaklığı, reformer basıncı, buhar/karbon oranı | Optimizasyon ve MPC tarafından değiştirilen proses koşulları |
| Model çıktıları | H2, CO, CO2, CH4, H2O, H2/CO | Aday çalışma koşulunun sentez gazı performansı |

**Tablo B.9. İleri surrogate model performans sonuçları**

| Çıkış değişkeni | R2 | RMSE | MAE |
|---|---:|---:|---:|
| H2 mol% | 0.997 | 0.414 | 0.211 |
| CO mol% | 0.997 | 0.220 | 0.087 |
| CO2 mol% | 0.987 | 0.233 | 0.102 |
| CH4 mol% | 0.998 | 0.188 | 0.071 |
| H2O mol% | 0.999 | 0.393 | 0.217 |
| H2/CO oranı | 0.997 | 0.157 | 0.062 |
| Ortalama | 0.996 | 0.268 | 0.125 |

**Bu alt bölümde kullanılacak tablo ve figürler:**

Tablo B.8. İleri surrogate modelin giriş ve çıkış değişkenleri  
Tablo B.9. İleri surrogate model performans sonuçları  
Şekil B.7. İleri surrogate modelin giriş-çıkış yapısı ve optimizasyon bloğu ile ilişkisi  
Şekil B.8. İleri surrogate model için gerçek ve tahmin edilen sentez gazı çıktılarının karşılaştırılması

#### B.2.5 Optimizasyon Probleminin Tanımlanması

Bu dönemde geliştirilen optimizasyon problemi, biyoyağ buhar reformlama sürecinde istenen H2/CO oranına mümkün olduğunca yakın sentez gazı üretirken prosesin enerji/işletme maliyetini azaltmayı hedefleyecek şekilde tanımlanmıştır. Optimizasyon yapısında biyoyağ kompozisyonu sabit bir durum girdisi olarak ele alınmış, karar değişkenleri ise yalnızca doğrudan kontrol edilebilir proses değişkenleri olan reformer sıcaklığı, reformer basıncı ve buhar/karbon oranı ile sınırlandırılmıştır.

Amaç fonksiyonu iki ana hedefi birlikte içermektedir. Birinci hedef, sentez gazının H2/CO oranını belirlenen hedef değere yaklaştırmaktır. İkinci hedef ise daha düşük enerji ve işletme maliyeti temsil eden çalışma koşullarını tercih etmektir. Bu nedenle sıcaklık, basınç ve buhar/karbon oranı için normalize edilmiş bir maliyet terimi tanımlanmış; sıcaklık maliyeti daha baskın, buhar/karbon oranı ve basınç maliyetleri ise daha düşük ağırlıklı olacak şekilde ele alınmıştır. Ayrıca hidrojen üretiminin çok düşük kalmasını ve CO2 oluşumunun artmasını önlemek için ceza terimleri kullanılmıştır.

Optimizasyon algoritması, tanımlanan sınırlar içinde aday çalışma koşullarını değerlendiren ızgara tabanlı bir tarama yaklaşımı ile uygulanmıştır. Bu tercih, üç kontrol değişkenli problemde kararlı, hızlı ve yorumlanabilir sonuçlar üretmiştir. Her aday noktada ileri surrogate model çalıştırılmış, elde edilen sentez gazı çıktıları amaç fonksiyonuna aktarılmış ve en düşük amaç fonksiyonu değerini veren çalışma koşulu seçilmiştir.

**Tablo B.10. Optimizasyon karar değişkenleri ve sınırları**

| Karar değişkeni | Alt sınır | Üst sınır | Birim |
|---|---:|---:|---|
| Reformer sıcaklığı | 650 | 850 | °C |
| Reformer basıncı | 5 | 30 | bar |
| Buhar/karbon oranı | 2 | 6 | - |

**Tablo B.11. Amaç fonksiyonu bileşenleri**

| Amaç fonksiyonu bileşeni | Rolü |
|---|---|
| H2/CO hedef sapması | Sentez gazı oranını hedef değere yaklaştırır |
| Enerji/işletme maliyeti | Daha düşük sıcaklık, basınç ve buhar kullanımını teşvik eder |
| H2 alt sınır cezası | Hidrojen üretiminin yetersiz kalmasını engeller |
| CO2 üst sınır cezası | CO2 oluşumunun artmasını sınırlar |
| Kontrol hareketi cezası | MPC senaryosunda ani kontrol değişimlerini azaltır |

**Bu alt bölümde kullanılacak tablo ve figürler:**

Tablo B.10. Optimizasyon karar değişkenleri ve sınırları  
Tablo B.11. Amaç fonksiyonu bileşenleri  
Şekil B.9. Biyoyağ kompozisyonu, ileri surrogate model ve amaç fonksiyonundan oluşan optimizasyon problem yapısı

#### B.2.6 Statik Optimizasyon Çalışmaları

Tanımlanan optimizasyon yapısı öncelikle statik case-study senaryoları üzerinde test edilmiştir. Bu amaçla üç farklı biyoyağ tipi seçilmiştir: aromatik bakımından zengin, asit bakımından zengin ve daha dengeli kompozisyona sahip biyoyağ örnekleri. Her bir biyoyağ için başlangıç koşulu 750 °C reformer sıcaklığı, 15 bar basınç ve 4 buhar/karbon oranı olarak alınmıştır. Optimizasyon çalışmaları H2/CO hedefinin 2.0 ve 2.5 olduğu iki farklı senaryo için yürütülmüştür.

Başlangıç koşullarında H2/CO oranları yaklaşık 5.78-6.07 aralığında bulunmuştur. Optimizasyon sonrasında bu oranlar seçilen biyoyağ kompozisyonuna ve hedef değere bağlı olarak yaklaşık 2.52-2.82 aralığına düşürülmüştür. Bu sonuç, geliştirilen optimizasyon yapısının sentez gazı kompozisyonunu hedeflenen kimyasal kullanım aralığına yaklaştırabildiğini göstermektedir. Bununla birlikte H2/CO = 2.0 hedefi, tanımlanan kontrol değişkeni sınırları ve mevcut veri uzayı içinde tam olarak yakalanamamıştır. Bu durum, hedef değerin bazı biyoyağ kompozisyonları için mevcut çalışma aralığında erişilebilir olmadığını göstermektedir.

H2/CO = 2.5 hedefinde, özellikle aromatik bakımından zengin ve dengeli biyoyağ örneklerinde hedefe daha yakın sonuçlar daha düşük enerji maliyetiyle elde edilmiştir. Asit bakımından zengin biyoyağ örneğinde ise model, hedefe yaklaşmak için yine yüksek sıcaklık ve düşük basınç koşulunu seçmiştir. Bu bulgu, biyoyağ kompozisyonunun optimum proses koşulları üzerinde doğrudan etkili olduğunu ve kompozisyon bilgisinin optimizasyon yapısına dahil edilmesinin gerekli olduğunu göstermektedir.

**Tablo B.12. Statik optimizasyon case-study sonuçları**

| Senaryo | BiooilID | Hedef H2/CO | Başlangıç H2/CO | Optimum T (°C) | Optimum P (bar) | Optimum S/C | Optimum H2/CO | Enerji maliyeti |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Aromatik zengin | 66 | 2.0 | 5.778 | 850 | 5 | 2 | 2.518 | 0.650 |
| Aromatik zengin | 66 | 2.5 | 5.778 | 775 | 5 | 2 | 2.770 | 0.406 |
| Asit zengin | 70 | 2.0 | 6.070 | 850 | 5 | 2 | 2.786 | 0.650 |
| Asit zengin | 70 | 2.5 | 6.070 | 850 | 5 | 2 | 2.786 | 0.650 |
| Dengeli | 60 | 2.0 | 5.907 | 850 | 5 | 2 | 2.647 | 0.650 |
| Dengeli | 60 | 2.5 | 5.907 | 800 | 5 | 2 | 2.819 | 0.488 |

**Bu alt bölümde kullanılacak tablo ve figürler:**

Tablo B.12. Statik optimizasyon case-study sonuçları  
Şekil B.10. Statik optimizasyon senaryolarında başlangıç ve optimize edilmiş H2/CO oranlarının karşılaştırılması. Kaynak dosya: `results/figures/static_optimization_h2co.png`

#### B.2.7 Model Öngörülü Kontrol Senaryosunun Geliştirilmesi

Statik optimizasyon çalışmasının ardından, geliştirilen soft-sensor ve ileri surrogate model kullanılarak basit bir model öngörülü kontrol senaryosu oluşturulmuştur. Bu senaryoda amaç, biyoyağ kompozisyonu zamanla değiştiğinde sentez gazı H2/CO oranını hedef değere yakın tutacak kontrol hareketlerini hesaplamaktır. MPC yapısı, her zaman adımında mevcut ölçüm bilgisini kullanarak biyoyağ kompozisyonunu tahmin etmekte, ardından ileri surrogate model yardımıyla yeni kontrol değişkenlerini belirlemektedir.

Geliştirilen kapalı çevrim senaryoda ölçülen sentez gazı bileşimi ve mevcut proses koşulları ters ML soft-sensor modeline verilmiştir. Soft-sensor çıktısı olarak elde edilen biyoyağ kompozisyonu, ileri surrogate modelin girişine aktarılmıştır. Optimizasyon modülü, sıcaklık, basınç ve buhar/karbon oranı adaylarını değerlendirerek bir sonraki zaman adımı için en uygun kontrol hareketini seçmiştir. Bu yaklaşımda her adımda yalnızca ilk kontrol hareketi uygulanmış ve sonraki adımda ölçüm/tahmin döngüsü tekrarlanmıştır.

MPC senaryosunda karar değişkenleri statik optimizasyonla aynı tutulmuştur. Ek olarak, kontrol hareketlerinin çok sert değişmesini önlemek için amaç fonksiyonuna hareket cezası eklenmiştir. Böylece algoritma yalnızca hedef H2/CO oranına yaklaşmayı değil, aynı zamanda daha düzenli kontrol hareketleri üretmeyi de dikkate almıştır. Bu yapı, gerçek zamanlı uygulama için henüz deneysel bir kontrol sistemi değildir; ancak geliştirilen ML modellerinin kapalı çevrim karar verme yapısında nasıl kullanılabileceğini gösteren bir hesaplamalı senaryodur.

**Tablo B.13. MPC algoritmasının temel adımları**

| Adım | İşlem | Kullanılan model/modül |
|---|---|---|
| 1 | Mevcut proses koşulu ve sentez gazı bileşimi alınır | Ölçüm/senaryo verisi |
| 2 | Biyoyağ kompozisyonu tahmin edilir | Ters ML soft-sensor |
| 3 | Aday T, P ve S/C değerleri denenir | Optimizasyon modülü |
| 4 | Her aday için sentez gazı bileşimi tahmin edilir | İleri surrogate model |
| 5 | Amaç fonksiyonuna göre en uygun kontrol hareketi seçilir | Optimizasyon modülü |
| 6 | Seçilen ilk kontrol hareketi uygulanır | MPC döngüsü |

**Tablo B.14. MPC senaryosunda kullanılan başlangıç koşulları**

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

**Bu alt bölümde kullanılacak tablo ve figürler:**

Tablo B.13. MPC algoritmasının temel adımları  
Tablo B.14. MPC senaryosunda kullanılan başlangıç koşulları  
Şekil B.11. Soft-sensor, ileri surrogate model ve optimizasyon bloğundan oluşan MPC kapalı çevrim yapısı

#### B.2.8 MPC Senaryosu ve Bozucu Etki Analizi

MPC senaryosu, dengeli biyoyağ kompozisyonu ile başlatılmış ve 10 zaman adımı boyunca çalıştırılmıştır. Başlangıç koşulunda sentez gazı H2/CO oranı 5.907 olarak hesaplanmıştır. Kontrol algoritması ilk adımda sıcaklığı 850 °C, basıncı 5 bar ve buhar/karbon oranını 2 olarak seçmiş; bu kontrol hareketi sonrasında H2/CO oranı yaklaşık 2.65 seviyesine düşmüştür. Bu değer H2/CO = 2.0 hedefini tam olarak yakalamasa da başlangıç durumuna göre önemli bir iyileşme sağlamıştır.

Senaryonun beşinci zaman adımında bozucu etki uygulanmıştır. Bu bozucu etki, biyoyağ kompozisyonunda asit içeriğinin artırılması, aromatik ve fenolik bileşenlerin azaltılması şeklinde tanımlanmıştır. Bozucu etki sonrasında sistemin H2/CO oranı yaklaşık 2.67 seviyesine yerleşmiştir. Kontrol algoritması aynı çalışma koşullarını koruyarak sentez gazı oranını dar bir aralıkta tutmuştur. Bu sonuç, geliştirilen hesaplamalı MPC yapısının kompozisyon değişimine rağmen sentez gazı oranını başlangıçtaki yüksek değerden hedef bölgeye yakın bir aralığa çekebildiğini göstermektedir.

Soft-sensor çıktıları bozucu etki sonrasında gerçek biyoyağ kompozisyonundaki yönelimi genel olarak takip etmiştir. Bununla birlikte bazı bileşenlerde, özellikle alkol ve aldehit-keton gruplarında farklar görülmüştür. Bu farklar, BiooilID bazlı validasyon sonuçlarıyla uyumludur ve kapalı çevrim uygulamada soft-sensor belirsizliğinin dikkate alınması gerektiğini göstermektedir.

**Tablo B.15. MPC senaryosu özet sonuçları**

| Zaman adımı | Durum | Uygulanan T (°C) | Uygulanan P (bar) | Uygulanan S/C | Ölçülen H2/CO | Sonraki tahmin H2/CO |
|---:|---|---:|---:|---:|---:|---:|
| 0 | Başlangıç | 750 | 15 | 4 | 5.907 | 2.639 |
| 1 | Kontrol sonrası | 850 | 5 | 2 | 2.647 | 2.639 |
| 5 | Bozucu etki sonrası | 850 | 5 | 2 | 2.671 | 2.670 |
| 9 | Son durum | 850 | 5 | 2 | 2.671 | 2.670 |

**Tablo B.16. Son zaman adımında gerçek ve soft-sensor tahmini biyoyağ kompozisyonu**

| Bileşen grubu | Gerçek kompozisyon (%) | Tahmin edilen kompozisyon (%) |
|---|---:|---:|
| Aromatikler | 0.000 | 1.455 |
| Asitler | 31.324 | 27.421 |
| Alkoller | 8.758 | 4.779 |
| Furanlar | 11.334 | 11.372 |
| Fenoller | 35.188 | 35.640 |
| Aldehit-ketonlar | 13.395 | 19.333 |

**Bu alt bölümde kullanılacak tablo ve figürler:**

Tablo B.15. MPC senaryosu özet sonuçları  
Tablo B.16. Son zaman adımında gerçek ve soft-sensor tahmini biyoyağ kompozisyonu  
Şekil B.12. MPC zaman serisi, H2/CO oranı ve kontrol değişkenlerinin değişimi. Kaynak dosya: `results/figures/mpc_case_study_timeseries.png`

#### B.2.9 Dönem İçi Çalışma Sonuçları

Bu dönem çalışmasında önceki dönemde geliştirilen ters makine öğrenmesi modeli, optimizasyon ve MPC yapısında kullanılabilecek bir soft-sensor bileşeni olarak konumlandırılmıştır. Bunun için modelin giriş-çıkış arayüzü tanımlanmış, biyoyağ kompozisyon tahminleri kontrol algoritmasına aktarılabilir hale getirilmiş ve modelin BiooilID bazlı genelleme davranışı ayrıca incelenmiştir.

BiooilID bazlı validasyon, modelin bazı bileşen gruplarında güçlü genelleme performansı verdiğini, bazı bileşenlerde ise yeni biyoyağ kompozisyonlarına geçildiğinde belirsizliğin arttığını göstermiştir. Bu sonuç, sonraki çalışmalarda model belirsizliği, veri çeşitliliği ve kompozisyon temsili konularının geliştirilmesi gerektiğini ortaya koymuştur.

Bu dönemin ikinci ana çıktısı ileri surrogate modeldir. Bu model, biyoyağ kompozisyonu ve proses koşullarından sentez gazı bileşimini yüksek doğrulukla tahmin etmiş ve ortalama R2 = 0.996 performansına ulaşmıştır. Böylece optimizasyon ve MPC algoritmalarının her aday çalışma koşulu için Cantera simülasyonu çalıştırmadan hızlı karar üretmesi mümkün hale gelmiştir.

Statik optimizasyon çalışmaları, üç farklı biyoyağ tipi için başlangıçta yaklaşık 5.8-6.1 aralığında bulunan H2/CO oranının yaklaşık 2.5-2.8 aralığına indirilebildiğini göstermiştir. MPC senaryosu ise kompozisyon bozucu etkisi altında H2/CO oranının başlangıçtaki yüksek değerden hedef bölgeye yakın ve daha kararlı bir aralığa çekilebildiğini ortaya koymuştur. Bununla birlikte H2/CO = 2.0 hedefinin mevcut kontrol sınırları içinde tam olarak yakalanamaması, karar değişkeni sınırlarının, amaç fonksiyonu ağırlıklarının ve gerekirse ek kontrol değişkenlerinin sonraki dönemde daha ayrıntılı incelenmesi gerektiğini göstermektedir.

**Tablo B.17. Dönem içi ana çıktılar ve bulgular**

| Çalışma adımı | Ana çıktı | Temel bulgu |
|---|---|---|
| Soft-sensor arayüzü | Ters ML modeli kontrol sistemine bağlandı | Biyoyağ kompozisyonu hızlı tahmin edilebilir hale geldi |
| BiooilID validasyonu | Grup bazlı genelleme testi yapıldı | Bazı bileşenlerde yeni biyoyağa geçişte belirsizlik arttı |
| İleri surrogate model | Sentez gazı tahmin modeli geliştirildi | Ortalama R2 = 0.996 elde edildi |
| Statik optimizasyon | Üç biyoyağ tipi için case-study çalıştırıldı | H2/CO oranı yaklaşık 2.5-2.8 aralığına indirildi |
| MPC senaryosu | Bozucu etki altında kapalı çevrim simülasyon yapıldı | H2/CO oranı bozucu etki sonrasında dar aralıkta tutuldu |

**Bu alt bölümde kullanılacak tablo ve figürler:**

Tablo B.17. Dönem içi ana çıktılar ve bulgular  
Şekil B.13. TİK-5 döneminde geliştirilen soft-sensor, ileri surrogate model, optimizasyon ve MPC sisteminin nihai özet akışı

### B.3 Bir Sonraki Dönem İçerisinde Yapılacak Çalışmalar

### B.4 Kaynaklar Dizini
