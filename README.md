# TÜBİTAK Havacılık ve Yapay Zeka Yarışması Sunucusu

Bu proje, TÜBİTAK Havacılık ve Yapay Zeka yarışması için şartnamede belirtilen API sunucusunu içerir.

## 🎯 Özellikler

- **Şartname Uyumlu**: Yarışma şartnamesinde belirtilen JSON formatları
- **IP Kısıtlaması**: Sadece belirlenen IP adreslerinden erişim
- **FastAPI**: Modern, hızlı ve otomatik dokümantasyon
- **RESTful API**: Standart HTTP metodları

## 📋 API Endpoint'leri

### GET `/frames/`
Görüntü karelerinin listesini döndürür (şartnamede belirtilen format).

### POST `/results/`
Yarışmacıların tespit sonuçlarını kabul eder.

### GET `/session/{id}/`
Oturum bilgilerini döndürür.

### GET `/health/`
Sunucu durumunu kontrol eder.

## 🚀 Kurulum ve Çalıştırma

1. **Gereksinimleri yükleyin:**
```bash
pip install -r requirements.txt
```

2. **Sunucuyu başlatın:**
```bash
python main.py
```

3. **Sunucu adresi:**
```
http://127.0.0.25:5000
```

## ⚙️ Konfigürasyon

`config.py` dosyasında:
- Sunucu adresi ve port
- İzinli IP adresleri listesi
- Base URL ayarları

## 📊 Şartname Formatları

### Gönderilen Veri (Görüntü Bilgileri):
```json
{
  "url": "http://localhost/frames/3598/",
  "image_url": "/ljfgpemcvkmuadhxabwn_V2_1/frame_000000.jpg",
  "video_name": "ljfgpemcvkmuadhxabwn_V2_1",
  "session": "http://localhost/session/2/",
  "translation_x": 0.02,
  "translation_y": 0.01,
  "translation_z": 0.03,
  "health_status": 1
}
```

### Alınan Veri (Sonuçlar):
```json
{
  "id": "...",
  "user": "...",
  "frame": "...",
  "detected_objects": [...],
  "detected_translations": [...]
}
```

## 🔧 Geliştirme

- API dokümantasyonu: `http://127.0.0.25:5000/docs`
- İnteraktif test: `http://127.0.0.25:5000/redoc` 