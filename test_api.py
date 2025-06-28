import requests
import json

# Test URL'leri
BASE_URL = "http://127.0.0.25:5000"

def test_api():
    """API endpoint'lerini test eder"""
    
    print("🚀 TÜBİTAK Yarışma Sunucusu API Testi")
    print("=" * 50)
    
    # 1. Ana sayfa testi
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Ana sayfa: {response.status_code}")
        print(f"   Yanıt: {response.json()}")
    except Exception as e:
        print(f"❌ Ana sayfa hatası: {e}")
    
    print("-" * 50)
    
    # 2. Frames endpoint testi
    try:
        response = requests.get(f"{BASE_URL}/frames/")
        print(f"✅ Frames endpoint: {response.status_code}")
        if response.status_code == 200:
            frames = response.json()
            print(f"   Toplam frame sayısı: {len(frames)}")
            print(f"   İlk frame: {frames[0] if frames else 'Yok'}")
        else:
            print(f"   Hata: {response.text}")
    except Exception as e:
        print(f"❌ Frames endpoint hatası: {e}")
    
    print("-" * 50)
    
    # 3. Health check testi
    try:
        response = requests.get(f"{BASE_URL}/health/")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Yanıt: {response.json()}")
    except Exception as e:
        print(f"❌ Health check hatası: {e}")
    
    print("-" * 50)
    
    # 4. Results endpoint testi (POST)
    test_result = {
        "id": "test_123",
        "user": "test_user",
        "frame": f"{BASE_URL}/frames/3598/",
        "detected_objects": [
            {
                "cls": "1",
                "landing_status": "1",
                "top_left_x": 100,
                "top_left_y": 150,
                "bottom_right_x": 200,
                "bottom_right_y": 250
            }
        ],
        "detected_translations": [
            {
                "translation_x": 0.05,
                "translation_y": 0.03,
                "translation_z": 0.02
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/results/", 
            json=test_result,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Results POST: {response.status_code}")
        print(f"   Yanıt: {response.json()}")
    except Exception as e:
        print(f"❌ Results POST hatası: {e}")
    
    print("=" * 50)
    print("🎯 Test tamamlandı!")

if __name__ == "__main__":
    test_api() 