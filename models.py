from pydantic import BaseModel, RootModel
from typing import List, Union, Optional

class FrameData(BaseModel):
    """Şartnamede belirtilen görüntü karesi veri modeli"""
    url: str
    image_url: str
    video_name: str
    session: str
    translation_x: Union[float, str]  # "NaN" olabilir
    translation_y: Union[float, str]  # "NaN" olabilir
    translation_z: Union[float, str]  # "NaN" olabilir
    health_status: int  # Şartnamede health_status yazıyor

class DetectedObject(BaseModel):
    """Tespit edilen nesne modeli"""
    cls: str  # "0", "1", "2", "3"
    landing_status: str  # "-1", "0", "1"
    top_left_x: int
    top_left_y: int
    bottom_right_x: int
    bottom_right_y: int

class DetectedTranslation(BaseModel):
    """Tespit edilen yer değiştirme modeli"""
    translation_x: float
    translation_y: float
    translation_z: float

class ResultSubmission(RootModel[List[FrameData]]):
    """Yarışmacıların göndereceği sonuç modeli"""
    pass 