import requests
import json
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv('config/.env')

def test_teknofest_connection():
    """Teknofest sunucusuna basit bağlantı testi"""
    
    # Çevre değişkenlerini al
    team_name = os.getenv('TEAM_NAME')
    password = os.getenv('PASSWORD')
    server_url = os.getenv('EVALUATION_SERVER_URL')
    session_name = os.getenv('SESSION_NAME')
    
    print(f"🚀 TEKNOFEST SUNUCU BAĞLANTI TESTİ")
    print(f"==================================")
    print(f"Takım: {team_name}")
    print(f"Sunucu: {server_url}")
    print(f"Oturum: {session_name}")
    print()
    
    try:
        # 1. Sağlık kontrolü
        print("1️⃣ Sunucu sağlık kontrolü...")
        health_url = f"{server_url}/health/"
        response = requests.get(health_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Sunucu sağlıklı!")
            print(f"   Yanıt: {response.json()}")
        else:
            print(f"❌ Sağlık kontrolü hatası: {response.status_code}")
            print(f"   Yanıt: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return False
    
    try:
        # 2. Kimlik doğrulama
        print("\n2️⃣ Kimlik doğrulama...")
        auth_url = f"{server_url}/auth/"
        auth_data = {
            "team_name": team_name,
            "password": password
        }
        
        response = requests.post(auth_url, json=auth_data, timeout=10)
        
        if response.status_code == 200:
            print("✅ Kimlik doğrulama başarılı!")
            print(f"   Yanıt: {response.json()}")
        else:
            print(f"❌ Kimlik doğrulama hatası: {response.status_code}")
            print(f"   Yanıt: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Kimlik doğrulama hatası: {e}")
        return False
    
    try:
        # 3. Frame listesi alma
        print("\n3️⃣ Frame listesi alınıyor...")
        frames_url = f"{server_url}/frames/"
        
        response = requests.get(frames_url, timeout=10)
        
        if response.status_code == 200:
            frames_data = response.json()
            print(f"✅ Frame listesi alındı! Frame sayısı: {len(frames_data)}")
            
            # İlk birkaç frame'i göster
            for i, frame in enumerate(frames_data[:3]):
                print(f"   Frame {i+1}: {frame.get('url', 'N/A')}")
                
        else:
            print(f"❌ Frame listesi alma hatası: {response.status_code}")
            print(f"   Yanıt: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Frame listesi alma hatası: {e}")
        return False
    
    print("\n🎉 Tüm testler başarılı! Teknofest sunucusuna bağlantı sağlandı.")
    return True

if __name__ == "__main__":
    test_teknofest_connection() 