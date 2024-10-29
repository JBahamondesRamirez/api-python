from fastapi import APIRouter
from db.schemas.users import *
from crud.user import create_user

router = APIRouter(prefix="/user",
                   tags=["User"])

@router.post("/create_user")
async def create_user_db(user : User):
    users_created = await create_user(user)
    return {"status": "success",
            "user" : users_created}
