# bookmark_model.py

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Bookmark(Document):
    url: str
    folderId: Optional[PydanticObjectId]
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
            [("url", "text"), ("aiSummary", "text")]
        ]