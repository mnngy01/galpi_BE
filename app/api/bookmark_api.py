from fastapi import APIRouter
from beanie import PydanticObjectId

import database
from models.bookmark_model import Bookmark
from schemas.bookmark_schema import CreateBookmark, UpdateBookmark


router = APIRouter()


@router.get("/bookmarks/{bookmarkId}")
async def get_bookmark(bookmarkId: int):
    bookmark = await database.retrieve_bookmark(bookmarkId)
    if bookmark:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Bookmark retrieved successfully",
            "data": bookmark,
        }

    return {
        "status_code": 404,
        "response_type": "error",
        "description": "잘못된 요청입니다",
    }


# 북마크 생성
@router.post("/bookmarks")
async def create_bookmark(new_bookmark: CreateBookmark):
    try:
        bookmark = Bookmark(**new_bookmark.model_dump())
        resp = await database.add_bookmark(bookmark)
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Bookmark created successfully",
            "data": resp,
        }
    except Exception as e:
        print(e)
        return {
            "status_code": 500,
            "response_type": "error",
            "description": f"Error occured: {e}",
        }