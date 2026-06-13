# schemas/bookmark_schema.py

from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime
from beanie import PydanticObjectId

# POST /bookmarks
class CreateBookmark(BaseModel):
    url: str

    class Config:
        json_schema_extra = {
            "example": {
                "url": "string",
            }
        }


# PUT /bookmarks/{bookmarkId}
class UpdateBookmark(BaseModel):
    url: str
    folderId: Optional[PydanticObjectId] = None
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