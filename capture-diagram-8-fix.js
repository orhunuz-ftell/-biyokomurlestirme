const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
  console.log('🚀 Diagram 8 için tarayıcı başlatılıyor...');

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  // Çok uzun diyagram için büyük viewport
  await page.setViewport({
    width: 1600,
    height: 2400, // Daha uzun yükseklik
    deviceScaleFactor: 2
  });

  const htmlPath = path.join(__dirname, 'flowcharts-complete.html');
  const htmlUrl = `file:///${htmlPath.replace(/\\/g, '/')}`;

  console.log(`📄 HTML yükleniyor: ${htmlUrl}`);
  await page.goto(htmlUrl, { waitUntil: 'networkidle0' });

  console.log('📸 Diagram 8 (Hidrojen Üretim Prosesi) kaydediliyor...');

  // 8. sekmeye tıkla (index 7)
  await page.click(`nav button:nth-of-type(8)`);

  // Render için bekle
  await new Promise(resolve => setTimeout(resolve, 1500));

  // Diyagram alanının tam boyutunu al
  const element = await page.$('#diagram-area');

  if (element) {
    // Element'in tam boyutunu kontrol et
    const boundingBox = await element.boundingBox();
    console.log(`   Diyagram boyutu: ${boundingBox.width}x${boundingBox.height} px`);

    // Screenshot al
    await element.screenshot({
      path: `diagram-8-hidrojen-uretim-prosesi.png`,
      type: 'png'
    });

    const stats = fs.statSync('diagram-8-hidrojen-uretim-prosesi.png');
    const sizeKB = (stats.size / 1024).toFixed(1);

    console.log(`\n✅ Başarıyla kaydedildi!`);
    console.log(`   📁 diagram-8-hidrojen-uretim-prosesi.png (${sizeKB} KB)`);
  } else {
    console.log('❌ Diyagram alanı bulunamadı!');
  }

  await browser.close();

  console.log('\n🎉 İşlem tamamlandı!');
})();
