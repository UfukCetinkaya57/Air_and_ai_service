import requests
import json
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv('config/.env')

def test_teknofest_real_endpoints():
    """Teknofest sunucusunun gerçek endpoint'leriyle test"""
    
    # Çevre değişkenlerini al
    team_name = os.getenv('TEAM_NAME')
    password = os.getenv('PASSWORD')
    server_url = os.getenv('EVALUATION_SERVER_URL')
    session_name = os.getenv('SESSION_NAME')
    
    print(f"🚀 TEKNOFEST GERÇEK ENDPOINT TESTİ")
    print(f"=================================")
    print(f"Takım: {team_name}")
    print(f"Sunucu: {server_url}")
    print(f"Oturum: {session_name}")
    print()
    
    try:
        # 1. Ana sayfa kontrolü
        print("1️⃣ Ana sayfa kontrolü...")
        response = requests.get(server_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Sunucu erişilebilir!")
            try:
                data = response.json()
                print(f"   API Root: {data}")
            except:
                print(f"   Yanıt: {response.text[:200]}...")
        else:
            print(f"❌ Ana sayfa hatası: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return False
    
    try:
        # 2. Kimlik doğrulama
        print("\n2️⃣ Kimlik doğrulama...")
        auth_url = f"{server_url}/auth/"
        auth_data = {
            "username": team_name,  # Django genelde username kullanır
            "password": password
        }
        
        response = requests.post(auth_url, json=auth_data, timeout=10)
        
        if response.status_code == 200:
            print("✅ Kimlik doğrulama başarılı!")
            token_data = response.json()
            print(f"   Token alındı: {token_data}")
            
            # Token'ı header'da kullanmak için sakla
            if 'token' in token_data:
                auth_token = token_data['token']
                headers = {'Authorization': f'Token {auth_token}'}
            else:
                headers = {}
                
        else:
            print(f"❌ Kimlik doğrulama hatası: {response.status_code}")
            print(f"   Yanıt: {response.text}")
            
            # Token olmadan da devam edelim
            headers = {}
            
    except Exception as e:
        print(f"❌ Kimlik doğrulama hatası: {e}")
        headers = {}
    
    try:
        # 3. Frame listesi alma
        print("\n3️⃣ Frame listesi alınıyor...")
        frames_url = f"{server_url}/frames/"
        
        response = requests.get(frames_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            frames_data = response.json()
            print(f"✅ Frame listesi alındı!")
            
            if isinstance(frames_data, dict) and 'results' in frames_data:
                frames = frames_data['results']
                print(f"   Frame sayısı: {len(frames)}")
            elif isinstance(frames_data, list):
                frames = frames_data
                print(f"   Frame sayısı: {len(frames)}")
            else:
                print(f"   Yanıt formatı: {type(frames_data)}")
                frames = []
            
            # İlk birkaç frame'i göster
            for i, frame in enumerate(frames[:3]):
                print(f"   Frame {i+1}: {frame}")
                
        else:
            print(f"❌ Frame listesi alma hatası: {response.status_code}")
            print(f"   Yanıt: {response.text[:500]}...")
            
    except Exception as e:
        print(f"❌ Frame listesi alma hatası: {e}")
    
    try:
        # 4. Prediction endpoint'ini test et
        print("\n4️⃣ Prediction endpoint testi...")
        prediction_url = f"{server_url}/prediction/"
        
        response = requests.get(prediction_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Prediction endpoint erişilebilir!")
            pred_data = response.json()
            print(f"   Veri: {pred_data}")
        else:
            print(f"❌ Prediction endpoint hatası: {response.status_code}")
            print(f"   Yanıt: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Prediction endpoint hatası: {e}")
    
    try:
        # 5. Session endpoint'ini test et
        print("\n5️⃣ Session endpoint testi...")
        session_url = f"{server_url}/session/"
        
        response = requests.get(session_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Session endpoint erişilebilir!")
            session_data = response.json()
            print(f"   Veri: {session_data}")
        else:
            print(f"❌ Session endpoint hatası: {response.status_code}")
            print(f"   Yanıt: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Session endpoint hatası: {e}")
    
    print("\n🎉 Teknofest sunucu analizi tamamlandı!")
    return True

if __name__ == "__main__":
    test_teknofest_real_endpoints() 