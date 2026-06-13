# app/api/auth_api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.member_model import Member

router = APIRouter()

class LoginRequest(BaseModel):
    loginId: str
    loginPw: str


@router.post("/auth/login")
async def login(request: LoginRequest):

    member = await Member.find_one(Member.loginId == request.loginId)

    if not member or member.loginPw != request.loginPw:
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 잘못 입력되었습니다")

    return {
        "status_code": 200,
        "response_type": "success",
        "description": "로그인 성공",
        "data": {
            "memberId": str(member.id),
            "name": member.name,
        }
    }