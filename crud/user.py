from db.schemas.users import *
from db.client import db_client
from fastapi import HTTPException
from datetime import datetime

async def create_user(user: User):
    user_exist = db_client.users.find_one({"_id": user.id})  
    if user_exist:
        raise HTTPException(status_code=400, detail="El usuario ya existe.")

    user_model = user.model_dump(by_alias=True)

    user_db_model = UserDb(
        _id=user_model["_id"], 
        name=user_model["name"],
        email=user_model["email"],
        email_verified=user_model["email_verified"],
        picture=user_model["picture"],
        auth_method=user_model["auth_method"],
        created_at=datetime.now(), 
        updated_at=datetime.now(), 
        account_blocked=False
    )

    result = db_client.users.insert_one(user_db_model.model_dump(by_alias=True))
    created_user = db_client.users.find_one({"_id": result.inserted_id})
    return created_user

