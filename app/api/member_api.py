# router/member_api

from fastapi import APIRouter, Body, HTTPException
from bson import ObjectId
# from configrations import collection
from beanie import PydanticObjectId

import database
from models.member_model import Member
from schemas.member_schema import CreateMember, UpdateMember, Response


router = APIRouter()


@router.get("/members/{memberId}", response_description="Member Retrieved", response_model=Response)
async def get_member(memberId: int):
    member = await database.retrieve_member(memberId)
    if member:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Member data retrieved successfully",
            "data": member,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "잘못된 요청입니다",
    }


@router.post("/members", response_description="Member data added into database", response_model=Response)
async def create_member(new_member: CreateMember):
    try:
        member = Member(**new_member.model_dump())
        resp = await database.add_member(member)
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Member created successfully",
            "data": resp
        }
    except Exception as e:
        return {
            "status_code": 500,
            "response_type": "error",
            "description": f"Some error occured {e}",
        }
