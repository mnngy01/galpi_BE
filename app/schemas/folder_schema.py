# folder_schema.py

from pydantic import BaseModel
from datetime import datetime

class Folder(BaseModel):
    name: str
    higherFolderId: int
    createdAt: datetime = datetime.now()