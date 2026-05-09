# bookmark_schema.py

from pydantic import BaseModel
from datetime import datetime

class Bookmark(BaseModel):
    url: str
    folderId: int
    imageUrl: str
    aiSummary: str
    like: bool = False
    createdAt: datetime = datetime.now()