# folder_model.py

from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime

class Folder(Document):
    name: str
    higherFolderId: int
    createdAt: datetime = Field(default_factory = datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "여행 정보",
                "higherFolderId": 1,
                "createdAt": "2024-02-22T07:47:49.8032",
            }
        }
    
    class Settings:
        name = "folder"