# app/api/auth_api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.member_model import Member

router = APIRouter()


# 로그인 요청 형식
class LoginRequest(BaseModel):
    loginId: str
    loginPw: str


# POST /auth/login — 로그인
@router.post("/auth/login")
async def login(request: LoginRequest):

    # DB에서 loginId로 회원 찾기
    member = await Member.find_one(Member.loginId == request.loginId)

    # 회원이 없거나 비밀번호 틀리면 에러
    if not member or member.loginPw != request.loginPw:
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 잘못 입력되었습니다")

    # 로그인 성공 → memberId 반환
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "로그인 성공",
        "data": {
            "memberId": str(member.id),
            "name": member.name,
        }
    }