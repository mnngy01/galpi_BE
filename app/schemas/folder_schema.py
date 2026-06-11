# schemas/folder_schema.py

from pydantic import BaseModel
from typing import Optional, Any
from beanie import PydanticObjectId


# POST /api/folders
class CreateFolder(BaseModel):
    name: str
    higherFolderId: Optional[PydanticObjectId]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "여행 장소",
                "higherFolderId": 1,
            }
        }


# PUT /api/folders/{folderId}
class UpdateFolder(BaseModel):
    # id: int # URL 경로에서 직접 받음
    name: str
    higherFolderId: int = 1

    class Config:
        json_schema_extra = {
            "example": {
                "id": 2,
                "name": "강릉 여행 북마크",
                "higherFolderId": 1,
            }
        }
