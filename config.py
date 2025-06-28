from typing import List

class Settings:
    """Sunucu ayarları"""
    HOST = "127.0.0.25"  # Şartnamede belirtilen format
    PORT = 5000
    
    # İzinli IP adresleri - yarışma sırasında güncellenecek
    ALLOWED_IPS: List[str] = [
        "127.0.0.1",  # Test için localhost
        "192.168.1.100",  # Örnek takım IP'si
        "192.168.1.101",  # Örnek takım IP'si
    ]
    
    # Session ve frame base URL'leri
    BASE_URL = f"http://{HOST}:{PORT}"
    FRAMES_BASE_URL = f"{BASE_URL}/frames"
    SESSION_BASE_URL = f"{BASE_URL}/session"

settings = Settings() 