# React Diyagramlarını PNG Olarak Kaydetme Talimatları

## En Hızlı Yöntem: Tarayıcı Ekran Görüntüsü

### Adım 1: Kodu Çalıştır
1. https://stackblitz.com/edit/react adresine git
2. `src/App.js` dosyasını aç
3. Tüm içeriği sil ve kodunuzu yapıştır
4. `lucide-react` paketini kur: Terminal'de `npm install lucide-react` çalıştır

### Adım 2: Her Diyagramı PNG Olarak Kaydet
1. Her sekmeyi tıklayarak diyagramı görüntüle
2. **Windows:** `Win + Shift + S` tuşlarına bas (Ekran Alıntısı)
3. Diyagramı seç ve kaydet
4. Dosya adı: `diagram-1-ana-sistem.png`, `diagram-2-cantera.png`, vb.

---

## Alternatif: HTML + Tarayıcı Yöntemi

### Adım 1: Standalone HTML Oluştur
Kodu tam standalone HTML olarak kaydet (tailwind CDN ile)

### Adım 2: Chrome DevTools ile PNG Kaydet
1. HTML dosyasını Chrome'da aç
2. `F12` bas (DevTools aç)
3. `Ctrl + Shift + P` → "Capture full size screenshot" yaz
4. Enter'a bas

---

## Profesyonel Yöntem: Puppeteer Script

```javascript
// save-diagrams.js
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  await page.goto('file:///C:/@biyokomurlestirme/algorithm-flowcharts.html');
  
  for (let i = 0; i < 8; i++) {
    await page.click(`button:nth-of-type(${i + 1})`);
    await page.waitForTimeout(500);
    await page.screenshot({ 
      path: `diagram-${i + 1}.png`,
      fullPage: false,
      clip: { x: 256, y: 0, width: 1200, height: 1000 }
    });
  }
  
  await browser.close();
})();
```

Çalıştırmak için:
```bash
npm install puppeteer
node save-diagrams.js
```
