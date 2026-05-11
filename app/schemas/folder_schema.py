# schemas/folder_schema.py

from pydantic import BaseModel
from typing import Optional, Any


# POST /api/folders
class RegisterFolder(BaseModel):
    name: str
    higherFolderId: int

    class Config:
        json_schema_extra = {
            "example": {
                "name": "여행 장소",
                "higherFolderId": 1,
            }
        }