<script setup lang="ts">
import { ref } from 'vue';

// Örnek sipariş verisi (Backend'den veya Store'dan gelen)
const siparisVerisi = ref({
  masa: "Masa 5",
  tarih: "16.11.2025 14:30",
  urunler: [
    { ad: "Çay", adet: 2, fiyat: 15 },
    { ad: "Türk Kahvesi", adet: 1, fiyat: 40 },
    { ad: "Su", adet: 1, fiyat: 10 }
  ],
  toplam: 80
});

// --- YAZDIRMA FONKSİYONU (Kütüphanesiz) ---
const adisyonYazdir = (data: Record<string, string>) => {
  // 1. Adım: Yazdırılacak HTML şablonunu oluştur (CSS dahil)
  // Not: Termal yazıcılar için CSS'i burada inline veya style tag içinde vermeliyiz.
  // Dışarıdaki style dosyalarını iframe görmez.
  const htmlContent = `
    <html>
      <head>
        <title>Adisyon</title>
        <style>
          body { font-family: 'Courier New', monospace; width: 80mm; margin: 0; padding: 0; font-size: 12px; }
          .header { text-align: center; margin-bottom: 10px; }
          .bold { font-weight: bold; }
          .line { border-bottom: 1px dashed #000; margin: 5px 0; }
          .item-row { display: flex; justify-content: space-between; }
          .footer { text-align: center; margin-top: 20px; font-size: 10px; }
        </style>
      </head>
      <body>
        <div class="header">
          <div class="bold">CAFE VUE POS</div>
          <div>${data.tarih}</div>
          <div>${data.masa}</div>
        </div>
        
        <div class="line"></div>
        
        ${data.urunler?.map(urun => `
          <div class="item-row">
            <span>${urun.adet}x ${urun.ad}</span>
            <span>${urun.adet * urun.fiyat} TL</span>
          </div>
        `).join('') || ''}
        
        <div class="line"></div>
        
        <div class="item-row bold" style="font-size: 14px;">
          <span>TOPLAM</span>
          <span>${data.toplam} TL</span>
        </div>
        
        <div class="footer">
          Bizi tercih ettiğiniz için teşekkürler.<br>
          Mali Değeri Yoktur
        </div>
      </body>
    </html>
  `;

  // 2. Adım: Görünmez Iframe Oluştur
  const iframe = document.createElement('iframe');
  
  // Iframe'i gizle (display: none bazen sorun yaratır, o yüzden absolute ile uçuruyoruz)
  iframe.style.position = 'absolute';
  iframe.style.width = '0px';
  iframe.style.height = '0px';
  iframe.style.left = '-9999px';
  iframe.style.top = '-9999px';
  
  document.body.appendChild(iframe);

  // 3. Adım: İçeriği Yaz ve Yazdır
  const doc = iframe.contentWindow.document;
  doc.open();
  doc.write(htmlContent);
  doc.close();

  // Iframe içeriğinin (resimlerin vs) render edilmesini bekle
  // Basit metinler için setTimeout yeterlidir.
  iframe.contentWindow.focus(); // Bazı tarayıcılar için focus gerekir
  setTimeout(() => {
    iframe.contentWindow.print();
    
    // 4. Adım: Temizlik (Clean-up)
    // Yazdırma diyaloğu kapandıktan sonra iframe'i siliyoruz (tahmini süre)
    setTimeout(() => {
      document.body.removeChild(iframe);
    }, 1000); // Kullanıcı diyaloğu kapatana kadar bekler, sonra siler
  }, 500);
};
</script>

<template>
  <div class="p-5">
    <h1>Sipariş Listesi</h1>
    <ul>
      <li v-for="urun in siparisVerisi.urunler" :key="urun.ad">
        {{ urun.ad }}
      </li>
    </ul>

    <button @click="adisyonYazdir(siparisVerisi)" class="btn-primary">
      Adisyon Yazdır (Gizli Render)
    </button>
  </div>
</template>