from fastapi import APIRouter, BackgroundTasks

import database
from models.bookmark_model import Bookmark
from schemas.bookmark_schema import CreateBookmark, UpdateBookmark
from services.ai_service import crawl_and_summarize

router = APIRouter()

# 백그라운드에서 요약 실행 후 DB 업데이트
async def run_summary(bookmark_id: str, url: str):
    summary = await crawl_and_summarize(url)
    if summary:
        bookmark = await Bookmark.get(bookmark_id)
        if bookmark:
            await bookmark.set({Bookmark.aiSummary: summary})

# @router.get("/bookmarks/{bookmarkId}")
# async def get_bookmark(bookmarkId: int):
#     bookmark = await database.retrieve_bookmark(bookmarkId)
#     if bookmark:
#         return {
#             "status_code": 200,
#             "response_type": "success",
#             "description": "Bookmark retrieved successfully",
#             "data": bookmark,
#         }

#     return {
#         "status_code": 404,
#         "response_type": "error",
#         "description": "잘못된 요청입니다",
#     }

@router.get("/bookmarks")
async def get_bookmarks():

    bookmarks = await Bookmark.find_all().to_list()

    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Bookmarks retrieved successfully",
        "data": bookmarks,
    }

# 북마크 생성
@router.post("/bookmarks")
async def create_bookmark(new_bookmark: CreateBookmark):
    try:
        summary = await crawl_and_summarize(new_bookmark.url)

        bookmark = Bookmark(**new_bookmark.model_dump(),  aiSummary=summary)
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