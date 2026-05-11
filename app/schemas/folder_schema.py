# schemas/folder_schema.py

from pydantic import BaseModel
from typing import Optional, Any


# POST /api/folders
class CreateFolder(BaseModel):
    name: str
    higherFolderId: int

    class Config:
        json_schema_extra = {
            "example": {
                "name": "여행 장소",
                "higherFolderId": 1,
            }
        }

# PUT /api/folders/{folderId}
class UpdateFolder(BaseModel):
    id: int
    name: str
    higherFolderId: 1

    class Config:
        json_schema_extra = {
            "example": {
                "id": 2,
                "name": "강릉 여행 북마크",
                "higherFolderId": 1,
            }
        }
