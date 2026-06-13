from fastapi import APIRouter, BackgroundTasks
from beanie import PydanticObjectId

import database, random
from models.folder_model import Folder
from models.bookmark_model import Bookmark
from schemas.bookmark_schema import CreateBookmark, UpdateBookmark
from services.ai_service import crawl_summarize_classify

router = APIRouter()

# 백그라운드: AI 요약 + 관심사 자동 분류 → folderId 자동 배정
async def run_summary_and_classify(bookmark_id: PydanticObjectId, url: str):
    summary, interest, image_url = await crawl_summarize_classify(url)  # 수정
    bookmark = await Bookmark.find_one(Bookmark.id == bookmark_id)
    if not bookmark:
        return

    update_data = {}

    if summary:
        update_data[Bookmark.aiSummary] = summary
    if image_url:
        update_data[Bookmark.imageUrl] = image_url  # 추가
    if interest:
        folder = await Folder.find_one(Folder.name == interest)
        if folder:
            update_data[Bookmark.folderId] = folder.id

    if update_data:
        await bookmark.set(update_data)
 
    update_data = {}

    # 요약 저장
    if summary:
        update_data[Bookmark.aiSummary] = summary

     # 관심사 태그 매칭 → 해당 폴더 찾아서 folderId 자동 배정
    async def run_summary_and_classify(bookmark_id: PydanticObjectId, url: str):
        summary, interest = await crawl_summarize_classify(url)
        bookmark = await Bookmark.find_one(Bookmark.id == bookmark_id)
        if not bookmark:
            return

    update_data = {}

    if summary:
        update_data[Bookmark.aiSummary] = summary

    # 수정: summary와 별개로 interest 있으면 무조건 folderId 배정
    if interest:
        folder = await Folder.find_one(Folder.name == interest)
        if folder:
            update_data[Bookmark.folderId] = folder.id

    if update_data:
        await bookmark.set(update_data)

# GET 북마크 검색
@router.get("/bookmarks/search")
async def search_bookmarks(q: str):
    try:
        # $regex로 부분 문자열 검색 (몽고디비 단어 단위 검색 해결, 대소문자 구분 없음)
        bookmarks = await Bookmark.find(
            {"$or": [
                {"aiSummary": {"$regex": q, "$options": "i"}},
                {"url": {"$regex": q, "$options": "i"}},
            ]}
        ).to_list()

        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"'{q}' 검색 결과",
            "data": [
                {
                    "id": str(b.id),
                    "url": b.url,
                    "folderId": str(b.folderId) if b.folderId else None,
                    "imageUrl": b.imageUrl,
                    "aiSummary": b.aiSummary,
                    "like": b.like,
                    "createdAt": b.createdAt,
                }
                for b in bookmarks
            ],
        }
    except Exception as e:
        return {
            "status_code": 500,
            "response_type": "error",
            "description": f"Error occured: {e}",
        }
    
# GET 추천 — 같은 폴더 내 북마크 랜덤 3개 반환
@router.get("/bookmarks/recommend")
async def recommend_bookmarks(folderId: PydanticObjectId):
    try:
        # 같은 폴더 내 북마크 전체 조회
        bookmarks = await Bookmark.find(
            Bookmark.folderId == folderId
        ).to_list()
 
        if not bookmarks:
            return {
                "status_code": 200,
                "response_type": "success",
                "description": "추천할 북마크가 없습니다",
                "data": [],
            }
 
        # 랜덤으로 최대 3개 선택
        recommended = random.sample(bookmarks, min(3, len(bookmarks)))
 
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "추천 북마크",
            "data": [
                {
                    "id": str(b.id),
                    "url": b.url,
                    "folderId": str(b.folderId) if b.folderId else None,
                    "imageUrl": b.imageUrl,
                    "aiSummary": b.aiSummary,
                    "like": b.like,
                    "createdAt": b.createdAt,
                }
                for b in recommended
            ],
        }
    except Exception as e:
        return {
            "status_code": 500,
            "response_type": "error",
            "description": f"Error occured: {e}",
        }

@router.get("/bookmarks/remind")
async def remind_bookmarks():
    try:
        from datetime import datetime, timedelta
        # 1일 이내 기준 날짜
        cutoff = datetime.now() - timedelta(days=1)

        # 1일 미만 된 북마크 전체 조회
        bookmarks = await Bookmark.find(
            Bookmark.createdAt >= cutoff
        ).to_list()

        if not bookmarks:
            return {
                "status_code": 200,
                "response_type": "success",
                "description": "리마인드할 북마크가 없습니다",
                "data": [],
            }

        # 랜덤으로 최대 3개 선택 (접속할 때마다 다르게)
        recommended = random.sample(bookmarks, min(3, len(bookmarks)))

        return {
            "status_code": 200,
            "response_type": "success",
            "description": "오래된 북마크 리마인드",
            "data": [
                {
                    "id": str(b.id),
                    "url": b.url,
                    "folderId": str(b.folderId) if b.folderId else None,
                    "imageUrl": b.imageUrl,
                    "aiSummary": b.aiSummary,
                    "like": b.like,
                    "createdAt": b.createdAt,
                }
                for b in recommended
            ],
        }
    except Exception as e:
        return {
            "status_code": 500,
            "response_type": "error",
            "description": f"Error occured: {e}",
        }

# GET 북마크 상세 조회
@router.get("/bookmarks/{bookmarkId}")
async def get_bookmark(bookmarkId: PydanticObjectId):
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

# GET 북마크 전체 조회
@router.get("/bookmarks")
async def get_bookmarks():

    bookmarks = await Bookmark.find_all().to_list()

    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Bookmarks retrieved successfully",
        "data": bookmarks,
    }

# GET 폴더별 북마크 조회
@router.get("/folders/{folderId}/bookmarks")
async def get_bookmark_by_folder(folderId: PydanticObjectId):
    try:
        bookmarks = await database.retrieve_bookmarks_by_folder(folderId)

        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Bookmarks retrieved successfully",
            "data": bookmarks,
        }
    
    except Exception as e:
        return {
            "status_code": 500,
            "response_type": "error",
            "description": f"Error occured: {e}",
        }

# POST 북마크 생성
@router.post("/folders/{folderId}/bookmarks")
async def create_bookmark(new_bookmark: CreateBookmark, folderId: PydanticObjectId, background_tasks: BackgroundTasks):
    try:
        bookmark = Bookmark(**new_bookmark.model_dump())
        resp = await database.add_bookmark(bookmark)
        background_tasks.add_task(
            run_summary_and_classify,
            PydanticObjectId(resp["id"]),
            resp["url"]
        )
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
    
# PUT 북마크 수정
@router.put("/bookmarks/{bookmarkId}")
async def update_bookmark(bookmarkId: PydanticObjectId, data: UpdateBookmark):
    updated = await database.update_bookmark(
        bookmarkId,
        {k: v for k, v in data.model_dump().items() if v is not None}
    )
    if updated:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Bookmark updated successfully",
            "data": updated,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "잘못된 요청입니다",
    }
    
# DELETE 북마크 삭제
@router.delete("/bookmarks/{bookmarkId}")
async def delete_bookmark(bookmarkId: PydanticObjectId):
    deleted = await database.delete_bookmark(bookmarkId)
    if deleted:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Bookmark deleted successfully",
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "잘못된 요청입니다",
    }