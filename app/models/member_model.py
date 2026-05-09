# member_model.py

from beanie import Document
from pydantic import BaseModel
from datetime import datetime

class Member(Document):
    name: str
    loginId: str
    loginPw: str
    birth: datetime = datetime.date()
    phone: int
    aiRecommendAlert: bool = True
    aiSummary: bool = True
    aiSave: bool = True
    imageUrl: str
    createdAt: datetime = datetime.now()

    class Config:
        json_schema_extra = {
            "example": {
                "name": "오또잉",
                "loginId": "autoing22",
                "loginPw": "autoingPw",
                "birth": "%Y-%m-%d",
                "phone": "01012345678",
                "aiRecommendAlert": True,
                "aiSummary": True,
                "aiSave": True,
                "imageUrl": "url",
                "createdAt": "%Y-%m-%d %H:%M:%S",
            }
        }

    class Settings:
        name = "member"