// Tüm diyagramları otomatik PNG olarak kaydet
// Kullanım: npm install puppeteer && node save-all-diagrams.js

const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  console.log('🚀 Tarayıcı başlatılıyor...');

  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();

  // Viewport ayarla (yüksek çözünürlük)
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 2 });

  const htmlPath = path.join(__dirname, 'algorithm-flowcharts.html');
  await page.goto(`file://${htmlPath}`);

  const diagrams = [
    'Ana Sistem',
    'Cantera Simülasyon',
    'MLP Mimarisi',
    'Eğitim Süreci',
    'Ters Tahmin',
    'Performans/Ensemble',
    'Özellik Önemi',
    'Hidrojen Üretim Prosesi'
  ];

  for (let i = 0; i < diagrams.length; i++) {
    console.log(`📸 ${i + 1}/${diagrams.length}: ${diagrams[i]} kaydediliyor...`);

    // Sekmeye tıkla
    await page.click(`nav button:nth-of-type(${i + 1})`);
    await page.waitForTimeout(1000); // Render için bekle

    // Sadece diyagram alanının screenshot'ını al
    const element = await page.$('.bg-white.shadow-2xl');
    await element.screenshot({
      path: `diagram-${i + 1}-${diagrams[i].toLowerCase().replace(/\s+/g, '-').replace(/\//g, '-')}.png`
    });
  }

  console.log('✅ Tüm diyagramlar kaydedildi!');
  await browser.close();
})();
