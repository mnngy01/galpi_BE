# bookmark_model.py

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from pymongo import IndexModel, TEXT
from datetime import datetime
from typing import Optional

class Bookmark(Document):
    url: str
    folderId: Optional[PydanticObjectId] = None
    imageUrl: Optional[str] = None
    aiSummary: Optional[str] = None
    like: bool = False
    createdAt: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://~~~",
                "folderId": 1,
                "imageUrl": "https://~~~",
                "aiSummary": "강릉 여행 묵호 바다 맛집",
                "like": False,
                "createdAt": "%Y-%m-%d %H:%M:%S",
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