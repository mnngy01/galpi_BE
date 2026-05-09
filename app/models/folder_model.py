# folder_model.py

from beanie import Document
from pydantic import BaseModel
from datetime import datetime

class Folder(Document):
    name: str
    higherFolderId: int
    createdAt: datetime = datetime.now()

    class Config:
        json_schema_extra = {
            "example": {
                "name": "여행 정보",
                "higherFolderId": 1,
                "createdAt": "%Y-%m-%d %H:%M:%S",
            }
        }
    
    class Settings:
        name = "folder"