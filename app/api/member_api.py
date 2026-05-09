# member_api

from fastapi import APIRouter
from database import database
from app.models.member_model import Member
from bson import ObjectId

router = APIRouter()
