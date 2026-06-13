from fastapi import APIRouter, Body, HTTPException
from bson import ObjectId
from beanie import PydanticObjectId

import database
from models.folder_model import Folder
from models.member_model import Member
from schemas.member_schema import CreateMember, UpdateMember, SetInterests, Response, VALID_INTERESTS


router = APIRouter()

@router.get("/members/{memberId}", response_description="Member Retrieved", response_model=Response)
async def get_member(memberId: PydanticObjectId):
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


@router.put("/members/{memberId}", response_model=Response)
async def update_member(memberId: PydanticObjectId, data: UpdateMember):
    updated = await database.update_member(
        memberId,
        {k: v for k, v in data.model_dump().items() if v is not None}
    )
    if updated:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Member updated successfully",
            "data": updated,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "잘못된 요청입니다",
    }
 
@router.delete("/members/{memberId}", response_model=Response)
async def delete_member(memberId: PydanticObjectId):
    deleted = await database.delete_member(memberId)
    if deleted:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Member deleted successfully",
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "잘못된 요청입니다",
    }

# POST 관심사 선택 + 폴더 자동 생성
# 회원가입 후 첫 로그인 시 관심사 선택 화면에서 호출
@router.post("/members/{memberId}/interests", response_model=Response)
async def set_interests(memberId: PydanticObjectId, data: SetInterests):
    try:
        # 유효하지 않은 관심사 필터링
        valid = [i for i in data.interests if i in VALID_INTERESTS]
        if not valid:
            return {
                "status_code": 400,
                "response_type": "error",
                "description": "관심사가 없습니다",
            }
 
        # 멤버 찾기
        member = await Member.find_one(Member.id == memberId)
        if not member:
            return {
                "status_code": 404,
                "response_type": "error",
                "description": "존재하지 않는 회원입니다",
            }
 
        # 관심사 저장
        await member.set({Member.interests: valid})
 
        # 선택한 관심사 이름으로 자동 생성
        # 이미 같은 이름의 폴더가 있으면 생성 안 함
        created_folders = []
        for interest in valid:
            existing = await Folder.find_one(Folder.name == interest)
            if not existing:
                folder = Folder(name=interest, higherFolderId=None)
                await folder.insert()
                created_folders.append(interest)

        # 관심사 폴더 생성 후 기타 폴더도 자동 생성
        existing_etc = await Folder.find_one(Folder.name == "기타")
        if not existing_etc:
            folder = Folder(name="기타", higherFolderId=None)
            await folder.insert()
            created_folders.append("기타")
 
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"관심사 저장 및 폴더 생성 완료",
            "data": {
                "interests": valid,
                "created_folders": created_folders,
            }
        }
    except Exception as e:
        return {
            "status_code": 500,
            "response_type": "error",
            "description": f"Error occured: {e}",
        }