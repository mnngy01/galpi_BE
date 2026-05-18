# main.py

from fastapi import FastAPI
from api.member_api import router as member_router

app = FastAPI()

"""
@app.get("/")
def read_root():
    return {"Message": "World"}
"""

app.include_router(member_router)