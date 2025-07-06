import requests
import json

BASE_URL = "http://127.0.0.25:5000"

def test_frame_list_format():
    """Frame listesi formatını test eder"""
    print("🚀 FRAME LİSTESİ FORMATI TESTİ")
    print("=" * 50)
    
    # Şartnamede belirtilen frame listesi formatı
    test_data = [
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
    ]
    
    print("📋 Gönderilen Frame Listesi:")
    for i, frame in enumerate(test_data):
        print(f"  Frame {i+1}: {frame['url']}")
        print(f"    Health Status: {frame['health_status']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/results/",
            json={"frames": test_data},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\n✅ POST /results/ Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Frame listesi formatı başarıyla kabul edildi!")
            print(f"✅ Sunucu Yanıtı:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"❌ Hata: {response.text}")
            
    except Exception as e:
        print(f"❌ Test hatası: {e}")

if __name__ == "__main__":
    test_frame_list_format() 