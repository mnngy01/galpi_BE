# schemas/folder_schema.py

from pydantic import BaseModel
from typing import Optional, Any
from beanie import PydanticObjectId


# POST /folders
class CreateFolder(BaseModel):
    name: str
    higherFolderId: Optional[PydanticObjectId]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "여행 장소",
                "higherFolderId": "string",
            }
        }


# PUT /folders/{folderId}
class UpdateFolder(BaseModel):
    name: str
    higherFolderId: Optional[PydanticObjectId]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "강릉 여행 북마크",
                "higherFolderId": "string",
            }
        }
