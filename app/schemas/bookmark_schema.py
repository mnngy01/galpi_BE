# schemas/bookmark_schema.py

from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime
from beanie import PydanticObjectId

# POST /api/folders/{folderId}/bookmarks
class CreateBookmark(BaseModel):
    # id: int, 몽고db가 자동으로 id 만들어줌
    url: str
    folderId: Optional[PydanticObjectId] = None
    # imageUrl: Optional[str] = None  # 서버 자동생성
    # aiSummary: str # 서버 자동생성
    # like: int = 0
    # createdAt: datetime = Field(default_factory = datetime.now) # 서버 자동생성

    class Config:
        json_schema_extra = {
            "example": {
                # "id": 자동생성
                "url": "string",
                "folderId": "string",
                # "imageUrl": "string",
                # "aiSummary": "string",
                # "like": 0,
                # "createdAt": "2024-02-22T07:47:49.803Z"
            }
        }


# PUT /api/bookmarks/{bookmarkId}
class UpdateBookmark(BaseModel):
    folderId: int
    imageUrl: str
    like: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "url": "string",
                "folderId": "string",
                "imageUrl": "string",
                "like": 0,
            }
        }