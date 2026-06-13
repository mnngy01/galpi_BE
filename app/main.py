# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

from api.member_api import router as member_router
from api.folder_api import router as folder_router
from api.bookmark_api import router as bookmark_router
from api.auth_api import router as auth_router 

from models.member_model import Member
from models.folder_model import Folder
from models.bookmark_model import Bookmark

import os



# mongoDB + Beanie 연결
# "mongodb+srv://minji_db_user:minji_pw001@galpi.qqwnswr.mongodb.net/?retryWrites=true&w=majority&tls=true"
@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(
        os.getenv("MONGODB_URI")
    )

    await init_beanie(
        database = client.galpi,
        document_models = [
            Member,
            Folder,
            Bookmark
            ]
    )

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# router 등록
app.include_router(member_router)
app.include_router(folder_router)
app.include_router(bookmark_router)
app.include_router(auth_router) 