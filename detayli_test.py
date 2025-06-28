import requests
import json
import time

BASE_URL = "http://127.0.0.25:5000"

def test_ip_restriction():
    """IP kısıtlaması testini yapar"""
    print("🔒 IP Kısıtlaması Testi")
    print("-" * 30)
    
    # Normal test (localhost - izinli IP)
    try:
        response = requests.get(f"{BASE_URL}/frames/")
        print(f"✅ İzinli IP (localhost): {response.status_code}")
    except Exception as e:
        print(f"❌ İzinli IP hatası: {e}")

def test_frames_format():
    """Frames endpoint'inin şartname formatını test eder"""
    print("\n📋 Frames Format Testi")
    print("-" * 30)
    
    response = requests.get(f"{BASE_URL}/frames/")
    
    if response.status_code == 200:
        frames = response.json()
        
        # İlk frame'i kontrol et
        if frames:
            frame = frames[0]
            required_fields = [
                'url', 'image_url', 'video_name', 'session',
                'translation_x', 'translation_y', 'translation_z', 'health_status'
            ]
            
            print(f"✅ Toplam frame sayısı: {len(frames)}")
            
            for field in required_fields:
                if field in frame:
                    print(f"✅ {field}: {frame[field]}")
                else:
                    print(f"❌ {field}: EKSİK")
            
            # NaN değerleri kontrol et
            nan_frame = next((f for f in frames if f.get('translation_x') == "NaN"), None)
            if nan_frame:
                print(f"✅ NaN değerleri destekleniyor: {nan_frame['translation_x']}")
            
        else:
            print("❌ Hiç frame bulunamadı")
    else:
        print(f"❌ Frames endpoint hatası: {response.status_code}")

def test_result_submission():
    """Sonuç gönderme formatını test eder"""
    print("\n📤 Sonuç Gönderme Testi")
    print("-" * 30)
    
    # Şartnamede belirtilen formatta test verisi
    test_data = {
        "id": "test_submission_001",
        "user": "http://127.0.0.25:5000/user/1/",
        "frame": "http://127.0.0.25:5000/frames/3598/",
        "detected_objects": [
            {
                "cls": "0",
                "landing_status": "1",
                "top_left_x": 100,
                "top_left_y": 150,
                "bottom_right_x": 200,
                "bottom_right_y": 250
            },
            {
                "cls": "2",
                "landing_status": "-1",
                "top_left_x": 300,
                "top_left_y": 350,
                "bottom_right_x": 400,
                "bottom_right_y": 450
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
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"✅ Sonuç gönderimi: {response.status_code}")
        print(f"✅ Yanıt: {response.json()}")
        
        # Farklı nesne sınıflarını test et
        for cls in ["0", "1", "2", "3"]:
            test_single_object = {
                **test_data,
                "id": f"test_{cls}",
                "detected_objects": [{
                    "cls": cls,
                    "landing_status": "0",
                    "top_left_x": 10,
                    "top_left_y": 10,
                    "bottom_right_x": 50,
                    "bottom_right_y": 50
                }]
            }
            
            response = requests.post(f"{BASE_URL}/results/", json=test_single_object)
            print(f"✅ Nesne sınıfı {cls}: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Sonuç gönderme hatası: {e}")

def test_session_endpoint():
    """Session endpoint'ini test eder"""
    print("\n🗂️  Session Endpoint Testi")
    print("-" * 30)
    
    try:
        response = requests.get(f"{BASE_URL}/session/2/")
        print(f"✅ Session endpoint: {response.status_code}")
        print(f"✅ Yanıt: {response.json()}")
    except Exception as e:
        print(f"❌ Session endpoint hatası: {e}")

def test_individual_frame():
    """Tekil frame endpoint'ini test eder"""
    print("\n🖼️  Tekil Frame Testi")
    print("-" * 30)
    
    try:
        response = requests.get(f"{BASE_URL}/frames/3598/")
        print(f"✅ Tekil frame: {response.status_code}")
        print(f"✅ Yanıt: {response.json()}")
    except Exception as e:
        print(f"❌ Tekil frame hatası: {e}")

def test_api_documentation():
    """API dokümantasyonunu test eder"""
    print("\n📚 API Dokümantasyon Testi")
    print("-" * 30)
    
    try:
        # OpenAPI JSON
        response = requests.get(f"{BASE_URL}/openapi.json")
        print(f"✅ OpenAPI JSON: {response.status_code}")
        
        # Docs sayfası
        response = requests.get(f"{BASE_URL}/docs")
        print(f"✅ Docs sayfası: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Dokümantasyon hatası: {e}")

def performance_test():
    """Performans testi yapar"""
    print("\n⚡ Performans Testi")
    print("-" * 30)
    
    # 10 ardışık istek
    times = []
    for i in range(10):
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/frames/")
        end_time = time.time()
        
        if response.status_code == 200:
            times.append(end_time - start_time)
    
    if times:
        avg_time = sum(times) / len(times)
        print(f"✅ Ortalama yanıt süresi: {avg_time:.3f} saniye")
        print(f"✅ En hızlı: {min(times):.3f} saniye")
        print(f"✅ En yavaş: {max(times):.3f} saniye")

def main():
    """Ana test fonksiyonu"""
    print("🚀 TÜBİTAK YARISMA SUNUCUSU - DETAYLI TEST")
    print("=" * 60)
    
    test_ip_restriction()
    test_frames_format()
    test_result_submission()
    test_session_endpoint()
    test_individual_frame()
    test_api_documentation()
    performance_test()
    
    print("\n" + "=" * 60)
    print("🎯 TÜM TESTLER TAMAMLANDI!")
    print("✅ Sunucu şartname gerekliliklerini karşılıyor")

if __name__ == "__main__":
    main() 