import os
import requests
import json
import time
from dotenv import load_dotenv
import logging
from datetime import datetime
import cv2
import torch
import torchvision.transforms as transforms
from ultralytics import YOLO
from utils import CNN_LSTM, process_frames2

# Log yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('_logs/teknofest_client.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# .env dosyasını yükle
load_dotenv('config/.env')

class TeknofestClient:
    def __init__(self):
        self.team_name = os.getenv('TEAM_NAME')
        self.password = os.getenv('PASSWORD')
        self.server_url = os.getenv('EVALUATION_SERVER_URL')
        self.session_name = os.getenv('SESSION_NAME')
        
        # Session için requests session oluştur
        self.session = requests.Session()
        self.auth_token = None
        
        logger.info(f"Teknofest İstemci başlatılıyor...")
        logger.info(f"Takım: {self.team_name}")
        logger.info(f"Sunucu: {self.server_url}")
        logger.info(f"Oturum: {self.session_name}")
    
    def authenticate(self):
        """Sunucuya kimlik doğrulama"""
        try:
            auth_url = f"{self.server_url}/auth/"
            auth_data = {
                "username": self.team_name,  # Test sonucuna göre username kullanıyoruz
                "password": self.password
            }
            
            logger.info("Kimlik doğrulama yapılıyor...")
            response = self.session.post(auth_url, json=auth_data, timeout=15)
            
            if response.status_code == 200:
                token_data = response.json()
                self.auth_token = token_data['token']
                
                # Session header'ını güncelle
                self.session.headers.update({'Authorization': f'Token {self.auth_token}'})
                
                logger.info("Kimlik doğrulama başarılı!")
                logger.info(f"Token: {self.auth_token}")
                return True
            else:
                logger.error(f"Kimlik doğrulama hatası: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Kimlik doğrulama sırasında hata: {e}")
            return False
    
    def get_frames(self):
        """Sunucudan frame listesini al"""
        try:
            frames_url = f"{self.server_url}/frames/"
            
            logger.info("Frame listesi alınıyor...")
            response = self.session.get(frames_url, timeout=15)
            
            if response.status_code == 200:
                frames_data = response.json()
                
                # Django REST Framework pagination kontrolü
                if isinstance(frames_data, dict) and 'results' in frames_data:
                    frames = frames_data['results']
                elif isinstance(frames_data, list):
                    frames = frames_data
                else:
                    logger.warning(f"Beklenmeyen frame formatı: {type(frames_data)}")
                    frames = []
                
                logger.info(f"Frame listesi başarıyla alındı. Frame sayısı: {len(frames)}")
                return frames
            else:
                logger.error(f"Frame listesi alma hatası: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Frame listesi alınırken hata: {e}")
            return None
    
    def submit_prediction(self, prediction_data):
        """Tek bir prediction'ı sunucuya gönder"""
        try:
            prediction_url = f"{self.server_url}/prediction/"
            
            logger.info(f"Prediction gönderiliyor: Frame {prediction_data.get('frame', 'N/A')}")
            response = self.session.post(prediction_url, json=prediction_data, timeout=30)
            
            if response.status_code == 200 or response.status_code == 201:
                result = response.json()
                logger.info(f"Prediction başarıyla gönderildi! ID: {result.get('id', 'N/A')}")
                return result
            else:
                logger.error(f"Prediction gönderme hatası: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Prediction gönderilirken hata: {e}")
            return None

def process_frame_with_model(frame_data):
    """
    Gerçek modelinizle frame işleme fonksiyonu - Teknofest formatında
    """
    try:
        logger.info(f"Frame işleniyor: {frame_data.get('url', 'N/A')}")
        
        # Model yolları
        yolo_od_model_path = YOLO(
            r'G:\teknofest-suns-project\datasets\runs\train_dataset_v5\suns_dataset_v5main_exp12\weights\best.pt')
        translation_model_path = r"G:\teknofest-suns-project\models\yolov8_prediction\src\cnn_lstm_model.pth"

        # Frame verilerini al
        health_status = frame_data.get('gps_health_status', frame_data.get('health_status', 1))
        image_path = frame_data.get('image_url', '')
        
        # Translation verilerini frame'den al (Teknofest frame'lerinde olmayabilir)
        translation_xyz = {
            "translation_x": frame_data.get("translation_x", 0.0),
            "translation_y": frame_data.get("translation_y", 0.0),
            "translation_z": frame_data.get("translation_z", 0.0)
        }

        # Device ve transform ayarları
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        # Translation modelini yükle
        translation_model = CNN_LSTM(hidden_size=128, seq_length=5).to(device)
        translation_model.load_state_dict(torch.load(translation_model_path))
        translation_model.eval()

        # Frame'i işle
        detected_objects, translation_xyz = process_frames2(
            yolo_od_model_path, 
            translation_model, 
            image_path, 
            transform,
            device, 
            translation_xyz=translation_xyz,
            health_status=health_status
        )

        # Test sonuçlarına göre doğru Teknofest formatı
        prediction_result = {
            "frame": frame_data["url"],
            "detected_objects": [],
            "detected_translations": [translation_xyz]
        }
        
        # Detected objects'i Teknofest formatına çevir
        for obj in detected_objects:
            teknofest_obj = {
                "cls": f"http://havaciliktayapayzeka.teknofest.org/classes/{obj.get('cls', 1)}/",  # URL string olmalı
                "landing_status": str(obj.get('landing_status', '-1')),  # String olmalı
                "top_left_x": float(obj.get('top_left_x', 0.0)),
                "top_left_y": float(obj.get('top_left_y', 0.0)),
                "bottom_right_x": float(obj.get('bottom_right_x', 0.0)),
                "bottom_right_y": float(obj.get('bottom_right_y', 0.0))
            }
            prediction_result["detected_objects"].append(teknofest_obj)
        
        logger.info(f"Frame başarıyla işlendi: {len(detected_objects)} nesne tespit edildi")
        return prediction_result
        
    except Exception as e:
        logger.error(f"Model işleme hatası: {e}")
        # Hata durumunda varsayılan sonuç döndür
        return {
            "frame": frame_data.get("url", ""),
            "detected_objects": [],
            "detected_translations": [
                {
                    "translation_x": 0.0,
                    "translation_y": 0.0,
                    "translation_z": 0.0
                }
            ]
        }

def main():
    """Ana çalışma fonksiyonu"""
    # Log klasörünü oluştur
    os.makedirs('_logs', exist_ok=True)
    
    # İstemciyi başlat
    client = TeknofestClient()
    
    # Kimlik doğrulama
    if not client.authenticate():
        logger.error("Kimlik doğrulama başarısız!")
        return
    
    # Frame listesini al
    frames = client.get_frames()
    if not frames:
        logger.warning("Frame listesi boş veya alınamadı!")
        
        # Test için örnek bir frame ile devam et
        logger.info("Test prediction gönderiliyor...")
        test_prediction = {
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
        
        result = client.submit_prediction(test_prediction)
        if result:
            logger.info("Test prediction başarıyla gönderildi!")
        else:
            logger.error("Test prediction gönderilemedi!")
        return
    
    # Her frame için işlem yap
    success_count = 0
    error_count = 0
    
    for i, frame in enumerate(frames):
        try:
            logger.info(f"Frame {i+1}/{len(frames)} işleniyor: {frame.get('url', 'N/A')}")
            
            # Kendi modelinizle frame'i işleyin
            prediction = process_frame_with_model(frame)
            
            # Sonucu gönder
            response = client.submit_prediction(prediction)
            if response:
                success_count += 1
                logger.info(f"Frame {i+1} için sonuç başarıyla gönderildi (ID: {response.get('id', 'N/A')})")
            else:
                error_count += 1
                logger.error(f"Frame {i+1} için sonuç gönderilemedi")
            
            # İstekler arası bekleme (sunucu yükünü azaltmak için)
            time.sleep(2)
            
        except Exception as e:
            error_count += 1
            logger.error(f"Frame {i+1} işlenirken hata: {e}")
    
    logger.info(f"Tüm işlemler tamamlandı! Başarılı: {success_count}, Hatalı: {error_count}")

if __name__ == "__main__":
    main() 