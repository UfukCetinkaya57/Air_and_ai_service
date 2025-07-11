from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import os

from models import FrameData
from config import settings

app = FastAPI(title="TÜBİTAK Yarışma Sunucusu", version="1.0.0")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# IP kontrolü için middleware
async def verify_ip(request: Request):
    """Şartnamede belirtilen IP kısıtlaması kontrolü"""
    client_ip = request.client.host
    if client_ip not in settings.ALLOWED_IPS:
        raise HTTPException(
            status_code=403, 
            detail=f"IP adresi {client_ip} yarışmaya katılım için yetkilendirilmemiş"
        )
    return client_ip

# Örnek veri - gerçek uygulamada veritabanından gelecek
sample_frames_data = [
    {
        "url": f"{settings.FRAMES_BASE_URL}/3598/",
        "image_url": "/ljfgpemcvkmuadhxabwn_V2_1/frame_000000.jpg",
        "video_name": "ljfgpemcvkmuadhxabwn_V2_1",
        "session": f"{settings.SESSION_BASE_URL}/2/",
        "translation_x": 0.02,
        "translation_y": 0.01,
        "translation_z": 0.03,
        "health_status": 1
    },
    {
        "url": f"{settings.FRAMES_BASE_URL}/4787/",
        "image_url": "/ljfgpemcvkmuadhxabwn_V2_1/frame_000004.jpg",
        "video_name": "ljfgpemcvkmuadhxabwn_V2_1",
        "session": f"{settings.SESSION_BASE_URL}/2/",
        "translation_x": 0.01,
        "translation_y": 0.02,
        "translation_z": 0.01,
        "health_status": 1
    },
    {
        "url": f"{settings.FRAMES_BASE_URL}/3916/",
        "image_url": "/ljfgpemcvkmuadhxabwn_V2_1/frame_000008.jpg",
        "video_name": "ljfgpemcvkmuadhxabwn_V2_1",
        "session": f"{settings.SESSION_BASE_URL}/2/",
        "translation_x": "NaN",
        "translation_y": "NaN",
        "translation_z": "NaN",
        "health_status": 0
    }
]

@app.get("/")
async def root():
    """Ana sayfa"""
    return {
        "message": "TÜBİTAK Havacılık ve Yapay Zeka Yarışması Sunucusu",
        "version": "1.0.0",
        "status": "aktif"
    }

@app.get("/frames/", response_model=List[FrameData])
async def get_frames(client_ip: str = Depends(verify_ip)):
    """
    Şartnamede belirtilen görüntü karelerinin listesini döndürür.
    Yarışmacılar bu endpoint'i kullanarak işleyecekleri görüntü bilgilerini alır.
    """
    return sample_frames_data

@app.get("/frames/{frame_id}/")
async def get_frame(frame_id: int, client_ip: str = Depends(verify_ip)):
    """Belirli bir frame ID'si için detay bilgisi"""
    # Burada veritabanından frame detayları getirilecek
    return {
        "url": f"{settings.FRAMES_BASE_URL}/{frame_id}/",
        "message": f"Frame {frame_id} detayları"
    }

@app.get("/session/{session_id}/")
async def get_session(session_id: int, client_ip: str = Depends(verify_ip)):
    """Oturum bilgilerini döndürür"""
    return {
        "session_url": f"{settings.SESSION_BASE_URL}/{session_id}/",
        "session_id": session_id,
        "status": "aktif"
    }

@app.post("/results/")
async def submit_results(
    frames: List[FrameData], 
    client_ip: str = Depends(verify_ip)
):
    """
    Şartnamede belirtilen formatta yarışmacıların sonuçlarını alır.
    Sadece frame listesi şeklinde gönderilmelidir.
    """
    
    # Sonuçları kaydet (gerçek uygulamada veritabanına kaydedilecek)
    print(f"IP {client_ip}'den sonuç alındı:")
    print(f"Gönderilen frame sayısı: {len(frames)}")
    
    for i, frame in enumerate(frames):
        print(f"Frame {i+1}: {frame.url}")
        print(f"  Video: {frame.video_name}")
        print(f"  Health Status: {frame.health_status}")
    
    # Başarılı yanıt döndür
    return {
        "id": 22246,
        "user": "http://localhost/users/4/",
        "frame": "http://localhost/frames/4000/",
        "detected_objects": [
            {
                "cls": "http://localhost/classes/1/",
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

@app.get("/health/")
async def health_check():
    """Sunucu sağlık kontrolü"""
    return {
        "status": "sağlıklı",
        "server": f"{settings.HOST}:{settings.PORT}",
        "api_version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT) 