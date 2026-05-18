# schemas/member_schema.py

from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime, date


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
                "id": 123,
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