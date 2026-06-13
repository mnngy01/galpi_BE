# schemas/member_schema.py

from pydantic import BaseModel
from typing import Optional, Any, List
from datetime import datetime, date

# 허용된 관심사 태그 목록 (고정값)
VALID_INTERESTS = ["차(tea)", "아웃도어", "아이와 함께", "반려", "건축", "해외여행", "맛집", "인테리어"]

# POST /api/members
class CreateMember(BaseModel):
    name: str
    loginId: str
    loginPw: str
    birth: date
    phone: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "김회원",
                "loginId": "kimId",
                "loginPw": "kimPw",
                "birth": "2003-01-01",
                "phone": "010-1234-5678",
            }
        }


# PUT /api/members/{memberId}
class UpdateMember(BaseModel):
    name: str
    loginId: str
    loginPw: str
    birth: date
    phone: str
    aiRecommendAlert: bool
    aiSummary: bool
    aiSave: bool
    imageUrl: str

    class Config:
        json_schema_extra = {
            "example": {
                # "id": 123,
	            "name": "김회원",
	            "loginId": "kimId",
	            "loginPw": "kimPw", 
	            "birth": "2003-01-01",
	            "phone": "010-1234-5555",
	            "imageUrl": "http://",
	            "aiRecommendAlert": True,
	            "aiSummary": True,
	            "aiSave": True,
                "imageUrl": "photo.com",
            }
        }

# POST /members/{memberId}/interests — 관심사 선택 (회원가입 후 첫 로그인 화면)
class SetInterests(BaseModel):
    interests: List[str]  # 선택한 관심사 목록 (예: ["차", "맛집"])
 
    class Config:
        json_schema_extra = {
            "example": {
                "interests": ["차", "맛집", "아웃도어"]
            }
        }

# GET /api/member/{memberId}
class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any] = None

    class Config:
        json_schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": "Sample data",
            }
        }