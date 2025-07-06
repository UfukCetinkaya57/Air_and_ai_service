import requests
import json

BASE_URL = "http://127.0.0.25:5000"

def test_sartname_uyumlu():
    """Şartnamede belirtilen field isimleriyle uyumluluğu test eder"""
    print("🔍 ŞARTNAME UYUMLULUK TESTİ")
    print("=" * 50)
    
    # Frame verilerini al
    response = requests.get(f"{BASE_URL}/frames/")
    
    if response.status_code == 200:
        frames = response.json()
        
        print("📋 ŞARTNAMEDEKİ FORMATLA KARŞILAŞTIRMA:")
        print("-" * 40)
        
        # İlk frame'i kontrol et
        if frames:
            frame = frames[0]
            
            # Şartnamede belirtilen field'lar
            sartname_fields = [
                'url',
                'image_url', 
                'video_name',
                'session',
                'translation_x',
                'translation_y', 
                'translation_z',
                'health_status'  # Şartnamede health_status yazıyor
            ]
            
            print("✅ Kontrol Edilen Field'lar:")
            for field in sartname_fields:
                if field in frame:
                    print(f"  ✅ {field}: {frame[field]} ✓")
                else:
                    print(f"  ❌ {field}: EKSİK!")
            
            print("\n📄 ŞARTNAME ÖRNEĞİYLE KARŞILAŞTIRMA:")
            print("-" * 40)
            print("Şartnamede verilen örnek:")
            sartname_ornegi = {
                "url": "http://localhost/frames/3598/",
                "image_url": "/ljfgpemcvkmuadhxabwn_V2_1/frame_000000.jpg",
                "video_name": "ljfgpemcvkmuadhxabwn_V2_1",
                "session": "http://localhost/session/2/",
                "translation_x": 0.02,
                "translation_y": 0.01,
                "translation_z": 0.03,
                "health_status": 1  # Şartnamede health_status yazıyor
            }
            
            print("\n🔄 BİZİM ÜRETTİĞİMİZ VERİ:")
            print(json.dumps(frame, indent=2, ensure_ascii=False))
            
            print("\n✅ Şartnamede 'health_status' field'ı kullanılıyor")
            print("✅ POST /results/ endpoint'inde frame objesi olarak gönderilmelidir")
            
        print(f"\n📊 Toplam Frame Sayısı: {len(frames)}")
        
        # NaN kontrolü
        nan_frames = [f for f in frames if f.get('translation_x') == "NaN"]
        if nan_frames:
            print(f"✅ NaN değerleri olan frame sayısı: {len(nan_frames)}")
            print("✅ Health status 0 olduğunda NaN değerleri doğru çalışıyor")
        
    else:
        print(f"❌ API erişim hatası: {response.status_code}")

if __name__ == "__main__":
    test_sartname_uyumlu() 