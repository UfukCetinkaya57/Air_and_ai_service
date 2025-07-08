import requests
import json
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv('config/.env')

def test_prediction_endpoint():
    """Prediction endpoint'ine POST isteği testi"""
    
    # Çevre değişkenlerini al
    team_name = os.getenv('TEAM_NAME')
    password = os.getenv('PASSWORD')
    server_url = os.getenv('EVALUATION_SERVER_URL')
    
    print(f"🔬 PREDICTION ENDPOINT POST TESTİ")
    print(f"=================================")
    print(f"Takım: {team_name}")
    print(f"Sunucu: {server_url}")
    print()
    
    # 1. Önce kimlik doğrulama yapıp token al
    try:
        print("1️⃣ Token alınıyor...")
        auth_url = f"{server_url}/auth/"
        auth_data = {
            "username": team_name,
            "password": password
        }
        
        response = requests.post(auth_url, json=auth_data, timeout=10)
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data['token']
            print(f"✅ Token alındı: {token}")
            
            # Header'ı hazırla
            headers = {'Authorization': f'Token {token}'}
            
        else:
            print(f"❌ Token alma hatası: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Token alma hatası: {e}")
        return False
    
    # 2. Prediction endpoint'ine örnek POST isteği gönder
    try:
        print("\n2️⃣ Prediction endpoint'ine POST isteği gönderiliyor...")
        
        prediction_url = f"{server_url}/prediction/"
        
        # Örnek prediction verisi (Teknofest formatına uygun)
        sample_prediction = {
            "id": 1,
            "user": f"http://havaciliktayapayzeka.teknofest.org/users/{team_name}/",
            "frame": "http://havaciliktayapayzeka.teknofest.org/frames/4897/",
            "detected_objects": [
                {
                    "cls": "http://havaciliktayapayzeka.teknofest.org/classes/1/",
                    "landing_status": "-1",
                    "top_left_x": 262.87,
                    "top_left_y": 734.47,
                    "bottom_right_x": 405.2,
                    "bottom_right_y": 847.3
                }
            ],
            "detected_translations": [
                {
                    "translation_x": 0.02,
                    "translation_y": 0.01,
                    "translation_z": 0.03
                }
            ]
        }
        
        print(f"📦 Gönderilen veri:")
        print(json.dumps(sample_prediction, indent=2, ensure_ascii=False))
        
        response = requests.post(
            prediction_url, 
            json=sample_prediction, 
            headers=headers, 
            timeout=30
        )
        
        print(f"\n📡 Yanıt:")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200 or response.status_code == 201:
            print("✅ Prediction başarıyla gönderildi!")
            try:
                result = response.json()
                print(f"Sunucu yanıtı: {json.dumps(result, indent=2, ensure_ascii=False)}")
            except:
                print(f"Sunucu yanıtı (text): {response.text}")
                
        elif response.status_code == 400:
            print("⚠️ Bad Request (400) - Veri formatı hatası")
            print(f"Hata detayı: {response.text}")
            
        elif response.status_code == 403:
            print("🔒 Permission Denied (403) - Yetki hatası")
            print(f"Hata detayı: {response.text}")
            
        elif response.status_code == 401:
            print("🔑 Unauthorized (401) - Kimlik doğrulama hatası")
            print(f"Hata detayı: {response.text}")
            
        else:
            print(f"❌ Beklenmeyen hata: {response.status_code}")
            print(f"Yanıt: {response.text}")
            
    except Exception as e:
        print(f"❌ POST isteği hatası: {e}")
        return False
    
    # 3. Alternatif formatlarla deneme
    try:
        print("\n3️⃣ Alternatif format ile deneme...")
        
        # Daha basit format
        simple_prediction = {
            "frame": "http://havaciliktayapayzeka.teknofest.org/frames/4897/",
            "detected_objects": [
                {
                    "cls": 1,
                    "landing_status": -1,
                    "top_left_x": 262.87,
                    "top_left_y": 734.47,
                    "bottom_right_x": 405.2,
                    "bottom_right_y": 847.3
                }
            ],
            "detected_translations": [
                {
                    "translation_x": 0.02,
                    "translation_y": 0.01,
                    "translation_z": 0.03
                }
            ]
        }
        
        print(f"📦 Alternatif veri formatı:")
        print(json.dumps(simple_prediction, indent=2, ensure_ascii=False))
        
        response = requests.post(
            prediction_url, 
            json=simple_prediction, 
            headers=headers, 
            timeout=30
        )
        
        print(f"\n📡 Alternatif format yanıtı:")
        print(f"Status Code: {response.status_code}")
        print(f"Yanıt: {response.text[:500]}...")
        
    except Exception as e:
        print(f"❌ Alternatif format test hatası: {e}")
    
    print("\n🎉 Prediction endpoint testi tamamlandı!")
    return True

if __name__ == "__main__":
    test_prediction_endpoint() 