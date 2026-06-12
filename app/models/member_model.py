# member_model.py

from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List
from pymongo import IndexModel, TEXT

class Member(Document):
    name: str
    loginId: str
    loginPw: str
    birth: date
    phone: str
    aiRecommendAlert: bool = True
    aiSummary: bool = True
    aiSave: bool = True
    imageUrl: Optional[str] = None
    interests: List[str] = []  # 추가: 관심사 목록 저장 (예: ["차", "맛집"])
    createdAt: datetime = Field(default_factory=datetime.now)

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
                "createdAt": "%Y-%m-%d %H:%M:%S"
            }
        }

    class Settings:
        name = "bookmark"
        indexes = [
            IndexModel(
                [("url", TEXT), ("aiSummary", TEXT)],
                default_language="none"  # 한국어 포함 모든 언어 검색
            )
        ]