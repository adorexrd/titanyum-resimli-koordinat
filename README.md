# 🗺️ Adorexrd Resimli Koordinat Botu

Bu proje, [kordinat-bot](https://github.com/adorexrd/kordinat-bot) için geliştirilmiş **ek bir bot**tur.  
Sonoyuncu Titanyum Casus ekran görüntülerini OCR ile okuyarak koordinat, dünya adı, claim sayısı ve kalan süre bilgilerini çıkartır, MongoDB veritabanındaki hesaplarla karşılaştırır ve en yakın hesapları embed olarak gösterir.

---

## 📂 Dosyalar

- **main.py** → Botun ana kodu  
- **kurulum.bat** → İlk kurulum için
- **baslat.bat** → Botu başlatmak için kolay başlatıcı

---

## 🔑 Gereksinimler

- **Python 3.10+** (PATH'e eklenmiş olmalı)
- **MongoDB** (hesap verilerini saklamak için)
- [kordinat-bot](https://github.com/adorexrd/kordinat-bot) → Hesap ekleme/silme işlemleri burada yapılır
- Discord bot token

---

## ⚙️ Kurulum

1. **kordinat-bot**’u kur ve MongoDB bağlantısını ayarla.
   Oradaki `/hesapekle` komutu ile hesap ekleyip veritabanını oluştur.

2. Bu botun `main.py` dosyasındaki ayarları yap:
   ```python
   TOKEN = "BOT_TOKENINIZ"
   MONGO_URI = "mongodb://localhost:27017"
   KODUN_CALISACAGI_KANAL_ID = 123456789012345678

--- 

## ❗ ÖNEMLİ! 

- **Botta Hata Olabilir.** (Bu Botu Kuracaksınız Tavsiyem Ana Koordinat Botunuda Kurmanız. Bu Bot Tek Başına Stabil Çalışmayabilir.)
