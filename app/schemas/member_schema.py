# schemas/member_schema.py

from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


# POST /api/members
class CreateMember(BaseModel):
    name: str
    memberId: str
    memberPw: str
    birth: datetime.date
    phone: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "김회원",
                "memberId": "kimId",
                "memberPw": "kimPw",
                "birth": "2003-01-01",
                "phone": "010-1234-5678",
            }
        }


# PUT /api/members/{memberId}
class UpdateMember(BaseModel):
    name: str
    memberId: str
    memberPw: str
    birth: datetime.date
    phone: str
    aiRecommendAlert: bool
    aiSummary: bool
    aiSave: bool
    imageUrl: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 123,
	            "name": "김회원",
	            "memberId": "kimId",
	            "memberPw": "kimPw", 
	            "birth": "2003-01-01",
	            "phone": "010-1234-5555",
	            "imageUrl": "http://",
	            "aiRecommendAlert": True,
	            "aiSummary": True,
	            "aiSave": True,
	            "createdAt": "2024-02-22T07:47:49.803Z"
            }
        }