# schemas/bookmark_schema.py

from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


# POST /api/folders/{folderId}/bookmarks
class createBookmark(BaseModel):
    id: int
    url: str
    folderId: int
    imageUrl: str
    aiSummary: str
    like: int = 0
    createdAt: datetime = Field(default_factory = datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 123,
                "url": "string",
                "folderId": 5,
                "imageUrl": "string",
                "aiSummary": "string",
                "like": 0,
                "createdAt": "2024-02-22T07:47:49.803Z"
            }
        }


# PUT /api/bookmarks/{bookmarkId}
class updateBookmark(BaseModel):
    url: str
    folderId: int
    imageUrl: str
    like: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "url": "string",
                "folderId": 5,
                "imageUrl": "string",
                "like": 0,
            }
        }