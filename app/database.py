# database.py
from typing import List, Union

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import PydanticObjectId
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
async def retrieve_member(memberId: PydanticObjectId) -> Member:
    member = await member_collection.get(memberId)
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
async def retrieve_folder(folderId: str):
    folder = await Folder_collection.get(folderId)
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
async def retrieve_bookmark(bookmarkId: str):
    bookmark = await Bookmark_collection.get(bookmarkId)
    if bookmark:
        return {
            "id": str(bookmark.id),
            "url": bookmark.url,
            "folderId": bookmark.folderId,
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
        "folderId": bookmark.folderId,
        "imageUrl": bookmark.imageUrl,
        "aiSummary": bookmark.aiSummary,
        "like": bookmark.like,
        "createdAt": bookmark.createdAt,
    }