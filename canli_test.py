import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.25:5000"

def servis_durumu():
    """Servis durumunu kontrol eder"""
    print("🔍 SERVİS DURUM KONTROLÜ")
    print("=" * 40)
    
    try:
        # Ana sayfa
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Ana Sayfa: {response.status_code}")
        print(f"   {response.json()}")
        
        # Health check
        response = requests.get(f"{BASE_URL}/health/")
        print(f"✅ Sağlık Kontrolü: {response.status_code}")
        print(f"   {response.json()}")
        
        return True
    except Exception as e:
        print(f"❌ Servis erişim hatası: {e}")
        return False

def frame_listesi_al():
    """Frame listesini alır ve gösterir"""
    print("\n📋 FRAME LİSTESİ")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/frames/")
        if response.status_code == 200:
            frames = response.json()
            print(f"Toplam Frame Sayısı: {len(frames)}")
            
            for i, frame in enumerate(frames):
                print(f"\nFrame {i+1}:")
                print(f"  URL: {frame['url']}")
                print(f"  Görsel: {frame['image_url']}")
                print(f"  Video: {frame['video_name']}")
                print(f"  Health Status: {frame['health_status']}")
                print(f"  Pozisyon: X={frame['translation_x']}, Y={frame['translation_y']}, Z={frame['translation_z']}")
            
            return frames
        else:
            print(f"❌ Frame listesi alınamadı: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Frame listesi hatası: {e}")
        return []

def ornek_sonuc_gonder():
    """Örnek tespit sonucu gönderir"""
    print("\n📤 ÖRNEK SONUÇ GÖNDERİMİ")
    print("=" * 40)
    
    # Örnek tespit sonucu
    timestamp = int(time.time())
    ornek_sonuc = {
        "id": f"test_detection_{timestamp}",
        "user": f"{BASE_URL}/user/test_team/",
        "frame": [
            {
                "url": f"{BASE_URL}/frames/3598/",
                "image_url": "/ljfgpemcvkmuadhxabwn_V2_1/frame_000000.jpg",
                "video_name": "ljfgpemcvkmuadhxabwn_V2_1",
                "session": f"{BASE_URL}/session/2/",
                "translation_x": 0.02,
                "translation_y": 0.01,
                "translation_z": 0.03,
                "health_status": 1
            },
            {
                "url": f"{BASE_URL}/frames/4787/",
                "image_url": "/ljfgpemcvkmuadhxabwn_V2_1/frame_000004.jpg",
                "video_name": "ljfgpemcvkmuadhxabwn_V2_1",
                "session": f"{BASE_URL}/session/2/",
                "translation_x": 0.01,
                "translation_y": 0.02,
                "translation_z": 0.01,
                "health_status": 1
            },
            {
                "url": f"{BASE_URL}/frames/3916/",
                "image_url": "/ljfgpemcvkmuadhxabwn_V2_1/frame_000008.jpg",
                "video_name": "ljfgpemcvkmuadhxabwn_V2_1",
                "session": f"{BASE_URL}/session/2/",
                "translation_x": "NaN",
                "translation_y": "NaN",
                "translation_z": "NaN",
                "health_status": 0
            }
        ],
        "detected_objects": [
            {
                "cls": "1",
                "landing_status": "1",
                "top_left_x": 150,
                "top_left_y": 200,
                "bottom_right_x": 250,
                "bottom_right_y": 300
            },
            {
                "cls": "2",
                "landing_status": "0",
                "top_left_x": 400,
                "top_left_y": 100,
                "bottom_right_x": 500,
                "bottom_right_y": 200
            }
        ],
        "detected_translations": [
            {
                "translation_x": 0.025,
                "translation_y": 0.018,
                "translation_z": 0.012
            }
        ]
    }
    
    print("Gönderilen veri:")
    print(json.dumps(ornek_sonuc, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(
            f"{BASE_URL}/results/",
            json=ornek_sonuc,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\n✅ Gönderim Sonucu: {response.status_code}")
        print(f"✅ Sunucu Yanıtı: {response.json()}")
        
    except Exception as e:
        print(f"❌ Sonuç gönderim hatası: {e}")

def api_dokumantasyonu():
    """API dokümantasyon linklerini gösterir"""
    print("\n📚 API DOKÜMANTASYONU")
    print("=" * 40)
    print(f"🔗 Swagger UI: {BASE_URL}/docs")
    print(f"🔗 ReDoc: {BASE_URL}/redoc")
    print(f"🔗 OpenAPI JSON: {BASE_URL}/openapi.json")

def interaktif_menu():
    """Interaktif test menüsü"""
    print("\n" + "="*50)
    print("🚀 TÜBİTAK YARISMA SERVİSİ - CANLI TEST")
    print("="*50)
    
    while True:
        print("\nNe yapmak istiyorsunuz?")
        print("1. 🔍 Servis durumunu kontrol et")
        print("2. 📋 Frame listesini al")
        print("3. 📤 Örnek sonuç gönder")
        print("4. 📚 API dokümantasyon linkleri")
        print("5. ❌ Çıkış")
        
        secim = input("\nSeçiminiz (1-5): ").strip()
        
        if secim == "1":
            servis_durumu()
        elif secim == "2":
            frame_listesi_al()
        elif secim == "3":
            ornek_sonuc_gonder()
        elif secim == "4":
            api_dokumantasyonu()
        elif secim == "5":
            print("\n👋 Test tamamlandı!")
            break
        else:
            print("❌ Geçersiz seçim! Lütfen 1-5 arası bir sayı girin.")

if __name__ == "__main__":
    # Önce servis durumunu kontrol et
    if servis_durumu():
        print("\n✅ Servis çalışıyor! Interaktif teste devam edebilirsiniz.")
        interaktif_menu()
    else:
        print("\n❌ Servis çalışmıyor! Lütfen önce 'python main.py' ile servisi başlatın.") 