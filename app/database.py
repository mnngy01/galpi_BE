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