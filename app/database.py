# database.py
from typing import List, Union
from beanie import PydanticObjectId

from motor.motor_asyncio import AsyncIOMotorClient
# from configrations import db

from models.member_model import Member
from models.bookmark_model import Bookmark
from models.folder_model import Folder

#MONGO_DETAILS = "mongodb://localhost:27017"

#client = AsyncIOMotorClient(MONGO_DETAILS)
#database = client.mydatabase

member_collection = Member
Bookmark_collection = Bookmark
Folder_collection = Folder


# GET member
async def retrieve_member(memberId: PydanticObjectId) -> dict:
    member = await member_collection.find_one(Member.id == memberId)  # 수정: get → find_one
    if member:
        return {
            "id": str(member.id),
            "name": member.name,
            "loginId": member.loginId,
            "loginPw": member.loginPw,
            "birth": member.birth,
            "phone": member.phone,
            "aiRecommendAlert": member.aiRecommendAlert,
            "aiSummary": member.aiSummary,
            "aiSave": member.aiSave,
            "imageUrl": member.imageUrl,
            "createdAt": member.createdAt,
        }


# POST member
async def add_member(new_member: Member) -> Member:
    member = await new_member.insert()
    return {
        "id": str(member.id),
	    "name": member.name,
	    "loginId": member.loginId,
	    "loginPw": member.loginPw, 
	    "birth": member.birth,
	    "phone": member.phone,
	    "createdAt": member.createdAt,
    }

# PUT member  # 추가
async def update_member(memberId: PydanticObjectId, data: dict) -> dict:
    member = await member_collection.find_one(Member.id == memberId)
    if not member:
        return None
    await member.set(data)
    return {
        "id": str(member.id),
        "name": member.name,
        "loginId": member.loginId,
        "birth": member.birth,
        "phone": member.phone,
        "imageUrl": member.imageUrl,
        "interests": member.interests,
    }

# DELETE member  # 추가
async def delete_member(memberId: PydanticObjectId) -> bool:
    member = await member_collection.find_one(Member.id == memberId)
    if not member:
        return False
    await member.delete()
    return True

# GET folder
async def retrieve_folder(folderId: PydanticObjectId) -> dict:
    folder = await Folder_collection.find_one(Folder.id == folderId)  # 수정: get → find_one
    if folder:
        return {
            "id": str(folder.id),
            "name": folder.name,
            "higherFolderId": folder.higherFolderId,
            "createdAt": folder.createdAt,
        }

# POST folder
async def add_folder(new_folder: Folder) -> dict:
    folder = await new_folder.insert()
    return {
        "id": str(folder.id),
        "name": folder.name,
        "higherFolderId": folder.higherFolderId,
        "createdAt": folder.createdAt,
    }

# GET folder 전체 목록  # 추가
async def retrieve_all_folders() -> list:
    folders = await Folder_collection.find_all().to_list()
    return [
        {
            "id": str(f.id),
            "name": f.name,
            "higherFolderId": str(f.higherFolderId) if f.higherFolderId else None,
            "createdAt": f.createdAt,
        }
        for f in folders
    ]

# PUT folder  # 추가
async def update_folder(folderId: PydanticObjectId, data: dict) -> dict:
    folder = await Folder_collection.find_one(Folder.id == folderId)
    if not folder:
        return None
    await folder.set(data)
    return {
        "id": str(folder.id),
        "name": folder.name,
        "higherFolderId": str(folder.higherFolderId) if folder.higherFolderId else None,
        "createdAt": folder.createdAt,
    }
 
# DELETE folder  # 추가
async def delete_folder(folderId: PydanticObjectId) -> bool:
    folder = await Folder_collection.find_one(Folder.id == folderId)
    if not folder:
        return False
    await folder.delete()
    return True

# GET bookmark
async def retrieve_bookmark(bookmarkId: PydanticObjectId) -> dict:
    bookmark = await Bookmark_collection.find_one(Bookmark.id == bookmarkId)  # 수정: get → find_one
    if bookmark:
        return {
            "id": str(bookmark.id),
            "url": bookmark.url,
            "folderId": str(bookmark.folderId) if bookmark.folderId else None,
            "imageUrl": bookmark.imageUrl,
            "aiSummary": bookmark.aiSummary,
            "like": bookmark.like,
            "createdAt": bookmark.createdAt,
        }
    

# GET folders/{folderId}/bookmarks 폴더별 북마크 조회
async def retrieve_bookmarks_by_folder(folderId: PydanticObjectId):
    bookmarks = await Bookmark.find(
        Bookmark.folderId == folderId
    ).to_list()

    return [
        {
            "id": str(bookmark.id),
            "url": bookmark.url,
            "folderId": str(bookmark.folderId) if bookmark.folderId else None,
            "imageUrl": bookmark.imageUrl,
            "aiSummary": bookmark.aiSummary,
            "like": bookmark.like,
            "createdAt": bookmark.createdAt,
        }
        for bookmark in bookmarks
    ]



# POST bookmark
async def add_bookmark(new_bookmark: Bookmark) -> dict:
    bookmark = await new_bookmark.insert()
    return {
        "id": str(bookmark.id),
        "url": bookmark.url,
        "folderId": str(bookmark.folderId) if bookmark.folderId else None,
        "imageUrl": bookmark.imageUrl,
        "aiSummary": bookmark.aiSummary,
        "like": bookmark.like,
        "createdAt": bookmark.createdAt,
    }

# PUT bookmark  # 추가
async def update_bookmark(bookmarkId: PydanticObjectId, data: dict) -> dict:
    bookmark = await Bookmark_collection.find_one(Bookmark.id == bookmarkId)
    if not bookmark:
        return None
    await bookmark.set(data)
    return {
        "id": str(bookmark.id),
        "url": bookmark.url,
        "folderId": str(bookmark.folderId) if bookmark.folderId else None,
        "imageUrl": bookmark.imageUrl,
        "aiSummary": bookmark.aiSummary,
        "like": bookmark.like,
        "createdAt": bookmark.createdAt,
    }
 
# DELETE bookmark  # 추가
async def delete_bookmark(bookmarkId: PydanticObjectId) -> bool:
    bookmark = await Bookmark_collection.find_one(Bookmark.id == bookmarkId)
    if not bookmark:
        return False
    await bookmark.delete()
    return True
 