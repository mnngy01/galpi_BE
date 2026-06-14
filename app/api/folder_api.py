from fastapi import APIRouter
from beanie import PydanticObjectId

import database
from models.folder_model import Folder
from schemas.folder_schema import CreateFolder, UpdateFolder


router = APIRouter()

# GET 폴더 전체 조회
@router.get("/folders")
async def get_folders():
    folders = await database.retrieve_all_folders()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Folders retrieved successfully",
        "data": folders,
    }

# GET 폴더 (1개) 상세 조회
@router.get("/folders/{folderId}")
async def get_folder(folderId: PydanticObjectId):
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

# POST 폴더 등록
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

# PUT 폴더 수정
@router.put("/folders/{folderId}")
async def update_folder(folderId: PydanticObjectId, data: UpdateFolder):
    updated = await database.update_folder(
        folderId,
        {k: v for k, v in data.model_dump().items() if v is not None}
    )
    if updated:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Folder updated successfully",
            "data": updated,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "잘못된 요청입니다",
    }
 
 # DELETE 폴더 삭제
@router.delete("/folders/{folderId}")
async def delete_folder(folderId: PydanticObjectId):
    deleted = await database.delete_folder(folderId)
    if deleted:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Folder deleted successfully",
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "잘못된 요청입니다",
    }