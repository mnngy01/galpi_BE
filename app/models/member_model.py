# member_model.py

from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime, date

class Member(Document):
    name: str
    loginId: str
    loginPw: str
    birth: date
    phone: str
    aiRecommendAlert: bool = True
    aiSummary: bool = True
    aiSave: bool = True
    imageUrl: str = None
    createdAt: datetime = Field(default_factory = datetime.now)

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