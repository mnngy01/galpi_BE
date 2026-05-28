from fastapi import APIRouter
from beanie import PydanticObjectId

import database
from models.folder_model import Folder
from schemas.folder_schema import CreateFolder, UpdateFolder


router = APIRouter()


@router.get("/folders/{folderId}")
async def get_folder(folderId: str):
    folder = await database.retrieve_folder(folderId)
    if folder:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Folder retrieved successfully",
            "data": folder,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "잘못된 요청입니다",
    }


@router.post("/folders")
async def create_folder(new_folder: CreateFolder):

    try:
        folder = Folder(**new_folder.model_dump())
        response = await database.add_folder(folder)
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Folder created successfully",
            "data": response,
        }
    except Exception as e:
        print(e)
        return {
            "status_code": 500,
            "response_type": "error",
            "description": f"Error occured: {e}",
        }