# member_schema.py

from pydantic import BaseModel
from datetime import datetime

class Member(BaseModel):
    name: str
    loginId: str
    loginPw: str
    birth: datetime = datetime.date()
    phone: int
    aiRecommendAlert: bool = True
    aiSummary: bool = True
    aiSave: bool = True
    imageUrl: str
    createdAt: datetime = datetime.now()