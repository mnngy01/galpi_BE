# bookmark_model.py

from beanie import Document
from pydantic import BaseModel
from datetime import datetime

class Bookmark(Document):
    url: str
    folderId: int
    imageUrl: str
    aiSummary: str
    like: bool = False
    createdAt: datetime = datetime.now()

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