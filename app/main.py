# main.py

from fastapi import FastAPI
from api.member_api import router as member_router
from api.folder_api import router as folder_router
from api.bookmark_api import router as bookmark_router

app = FastAPI()

"""
@app.get("/")
def read_root():
    return {"Message": "World"}
"""

app.include_router(member_router)
app.include_router(folder_router)
app.include_router(bookmark_router)