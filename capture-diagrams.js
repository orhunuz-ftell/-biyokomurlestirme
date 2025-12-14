const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
  console.log('🚀 Tarayıcı başlatılıyor...');

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  // Yüksek çözünürlük için viewport ayarla
  await page.setViewport({
    width: 1600,
    height: 1200,
    deviceScaleFactor: 2
  });

  const htmlPath = path.join(__dirname, 'flowcharts-complete.html');
  const htmlUrl = `file:///${htmlPath.replace(/\\/g, '/')}`;

  console.log(`📄 HTML yükleniyor: ${htmlUrl}`);
  await page.goto(htmlUrl, { waitUntil: 'networkidle0' });

  const diagrams = [
    'ana-sistem',
    'cantera-simulasyon',
    'mlp-mimarisi',
    'egitim-sureci',
    'ters-tahmin',
    'performans-ensemble',
    'ozellik-onemi',
    'hidrojen-uretim-prosesi'
  ];

  console.log('\n📸 Diyagramlar kaydediliyor...\n');

  for (let i = 0; i < diagrams.length; i++) {
    console.log(`  [${i + 1}/8] ${diagrams[i]}.png`);

    // Sekmeye tıkla
    await page.click(`nav button:nth-of-type(${i + 1})`);

    // Render için bekle
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Sadece diyagram alanının screenshot'ını al
    const element = await page.$('#diagram-area');

    if (element) {
      await element.screenshot({
        path: `diagram-${i + 1}-${diagrams[i]}.png`,
        type: 'png'
      });
    }
  }

  await browser.close();

  console.log('\n✅ Tüm diyagramlar başarıyla kaydedildi!');
  console.log('\n📁 Oluşturulan dosyalar:');

  for (let i = 0; i < diagrams.length; i++) {
    const filename = `diagram-${i + 1}-${diagrams[i]}.png`;
    const stats = fs.statSync(filename);
    const sizeKB = (stats.size / 1024).toFixed(1);
    console.log(`   ✓ ${filename} (${sizeKB} KB)`);
  }

  console.log('\n🎉 İşlem tamamlandı!');
})();
